import pygame
import math

pygame.mixer.init()
soundVolume = 1
class SFX:
    def __init__(self, path,volume=1):
        self.path = path
        self.sfx = pygame.mixer.Sound(path)
        self.anotherVolume = volume
        self.currentDuration = 0
        self.duration = self.sfx.get_length()* 60
        self.volume = volume
        self.volumeMultiplierConstant = 0.001
        self.soundVolume = soundVolume
        self.playing = False
        self.playOnceBool = False


    def update(self):
        self.soundVolume = soundVolume
        if not self.playing and not self.playOnceBool:
            self.currentDuration = 0
            self.sfx.stop()
        self.sfx.set_volume(self.volume*self.soundVolume)
        self.playing = False

    def SoundDropOff(self, dist):
        dist *= self.volumeMultiplierConstant

        amount = (4*math.pi*(dist**2))
        if amount < 1:
            amount = 1

        self.volume = 1/amount


    def playOnce(self, dist):
        self.playing = True
        self.playOnceBool = True
        self.soundVolume = soundVolume
        if dist != -1:
            self.SoundDropOff(dist)
            self.sfx.set_volume(self.volume*self.soundVolume*self.anotherVolume)
        else:
            self.sfx.set_volume(self.soundVolume*self.anotherVolume)

        pygame.mixer.Sound.play(self.sfx)

    def play(self, dist):
        if dist != -1:
            self.SoundDropOff(dist)
            self.sfx.set_volume(self.volume*self.soundVolume*self.anotherVolume)
        else:
            self.sfx.set_volume(self.soundVolume*self.anotherVolume)

        if not self.playing:
            pygame.mixer.Sound.play(self.sfx)

        self.playing = True
        if self.currentDuration > 0:
            self.currentDuration -= 1
            return 0



        self.currentDuration = self.duration-10

    def anotherUpdate(self):
        self.currentDuration -= 1
        if self.currentDuration <= 0:
            self.playing = False

    def playSimple(self, dist):


        if not self.playing:
            if dist != -1:
                self.SoundDropOff(dist)
                self.sfx.set_volume(self.volume * self.soundVolume * self.anotherVolume)
            else:
                self.sfx.set_volume(self.soundVolume * self.anotherVolume)
            pygame.mixer.Sound.play(self.sfx)
            self.currentDuration = self.duration / 8

        self.playing = True


dirtBreakSFX = SFX("data/assets/SFX/breakDirt.mp3")
stoneBreakSFX = SFX("data/assets/SFX/breakStone.mp3",2)
ironBreakSFX = SFX("data/assets/SFX/breakIron.mp3",0.1)
diamondBreakSFX = SFX("data/assets/SFX/breakDiamond.wav")
popSFX = SFX("data/assets/SFX/pop.mp3", 0.1)
moneySFX = SFX("data/assets/SFX/chaChing.mp3", 0.1)

def updateSFX():
    popSFX.anotherUpdate()
    dirtBreakSFX.anotherUpdate()
    stoneBreakSFX.anotherUpdate()
    ironBreakSFX.anotherUpdate()
    diamondBreakSFX.anotherUpdate()
    moneySFX.anotherUpdate()
