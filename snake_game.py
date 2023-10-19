import pygame
import random
import os
pygame.mixer.init()
pygame.init()


# Game specific variables...

white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
yellow = (255, 255, 26)
width = 850
height = 500

# pause, running = 1, 0

game_window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game by Arnab")
# background image

bg_img = pygame.image.load("snake_assets/4.jpg")
bg_img = pygame.transform.scale(bg_img, (width, height)).convert_alpha()
pygame.display.update()

font = pygame.font.SysFont(None, 55, True)
clock = pygame.time.Clock()


def screen_score_printing(text, color, x, y):
    screen_text = font.render(text, True, color)
    game_window.blit(screen_text, [x, y])


def plot_snake(pygame_window, color, pysnk_list, pysnake_size):
    for x, y in pysnk_list:
        pygame.draw.rect(pygame_window, color, [x, y, pysnake_size, pysnake_size])


def plot_food(pygame_window, color, pyfood_x, pyfood_y, pysnake_size):
    pygame.draw.rect(pygame_window, color, [pyfood_x, pyfood_y, pysnake_size, pysnake_size])


# def exit_confirmation():
#     game_window.fill(black)
#     screen_score_printing('Really want to Exit ?', yellow, 100, 100)
#     screen_score_printing('Press -[ y/n ]', yellow, 100, 150)
#     for event in pygame.event.get():
#         if event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_y:
#                 run = False
#             if event.key == pygame.K_n:
#                 state = running


def welcome():
    pygame.mixer.music.load("snake_assets/welcome.wav")
    pygame.mixer.music.play()
    exit_game = False
    while not exit_game:
        game_window.fill(black)
        wlc_img = pygame.image.load("snake_assets/2.png")
        wlc_img = pygame.transform.scale(wlc_img, (width, height)).convert_alpha()
        game_window.blit(wlc_img, (0, 0))
        # screen_score_printing("Welcome To Snake Game", white, 150, 200)
        # screen_score_printing("Press Spacebar To Play", white, 170, 290)
        # screen_score_printing("Press Esc To Quit", white, 240, 370)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop()
                if event.key == pygame.K_ESCAPE:
                    exit_game = True

        pygame.display.update()
        clock.tick(60)


# pause = False
# for e in pygame.event.get():
#     if e.type == pygame.KEYDOWN:
#         if e.key == pygame.K_p:
#             pause = True


def game_loop():
    pygame.mixer.music.load("snake_assets/back.mp3")
    pygame.mixer.music.play(loops=10)
    snake_x = 44
    snake_y = 55
    snake_size = 10
    fps = 60
    velocity_x = 0
    velocity_y = 0
    init_velocity = 4
    score = 0
    snk_length = 1
    snk_list = []
    # Initializing random food...
    food_x = random.randint(200, width)
    food_y = random.randint(70, height)
    # Game Loop...
    run = True
    game_over = False

    # if there is no file with 'Hiscore.txt' the below code will force to create one first --
    if not os.path.exists("Hiscore.txt"):
        with open("Hiscore.txt", "w") as f:
            f.write("0")

    # Extracting hiscore variable from file / if Hiscore.txt exists --
    with open("Hiscore.txt", "r") as f1:
        hiscore = f1.read()

    while run:
        if game_over:
            with open("Hiscore.txt", "w") as f1:
                f1.write(str(hiscore))
            game_window.fill(black)
            game_over_img = pygame.image.load("snake_assets/1.png")
            game_over_img = pygame.transform.scale(game_over_img, (width, height)).convert_alpha()
            game_window.blit(game_over_img, (0, 0))
            screen_score_printing(f"Your Score :{score}  Hiscore :{hiscore}", yellow, 150, 450)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # state = pause
                    # Trying --
                    # running = True
                    # while running:
                    #     game_window.fill(black)
                    #     game_window.blit(game_window, (width, height))
                    #     screen_score_printing('Really want to Exit ?', yellow, 100, 100)
                    #     screen_score_printing('Press -[ y/n ]', yellow, 100, 150)
                    #     for event in pygame.event.get():
                    #         if event.type == pygame.KEYDOWN:
                    #             if event.key == pygame.K_y:
                    #                 running = False
                    #                 run = False
                    #             if event.key == pygame.K_n:
                    #                 game_loop()
                    #     pygame.display.update()
                    #     clock.tick(fps)
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        run = False
                    if event.key == pygame.K_RETURN:
                        welcome()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # exit_confirmation()
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        velocity_x = init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        velocity_x = -init_velocity
                        velocity_y = 0
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        velocity_x = 0
                        velocity_y = -init_velocity
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        velocity_x = 0
                        velocity_y = init_velocity
                    elif event.key == pygame.K_q:
                        score += 10
                        # adding condition, when you should make it equal --
                        if hiscore == score:
                            hiscore = score

                        # elif hiscore != score:
                        #     with open("Hiscore.txt") as f:
                        #         hiscore = f.read()

                    elif event.key == pygame.K_ESCAPE:
                        run = False

            snake_x = snake_x + velocity_x
            snake_y = snake_y + velocity_y

            if abs(snake_x - food_x) < 8 and abs(snake_y - food_y) < 8:
                score += 10
                snk_length += 5
                # pygame.mixer.music.load("snake_assets/eat.mp3")
                # pygame.mixer.music.play()
                food_x = random.randint(70, width - 50)
                food_y = random.randint(70, height - 60)

            # giving the condition, for this your hiscore will update itself on the screen --
            if score > int(hiscore):
                hiscore = score

            head = []                     # Head is the 1st quardant of the moving snake
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            # Setting game over conditions :
            if head in snk_list[0:-2]:
                pygame.mixer.music.load("snake_assets/lost.wav")
                pygame.mixer.music.play()
                game_over = True

            if snake_x < 0 or snake_x > width or snake_y < 0 or snake_y > height:
                pygame.mixer.music.load("snake_assets/lost.wav")
                pygame.mixer.music.play()
                game_over = True

            # Removing the last list, so that the snake isn't able to leave any mark on the screen.
            if len(snk_list) > snk_length:
                del snk_list[0]

            game_window.fill(white)
            game_window.blit(bg_img, (0, 0))
            screen_score_printing("Score : " + str(score) + "  Hiscore :"+str(hiscore), red, 5, 5)
            screen_score_printing("'Esc' to exit", red, 550, 5)
            plot_snake(game_window, white, snk_list, snake_size)
            plot_food(game_window, yellow, food_x, food_y, snake_size)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()


welcome()

