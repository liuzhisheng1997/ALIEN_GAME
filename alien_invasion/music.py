import pygame

class MusicPlay():
    def __init__(self):
        self.volume=0.2
        self.shoot_music='music/shoot.mp3'
        self.background_music='music/background.mp3'
    def shoot_music_play(self):
        pygame.mixer.music.load(self.shoot_music)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer.music.play()
    def background_music_play(self):
        pygame.mixer.music.load(self.background_music)
        pygame.mixer.music.set_volume(self.volume)
        pygame.mixer_music.play()