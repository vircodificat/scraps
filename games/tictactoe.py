from dataclasses import dataclass
import pygame
from pygame.math import Vector2
from typing import Optional, Tuple, cast

WIDTH, HEIGHT = (800, 600)
MARK_SIZE = 64

BOARD_SIZE = 300

SFX_VOLUME = 0.3

screen: pygame.Surface = cast(pygame.Surface, None)
mark_x: pygame.Surface = cast(pygame.Surface, None)
mark_o: pygame.Surface = cast(pygame.Surface, None)

sound_x: pygame.Sound = cast(pygame.Sound, None)
sound_o: pygame.Sound = cast(pygame.Sound, None)

mouse_pos = Vector2(0, 0)

@dataclass
class Game:
    positions: list[Vector2]
    selected: Optional[Tuple[int, int]]
    selections: list[Tuple[int, int]]

    def current_player(self) -> int:
        return len(self.positions) % 2

    def hover(self, pos) -> None:
        delta = Vector2(WIDTH - BOARD_SIZE, HEIGHT - BOARD_SIZE) / 2

        game.selected = None

        for x in range(3):
            for y in range(3):
                top_left = (BOARD_SIZE * x / 3, BOARD_SIZE * y / 3) + delta
                bot_right = (BOARD_SIZE * (x + 1) / 3, BOARD_SIZE * (y + 1) / 3) + delta
                size = bot_right - top_left
                rect = pygame.rect.Rect(top_left, size)
                if rect.collidepoint(pos):
                    game.selected = (x, y)
                    break

    def click(self, pos) -> None:
        if self.selected is not None:
            if self.selected not in self.selections:
                self.positions.append(mouse_pos)
                self.selections.append(self.selected)
                #print(self.selections)
                if self.current_player() == 0:
                    sound_x.play()
                else:
                    sound_o.play()


game: Game = cast(Game, None)

def main():
    global screen, mark_x, mark_o, mouse_pos, sound_x, sound_o

    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    running = True

    mark_x = pygame.transform.scale(
        pygame.image.load('assets/xmark.png'),
        (MARK_SIZE, MARK_SIZE),
    )

    mark_o = pygame.transform.scale(
        pygame.image.load('assets/omark.png'),
        (MARK_SIZE, MARK_SIZE),
    )

    sound_x = pygame.mixer.Sound('assets/chess_clink.wav')
    sound_x.set_volume(SFX_VOLUME)
    sound_o = pygame.mixer.Sound('assets/chess_plop.wav')
    sound_o.set_volume(SFX_VOLUME)

    reset()

    try:
        while running:
            for event in pygame.event.get():
                #print(event)
                match event.type:
                    case pygame.QUIT:
                        running = False
                    case pygame.MOUSEMOTION:
                        mouse_pos = event.pos
                        game.hover(mouse_pos)
                    case pygame.MOUSEBUTTONDOWN:
                        game.click(mouse_pos)
                    case pygame.KEYDOWN:
                        match event.key:
                            case pygame.K_ESCAPE:
                                running = False
                            case pygame.K_r:
                                reset()

            render()

            clock.tick(60)


    except KeyboardInterrupt:
        pass

    pygame.quit()


def reset():
    global game
    game = Game(
        positions=[],
        selected=(1, 1),
        selections=[],
    )


def render():
    screen.fill((0, 255, 0))

    draw_grid()
    draw_marks()

    pygame.display.flip()


def draw_grid():
    black = (0, 0, 0)
    width = 3

    delta = Vector2(WIDTH - BOARD_SIZE, HEIGHT - BOARD_SIZE) / 2


    if game.selected is not None:
        x, y = game.selected
        yellow = (255, 255, 0)
        top_left = (BOARD_SIZE * x / 3, BOARD_SIZE * y / 3) + delta
        bot_right = (BOARD_SIZE * (x + 1) / 3, BOARD_SIZE * (y + 1) / 3) + delta
        size = bot_right - top_left
        rect = pygame.rect.Rect(top_left, size)
        pygame.draw.rect(screen, yellow, rect)

    for i in range(4):
        # vertical
        start_pos = (BOARD_SIZE * i / 3,          0) + delta
        end_pos   = (BOARD_SIZE * i / 3, BOARD_SIZE) + delta
        pygame.draw.line(screen, black, start_pos, end_pos, width=width)

        # horizontal
        start_pos = (         0, BOARD_SIZE * i / 3) + delta
        end_pos   = (BOARD_SIZE, BOARD_SIZE * i / 3) + delta
        pygame.draw.line(screen, black, start_pos, end_pos, width=width)
        pygame.draw.line(screen, black, start_pos, end_pos, width=width)


def draw_marks():
    for i, pos in enumerate(game.positions):
        player = i % 2
        draw_mark(player, pos)

    draw_mark(game.current_player(), mouse_pos)


def draw_mark(player, pos) -> None:
    blit_pos = pos - Vector2(MARK_SIZE / 2, MARK_SIZE / 2)

    if player == 0:
        mark = mark_x
    else:
        mark = mark_o

    screen.blit(mark, blit_pos)


if __name__ == "__main__":
    main()
