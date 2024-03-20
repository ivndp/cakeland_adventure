import pygame
from pygame.locals import *
import random
import time


pygame.init()
vec = pygame.math.Vector2

height = 640
width = 640
acc = 0.5
fric = -0.12
fps = 60

FramePerSec = pygame.time.Clock()

display_surface = pygame.display.set_mode((width, height))

pygame.display.set_caption("Cake Land Adventure")

logo = pygame.image.load("./img/logo.png")
pygame.display.set_icon(logo)

font = pygame.font.SysFont("Verdana", 20)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # self.surf = pygame.Surface((64, 64))
        # self.surf.fill((128,255,40))
        self.image_right = pygame.image.load("./img/YYS_walking01.png")
        self.image_left = pygame.image.load("./img/YYS_walking_left.png")
        self.image = self.image_right
        self.rect = self.image.get_rect()

        self.pos = vec((width/2,330))
        self.vel = vec(0,0)
        self.acc = vec(0,0)

        self.jumping = False
        self.score = 0
        self.meter = 0
    
    def move(self):
        self.acc = vec(0,0.5)

        pressed_keys = pygame.key.get_pressed()

        if pressed_keys[K_LEFT]:
            self.acc.x = -acc
            self.image = self.image_left
        if pressed_keys[K_RIGHT]:
            self.acc.x = acc
            self.image = self.image_right

        self.acc.x += self.vel.x * fric
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc

        if self.pos.x > width:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = width
        
        self.rect.midbottom = self.pos
    
    def update(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if self.vel.y > 0:
            if hits:
                if self.pos.y < hits[0].rect.bottom:
                    if hits[0].point:
                        hits[0].point = False
                        self.score += 1
                    self.pos.y = hits[0].rect.top + 1
                    self.vel.y = 0
                    self.jumping = False

    def jump(self):
        hits = pygame.sprite.spritecollide(self, platforms, False)
        if hits and not self.jumping:
            self.jumping = True
            self.vel.y = -15

    def cancel_jump(self):
        if self.jumping:
            if self.vel.y < -3:
                self.vel.y = -3

class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.length = random.randint(1,3)
        self.head_image = pygame.image.load("./img/cream_plat_head.png")
        self.body_image = pygame.image.load("./img/cream_plat.png")
        self.tail_image = pygame.image.load("./img/cream_plat_tail.png")
        self.image = self.create_platform_surface()
        # self.image = pygame.Surface((random.randint(50,100), 12))
        # self.image.fill((255,178,102))
        self.rect = self.image.get_rect(center = (random.randint(94,width-94), random.randint(0,height-30)))
        self.point = True
        self.speed = random.randint(-1, 1)
        self.moving = True
    
    def create_platform_surface(self):
        platform_surface = pygame.Surface((self.length * 40 + 10, 20), pygame.SRCALPHA)
        platform_surface.blit(self.head_image,(0,0))
        for i in range(self.length):
            platform_surface.blit(self.body_image, (i*40+5, 0))
        platform_surface.blit(self.tail_image, (self.length*40+5, 0) )
        return platform_surface

    def move(self):
        hits = self.rect.colliderect(P1.rect)
        if self.moving:
            self.rect.move_ip(self.speed, 0)
            if hits:
                P1.pos += (self.speed, 0)
            if self.speed > 0 and self.rect.right > width-64:
                self.speed *= -1
            if self.speed < 0 and self.rect.left < 64:
                self.speed *= -1

    def generate_strawberry(self):
        if (self.speed == 0):
            s = Strawberry((self.rect.centerx - 20, self.rect.centery - 60))
            strawberries.add(s)
            all_sprites.add(s)

class Strawberry(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()

        self.image = pygame.image.load("./img/strawberry.png")
        self.rect = self.image.get_rect()

        self.rect.topleft = pos

    def update(self):
        if self.rect.colliderect(P1.rect):
            P1.score += 100
            self.kill()

    def move(self):
        pass

class Background_cake(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_list = [
            "./img/cake_cc.png",
            "./img/cake_a.png",
            "./img/cake_b.png",
            "./img/cake_cho_a.png",
            "./img/cake_cho_b.png"
            ]
        self.image = pygame.image.load(random.choice(self.image_list))
        self.rect = self.image.get_rect()

    def move(self):
        pass

def plat_gen():
    while len(platforms) < 8:
        p = platform()
        platform_too_close = True
        tries = 0

        while platform_too_close and tries < 10:
            p = platform()
            p.rect.center = (random.randrange(89, width - 89), random.randrange(-50, 0))
            platform_too_close = check_platform(p, platforms)
            tries += 1

        p.generate_strawberry()
        platforms.add(p)
        all_sprites.add(p)

def bg_cake_gen():
    while len(bg_cakes) <3:
        bg_cake_too_close = True
        tries = 0
        
        while bg_cake_too_close:
            bg_cake = Background_cake()
            bg_cake.rect.center = ((width/2-1), random.randint(-50, 0))
            bg_cake_too_close = check_platform(bg_cake, bg_cakes)
            tries += 1
        
        bg_cakes.add(bg_cake)

def check_platform(platform, groupies):
    if pygame.sprite.spritecollideany(platform, groupies):
        return True
    else:
        for entity in groupies:
            if entity == platform:
                continue
            if (abs(platform.rect.top - entity.rect.bottom) < 50) and (abs(platform.rect.bottom - entity.rect.top)  < 50):
                return True
        return False

bg_cakes = pygame.sprite.Group()
bg_cake = Background_cake()
bg_cake.rect = bg_cake.image.get_rect(center = (width/2-1, height-random.randint(50,200)))
bg_cake2 = Background_cake()
bg_cake2.rect = bg_cake.image.get_rect(center = (width/2-1, height-random.randint(300,400)))
bg_cakes.add(bg_cake, bg_cake2)

base_platform = platform()
P1 = Player()

base_platform.image = pygame.image.load("./img/cream_base.png")
# base_platform.image.fill((240,240,240))
base_platform.rect = base_platform.image.get_rect(center = (width/2,height - 15))
base_platform.point = False
base_platform.moving = False

all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(base_platform)

platforms = pygame.sprite.Group()
platforms.add(base_platform)

strawberries = pygame.sprite.Group()


for x in range(7):
    pl = platform()
    pl.rect = pl.image.get_rect(center = (random.randint(50, width-50), height-(x+1)*75))
    pl.generate_strawberry()
    platforms.add(pl)
    all_sprites.add(pl)

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                P1.jump()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                P1.cancel_jump()

    if P1.rect.top > height:
        for entity in all_sprites:
            entity.kill()
            time.sleep(1)
            display_surface.fill((0,0,0))
            gg_font = pygame.font.SysFont("Verdana", 50)
            game_over = gg_font.render("Game Over", True, (255,255,255))
            final_score = font.render(f"Score: {P1.score}", True, (255,255,255))
            final_score2 = font.render(f"Highest Reached: {round(P1.meter, 2)}M", True, (255,255,255))
            display_surface.blit(game_over, (width/2-130, height/5))
            display_surface.blit(final_score, (120, height/2))
            display_surface.blit(final_score2, (120, height/2+40))
            pygame.display.update()
            time.sleep(5)
            pygame.quit()

    bg_image = pygame.image.load("./img/cake_land_bg.png")
    display_surface.blit(bg_image, (0,0))
    score_text = font.render(f"Score: {P1.score}", True, (0,0,0))
    meter_text = font.render(f"{round(P1.meter, 2)}M", True, (0,0,0))
    
    if P1.rect.top <= height / 3:
        P1.pos.y += abs(P1.vel.y)
        for plat in platforms:
            plat.rect.y += abs(P1.vel.y)
            if plat.rect.top >= height:
                plat.kill()
        for straw in strawberries:
            straw.rect.y += abs(P1.vel.y)
            if straw.rect.top >= height:
                straw.kill()
        for bg in bg_cakes:
            bg.rect.y += abs(P1.vel.y)
            if bg.rect.top >= height:
                bg.kill()
        P1.meter -= round(P1.vel.y/100, 2)

    bg_cake_gen()
    P1.update()
    plat_gen()

    for entity in bg_cakes:
        display_surface.blit(entity.image, entity.rect)

    for entity in all_sprites:
        if entity != P1:
            display_surface.blit(entity.image, entity.rect)
        entity.move()

    for straw in strawberries:
        display_surface.blit(straw.image, straw.rect)
        straw.update()

    display_surface.blit(P1.image, P1.rect)

    display_surface.blit(score_text, (width/4, 10))
    display_surface.blit(meter_text, (width/3*2, 10))

    pygame.display.update()
    FramePerSec.tick(fps)