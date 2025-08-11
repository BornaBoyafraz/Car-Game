#Car game
#press Q or Esc to Quit

# import LIB
import pygame
import pygame.locals
import random


pygame.init()
icon = pygame.image.load('Car-Game/Images/Car_gif.gif')
pygame.display.set_icon(icon)



#VAR num (int, float, ...)
width = 500
height = 500
speed = 2
score = 0
high_score = 0
fps = 120
marker_width = 10
marker_height = 50
left_lane = 150
center_lane = 250
right_lane = 350
lane_marker_move_y = 0
player_x = 250
player_y = 400

#Creat screen
screen_size = (width, height)
screen = pygame.display.set_mode(screen_size)
pygame.display.set_caption('Car Game')

# VAR colors(red , blue , ...)
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)
black = (0, 0, 0)

# VAR bool(True, False)
game_over = False
running = True

#list
road = (100, 0, 300, height)
left_edge_marker = (95, 0, marker_width, height)
right_edge_marker = (395, 0,marker_width, height)
lanes = [left_lane, center_lane, right_lane]

#game loop
clock = pygame.time.Clock()


#def
def Play_Music(music_name, vol):
    pygame.mixer.init()
    pygame.mixer.music.load(music_name)
    pygame.mixer.music.set_volume(vol)
    pygame.mixer.music.play()


# class
class Vehicle(pygame.sprite.Sprite):

    def __init__(self, image, x, y):
        pygame.sprite.Sprite.__init__(self)

        #scale the image down so it fits in the lane
        image_scale = 45 / image.get_rect().width
        new_width = image.get_rect().width * image_scale
        new_height = image.get_rect().height * image_scale
        self.image = pygame.transform.scale(image, (new_width, new_height))

        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

class PlayerVehicle(Vehicle):

    def __init__(self, x, y):
        image = pygame.image.load('Car-Game/Images/car.png')
        super().__init__(image, x, y)

#creat the player's car
player_group = pygame.sprite.Group()
player = PlayerVehicle(player_x, player_y,)
player_group.add(player)

# load the other vehical images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = []
for image_filename in image_filenames:
    image = pygame.image.load('Car-Game/Images/' + image_filename)
    vehicle_images.append(image) 


#sprite group for vehical
vehicle_group = pygame.sprite.Group()

crash = pygame.image.load('Car-Game/Images/crash.png')
crash_rect = crash.get_rect()


while running:

    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_LEFT and player.rect.center[0] > left_lane or \
                event.key == pygame.K_a and player.rect.center[0] > left_lane:
                player.rect.x -= 100
            if event.key == pygame.K_RIGHT and player.rect.center[0] < right_lane or\
                event.key == pygame.K_d and player.rect.center[0] < right_lane:
                player.rect.x += 100
            if event.key == pygame.K_SPACE and game_over:
                pass

            for vehicle in vehicle_group:
                if pygame.sprite.collide_rect(player, vehicle):
                    game_over = True

                    if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        player.rect.left = vehicle.rect.right
                        crash_rect.center = [player.rect.left, (player.rect.center[1] + vehicle.rect.center[1]) / 2]
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        player.rect.right = vehicle.rect.left
                        crash_rect.center = [player.rect.right, (player.rect.center[1] + vehicle.rect.center[1])/ 2]

    #draw the gass
    screen.fill(green)

    #draw the road
    pygame.draw.rect(screen, gray, road)

    # draw the edge marker 
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # draw the lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= marker_height * 2:
        lane_marker_move_y = 0 

    for y in range(marker_height * (-2), height, marker_height * 2):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, marker_width, marker_height))
        
    
    # draw the player's car
    player_group.draw(screen)

    # add up to two vehicles
    if len(vehicle_group) < 2:
        
        add_vehicle = True
        for vehicle in vehicle_group:
            if vehicle.rect.top < vehicle.rect.height * 1.5:
                add_vehicle = False
        
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, height / (-2))
            vehicle_group.add(vehicle)

    
    if game_over == False: 
        for vehicle in vehicle_group:
            vehicle.rect.y += speed

            if vehicle.rect.top >= height:
                vehicle.kill()
                score += 1
                Play_Music('Car-Game/Images/point.mp3', 1)

                if score > 0 and score % 5 == 0:
                    speed += 1
            
            if score > high_score:
                high_score = score

    else:
        pass
    
    vehicle_group.draw(screen)

    font = pygame.font.Font(pygame.font.get_default_font(), 13)
    score_text = font.render('Score: ' + str(score), True, white)
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (50, 450)
    screen.blit(score_text, score_text_rect)
    
    high_score_text = font.render('High Score: ' + str(high_score), True, white)
    high_score_text_rect = high_score_text.get_rect()
    high_score_text_rect.center = (50, 470)
    screen.blit(high_score_text, high_score_text_rect)

    font = pygame.font.Font(pygame.font.get_default_font(), 10)
    q_to_quit = font.render('Press "Q" to Quit', True, white)
    q_to_quit_rect = q_to_quit.get_rect()
    q_to_quit_rect.center = (50, 50)
    screen.blit(q_to_quit, q_to_quit_rect)

    
    if pygame.sprite.spritecollide(player, vehicle_group, True):
        game_over = True
        crash_rect.center = [player.rect.center[0], player.rect.top]
    
    if game_over:
        screen.blit(crash, crash_rect)

        pygame.draw.rect(screen, red, (0, 50 , width, 100))

        font = pygame.font.Font (pygame.font.get_default_font(), 16)
        text = font.render('Game Over. Press "Space" to play again. Press "Q" to Quit', True, white)
        text_rect = text.get_rect()
        text_rect.center = (width/ 2, 100)
        screen.blit(text, text_rect)
        Play_Music('Car-Game/Images/Crash.mp3', .2)


    pygame.display.flip()


    while game_over:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q or event.key == pygame.K_ESCAPE:
                    game_over = False
                    running = False
                if event.key == pygame.K_SPACE:           
                    speed = 2
                    score = 0
                    vehicle_group.empty()
                    player.rect.center = [player_x, player_y]
                    game_over = False

pygame.quit()
