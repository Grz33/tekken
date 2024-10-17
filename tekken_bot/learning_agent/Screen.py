from PIL import Image

import cv2
import mss
import numpy as np
from PIL import ImageGrab

IMAGE_WIDTH = 84
IMAGE_HEIGHT = 84


class Screen:
    screen = {'left': 0, 'top': 0, 'width': 1920, 'height': 1080}
    left_hp_capture = {'left': 367, 'top': 115, 'width': 520, 'height': 30}
    right_hp_capture = {'left': 1032, 'top': 115, 'width': 520, 'height': 30}

    def __init__(self):
        self.hp_before_combo = None

    def count_health_colors(self, hp_image):
        # Konwersja obrazu na tablicę NumPy
        hp_image_np = np.array(hp_image)

        # Podziel obraz na kanały kolorów (RGB)
        r, g, b = hp_image_np[:, :, 0], hp_image_np[:, :, 1], hp_image_np[:, :, 2]

        # Definiowanie zakresów dla kolorów
        # Pomarańczowy zakres (RGB: ~[255, 165, 0])
        orange_mask = (r > 200) & (r <= 255) & (g > 100) & (g <= 165) & (b < 100)

        # Czerwony zakres (RGB: ~[255, 0, 0])
        red_mask = (r > 200) & (r <= 255) & (g < 50) & (b < 50)

        # Zliczanie pikseli pomarańczowych i czerwonych
        orange_count = np.sum(orange_mask)
        red_count = np.sum(red_mask)

        return orange_count, red_count



    def get_hp_value(self):
        left_hp = ImageGrab.grab(bbox=(
            self.left_hp_capture['left'], self.left_hp_capture['top'],
            self.left_hp_capture['left'] + self.left_hp_capture['width'],
            self.left_hp_capture['top'] + self.left_hp_capture['height']

        ))

        right_hp = ImageGrab.grab(bbox=(
            self.right_hp_capture['left'], self.right_hp_capture['top'],
            self.right_hp_capture['left'] + self.right_hp_capture['width'],
            self.right_hp_capture['top'] + self.right_hp_capture['height']
        ))


        return left_hp, right_hp

    def get_hp(self):
        left_hp_image, right_hp_image = self.get_hp_value()
        orange_count_left, red_count_left = self.count_health_colors(left_hp_image)
        total_pixels_left = orange_count_left + red_count_left
        orange_count_right, red_count_right = self.count_health_colors(right_hp_image)
        total_pixels_right = orange_count_right + red_count_right

        if total_pixels_left == 0:
            left_hp_value = 0
        else:
            left_hp_value = int (orange_count_left)

        if total_pixels_right == 0:
            right_hp_value = 0
        else:
            right_hp_value = int(orange_count_right)

        print(left_hp_value,right_hp_value )
        return left_hp_value, right_hp_value

    def get_screen(self):
        with mss.mss() as sct:
            sct_img = sct.grab(self.screen)
            img = Image.frombytes('RGB', sct_img.size, sct_img.rgb)
            img = img.resize((IMAGE_WIDTH, IMAGE_HEIGHT), Image.LANCZOS)
            curr_screen = np.array(img)

        return cv2.cvtColor(curr_screen, cv2.COLOR_BGR2GRAY)

    def get_hp_before_combo(self):
        self.hp_before_combo = self.get_hp()

    def get_reward(self):
        reward = 0
        left_hp_after_combo, right_hp_after_combo = self.get_hp()

        if right_hp_after_combo > self.hp_before_combo[1]:
            return reward

        diff_left_hp = int(self.hp_before_combo[0]) - int(left_hp_after_combo)
        diff_right_hp = int(self.hp_before_combo[1]) - int(right_hp_after_combo)

        reward -= diff_left_hp
        reward += diff_right_hp

        return reward
#screeny paskow zycie oraz co sciaga obraz to czarne biale
