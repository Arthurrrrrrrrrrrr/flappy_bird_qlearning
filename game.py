import pygame
import sys
import random

pygame.init()

class GameAI:

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.reset()

    def reset(self):
        self.game_active = True

        self.score = 0
        self.frame_iteration = 0

        self.gravity = 0.25
        self.bird_movement = 0

        self.vertical_distance = 0
        self.vertical_distance_top_pipe = 0
        self.vertical_distance_bottom_pipe = 0
        self.horizontal_distance = 0
        self.vertical_distance_to_bottom = 0
        self.vertical_distance_to_top = 0
        self.prev_bird_y = 0
        self.vertical_speed = 0

        self.screen = pygame.display.set_mode((576, 1024))

        self.background = pygame.image.load('assets/background-day.png').convert()
        self.background = pygame.transform.scale2x(self.background)

        self.bird = pygame.image.load('assets/bluebird-midflap.png').convert_alpha()
        self.bird = pygame.transform.scale2x(self.bird)
        self.bird_rect = self.bird.get_rect(center=(100, 512))

        self.floor_base = pygame.image.load("assets/base.png").convert()
        self.floor_base = pygame.transform.scale2x(self.floor_base)
        self.floor_x_pos = 0

        self.message = pygame.image.load("assets/message.png").convert_alpha()
        self.message = pygame.transform.scale2x(self.message)
        self.game_over_rect = self.message.get_rect(center=(288, 512))

        self.counter = pygame.image.load("assets/0.png").convert_alpha()
        self.counter = pygame.transform.scale2x(self.counter)
        self.counter_rect = self.counter.get_rect(center=(288, 200))

        self.pipe_surface = pygame.image.load("assets/pipe-green.png")
        self.pipe_surface = pygame.transform.scale2x(self.pipe_surface)
        self.pipe_list = []
        self.pipe_height = [400, 600, 800]
        self.SPAWNPIPE = pygame.USEREVENT
        pygame.time.set_timer(self.SPAWNPIPE, 1200)

    def get_game_state(self):
        v_d_t_p = abs(self.vertical_distance_top_pipe)/1450
        if self.vertical_distance_top_pipe < 0:
            s_v_d_t_p = 0 
        else:
            s_v_d_t_p = 1
        v_d_b_p = abs(self.vertical_distance_bottom_pipe)/850
        if self.vertical_distance_bottom_pipe < 0:
            s_v_d_b_p = 0
        else :
            s_v_d_b_p = 1
        h_d = abs(self.horizontal_distance)/650
        v_s = abs(self.vertical_speed)/650
        if self.vertical_speed < 0:
            s_v_s = 0
        else:
            s_v_s = 1

        return v_d_t_p, s_v_d_t_p, v_d_b_p, s_v_d_b_p, h_d, v_s, s_v_s

    def game_floor(self):
        self.screen.blit(self.floor_base, (self.floor_x_pos, 900))
        self.screen.blit(self.floor_base, (self.floor_x_pos + 576, 900))

    def check_collision(self):
        for pipe in self.pipe_list:
            if self.bird_rect.colliderect(pipe):
                return False
        if self.bird_rect.top <= -100 or self.bird_rect.bottom >= 900:
            return False
        return True

    def create_pipe(self):
        random_pipe_pos = random.choice(self.pipe_height)
        top_pipe = self.pipe_surface.get_rect(midbottom=(700, random_pipe_pos - 300))
        bottom_pipe = self.pipe_surface.get_rect(midtop=(700, random_pipe_pos))
        return bottom_pipe, top_pipe

    def move_pipes(self):
        for pipe in self.pipe_list:
            pipe.centerx -= 5
        return self.pipe_list

    def draw_pipes(self):
        for pipe in self.pipe_list:  
            if pipe.bottom >= 1024:
                self.screen.blit(self.pipe_surface, pipe)
            else:
                flip_pipe = pygame.transform.flip(self.pipe_surface, False, True)
                self.screen.blit(flip_pipe, pipe)

    def update_counter(self):
        self.score = len(self.pipe_list) // 2 - 1
        if self.score >= 0 and self.score <= 9:
            counter = pygame.image.load("assets/" + str(self.score) + ".png").convert_alpha()
            counter = pygame.transform.scale2x(counter)
            return counter
        elif self.score >= 10 and self.score <= 99:
            tens = self.score // 10
            units = self.score % 10
            counter_tens = pygame.image.load("assets/" + str(tens) + ".png").convert_alpha()
            counter_units = pygame.image.load("assets/" + str(units) + ".png").convert_alpha()
            counter_tens = pygame.transform.scale2x(counter_tens)
            counter_units = pygame.transform.scale2x(counter_units)
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
            counter_hundreds = pygame.transform.scale2x(counter_hundreds)
            counter_tens = pygame.transform.scale2x(counter_tens)
            counter_units = pygame.transform.scale2x(counter_units)
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
            counter_thousands = pygame.transform.scale2x(counter_thousands)
            counter_hundreds = pygame.transform.scale2x(counter_hundreds)
            counter_tens = pygame.transform.scale2x(counter_tens)
            counter_units = pygame.transform.scale2x(counter_units)
            counter = pygame.Surface((counter_thousands.get_width() + counter_hundreds.get_width() + counter_tens.get_width() + counter_units.get_width(), counter_thousands.get_height()), pygame.SRCALPHA)
            counter.blit(counter_thousands, (0, 0))
            counter.blit(counter_hundreds, (counter_thousands.get_width(), 0))
            counter.blit(counter_tens, (counter_thousands.get_width() + counter_hundreds.get_width(), 0))
            counter.blit(counter_units, (counter_thousands.get_width() + counter_hundreds.get_width() + counter_tens.get_width(), 0))
            return counter
        else:
            counter = pygame.image.load("assets/0.png").convert_alpha()
            counter = pygame.transform.scale2x(counter)
            return counter

    def display_counter(self):
        self.screen.blit(self.counter, self.counter_rect)

    def update_distances_speed(self):
        # Calculate vertical and horizontal distance to the next pipe
        if len(self.pipe_list) > 1:
            next_pipe = self.pipe_list[-1]
            self.vertical_distance = abs(next_pipe.bottom + 150 - self.bird_rect.centery)
            self.vertical_distance_top_pipe = next_pipe.top - self.bird_rect.top
            self.vertical_distance_bottom_pipe = self.bird_rect.bottom - next_pipe.bottom
            self.horizontal_distance = next_pipe.centerx - self.bird_rect.centerx
        else:
            self.vertical_distance = 0
            self.vertical_distance_top_pipe = 0
            self.vertical_distance_bottom_pipe = 0
            self.horizontal_distance = 0
        # Calculate vertical distance to bottom of the screen
        self.vertical_distance_to_bottom = 1024 - self.bird_rect.bottom
        # Calculate vertical distance to top of the screen
        self.vertical_distance_to_top = self.bird_rect.top
        # Calculate vertical speed
        bird_y = self.bird_rect.centery
        self.vertical_speed = bird_y - self.prev_bird_y
        # Update the previous vertical position with the current position
        self.prev_bird_y = bird_y

    def play_step_human(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and self.game_active:
                    self.bird_movement = 0
                    self.bird_movement -= 10 
                if event.key == pygame.K_SPACE and not self.game_active:
                    self.bird_rect.center = (100, 512)
                    self.bird_movement = 0
                    self.pipe_list.clear()
                    self.game_active = True
            if event.type == self.SPAWNPIPE and self.game_active:
                self.pipe_list.extend(self.create_pipe())

        self.screen.blit(self.background, (0, 0))

        if self.game_active:
            self.bird_movement += self.gravity
            self.bird_rect.centery += self.bird_movement
            self.screen.blit(self.bird, self.bird_rect)

            self.pipe_list = self.move_pipes()
            self.draw_pipes()

            self.game_active = self.check_collision()

            self.update_distances_speed()

        self.counter = self.update_counter()
        self.display_counter()

        if not self.game_active:
            self.screen.blit(self.message, self.game_over_rect)

        self.floor_x_pos -= 1
        self.game_floor()
        if self.floor_x_pos <= -576:
            self.floor_x_pos = 0
    
    def play_step_bot(self, action):

        done = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == self.SPAWNPIPE and self.game_active:
                self.pipe_list.extend(self.create_pipe())
        if action[0] == 1 and self.game_active:
            self.bird_movement = 0
            self.bird_movement -= 10
        if not self.game_active: #reset
            self.bird_rect.center = (100, 512)
            self.bird_movement = 0
            self.pipe_list.clear()
            self.game_active = True

        self.screen.blit(self.background, (0, 0))

        if self.game_active:
            self.bird_movement += self.gravity
            self.bird_rect.centery += self.bird_movement
            self.screen.blit(self.bird, self.bird_rect)

            self.pipe_list = self.move_pipes()
            self.draw_pipes()

            self.game_active = self.check_collision()

            self.update_distances_speed()

        self.counter = self.update_counter()
        self.display_counter()

        if not self.game_active:
            self.screen.blit(self.message, self.game_over_rect)
            done = True

        self.floor_x_pos -= 1
        self.game_floor()
        if self.floor_x_pos <= -576:
            self.floor_x_pos = 0

        return done

    def update_ui(self):
        pygame.display.update()
        self.clock.tick(120)

# game = GameAI()
# game.game_active = True
# max = [0, 0, 0, 0, 0, 0, 0]
# min = [1000, 1000, 1000, 1000, 1000, 1000, 1000] 
# while True :
#     game.play_step_human()
#     for i in range(len(max)):
#         if max[i] < game.get_game_state()[i]:
#             max[i] = game.get_game_state()[i]
#         if min[i] > game.get_game_state()[i]:
#             min[i] = game.get_game_state()[i]
#     print(max, min)
#     game.update_ui()