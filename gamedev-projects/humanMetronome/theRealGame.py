import time
import pygame
import random
import screens

click_times = []
accuracyPercent = []
third_screen = None  # Define the third screen globally


def draw_second_screen():
    screens.draw_button(screens.button_second)  # Draw the button on the second screen


def draw_third_screen():
    screens.screen.fill(screens.WHITE)

    font = pygame.font.Font(None, 36)  # Choose the font and size for the labels
    average_accuracy_text = "Average accuracy: {:.2f}%".format(avgTimeAccuracy * 100)

    if avgTimeAccuracy >= 0.85:
        result_text = "You won!"
        # print("You won!")
        button_third = screens.ThirdScreen(screens.button_x, screens.button_y, screens.button_width,
                                           screens.button_height, screens.BLACK,
                                           str(avgTimeAccuracy * 100) + "% \n You won")
    else:
        result_text = "You lost!"
        # print("You lost!")
        button_third = screens.ThirdScreen(screens.button_x, screens.button_y, screens.button_width,
                                           screens.button_height, screens.BLACK,
                                           str(avgTimeAccuracy * 100) + "% \n You lost")

    # button_third.draw(screens.screen)  # Draw the button on the third screen

    result_surface = font.render(result_text, True, screens.BLACK)  # Render the result text
    result_rect = result_surface.get_rect(
        center=(screens.width // 2, screens.height // 2 + 50))  # Position the result text

    text_surface = font.render(average_accuracy_text, True, screens.BLACK)  # Render the label text
    text_rect = text_surface.get_rect(center=(screens.width // 2, screens.height // 2))  # Position the label

    screens.screen.blit(result_surface, result_rect)  # Blit the result text onto the third screen
    screens.screen.blit(text_surface, text_rect)  # Blit the label onto the third screen

    pygame.display.flip()


def game():
    global click_times

    # Check for spacebar press or button click event
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            click_times.append(time.time())  # Record the time of the spacebar press
            if len(click_times) == 8:
                time_diffs_sec = calculate_time_differences(click_times)
                perform_additional_calculations(time_diffs_sec)
                return

    # Check for left mouse button click event
    if pygame.mouse.get_pressed()[0] == 1:
        mouse_pos = pygame.mouse.get_pos()
        if screens.button_second.rect.collidepoint(mouse_pos):
            click_times.append(time.time())  # Record the time of the button click
            if len(click_times) == 8:
                time_diffs_sec = calculate_time_differences(click_times)
                perform_additional_calculations(time_diffs_sec)

    # Draw the second screen elements
    screens.screen.fill(screens.WHITE)
    screens.draw_button(screens.button_second)

    pygame.display.flip()


def calculate_time_differences(click_times):
    time_diffs = []
    for i in range(1, len(click_times)):
        time_diff = click_times[i] - click_times[i - 1]
        time_diffs.append(time_diff)

    time_diffs_sec = [round(diff, 2) for diff in time_diffs]  # Convert time differences to seconds

    return time_diffs_sec


def perform_additional_calculations(time_diffs_sec):
    global third_screen  # Use the global third_screen variable
    global accuracyPercent
    global avgTimeAccuracy

    sixtyByTempo = 60 / tempo
    # Perform your additional calculations or actions with the time differences
    print("Performing additional calculations with time differences:", time_diffs_sec)

    for j in range(len(time_diffs_sec)):
        if time_diffs_sec[j] <= sixtyByTempo:
            accuracyPercent.append(time_diffs_sec[j] / sixtyByTempo)
        elif time_diffs_sec[j] > sixtyByTempo:
            calcVar = (time_diffs_sec[j] / sixtyByTempo) - 1
            calcVar = 1 - calcVar
            accuracyPercent.append(calcVar)

    avgTimeAccuracy = sum(accuracyPercent) / len(accuracyPercent)

    # Switch to the third screen and draw it
    third_screen = screens.ThirdScreen(screens.button_x, screens.button_y, screens.button_width, screens.button_height,
                                       screens.BLACK, str(avgTimeAccuracy * 100) + "%")
    third_screen.draw(screens.screen)
    pygame.display.flip()


def initialMetronome():
    global tempo
    pygame.font.init()
    pygame.mixer.init()
    tempo = random.randint(40, 200)
    screens.screen.fill(screens.WHITE)
    pygame.display.flip()

    metronome_sound = pygame.mixer.Sound('metronomeBeep.mp3')  # Load the metronome sound file

    for i in range(8):
        metronome_sound.play()  # Play the metronome sound
        pygame.time.wait(int(60 / tempo * 1000))  # Wait for the appropriate duration
        metronome_sound.stop()  # Stop the metronome sound

    return tempo
