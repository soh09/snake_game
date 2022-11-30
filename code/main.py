import pygame
import sys
import game
from pygame.math import Vector2
import random

class Snake:
    def __init__(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0)
        self.grow = False
    
        self.head_up = pygame.image.load('snake/Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('snake/Graphics/head_down.png').convert_alpha()
        self.head_left = pygame.image.load('snake/Graphics/head_left.png').convert_alpha()
        self.head_right = pygame.image.load('snake/Graphics/head_right.png').convert_alpha()
		
        self.tail_up = pygame.image.load('snake/Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('snake/Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('snake/Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('snake/Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('snake/Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('snake/Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('snake/Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('snake/Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('snake/Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('snake/Graphics/body_bl.png').convert_alpha()

        self.head = self.head_right
        self.tail = self.tail_left

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            # making a rect for the block
            x = block.x * cell_size
            y = block.y * cell_size
            body_rect = pygame.Rect(x, y, cell_size, cell_size)

            # what direction is the face heading
            if index == 0: # drawing the head
                screen.blit(self.head, body_rect)
            elif index == (len(self.body) - 1): # drawing the tail
                screen.blit(self.tail, body_rect)
            else: # drawing the body
                prev_diff = self.body[index - 1] - block
                next_diff = block - self.body[index + 1]
                # if vectors are the same, aka this is a horizontal/vertical block
                if prev_diff == next_diff:
                    if prev_diff.y == 0: # if horizontal
                        screen.blit(self.body_horizontal, body_rect)
                    elif prev_diff.x == 0: # if vertical
                        screen.blit(self.body_vertical, body_rect)
                else:
                    # if the block is top right 
                    if prev_diff == Vector2(0, 1) and next_diff == Vector2(-1, 0) or prev_diff == Vector2(1, 0) and next_diff == Vector2(0, -1):
                        screen.blit(self.body_br, body_rect)
                    elif prev_diff == Vector2(0, 1) and next_diff == Vector2(1, 0) or prev_diff == Vector2(-1, 0) and next_diff == Vector2(0, -1):
                        screen.blit(self.body_bl, body_rect)
                    elif prev_diff == Vector2(0, -1) and next_diff == Vector2(1, 0) or prev_diff == Vector2(-1, 0) and next_diff == Vector2(0, 1):
                        screen.blit(self.body_tl, body_rect)
                    else:
                        screen.blit(self.body_tr, body_rect)

    def update_head_graphics(self):
        head_relations = self.body[1] - self.body[0]
        if head_relations == Vector2(1, 0): self.head = self.head_left
        elif head_relations == Vector2(-1, 0): self.head = self.head_right
        elif head_relations == Vector2(0, 1): self.head = self.head_up
        else: self.head = self.head_down

    def update_tail_graphics(self):
        tail_relations = self.body[-2] - self.body[-1]
        if tail_relations == Vector2(1, 0): self.tail = self.tail_left
        elif tail_relations == Vector2(-1, 0): self.tail = self.tail_right
        elif tail_relations == Vector2(0, 1): self.tail = self.tail_up
        else: self.tail = self.tail_down

    def move_snake(self):
        if self.grow == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.grow = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.grow = True

    def reset(self):
        self.body = [Vector2(7, 10), Vector2(6, 10), Vector2(5, 10)]
        self.direction = Vector2(0, 0) 

class Fruit:
    # create x and y pos
    # draw the fruit
    def __init__(self):
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)

    def draw_fruit(self):
        # create rectangle
        # draw it at self.pos
        fruit_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)

class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.score = 0
    
    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_dead()

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def draw_grass(self):
        for col in range(cell_num):
            for row in range(cell_num):
                if (col + row) % 2 == 0:
                    grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, (172, 208, 95), grass_rect)

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            # make new fruit and make snake longer
            self.fruit.randomize()
            # make sure that the new fruit is not 'on' the snake body
            while any([self.fruit.pos == body for body in self.snake.body]):
                self.fruit.randomize()
            self.snake.add_block()
            self.score += 1

    def check_dead(self):
        # check if the snake is out of bounds
        if not 0 <= self.snake.body[0].x < cell_num:
            self.game_over()
        if not 0 <= self.snake.body[0].y < cell_num:
            self.game_over()
        
        # check if the snake's head has collided with its head
        for block in self.snake.body[1:]:
            if self.snake.body[0] == block:
                self.game_over()

    def game_over(self):
        self.snake.reset()
        self.score = 0
    
    def draw_score(self):
        score_surface = game_font.render(str(self.score), True, (56, 74, 112))
        x = cell_size * cell_num - 60
        y = cell_size * cell_num - 60
        score_rect = score_surface.get_rect(center = (x, y))

        apple_rect = apple.get_rect(midright = (score_rect.left, score_rect.centery))

        bg_rect = pygame.Rect(apple_rect.left, apple_rect.top, score_rect.right - apple_rect.left + 10, apple_rect.height + 5)

        pygame.draw.rect(screen, (167, 209, 61), bg_rect)
        screen.blit(score_surface, score_rect)
        screen.blit(apple, apple_rect)
        pygame.draw.rect(screen, (56, 74, 112), bg_rect, 2)


pygame.init()

clock = pygame.time.Clock()
cell_size = 40
cell_num = 20
screen = pygame.display.set_mode((cell_size * cell_num, cell_size * cell_num))

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

apple = pygame.image.load('snake/Graphics/apple.png').convert_alpha()
game_font = pygame.font.Font('snake/Font/PoetsenOne-Regular.ttf', 50)

main_game = Main()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            main_game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if main_game.snake.direction.y != 1:
                    main_game.snake.direction = Vector2(0, -1)
            if event.key == pygame.K_DOWN:
                if main_game.snake.direction.y != -1:
                    main_game.snake.direction = Vector2(0, 1)
            if event.key == pygame.K_RIGHT:
                if main_game.snake.direction.x != -1:
                    main_game.snake.direction = Vector2(1, 0)
            if event.key == pygame.K_LEFT:
                if main_game.snake.direction.x != 1:
                    main_game.snake.direction = Vector2(-1, 0)

    screen.fill((179, 214, 101))
    main_game.draw_elements()
    pygame.display.update()
    clock.tick(60)