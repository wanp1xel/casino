import pygame
import sys
import random
import time

pygame.init()

pygame.mixer.init()

spin_sound = pygame.mixer.Sound('music/slot_1.ogg')  
win_sound = pygame.mixer.Sound('music/jackpot.ogg')  
lose_sound = pygame.mixer.Sound('music/fail.ogg')

WHITE = (255, 255, 255)
RED = (255, 0, 0)

font = pygame.font.Font(None, 36)

symbol_images = {
    'cherry': pygame.image.load('img/slots/cherry.png'),
    'lemon': pygame.image.load('img/slots/lemon.png'),
    'bell': pygame.image.load('img/slots/bell.png'),
    'watermelon': pygame.image.load('img/slots/watermelon.png'),
    'star': pygame.image.load('img/slots/star.png'),
    'diamond': pygame.image.load('img/slots/diamond.png')
}

for key in symbol_images:
    symbol_images[key] = pygame.transform.scale(symbol_images[key], (80, 80))   

symbols = ['cherry', 'lemon', 'bell', 'watermelon', 'star', 'diamond']

slot_positions = [
    (80, 180),  # Перше вікно
    (180, 180),  # Друге вікно
    (285, 180)   # Третє вікно
]

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def draw_button(surface, x, y, w, h, color, text=''):
    if text != '':
        draw_text(text, font, WHITE, surface, x + (w // 2), y + (h // 2))

def spin_animation():
    spin_time = 3  
    end_time = time.time() + spin_time

    spin_sound.play() 

    slot1, slot2, slot3 = None, None, None

    while time.time() < end_time:
        slot1 = random.choice(symbols)
        slot2 = random.choice(symbols)
        slot3 = random.choice(symbols)

        screen.fill(WHITE)
        screen.blit(background, (0, 0))
        screen.blit(symbol_images[slot1], slot_positions[0])
        screen.blit(symbol_images[slot2], slot_positions[1])
        screen.blit(symbol_images[slot3], slot_positions[2])
        pygame.display.update()

        pygame.time.delay(100)  

    spin_sound.stop()  
    return slot1, slot2, slot3  

def update_screen_size(new_width, new_height):
    global screen, background, screen_width, screen_height, slot_positions

    screen_width = new_width
    screen_height = new_height
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  
    background = pygame.image.load('img/slots/game1.png') 
    background = pygame.transform.scale(background, (screen_width, screen_height))  

    # Оновлюємо позиції слотів відповідно до нового розміру екрану
    slot_positions = [
        (screen_width // 5, screen_height // 3),
        (screen_width // 2 - 40, screen_height // 3),
        (screen_width - screen_width // 5 - 80, screen_height // 3)
    ]

def slots_game(screen_width, screen_height):
    global screen, background

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)  # Оновлюємо розмір вікна
    background = pygame.image.load('img/slots/game1.png')
    background = pygame.transform.scale(background, (screen_width, screen_height))

    running = True

    slot1 = random.choice(symbols)
    slot2 = random.choice(symbols)
    slot3 = random.choice(symbols)

    message = "Натисніть кнопку для обертання!"

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False   
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if 420 <= mouse_pos[0] <= 470 and 100 <= mouse_pos[1] <= 150:
                    slot1, slot2, slot3 = spin_animation()

                    if slot1 == slot2 == slot3:
                        message = "Виграш!"
                        win_sound.play() 
                    else:
                        message = "Спробуйте ще раз!"
                        lose_sound.play()  

            if event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                update_screen_size(screen_width, screen_height)

        screen.fill(WHITE) 
        screen.blit(background, (0, 0))

        screen.blit(symbol_images[slot1], slot_positions[0])
        screen.blit(symbol_images[slot2], slot_positions[1])
        screen.blit(symbol_images[slot3], slot_positions[2])

        draw_text(message, font, RED, screen, screen_width // 2, screen_height // 2 + 200)

        draw_button(screen, 420, 100, 50, 50, RED, "")

        pygame.display.update()



if __name__ == "__main__":
    screen_width, screen_height = 800, 600  # Початковий розмір екрану
    update_screen_size(screen_width, screen_height)  # Оновлюємо екран
    slots_game()
