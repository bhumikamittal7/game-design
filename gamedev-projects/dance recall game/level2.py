import pygame
import cv2
import tkinter as tk
from tkinter import messagebox
from pygame import mixer
pygame.init()
import random

window_width = 540
window_height = 540

window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Dance Recall Level 2')
clock = pygame.time.Clock()
mixer.init()
songpaths = [
"song.mp3","song2.mp3","song3.mp3","song4.mp3"


]
mixer.music.load(random.choice(songpaths))


mixer.music.set_volume(100)


mixer.music.play()

video_paths = {
    'a': "a-part1.mp4",
    'z': "z-part1.mp4",
    'y': "y-part1.mp4",
    'c': "c-part1.mp4",
    'n': "n-part1.mp4",
    'q': "q-part1.mp4",
    'm': "m-part2.mp4",
    'f': "f-part2.mp4",
    'b': "b-part2.mp4",
    'k': "k-part2.mp4",
    'o': "o-part2.mp4",
    'p': "p-part2.mp4"

}

video_captures = {key: cv2.VideoCapture(path) for key, path in video_paths.items()}
is_video_playing = False
sequence = []
iscorrectsequence = False
issequenceincorrect = False
is_first_video_playing = True
first_video_path = "intro2.mp4"
first_video_capture = cv2.VideoCapture(first_video_path)
running = True
while running:
    mixer.music.unpause()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
          if not is_first_video_playing:
            key = pygame.key.name(event.key)
            if key in video_paths:
                sequence.append(key)
                is_video_playing = True
                if not iscorrectsequence and sequence != ['a', 'z', 'y', 'c', 'n', 'q','m','f','b','k','o','p'][:len(sequence)]:
                    issequenceincorrect = True
            else:
                sequence = []
                is_video_playing = False
                win = pygame.image.load("lost2.png").convert()
                window.blit(win, (0, 0))

    if issequenceincorrect:
        win = pygame.image.load("lost2.png").convert()
        window.blit(win, (0, 0))
        issequenceincorrect = False

    if is_first_video_playing:
        ret, frame = first_video_capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (window_width, window_height))
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame = cv2.flip(frame,0)
            pygame_frame = pygame.surfarray.make_surface(frame)
            window.blit(pygame_frame, (0, 0))
        else:
            is_first_video_playing = False
            win = pygame.image.load("ntro.png").convert()
            window.blit(win, (0, 0))
            first_video_capture.release()

    if is_video_playing:
        if sequence == ['a', 'z', 'y', 'c', 'n', 'q','m','f','b','k','o','p']:
            iscorrectsequence = True

        key = sequence[-1]
        video_capture = video_captures[key]

        ret, frame = video_capture.read()

        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = cv2.resize(frame, (window_width, window_height))
            frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
            frame = cv2.flip(frame,0)
            pygame_frame = pygame.surfarray.make_surface(frame)
            window.blit(pygame_frame, (0, 0))
        else:
            is_video_playing = False
            video_capture.release()

            if iscorrectsequence and key == 'p':
                win = pygame.image.load("won2.png").convert()
                window.blit(win, (0, 0))

                #messagebox.showinfo("Game Over", "You won!")


    pygame.display.flip()

    clock.tick(30)

for video_capture in video_captures.values():
    video_capture.release()

pygame.quit()