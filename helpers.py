import pygame

def draw_horizontal_dashed_line(surf, colour, start_pos, end_pos, width=1, dash_length=10):
    length = end_pos[0] - start_pos[0]
    y_value = start_pos[1]
    for index in range(0, length//dash_length, 2):
        start = start_pos[0] + (index * dash_length)
        end = start_pos[0] + ((index + 1) * dash_length)
        pygame.draw.line(surf, colour, (start, y_value), (end, y_value), width)
