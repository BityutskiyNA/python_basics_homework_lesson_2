import pygame
import sys
import random


def make_move(gamefield):
    """Функция выполняет хода компьютера
           Передаваемые параметры: gamefield - массив игрового поля"""
    free_cells = []
    for col in range(len(gamefield)):
        for row in range(len(gamefield[col])):
            if gamefield[col][row] == 0:
                free_cells.append((col, row))
    cell = random.sample(free_cells, 1)
    cell = cell[0]
    gamefield[cell[0]][cell[1]] = 2


def get_coordinates(point, iterations, variant):
    """Функция возвращает координаты точек по горизонтали и вертикали в зависимости от варианта
           Передаваемые параметры: iterations - количество итераций цикла зависит от длины ряда проигрыша
                                   point - точка которую проверяем
                                   variant - номер варианта расчета
                                       1 - это диагональ с лево на право
                                       2 - это диагональ с право на лево
                                       3 - это горизонталь
                                       4 - это вертикаль
           Результат: если по точке есть ряд из 5 фигур одного вида то возвращает 1 если нет 0"""
    diagonal = [point]
    x = 1
    while x <= iterations:
        if variant == 1:
            diagonal.append((point[0] + x, point[1] + x))
            diagonal.append((point[0] - x, point[1] - x))
        elif variant == 2:
            diagonal.append((point[0] + x, point[1] - x))
            diagonal.append((point[0] - x, point[1] + x))
        elif variant == 3:
            diagonal.append((point[0], point[1] + x))
            diagonal.append((point[0], point[1] - x))
        elif variant == 4:
            diagonal.append((point[0] + x, point[1]))
            diagonal.append((point[0] - x, point[1]))
        x = x + 1
    diagonal.sort()
    return diagonal


def check_point(mas, point):
    """Функция проверяет отдельную точку на пройгрыш в партии и возращает переменную game_over
       Передаваемые параметры: mas - игровое поле
                               point - точка которую проверяем
       Результат: если по точке есть ряд в 5 фигур одного вида то возвращает 1 если нет 0"""
    diog = []
    diog.append(get_coordinates(point, 4, 1))
    diog.append(get_coordinates(point, 4, 2))
    diog.append(get_coordinates(point, 4, 3))
    diog.append(get_coordinates(point, 4, 4))
    game_over = 0
    for col in range(len(diog)):
        line_crosses = 0
        string_zeros = 0
        for row in range(len(diog[col])):
            point = diog[col][row]
            if len(point) < 3:
                if (point[0] >= 0 and point[0] < 10) and (point[1] >= 0 and point[1] < 10):
                    if mas[point[0]][point[1]] == 1:
                        line_crosses = line_crosses + 1
                    elif mas[point[0]][point[1]] == 2:
                        string_zeros = string_zeros + 1
                    elif mas[point[0]][point[1]] == 0:
                        line_crosses = 0
                        string_zeros = 0

            if line_crosses == 5 or string_zeros == 5:
                game_over = 1
    return game_over


def check_array(main_array):
    """Функция проверяет все поле по каждой точке на пройгрыш
           Передаваемые параметры: main_array - массив игрового поля"""
    game_over = 0
    for col in range(len(main_array)):
        for line in range(len(main_array[col])):
            point_number = (col, line)
            if main_array[col][line] == 1:
                if game_over == 0:
                    game_over = check_point(main_array, point_number)
    return game_over

def Display_message(screen, message, font_color, background_color):
    """Функция выводит экран с нужным фоном и надписью
           Передаваемые параметры: screen - экран на который выводим сообщение
                                   message - текст сообщения
                                   font_color - цвет шрифта
                                   background_color - цвет фона"""
    screen.fill(background_color)
    font = pygame.font.SysFont('stxingkai', 80)
    text = font.render(message, True, font_color)
    text_rect = text.get_rect()
    text_x = screen.get_height() / 2 - text_rect.width / 2
    text_y = screen.get_width() / 2 - text_rect.height / 2
    screen.blit(text, [text_x, text_y])


if __name__ == '__main__':
    pygame.init()

    size = (510, 510)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Game")
    width = 40
    height = 40
    margin = 10
    white = (255, 255, 255)
    black = (0, 0, 0)
    field_array = []
    image_cross = pygame.image.load('cross.png').convert_alpha()
    image_zero = pygame.image.load('zero.png').convert_alpha()
    image_start = pygame.image.load('Start_game.png').convert_alpha()
    game_over = 0
    start_game = 0
    for i in range(10):
        field_array.append([0] * 10)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)
            elif event.type == pygame.MOUSEBUTTONDOWN: # Обарабатываем события нажатие мыши
                if start_game == 0:                    # Первый клик начало игры
                    start_game = 1
                    Display_message(screen, '', white, black)
                else:
                    x_mouse, y_mouse = pygame.mouse.get_pos() # клик по игроваому полю, выставляем крестик проверяем на
                    col = x_mouse // (margin + width)         # проверяем на окончание игры
                    row = y_mouse // (margin + height)        # делаем свой ход
                    if field_array[row][col] == 0:
                       field_array[row][col] = 1
                       game_over = check_array(field_array)
                       make_move(field_array)

        for row in range(10):
            for col in range(10):                         # выводим картинки крестика и нолика по состояния поля
                x = col * width + (col + 1) * margin
                y = row * width + (row + 1) * margin
                pygame.draw.rect(screen, white, (x, y, width, height))
                if field_array[row][col] == 1:
                    screen.blit(image_cross, (x, y))
                elif field_array[row][col] == 2:
                    screen.blit(image_zero, (x, y))
        if game_over == 1:                                 # если игра закончена то выводим экран окончания игры
            Display_message(screen, 'Game over', white, black)

        if start_game == 0:
            screen.blit(image_start, (0, 0))

        pygame.display.update()
