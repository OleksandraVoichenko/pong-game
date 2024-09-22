import pygame.sprite
from settings import *

class Paddle(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)

        # image
        self.image = pygame.Surface(SIZE['paddle'], pygame.SRCALPHA)
        pygame.draw.rect(self.image, COLORS['paddle'], pygame.FRect((0, 0), SIZE['paddle']), 0, 4)

        # rect and movement logic
        self.rect = self.image.get_frect(center=POS['player'])
        self.old_rect = self.rect.copy()
        self.dir = 0
        self.speed = 0


    def move(self, dt):
        self.rect.centery += self.dir * self.speed * dt
        self.rect.top = 0 if self.rect.top < 0 else self.rect.top
        self.rect.bottom = WINDOW_HEIGHT if self.rect.bottom > WINDOW_HEIGHT else self.rect.bottom


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.get_direction()
        self.move(dt)


    def get_direction(self):
        pass


class Player(Paddle):
    def __init__(self, groups):
        super().__init__(groups)
        self.speed = SPEED['player']


    def get_direction(self):
        keys = pygame.key.get_pressed()
        self.dir = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])


class Opponent(Paddle):
    def __init__(self, groups, ball):
        super().__init__(groups)
        self.ball = ball
        self.speed = SPEED['opponent']
        self.rect = self.image.get_frect(center=POS['opponent'])


    def get_direction(self):
        self.dir = 1 if self.ball.rect.centery > self.rect.centery else -1


class Ball(pygame.sprite.Sprite):
    def __init__(self, groups, paddle_sprites, update_score):
        super().__init__(groups)
        self.paddle_sprites = paddle_sprites
        self.update_score = update_score

        # images
        self.image = pygame.Surface(SIZE['ball'], pygame.SRCALPHA)
        pygame.draw.circle(self.image, COLORS['ball'], (SIZE['ball'][0] / 2, SIZE['ball'][1] / 2), SIZE['ball'][0] / 2)

        # rect
        self.rect = self.image.get_frect(center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT))
        self.old_rect = self.rect.copy()
        self.dir = pygame.Vector2(choice((-1, 1)), uniform(0.7, 0.8) * choice((-1, 1)))
        self.speed = SPEED['ball']


    def move(self, dt):
        self.rect.x += self.dir.x * self.speed * dt
        self.collision('horizontal')
        self.rect.y += self.dir.y * self.speed * dt
        self.collision('vertical')


    def collision(self, direction):
        for sprite in self.paddle_sprites:
            if sprite.rect.colliderect(self.rect):
                if direction == 'horizontal':
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >=  sprite.old_rect.right:
                        self.rect.left = sprite.rect.right
                    self.dir.x *= -1
                else:
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    self.dir.y *= -1


    def wall_collision(self):
        if self.rect.bottom > WINDOW_HEIGHT:
            self.rect.bottom = WINDOW_HEIGHT
            self.dir.y *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.dir.y *= -1
        if self.rect.right >= WINDOW_WIDTH or self.rect.left <= 0:
            self.update_score('player' if self.rect.x < WINDOW_WIDTH / 2 else 'opponent')
            self.reset()


    def reset(self):
        self.rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        self.dir = pygame.Vector2(choice((-1, 1)), uniform(0.7, 0.8) * choice((-1, 1)))


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.move(dt)
        self.wall_collision()