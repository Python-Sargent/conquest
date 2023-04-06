# PYTHON 3
import pygame
from pygame import *
from random import randint
from time import sleep

pygame.init()

pygame.mixer.init()

if pygame.mixer.get_init():
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


class DisplayParams:
    size = width, height = 1540, 980
    title = "Conquest - Pygame"
    fill_color = 0, 0, 0
    icon = "images/icon.png"
    text_size = 96
    title_size = 128
    center = (0, 0)

""" TODO this is for difficulty stuff (maybe later)
dificulty_mode = input(str("Enter Dificulty Mode (easy, normal, hard, dad): "))

class ModeData:
    def __init__(self, mode):
        self.mode = mode
        if self.mode == "normal":
            self.troop_gain = 1
            self.troop_loss = 1
        elif self.mode == "easy":
            self.troop_gain = 2
            self.troop_loss = 1
        elif self.mode == "hard":
            self.troop_gain = 1
            self.troop_loss = 2
        elif self.mode == "dad":
            self.troop_gain = 5
            self.troop_loss = 1
"""

DisplayParams.center = (DisplayParams.size[0] / 2, DisplayParams.size[1] / 2)

icon_image_object = pygame.image.load(DisplayParams.icon)

screen = pygame.display.set_mode(DisplayParams.size)
pygame.display.set_caption(DisplayParams.title)
pygame.display.set_icon(icon_image_object)

clock = pygame.time.Clock()

red = 255, 0, 0
orange = 175, 80, 0
yellow = 200, 200, 5
green = 0, 255, 0
cyan = 5, 125, 125
blue = 0, 0, 255
purple = 125, 5, 125
black = 0, 0, 0
white = 255, 255, 255

darkgrey = 80, 80, 80
darkgrey2 = 60, 60, 70

colors = [red, orange, yellow, green, cyan, blue, purple, black, white]

Font = pygame.font.Font

# splash screen

background_image = pygame.image.load("images/menu_background2.png")
background_rect = background_image.get_rect()
background_rect.center = (0, 0)
scale = 6
size = background_image.get_size()
size = (size[0] * scale, size[1] * scale)
background_image = pygame.transform.scale(background_image, size)

word_cover_image = pygame.image.load("images/word_cover1.png")
word_cover_rect = word_cover_image.get_rect()
word_cover_rect.center = (DisplayParams.center[0], DisplayParams.center[1])

font = Font(None, DisplayParams.title_size + 32)
loading_text_image = font.render("Loading...", False, black)
loading_text_rect = loading_text_image.get_rect()
loading_text_rect.center = (DisplayParams.center[0], DisplayParams.center[1])

screen.fill(darkgrey)
screen.blit(background_image, background_rect)
screen.blit(word_cover_image, word_cover_rect)
screen.blit(loading_text_image, loading_text_rect)
pygame.display.flip()

play_track("music/background.wav", 0.5)

sleep(1)

# splash screen end

word_cover_img = pygame.image.load("images/word_cover1.png")
word_cover_rect = word_cover_img.get_rect()
word_cover_rect.center = (DisplayParams.center[0], DisplayParams.center[1])

# player / map classes

players = {}  # list of all players

unused_player_colors = colors[:]

def get_player_color(game_type, player):
    if game_type == "singlplayer" and player == "player1":
        return blue
    elif game_type == "singlplayer" and player == "bot1":
        return red
    elif game_type == "singlplayer" and player == "gaia":
        return black
    player_color = unused_player_colors[randint(0, len(unused_player_colors) - 1)]
    unused_player_colors.remove(player_color)  # remove color from list to ensure no duplicate colors
    return player_color


class Player:
    def __init__(self, name="player1", game_type="singleplayer"):
        self.name = name
        self.display_name = name[:1].upper() + name[1:]  # Change name to uppercase first letter
        self.color = get_player_color(game_type, name)

    def turn(self, game):
        bot_turn = True
        bot_selectable_areas = []
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == self.name:
                bot_selectable_areas.append(game.continent.areas[area])
        if bot_selectable_areas:
            game.bot_selected_area = bot_selectable_areas[0]
        else:
            bot_turn = False
        bot_attackbles = []
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "player1" or game.continent.areas[area].owner == "":
                bot_attack = game.continent.areas[area]
                break
        bot_attack_index = 0
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "player1" or game.continent.areas[area].owner == "":
                if game.continent.areas[area].count < bot_attack.count:
                    bot_attack = game.continent.areas[area]
                    bot_attack_index = area
        while bot_turn is True and game.bot_selected_area.count > bot_attack.count * 5:
            print(self.display_name + " Attacking: " + game.continent.areas[bot_attack_index].name + ", From: " + game.bot_selected_area.name)
            bot_turn, game.continent.areas[bot_attack_index], game.bot_selected_area, has_succeded = game.attack(game.continent.areas[bot_attack_index], game.bot_selected_area)
            bot_selectable_areas.remove(game.bot_selected_area)
            if bot_selectable_areas:
                game.bot_selected_area = bot_selectable_areas[0]
            else:
                bot_turn = False
        return game.continent.areas


class Area:
    def __init__(self, name="", area_pos=(0, 0), offset=(0, 0)):
        self.name = name
        self.display_name = name[:1].upper() + name[1:]  # Change name to uppercase first letter
        self.image = pygame.image.load("images/area_" + name + ".png")  # ex: images/area_england.png
        self.rect = self.image.get_rect()
        self.rect.center = area_pos
        self.owner = ""
        self.count = 0
        self.count_pos_offset = offset


def add_player(name, ptype):
    players[name] = Player(name, ptype)


def remove_player(name):
    players[name] = None


"""
This is Where you want to go if you want to mod maps

This is where all the map initialization happpens
"""


# size = width, height = 960, 720

class Europe:
    areas = []
    name = "Europe"
    color = blue


Europe.areas.append(Area("england", (DisplayParams.center[0] - DisplayParams.center[0] / 2.25, DisplayParams.center[1] - DisplayParams.center[0] / 5.5), (0, 24)))
Europe.areas.append(Area("franconia", (DisplayParams.center[0] - DisplayParams.center[0] / 2.83, DisplayParams.center[1] + DisplayParams.center[0] / 9.9), (0, -32)))
Europe.areas.append(Area("sweden", (DisplayParams.center[0] - DisplayParams.center[0] / 8.6, DisplayParams.center[1] - DisplayParams.center[0] / 2.92), (0, 48)))
Europe.areas.append(Area("spain", (DisplayParams.center[0] - DisplayParams.center[0] / 2.05, DisplayParams.center[1] + DisplayParams.center[0] / 3.25), (0, -48)))
Europe.areas.append(Area("moscovy", (DisplayParams.center[0] + DisplayParams.center[0] / 3.15, DisplayParams.center[1] - DisplayParams.center[0] / 5.48), (0, 80)))
Europe.areas.append(Area("germana", (DisplayParams.center[0] - DisplayParams.center[0] / 7.5, DisplayParams.center[1] + DisplayParams.center[0] / 20), (0, 48)))
Europe.areas.append(Area("ottoman", (DisplayParams.center[0] + DisplayParams.center[0] / 3.23, DisplayParams.center[1] + DisplayParams.center[0] / 4.8), (0, -48)))

continents = [Europe]

menu_is_going = True  # starts with the menu


class HUD:
    def __init__(self):
        font = pygame.font.Font(None, 48)
        width = DisplayParams.size[0]
        heihgt = DisplayParams.size[1]
        self.end_turn_image = font.render("End Turn", True, red)
        self.end_turn_rect = self.end_turn_image.get_rect()
        self.end_turn_rect.center = (DisplayParams.center[0], 24)
        self.play_name_image = font.render("Player1", False, black)
        self.play_name_rect = self.play_name_image.get_rect()
        self.play_name_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - width / 20), 24)
        self.info_image = font.render("Enemies: Bot1(red)", False, black)
        self.info_rect = self.info_image.get_rect()
        self.info_rect.center = (DisplayParams.center[0] + (DisplayParams.center[0] - width / 8), 24)
        self.game_name_image = font.render("Game: Conquest Classic", False, black)
        self.game_name_rect = self.game_name_image.get_rect()
        self.game_name_rect.center = (DisplayParams.center[0], DisplayParams.size[1] - 24)
        self.select_image = font.render("Selected: ", False, black)
        self.select_rect = self.select_image.get_rect()
        self.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - width / 8), DisplayParams.size[1] - 24)
        self.turn_play_image = font.render("Turn: Player1", False, black)
        self.turn_play_rect = self.turn_play_image.get_rect()
        self.turn_play_rect.center = (DisplayParams.center[0] + (DisplayParams.center[0] - width / 8), DisplayParams.size[1] - 24)
        self.hudbar_image = pygame.image.load("images/hudbar.png")
        self.hudbar_top_rect = self.hudbar_image.get_rect()
        self.hudbar_top_rect.center = (DisplayParams.center[0], 24)
        self.hudbar_bottom_rect = self.hudbar_image.get_rect()
        self.hudbar_bottom_rect.center = (DisplayParams.center[0], DisplayParams.size[1] - 24)


class Game:
    def __init__(self, name="", maxturns=1000):
        self.continent = continents[randint(0, len(continents)) - 1]
        self.players = players
        self.name = name
        self.maxturns = maxturns
        self.background_image = pygame.image.load("images/ocean.png")
        self.background_rect = self.background_image.get_rect()
        self.background_rect.center = DisplayParams.center
        self.selected_area = None
        self.HUD = HUD()

    def attack(self, attack_area, selected_area):
        has_conquered = False
        if attack_area.owner == selected_area.owner:
            self.HUD = log_action(self, "Cannot attack self")
            print("Cannot attack own area")
            return not has_conquered, attack_area, selected_area, has_conquered
        while has_conquered is False:
            if selected_area.count < 2:
                self.HUD = log_action(self, "Not enough troops")
                print("Not enough troops in selected area, skipping.")
                return not has_conquered, attack_area, selected_area, has_conquered
            match self.name:
                case "conquest_classic":
                    lose_win = randint(0, 15)
                    if lose_win < 5:
                        self.HUD = log_action(self, "Defender Lost")
                        print("Attacked area lost 1 troop")
                        attack_area.count -= 1
                    else:
                        self.HUD = log_action(self, "Attacker Lost")
                        print("Selected area lost 1 troop")
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
                    print("Multiplayer unsupported!")
            if attack_area.count < 1 and selected_area.count > 1:
                if selected_area.owner == "player1":
                    has_conquered = True
                    self.HUD = log_action(self, "Player1 conquered another area")
                    print("Player1 has defeated the opposing territory")
                    attack_area.owner = "player1"
                    attack_area.count = 0  # reset the count
                    attack_area.count = -1 + selected_area.count  # move all except one troop into invaded territory
                    selected_area.count -= selected_area.count - 1  # leave one troop
                elif selected_area.owner == "bot1":
                    has_conquered = True
                    self.HUD = log_action(self, "Bot1 conquered another area")
                    print("Bot1 has defeated the opposing territory")
                    attack_area.owner = "bot1"
                    attack_area.count = 0  # reset the count
                    attack_area.count = -1 + selected_area.count  # move all except one troop into invaded territory
                    selected_area.count -= selected_area.count - 1  # leave one troop
                elif attack_area.owner == "":
                    has_conquered = True
                    self.HUD = log_action(self, selected_area.owner[:1].upper() + selected_area.owner[1:] + " claimed a new area")
                    print(selected_area.owner[:1].upper() + selected_area.owner[1:] + " has claimed a territory")
                    attack_area.owner = selected_area.owner
                    attack_area.count = 0  # reset the count
                    attack_area.count = -1 + selected_area.count  # move all except one troop into invaded territory
                    selected_area.count -= selected_area.count - 1  # leave one troop
        return not has_conquered, attack_area, selected_area, has_conquered


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


def display_screen(game):
    screen.fill(black)
    screen.blit(game.background_image, game.background_rect)
    for area in range(len(game.continent.areas)):
        font = pygame.font.Font(None, 48)
        count_image = font.render(str(game.continent.areas[area].count), False, game.players[game.continent.areas[area].owner].color)
        count_rect = count_image.get_rect()
        count_rect.center = (game.continent.areas[area].rect.center[0] - game.continent.areas[area].count_pos_offset[0],
                             game.continent.areas[area].rect.center[1] - game.continent.areas[area].count_pos_offset[1])
        screen.blit(game.continent.areas[area].image, game.continent.areas[area].rect)
        screen.blit(count_image, count_rect)
        screen.blit(game.HUD.hudbar_image, game.HUD.hudbar_top_rect)
        screen.blit(game.HUD.hudbar_image, game.HUD.hudbar_bottom_rect)
        screen.blit(game.HUD.end_turn_image, game.HUD.end_turn_rect)
        screen.blit(game.HUD.select_image, game.HUD.select_rect)
        screen.blit(game.HUD.turn_play_image, game.HUD.turn_play_rect)
        screen.blit(game.HUD.game_name_image, game.HUD.game_name_rect)
        screen.blit(game.HUD.info_image, game.HUD.info_rect)
        screen.blit(game.HUD.play_name_image, game.HUD.play_name_rect)
    pygame.display.flip()

def log_action(game, msg):
    font = pygame.font.Font(None, 32)
    game.HUD.info_image = font.render(str(msg), False, black)
    game.HUD.info_rect = game.HUD.info_image.get_rect()
    game.HUD.info_rect.center = (DisplayParams.center[0] + (DisplayParams.center[0] - DisplayParams.size[0] / 8), 24)
    return game.HUD

def play_game_classic():
    play_track("music/play.wav", 0.5)
    game = Game("conquest_classic")
    game.players = {"player1": Player("player1", "singleplayer"), "bot1": Player("bot1", "singleplayer"), "": Player("gaia1", "singleplayer")}
    game.players["player1"].color = blue
    game.players["bot1"].color = red
    game.players[""].color = white
    for area in range(len(game.continent.areas)):
        game.continent.areas[area].owner = ""
        game.continent.areas[area].count = 0
    random_area = randint(0, len(game.continent.areas) - 1)
    game.continent.areas[random_area].owner = "player1"
    game.continent.areas[random_area].count = 5
    print("Player1 home area is: " + game.continent.areas[random_area].name)
    player_home = random_area
    bot_home = random_area - 1
    game.continent.areas[random_area - 1].owner = "bot1"
    game.continent.areas[random_area - 1].count = 5
    game.bot_selected_area = game.continent.areas[random_area - 1]
    turns = 0
    has_quit = False
    has_won = False
    has_lost = False
    while (game.maxturns > turns) and (has_quit is False) and not (has_won is True) and not (has_lost is True):
        turn = True
        font = pygame.font.Font(None, 48)
        player_areas = 0
        bot_areas = 0
        display_screen(game)
        turns += 1
        while turn is True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    turn = False
                    has_quit = True
                    break
                elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
                    pos = pygame.mouse.get_pos()
                    for area in range(len(game.continent.areas)):
                        if game.continent.areas[area].rect.collidepoint(pos[0], pos[1]):
                            if game.continent.areas[area].owner == "player1":
                                game.selected_area = game.continent.areas[area]
                                game.HUD.select_image = font.render("Selected: " + game.continent.areas[area].display_name, False, black)
                                game.HUD.select_rect = game.HUD.select_image.get_rect()
                                game.HUD.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - DisplayParams.size[0] / 8), DisplayParams.size[1] - 24)
                                print("Player1 selecting area: " + game.continent.areas[area].name)
                            elif game.continent.areas[area].owner == "bot1" or game.continent.areas[area].owner == "":
                                if game.selected_area is None:
                                    print("No Area selected, cannot attack")
                                    game.HUD = log_action(game, "No selection")
                                else:
                                    print("Player1 attacking area: " + game.continent.areas[area].name + ", From: " + game.selected_area.name)
                                    turn, game.continent.areas[area], game.selected_area, succeded = game.attack(game.continent.areas[area], game.selected_area)
                    if game.HUD.end_turn_rect.collidepoint(pos[0], pos[1]):
                        turn = False
                        break
            bot_areas = 0
            bot_owned_areas = []
            for area in range(len(game.continent.areas)):
                if game.continent.areas[area].owner == "bot1":
                    bot_areas += 1
                    bot_owned_areas.append(game.continent.areas[area])
            if bot_areas <= 0:
                has_won = True
                display_screen(game)
                game.HUD = log_action(game, "Player1 has won")
                print("Player1 has beat bot1")
                break
            player_areas = 0
            for area in range(len(game.continent.areas)):
                if game.continent.areas[area].owner == "player1":
                    player_areas += 1
            if player_areas <= 0:
                has_lost = True
                display_screen(game)
                game.HUD = log_action(game, "Player1 has lost")
                print("Player1 has lost to bot1")
                break
            display_screen(game)
            turns += 1
        game.selected_area = None
        game.continent.areas = game.players["bot1"].turn(game)
        if game.continent.areas[player_home].owner == "player1":
            game.continent.areas[player_home].count += player_areas  # make it so that you can't get stuck, especially when attacked by the bot1 player.
        else:
            for area in range(len(game.continent.areas)):
                if game.continent.areas[area].owner == "player1":
                    player_home = area
            game.continent.areas[
                player_home].count += player_areas  # do the same, but after having found a new home base
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "bot1":
                bot_home = area
        game.continent.areas[bot_home].count += bot_areas   # this may make it take a while to kill them, but they aren't going for world domination.
    if has_won is True:
        print("Player1 has won!")
        sleep(1)
        win_game(game.players["player1"].display_name)
    elif has_lost is True:
        print("Player1 has lost.")
        sleep(1)
        lose_game()


def play_game_mission():
    play_track("music/play.wav", 0.5)


def play_game_invasion():
    play_track("music/play.wav", 0.5)


def play_game_multiplayer():
    play_track("music/play.wav", 0.5)
    print("Multiplayer is not implemented in this version, please just use singleplayer campaigns.")


def win_game(player):
    global menu_is_going
    play_track("music/win.wav", 0.5)
    font = pygame.font.Font(None, DisplayParams.title_size)
    title_img = font.render("Game Stats", False, darkgrey)
    title_rect = title_img.get_rect()
    title_rect.center = (DisplayParams.center[0], DisplayParams.center[1] - 56)

    font = pygame.font.Font(None, 64)
    stat_img = font.render(player + " wins!", False, darkgrey2)
    stat_rect = stat_img.get_rect()
    stat_rect.center = (DisplayParams.center[0], DisplayParams.center[1] + 72 * 1 - 56)

    font = pygame.font.Font(None, DisplayParams.text_size)
    back_img = font.render("Main Menu", False, darkgrey2)
    back_rect = back_img.get_rect()
    back_rect.center = (DisplayParams.center[0], DisplayParams.center[1] + 72 * 2 - 56)

    win = True

    while win is True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                win = False
                menu_is_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
                mouse_pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(mouse_pos[0], mouse_pos[1]):
                    win = False

        screen.fill(darkgrey)  # background may not fill whole screen, just in case
        screen.blit(background_image, background_rect)
        screen.blit(word_cover_img, word_cover_rect)
        screen.blit(title_img, title_rect)
        screen.blit(stat_img, stat_rect)
        screen.blit(back_img, back_rect)
        pygame.display.flip()
    play_track("music/background.wav", 0.5)
    menu_is_going = True


def lose_game(player):
    global menu_is_going
    play_track("music/win.wav", 0.5)
    font = pygame.font.Font(None, DisplayParams.title_size)
    title_img = font.render("Game Stats", False, darkgrey)
    title_rect = title_img.get_rect()
    title_rect.center = (DisplayParams.center[0], DisplayParams.center[1] - 56)

    font = pygame.font.Font(None, 64)
    stat_img = font.render(player + " lost!", False, darkgrey2)
    stat_rect = stat_img.get_rect()
    stat_rect.center = (DisplayParams.center[0], DisplayParams.center[1] + 72 * 1 - 56)

    font = pygame.font.Font(None, DisplayParams.text_size)
    back_img = font.render("Main Menu", False, darkgrey2)
    back_rect = back_img.get_rect()
    back_rect.center = (DisplayParams.center[0], DisplayParams.center[1] + 72 * 2 - 56)

    lose = True

    while lose is True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lose = False
                menu_is_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                if back_rect.collidepoint(pos[0], pos[1]):
                    lose = False

        screen.fill(darkgrey)  # background may not fill whole screen, just in case
        screen.blit(background_image, background_rect)
        screen.blit(word_cover_img, word_cover_rect)
        screen.blit(title_img, title_rect)
        screen.blit(stat_img, stat_rect)
        screen.blit(back_img, back_rect)
        pygame.display.flip()
    play_track("music/background.wav", 0.5)
    menu_is_going = True


def choose_offset(stage):
    return DisplayParams.center[0], DisplayParams.center[1] + 72 * stage - DisplayParams.size[1] / 4 + 56


def choose_game():
    unused_player_colors = colors[:]
    # setup
    global menu_is_going
    choosing = True
    font = pygame.font.Font(None, DisplayParams.title_size)
    title_img = font.render("Choose Game", False, darkgrey)
    title_rect = title_img.get_rect()
    title_rect.center = (choose_offset(0))

    font = pygame.font.Font(None, DisplayParams.text_size)
    classic_img = font.render("Conquest", False, darkgrey2)
    classic_rect = classic_img.get_rect()
    classic_rect.center = (choose_offset(1))

    mission_img = font.render("Mission", False, darkgrey2)
    mission_rect = mission_img.get_rect()
    mission_rect.center = (choose_offset(2))

    invasion_img = font.render("Invasion", False, darkgrey2)
    invasion_rect = invasion_img.get_rect()
    invasion_rect.center = (choose_offset(3))

    multiplayer_img = font.render("Multiplayer", False, darkgrey2)
    multiplayer_rect = multiplayer_img.get_rect()
    multiplayer_rect.center = (choose_offset(4))

    back_img = font.render("Back", False, darkgrey2)
    back_rect = back_img.get_rect()
    back_rect.center = (choose_offset(5))

    play_track("music/background2.wav", 0.5)
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

        screen.fill(darkgrey)
        screen.blit(background_image, background_rect)
        screen.blit(word_cover_img, word_cover_rect)
        screen.blit(title_img, title_rect)
        screen.blit(classic_img, classic_rect)
        screen.blit(mission_img, mission_rect)
        screen.blit(invasion_img, invasion_rect)
        screen.blit(multiplayer_img, multiplayer_rect)
        screen.blit(back_img, back_rect)
        pygame.display.flip()
    play_track("music/background.wav", 0.5)

font = pygame.font.Font(None, DisplayParams.title_size)
title_img = font.render("Main Menu", False, darkgrey)
title_rect = title_img.get_rect()
title_rect.center = (DisplayParams.center[0], DisplayParams.center[1] - 116)

font = pygame.font.Font(None, DisplayParams.text_size)
play_img = font.render("Play", False, darkgrey2)
play_rect = play_img.get_rect()
play_rect.center = (DisplayParams.center[0], DisplayParams.center[1])

quit_img = font.render("Quit", False, darkgrey2)
quit_rect = quit_img.get_rect()
quit_rect.center = (DisplayParams.center[0], DisplayParams.center[1] + 56)

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

    screen.fill(darkgrey)
    screen.blit(background_image, background_rect)
    screen.blit(word_cover_img, word_cover_rect)
    screen.blit(title_img, title_rect)
    screen.blit(play_img, play_rect)
    screen.blit(quit_img, quit_rect)
    pygame.display.flip()
