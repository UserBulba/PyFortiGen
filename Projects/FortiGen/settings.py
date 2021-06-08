'''Settings file'''
# settings.py

import os

GOLDEN_IMAGE_FILE = "golden.conf"

current_dir = (os.path.dirname(os.path.realpath(__file__)))
golden_image_path = os.path.join(current_dir, "conf", GOLDEN_IMAGE_FILE)

GOLDEN_IMAGE_PATH = golden_image_path
