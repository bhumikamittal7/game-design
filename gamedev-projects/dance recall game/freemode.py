import pygame
import cv2
import tkinter as tk
from tkinter import messagebox
import time
import random
pygame.init()

window_width = 540
window_height = 540
from pygame import mixer
is_first_video_playing = True

mixer.init()
songpaths = [
"song.mp3","song2.mp3","song3.mp3","song4.mp3"


]
first_video_capture = cv2.VideoCapture("introfree.mp4")

mixer.music.load(random.choice(songpaths))


mixer.music.set_volume(100)


mixer.music.play()

    


window = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption('Dance Recall Free Mode')
clock = pygame.time.Clock()
videopaths = [
   "vid1.mp4","vid2.mp4","vid3.mp4","vid4.mp4","vid5.mp4","vid6.mp4","vid7.mp4","vid8.mp4","vid9.mp4","vid10.mp4"
    

]


running = True

playanim = False


while running:
    
  
    mixer.music.unpause()
     
     




    for event in pygame.event.get():
        
   
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            path = random.choice(videopaths)
            video_capture = cv2.VideoCapture(path)
            playanim = True
    
    if playanim:
       
        ret, frame = video_capture.read()

        if ret:
          frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          frame = cv2.resize(frame, (window_width, window_height))
          frame = cv2.rotate(frame, cv2.ROTATE_90_COUNTERCLOCKWISE)
          pygame_frame = pygame.surfarray.make_surface(frame)
          window.blit(pygame_frame, (0, 0))
        else:
          playanim = False
         # video_capture.release()
               
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
            first_video_capture.release()
            



  
            
        

          
   
    pygame.display.flip()

    clock.tick(30)

pygame.quit()
cv2.destroyAllWindows()
mixer.music.stop()