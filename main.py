import curses
import math
import time
from tkinter import dialog
from turtle import distance
import numpy as np
import keyboard as kb
import sys

fireball = np.random.randint(1,50)
sword = np.random.randint(20,30)
RESOLUTION = (60,30) #game resolution
cur_dialog = 'WELCOME TO KNIGHT VS DRAGON'
game_ticks = 0

def distance_calc(x,y,x2,y2):
    return math.sqrt((x-x2)**2+(y-y2)**2)


class Fireball:
    xpos = 0
    ypos = 0
    firing = False
    directions = 'right'
    def direction(self, dir):
        self.directions = dir
    def fire(self):
        self.firing = True
    def stop(self):
        self.firing = False
    def active(self):
        return self.firing
    def getX(self):
        return self.xpos
    def getY(self):
        return self.ypos
    def setX(self,x):
        self.xpos = x
    def setY(self,y):
        self.ypos = y
    def update(self):
        if self.directions == 'up':
            self.ypos -= 1
        if self.directions == 'down':
            self.ypos += 1
        if self.directions == 'right':
            self.xpos += 1
        if self.directions == 'left':
            self.xpos -= 1
        if self.xpos == (RESOLUTION[0]-1) or self.xpos == 0 or self.ypos == 0 or self.ypos ==  (RESOLUTION[1]-1):
            self.firing = False


class Knight:       
    xpos = 28
    ypos = 28  
    last_moved = 0
    health = 100
    time_dash = 0
    def __init_(self):
        self.direction = 'right'

    def getPos(self):
        return (self.xpos,self.ypos)
    
    def move(self):
        if game_ticks - self.last_moved > 8:
            if kb.is_pressed('space') and self.time_dash < game_ticks:
                if self.direction == 'up':
                    self.ypos -= 3
                if self.direction == 'down':
                    self.ypos += 3
                if self.direction == 'left':
                    self.xpos -= 3
                if self.direction == 'right':
                    self.xpos += 3
                self.time_dash = game_ticks + 30
                return
            if kb.is_pressed('up'):
                self.direction = 'up'
                self.ypos -= 1
                self.last_moved = game_ticks
            if kb.is_pressed('down'):
                self.direction = 'down'
                self.ypos += 1
                self.last_moved = game_ticks
            if kb.is_pressed('right'):
                self.direction = 'right'
                self.xpos +=1
                self.last_moved = game_ticks
            if kb.is_pressed('left'):
                self.direction = 'left'
                self.xpos -=1
                self.last_moved = game_ticks

    def getAction(self):
        if kb.is_pressed('z'):
            return 1
        elif kb.is_pressed('x'):
            return 2
        else:
            return 0

    def getDirection(self):
        return self.direction

    def getHealth(self):
        return self.health
    def setHealth(self,health):
        self.health = health
    def collision(self,dragon): 
        global cur_dialog

        if self.health > 0 and dragon.getHealth() > 0:
            if(distance_calc(dragon.getPos()[0],dragon.getPos()[1],self.xpos,self.ypos) < 4):
                self.health -= 0.2
        elif(self.health <= 0):
            sys.exit()


class Dragon:
    xpos = 15
    ypos = 15
    health = 200
    dialog_list= [
        "The Fire... It Burns!",
        "Damnnn that sword is sharp! OW",
        "NOOOOoooOOoOo YOU WON!!!"
    ]
    damage_time = 0
    move_time = 0
    seek = False
    attack_time = 200

    def getPos(self):
        return (self.xpos,self.ypos)
    
    def collision(self,fireball,player):
        global cur_dialog
        global game_ticks
        if self.health > 0 and player.getHealth()>0:
            if(distance_calc(fireball.getX(),fireball.getY(),self.xpos,self.ypos) < 3 and fireball.active()):
                fireball.stop()
                if( game_ticks - self.damage_time > 20):
                    self.health -= 10
                    cur_dialog = self.dialog_list[0]
                    self.damage_time = game_ticks
            
            if(distance_calc(player.getPos()[0],player.getPos()[1],self.xpos,self.ypos) < 3 and player.getAction() == 1 and game_ticks - self.damage_time > 20):
                self.health -= 10
                cur_dialog = self.dialog_list[1]
                self.damage_time = game_ticks 
        else:
            cur_dialog = self.dialog_list[2]
            self.health = 0
    
    def getHealth(self):
        return self.health
    def setHealth(self,health):
        self.health = health
    def moveAI(self,player):
        global game_ticks
        global cur_dialog

        if self.seek:
            if self.xpos < player.getPos()[0]:
                self.xpos+=1
            if self.xpos > player.getPos()[0]:
                self.xpos-=1
            if self.ypos < player.getPos()[1]:
                self.ypos+=1
            if self.ypos > player.getPos()[1]:
                self.ypos-=1
        if self.attack_time < game_ticks:
            self.seek = True
            self.attack_time = game_ticks + np.random.randint(50,300)
            cur_dialog = "CHARGEEEE"

        if distance_calc(self.xpos,self.ypos,player.getPos()[0],player.getPos()[1]) < 2:
            self.seek = False
                
        if self.move_time < game_ticks: 
            self.move_time = game_ticks + np.random.randint(10,100)
            direction = np.random.randint(0,4)
            if self.xpos == 0:
                self.xpos += 1
            elif self.xpos == RESOLUTION[0]-1:
                self.xpos -= 1
            elif self.ypos == RESOLUTION[1]-1:
                self.ypos -= 1
            elif self.ypos == 0:
                self.ypos += 1
            elif direction == 0:
                self.xpos += 1
            elif direction == 1:
                self.xpos -= 1
            elif direction == 2:
                self.ypos += 1
            elif direction == 3:
                self.ypos -= 1


class Field:
    def __init__(self):
        self.icons = {
            0: '. ',
            1: '--',
            2: 'o',
            3: 'o)',
            4: '(o',
            5: 'a',
            6: '_',
            7: '♘ ',
            8: '🔥',
            9: '⚔ '
        }
        self.field = np.zeros(RESOLUTION)
        self.init()
    def init(screen):
        print("made by CASI")

    def update_screen(self,screen,player,dragon): #update screen
        global cur_dialog
        for i in range(RESOLUTION[1]):
            row = ''
            for j in range(RESOLUTION[0]):
                row += (self.icons[int(self.field[j][i])])
            screen.addstr(i, 0, row) 
        screen.addstr(RESOLUTION[1]+1,0,(cur_dialog + "                                "))
        screen.addstr(RESOLUTION[1]+2,0,("Your Health: {}        ".format(player.getHealth())))
        screen.addstr(RESOLUTION[1]+3,0,("Dragon Health: {}       ".format(dragon.getHealth())))


    def render(self,player,dragon,fireball):
        global RESOLUTION
        self.field = np.zeros(RESOLUTION)
        if player.health > 0:
            self.field[player.getPos()[0]][player.getPos()[1]] = 7
        if(player.getAction()==1):
            if player.getDirection() == 'up':
                self.field[player.getPos()[0]][player.getPos()[1]-1] = 9
            if player.getDirection() == 'down':
                self.field[player.getPos()[0]][player.getPos()[1]+1] = 9
            if player.getDirection() == 'right':
                self.field[player.getPos()[0]+1][player.getPos()[1]] = 9
            if player.getDirection() == 'left':
                self.field[player.getPos()[0]-1][player.getPos()[1]] = 9

        proj_coord = self.handle_projectiles(fireball,player)
        if(fireball.active()):
            self.field[proj_coord[0]][proj_coord[1]] = 8
        self.render_dragon(dragon)
    
    def handle_projectiles(self, proj, player):
        if(player.getAction()==2 and not proj.active()):
            proj.fire()
            proj.direction(player.getDirection())
            proj.setX(player.getPos()[0])
            proj.setY(player.getPos()[1])
        if(proj.active()):
            proj.update()
        return (proj.getX(),proj.getY())

    def render_dragon(self,dragon):
        if(dragon.getHealth() > 0):
            x = dragon.getPos()[0]-3
            y = dragon.getPos()[1]
            self.field[x+1][y] = 4
            self.field[x+2][y] = 1
            self.field[x+3][y] = 3

def main(screen):
    global game_ticks
    game = Field()
    player = Knight()
    dragon = Dragon()
    shoot = Fireball()

    screen.timeout(0) 
    while(True):
        player.move()
        game.render(player, dragon, shoot)
        game.update_screen(screen,player,dragon)
        player.collision(dragon)
        dragon.collision(shoot,player)
        dragon.moveAI(player)
        screen.refresh()
        time.sleep(0.00001)
        game_ticks += 1

if __name__=='__main__':
    curses.wrapper(main)
