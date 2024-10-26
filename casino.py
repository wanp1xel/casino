import pygame
import sys
import slots   
import tiles   
import poker
import match_3  
import roulette 

pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  
pygame.display.set_caption("Casino Games")

font = pygame.font.Font(None, 36)

background = pygame.image.load('img/background.png')  
background = pygame.transform.scale(background, (screen_width, screen_height))   
pygame.mixer.music.stop()
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

class CasinoGame:
    def __init__(self):
        self.running = True

    def game_loop(self):
        global screen, screen_width, screen_height, background  
        offset = 200  

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.VIDEORESIZE:
                    screen_width, screen_height = event.w, event.h
                    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
                    background = pygame.transform.scale(pygame.image.load('img/background.png'), (screen_width, screen_height))

            screen.blit(background, (0, 0))   
            draw_text("Casino Games", font, BLACK, screen, screen_width // 2, 50)

            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            # Poker Game
            if 195 + offset - 75 < mouse[0] < 195 + offset + 75 and 470 - 55 < mouse[1] < 470 + 55:
                if click[0] == 1:
                    pygame.mixer.music.stop()  # Зупинити музику перед запуском гри
                    self.running = False
                    poker_width, poker_height = 1200, 700  # Розмір вікна для покеру
                    pygame.display.set_mode((poker_width, poker_height), pygame.RESIZABLE)
                    poker.poker_game(poker_width, poker_height)
            draw_text("Poker", font, BLACK, screen, 195 + offset, 470)
            
            # Roulette Game
            if 410 + offset - 75 < mouse[0] < 410 + offset + 75 and 470 - 55 < mouse[1] < 470 + 55:
                if click[0] == 1:
                    pygame.mixer.music.stop()  # Зупинити музику перед запуском гри
                    self.running = False
                    roulette_width, roulette_height = 1400, 800  # Розмір вікна для рулетки
                    pygame.display.set_mode((roulette_width, roulette_height), pygame.RESIZABLE)
                    roulette.roulette_game(roulette_width, roulette_height)
            draw_text("Roulette", font, BLACK, screen, 410 + offset, 470)
            
            # Slots Game
            if 310 + offset - 75 < mouse[0] < 310 + offset + 75 and 290 - 55 < mouse[1] < 290 + 55:
                if click[0] == 1:
                    pygame.mixer.music.stop()  # Зупинити музику перед запуском гри
                    self.running = False
                    slots_width, slots_height = 500, 600  # Розмір вікна для слотів
                    pygame.display.set_mode((slots_width, slots_height), pygame.RESIZABLE)
                    slots.slots_game(slots_width, slots_height)
            draw_text("Slots", font, WHITE, screen, 310 + offset, 290)

            # Tiles Game (Mines)
            if 600 + offset - 75 < mouse[0] < 600 + offset + 75 and 485 - 55 < mouse[1] < 485 + 55:
                if click[0] == 1:
                    pygame.mixer.music.stop()  # Зупинити музику перед запуском гри
                    self.running = False
                    tiles_width, tiles_height = 600, 600  # Розмір вікна для гри Mines
                    pygame.display.set_mode((tiles_width, tiles_height), pygame.RESIZABLE)
                    tiles.tiles_game(tiles_width, tiles_height)
            draw_text("Mines", font, WHITE, screen, 600 + offset, 485)

            # Match-3 Game
            if 505 + offset - 75 < mouse[0] < 505 + offset + 75 and 290 - 55 < mouse[1] < 290 + 55:
                if click[0] == 1:
                    pygame.mixer.music.stop()  # Зупинити музику перед запуском гри
                    self.running = False
                    match_3_width, match_3_height = 1500, 780  # Розмір вікна для гри Match-3
                    pygame.display.set_mode((match_3_width, match_3_height), pygame.RESIZABLE)
                    match_3.match_3_game(match_3_width, match_3_height)
            draw_text("Match-3", font, WHITE, screen, 505 + offset, 290)
            pygame.display.update()


if __name__ == "__main__":
    game = CasinoGame()
    game.game_loop()
