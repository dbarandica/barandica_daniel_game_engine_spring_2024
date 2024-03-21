# This file was created by: Daniel Barandica
# This code was inspired by Zelda and informed by Chris Bradfield

import pygame as pg
from settings import *
from random import choice
from utils import *

# player sprite

mobdisguise = False

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.hitpoints = 100
        self.life_count = 3
    
    def get_keys(self):
        self.vx, self.vy = 0, 0
        keys = pg.key.get_pressed()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed  
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed  
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071

            
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y

    
    def collide_with_group(self, group, kill):
            global mobdisguise
            hits = pg.sprite.spritecollide(self, group, kill)
            if hits:
                for hit in hits:
                    if isinstance(hit, Mob):
                        self.life_count -= 1
                        if self.life_count <= 0: 
                            self.game_over()
                        else:
                            self.reset_position()
                        
                    if str(hit.__class__.__name__) == "Coin":
                        self.moneybag += 1
                    if str(hit.__class__.__name__) == "Powerup":
                        if(choice(POWER_UP_EFFECTS) == "Speed"):
                            self.speed *= 5
                    if str(hit.__class__.__name__) == "Powerup":
                        if(choice(POWER_UP_EFFECTS) == "Disguise"):
                            mobdisguise = True
                            self.image.fill(RED)
                    if str(hit.__class__.__name__) == "Mob":
                        self.hitpoints -= 1
                        self.speed = 150
    
    def update(self):
        self.get_keys()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')
        self.collide_with_group(self.game.coins, True)
        self.collide_with_group(self.game.power_ups, True)
        
    def draw_health_bar(self):
        font = pg.font.Font(None, 36)
        text = font.render("Lives: " + str(self.life_count), True, (0, 255, 0))
        self.game.screen.blit(text, (100, 100))
        
    def game_over(self):
        self.game.screen.fill((0, 0, 0))
        font = pg.font.Font(None, 48)
        text = font.render("Game Over", True, (255, 0, 0))
        text_rect = text.get_rect(center=(self.game.screen.get_width() / 2, self.game.screen.get_height() / 2))
        self.game.screen.blit(text, text_rect)
        pg.display.flip()
        pg.time.delay(3000)
        self.game.quit()  

class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Powerup(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

        
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
    
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    
    def update(self):
        if mobdisguise == False:
            self.x += self.vx * self.game.dt
            self.y += self.vy * self.game.dt
            
            if self.rect.x < self.game.player1.rect.x:
                self.vx = 100
            if self.rect.x > self.game.player1.rect.x:
                self.vx = -100    
            if self.rect.y < self.game.player1.rect.y:
                self.vy = 100
            if self.rect.y > self.game.player1.rect.y:
                self.vy = -100
            self.rect.x = self.x
            self.collide_with_walls('x')
            self.rect.y = self.y
            self.collide_with_walls('y')
        elif mobdisguise == True:
            pass  # Adjust behavior for mobdisguise=True if needed
