import os
import random
import math
import sys
import pygame
from os import listdir
from os.path import isfile, join
pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 800
FPS = 30
PLAYER_VEL = 10

window = pygame.display.set_mode((WIDTH, HEIGHT))
#ansh
def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            sprite_name = image.replace(".png", "")
            all_sprites[sprite_name] = sprites

    return all_sprites


def get_block(size):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
def get_train(width,height):
    path = join("assets", "MainCharacters", "train.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
    rect = pygame.Rect(96, 0, width, height)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)

#ansh

#sahili
class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "Enchantress", 128, 128, True)
    ANIMATION_DELAY = 5

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0
        self.health = 100


    def jump(self):
        self.y_vel = -self.GRAVITY * 10
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def make_hit(self):
        if not self.hit:
            self.hit = True
            self.health -= 20  # Decrease health by 20 when hit
            if self.health <= 0:
                # Game over logic (reset or exit the game)
                pygame.quit()
                sys.exit()

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "fall"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        if sprite_sheet_name not in self.SPRITES:
            sprite_sheet_name = "idle_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))
#sahili

#Aditya
class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_block(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

class Train(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        train = get_train(width,height)
        self.image.blit(train, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def get_spike(size):
    path = join("assets", "Traps","Spike Head", "Idle.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    rect = pygame.Rect(0, 0, size, size)
    surface.blit(image, (0, 0), rect)
    return pygame.transform.scale2x(surface)
class SpikedBlock(Object):
    def __init__(self, x, y, size):
        super().__init__(x, y, size, size)
        block = get_spike(size)
        self.image.blit(block, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)
class Building(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        building = pygame.image.load(join("assets", "Building", "building.png")).convert_alpha()
        self.image.blit(building, (0, 0))
        self.mask = pygame.mask.from_surface(self.image)

def display_victory_scene(window):
    # Code to display the victory scene
    star_rating = Coin.COLLECTED_COINS
    victory_font = pygame.font.SysFont(None, 72)
    victory_text = victory_font.render("Victory!", True, (0, 255, 0))
    VadaPav = victory_font.render(f"VadaPav:{star_rating} ", True, (0, 255, 0))
    window.blit(victory_text, (WIDTH // 2 - victory_text.get_width() // 2, HEIGHT // 2 - victory_text.get_height() // 2))
    window.blit(VadaPav, (WIDTH // 2 - VadaPav.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()
    pygame.time.wait(3000)        

class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", width, height)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)
    font = pygame.font.SysFont(None, 36)
    coins_text = font.render(f"VadaPav: {Coin.COLLECTED_COINS}", True, (255, 255, 255))
    window.blit(coins_text, (10, 50))
    health_text = font.render(f"Health: {player.health}", False, (255, 255, 255))
    window.blit(health_text, (10, 10))

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]

    for obj in to_check:
        if obj and obj.name == "fire":
            player.make_hit()

#Aditya
class Coin(Object):
    COLLECTED_COINS = 0

    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height, "Idle")
        self.coin_sprites = load_sprite_sheets("Traps", "Rock Head", width, height)
        self.image = self.coin_sprites.get("Idle", [pygame.Surface((width, height))])[0]
        self.mask = pygame.mask.from_surface(self.image)
        self.collected = False

    def draw(self, win, offset_x):
        if not self.collected:
            win.blit(self.image, (self.rect.x - offset_x, self.rect.y))

    def handle_collision(self, player):
        if not self.collected and pygame.sprite.collide_mask(player, self):
            self.collected = True
            Coin.COLLECTED_COINS += 1
            #once collected the coin will disappear
            self.rect.x = -1000
            

#Ansh&Rishabh
def main(window):
    clock = pygame.time.Clock()
    background, bg_image = get_background("Pink.png")

    block_size = 96


    player = Player(-40, 100, 20, 20)
    fire = Fire(100, HEIGHT - block_size - 64, 16, 32)
    fire.on()
    
    coin1 = Coin(800, HEIGHT - block_size - 64, 32, 32)
    coin2 = Coin(1000, HEIGHT - block_size - 64, 32, 32)
    coin3 = Coin(1200, HEIGHT - block_size - 158,32, 32)

    floor1 = Block(2000, HEIGHT - block_size, block_size)
    floor2 = Block(2200, HEIGHT - block_size, block_size)
    #create 20 floors
    floor3 = Block(2400, HEIGHT - block_size, block_size)
    floor4 = Block(2600, HEIGHT - block_size, block_size)
    floor5 = Block(2800, HEIGHT - block_size, block_size)
    train = Train(1200, HEIGHT - block_size - 96, 96, 96)
    train2 = Train(1296, HEIGHT - block_size - 96, 96, 96)
    floor = [Block(i * block_size, HEIGHT - block_size, block_size)
             for i in range(-WIDTH // block_size, (WIDTH * 2) // block_size)]
    #append floors after floor 5
    floor6 = Block(2400, HEIGHT - block_size, block_size)
   
   
    objects = [*floor, Block(0, HEIGHT - block_size * 2, block_size),
               Block(block_size * 3, HEIGHT - block_size * 4, block_size *2,), fire, coin1, coin2, floor1,floor2,train,train2, coin3,floor3,floor4,floor5,floor6,]
    objects = [*objects, Block(block_size * 6, HEIGHT - block_size * 2, block_size),]
    spike = SpikedBlock(200, HEIGHT - block_size * 2, block_size)
    objects.append(spike)
    objects.append(SpikedBlock(300, HEIGHT - block_size * 2, block_size))
    objects.append(SpikedBlock(400, HEIGHT - block_size * 2, block_size))
    fire1= Fire(900, HEIGHT - block_size - 64, 16, 32)
    fire1.on()
    objects.append(fire1)


    objects.append(Train(1296+96, HEIGHT - block_size - 96, 96, 96))
    objects.append(Train(2500, HEIGHT - block_size - 96, 96, 96))
    objects.append(Train(2596, HEIGHT - block_size - 96*2, 96, 96))
    objects.append(Train(2596+96, HEIGHT - block_size - 96*3, 96, 96))


    for i in range(0, 500-90, 96):
        objects.append(Train(1296+96+i, HEIGHT - block_size - 96, 96, 96))
    for i in range(0,  1000, 96):
        objects.append(Block(2400+i, HEIGHT - block_size, block_size))    

    offset_x = 0
    scroll_area_width = 200

    coin_count = 0
    building = Building(2800, HEIGHT - 530, 600, 400)  # Adjust the position and size accordingly
    objects.append(building)
    run = True
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)
        fire.loop()
        fire1.loop()

        for coin in [coin1, coin2, coin3]:
            coin.handle_collision(player)

        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel
        
        if player.rect.y > HEIGHT:
            
            #show game over screen and if all of the coins are collected show 3 stars
            game_over_font = pygame.font.SysFont(None, 72)
            game_over_text = game_over_font.render("Game Over", True, (255, 0, 0))
            window.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)  # Wait for 2 seconds

            # Star rating based on collected coin
            star_rating = Coin.COLLECTED_COINS
            stars_font = pygame.font.SysFont(None, 48)
            stars_text = stars_font.render(f"VadaPav: {star_rating}", True, (255, 255, 0))
            window.blit(stars_text, (WIDTH // 2 - stars_text.get_width() // 2, HEIGHT // 2 + 50))
            pygame.display.flip()
            pygame.time.wait(3000)
            
        if player.rect.colliderect(building.rect):
            if player.rect.centerx >= building.rect.centerx - player.rect.width/2 and player.rect.centerx <= building.rect.centerx + player.rect.width/2:
                display_victory_scene(window)
                break
            
        
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        if player.rect.y > HEIGHT:
            run = False
            break    
        
        #add image for the background at x=2800

    
        pygame.display.flip()
    pygame.quit()
    quit()


if __name__ == "__main__":
    main(window)

    

