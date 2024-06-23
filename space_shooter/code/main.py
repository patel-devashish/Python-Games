import pygame

#initialising pygame
pygame.init()

#creating screen
window_width, window_height = 1280, 720
display_surface = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Space Shooter')

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
    display_surface.fill('red')
    pygame.display.update()

#uninitializes everything and closes the game properly
pygame.quit()