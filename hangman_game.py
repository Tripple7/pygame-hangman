import pygame
import sys
import random

WORDS = [
    "Corn","unstable","Loner","Reporter","Anxiety","flackojoestar","ragebait"
]

def draw_gallows(screen):
    pygame.draw.line(screen, (139, 69, 19), (50, 350), (200, 350), 6) # base
    pygame.draw.line(screen, (139, 69, 19), (125, 350), (125, 50), 6) # pole
    pygame.draw.line(screen, (139, 69, 19), (125, 50), (275, 50), 6) # top
    pygame.draw.line(screen, (139, 69, 19), (275, 50), (275, 100), 4) # rope

def draw_head(screen):
    pygame.draw.circle(screen, (0,0,0), (275, 130), 30, 3)

def draw_body(screen):
    pygame.draw.line(screen, (0,0,0), (275, 160), (275, 250), 3)

def draw_left_arm(screen):
    pygame.draw.line(screen, (0,0,0), (275, 180), (235, 220), 3)

def draw_right_arm(screen):
    pygame.draw.line(screen, (0,0,0), (275, 180), (315, 220), 3)

def draw_left_leg(screen):
    pygame.draw.line(screen, (0,0,0), (275, 250), (235, 300), 3)

def draw_right_leg(screen):
    pygame.draw.line(screen, (0,0,0), (275, 250), (315, 300), 3)

HANGMAN_DRAW_FUNCS = [
    draw_gallows,
    draw_head,
    draw_body,
    draw_left_arm,
    draw_right_arm,
    draw_left_leg,
    draw_right_leg
]

WIDTH, HEIGHT = 800, 400
BG_COLOR = (245, 245, 245)
WORD_COLOR = (0, 0, 0)
GUESSED_COLOR = (30, 144, 255)
INFO_COLOR = (220, 20, 60)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hangman Game (Pygame)")
font_word = pygame.font.SysFont('arial', 40, bold=True)
font_info = pygame.font.SysFont('arial', 24)
font_small = pygame.font.SysFont('arial', 18)
clock = pygame.time.Clock()

def draw_game_state(secret_word, guessed_letters, incorrect_guesses, message):
    screen.fill(BG_COLOR)
    for i in range(incorrect_guesses+1):
        if i < len(HANGMAN_DRAW_FUNCS):
            HANGMAN_DRAW_FUNCS[i](screen)
    if message:
        msg_surface = font_info.render(message, True, (0, 0, 128))
        msg_x = WIDTH - msg_surface.get_width() - 40
        msg_y = 180
        screen.blit(msg_surface, (msg_x, msg_y))
    display_word = ' '.join([letter if letter in guessed_letters else '_' for letter in secret_word])
    word_surface = font_word.render(display_word, True, WORD_COLOR)
    screen.blit(word_surface, (WIDTH//2 - word_surface.get_width()//2, 320))
    guessed_text = f"Guessed: {', '.join(sorted(guessed_letters))}"
    guessed_surface = font_info.render(guessed_text, True, GUESSED_COLOR)
    screen.blit(guessed_surface, (20, 370))
    attempts_left = len(HANGMAN_DRAW_FUNCS) - 1 - incorrect_guesses
    attempts_surface = font_info.render(f"Attempts left: {attempts_left}", True, INFO_COLOR)
    screen.blit(attempts_surface, (400, 20))
    pygame.display.flip()

def main():
    running = True
    secret_word = random.choice(WORDS).upper()
    guessed_letters = set()
    incorrect_guesses = 0
    max_incorrect = len(HANGMAN_DRAW_FUNCS) - 1
    message = "Type a letter to guess."
    game_over = False

    while running:
        draw_game_state(secret_word, guessed_letters, incorrect_guesses, message)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif pygame.K_a <= event.key <= pygame.K_z:
                    guess = chr(event.key).upper()
                    if guess in guessed_letters:
                        message = f"You already guessed '{guess}'."
                    else:
                        guessed_letters.add(guess)
                        if guess in secret_word:
                            message = f"Good guess! '{guess}' is in the word."
                            if all(letter in guessed_letters for letter in secret_word):
                                message = f"Congratulations! You guessed the word: {secret_word}"
                                game_over = True
                        else:
                            incorrect_guesses += 1
                            if incorrect_guesses >= max_incorrect:
                                message = f"Game Over! The word was: {secret_word}"
                                game_over = True
                            else:
                                message = f"Sorry, '{guess}' is not in the word."
            elif event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    secret_word = random.choice(WORDS).upper()
                    guessed_letters = set()
                    incorrect_guesses = 0
                    message = "Type a letter to guess."
                    game_over = False
        if game_over:
            restart_surface = font_small.render("Press Enter to play again or close the window to exit.", True, (0,0,0))
            screen.blit(restart_surface, (WIDTH//2 - restart_surface.get_width()//2, 60))
            pygame.display.flip()
        clock.tick(30)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
