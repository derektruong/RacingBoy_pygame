import pygame
import time
import random
import datetime

pygame.init()

display_width = 800
display_height = 1000

gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Racing boy VN')
clock = pygame.time.Clock()
# color
black = (0, 0, 0)
white = (255, 255, 255)
lower_red = (220, 20, 60)
upper_red = (255, 0, 0)
blue = (30, 144, 255)
lower_orange = (255, 99, 71)
upper_orange = (255, 69, 0)
yellow = (255, 226, 4)
lower_pink = (255, 171, 208)
upper_pink = (255, 20, 147)
green = (27, 210, 42)

# imageLib
shipImg = pygame.image.load(".\\.images\\spaceship.png")
##ThingImg
ufo1Img = pygame.image.load(".\\.images\\ufo1.png")
ufo2Img = pygame.image.load(".\\.images\\ufo2.png")
ufo3Img = pygame.image.load(".\\.images\\ufo3.png")
meteo2Img = pygame.image.load(".\\.images\\meteo2.png")
meteo3Img = pygame.image.load(".\\.images\\meteo3.png")
# bullet
bulletImg = pygame.image.load(".\\.images\\bullet.png")
# explosive
explosiveImg = pygame.image.load(".\\.images\\explosive.png")

titleImg = pygame.image.load(".\\.images\\coollogo.png")
iconImg = pygame.image.load(".\\.images\\ico.png")

background_rank = pygame.image.load(".\\.images\\rank_score.png")
background_menu = pygame.image.load(".\\.images\\bg.png")
background_game = pygame.image.load(".\\.images\\space.png")

# soundLib
maingameSou = pygame.mixer.Sound(".\\.sounds\\maingame.wav")
crashSou = pygame.mixer.Sound(".\\.sounds\\crash.wav")
pauseSou = pygame.mixer.Sound(".\\.sounds\\pause.wav")
unpauseSou = pygame.mixer.Sound(".\\.sounds\\unpause.wav")
shootingSou = pygame.mixer.Sound(".\\.sounds\\shooting.wav")
explosionSou = pygame.mixer.Sound(".\\.sounds\\explosion.wav")
# Load icon
pygame.display.set_icon(iconImg)
# Size of image
ship_width = 50
ship_height = 94
# global pause
pause = False
# global bullet status
bullet_status = False


def things(x, y, img):
    gameDisplay.blit(img, (int(x), int(y)))


def things_pass(count):
    font = pygame.font.SysFont(None, 25)
    strtime = datetime.datetime.now()
    text1 = font.render("Score: " + str(count), True, blue)
    text2 = font.render(f"Now: {strtime.strftime('%X')}", True, blue)
    gameDisplay.blit(text1, (0, 0))
    gameDisplay.blit(text2, (0, 18))


def ship(x, y):
    gameDisplay.blit(shipImg, (int(x), int(y)))


def bullet_display(x, y):
    global bullet_status
    if bullet_status:
        gameDisplay.blit(bulletImg, (int(x + 15), int(y - 40)))


def text_objects(text, font, color):
    text_surface = font.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_display(text, x, y, color, size):
    large_text = pygame.font.Font(None, size)
    text_surf, text_rect = text_objects(text, large_text, color)
    text_rect.center = (int(x), int(y))
    gameDisplay.blit(text_surf, text_rect)


def score_record():
    rank = False
    li_score = []
    with open(".\\.file\\score.txt", 'r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', "")
            li_score.append(int(line))
    li_score.sort(reverse=True)
    while not rank:
        mouse = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if 315 < mouse[0] < 465 and 800 < mouse[1] < 875 and event.type == pygame.BUTTON_X1:
                game_menu()
        gameDisplay.blit(background_rank, (0, 0))
        for i in range(10):
            if i == len(li_score): break
            large_text = pygame.font.Font(None, 80)
            text_surf, text_rect = text_objects(f"Rank {i + 1}: {li_score[i]}", large_text, white)
            text_rect.midleft = (int(240), int(120 + i * 70))
            gameDisplay.blit(text_surf, text_rect)
        # Menu
        button_display("Menu", 315, 800, 150, 75, 50, 387, 837, upper_pink, lower_pink)
        pygame.display.update()
        clock.tick(75)


def unpaused():
    global pause
    pause = False
    count_down = 3
    font = pygame.font.SysFont(None, 70)
    while count_down > 0:
        text = font.render(str(count_down) + "s", True, white)
        gameDisplay.blit(text, (int(display_width / 2 - 150 + (3 - count_down) * 100), int(display_height / 2 - 250)))
        count_down -= 1
        pygame.display.update()
        time.sleep(1)
    unpauseSou.play()


def paused(score):
    global pause
    maingameSou.stop()
    pauseSou.play()
    while pause:
        mouse = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p and pause:
                    unpaused()
            if 210 < mouse[0] < 360 and 500 < mouse[1] < 575 and event.type == pygame.BUTTON_X1:
                unpaused()
            if 410 < mouse[0] < 560 and 500 < mouse[1] < 575 and event.type == pygame.BUTTON_X1:
                with open(".\\.file\\score.txt", 'a', encoding='utf-8') as f:
                    f.write(f"{score}\n")
                game_menu()
        message_display("PAUSED!!", display_width / 2, display_height / 2 - 100, white, 165)
        # Continue
        button_display("Continue", 210, 500, 150, 75, 45, 282, 535, upper_orange, lower_orange)
        # Menu
        button_display("Menu", 410, 500, 150, 75, 50, 482, 535, upper_pink, lower_pink)
        pygame.display.update()
        clock.tick(75)


def crash(score):
    crashSou.play()
    with open(".\\.file\\score.txt", 'a', encoding='utf-8') as f:
        f.write(f"{score}\n")
    font = pygame.font.SysFont(None, 70)
    menu = False
    count_down = 1000
    while not menu and count_down > 0:
        # Get pos of mouse
        mouse = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if 210 < mouse[0] < 360 and 600 < mouse[1] < 675 and event.type == pygame.BUTTON_X1:
                game_loop()
            if 410 < mouse[0] < 560 and 600 < mouse[1] < 675 and event.type == pygame.BUTTON_X1:
                game_menu()
        gameDisplay.blit(background_game, (0, 0))
        message_display("You Crashed!", display_width / 2, display_height / 2 - 100, white, 165)
        text = font.render("Continue?? " + str(int(count_down / 100)) + "s", True, lower_red)
        gameDisplay.blit(text, (int(display_width / 2 - 200), int(display_height / 2 - 25)))
        # Restart
        button_display("Restart", 210, 600, 150, 75, 50, 282, 635, upper_orange, lower_orange)
        # Menu
        button_display("Menu", 410, 600, 150, 75, 50, 482, 635, upper_pink, lower_pink)
        pygame.display.update()
        time.sleep(0.006)
        count_down -= 1
    game_menu()


def button_display(text, x, y, w, h, size_font, center_x, center_y, color1, color2):
    mouse = pygame.mouse.get_pos()
    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        pygame.draw.ellipse(gameDisplay, color1, (x, y, w, h))
    else:
        pygame.draw.ellipse(gameDisplay, color2, (x, y, w, h))

    text_display = pygame.font.Font(None, size_font)
    text_display, text_rect = text_objects(text, text_display, white)
    text_rect.center = (center_x, center_y)
    gameDisplay.blit(text_display, text_rect)


def game_menu():
    menu = False
    while not menu:
        # Get pos of mouse
        mouse = pygame.mouse.get_pos()
        pygame.mouse.set_visible(True)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if 315 < mouse[0] < 465 and 425 < mouse[1] < 500 and event.type == pygame.BUTTON_X1:
                menu = True
            if 315 < mouse[0] < 465 and 525 < mouse[1] < 600 and event.type == pygame.BUTTON_X1:
                score_record()
            if 315 < mouse[0] < 465 and 625 < mouse[1] < 700 and event.type == pygame.BUTTON_X1:
                pygame.quit()
                quit()
        # text_rect_1.center = ((display_width / 2), (display_height / 2 - 150))

        gameDisplay.blit(background_menu, (0, 0))
        gameDisplay.blit(titleImg, (25, int(display_height / 2 - 250)))
        # Start
        button_display("Start", 315, 425, 150, 75, 50, 387, 464, upper_orange, lower_orange)
        # Score record
        button_display("Score Record", 315, 525, 150, 75, 30, 387, 564, upper_pink, lower_pink)
        # Quit
        button_display("Exit", 315, 625, 150, 75, 50, 387, 664, upper_red, lower_red)
        pygame.display.update()
        clock.tick(144)
    game_loop()


def game_loop():
    # Ship info
    x = (display_width * 0.45)
    y = (display_height * 0.8)

    x_change = 0
    ship_speed = 0
    # Things info
    img = [ufo1Img, ufo2Img, ufo3Img, meteo2Img, meteo3Img]
    things_img = [0] * 100
    things_start_x = [0] * 100
    things_start_y = [0] * 100
    li_check = [0] * 100
    things_speed = [0] * 100
    things_width = [0] * 100
    things_height = [0] * 100
    nums_of_things = 2
    for i in range(nums_of_things):
        things_img[i] = random.choice(img)
        things_start_x[i] = random.randrange(0, display_width)
        things_start_y[i] = random.randrange(-500, -100)
        things_speed[i] = random.randrange(2, 6)
        if things_img[i] == ufo1Img:
            things_width[i] = 95
            things_height[i] = 95
        elif things_img[i] == ufo2Img:
            things_width[i] = 89
            things_height[i] = 76
        elif things_img[i] == ufo3Img:
            things_width[i] = 95
            things_height[i] = 56
        elif things_img[i] == meteo2Img:
            things_width[i] = 49
            things_height[i] = 54
        elif things_img[i] == meteo3Img:
            things_width[i] = 105
            things_height[i] = 221

    #
    # Bullet info
    bullet_x = []
    bullet_y = []
    #
    gameExit = False
    global pause
    global bullet_status
    # Score counter
    count_score = 0
    # Game_loop in while loop
    while not gameExit:
        # Get pos of mouse
        mouse = pygame.mouse.get_pos()
        pygame.mouse.set_visible(False)
        x = mouse[0]
        y = mouse[1]
        # MaingameSound
        maingameSou.play()
        maingameSou.set_volume(0.3)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.BUTTON_X1:
                maingameSou.stop()
                shootingSou.play()
                bullet_status = True
                bullet_x.append(mouse[0])
                bullet_y.append(mouse[1])

            if event.type == pygame.KEYDOWN:
                """if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    x_change -= 5
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    x_change += 5
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    ship_speed -= 5
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    ship_speed += 5"""
                if event.key == pygame.K_p and not pause:
                    pause = True
                    paused(count_score)

            """if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d:
                    x_change = 0
                elif event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                    ship_speed = 0"""

        x += x_change
        y += ship_speed

        # Background display
        gameDisplay.blit(background_game, (0, 0))
        # Display ship,things,...
        for j in range(nums_of_things):
            things_start_y[j] += things_speed[j]
            things(things_start_x[j], things_start_y[j], things_img[j])
        # ship(x, y)#Old by keyboard
        ship(mouse[0], mouse[1])
        things_pass(count_score)
        #Check ship touch in wall
        if x < 0:
            x = 0
            pygame.mouse.set_pos(x,y)
        if x > display_width - ship_width:
            x = display_width - ship_width
            pygame.mouse.set_pos(x, y)
        if y < 0:
            y = 0
            pygame.mouse.set_pos(x, y)
        if y > display_height - ship_height:
            y = display_height - ship_height
            pygame.mouse.set_pos(x, y)
        for j in range(nums_of_things):
            if things_start_y[j] > display_height:
                things_start_y[j] = random.randrange(-500, -100)
                things_start_x[j] = random.randrange(0, display_width)
                count_score += 1
        # Bullet processing
        if bullet_status:
            for j in range(len(bullet_x)):
                bullet_display(bullet_x[j], bullet_y[j])
                bullet_y[j] -= 4
        ##Remove index bullet if bullet_y<0:
        if len(bullet_x) > 0 and bullet_y[0] < 0:
            bullet_x.pop(0)
            bullet_y.pop(0)
            if not bullet_x: bullet_status = False
        ##
        #
        # Check bullet hit things:
        a = 0
        if len(bullet_x) > 0:
            while True:
                check_hit = False
                for b in range(nums_of_things):
                    if bullet_y[a] < things_start_y[b] + things_height[b] and bullet_y[a] - things_start_y[b] > -48:
                        if things_start_x[b] < bullet_x[a] < things_start_x[b] + things_width[b] or things_start_x[b] < bullet_x[a] + 15 < \
                                things_start_x[
                                    b] + things_width[b]:
                            things(things_start_x[b], things_start_y[b], explosiveImg)
                            maingameSou.stop()
                            explosionSou.play()
                            count_score += 1
                            things_start_x[b] = random.randrange(0, display_width)
                            things_start_y[b] = random.randrange(-500, -100)
                            things_img[b] = random.choice(img)
                            things_speed[b] = random.randrange(2, 6)
                            if things_img[b] == ufo1Img:
                                things_width[b] = 95
                                things_height[b] = 95
                            elif things_img[b] == ufo2Img:
                                things_width[b] = 89
                                things_height[b] = 76
                            elif things_img[b] == ufo3Img:
                                things_width[b] = 95
                                things_height[b] = 56
                            elif things_img[b] == meteo2Img:
                                things_width[b] = 49
                                things_height[b] = 54
                            elif things_img[b] == meteo3Img:
                                things_width[b] = 105
                                things_height[b] = 221
                            check_hit = True
                            break
                if check_hit:
                    bullet_x.pop(0)
                    bullet_y.pop(0)
                    if not bullet_x: bullet_status = False
                elif not check_hit:
                    a += 1
                if not len(bullet_x) or a == len(bullet_x):
                    break
        #
        # Check crash event
        for j in range(nums_of_things):
            if y < things_start_y[j] + things_height[j] and y - things_start_y[j] > -ship_height:
                if things_start_x[j] < x < things_start_x[j] + things_width[j] or things_start_x[j] < x + ship_width < things_start_x[j] + \
                        things_width[j]:
                    maingameSou.stop()
                    crash(count_score)
        #
        # Check status if score % 15
        if count_score > 0 and count_score % 15 == 0 and not li_check[int(count_score / 5) - 1]:
            nums_of_things += 1
            index = nums_of_things - 1
            things_start_x[index] = random.randrange(0, display_width)
            things_start_y[index] = random.randrange(-500, -100)
            things_img[index] = random.choice(img)
            things_speed[index] = random.randrange(2, 6)
            if things_img[index] == ufo1Img:
                things_width[index] = 95
                things_height[index] = 95
            elif things_img[index] == ufo2Img:
                things_width[index] = 89
                things_height[index] = 76
            elif things_img[index] == ufo3Img:
                things_width[index] = 95
                things_height[index] = 56
            elif things_img[index] == meteo2Img:
                things_width[index] = 49
                things_height[index] = 54
            elif things_img[index] == meteo3Img:
                things_width[index] = 105
                things_height[index] = 221
            # Check one time
            li_check[int(count_score / 5) - 1] = int(count_score / 5)
            #
        #

        pygame.display.update()
        clock.tick(144)


game_menu()
pygame.quit()
quit()
