import pygame

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
player_surf = pygame.image.load("space_shooter/images/player.png")

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
    #update() - updates entire window, flip() - updates part of window we want to
    #filling the screen with a colour
    display_surface.fill('darkgray')
    x += 0.1  #here is the increment to move the surface
    #display_surface.blit(surf, (x,150))           #if we remove the display_surface fill and run this code there will be a trailing effect on the 
    #surface because it is not being cleared every frame.
    display_surface.blit(player_surf, (x,150))
    pygame.display.update()

#uninitializes everything and closes the game properly
pygame.quit()