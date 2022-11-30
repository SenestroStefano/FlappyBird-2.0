from __modules__ import *

DeltaTime = 2
MoltScreen = 3.15
Divider = 1

width, height = 490 * MoltScreen, 270 * MoltScreen
FPS = 30 * DeltaTime

py.init()

screen = py.display.set_mode((width, height))
py.display.set_caption("Flappy Bird")

clock = py.time.Clock()

Bird_Fall = 0.5

Background_speed = 3 * MoltScreen / Divider
Num_tubes = 10

GameOver = False
Debug = False

Collisions = True

flag_beat_record = True

Score = 0
Record = 0
with open('score.txt', 'r') as f:
   f_contest = f.readlines()
   Record = int(f_contest[1])
f.close()