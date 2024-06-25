import pygame
#for using the join function below
from os.path import join
from random import randint

#initialising pygame
pygame.init()

#creating screen
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space Shooter')

#plain surface creation
surf = pygame.Surface((100,200))
surf.fill('orange')
#now this surface created will only be visible when we actually attach or join it to the display surface by 
#using the blit method in the draw section of while loop.
#blit method - draws the surface on the display surface

#now let's try to move our surface. We do that by in[de]crementing the position of surface in the loop
x = 100 

#importing an image - using image as a surface (same using blit)
# now since different OS has different preference of slashes when writing the path of a file, to make the code universally accepted
# we will use the jion function instead to write the file path instead of the string, "space_shoooter/images/player.png"
# print(join("space_shooter", "images", "player.png"))
#convert_alpha() - to increase fps as this conversion makes it easier for pygame to process
player_surf = pygame.image.load(join("space_shooter", "images", "player.png")).convert_alpha()
star_surf = pygame.image.load(join("space_shooter", "images", "star.png")).convert_alpha()
star_positions = [(randint(0, window_width), randint(0, window_height)) for i in range(20)]
#to keep the code running and keep the screen visible, we can run the following code:
# while True:
#     pass
# but this does not give us the option of closing the screen and we have an error in doing so.
# So we use the following code:
running = True
while running:
    #event loop - we can access all the events.
    for event in pygame.event.get():
        #if the user wants to quit the game
        if event.type == pygame.QUIT:
            running = False


    #draw the game - take all the elements in the while loop before and draws it
    #also the drawing order matters, as we go down, things drawn are layered on top of the things already drawn
    #so the player will be on top of the stars, so rearrange.
    #update() - updates entire window, flip() - updates part of window we want to
    #filling the screen with a colour
    display_surface.fill('darkgray')
    #display_surface.blit(surf, (x,150))           #if we remove the display_surface fill and run this code there will be a trailing effect on the 
    #surface because it is not being cleared every frame.
    for pos in star_positions:
    #for i in range(20):
        #display_surface.blit(star_surf, (randint(0, window_width), randint(0, window_height)))
        #this bit of code upwards creates twinkling stars which rerenders every frame of the game as this runs inside the while loop.
        #to stop thatwe can run the randint part outside the loop and use it once inside.
        display_surface.blit(star_surf, pos)
    x += 0.2  #here is the increment to move the surface
    display_surface.blit(player_surf, (x,150))
    pygame.display.update()

#uninitializes everything and closes the game properly
pygame.quit()