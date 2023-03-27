import pygame
from pygame import *
from random import randint
from time import sleep


pygame.init()

pygame.mixer.init()

if pygame.mixer.get_init():
    class sounds():
        pass
else:
    print("WARNING: 'pygame.mixer' Module Is Missing or Has Malfunctioned")

class display_params():
    size = width, height = 960, 720
    title = "Conquest - Pygame"
    fill_color = 0, 0, 0
    icon = "images/icon.png"

icon_image_object = pygame.image.load(display_params.icon)

screen = pygame.display.set_mode(display_params.size)
pygame.display.set_caption(display_params.title)
pygame.display.set_icon(icon_image_object)

clock = pygame.time.Clock()

red = 255, 0, 0
orange = 175, 80, 0
yellow = 125, 125, 5
green = 0, 255, 0
cyan = 5, 125, 125
blue = 0, 0, 255
purple = 125, 5, 125
black = 0, 0, 0
white = 255, 255, 255

darkgrey = 100, 100, 100

colors = [red, orange, yellow, green, cyan, blue, purple, black, white]
unused_player_colors = colors[:]

Font = pygame.font.Font

# splash screen

background_image = pygame.image.load("images/menu_background2.png")
background_rect = background_image.get_rect()
background_rect.center = (0, 0)
scale = 5
size = background_image.get_size()
size = (size[0] * scale, size[1] * scale)
background_image = pygame.transform.scale(background_image, size)

word_cover_image = pygame.image.load("images/word_cover3.png")
word_cover_rect = word_cover_image.get_rect()
word_cover_rect.center = (480, 360)

font = Font(None, 80)
loading_text_image = font.render("Loading...", False, black)
loading_text_rect = loading_text_image.get_rect()
loading_text_rect.center = (480, 360)

screen.fill(darkgrey)
screen.blit(background_image, background_rect)
screen.blit(word_cover_image, word_cover_rect)
screen.blit(loading_text_image, loading_text_rect)
pygame.display.flip()

sleep(2)

# define helper functions

def get_player_color():
	global unused_player_colors
	color = unused_player_colors[randint(0, len(unused_player_colors))]
	unused_player_colors.remove(color)  # remove color from list to ensure no duplicate colors
	return color

def main():
    pass

def draw():
    pass

def start_game(game_type):
    match game_type:
        case "conquest_classic":
            play_game_classic()
        case "conquest_mission":
            play_game_mission()
        case "conquest_invasion":
            play_game_invasion()
        case "conquest_multiplayer":
            play_game_multiplayer()
        case _:
            raise TypeError("Game type not specified or not know.")

def play_game_classic():
    pass

def choose_game():
    choosing = true
    font = pygame.font.Font(None, 80)
    title_img = font.render("Main Menu", False, darkgrey)
    title_rect = title_img.get_rect()
    title_rect.center = (480, 200)

    font = pygame.font.Font(None, 64)
    classic_img = font.render("Conquest", False, darkgrey)
    classic_rect = classic_img.get_rect()
    classic_rect.center = (480, 270)
    
    mission_img = font.render("Mission", False, darkgrey)
    mission_rect = mission_img.get_rect()
    mission_rect.center = (480, 270)
    
    invasion_img = font.render("Invasion", False, darkgrey)
    invasion_rect = invasion_img.get_rect()
    invasion_rect.center = (480, 270)

    quit_img = font.render("Quit", False, darkgrey)
    quit_rect = quit_img.get_rect()
    quit_rect.center = (480, 340)

    word_cover_img = pygame.image.load("images/word_cover1.png")
    word_cover_rect = word_cover_img.get_rect()
    word_cover_rect.center = (480, 340)

    choose_has_blit = False

    while choosing is True:
        clock.tick(30)
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    choosing = False
                    menu_is_going = False

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
            pos = pygame.mouse.get_pos()
            if classic_rect.collidepoint(pos[0], pos[1]):
                choosing = False
                start_game("conquest_classic")
            elif mission_rect.collidepoint(pos[0], pos[1]):
                choosing = False
                start_game("conquest_mission")
            elif invasion_rect.collidepoint(pos[0], pos[1]):
                choosing = False
                start_game("conquest_invasion")
            elif multiplayer_rect.collidepoint(pos[0], pos[1]):
                choosing = False
                start_game("conquest_multiplayer")
            elif back_rect.collidepoint(pos[0], pos[1]):
                choosing = False

        if choose_has_blit is False:  # only blit once to save memory usage
            screen.fill(darkgrey)  # background may not fill whole screen, just in case
            screen.blit(background_image, background_rect)
            screen.blit(word_cover_img, word_cover_rect)
            screen.blit(title_img, title_rect)
            screen.blit(classic_img, classic_rect)
            screen.blit(mission_img, mission_rect)
            screen.blit(invasion_img, invasion_rect)
            screen.blit(quit_img, quit_rect)
            pygame.display.flip()
            choose_has_blit = True

menu_is_going = True  # starts with the menu

font = pygame.font.Font(None, 80)
title_img = font.render("Main Menu", False, darkgrey)
title_rect = title_img.get_rect()
title_rect.center = (480, 200)

font = pygame.font.Font(None, 60)
play_img = font.render("Play Game", False, darkgrey)
play_rect = play_img.get_rect()
play_rect.center = (480, 270)

quit_img = font.render("Quit", False, darkgrey)
quit_rect = quit_img.get_rect()
quit_rect.center = (480, 340)

word_cover_img = pygame.image.load("images/word_cover1.png")
word_cover_rect = word_cover_img.get_rect()
word_cover_rect.center = (480, 340)

menu_has_blit = False

while menu_is_going is True:
    clock.tick(30)
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu_is_going = False

    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
        pos = pygame.mouse.get_pos()
        if play_rect.collidepoint(pos[0], pos[1]):
            choose_game()
        elif quit_rect.collidepoint(pos[0], pos[1]):
            menu_is_going = False

    if menu_has_blit is False:  # only blit once to save memory usage
        screen.fill(darkgrey)
        screen.blit(background_image, background_rect)
        screen.blit(word_cover_img, word_cover_rect)
        screen.blit(title_img, title_rect)
        screen.blit(play_img, play_rect)
        screen.blit(quit_img, quit_rect)
        pygame.display.flip()
        menu_has_blit = True



