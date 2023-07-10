import pygame
import screens
import theRealGame

pygame.init()

screens.screen = pygame.display.set_mode((screens.width, screens.height))

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

running = True
active_screen = "first"  # Initial active screen is the first screen

# Draw the first screen before entering the main event loop
screens.screen.fill(WHITE)  # Clear the screen
screens.draw_button(screens.button_first)  # Draw the button on the first screen
pygame.display.flip()  # Update the display

gamedonecounter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if active_screen == "first" and event.type == pygame.MOUSEBUTTONDOWN:
            if screens.button_first.rect.collidepoint(event.pos):
                screens.screen.fill(screens.WHITE)
                theRealGame.initialMetronome()
                active_screen = "second"  # Switch to the second screen
                break

        if active_screen == "second" and (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE
                                          or event.type == pygame.MOUSEBUTTONDOWN):
            screens.screen.fill(screens.WHITE)
            theRealGame.game()

    screens.screen.fill(screens.WHITE)  # Clear the screen

    if active_screen == "first":
        screens.draw_button(screens.button_first)  # Draw the button on the first screen
    elif active_screen == "second" and len(theRealGame.click_times) < 8:
        theRealGame.draw_second_screen()
    elif active_screen == "second" and len(theRealGame.click_times) == 8:
        theRealGame.draw_third_screen()
        gamedonecounter += 1

    pygame.display.flip()  # Update the display
