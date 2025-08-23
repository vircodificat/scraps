import pygame
from pygame.math import Vector2
from pygame import Color, Rect
import random


SQUARE_SIZE = 20
GRID_SIZE = (20, 20)
SCREEN_SIZE = (GRID_SIZE[0] * SQUARE_SIZE, GRID_SIZE[1] * SQUARE_SIZE)


def main():
    random.seed(0)
    pygame.init()

    screen = pygame.display.set_mode(SCREEN_SIZE)
    clock = pygame.time.Clock()

    running = True
    direction = 'stopped'
    snake = make_initial_snake()
    length = 1
    walls = make_initial_walls()
    apples = make_initial_apples(snake, walls)

    frame_time = 0
    new_direction = None

    while running:
        for event in pygame.event.get():
            #print(event)
            match event.type:
                case pygame.QUIT:
                    running = False
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_ESCAPE:
                            running = False
                        case pygame.K_r:
                            direction = 'stopped'
                            snake = make_initial_snake()
                            length = 1
                            walls = make_initial_walls()
                            apples = make_initial_apples(snake, walls)
                            new_direction = None

                        case pygame.K_LEFT:
                            if direction == 'up' or direction == 'down' or direction == 'stopped':
                                new_direction = 'left'
                        case pygame.K_RIGHT:
                            if direction == 'up' or direction == 'down' or direction == 'stopped':
                                new_direction = 'right'
                        case pygame.K_UP:
                            if direction == 'left' or direction == 'right' or direction == 'stopped':
                                new_direction = 'up'
                        case pygame.K_DOWN:
                            if direction == 'left' or direction == 'right' or direction == 'stopped':
                                new_direction = 'down'


        if frame_time > 100:
            frame_time = 0

            direction = new_direction

            old_head = snake[0]
            match direction:
                case 'up':
                    new_head = (old_head[0], old_head[1] + 1)
                case 'down':
                    new_head = (old_head[0], old_head[1] - 1)
                case 'left':
                    new_head = (old_head[0] - 1, old_head[1])
                case 'right':
                    new_head = (old_head[0] + 1, old_head[1])
                case _:
                    new_head = old_head

            if new_head in apples:
                length += 1
                apples.remove(new_head)
                apples.append(random_apple(snake, walls, apples))
            elif new_head in walls:
                direction = 'stopped'
            elif new_head in snake:
                direction = 'stopped'
            else:
                if old_head != new_head:
                    snake.insert(0, new_head)
                    if len(snake) > length:
                        snake.pop()

        screen.fill(Color("white"))
        draw_grid(screen)
        draw_walls(screen, walls)
        draw_snake(screen, snake)
        draw_apples(screen, apples)
        pygame.display.flip()

        frame_time += clock.tick()

    pygame.quit()


def draw_grid(screen):
    for x in range(1, GRID_SIZE[0]):
        start = Vector2(SQUARE_SIZE * x, 0)
        end = Vector2(SQUARE_SIZE * x, SCREEN_SIZE[1])
        pygame.draw.line(screen, Color("gray"), start, end)

    for y in range(1, GRID_SIZE[1]):
        start = Vector2(0, SQUARE_SIZE * y)
        end = Vector2(SCREEN_SIZE[0], SQUARE_SIZE * y)
        pygame.draw.line(screen, Color("gray"), start, end)


def draw_snake(screen, snake):
    for snake_segment in snake:
        draw_square(screen, snake_segment, Color("green"))

    draw_square(screen, snake[0], Color(0, 200, 0))


def draw_walls(screen, walls):
    for wall_segment in walls:
        draw_square(screen, wall_segment, Color("black"))


def draw_apples(screen, apples):
    for apple_segment in apples:
        draw_square(screen, apple_segment, Color("red"))


def draw_square(screen, square, color):
    x, y = square
    rect = Rect(SQUARE_SIZE * x, SCREEN_SIZE[1] - SQUARE_SIZE * (y + 1), SQUARE_SIZE, SQUARE_SIZE)
    pygame.draw.rect(screen, color, rect)


def make_initial_snake():
    initial_position = (GRID_SIZE[0] // 2, GRID_SIZE[1] // 2)
    snake = [initial_position]
    return snake


def make_initial_walls():
    walls = []
    for x in range(GRID_SIZE[0]):
        walls.append((x, 0))
        walls.append((x, GRID_SIZE[1] - 1))

    for y in range(GRID_SIZE[1]):
        walls.append((0, y))
        walls.append((GRID_SIZE[0] - 1, y))

    return walls


def make_initial_apples(snake, walls):
    apples = []
    num_apples = 2

    while len(apples) < num_apples:
        apples.append(random_apple(snake, walls, apples))

    return apples


def random_apple(snake, walls, apples):
    while True:
        square = random_square()
        if square not in snake and square not in walls and square not in apples:
            return square


def random_square():
    x = random.randint(0, GRID_SIZE[0] - 1)
    y = random.randint(0, GRID_SIZE[1] - 1)
    return (x, y)



if __name__ == '__main__':
    main()
