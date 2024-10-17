
from .Model import *
from .Memory import *
from tekken_bot.moves import random_moves


class LearningAgent:
    steps = 0
    latest_Q = 0
    epsilon = MAX_EPSILON

    def __init__(self, learning=True):
        # super(learning_agent, self).__init__()
        self.state = None
        self.learning = learning
        self.inputShape = (IMAGE_STACK, IMAGE_WIDTH, IMAGE_HEIGHT)
        self.numActions = len(random_moves.valid_actions)
        self.model = Model(self.inputShape, self.numActions)
        # self.Model = Model()
        self.memory = Memory(MEMORY_CAPACITY)

    def observe(self, sample):

        # sample = [state, action, reward, next_state ]
        x, y, errors = self.get_targets([(0, sample)])
        self.memory.add(errors[0], sample)

        if self.steps % UPDATE_TARGET_FREQUENCY == 0:
            self.model.update_target_model()

        self.steps = self.steps + 1
        self.epsilon = MIN_EPSILON + (MAX_EPSILON - MIN_EPSILON) * math.exp(-LAMBDA * self.steps)

    def get_targets(self, batch):
        no_state = np.zeros(self.inputShape)
        states = np.array([o[1][0] for o in batch])
        states_ = np.array([(no_state if o[1][3] is None else o[1][3]) for o in batch])
        p = self.model.predict(states)
        p_ = self.model.predict(states_, target=False)
        ptarget_ = self.model.predict(states_, target=True)
        x = np.zeros((len(batch), IMAGE_STACK, IMAGE_WIDTH, IMAGE_HEIGHT))
        y = np.zeros((len(batch), self.numActions))
        errors = np.zeros(len(batch))

        for i in range(len(batch)):
            o = batch[i][1]
            s, a, r, s_ = o
            t = p[i]
            old_value = t[a]

            if s_ is None:
                t[a] = r
            else:
                t[a] = r + GAMMA * ptarget_[i][np.argmax(p_[i])]  # DDQN portion

            x[i] = s
            y[i] = t
            errors[i] = abs(old_value - t[a])
            self.latest_Q = t[a]

        return x, y, errors

    def choose_action(self, state):
        self.state = state
        self.steps += 1
        action = None

        if not self.learning:
            action = random.randint(0, len(random_moves.valid_actions) - 1)
        else:
            if random.uniform(0, 1) < self.epsilon:
                action = random.randint(0, len(random_moves.valid_actions) - 1)
            else:
                action = np.argmax(self.model.predict_one(state))

        return action

    def replay(self):
        batch = self.memory.sample(BATCH_SIZE)
        x, y, errors = self.get_targets(batch)

        for i in range(len(batch)):
            idx = batch[i][0]
            self.memory.update(idx, errors[i])

        self.model.train(x, y)

    def play(self, state):
        self.state = state
        action = np.argmax(self.model.predict_one(state))
        return action
