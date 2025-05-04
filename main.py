import pygame
from sys import exit
from random import randint

def Time():
    CurTime = int(pygame.time.get_ticks() / 1000) - startTime
    score = Font.render("score: " + str(CurTime), False, (64, 64, 64))
    score_HitBox  = score.get_rect(topleft = (10, 100))
    screen.blit(score, score_HitBox)
    print(CurTime)
    return CurTime

def enemy_movement(enemy_list):
    if enemy_list:
        for enemy_HitBox in enemy_list:
            enemy_HitBox.x -= 5

            if enemy_HitBox.bottom == 300:
                screen.blit(snail, enemy_HitBox)
            else:
                screen.blit(fly, enemy_HitBox)
                



        enemy_list = [enemy for enemy in enemy_list if enemy.x > -100]

        return enemy_list
    else: return []

def collision(player, enemy):
    if enemy:
        for enemy_HitBox in enemy:
            if player.colliderect(enemy_HitBox): return False
    return True        

def player_animation():
    global player, player_index

    if player_HitBox.bottom < 300:
        player = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): player_index = 0 
        player = player_walk[int(player_index)]

def Coins():
    Coin_counter_text = Font.render("Coins: " + str(Coin_counter), False, (64, 64, 64))
    Coin_counter_text_HitBox = Coin_counter_text.get_rect(topleft = (10, 10))
    screen.blit(Coin_counter_text, Coin_counter_text_HitBox)

pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("CoinCollector")

# Variables
clock = pygame.time.Clock()
Font = pygame.font.Font("font/pixeltype.ttf", 100)
gameIsActive = False
startTime = 0
Zeit = 0

# Text
menu_welcomer = Font.render("Welcome to PixelRunner", False, (111, 196, 169))
menu_welcomer_HitBox = menu_welcomer.get_rect(center = (400, 70))
menu_befehl = Font.render('Press "Space" to play', False, (111, 196, 169))
menu_befehl_HitBox = menu_befehl.get_rect(center = (400, 340))

Coin_counter = 0
Coin_counter_text = Font.render("Coins: " + str(Coin_counter), False, (64, 64, 64))
Coin_counter_text_HitBox = Coin_counter_text.get_rect(topleft = (10, 10))

# Background
sky = pygame.image.load("graphics/Sky.png").convert()
ground = pygame.image.load("graphics/ground.png").convert()

# enemys
snail1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_ani = [snail1, snail2]
snail_index = 0
snail = snail_ani[snail_index]

fly1 = pygame.image.load("graphics/fly/fly1.png").convert_alpha()
fly2 = pygame.image.load("graphics/fly/fly2.png").convert_alpha()
fly_ani = [fly1, fly2]
fly_index = 0
fly = fly_ani[fly_index]

enemy_HitBox_list = []

# Coin 
Coin = pygame.image.load("graphics/Coin.png").convert_alpha()
Coin_HitBox = Coin.get_rect(center = (400, 200))

# Player
player1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player1, player2]
player_index = 0
player_jump = pygame.image.load("graphics/player/jump.png").convert_alpha()
player = player_walk[player_index]

player_HitBox = player.get_rect(midbottom = (80, 300))
Gravity = 0

#* Player menu
player_menu = pygame.image.load("graphics/player/player_stand.png").convert_alpha()
player_menu = pygame.transform.rotozoom(player_menu, 0, 2)
player_menu_HitBox = player_menu.get_rect(center = (400, 200))

# Timer
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

snail_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_timer, 200)

fly_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_timer, 200)

# forever Loop des Games
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        # Jump Motion Player
        if gameIsActive:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if player_HitBox.bottom == 300:
                        Gravity = -20

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                gameIsActive = True
                startTime = int(pygame.time.get_ticks() / 1000)

        if gameIsActive:        
            if event.type == enemy_timer and gameIsActive:
                if randint(0, 2):
                    enemy_HitBox_list.append(snail.get_rect(midbottom = (randint(900, 1100), 300)))
                else:
                    enemy_HitBox_list.append(fly.get_rect(midbottom = (randint(900, 1100), 210)))
            
            if event.type == snail_timer:
                if snail_index == 0: snail_index = 1
                else: snail_index = 0
                snail = snail_ani[snail_index]

            if event.type == fly_timer:
                if fly_index == 0: fly_index = 1
                else: fly_index = 0
                fly = fly_ani[fly_index]

    if gameIsActive:

        # GUI
        screen.blit(sky, (0, 0))
        screen.blit(ground, (0, 300))
        Zeit = Time()

        enemy_HitBox_list = enemy_movement(enemy_HitBox_list)

        # Coin
        screen.blit(Coin, Coin_HitBox)
        if player_HitBox.colliderect(Coin_HitBox):
            Coin_counter += 1
            Coin_HitBox.center = (randint(50, 750), randint(20, 270))
        Coins()

        # Player 
        #* Gravity declaration 
        Gravity += 1
        player_HitBox.y += Gravity

        #* Boden Collision
        if player_HitBox.bottom >= 300:
            player_HitBox.bottom = 300

        #* Movement left/right
        d_key = pygame.key.get_pressed()
        a_key = pygame.key.get_pressed()
        if d_key [pygame.K_d]:
            player_HitBox.x += 5
        if a_key [pygame.K_a]:
            player_HitBox.x -= 5
        screen.blit(player, player_HitBox)

        gameIsActive = collision(player_HitBox, enemy_HitBox_list)
        player_animation()

    else: 
        screen.fill((94, 129, 162))
        screen.blit(player_menu, player_menu_HitBox)
        enemy_HitBox_list.clear()
        player_HitBox.midbottom = (80, 300)
        Gravity = 0
        Zeit_menu = Font.render("Your Time: " + str(Zeit), False, (111, 196, 169))
        Zeit_menu_HitBox = Zeit_menu.get_rect(center = (400, 340))
        screen.blit(menu_welcomer, menu_welcomer_HitBox)
        Coin_counter = 0
        if Zeit == 0:
            screen.blit(menu_befehl, menu_befehl_HitBox)
        else:
            screen.blit(Zeit_menu, Zeit_menu_HitBox)

    pygame.display.update() # jeder Frame wird geUpdated
    clock.tick(60) # FPS = 60