# Welcome to snake! You can move the snake by using the arrows 


import pygame as pg
from pygame import (
    Surface,
    KEYDOWN,
    K_UP,
    K_LEFT,
    K_DOWN,
    K_RIGHT,
)


class Snake:
    LENGTH = 25
    COLOUR = (14, 143, 51)

    def __init__(self, x, y):
        self.surf = Surface((Snake.LENGTH, Snake.LENGTH))
        self.surf.fill(Snake.COLOUR)
        self.rect = self.surf.get_rect(center=(x, y))
        self.move = 0  # Direction

    def moving(self, speed=5):
        if self.move == K_UP:
            self.rect.top -= speed
        elif self.move == K_LEFT:
            self.rect.left -= speed
        elif self.move == K_DOWN:
            self.rect.bottom += speed
        elif self.move == K_RIGHT:
            self.rect.right += speed


class Apple:
    COLOUR = (168, 50, 50)
    RADIUS = 10

    def __init__(self, start, end):
        self.surf = Surface((Apple.RADIUS, Apple.RADIUS))
        self.surf.fill(Apple.COLOUR)
        self.rect = self.set_location(start, end)

    def set_location(self, start, end):
        import random
        return self.surf.get_rect(center=(
            random.randint(start, end),
            random.randint(start, end)
        ))


class Game:
    W = 500

    def __init__(self):
        self.sc = pg.display.set_mode((Game.W, Game.W))
        self.apple = Apple(10, Game.W - 10)
        self.main = Snake(Game.W // 2, Game.W // 2)  # Head 
        self.obj_list = [self.main]  # Snake's body (consists of Snake's objects)
        self.clock = pg.time.Clock()
        self.state = True

    def get_event(self, object):
        LIMIT = ([K_UP, K_DOWN], [K_LEFT, K_RIGHT])  # For ex.: you cannot use arrow down after the arrow up
        for event in pg.event.get(): 
            if event.type == KEYDOWN:
                for collab in LIMIT:
                    if object.move in collab and event.key in collab:
                        return None
                object.move = event.key 
            elif event.type == pg.QUIT:
                self.state = False

    def increase_snake(self, snake):
        if snake[-1].move == K_UP:  # The new "block" appears behind the last one 
            new = Snake(snake[-1].rect.centerx,
                        snake[-1].rect.centery + Snake.LENGTH)
            new.move = snake[-1].move  # And takes the same direction
            snake.append(new)
        elif snake[-1].move == K_LEFT:
            new = Snake(snake[-1].rect.centerx + Snake.LENGTH,
                        snake[-1].rect.centery)
            new.move = snake[-1].move
            snake.append(new)
        elif snake[-1].move == K_DOWN:
            new = Snake(snake[-1].rect.centerx,
                        snake[-1].rect.centery - Snake.LENGTH)
            new.move = snake[-1].move
            snake.append(new)
        elif snake[-1].move == K_RIGHT:
            new = Snake(snake[-1].rect.centerx - Snake.LENGTH,
                        snake[-1].rect.centery)
            new.move = snake[-1].move
            snake.append(new)

    def follow_main(self, snake):  # Every iterable the block keeps its direction
        for s in range(1, len(snake)):  
            if snake[s - 1].move in (K_UP, K_DOWN):  # If the direction was changed by height 
                if snake[s].rect.centerx == snake[s - 1].rect.centerx:  # We define by width 
                    snake[s].move = snake[s - 1].move  
            elif snake[s - 1].move in (K_LEFT, K_RIGHT):  # If changed by width
                if snake[s].rect.centery == snake[s - 1].rect.centery:  # Define by height
                    snake[s].move = snake[s - 1].move

    @classmethod
    def is_collided(cls, snake):
        for s in range(2, len(snake)):
            if snake[0].rect.colliderect(snake[s]):
                return True
        for move in snake[0].rect.center:
            if move < 5 or move > Game.W - 20:
                return True

    def game(self):
        SC_COLOR = (191, 44, 186)
        PINK = (230, 46, 211)
        YELLOW = (207, 227, 25)
        RED = (237, 7, 7)
        play_gr = Surface((Game.W - 20, Game.W - 20))

        while self.state:
            self.get_event(self.main)
            self.sc.fill(SC_COLOR)
            play_gr.fill(PINK)
            for block in self.obj_list:
                block.moving()
                play_gr.blit(block.surf, (block.rect.x, block.rect.y))
            play_gr.blit(self.apple.surf, (self.apple.rect.x,
                                           self.apple.rect.y))
            self.sc.blit(play_gr, (play_gr.get_rect().x+10,
                                   play_gr.get_rect().y+10))
            pg.display.update()
            self.follow_main(self.obj_list)

            if self.is_collided(self.obj_list):
                self.sc.fill(YELLOW)
                for block in self.obj_list:
                    block.surf.fill(RED)
                    self.sc.blit(block.surf, (block.rect.x, block.rect.y))
                pg.display.update()
                pg.time.delay(500)
                self.state = False

            if self.main.rect.colliderect(self.apple.rect):
                self.apple.rect = self.apple.set_location(10, Game.W-10)
                self.increase_snake(self.obj_list)

            self.clock.tick(30)
pg.init()
game = Game()
game.game()
pg.quit()
