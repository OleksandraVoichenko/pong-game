import pygame.time
import json
from settings import *
from sprites import Player, Ball, Opponent


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.running = True

        self.all_sprites = pygame.sprite.Group()
        self.paddle_sprites = pygame.sprite.Group()

        self.player = Player((self.all_sprites, self.paddle_sprites))
        self.ball = Ball(self.all_sprites, self.paddle_sprites, self.update_score)
        self.opponent = Opponent((self.all_sprites, self.paddle_sprites), self.ball)

        try:
            with open(join('..', 'data', 'score.txt')) as file:
                self.score = json.load(file)
        except:
            self.score = {'player': 0, 'opponent': 0}
        self.font = pygame.font.Font(None, 160)


    def display_score(self):
        player_surf = self.font.render(str(self.score['player']), True, COLORS['bg detail'])
        player_rect = player_surf.get_frect(center=(WINDOW_WIDTH/2 + 100, WINDOW_HEIGHT/2))
        self.screen.blit(player_surf, player_rect)

        opponent_surf = self.font.render(str(self.score['opponent']), True, COLORS['bg detail'])
        opponent_rect = opponent_surf.get_frect(center=(WINDOW_WIDTH/2 - 100, WINDOW_HEIGHT/2))
        self.screen.blit(opponent_surf, opponent_rect)

        pygame.draw.line(self.screen, COLORS['bg detail'], (WINDOW_WIDTH / 2, 0), (WINDOW_WIDTH / 2, WINDOW_HEIGHT), 10)


    def update_score(self, side):
        self.score['player' if side == 'player' else 'opponent'] += 1

    def run(self):
        while self.running:
            dt = self.clock.tick()/ 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    with open(join('..', 'data', 'score.txt'), 'w') as file:
                        json.dump(self.score, file)

            self.screen.fill(COLORS['bg'])
            self.display_score()
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()


        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()