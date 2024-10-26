import pygame
import random
import sys
import os
from collections import Counter

pygame.init()
pygame.mixer.init()  
CARD_WIDTH, CARD_HEIGHT = 80, 135
CARD_SPACING = 25
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)

# Завантажуємо фон столу
table = pygame.image.load('img/card/PokerTable.png')

screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
pygame.display.set_caption("Poker Game 1-on-AI")

font = pygame.font.Font(None, 36)
winner_font = pygame.font.Font(None, 60)

SUITS = ['hearts', 'diamonds', 'clubs', 'spades']
RANKS = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']

player_chips = 1000
ai_chips = 1000
pot = 0
current_bet = 0
community_cards = []
hands = {}
game_phase = 'pre-flop'
winner_text = ""
small_blind = 50
big_blind = 100
bet_phase = "initial"
raise_amount = 100  

card_images = {}
for suit in SUITS:
    for rank in RANKS:
        card_images[f"{rank}_of_{suit}"] = pygame.image.load(f"img/card/{rank}_of_{suit}.png")

card_back_image = pygame.image.load("img/card/back.png")

music_folder = "music/radio" 
music_files = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith(".ogg")]
def play_random_music(volume=0.5):
    if music_files:
        random_music = random.choice(music_files)
        pygame.mixer.music.load(random_music)
        pygame.mixer.music.play()

def create_deck():
    deck = [{'rank': rank, 'suit': suit} for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck

def deal_cards(deck):
    return {'Player': [deck.pop(), deck.pop()], 'AI': [deck.pop(), deck.pop()]}

def draw_card(card, x, y):
    card_key = f"{card['rank']}_of_{card['suit']}"
    scaled_card = pygame.transform.scale(card_images[card_key], (CARD_WIDTH, CARD_HEIGHT))
    screen.blit(scaled_card, (x, y))

def draw_community_cards(cards):
    community_card_y = screen_height // 2 - CARD_HEIGHT // 2 - 60
    for i, card in enumerate(cards):
        x_position = 263 + (CARD_WIDTH + CARD_SPACING + 22) * i +35
        draw_card(card, x_position, community_card_y)

def draw_player_hands(hands):
    player_hand_y = screen_height - CARD_HEIGHT - 175
    for i, card in enumerate(hands['Player']):
        x_position = 471 + (CARD_WIDTH + CARD_SPACING + 55) * i
        draw_card(card, x_position, player_hand_y)

def draw_ai_hands(ai_hand, reveal=False):
    ai_hand_y = 40
    for i, card in enumerate(ai_hand):
        x_position = 472 + (CARD_WIDTH + CARD_SPACING + 55) * i
        if reveal:
            draw_card(card, x_position, ai_hand_y)
        else:
            scaled_back = pygame.transform.scale(card_back_image, (CARD_WIDTH, CARD_HEIGHT))
            screen.blit(scaled_back, (x_position, ai_hand_y))

def create_button(x, y, w, h, text):
    pygame.draw.rect(screen, BLUE, (x, y, w, h))
    text_surf = font.render(text, True, WHITE)
    screen.blit(text_surf, (x + w // 4, y + h // 4))

def get_hand_rank(hand):
    ranks = sorted([RANKS.index(card['rank']) for card in hand], reverse=True)
    suits = [card['suit'] for card in hand]

    rank_counts = Counter(ranks)
    most_common_ranks = rank_counts.most_common()
    
    is_flush = len(set(suits)) == 1
    is_straight = ranks == list(range(ranks[0], ranks[0] - 5, -1))

    if is_flush and is_straight:
        return (8, ranks)  # Стріт-флеш
    elif most_common_ranks[0][1] == 4:
        return (7, ranks)  # Каре
    elif most_common_ranks[0][1] == 3 and most_common_ranks[1][1] == 2:
        return (6, ranks)  # Фул хаус
    elif is_flush:
        return (5, ranks)  # Флеш
    elif is_straight:
        return (4, ranks)  # Стріт
    elif most_common_ranks[0][1] == 3:
        return (3, ranks)  # Сет
    elif most_common_ranks[0][1] == 2 and most_common_ranks[1][1] == 2:
        return (2, ranks)  # Дві пари
    elif most_common_ranks[0][1] == 2:
        return (1, ranks)  # Пара
    else:
        return (0, ranks)  # Старша карта

def determine_winner(player_hand, ai_hand, community_cards):
    player_full_hand = player_hand + community_cards
    ai_full_hand = ai_hand + community_cards
    
    player_rank = get_hand_rank(player_full_hand)
    ai_rank = get_hand_rank(ai_full_hand)
    
    if player_rank > ai_rank:
        return "Player Wins!"
    elif ai_rank > player_rank:
        return "AI Wins!"
    else:
        return "It's a Draw!"

def poker_game(screen_width, screen_height):
    global player_chips, ai_chips, pot, current_bet, community_cards, hands, game_phase, screen, winner_text, bet_phase, raise_amount, table

    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Poker Game 1-on-AI")

    deck = create_deck()
    hands = deal_cards(deck)
    community_cards = [deck.pop() for _ in range(5)]
    showdown = False

    running = True
    num_community_cards = 0
    call_phase = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.size
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()

                # Bet
                if 210 <= mouse_x <= 360 and screen_height - 100 <= mouse_y <= screen_height - 50:
                    if player_chips >= big_blind and bet_phase == "initial":
                        current_bet = big_blind
                        player_chips -= current_bet
                        pot += current_bet
                        bet_phase = "flop"
                        num_community_cards = 3
                        call_phase = False

                # Call
                elif 410 <= mouse_x <= 560 and screen_height - 100 <= mouse_y <= screen_height - 50:
                    if player_chips >= current_bet:
                        player_chips -= current_bet
                        pot += current_bet
                        call_phase = True

                # Raise
                elif 610 <= mouse_x <= 760 and screen_height - 100 <= mouse_y <= screen_height - 50:
                    if player_chips >= current_bet + raise_amount:
                        pot += raise_amount
                        call_phase = False
                        if num_community_cards < 5:
                            num_community_cards += 1
                        if num_community_cards == 5:
                            showdown = True

                # Fold
                elif 810 <= mouse_x <= 960 and screen_height - 100 <= mouse_y <= screen_height - 50:
                    ai_chips += pot
                    pot = 0
                    deck = create_deck()
                    hands = deal_cards(deck)
                    community_cards = [deck.pop() for _ in range(5)]
                    current_bet = 0
                    num_community_cards = 0
                    showdown = False
                    bet_phase = "initial"
                    call_phase = False

        # Використовуємо фон столу замість зеленого кольору
        screen.blit(pygame.transform.scale(table, (screen_width, screen_height)), (0, 0))
        
        draw_player_hands(hands)
        draw_community_cards(community_cards[:num_community_cards])

        if showdown:
            draw_ai_hands(hands['AI'], reveal=True)
            winner_text = determine_winner(hands['Player'], hands['AI'], community_cards)
            print(winner_text)

            if winner_text == "Player Wins!":
                player_chips += pot
                ai_chips -= pot
            elif winner_text == "AI Wins!":
                ai_chips += pot
                player_chips -= pot
            else:
                player_chips += pot // 2
                ai_chips += pot // 2

            pot = 0

            text_surf = winner_font.render(winner_text, True, WHITE)
            screen.blit(text_surf, (screen_width // 2 - 120, screen_height // 2 - 180))

            pygame.display.update()
            pygame.time.wait(3000)

            deck = create_deck()
            hands = deal_cards(deck)
            community_cards = [deck.pop() for _ in range(5)]
            num_community_cards = 0
            showdown = False
        else:
            draw_ai_hands(hands['AI'])

        create_button(210, screen_height - 100, 150, 50, "Bet")
        create_button(410, screen_height - 100, 150, 50, "Call")
        create_button(610, screen_height - 100, 150, 50, "Raise")
        create_button(810, screen_height - 100, 150, 50, "Fold")

        text_surf = font.render(f"Player Chips: {player_chips}   Pot: {pot}   AI Chips: {ai_chips}", True, WHITE)
        screen.blit(text_surf, (screen_width // 2 - 300, 50))

        pygame.display.update()

        if not pygame.mixer.music.get_busy():
            play_random_music()


if __name__ == "__main__":
    play_random_music()
    poker_game(1200, 700)  # Передаємо розмір вікна
