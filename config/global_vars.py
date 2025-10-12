import pygame

# font
font = pygame.font.Font("fonts/ChironHeiHK-Medium.ttf", 28)
font_bold = pygame.font.Font("fonts/ChironHeiHK-Black.ttf", 28)

# colors
color_light = (242, 211, 240)
color_normal = (194, 169, 192)
color_dark = (140, 94, 155)

# screen
game_name = "Automatontron"
pygame.display.set_caption(game_name)

game_icon = pygame.image.load("assets/circle_initial.png")
pygame.display.set_icon(game_icon)

screen_width, screen_height = (1280, 720)
