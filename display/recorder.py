import os

import pygame
from PIL import Image

from utils import assure_directory


class Recorder:
    def __init__(self, rec_path):
        self.frame_number = 0
        self.dir = rec_path
        assure_directory(self.dir)

    def take_frame(self, screen):
        name = "000000"
        id = str(self.frame_number)
        name = name[:-len(id)]
        name += id + ".jpg"
        pygame.image.save(screen, self.dir + "/" + name)
        self.frame_number += 1

    def create_gif(self, destination_directory, destination_name, fps):
        skip = 11
        assure_directory(destination_directory)
        img_list = []
        imgs_names = sorted(os.listdir(self.dir), key=lambda x: int(x[:-4]))
        for name in imgs_names[:self.frame_number + 1][::skip]:
            img_list.append(Image.open(self.dir + "/" + name))
        if len(img_list) > 1:
            img_list[0].save(os.path.join(destination_directory, destination_name + ".gif"), save_all=True,
                             append_images=img_list[1:], duration=1000 / fps, loop=0)
        elif len(img_list) == 1:
            img_list[0].save(os.path.join(destination_directory, destination_name + ".gif"))


"""Dir = "D:/code/personal/bnn/gallery/imgs"
frame_number = 364
create_gif("D:/code/personal/bnn/gallery/videos", "demo1", 12)"""
