import math as m
import pygame

def findDistance(x1, y1, x2, y2):
    dist = m.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return dist


# Calculate angle.
def findAngle(x1, y1, x2, y2):
    theta = m.acos((y2 - y1) * (-y1) / (m.sqrt(
        (x2 - x1) ** 2 + (y2 - y1) ** 2) * y1))
    degree = int(180 / m.pi) * theta
    return degree


audio = 'sound_warning\mixkit-alarm-clock-beep-988.wav'
def sendWarning():
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()

    pass


