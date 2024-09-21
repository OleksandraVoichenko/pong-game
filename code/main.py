import pygame.time
from settings import *
from sprites import Player, Ball


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites)


    def run(self):
        while self.running:
            dt = self.clock.tick()/ 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.screen.fill(COLORS['bg'])
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()


        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()