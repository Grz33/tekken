import math

from keras.src.losses import Huber
from keras.models import Sequential
from keras.layers import Conv2D, Dense, Flatten
from keras.optimizers import *
from .Screen import IMAGE_HEIGHT, IMAGE_WIDTH

IMAGE_STACK = 2
LEARNING_RATE = 0.00025
MEMORY_CAPACITY = 400000
BATCH_SIZE = 32
GAMMA = 0.99
MAX_EPSILON = 1
MIN_EPSILON = 0.1
EXPLORATION_STOP = 500000
LAMBDA = - math.log(0.01) / EXPLORATION_STOP
UPDATE_TARGET_FREQUENCY = 10000

class Model:

    def __init__(self, input_shape, actioncnt):
        self.actionCnt = actioncnt
        self.input_shape = input_shape
        self.model = self.create_model()
        self.target_model = self.create_model()

    def create_model(self):
        model = Sequential()
        model.add(Conv2D(32, (8, 8), strides=(4, 4), activation='relu', input_shape=(self.input_shape),
                         data_format='channels_first'))
        model.add(Conv2D(64, (4, 4), strides=(2, 2), activation='relu'))
        model.add(Conv2D(64, (3, 3), activation='relu'))
        model.add(Flatten())
        model.add(Dense(units=512, activation='relu'))
        model.add(Dense(units=self.actionCnt, activation='linear'))

        opt = RMSprop(learning_rate=0.0005)
        model.compile(loss=Huber(), optimizer=opt)

        return model

    def train(self, x, y):
        self.model.fit(x, y, batch_size=32, epochs=1, verbose=0)

    def predict(self, state, target=False):
        if target:
            return self.target_model.predict(state)
        else:
            return self.model.predict(state)

    def predict_one(self, state, target=False):
        return self.predict(state.reshape(1, IMAGE_STACK, IMAGE_WIDTH, IMAGE_HEIGHT), target).flatten()

    def update_target_model(self):
        self.target_model.set_weights(self.model.get_weights())
