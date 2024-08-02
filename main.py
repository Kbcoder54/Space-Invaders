import pygame,os,random,math,sys

from pygame import mixer,mixer_music


pygame.init()






    

mixer.music.load('palms.wav')
mixer.music.play(-1)
mixer.music.set_volume(0.2)


size = (800,600)
screen = pygame.display.set_mode(size)

running =  True
pygame.display.set_caption("Space Invaders")

icon = pygame.image.load(r'ufo.png')
pygame.display.set_icon(icon)

background = pygame.image.load(r'background.jpg')
background = pygame.transform.scale(background, (size[0], size[1]))

color = 0, 0, 0

clock = pygame.time.Clock() 

global playerImg
playerX = 370
playerY = 530
Xaxis_change = 0.1

# enemyXaxis_change = 0.3
# enemyYaxis_change = 0



auto = True
manual = False

# enemyX = random.randrange(0,799) 
# enemyY = random.randrange(0,799)

enemyX = []
enemyY = []
enemyXaxis_change = []
enemyYaxis_change = []
enemyImg = []

num_of_enemies = 4

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load(r'alien.png'))
    enemyX.append(random.randrange(0,799))
    enemyY.append(random.randrange(50,200))
    enemyXaxis_change.append(0.3)
    enemyYaxis_change.append(0)



def enemy(x,y,i):
    enemyImg[i] = pygame.transform.scale(enemyImg[i],(50,50))
    screen.blit(enemyImg[i],(x,y))


global rocket_state
rocket_state = 'ready'
rocket_Y = playerY
rocket_change = 0.5

gameoverText = pygame.font.Font('freesansbold.ttf',64)



#defining a font
out_of_bounds = True



# Create a surface for the button
red_button = pygame.Surface((70, 50))
red_button.fill((255, 0, 0))

def rendertext(text,button,color=(255, 0, 0)):
    # Create a font object
    font = pygame.font.SysFont('Arial', 24)

    red_button.fill(color)
    # Render the text onto a new surface
    text_surface = font.render(f'{text}', True, (255,255,255))

    # Get the rectangle of the text surface
    text_rect = text_surface.get_rect(center=(35, 25))  # Center the text on the button

    button.blit(text_surface, text_rect)

rendertext("Auto",red_button,(255, 255, 255))

def gameover():
    over_text = gameoverText.render('Game Over',True,(255,255,255))
    screen.blit(over_text,(200,300))


def player(x,y):
    playerImg = pygame.image.load(r'player.png')
    playerImg = pygame.transform.scale(playerImg, (50, 50)) 
    screen.blit(playerImg,(x,y))

def fire(x,y):
    rocketImg = pygame.image.load(r'missile.png')
    rocketImg = pygame.transform.scale(rocketImg,(25,25))
    screen.blit(rocketImg,(x+13,y-20))

    return 'fired'

def ifKilled(rocketX,rocketY,enemyX,enemyY):
    a = math.pow(rocketX-enemyX,2)
    b = math.pow(rocket_Y-enemyY,2)
    distance = math.sqrt((a+b))
    if distance < 15:
        return True
    else:
        return False

    


def automove(change):
    if event.type == pygame.KEYDOWN: 
        if event.key == pygame.K_LEFT or event.key == pygame.K_a: 
            change = -0.3 
        if event.key == pygame.K_RIGHT or event.key == pygame.K_d: 
            change = 0.3
    return change

def usermove(x):
    key_pressed_is = pygame.key.get_pressed() 
    if key_pressed_is[pygame.K_LEFT] or key_pressed_is[pygame.K_a]: 
        x -= 8
    if key_pressed_is[pygame.K_RIGHT] or key_pressed_is[pygame.K_d]: 
        x += 8
    return x


global score
score = 0

def show_score():
    font = pygame.font.SysFont('Arial', 18)
    placeholder = font.render('Score:'+str(score),True,(255,255,0))
    return placeholder
    

    


number = 0
knum = 0

rocketImg = pygame.image.load(r'missile.png')
rocketImg = pygame.transform.scale(rocketImg,(25,25))
rocket_X = 0


global killed
killed = [False for i in range(num_of_enemies)]



while running:
    hovered = True
    
    screen.fill(color) #draw the screen
    screen.blit(background,(0,0))

    clock.tick(240)
    mouse = pygame.mouse.get_pos()
    
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

         
        pos = pygame.mouse.get_pos()
        x,y = pos


        

        
        if red_button.get_rect().collidepoint(pos):
            
            if pygame.mouse.get_pressed()[0] == True:
                manual = True
                auto = False
                number = number + 1

           
        if number % 2 == 0:
            auto = True
            manual = False

        if manual == True:
            rendertext('Manual',red_button,(0,0,255))

        if auto == True:
            rendertext('Auto',red_button,(255,0,0))

        
        
        if auto == True:
            Xaxis_change = automove(Xaxis_change)

    if auto == True:
        playerX += Xaxis_change
    if manual == True:
        playerX = usermove(playerX)


    

    key_pressed = pygame.key.get_pressed() 
    if key_pressed[pygame.K_SPACE] or key_pressed[pygame.MOUSEBUTTONUP]:
        if rocket_state == 'ready': #to make sure rocket dosent follow the player
            temp = playerX
        rocket_state = 'fired'
        
    if rocket_Y < 0: #TO FIRE MULTIPLE BULLETS
        rocket_Y = 530
        rocket_state = 'ready'
    
    if (rocket_state == 'fired'):
        fired_effect = mixer.Sound('laser.wav')
        fired_effect.play()
        
        screen.blit(rocketImg,(temp+13,rocket_Y-20))
        
        rocket_Y -= 2.5
        if (rocket_Y >= size[1]):
            rocket_state = 'ready'
        rocket_X = temp

    

    


    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(num_of_enemies):
        if enemyY[i] > 600:
            for j in range(num_of_enemies):
                enemyY[j] = 1000
            gameover()
            pygame.time.delay(5000)
            
            
        if enemyX[i] <= 0:
            enemyXaxis_change[i] = 0.3
            enemyYaxis_change[i] = 0.1
        elif enemyX[i] >= 736:
            enemyXaxis_change[i] = -0.3
            enemyYaxis_change[i] = 0.1

        enemyX[i] += enemyXaxis_change[i]
        enemyY[i] += enemyYaxis_change[i]

        tempkilled = ifKilled(rocket_X,rocket_Y,enemyX[i],enemyY[i])
        if tempkilled:
            rocket_Y = 530
            temp = playerX
            score += 1
            
            killed[i] = True
            kill_effect = mixer.Sound('explosion.wav')
            kill_effect.play()
            

        
        if killed[i] == False:
        
            enemy(enemyX[i],enemyY[i],i)
        
        
    
        
        
    player(playerX,playerY) #draw player over the screen
    
    
    

    screen.blit(show_score(),(700,50))
        
    screen.blit(red_button,(0, 0))
    pygame.display.flip()
    
    pygame.display.update()



pygame.quit()