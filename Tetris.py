import pygame
import random
from pygame.locals import *
import sys

#変数の設定
CELL_SIZE = 32
FIELD_WIDTH = 10
FIELD_HEIGHT = 20
SCREEN_SIZE = (832, 640)
BLOCK_IMAGE = [None]*9
TET = [
    [   #T型
        [(1, 0), (0, 1), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (1, 2)],
        [(1, 1), (0, 0), (1, 0), (2, 0)],
        [(1, 0), (2, 1), (1, 1), (1, 2)]
    ],
    [  #I型
        [(0, 0), (1, 0), (2, 0), (3, 0)],
        [(1, 0), (1, 1), (1, 2), (1, 3)]
    ],
    [  #O型
        [(0, 0), (1, 0), (0, 1), (1, 1)]
    ],
    [  #Z型
        [(0, 0), (1, 0), (1, 1), (2, 1)],
        [(1, 0), (0, 1), (1, 1), (0, 2)]
    ],
    [  #S型
        [(1, 0), (2, 0), (0, 1), (1, 1)],
        [(0, 0), (0, 1), (1, 1), (1, 2)]
    ],
    [  #L型
        [(0, 0), (1, 0), (2, 0), (0, 1)],
        [(0, 0), (1, 0), (1, 1), (1, 2)],
        [(2, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (0, 1), (0, 2), (1, 2)]
    ],
    [  #J型
        [(0, 0), (1, 0), (2, 0), (2, 1)],
        [(1, 0), (1, 1), (0, 2), (1, 2)],
        [(0, 0), (0, 1), (1, 1), (2, 1)],
        [(0, 0), (1, 0), (0, 1), (0, 2)]
    ]
]

field_data = []
for i in range(FIELD_HEIGHT):
    field_data.append([7] + [-1]*FIELD_WIDTH + [7])
field_data.append([7]*(FIELD_WIDTH + 2))

fall_frm = 60   #落下までのフレーム
fall_cnt = 0    #フレームカウンタ
fall_frm_down = 2   #したボタン押したときの落下フレーム
fall_frm_normal = 60    #押してないときの落下フレーム
ctrlable_frm = 0        #コントロール可能フレーム

tet_x = 4   #テトリミノのX座標
tet_y = 0   #テトリミノのY座標
tet_n = 0   #テトリミノの番号
tet_a = 0   #テトリミノの回転角度
tet_next = random.randint(0, 6) #ネクストの設定
score = 0
lines = 0

def fieldView():   #フィールドの描写
    #ブロックの描写
    for i in range(FIELD_HEIGHT):
        for j in range(FIELD_WIDTH + 2):
            if field_data[i][j] != -1:
                screen.blit(BLOCK_IMAGE[field_data[i][j]], ((j+7) * CELL_SIZE, i * CELL_SIZE))
            else:
                screen.blit(BLOCK_IMAGE[8], ((j+7) * CELL_SIZE, i * CELL_SIZE))
    #落下中のブロックの処理
    for i in range(4):
        x = TET[tet_n][tet_a][i][0] + tet_x
        y = TET[tet_n][tet_a][i][1] + tet_y
        screen.blit(BLOCK_IMAGE[tet_n], ((x+7) * CELL_SIZE, y * CELL_SIZE))
    return

def nextView():
    global tet_next
    #落下中のブロックの処理
    for i in range(5):
        for j in range(5):
            x = i + 20
            y = j + 3
            screen.blit(BLOCK_IMAGE[8], (x * CELL_SIZE, y * CELL_SIZE))
    for i in range(4):
        x = TET[tet_next][0][i][0] + 21
        y = TET[tet_next][0][i][1] + 4
        screen.blit(BLOCK_IMAGE[tet_next], (x * CELL_SIZE, y * CELL_SIZE))

def falling():      #落下処理
    global tet_x, tet_y, tet_n, tet_a
    if isSetable(tet_x, tet_y + 1, tet_n, tet_a)==True:
        tet_y += 1
        ctrlable_frm = 60
        return True
    else:
        tet_set()
        return False
def tet_set():      #テトリミノの落下確定
    for i in range(4):
        x = TET[tet_n][tet_a][i][0] + tet_x
        y = TET[tet_n][tet_a][i][1] + tet_y
        field_data[y][x] = tet_n
    lineClear()
    fallStart()
    return
def lineClear():
    i = 20
    l = 0
    while i > 0:
        i -= 1
        if isFilled(i)==True:
            l += 1
            for j in range(i-1, -1, -1):
                for k in range(FIELD_WIDTH):
                    field_data[j+1][k+1] = field_data[j][k+1]
            i += 1
    global score, lines
    score += l * l * 100
    lines += l
    return
def isFilled(i):
    for m in range(FIELD_WIDTH):
        if field_data[i][m+1] == -1:
            return False
    return True
def fallStart():
    global tet_x, tet_y, tet_n, tet_a, tet_next
    tet_x = 4   #テトリミノのX座標
    tet_y = 0   #テトリミノのY座標
    tet_n = tet_next   #テトリミノの番号
    tet_a = 0   #テトリミノの回転角度
    tet_next = random.randint(0,6)
    if isSetable(tet_x, tet_y, tet_n, tet_a)==False:
        gameOver()
    return
def gameOver():
    fieldView()    #フィールドのブロックの表示
    nextView()
    pygame.display.update()
    print("score:"+str(score))
    print("lines:"+str(lines))
    while True:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                sys.exit()
def rolling():      #回転処理
    global tet_x, tet_y, tet_n, tet_a
    if isSetable(tet_x, tet_y, tet_n, (tet_a + 1) % len(TET[tet_n]))==True:
        tet_a = (tet_a + 1) % len(TET[tet_n])
        fieldView()
    elif isSetable(tet_x - 1, tet_y, tet_n, (tet_a + 1) % len(TET[tet_n]))==True:
        tet_x -= 1
        tet_a = (tet_a + 1) % len(TET[tet_n])
        fieldView()
    elif isSetable(tet_x + 1, tet_y, tet_n, (tet_a + 1) % len(TET[tet_n]))==True:
        tet_x += 1
        tet_a = (tet_a + 1) % len(TET[tet_n])
        fieldView()
    return

def left():         #左移動
    global tet_x, tet_y, tet_n, tet_a
    if isSetable(tet_x-1, tet_y, tet_n, tet_a)==True:
        tet_x -= 1
        fieldView()
    return

def right():        #右移動
    global tet_x, tet_y, tet_n, tet_a
    if isSetable(tet_x+1, tet_y, tet_n, tet_a)==True:
        tet_x += 1
        fieldView()
    return

def moment():       #瞬間落下
    dflag = True
    while dflag == True:
        dflag = falling()

def isSetable(x, y, n, a):  #嵌め込めるか
    for i in range(4):
        ax = TET[n][a][i][0] + x
        ay = TET[n][a][i][1] + y
        if ax>=1 and ay>= 0 and ax<FIELD_WIDTH+1 and ay<FIELD_HEIGHT:
            if field_data[ay][ax] != -1:
                return False
        else:
            return False
    return True

#Pygameを初期化
pygame.init()

#スクリーンの作成
screen = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption(u"Tetris")

#ブロックの画像の設定
for i in range(9):
    BLOCK_IMAGE[i] = pygame.image.load("image/"+str(i)+".gif").convert()

#時計の設定
clock = pygame.time.Clock()

#背景の設定
background_image = pygame.image.load("image/background.png").convert()
screen.blit(background_image, (0, 0))

#BGMの設定
pygame.mixer.music.load("music/tetris_bgm.mp3")
pygame.mixer.music.play(-1)

#落下開始
fallStart()

#ループ処理
while True:
    clock.tick(60)

    #ブロックの落下処理
    if fall_cnt >= fall_frm:
        fall_cnt = 0
        falling()
    else:
        fall_cnt += 1

    fieldView()    #フィールドのブロックの表示
    nextView()
    pygame.display.update()

    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif event.type == KEYDOWN and event.key == K_SPACE:
            rolling()
        elif event.type == KEYDOWN and event.key == K_LEFT:
            left()
        elif event.type == KEYDOWN and event.key == K_RIGHT:
            right()
        elif event.type == KEYDOWN and event.key == K_UP:
            moment()
        elif event.type == KEYDOWN and event.key == K_DOWN:
            fall_frm = fall_frm_down
        elif event.type == KEYUP and event.key == K_DOWN:
            fall_frm = fall_frm_normal