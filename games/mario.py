import pygame
from pygame import Color, Rect
from pygame.math import Vector2

from dataclasses import dataclass
from typing import Optional, Any

SCREEN_SIZE = (800, 600)


@dataclass
class PlayerInput:
    dir: Optional[str] = None
    jump: bool = False
    quit: bool = False


@dataclass
class Wall:
    bottom_left: Vector2
    upper_right: Vector2


class Game:
    def __init__(self):
        self.frame = 0

        self.camera_offset = Vector2(0, 0)
        self.player = Vector2(SCREEN_SIZE[0]/2, SCREEN_SIZE[1]/2)
        self.player_vel = Vector2(0, 0)
        self.player_state = 'standing'
        self.player_state_frame = 0

        self.walls = [
            Wall(Vector2(0, 0), Vector2(100, 600)),
        ]

    def set_player_state(self, state):
        self.player_state = state
        self.player_state_frame = self.frame

    def frames_in_state(self):
        return self.frame - self.player_state_frame

    def world2screen(self, v: Vector2) -> Vector2:
        result = v.copy()
        result[1] = SCREEN_SIZE[1] - v[1]
        result + self.camera_offset
        return result

    def update(self, player_input: PlayerInput):
        self.frame += 1

        apply_friction = True

        match player_input.dir:
            case 'left':
                apply_friction = False
                if self.player_vel[0] > -10:
                    if self.player_vel[0] > 0:
                        self.player_vel[0] -= 2
                    else:
                        self.player_vel[0] -= 1
            case 'right':
                apply_friction = False
                if self.player_vel[0] < 10:
                    if self.player_vel[0] < 0:
                        self.player_vel[0] += 2
                    else:
                        self.player_vel[0] += 1

        match self.player_state:
            case 'standing':
                if apply_friction:
                    if self.player_vel[0] < 0:
                        self.player_vel[0] += 1
                    elif self.player_vel[0] > 0:
                        self.player_vel[0] -= 1

                if player_input.jump:
                    self.player_vel[1] = 10
                    self.set_player_state('preaerial')
            case 'preaerial':
                if not player_input.jump or self.frames_in_state() > 5:
                    self.set_player_state('aerial')
            case 'aerial':
                self.player_vel[1] -= 1
                if self.player[1] <= SCREEN_SIZE[1]/2:
                    self.player[1] = SCREEN_SIZE[1]/2
                    self.set_player_state('standing')
                    self.player_vel[1] = 0

        self.player += self.player_vel


def main():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    game = Game()

    while True:
        player_input = get_player_input()
        if player_input.quit:
            break
        game.update(player_input)
        render(screen, game)
        clock.tick(30)

    pygame.quit()


def get_player_input():
    player_input = PlayerInput()

    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT] and not keys[pygame.K_RIGHT]:
        player_input.dir = 'left'

    if keys[pygame.K_RIGHT] and not keys[pygame.K_LEFT]:
        player_input.dir = 'right'

    if keys[pygame.K_SPACE]:
        player_input.jump = True

    for event in pygame.event.get():
        match event.type:
            case pygame.QUIT:
                player_input.quit = True
            case pygame.KEYDOWN:
                match event.key:
                    case pygame.K_ESCAPE:
                        player_input.quit = True

    return player_input


def render(screen, game):
    screen.fill(Color("black"))
    draw_walls(screen, game)
    draw_player(screen, game)
    pygame.display.flip()


def draw_player(screen, game):
    player = game.world2screen(game.player)
    pygame.draw.circle(screen, Color("cyan"), player, 5)

def draw_walls(screen, game):
    for wall in game.walls:
        bottom_left = game.world2screen(wall.bottom_left)
        upper_right = game.world2screen(wall.upper_right)

        bottom_right = (upper_right[0], bottom_left[1])
        upper_left = (bottom_left[0], upper_right[1])
        dim = upper_right - bottom_left

        rect = Rect(bottom_right, dim)
        print(rect)
        pygame.draw.rect(screen, Color("white"), rect)


if __name__ == '__main__':
    main()
