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

class Easy:
    bot_attack_threshold = 5
    gain_basis = 4
    class conquest:
        start_count_player = 10
        start_count_bot = 10
        start_count_gaia = 1
    class mission:
        start_count_player = 30
        start_count_bot = 20
        start_count_gaia = 10
    class invasion:
        start_count_player = 20
        start_count_bot = 10
        start_count_gaia = 5
        invasion_turns = 30

class Normal:
    bot_attack_threshold = 4
    gain_basis = 5
    class conquest:
        start_count_player = 20
        start_count_bot = 20
        start_count_gaia = 5
    class mission:
        start_count_player = 25
        start_count_bot = 25
        start_count_gaia = 13
    class invasion:
        start_count_player = 30
        start_count_bot = 30
        start_count_gaia = 7
        invasion_turns = 50

class Hard:
    bot_attack_threshold = 3
    gain_basis = 6
    class conquest:
        start_count_player = 25
        start_count_bot = 30
        start_count_gaia = 8
    class mission:
        start_count_player = 20
        start_count_bot = 30
        start_count_gaia = 15
    class invasion:
        start_count_player = 30
        start_count_bot = 30
        start_count_gaia = 10
        invasion_turns = 75

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

volume = 0.5

hardness = Easy

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

play_track("music/background.wav", volume)

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
    def __init__(self, name="player1", player_type="bot", game_type="singleplayer"):
        self.name = name
        self.display_name = name[:1].upper() + name[1:]  # Change name to uppercase first letter
        self.color = get_player_color(game_type, name)
        self.player_type = player_type
    
    def turn(self, game):
        if self.player_type == "bot":
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
            for area in range(len(game.continent.areas)): # find an attackable area
                if game.continent.areas[area].owner != self.name:
                    bot_attackbles.append(game.continent.areas[area])
                    bot_attack = game.continent.areas[area]
                    break
            bot_attack_index = 0
            for area in range(len(game.continent.areas)):
                if game.continent.areas[area].owner != self.name:
                    if game.continent.areas[area].count < bot_attack.count:
                        bot_attack = game.continent.areas[area]
                        bot_attack_index = area
            while bot_turn is True and game.bot_selected_area.count > bot_attack.count * game.difficulty.bot_attack_threshold:
                print(self.display_name + " Attacking: " + game.continent.areas[bot_attack_index].name + ", From: " + game.bot_selected_area.name)
                bot_turn, game.continent.areas[bot_attack_index], game.bot_selected_area, has_succeded = game.attack(game.continent.areas[bot_attack_index], game.bot_selected_area)
                bot_selectable_areas.remove(game.bot_selected_area)
                if bot_selectable_areas:
                    game.bot_selected_area = bot_selectable_areas[0]
                else:
                    bot_turn = False
            return game.continent.areas, game.HUD, game.selected_area
        elif self.player_type == "player":
            turn = True
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
                                    if game.selected_area:
                                        game.selected_area.image = pygame.image.load("images/selection_area.png")
                                        game.selected_area = None
                                    game.selected_area = game.continent.areas[area]
                                    game.selected_area.image = pygame.image.load("images/selection_area_selected.png")
                                    font = pygame.font.Font(None, 48)
                                    game.HUD.select_image = font.render("Selected: " + game.continent.areas[area].display_name, False, black)
                                    game.HUD.select_rect = game.HUD.select_image.get_rect()
                                    game.HUD.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - DisplayParams.size[0] / 8), DisplayParams.size[1] - 24)
                                elif game.continent.areas[area].owner == "bot1" or game.continent.areas[area].owner == "":
                                    if game.selected_area is None:
                                        game.HUD = log_action(game, "No selection")
                                    else:
                                        print("Player1 attacking area: " + game.continent.areas[area].name + ", From: " + game.selected_area.name)
                                        print("Fighting areas owners: " + game.players[game.continent.areas[area].owner].name + " Defending Against " + game.players[game.selected_area.owner].name)
                                        turn, game.continent.areas[area], game.selected_area, succeded = game.attack(game.continent.areas[area], game.selected_area)
                        if game.HUD.end_turn_rect.collidepoint(pos[0], pos[1]):
                            turn = False
                display_screen(game)
            if game.selected_area:
                game.selected_area.image = pygame.image.load("images/selection_area.png")
                game.selected_area = None
            display_screen(game)
            return game.continent.areas, game.HUD, game.selected_area
        else:
            return game.continent.areas, game.HUD, game.selected_area  # just return, cannot pass because requires returned values

class Area:
    def __init__(self, name="", area_pos=(0, 0), offset=(0, 0)):
        self.name = name
        self.display_name = name[:1].upper() + name[1:]  # Change name to uppercase first letter
        self.image = pygame.image.load("images/selection_area.png")
        self.rect = self.image.get_rect()
        self.rect.center = area_pos
        self.owner = ""
        self.count = 0
        self.count_pos_offset = offset


"""
This is Where you want to go if you want to mod maps

This is where all the map initialization happpens
"""


# size = width, height = 960, 720

class Europe:
    areas = []
    name = "Europe"
    color = blue


Europe.areas.append(Area("england", (DisplayParams.center[0] - DisplayParams.center[0] / 2.25, DisplayParams.center[1] - DisplayParams.center[0] / 5.5), (0, 0)))
Europe.areas.append(Area("franconia", (DisplayParams.center[0] - DisplayParams.center[0] / 2.83, DisplayParams.center[1] + DisplayParams.center[0] / 9.9), (0, 0)))
Europe.areas.append(Area("sweden", (DisplayParams.center[0] - DisplayParams.center[0] / 8.6, DisplayParams.center[1] - DisplayParams.center[0] / 2.3), (0, 0)))
Europe.areas.append(Area("spain", (DisplayParams.center[0] - DisplayParams.center[0] / 2.05, DisplayParams.center[1] + DisplayParams.center[0] / 2.65), (0, 0)))
Europe.areas.append(Area("moscovy", (DisplayParams.center[0] + DisplayParams.center[0] / 3.15, DisplayParams.center[1] - DisplayParams.center[0] / 2.6), (0, 0)))
Europe.areas.append(Area("germana", (DisplayParams.center[0] - DisplayParams.center[0] / 7.5, DisplayParams.center[1] + DisplayParams.center[0] / 8.5), (0, 0)))
Europe.areas.append(Area("ottoman", (DisplayParams.center[0] + DisplayParams.center[0] / 7.2, DisplayParams.center[1] + DisplayParams.center[0] / 4.2), (0, 0)))

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

def display_screen(game):
    screen.fill(black)
    screen.blit(game.background_image, game.background_rect)
    screen.blit(game.continent_image, game.continent_rect)
    for area in range(len(game.continent.areas)):
        font = pygame.font.Font(None, 64)
        count_image = font.render(str(game.continent.areas[area].count), False, game.players[game.continent.areas[area].owner].color)
        count_rect = count_image.get_rect()
        count_rect.center = (game.continent.areas[area].rect.center[0] - game.continent.areas[area].count_pos_offset[0], game.continent.areas[area].rect.center[1] - game.continent.areas[area].count_pos_offset[1])
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

class Game:
    def __init__(self, name="", maxturns=1000):
        self.continent = continents[randint(0, len(continents)) - 1]
        self.players = players
        self.name = name
        self.maxturns = maxturns
        self.background_image = pygame.image.load("images/ocean.png")
        self.background_rect = self.background_image.get_rect()
        self.background_rect.center = DisplayParams.center
        self.continent_image = pygame.image.load("images/europe_map.png")
        self.continent_rect = self.continent_image.get_rect()
        self.continent_rect.center = DisplayParams.center
        self.selected_area = None
        self.HUD = HUD()
        self.mission_index = randint(0, len(self.continent.areas) - 1)
        self.difficulty = hardness()

    def attack(self, attack_area, selected_area):
        has_conquered = False
        if attack_area.owner == selected_area.owner:
            self.HUD = log_action(self, "Cannot attack self")
            return not has_conquered, attack_area, selected_area, has_conquered
        while has_conquered is False:
            if selected_area.count < 2:
                self.HUD = log_action(self, "Not enough troops, skipping")
                return not has_conquered, attack_area, selected_area, has_conquered
            sleep(0.05)
            attack_area.image = pygame.image.load("images/selection_area_attack.png")
            display_screen(self)
            lose_win = randint(0, 15)
            if lose_win < self.difficulty.gain_basis:
                self.HUD = log_action(self, "Defender Lost")
                attack_area.count -= 1
            else:
                self.HUD = log_action(self, "Attacker Lost")
                selected_area.count -= 1
            if attack_area.count < 1 and selected_area.count > 1:
                if selected_area.owner == "player1":
                    has_conquered = True
                    self.HUD = log_action(self, "Player1 conquered an area")
                    attack_area.owner = "player1"
                    attack_area.count = 0  # reset the count
                    attack_area.count = -1 + selected_area.count  # move all except one troop into invaded territory
                    selected_area.count -= selected_area.count - 1  # leave one troop
                elif selected_area.owner == "bot1":
                    has_conquered = True
                    self.HUD = log_action(self, "Bot1 conquered an area")
                    attack_area.owner = "bot1"
                    attack_area.count = 0  # reset the count
                    attack_area.count = -1 + selected_area.count  # move all except one troop into invaded territory
                    selected_area.count -= selected_area.count - 1  # leave one troop
                elif attack_area.owner == "":
                    has_conquered = True
                    self.HUD = log_action(self, selected_area.owner[:1].upper() + selected_area.owner[1:] + " claimed an area")
                    attack_area.owner = selected_area.owner
                    attack_area.count = 0  # reset the count
                    attack_area.count = -1 + selected_area.count  # move all except one troop into invaded territory
                    selected_area.count -= selected_area.count - 1  # leave one troop
        attack_area.image = pygame.image.load("images/selection_area.png")
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


def log_action(game, msg):
    font = pygame.font.Font(None, 32)
    game.HUD.info_image = font.render(str(msg), False, black)
    game.HUD.info_rect = game.HUD.info_image.get_rect()
    game.HUD.info_rect.center = (DisplayParams.center[0] + (DisplayParams.center[0] - DisplayParams.size[0] / 8), 24)
    return game.HUD


def menu_transition_close():
    # Get the current display surface
    screen_surface = pygame.display.get_surface().copy()
    opacity = 0
    while opacity < 255:
        # Create a new overlay to hold the overlay
        overlay = pygame.Surface(screen_surface.get_size(), pygame.SRCALPHA)
        # Copy the contents of the screen to the overlay
        overlay.blit(screen_surface, (0, 0))

        overlay.fill((200, 200, 200, opacity), None, pygame.BLEND_RGBA_MULT)

        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        opacity += 50
        opacity = min(opacity, 255)
        del overlay

    del screen_surface
    """overlay = pygame.image.load("images/menu_transition_scale.png")
    rect = overlay.get_rect()
    rect.center = (DisplayParams.center[0], DisplayParams.center[1])
    scale = 1  # ends at 6
    size = overlay.get_size()
    size = (size[0] * scale, size[1] * scale)
    overlay = pygame.transform.scale(overlay, size)
    screen.blit(overlay, rect)
    pygame.display.flip()
    step = 1
    while step <= 6:
        sleep(0.125)
        size = overlay.get_size()
        size = (size[0] * step, size[1] * step)
        overlay = pygame.transform.scale(overlay, size)
        rect = overlay.get_rect()
        rect.center = (DisplayParams.center[0], DisplayParams.center[1])
        screen.blit(overlay, rect)
        pygame.display.flip()
        step += 0.125"""


def menu_transition_open():
    # Get the current display surface
    screen_surface = pygame.display.get_surface().copy()
    opacity = 255
    while opacity > 0:
        # Create a new overlay to hold the overlay
        overlay = pygame.Surface(screen_surface.get_size(), pygame.SRCALPHA)
        # Copy the contents of the screen to the overlay
        overlay.blit(screen_surface, (0, 0))

        overlay.fill((200, 200, 200, opacity), None, pygame.BLEND_RGBA_MULT)

        screen.blit(overlay, (0, 0))
        pygame.display.flip()
        pygame.time.wait(10)
        opacity -= 50
        del overlay

    del screen_surface
    """overlay = pygame.image.load("images/menu_transition_scale.png")
    rect = overlay.get_rect()
    rect.center = (DisplayParams.center[0], DisplayParams.center[1])
    scale = 6  # ends at 1
    size = overlay.get_size()
    size = (size[0] * scale, size[1] * scale)
    scaled_overlay = pygame.transform.scale(overlay, size)
    screen.blit(scaled_overlay, rect)
    del scaled_overlay
    pygame.display.flip()
    step = 6
    while step > 1:  # should run through 48 times
        print("Step:" + str(step) + " size:" + str(size) + " rect.center:" + str(rect.center ))
        sleep(0.025)
        size = overlay.get_size()
        size = (size[0] * step, size[1] * step)
        scaled_overlay = pygame.transform.scale(overlay, size)
        screen.blit(scaled_overlay, rect)
        pygame.display.flip()
        del scaled_overlay
        step -= 0.125"""

def player_homes(game):
    for area in range(len(game.continent.areas)):
        game.continent.areas[area].owner = ""
    random_area = randint(0, len(game.continent.areas) - 1)
    game.continent.areas[random_area].owner = "player1"
    player_home = random_area
    bot_home = random_area - 1
    game.continent.areas[random_area - 1].owner = "bot1"
    game.bot_selected_area = game.continent.areas[random_area - 1]
    if game.name == "conquest_classic":
        game.continent.areas[random_area].count = game.difficulty.conquest.start_count_player # TODO - NEEDS FIXING: Make game.difficulty use list game class
        game.continent.areas[random_area - 1].count = game.difficulty.conquest.start_count_bot
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "":
                game.continent.areas[area].count = game.difficulty.conquest.start_count_gaia
    elif game.name == "conquest_mission":
        game.continent.areas[random_area].count = game.difficulty.mission.start_count_player
        game.continent.areas[random_area - 1].count = game.difficulty.mission.start_count_bot
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "":
                game.continent.areas[area].count = game.difficulty.mission.start_count_gaia
    elif game.name == "conquest_invasion":
        game.continent.areas[random_area].count = game.difficulty.invasion.start_count_player
        game.continent.areas[random_area - 1].count = game.difficulty.invasion.start_count_bot
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "":
                game.continent.areas[area].count = game.difficulty.invasion.start_count_gaia
    elif game.name == "conquest_multiplayer":
        game.continent.areas[random_area].count = game.difficulty.conquest.start_count_player
        game.continent.areas[random_area - 1].count = game.difficulty.conquest.start_count_bot
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "":
                game.continent.areas[area].count = game.difficulty.multiplayer.start_count_gaia
    return player_home, bot_home, game

def play_game_classic():
    menu_transition_open()
    play_track("music/play.wav", volume)
    game = Game("conquest_classic")
    game.players = {"player1": Player("player1", "player"), "bot1": Player("bot1", "bot"), "": Player("gaia1", "unclaimed")}
    game.players["player1"].color = blue
    game.players["bot1"].color = red
    game.players[""].color = white
    player_home, bot_home, game = player_homes(game)
    turns = 0
    has_quit = False
    has_won = False
    has_lost = False
    while (game.maxturns > turns) and (has_quit is False) and not (has_won is True) and not (has_lost is True):
        font = pygame.font.Font(None, 48)
        player_areas = 0
        bot_areas = 0
        display_screen(game)
        bot_areas = 0
        player_areas = 0
        bot_owned_areas = []
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "bot1":
                bot_areas += 1
                bot_owned_areas.append(game.continent.areas[area])
            elif game.continent.areas[area].owner == "player1":
                player_areas += 1
        if bot_areas <= 0:
            has_won = True
            display_screen(game)
            game.HUD = log_action(game, "Bot1 has lost")
            break
        if player_areas <= 0:
            has_lost = True
            display_screen(game)
            game.HUD = log_action(game, "Player1 has lost")
            break
        game.HUD.select_image = font.render("Selected: ", False, black)
        game.HUD.select_rect = game.HUD.select_image.get_rect()
        game.HUD.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - DisplayParams.size[0] / 8), DisplayParams.size[1] - 24)
        for player in game.players:
            game.HUD.select_image = font.render("Selected: ", False, black)
            game.HUD.select_rect = game.HUD.select_image.get_rect()
            game.HUD.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - DisplayParams.size[0] / 8), DisplayParams.size[1] - 24)
            sleep(0.05)
            game.continent.areas, game.HUD, game.selected_area = game.players[player].turn(game)
        turns += 1
        if game.continent.areas[player_home].owner == "player1":
            game.continent.areas[player_home].count += player_areas  # make it so that you can't get stuck, especially when attacked by the bot1 player.
        else:
            for area in range(len(game.continent.areas)):
                if game.continent.areas[area].owner == "player1":
                    player_home = area
            game.continent.areas[player_home].count += player_areas  # do the same, but after having found a new home base
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "bot1":
                bot_home = area
        game.continent.areas[bot_home].count += bot_areas   # this may make it take a while to kill them.
    if has_won is True:
        print("Player1 has won!")
        sleep(1)
        win_game(game.players["player1"].display_name)
    elif has_lost is True:
        print("Player1 has lost.")
        sleep(1)
        lose_game(game.players["player1"].display_name)
    menu_transition_close()


def play_game_mission():
    menu_transition_open()
    play_track("music/play.wav", volume)
    game = Game("conquest_classic")
    game.players = {"player1": Player("player1", "player"), "bot1": Player("bot1", "bot"), "": Player("gaia1", "unclaimed")}
    game.players["player1"].color = blue
    game.players["bot1"].color = red
    game.players[""].color = white
    player_home, bot_home, game = player_homes(game)
    turns = 0
    has_quit = False
    has_won = False
    has_lost = False
    while (game.maxturns >= turns) and (has_quit is False) and not (has_won is True) and not (has_lost is True):
        font = pygame.font.Font(None, 48)
        player_areas = 0
        bot_areas = 0
        display_screen(game)
        bot_areas = 0
        player_areas = 0
        bot_owned_areas = []
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "bot1":
                bot_areas += 1
                bot_owned_areas.append(game.continent.areas[area])
            elif game.continent.areas[area].owner == "player1":
                player_areas += 1
        if game.continent.areas[game.mission_index].owner == "player1":
            has_won = True
            display_screen(game)
            game.HUD = log_action(game, "Bot1 has lost")
            break
        if player_areas <= 0:
            has_lost = True
            display_screen(game)
            game.HUD = log_action(game, "Player1 has lost")
            break
        game.HUD.select_image = font.render("Selected: ", False, black)
        game.HUD.select_rect = game.HUD.select_image.get_rect()
        game.HUD.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - DisplayParams.size[0] / 8), DisplayParams.size[1] - 24)
        game.HUD = log_action(game, "Mission: capture " + game.continent.areas[game.mission_index].name)
        for player in game.players:
            game.HUD.select_image = font.render("Selected: ", False, black)
            game.HUD.select_rect = game.HUD.select_image.get_rect()
            game.HUD.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - DisplayParams.size[0] / 8), DisplayParams.size[1] - 24)
            sleep(0.05)
            game.continent.areas, game.HUD, game.selected_area = game.players[player].turn(game)
        turns += 1
        if game.continent.areas[player_home].owner == "player1":
            game.continent.areas[player_home].count += player_areas  # make it so that you can't get stuck, especially when attacked by the bot1 player.
        else:
            for area in range(len(game.continent.areas)):
                if game.continent.areas[area].owner == "player1":
                    player_home = area
            game.continent.areas[player_home].count += player_areas  # do the same, but after having found a new home base
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "bot1":
                bot_home = area
        game.continent.areas[bot_home].count += bot_areas   # this may make it take a while to kill them.
    if has_won is True:
        print("Player1 has won!")
        sleep(1)
        win_game(game.players["player1"].display_name)
    elif has_lost is True:
        print("Player1 has lost.")
        sleep(1)
        lose_game(game.players["player1"].display_name)
    menu_transition_close()


def play_game_invasion():
    menu_transition_open()
    play_track("music/play.wav", volume)
    game = Game("conquest_classic", 20) # defend for N turns
    game.players = {"player1": Player("player1", "player"), "bot1": Player("bot1", "bot"), "": Player("gaia1", "unclaimed")}
    game.players["player1"].color = blue
    game.players["bot1"].color = red
    game.players[""].color = white
    player_home, bot_home, game = player_homes(game)
    turns = 0
    has_quit = False
    has_won = False
    has_lost = False
    while (game.maxturns > turns) and (has_quit is False) and not (has_won is True) and not (has_lost is True):
        font = pygame.font.Font(None, 48)
        player_areas = 0
        bot_areas = 0
        display_screen(game)
        bot_areas = 0
        player_areas = 0
        bot_owned_areas = []
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "bot1":
                bot_areas += 1
                bot_owned_areas.append(game.continent.areas[area])
            elif game.continent.areas[area].owner == "player1":
                player_areas += 1
        if bot_areas <= 0:
            has_won = True
            display_screen(game)
            game.HUD = log_action(game, "Bot1 has lost")
            break
        if game.continent.areas[player_home].owner != "player1":
            has_lost = True
            display_screen(game)
            game.HUD = log_action(game, "Player1 has lost")
            break
        game.HUD.select_image = font.render("Selected: ", False, black)
        game.HUD.select_rect = game.HUD.select_image.get_rect()
        game.HUD.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - DisplayParams.size[0] / 8), DisplayParams.size[1] - 24)
        for player in game.players:
            game.HUD.select_image = font.render("Selected: ", False, black)
            game.HUD.select_rect = game.HUD.select_image.get_rect()
            game.HUD.select_rect.center = (DisplayParams.center[0] - (DisplayParams.center[0] - DisplayParams.size[0] / 8), DisplayParams.size[1] - 24)
            sleep(0.05)
            game.continent.areas, game.HUD, game.selected_area = game.players[player].turn(game)
        turns += 1
        if game.continent.areas[player_home].owner == "player1":
            game.continent.areas[player_home].count += player_areas  # make it so that you can't get stuck, especially when attacked by the bot1 player.
        for area in range(len(game.continent.areas)):
            if game.continent.areas[area].owner == "bot1":
                bot_home = area
        game.continent.areas[bot_home].count += bot_areas   # this may make it take a while to kill them.
    if has_lost is True:
        print("Player1 has lost.")
        sleep(0.125)
        lose_game(game.players["player1"].display_name)
    else:
        print("Player1 has won!")
        sleep(0.125)
        win_game(game.players["player1"].display_name)
    menu_transition_close()


def play_game_multiplayer():
    play_track("music/play.wav", volume)
    print("Multiplayer is not implemented in this version, please just use singleplayer campaigns.")

def win_game(player):
    menu_transition_open()
    global menu_is_going
    play_track("music/win.wav", volume)
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
    play_track("music/background.wav", volume)
    menu_is_going = True
    menu_transition_close()


def lose_game(player):
    menu_transition_open()
    global menu_is_going
    play_track("music/win.wav", volume)
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
    play_track("music/background.wav", volume)
    menu_is_going = True
    menu_transition_close()


def choose_offset(stage):
    return DisplayParams.center[0], DisplayParams.center[1] + 72 * stage - DisplayParams.size[1] / 4 + 56

def options():
    menu_transition_open()
    global menu_is_going
    global hardness
    options_continue = True
    font = pygame.font.Font(None, DisplayParams.title_size)
    title_img = font.render("Options", False, darkgrey)
    title_rect = title_img.get_rect()
    title_rect.center = (choose_offset(0))

    font = pygame.font.Font(None, DisplayParams.text_size)
    sect_img = font.render("Difficulty:", False, darkgrey2)
    sect_rect = sect_img.get_rect()
    sect_rect.center = (choose_offset(1))
    
    font = pygame.font.Font(None, DisplayParams.text_size)
    opt1_img = font.render("Easy", False, darkgrey2)
    opt1_rect = opt1_img.get_rect()
    opt1_rect.center = (choose_offset(2))
    
    font = pygame.font.Font(None, DisplayParams.text_size)
    opt2_img = font.render("Normal", False, darkgrey2)
    opt2_rect = opt2_img.get_rect()
    opt2_rect.center = (choose_offset(3))
    
    font = pygame.font.Font(None, DisplayParams.text_size)
    opt3_img = font.render("Hard", False, darkgrey2)
    opt3_rect = opt3_img.get_rect()
    opt3_rect.center = (choose_offset(4))

    back_img = font.render("Back", False, darkgrey2)
    back_rect = back_img.get_rect()
    back_rect.center = (choose_offset(5))

    play_track("music/background2.wav", volume)
    while options_continue is True:
        clock.tick(30)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                options_continue = False
                menu_is_going = False
            elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
                pos = pygame.mouse.get_pos()
                if opt1_rect.collidepoint(pos[0], pos[1]):
                    hardness = Easy
                    print("Difficulty: Easy")
                elif opt2_rect.collidepoint(pos[0], pos[1]):
                    hardness = Normal
                    print("Difficulty: Normal")
                elif opt3_rect.collidepoint(pos[0], pos[1]):
                    hardness = Hard
                    print("Difficulty: Hard")
                elif back_rect.collidepoint(pos[0], pos[1]):
                    options_continue = False

        screen.fill(darkgrey)
        screen.blit(background_image, background_rect)
        screen.blit(word_cover_img, word_cover_rect)
        screen.blit(title_img, title_rect)
        screen.blit(sect_img, sect_rect)
        screen.blit(opt1_img, opt1_rect)
        screen.blit(opt2_img, opt2_rect)
        screen.blit(opt3_img, opt3_rect)
        screen.blit(back_img, back_rect)
        pygame.display.flip()
    play_track("music/background.wav", volume)
    menu_transition_close()

def choose_game():
    menu_transition_open()
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

    play_track("music/background2.wav", volume)
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
    play_track("music/background.wav", volume)
    menu_transition_close()

font = pygame.font.Font(None, DisplayParams.title_size)
title_img = font.render("Main Menu", False, darkgrey)
title_rect = title_img.get_rect()
title_rect.center = (DisplayParams.center[0], DisplayParams.center[1] - 116)

font = pygame.font.Font(None, DisplayParams.text_size)
play_img = font.render("Play", False, darkgrey2)
play_rect = play_img.get_rect()
play_rect.center = (DisplayParams.center[0], DisplayParams.center[1])

font = pygame.font.Font(None, DisplayParams.text_size)
opt_img = font.render("Options", False, darkgrey2)
opt_rect = opt_img.get_rect()
opt_rect.center = (DisplayParams.center[0], DisplayParams.center[1] + 56)

quit_img = font.render("Quit", False, darkgrey2)
quit_rect = quit_img.get_rect()
quit_rect.center = (DisplayParams.center[0], DisplayParams.center[1] + 56*2)

mute_image = pygame.image.load("images/mute.png")
unmute_image = mute_image = pygame.image.load("images/unmute.png")
mute_toggle_image = pygame.image.load("images/mute.png")
mute_rect = mute_image.get_rect()
mute_rect.center = (DisplayParams.center[0] + DisplayParams.center[0] / 2.5, DisplayParams.center[1] - DisplayParams.center[0] / 3.5)

while menu_is_going is True:
    clock.tick(30)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            menu_is_going = False

    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed():
        pos = pygame.mouse.get_pos()
        if mute_rect.collidepoint(pos[0], pos[1]):
            if volume <= 0.0:
                mute_toggle_image = mute_image
                volume = 0.5
                play_track("music/background.wav", volume)
            elif volume > 0.0:
                volume = 0.0
                mute_toggle_image = unmute_image
                play_track("music/background.wav", volume)
        elif play_rect.collidepoint(pos[0], pos[1]):
            menu_transition_close()
            choose_game()
        elif opt_rect.collidepoint(pos[0], pos[1]):
            menu_transition_close()
            options()
        elif quit_rect.collidepoint(pos[0], pos[1]):
            menu_is_going = False

    screen.fill(darkgrey)
    screen.blit(background_image, background_rect)
    screen.blit(word_cover_img, word_cover_rect)
    screen.blit(mute_toggle_image, mute_rect)
    screen.blit(title_img, title_rect)
    screen.blit(play_img, play_rect)
    screen.blit(opt_img, opt_rect)
    screen.blit(quit_img, quit_rect)
    pygame.display.flip()

pygame.quit()
