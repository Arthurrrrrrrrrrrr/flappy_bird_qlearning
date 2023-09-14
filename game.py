import pygame
import sys
import random
import numpy as np

pygame.init()

class GameAI:

    def __init__(self, fps):
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.game_active = True
        self.frame_iteration = 0
        self.score = 0
        self.current_pipe_idx = 0
        self.current_pipe = []

        self.gravity = 2
        self.bird_movement = 0

        self.screen = pygame.display.set_mode((288, 512))

        self.background = pygame.image.load('assets/background-day.png').convert()

        self.bird = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
        self.bird_rect = self.bird.get_rect(center=(50, 256))

        self.message = pygame.image.load("assets/message.png").convert_alpha()
        self.game_over_rect = self.message.get_rect(center=(144, 256))

        self.counter = pygame.image.load("assets/0.png").convert_alpha()
        self.counter_rect = self.counter.get_rect(center=(144, 60))

        self.pipe_surface = pygame.image.load("assets/pipe-green.png")
        self.pipe_list = []
        self.pipe_height = [200, 250, 300, 350, 400]

    def restart(self):
        self.bird_rect.center = (50, 256)
        self.bird_movement = 0
        self.pipe_list.clear()
        self.game_active = True
        self.score = 0
        self.frame_iteration = 0
        self.current_pipe_idx = 0

    def check_collision(self):
        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe):
                return False
        if self.bird_rect.top <= -50 or self.bird_rect.bottom >= 500:
            return False
        return True

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        top_pipe = self.pipe_surface.get_rect(bottomleft=(288, random_pipe_pos - 150))
        bottom_pipe = self.pipe_surface.get_rect(topleft=(288, random_pipe_pos))
        return bottom_pipe, top_pipe

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5
        return self.pipe_list

    def draw_pipes(self):
        for pipe in self.pipe_list:  
            if pipe.bottom >= 512:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def update_counter(self):
        if self.score >= 0 and self.score <= 9:
            counter = pygame.image.load("assets/" + str(self.score) + ".png").convert_alpha()
            return counter
        elif self.score >= 10 and self.score <= 99:
            tens = self.score // 10
            units = self.score % 10
            counter_tens = pygame.image.load("assets/" + str(tens) + ".png").convert_alpha()
            counter_units = pygame.image.load("assets/" + str(units) + ".png").convert_alpha()
            counter = pygame.Surface((counter_tens.get_width() + counter_units.get_width(), counter_tens.get_height()), pygame.SRCALPHA)
            counter.blit(counter_tens, (0, 0))
            counter.blit(counter_units, (counter_tens.get_width(), 0))
            return counter
        elif self.score >= 100 and self.score <= 999:
            hundreds = self.score // 100
            tens = (self.score % 100) // 10
            units = (self.score % 100) % 10
            counter_hundreds = pygame.image.load("assets/" + str(hundreds) + ".png").convert_alpha()
            counter_tens = pygame.image.load("assets/" + str(tens) + ".png").convert_alpha()
            counter_units = pygame.image.load("assets/" + str(units) + ".png").convert_alpha()
            counter = pygame.Surface((counter_hundreds.get_width() + counter_tens.get_width() + counter_units.get_width(), counter_hundreds.get_height()), pygame.SRCALPHA)
            counter.blit(counter_hundreds, (0, 0))
            counter.blit(counter_tens, (counter_hundreds.get_width(), 0))
            counter.blit(counter_units, (counter_hundreds.get_width() + counter_tens.get_width(), 0))
            return counter
        elif self.score >= 1000 and self.score <= 9999:
            thousands = self.score // 1000
            hundreds = (self.score % 1000) // 100
            tens = (self.score % 100) // 10
            units = (self.score % 100) % 10
            counter_thousands = pygame.image.load("assets/" + str(thousands) + ".png").convert_alpha()
            counter_hundreds = pygame.image.load("assets/" + str(hundreds) + ".png").convert_alpha()
            counter_tens = pygame.image.load("assets/" + str(tens) + ".png").convert_alpha()
            counter_units = pygame.image.load("assets/" + str(units) + ".png").convert_alpha()
            counter = pygame.Surface((counter_thousands.get_width() + counter_hundreds.get_width() + counter_tens.get_width() + counter_units.get_width(), counter_thousands.get_height()), pygame.SRCALPHA)
            counter.blit(counter_thousands, (0, 0))
            counter.blit(counter_hundreds, (counter_thousands.get_width(), 0))
            counter.blit(counter_tens, (counter_thousands.get_width() + counter_hundreds.get_width(), 0))
            counter.blit(counter_units, (counter_thousands.get_width() + counter_hundreds.get_width() + counter_tens.get_width(), 0))
            return counter
        else:
            counter = pygame.image.load("assets/0.png").convert_alpha()
            return counter

    def display_counter(self):
        self.screen.blit(self.counter, self.counter_rect)

    def update_ui(self):
        pygame.display.update()
        self.frame_iteration += 1
        self.clock.tick(self.fps)

    def get_values(self):
        pipe = self.current_pipe
        # horizontal distance between the bird and the next pipes
        horizontal_distance = self.bird_rect.right - pipe.left
        # vertical distance between the bird and the middle between the next pipes
        vertical_distance = self.bird_rect.centerx - pipe.top
        return horizontal_distance, vertical_distance

    def play_step_human(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 15
                if event.key == pygame.K_SPACE and not self.game_active:
                    self.restart()
        if self.frame_iteration % 32 == 0 and self.game_active:
            self.pipe_list.extend(self.create_pipe())
        if len(self.pipe_list) == 2:
            self.current_pipe = self.pipe_list[0]
        if  self.bird_rect.left > self.current_pipe.right :
            self.score += 1
            self.current_pipe_idx += 2
            self.current_pipe = self.pipe_list[self.current_pipe_idx]
        
        self.screen.blit(self.background, (0, 0))

        if self.game_active:
            self.bird_movement += self.gravity
            self.bird_rect.centery += self.bird_movement
            self.screen.blit(self.bird, self.bird_rect)
            self.pipe_list = self.move_pipes()
            self.draw_pipes()
            self.game_active = self.check_collision()

        self.counter = self.update_counter()
        self.display_counter()

        if not self.game_active:
            self.screen.blit(self.message, self.game_over_rect)
    
    def play_step_bot(self, action):

        # exit the game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        # action = jump
        if action == [1, 0]:
            self.bird_movement = 0
            self.bird_movement -= 15
        # create new pipes each 32 frames
        if self.frame_iteration % 32 == 0 and self.game_active:
            self.pipe_list.extend(self.create_pipe())
        # initialize current_pipe
        if len(self.pipe_list) == 2:
            self.current_pipe = self.pipe_list[0]
        # increment score and current_pipe when the bird pass the pipes
        if  self.bird_rect.left > self.current_pipe.right :
            self.score += 1
            self.current_pipe_idx += 2
            self.current_pipe = self.pipe_list[self.current_pipe_idx]
        # blit background
        self.screen.blit(self.background, (0, 0))
        # apply gravity, move bird, blit bird, move pipes, draw pipes, check collisions
        if self.game_active:
            self.bird_movement += self.gravity
            self.bird_rect.centery += self.bird_movement
            self.screen.blit(self.bird, self.bird_rect)
            self.pipe_list = self.move_pipes()
            self.draw_pipes()
            self.game_active = self.check_collision()
        # update and display counter
        self.counter = self.update_counter()
        self.display_counter()
        # return True if game over, False if not
        if not self.game_active:
            return True
        return False

# game = GameAI(fps = 30)
# game.game_active = True
# while True :
#     game.play_step_human()
#     game.update_ui()