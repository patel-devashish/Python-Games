import pygame
#for using the join function below
from os.path import join
from random import randint, uniform

#organising the code using Sprites(classes with surface and rect inbuilt) in pygame
class Player(pygame.sprite.Sprite):
    def __init__(self, groups):
        super().__init__(groups)
        self.image = pygame.image.load(join("space_shooter", "images", "player.png")).convert_alpha()
        self.rect = self.image.get_frect(center=(window_width/2, window_height/2))
        self.direction = pygame.Vector2()
        self.speed = 300
        #cooldown - to not give the player unlimited power of shooting lasers and give the laser a cooldown duration in which it doesent fire even if pressed
        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 200

        #mask - makes the visible pixels white and the invisible, black.
        #below three lines show mask in action
        # mask = pygame.mask.from_surface(self.image)
        # mask_surf = mask.to_surface()
        # self.image = mask_surf
        # self.mask = pygame.mask.from_surface(self.image)  #no need
    
    def laser_timer(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt

        recent_keys = pygame.key.get_just_pressed()
        if recent_keys[pygame.K_SPACE] and self.can_shoot:
            Laser(laser_surf, self.rect.midtop, (all_sprites, laser_sprites))
            self.can_shoot = False
            self.laser_shoot_time = pygame.time.get_ticks()
            laser_sound.play()
        self.laser_timer()
class Star(pygame.sprite.Sprite):
    def __init__(self, groups, surf):
        super().__init__(groups)
        self.image = surf
        #to optimize the code, we can write the above line outside the class, since this class is being called 20 times, this 
        #line will be called 20 times, which is not efficient.
        self.rect = self.image.get_frect(center = (randint(0, window_width), randint(0, window_height)))
class Laser(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_frect(midbottom = pos)
        # self.mask = pygame.mask.from_surface(self.image)
    
    def update(self, dt):
        self.rect.centery -= 400 * dt
        #now since so much lasers are being shot every laser still exists though not visible in the screen, so to solve that we need to destroy them
        #once they are out of the screen.
        if self.rect.bottom <= 0:
            self.kill()
class Meteor(pygame.sprite.Sprite):
    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_frect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5),1)
        self.speed = randint(400, 500)
        # self.mask = pygame.mask.from_surface(self.image)    #no need
        self.rotaion_speed = randint(40, 80)
        self.rotaion = 0

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill() #well we can use the laser logic to kill meteor sprites which is more suitable but giving here another approach
        self.rotaion += self.rotaion_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotaion, 1)
        self.rect = self.image.get_frect(center = self.rect.center)    

class AnimatedExplosion(pygame.sprite.Sprite):
    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = frames[self.frame_index]
        self.rect = self.image.get_frect(center = pos)

    def update(self, dt):
        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index)]
        else:
            self.kill()

def collision():
    global running
    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True, pygame.sprite.collide_mask) #once specified here, we dont need to create the mask surface in every rect.
    if collision_sprites:    
        running = False

    for laser in laser_sprites:
        collided_sprites = pygame.sprite.spritecollide(laser, meteor_sprites, True)
        if collided_sprites:
            laser.kill()
            AnimatedExplosion(explosion_frames, laser.rect.midtop, all_sprites)
            explosion_sound.play()

def display_score():
    current_time = pygame.time.get_ticks() // 100
    text_surf = font.render(str(current_time), True, (240 ,240,240))
    text_rect = text_surf.get_rect(midbottom = (window_width / 2, window_height - 50))
    display_surface.blit(text_surf,text_rect)
    pygame.draw.rect(display_surface, (240,240,240), text_rect.inflate(20,20).move(0,-8), 5, 10) #this wraps a rectangle around the score but with no padding
    #inflate method adds the padding here. But you will notice that the rect is a bit stretched downwards (foe letters like p, j, etc. which use down space more). 
    # To move that up we use move

#initialising pygame
pygame.init()

#creating screen
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space Shooter')
running = True
clock  = pygame.time.Clock() # it can control the frame rate

#plain surface creation
# surf = pygame.Surface((100,200))
# surf.fill('orange')
#now this surface created will only be visible when we actually attach or join it to the display surface by 
#using the blit method in the draw section of while loop.
#blit method - draws the surface on the display surface

#now let's try to move our surface. We do that by in[de]crementing the position of surface in the loop
# x = 100 
all_sprites = pygame.sprite.Group() #using pygame Group to draw and update sprites 
meteor_sprites = pygame.sprite.Group() #creating seperate sprite for meteor for sprite collision
laser_sprites = pygame.sprite.Group() #same as above
star_surf = pygame.image.load(join("space_shooter", "images", "star.png")).convert_alpha() #through this, we are doing the import once
for i in range(20):
    Star(all_sprites, star_surf)  #the order of these instance of classes decide which layer is on top of the other
player = Player(all_sprites) #instance of Player class
#importing an image - using image as a surface (same using blit)
# now since different OS has different preference of slashes when writing the path of a file, to make the code universally accepted
# we will use the jion function instead to write the file path instead of the string, "space_shoooter/images/player.png"
# print(join("space_shooter", "images", "player.png"))
#convert_alpha() - to increase fps as this conversion makes it easier for pygame to process
# player_surf = pygame.image.load(join("space_shooter", "images", "player.png")).convert_alpha()
# #using RECT concept for surface pos and placement
# player_rect = player_surf.get_frect(center=(window_width/2, window_height/2))
# #the goal is to bounce the player off the walls left and right so we define direction with 1 for right and -1 for left
# player_direction = pygame.math.Vector2() # using vectors for movement and direction
# #when developing actual games we want the above values to be fairly low to control speed
# player_speed = 300

# star_surf = pygame.image.load(join("space_shooter", "images", "star.png")).convert_alpha()
# star_positions = [(randint(0, window_width), randint(0, window_height)) for i in range(20)]

meteor_surf = pygame.image.load(join("space_shooter", "images", "meteor.png")).convert_alpha()
#meteor_rect = meteor_surf.get_frect(center = (window_width/2, window_height/2))

laser_surf = pygame.image.load(join("space_shooter", "images", "laser.png")).convert_alpha()
#laser_rect = laser_surf.get_frect(bottomleft = (20, window_height-20))

#creating font
font = pygame.font.Font(join("space_shooter","images","Oxanium-Bold.ttf"), 40)
# text_surf = font.render('text', True, (240 ,240,240))

explosion_frames = [pygame.image.load(join("space_shooter", "images", "explosion", f"{i}.png")).convert_alpha() for i in range(21)]

laser_sound = pygame.mixer.Sound(join("space_shooter","audio","laser.wav"))
laser_sound.set_volume(0.2)
explosion_sound = pygame.mixer.Sound(join("space_shooter","audio","explosion.wav"))
explosion_sound.set_volume(0.2)
# damage_sound = pygame.mixer.Sound(join("space_shooter","audio","damage.ogg")) #game over as soon as hit by meteor
game_music = pygame.mixer.Sound(join("space_shooter","audio","game_music.wav"))
game_music.set_volume(0.1)
game_music.play(loops = -1) # -1 for indefinite loop as expected from a game music

#working with time using custom events
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

#to keep the code running and keep the screen visible, we can run the following code:
# while True:
#     pass
# but this does not give us the option of closing the screen and we have an error in doing so.
# So we use the following code:
while running:
    dt = clock.tick() / 1000 #specify the frame rate
    #using the delta time concept to give the game equal speed in any pc i.e. framerate independence
    #so now the argument inside tick() will change only how often we draw the game when earlier it changed the speed as well
    #print(clock.get_fps())
    #event loop - we can access all the events.
    for event in pygame.event.get():
        #if the user wants to quit the game
        if event.type == pygame.QUIT:
            running = False
        # getting user input through event loop
        # if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
        #     print(1)
        #getting input in the event loop, the output is displayed only once even if the button is pressed down continuously.
        #to check, uncomment the above two lines.
        # if event.type == pygame.MOUSEMOTION:
        #     player_rect.center = event.pos
        
        if event.type == meteor_event:
            x,y = randint(0, window_width), randint(-200, -100)
            Meteor(meteor_surf, (x,y), (all_sprites, meteor_sprites))

    #input
    #print(pygame.mouse.get_rel())
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_1]:
    #     print(1)
    #getting input outside the event loop, the output keeps getting displayed as long as the button in being pressed down.
    #to check, uncomment the above three lines.
    # keys = pygame.key.get_pressed()
    # if keys[pygame.K_RIGHT]:
    #     player_direction.x = 1
    # else:
    #     player_direction.x = 0
    # condensing above 4 lines in one line and also adding left movement
    # player_direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT])
    # player_direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP])
    # player_direction = player_direction.normalize() if player_direction else player_direction
    # #line just above reduces the diagonal speed to one which got increased to greater than 1 due to vector sum of two directions
    # player_rect.center += player_direction * player_speed * dt
    # #print(player_direction)

    #exercise 2
    #does what the event loop does, despite holding the spacebar, "fire laser" printing once
    # recent_keys = pygame.key.get_just_pressed()
    # if recent_keys[pygame.K_SPACE]:
    #     print("fire laser")

    all_sprites.update(dt)

    #sprite collision
    collision()

    #draw the game - take all the elements in the while loop before and draws it
    #also the drawing order matters, as we go down, things drawn are layered on top of the things already drawn
    #so the player will be on top of the stars, so rearrange.
    #update() - updates entire window, flip() - updates part of window we want to
    #filling the screen with a colour
    display_surface.fill("#3a2e3f")
    #display_surface.blit(surf, (x,150))           #if we remove the display_surface fill and run this code there will be a trailing effect on the 
    #surface because it is not being cleared every frame.
    #for i in range(20):
        #display_surface.blit(star_surf, (randint(0, window_width), randint(0, window_height)))
        #this bit of code upwards creates twinkling stars which rerenders every frame of the game as this runs inside the while loop.
        #to stop that we can run the randint part outside the loop and use it once inside.
    # for pos in star_positions:
    #     display_surface.blit(star_surf, pos)
    #display_surface.blit(meteor_surf, meteor_rect)
    #display_surface.blit(laser_surf, laser_rect)

    #player movement
    # if player_rect.right < window_width: #to stop the spaceship going out of the screen
    #     player_rect.left += 0.2 #we increment the value to move it
    # player_rect.x += player_direction * 1     # x here means left and similarly y means right
    # if player_rect.right > window_width or player_rect.left < 0:
    #     player_direction *= -1 #this will reverse the direction of the player

    #exercise 1 
    # if player_rect.right >= window_width or player_rect.left <= 0:
    #     player_direction[0] *= -1
    # elif player_rect.bottom >= window_height or player_rect.top <= 0:
    #     player_direction[1] *= -1
    # player_rect.center += player_direction * player_speed * dt
    # display_surface.blit(player_surf, player_rect) # player_rect or any rect is player_rect.topleft by default
    # display_surface.blit(player.image, player.rect) #bad (but possible) approach to display
    display_score()
    all_sprites.draw(display_surface)
    
    #drawing lines and polygons
    # pygame.draw.line(display_surface, "red", (0,0), (500,500), 10)
    # pygame.draw.rect(display_surface, "red", player.rect)

    pygame.display.update()


    # point and rect collision 
    # print(player.rect.collidepoint(pygame.mouse.get_pos()))
    # print(player_rect.colliderect(<any rect>))

#uninitializes everything and closes the game properly
pygame.quit()