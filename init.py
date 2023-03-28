# PYTHON 3
import pygame
from pygame import *
from random import randint
from time import sleep


pygame.init()

pygame.mixer.init()

if pygame.mixer.get_init():
    class sounds():
        def play_track(track, volume, repeat=20):
            pygame.mixer.music.load(track)
            pygame.mixer.music.set_volume(volume)
            pygame.mixer.music.play(repeat)
    pygame.mixer.music.load("music/background.wav")
    pygame.mixer.music.load("music/background2.wav")
    pygame.mixer.music.load("music/play.wav")
    pygame.mixer.music.load("music/battle.wav")
    pygame.mixer.music.load("music/win.wav")
else:
    raise ValueError("missing module 'pygame.mixer'")

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

darkgrey = 80, 80, 80
darkgrey2 = 60, 60, 70

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

sounds.play_track("music/background.wav", 0.5)

sleep(1)

# player / map classes

players = {} # list of all players

def get_player_color():
	global unused_player_colors
	color = unused_player_colors[randint(0, len(unused_player_colors))]
	unused_player_colors.remove(color)  # remove color from list to ensure no duplicate colors
	return color

class Player:
    def __init__(self, name="player1",):
        self.name = name
        self.display_name = name[:1].upper() + name[1:] # Change name to uppercase first letter
        self.color = get_player_color()

class Bot(Player):
    def __init__(self, name=""):
        self.name = name
    def turn():
        pass # AI code to take a turn

class KeyPlayer(Player):
    def __init__(self, name=""):
        self.name = name

class Area:
    def __init__(self, name="", pos=(0, 0)):
        self.name = name
        self.display_name = name[:1].upper() + name[1:] # Change name to uppercase first letter
        self.image = pygame.image.load("images/area_" + name + ".png")  # ex: images/area_england.png
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.owner = ""
        self.count = 0

def joinplayer(name, ptype):
    players[name] = Player(name, ptype)

def leaveplayer(name):
    players[name] = None

"""
This is Where you want to go if you want to mod maps!

This is where all the map initialization happpens
"""


class europe:
    areas = []
    name = "europe"
    color = blue

europe.areas.append(Area("england", (0, 0)))
europe.areas.append(Area("franconia", (0, 0)))
europe.areas.append(Area("sweden", (0, 0)))
europe.areas.append(Area("spain", (0, 0)))
europe.areas.append(Area("moscovy", (0, 0)))
europe.areas.append(Area("germana", (0, 0)))
europe.areas.append(Area("ottoman", (0, 0)))

continents = [europe]

# define game object

class Game:
    def __init__(self, name="", maxturns=1000):
        self.continent = continents[randint(0, len(continents)) - 1]
        self.players = players
        self.name = name
        self.maxturns = maxturns
        self.background_image = pygame.image.load("images/ocean.png")
        self.background_rect = self.background_image.get_rect()
        self.background_rect.center = pos
        self.selected_area = None
    def attack(attack_area, selected_area, _):
        if selected_area.count < 1:
            return True, attack_area, selected_area
        match self.name:
            case "conquest_classic":
                lose_win = randint(0, 11)
                if lose_win < 5:
                    attack_area.count -= 1
                else:
                    selected_area.count -= 1
            case "conquest_mission":
                lose_win = randint(0, 11)
                if lose_win < 5:
                    attack_area.count -= 1
                else:
                    selected_area.count -= 1
            case "conquest_invasion":
                lose_win = randint(0, 11)
                if lose_win < 5:
                    attack_area.count -= 1
                else:
                    selected_area.count -= 1
            case "conquest_multiplayer":
                print("multiplayer unsupported")
        if attack_area.count < 1:
            attack_area.owner = "player1"
            attack_area.count = 1
            selected_area.count -= 1
        return False, attack_area, selected_area
        

# define helper functions

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
            raise ValueError("Game type not specified or not known.")

def play_game_classic():
    sounds.play_track("music/play.wav", 0.5)
    game = Game("conquest_classic")
    game.players = {"player1" : KeyPlayer("player1"), "bot1" : Bot("bot1")}
    random_area = randint(0, len(game.continent.areas) - 1)
    game.continent.areas[random_area].owner = "player1"
    game.continent.areas[random_area - 1].owner = "bot1"
    turns = 0
    has_quit = False
    has_won = False
    while game.maxturns > turns and has_quit is False and not has_won is True:
        screen.fill(black)
        screen.blit(game.background_image, game.background_rect)
        for area in range(len(game.continent.areas)):
            screen.blit(game.continent.areas[area].image, game.continent.areas[area].rect)
        turn = True
        while turn is True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                   turn = False
                   has_quit = True
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
                    pos = pygame.mouse.get_pos()
                    for area in range(len(game.continent.areas)):
                        loc = game.continent.areas[area]
                        if loc.rect.collidepoint(pos[0], pos[1]):
                            if loc.owner == "player1":
                                game.selected_area = loc
                            elif loc.owner == "bot1" or loc.owner == "":
                                turn, game.continent.areas[area], game.selected_area = game.attack(loc, game.selected_area)
        turns += 1
        #game.players["bot1"].turn()
    if has_won is True:
        win_game(game.players["player1"].name)
    else:
        lose_game()

def play_game_mission():
    sounds.play_track("music/play.wav", 0.5)

def play_game_invasion():
    sounds.play_track("music/play.wav", 0.5)

def play_game_multiplayer():
    sounds.play_track("music/play.wav", 0.5)
    print("Multiplayer is not implemented in this version, please just use singleplayer campaigns.")

def win_game(player):
    sounds.play_track("music/win.wav", 0.5)
    font = pygame.font.Font(None, 80)
    title_img = font.render("Game Stats", False, darkgrey)
    title_rect = title_img.get_rect()
    title_rect.center = (480, 200)
    
    font = pygame.font.Font(None, 48)
    stat_img = font.render(player + " wins!", False, darkgrey2)
    stat_rect = stat_img.get_rect()
    stat_rect.center = (480, 200 + 72 * 1)
    
    font = pygame.font.Font(None, 64)
    back_img = font.render("Main Menu", False, darkgrey2)
    back_rect = back_img.get_rect()
    back_rect.center = (480, 200 + 72 * 2)

    word_cover_img = pygame.image.load("images/word_cover1.png")
    word_cover_rect = word_cover_img.get_rect()
    word_cover_rect.center = (480, 340)
    
    win = True
    win_has_blit = False
    
    while win is True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
                menu_is_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(pos[0], pos[1]):
                    win = False

        if win_has_blit is False:  # only blit once to save memory usage
            screen.fill(darkgrey)  # background may not fill whole screen, just in case
            screen.blit(background_image, background_rect)
            screen.blit(word_cover_img, word_cover_rect)
            screen.blit(title_img, title_rect)
            screen.blit(stat_img, stat_rect)
            screen.blit(back_img, back_rect)
            pygame.display.flip()
            win_has_blit = True
    sounds.play_track("music/background.wav", 0.5)
    choosing = False
    win = False
    has_quit = True
    menu_is_going = True

def lose_game():
    sounds.play_track("music/lose.wav", 0.5)
    font = pygame.font.Font(None, 80)
    title_img = font.render("Game Stats", False, darkgrey)
    title_rect = title_img.get_rect()
    title_rect.center = (480, 200)
    
    font = pygame.font.Font(None, 48)
    stat_img = font.render("You Lose!", False, darkgrey2)
    stat_rect = stat_img.get_rect()
    stat_rect.center = (480, 200 + 72 * 1)
    
    font = pygame.font.Font(None, 64)
    back_img = font.render("Main Menu", False, darkgrey2)
    back_rect = back_img.get_rect()
    back_rect.center = (480, 200 + 72 * 2)

    word_cover_img = pygame.image.load("images/word_cover1.png")
    word_cover_rect = word_cover_img.get_rect()
    word_cover_rect.center = (480, 340)
    
    win = True
    win_has_blit = False
    
    while win is True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
                menu_is_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(pos[0], pos[1]):
                    win = False

        if win_has_blit is False:  # only blit once to save memory usage
            screen.fill(darkgrey)  # background may not fill whole screen, just in case
            screen.blit(background_image, background_rect)
            screen.blit(word_cover_img, word_cover_rect)
            screen.blit(title_img, title_rect)
            screen.blit(stat_img, stat_rect)
            screen.blit(back_img, back_rect)
            pygame.display.flip()
            win_has_blit = True
    sounds.play_track("music/background.wav", 0.5)
    choosing = False
    win = False
    menu_is_going = True

def choose_game():
    # setup
    choosing = True
    font = pygame.font.Font(None, 80)
    title_img = font.render("Choose Game", False, darkgrey)
    title_rect = title_img.get_rect()
    title_rect.center = (480, 200)

    font = pygame.font.Font(None, 64)
    classic_img = font.render("Conquest", False, darkgrey2)
    classic_rect = classic_img.get_rect()
    classic_rect.center = (480, 200 + 72 * 1)
    
    mission_img = font.render("Mission", False, darkgrey2)
    mission_rect = mission_img.get_rect()
    mission_rect.center = (480, 200 + 72 * 2)
    
    invasion_img = font.render("Invasion", False, darkgrey2)
    invasion_rect = invasion_img.get_rect()
    invasion_rect.center = (480, 200 + 72 * 3)
    
    multiplayer_img = font.render("Multiplayer", False, darkgrey2)
    multiplayer_rect = multiplayer_img.get_rect()
    multiplayer_rect.center = (480, 200 + 72 * 4)

    back_img = font.render("Back", False, darkgrey2)
    back_rect = back_img.get_rect()
    back_rect.center = (480, 200 + 72 * 5)

    word_cover_img = pygame.image.load("images/word_cover1.png")
    word_cover_rect = word_cover_img.get_rect()
    word_cover_rect.center = (480, 340)

    choose_has_blit = False

    sounds.play_track("music/background2.wav", 0.5)
    # actual frontend
    while choosing is True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                choosing = False
                menu_is_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
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
            screen.blit(multiplayer_img, multiplayer_rect)
            screen.blit(back_img, back_rect)
            pygame.display.flip()
            choose_has_blit = True
    sounds.play_track("music/background.wav", 0.5)
    return False

menu_is_going = True  # starts with the menu

font = pygame.font.Font(None, 80)
title_img = font.render("Main Menu", False, darkgrey)
title_rect = title_img.get_rect()
title_rect.center = (480, 200)

font = pygame.font.Font(None, 60)
play_img = font.render("Play", False, darkgrey2)
play_rect = play_img.get_rect()
play_rect.center = (480, 316)

quit_img = font.render("Quit", False, darkgrey2)
quit_rect = quit_img.get_rect()
quit_rect.center = (480, 372)

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
            menu_has_blit = choose_game()
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

