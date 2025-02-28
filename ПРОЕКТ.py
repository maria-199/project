import pygame
from copy import deepcopy
from random import choice, randrange
import sys

pygame.init()  # Инициализация Pygame
# Цвета
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 128, 0)
GRAY = (192, 192, 192)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 600  # Установка размеров окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Создание окна с заданными размерами
pygame.display.set_caption("Тетрис")  # Установка заголовка окна игры

font = pygame.font.Font("font.ttf", 74)  # Шрифт для текста
button_font = pygame.font.Font("font.ttf", 48)


def draw_button(text, x, y, w, h, color):
    """
        Функция рисует кнопку
         text: Текст
         x: X-координата
         y: Y-координата
         w: Ширина
         h: Высота
         color: Цвет
        """
    pygame.draw.rect(screen, color, (x, y, w, h))
    button_text = button_font.render(text, True, BLACK)
    text_rect = button_text.get_rect(center=(x + w // 2, y + h // 2))
    screen.blit(button_text, text_rect)


def main_menu():
    while True:  # Основной цикл меню
        screen.fill(WHITE)
        # Создание и отображение заголовка
        title_text = font.render("ТЕТРИС", True, BLACK)
        title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
        screen.blit(title_text, title_rect)
        # Кнопки для выбора уровней
        draw_button("1 уровень", WIDTH // 4, HEIGHT // 2, 300, 50, GREEN)
        draw_button("2 уровень", WIDTH // 4, HEIGHT // 2 + 60, 300, 50, (150, 150, 150))

        pygame.display.flip()  # Обновление экрана

        for event in pygame.event.get():  # Обработка событий
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_x, mouse_y = event.pos
                    if WIDTH // 4 <= mouse_x <= WIDTH // 4 + 300:
                        if HEIGHT // 2 <= mouse_y <= HEIGHT // 2 + 50:
                            level1()
                        elif HEIGHT // 2 + 60 <= mouse_y <= HEIGHT // 2 + 110:
                            level2()


def level1():  # функция для создания 1 уровня
    while True:
        pygame.display.flip()
        w, h = 10, 17
        title = 45
        game_res = w * title, h * title
        res = 750, 800
        FPS = 60
        pygame.init()  # Создание окна
        sc = pygame.display.set_mode(res)
        game_sc = pygame.Surface(game_res)
        clock = pygame.time.Clock()
        grid = [pygame.Rect(x * title, y * title, title, title) for x in range(w) for y in range(h)]  # Создание сетки

        figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                       [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                       [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                       [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                       [(0, 0), (0, -1), (0, 1), (-1, -1)],
                       [(0, 0), (0, -1), (0, 1), (1, -1)],
                       [(0, 0), (0, -1), (0, 1), (-1, 0)]]
        figures = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
        figure_rect = pygame.Rect(0, 0, title - 2, title - 2)
        field = [[0 for i in range(w)] for j in range(h)]
        anim_count, anim_speed, anim_limit = 0, 100, 2000  # параметры для анимации
        # Загрузка фонов
        bg = pygame.image.load('bg.jpg').convert()
        game_bg = pygame.image.load('bg2.jpg').convert()
        # Создание текста заголовков
        main_font = pygame.font.Font('font.ttf', 65)
        font = pygame.font.Font('font.ttf', 45)
        title_tetris = main_font.render('TETRIS', True, pygame.Color('white'))
        title_score = font.render('score:', True, pygame.Color('white'))
        title_record = font.render('record:', True, pygame.Color('white'))
        # Получение рандомного цвета
        get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

        fig, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
        color, next_color = get_color(), get_color()

        score, lines = 0, 0
        scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}  # Бонусы за линии

        def check_borders():  # Функция для проверки границ фигуры
            if fig[i].x < 0 or fig[i].x > w - 1:
                return False
            elif fig[i].y > h - 1 or field[fig[i].y][fig[i].x]:
                return False
            return True

        def get_record():  # Функция для получения рекорда
            try:
                with open('record') as f:
                    return f.readline()
            except FileNotFoundError:
                with open('record', 'w') as f:
                    f.write('0')

        def set_record(record, score):  # Функция для установки рекорда
            rec = max(int(record), score)
            with open('record', 'w') as f:
                f.write(str(rec))

        while True:
            record = get_record()  # Получение текущего рекорда
            dx, rotate = 0, False  # Инициализация переменных для перемещения
            sc.blit(bg, (0, 0))  # Отображение фонового изображения
            sc.blit(game_sc, (20, 20))  # Отображение игровой поверхности
            game_sc.blit(game_bg, (0, 0))  # Отображение фона игры
            for i in range(lines):
                pygame.time.wait(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_DOWN:
                        anim_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True
            # передвижение по x
            figure_old = deepcopy(fig)
            for i in range(4):
                fig[i].x += dx
                if not check_borders():
                    fig = deepcopy(figure_old)
                    break
            # передвижение по y
            anim_count += anim_speed
            if anim_count > anim_limit:
                anim_count = 0
                figure_old = deepcopy(fig)
                for i in range(4):
                    fig[i].y += 1
                    if not check_borders():
                        for i in range(4):
                            field[figure_old[i].y][figure_old[i].x] = color
                        fig, color = next_figure, next_color
                        next_figure, next_color = deepcopy(choice(figures)), get_color()
                        anim_limit = 2000
                        break
            # поворот фигуры
            center = fig[0]
            figure_old = deepcopy(fig)
            if rotate:
                for i in range(4):
                    x = fig[i].y - center.y
                    y = fig[i].x - center.x
                    fig[i].x = center.x - x
                    fig[i].y = center.y + y
                    if not check_borders():
                        fig = deepcopy(figure_old)
                        break

            line, lines = h - 1, 0
            for row in range(h - 1, -1, -1):
                count = 0
                for i in range(w):
                    if field[row][i]:
                        count += 1
                    field[line][i] = field[row][i]
                if count < w:
                    line -= 1
                else:
                    anim_speed += 3  # Увеличение скорости анимации за заполненные линии
                    lines += 1

            score += scores[lines]
            # отрисовка сетки
            [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
            # отрисовка фигуры
            for i in range(4):
                figure_rect.x = fig[i].x * title
                figure_rect.y = fig[i].y * title
                pygame.draw.rect(game_sc, color, figure_rect)
            # отрисовка падения
            for y, raw in enumerate(field):
                for x, col in enumerate(raw):
                    if col:
                        figure_rect.x, figure_rect.y = x * title, y * title
                        pygame.draw.rect(game_sc, col, figure_rect)
            # отрисовка следующей фигуры
            for i in range(4):
                figure_rect.x = next_figure[i].x * title + 380
                figure_rect.y = next_figure[i].y * title + 185
                pygame.draw.rect(sc, next_color, figure_rect)
            # отрисовка результатов
            sc.blit(title_tetris, (485, 10))
            sc.blit(title_score, (535, 630))
            sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 690))
            sc.blit(title_record, (525, 500))
            sc.blit(font.render(record, True, pygame.Color('white')), (550, 560))
            # конец игры
            for i in range(w):
                if field[0][i]:
                    set_record(record, score)
                    field = [[0 for i in range(w)] for i in range(h)]
                    anim_count, anim_speed, anim_limit = 0, 100, 2000
                    score = 0
                    for i_rect in grid:
                        pygame.draw.rect(game_sc, get_color(), i_rect)
                        sc.blit(game_sc, (20, 20))
                        pygame.display.flip()
                        clock.tick(100)

            pygame.display.flip()
            clock.tick(FPS)


# функция level2 повторяет фукцию level1 кроме значений некоторых переменных
def level2():  # функция для создания 2 уровня
    while True:
        pygame.display.flip()
        w, h = 8, 15
        title = 45
        game_res = w * title, h * title
        res = 750, 780
        FPS = 60
        pygame.init()  # Создание окна
        sc = pygame.display.set_mode(res)
        game_sc = pygame.Surface(game_res)
        clock = pygame.time.Clock()
        grid = [pygame.Rect(x * title, y * title, title, title) for x in range(w) for y in range(h)]  # Создание сетки

        figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
                       [(0, -1), (-1, -1), (-1, 0), (0, 0)],
                       [(-1, 0), (-1, 1), (0, 0), (0, -1)],
                       [(0, 0), (-1, 0), (0, 1), (-1, -1)],
                       [(0, 0), (0, -1), (0, 1), (-1, -1)],
                       [(0, 0), (0, -1), (0, 1), (1, -1)],
                       [(0, 0), (0, -1), (0, 1), (-1, 0)]]
        figures = [[pygame.Rect(x + w // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
        figure_rect = pygame.Rect(0, 0, title - 2, title - 2)
        field = [[0 for i in range(w)] for j in range(h)]
        anim_count, anim_speed, anim_limit = 0, 60, 2000  # параметры для анимации
        # Загрузка фонов
        bg = pygame.image.load('bg.jpg').convert()
        game_bg = pygame.image.load('bg2.jpg').convert()
        # Создание текста заголовков
        main_font = pygame.font.Font('font.ttf', 65)
        font = pygame.font.Font('font.ttf', 45)
        title_tetris = main_font.render('TETRIS', True, pygame.Color('white'))
        title_score = font.render('score:', True, pygame.Color('white'))
        title_record = font.render('record:', True, pygame.Color('white'))
        # Получение рандомного цвета
        get_color = lambda: (randrange(30, 256), randrange(30, 256), randrange(30, 256))

        fig, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))
        color, next_color = get_color(), get_color()

        score, lines = 0, 0
        scores = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}  # Бонусы за линии

        def check_borders():  # Функция для проверки границ фигуры
            if fig[i].x < 0 or fig[i].x > w - 1:
                return False
            elif fig[i].y > h - 1 or field[fig[i].y][fig[i].x]:
                return False
            return True

        def get_record():  # Функция для получения рекорда
            try:
                with open('record2') as f:
                    return f.readline()
            except FileNotFoundError:
                with open('record2', 'w') as f:
                    f.write('0')

        def set_record(record, score):  # Функция для установки рекорда
            rec = max(int(record), score)
            with open('record2', 'w') as f:
                f.write(str(rec))

        while True:
            record = get_record()  # Получение текущего рекорда
            dx, rotate = 0, False  # Инициализация переменных для перемещения
            sc.blit(bg, (0, 0))  # Отображение фонового изображения
            sc.blit(game_sc, (20, 20))  # Отображение игровой поверхности
            game_sc.blit(game_bg, (0, 0))  # Отображение фона игры
            for i in range(lines):
                pygame.time.wait(200)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        dx = -1
                    elif event.key == pygame.K_RIGHT:
                        dx = 1
                    elif event.key == pygame.K_DOWN:
                        anim_limit = 100
                    elif event.key == pygame.K_UP:
                        rotate = True
            # передвижение по x
            figure_old = deepcopy(fig)
            for i in range(4):
                fig[i].x += dx
                if not check_borders():
                    fig = deepcopy(figure_old)
                    break
            # передвижение по y
            anim_count += anim_speed
            if anim_count > anim_limit:
                anim_count = 0
                figure_old = deepcopy(fig)
                for i in range(4):
                    fig[i].y += 1
                    if not check_borders():
                        for i in range(4):
                            field[figure_old[i].y][figure_old[i].x] = color
                        fig, color = next_figure, next_color
                        next_figure, next_color = deepcopy(choice(figures)), get_color()
                        anim_limit = 2000
                        break
            # поворот фигуры
            center = fig[0]
            figure_old = deepcopy(fig)
            if rotate:
                for i in range(4):
                    x = fig[i].y - center.y
                    y = fig[i].x - center.x
                    fig[i].x = center.x - x
                    fig[i].y = center.y + y
                    if not check_borders():
                        fig = deepcopy(figure_old)
                        break

            line, lines = h - 1, 0
            for row in range(h - 1, -1, -1):
                count = 0
                for i in range(w):
                    if field[row][i]:
                        count += 1
                    field[line][i] = field[row][i]
                if count < w:
                    line -= 1
                else:
                    anim_speed += 3  # Увеличение скорости анимации за заполненные линии
                    lines += 1

            score += scores[lines]
            # отрисовка сетки
            [pygame.draw.rect(game_sc, (40, 40, 40), i_rect, 1) for i_rect in grid]
            # отрисовка фигуры
            for i in range(4):
                figure_rect.x = fig[i].x * title
                figure_rect.y = fig[i].y * title
                pygame.draw.rect(game_sc, color, figure_rect)
            # отрисовка падения
            for y, raw in enumerate(field):
                for x, col in enumerate(raw):
                    if col:
                        figure_rect.x, figure_rect.y = x * title, y * title
                        pygame.draw.rect(game_sc, col, figure_rect)
            # отрисовка следующей фигуры
            for i in range(4):
                figure_rect.x = next_figure[i].x * title + 380
                figure_rect.y = next_figure[i].y * title + 185
                pygame.draw.rect(sc, next_color, figure_rect)
            # отрисовка результатов
            sc.blit(title_tetris, (485, 10))
            sc.blit(title_score, (535, 630))
            sc.blit(font.render(str(score), True, pygame.Color('white')), (550, 690))
            sc.blit(title_record, (525, 500))
            sc.blit(font.render(record, True, pygame.Color('white')), (550, 560))
            # конец игры
            for i in range(w):
                if field[0][i]:
                    set_record(record, score)
                    field = [[0 for i in range(w)] for i in range(h)]
                    anim_count, anim_speed, anim_limit = 0, 60, 2000
                    score = 0
                    for i_rect in grid:
                        pygame.draw.rect(game_sc, get_color(), i_rect)
                        sc.blit(game_sc, (20, 20))
                        pygame.display.flip()
                        clock.tick(100)

            pygame.display.flip()
            clock.tick(FPS)


# Запуск программы
if __name__ == "__main__":
    main_menu()