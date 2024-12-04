import pygame
import sys
black = (0, 0, 0)


class Button:
    def __init__(self, x, y, width, height, text, inactive_color, active_color, action=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.action = action

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if self.x + self.width > mouse[0] > self.x and self.y + self.height > mouse[1] > self.y:
            pygame.draw.rect(screen, self.active_color,
                             (self.x, self.y, self.width, self.height))
            if click[0] == 1 and self.action is not None:
                self.action()
        else:
            pygame.draw.rect(screen, self.inactive_color,
                             (self.x, self.y, self.width, self.height))

        font = pygame.font.Font(None, 30)
        # Use the black variable (tuple)
        text_surface = font.render(self.text, True, (black))
        text_rect = text_surface.get_rect(
            center=((self.x + self.width / 2), (self.y + self.height / 2)))
        screen.blit(text_surface, text_rect)


def my_button_action():
    global game_over
    global lub
    global lid
    game_over = False
    global timer
    timer = 5
    global timer_color
    timer_color = (255, 255, 255)  # White
    lub = 180
    lid = 3240


def go_new_day():
    global new_day
    global lub
    global lid
    global days_left
    global win
    global timer
    new_day = False
    # timers
    timer = 5
    lub = 180
    lid = 3240
    days_left -= 1
    if days_left == 0:
        win = True


# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Treadmill Simulator")

# Load images
s1_image = pygame.image.load("s1.png")
s2_image = pygame.image.load("s2.png")
# s1_image = pygame.transform.scale(s1_image, (200, 150))
# s2_image = pygame.transform.scale(s2_image, (200, 150))

# Font
font = pygame.font.Font(None, 74)

# Global variables
timer = 5
timer_color = (255, 255, 255)
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)  # 1-second timer

current_image = s1_image
game_over = False

# Remaining time variables
# timer 180 3240 91
global lub
global lid
global days_left
lub = 180  # Actions until break
lid = 3240  # Actions until day end
days_left = 91
win = False

# Break timer
break_timer = 4  # 5 minutes (300 seconds)
running_main_loop = True  # True if main loop is running, False if break timer is active

# Key requirement
needed = "a"

# Main game loop
running = True
new_day = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == timer_event:
            if running_main_loop and not game_over:
                timer -= 1
                # Update timer color
                if timer == 1:
                    timer_color = (0, 255, 0)  # Green
                elif timer == 0:
                    game_over = True
                else:
                    timer_color = (255, 255, 255)  # White
            elif not running_main_loop:  # During break
                break_timer -= 1
                if break_timer == 0:
                    running_main_loop = True
                    # timer
                    lub = 180  # Reset actions until next break
                    # timer
                    break_timer = 5

        elif event.type == pygame.KEYDOWN and running_main_loop and not game_over:
            if timer == 1:  # Only allow changes when timer is green
                if event.key == pygame.K_a and needed == "a":  # A key
                    current_image = s2_image
                    timer = 5
                    timer_color = (255, 255, 255)
                    needed = "d"
                    lub -= 1
                    lid -= 1
                    if lid == 0:
                        new_day = True
                    elif lub == 0:
                        running_main_loop = False
                elif event.key == pygame.K_d and needed == "d":  # D key
                    current_image = s1_image
                    timer = 5
                    timer_color = (255, 255, 255)
                    needed = "a"
                    lub -= 1
                    lid -= 1
                    if lid == 0:
                        new_day = True
                    elif lub == 0:
                        running_main_loop = False

    # Clear screen
    screen.fill((0, 0, 0))
    if win:
        you_win_text = font.render("You Win!", True, (255, 255, 255))
        screen.fill((0, 0, 0))
        screen.blit(you_win_text, (width // 2 - you_win_text.get_width() //
                    2, height // 2 - you_win_text.get_height() // 2))
    elif new_day:
        congrats_text = font.render("Congratulations", True, (255, 255, 255))
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(congrats_text, (width // 2 - congrats_text.get_width() //
                    2, height // 2 - congrats_text.get_height() // 2))
        next_day_button = Button(
            400, 500, 200, 200, "Next Day", "gray", "red", go_new_day)
        next_day_button.draw(screen)

    elif not running_main_loop:  # Break timer
        break_text = font.render("Break Time", True, (255, 255, 255))
        break_timer_text = font.render(
            f"{break_timer // 60}:{break_timer % 60:02}", True, (255, 255, 255))
        screen.blit(break_text, (width // 2 - break_text.get_width() //
                    2, height // 2 - break_text.get_height() // 2 - 50))
        screen.blit(break_timer_text, (width // 2 - break_timer_text.get_width() //
                    2, height // 2 - break_timer_text.get_height() // 2 + 50))

    elif not game_over:
        # Draw the current image
        screen.blit(current_image, (width // 2 - current_image.get_width() //
                    2, height - current_image.get_height()))

        # Display the timer
        timer_text = font.render(str(timer), True, timer_color)
        screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 50))

        # Display lub
        lub_text = font.render(
            f"Left until break: {lub}", True, (255, 255, 255))
        screen.blit(lub_text, (10, 120))

        # Display lid
        lid_text = font.render(
            f"Left until day end: {lid}", True, (255, 255, 255))
        screen.blit(lid_text, (10, 190))

        # Display days
        days_text = font.render(
            f"Days remaining: {days_left}", True, (255, 255, 255))
        screen.blit(days_text, (10, 260))
        if needed == "a":
            instruct_text = font.render(
                f"Hit \"A\" when the timer turns green", True, (255, 0, 0))
        else:
            instruct_text = font.render(
                f"Hit \"D\" when the timer turns green", True, (255, 0, 0))
        screen.blit(instruct_text, (10, 330))

    else:
        # Game Over screen
        game_over_text = font.render("Day Failed", True, (255, 0, 0))
        screen.fill((0, 0, 0))  # Clear screen
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() //
                    2, height // 2 - game_over_text.get_height() // 2))
        try_again_button = Button(
            400, 500, 200, 200, "Try Again", "gray", "red", my_button_action)
        try_again_button.draw(screen)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()
