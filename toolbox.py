import pygame
import math


# функция поворота картинки
def getRotatedImage(image, rect, angle):
    new_image = pygame.transform.rotate(image, angle)
    new_rect = new_image.get_rect(center=rect.center)
    return new_image, new_rect

# функция возврата угла между 2мя точками
def angleBetweenPoints(x1, y1, x2, y2):
    x_diff = x2 - x1
    y_diff = y2 - y1
    angle = math.degrees(math.atan2(-y_diff, x_diff))
    return angle

# функция возврата координат центра экрана
def centerCoords(img, screen):
    new_x = screen.get_width() /2 - img.get_width() /2
    new_y = screen.get_height() / 2 - img.get_height() / 2

    return new_x, new_y