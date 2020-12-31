import pygame

from display.recorder import Recorder

pygame.init()


class Screen:
    def __init__(self, size, background_color, title, space, record_settings=None):
        """
        A class encapsulating a surface object of pygame.
        :param size: Size of surface
        :param background_color: background color
        :param title: the title of the surface
        :param space: the space it represents
        :param record_settings: the settings for recording  ===> (images_directory, result_directory, result_name, fps)
        """
        self.background_color = background_color
        self.screen = pygame.display.set_mode(size)
        self.record_settings = record_settings
        pygame.display.update()
        pygame.display.set_caption(title)
        self.recorder = None

        # Initialize the screen recorder (basically just resets a counter and sets the cache path)
        if not (self.record_settings is None):
            self.recorder = Recorder(record_settings[0])
            print("initializing a GIF recorder")

    def clear_screen(self):
        self.screen.fill(self.background_color)

    def update(self):
        pygame.display.flip()
        if not (self.record_settings is None):
            self.recorder.take_frame(self.screen)

    def finalize(self):
        if not (self.record_settings is None):
            self.recorder.create_gif(self.record_settings[1], self.record_settings[2], self.record_settings[3])
