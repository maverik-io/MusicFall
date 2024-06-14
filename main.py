#! /usr/bin/env python3
import pygame as pg
import sys
import random
from time import time
import pickle

pg.init()
screen = pg.display.set_mode((600, 800))
pg.display.set_caption('MusicFall')

font = pg.font.Font('Mono.ttf', 30)
font2 = pg.font.Font('Mono.ttf', 20)
font3 = pg.font.Font('Mono.ttf', 100)

sounds = [pg.mixer.Sound(f'Sounds/sound{i+1}.wav') for i in range(8)]
hit = pg.mixer.Sound('Sounds/hit.wav')
pg.mixer.music.load('Sounds/theme.wav')
pg.mixer.music.play(-1)
pg.mixer.music.set_volume(0.15)   

# Colors
BG = '#333333'
LANE_COLORS = [
        "#E0335B",
        "#E85BB1",
        "#5B3EC9",
        "#1B816D",
        "#96C43E",
        "#ECD73F",
        "#F59447",
        "#E0335B",
    ]

class Letter():
    def __init__(self, lane, letter):
        self.letter = letter
        self.lane = lane
        self.x = (50 + lane * 50 if lane < 4 else lane * 50 + 150) + 25
        self.active = False
        self.activecounter = 0
        self.lastpointtime = 0

    def update(self, deltatime):
        self.lastpointtime += deltatime

        if self.active:
            self.activecounter += deltatime
            if self.activecounter > 0.75:
                self.active = False
                self.activecounter = 0
                if self.lastpointtime > 0.75:
                    Box.score -= 1
                    self.lastpointtime = 0


    def draw(self):
        pg.draw.circle(screen, '#dddddd' if self.active else '#bbbbbb', (self.x, 725), 20)
        text = font.render(self.letter, True, '#000000')
        text_rect = text.get_rect(center=(self.x, 725))
        screen.blit(text, text_rect)

class Box():
    boxes = []
    score = 0
    lives = 10

    def __init__(self, x, lane):
        self.lane = lane
        self.y = - 50
        self.x =  x
        self.width = 50

        Box.boxes.append(self)

        # For debugging

    def update(self, deltatime):
        self.y += 150 * deltatime

        if 650 < self.y < 750 :
            if letters[self.lane].active:
                Box.score += 1
                letters[self.lane].lastpointtime = 0
                sounds[self.lane].play()
                Box.boxes.remove(self)

        elif self.y > 800:
            Box.boxes.remove(self)
            Box.lives -= 1
            hit.play()
            


    def draw(self):
        pg.draw.rect(screen, LANE_COLORS[self.lane], pg.Rect(self.x, self.y, self.width, self.width).inflate(-10, -10))

class Lane():

    def __init__(self, i):
        self.x = 50 + i * 50 if i < 4 else i * 50 + 150
        self.surf = pg.Surface((50, 800))
        self.surf.fill(LANE_COLORS[i])
        self.surf.set_alpha(50)

    def draw(self):
        screen.blit(self.surf, (self.x, 0))

class BoxManager():
    def __init__(self):
        self.counter = 0
        self.spawnrate = 2

    def update(self, deltatime):
        self.counter += deltatime

        if self.counter > self.spawnrate:
            self.counter = 0
            for i in random.sample(range(8), random.randint(1, 3)):
                Box(50 + i * 50 if i < 4 else i * 50 + 150, i)

boxman = BoxManager()
lanes = [Lane(i) for i in range(8)]
letters = [Letter(i, l) for i, l in enumerate("ASDFJKL;")]

def main():    

    try:
        with open('highscore.pkl', 'rb') as f:
            highscore = pickle.load(f)
    except:
        highscore = 0

    deltatime = 1/60
    started = False
    while True:
        for letter in letters:
            letter.active = False

        prevtime = time()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    if not started:
                        started = True
                        Box.boxes = []
                        Box.score = 0
                        Box.lives = 10
                        boxman.counter = 0
                        boxman.spawnrate = 2
                    
        if started:
            keys = pg.key.get_pressed()
            if keys[pg.K_a]:
                letters[0].active = True
            if keys[pg.K_s]:
                letters[1].active = True
            if keys[pg.K_d]:
                letters[2].active = True
            if keys[pg.K_f]:
                letters[3].active = True
            if keys[pg.K_j]:
                letters[4].active = True
            if keys[pg.K_k]:
                letters[5].active = True
            if keys[pg.K_l]:
                letters[6].active = True
            if keys[pg.K_SEMICOLON]:
                letters[7].active = True

            boxman.update(deltatime)
            for box in Box.boxes:
                box.update(deltatime)
                

        screen.fill(BG)

        for lane in lanes:
            lane.draw()

        for box in Box.boxes:
            box.draw()


        pg.draw.rect(screen, '#aaaaaa', pg.Rect(0, 700, 700, 50))
        for letter in letters:
            letter.draw()
            letter.update(deltatime)


        if Box.lives <= 0:
            started = False
            if Box.score > highscore:
                highscore = Box.score
                with open('highscore.pkl', 'wb') as f:
                    pickle.dump(Box.score, f)

           

        pg.draw.rect(screen, '#aaaaaa', pg.Rect(0, 0, 700, 50))
        if started:
            text = font.render(f"Score: {Box.score}", True, '#000000')
            text_rect = text.get_rect(midleft=(50, 25))
            screen.blit(text, text_rect)

            text2 = font2.render('██'*Box.lives+f'{Box.lives:>3}', True, '#550000')
            text_rect2 = text2.get_rect(midright=(550, 25))
            screen.blit(text2, text_rect2)

        else:
            text4 = font.render('MUSICFALL', True, '#000000')
            text_rect4 = text4.get_rect(center=(300, 25))
            screen.blit(text4, text_rect4)

            text = font3.render(f"{Box.score}   {highscore}", True, '#ffffff')
            text_rect = text.get_rect(center=(300, 400))
            screen.blit(text, text_rect)

            text3 = font.render('LASTSCORE     HIGHSCORE', True, '#ffffff')
            text_rect3 = text3.get_rect(center=(300, 300))
            screen.blit(text3, text_rect3)

            text2 = font.render('Press Space to start', True, '#ffffff')
            text_rect2 = text2.get_rect(center=(300, 550))
            screen.blit(text2, text_rect2)


        pg.display.flip()

        deltatime = time() - prevtime

if __name__ == '__main__':
    while True:
        main()