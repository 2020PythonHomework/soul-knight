import pygame

class Music(object):
    def __init__(self, sound):
        self.channal = None
        self.sound = sound
    def play_sound(self):
        self.channal = pygame.mixer.find_channel(True)
        self.channal.set_volume(0.5)
        self.channal.play(self.sound)
    def play_pause(self):
        self.channal.set_volume(0.0)
        self.channal.play(self.sound)
    def replay_music(self):
        self.play_pause()
        self.play_sound()