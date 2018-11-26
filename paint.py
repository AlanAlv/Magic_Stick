# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 16:05:08 2018

@author: A01630612
"""

import numpy as np
import cv2
from collections import deque
import Tkinter
import tkMessageBox


# Define the upper and lower boundaries for a color to be considered "Blue"
#blueLower = np.array([100, 60, 60])
#blueUpper = np.array([140, 255, 255])
blueLower = (29, 86, 6)
blueUpper = (64, 255, 255)

# Define a 5x5 kernel for erosion and dilation
kernel = np.ones((5, 5), np.uint8)

# Initialize deques to store different colors in different arrays
bpoints = [deque(maxlen=512)]
gpoints = [deque(maxlen=512)]
rpoints = [deque(maxlen=512)]
ypoints = [deque(maxlen=512)]

# Initialize an index variable for each of the colors 
bindex = 0
gindex = 0
rindex = 0
yindex = 0

# Just a handy array and an index variable to get the color-of-interest on the go
# Blue, Green, Red, Yellow respectively
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)] 
colorIndex = 0

# Create a blank white image
paintWindow = np.zeros((471,636,3)) + 255

# Draw buttons like colored rectangles on the white image
paintWindow = cv2.rectangle(paintWindow, (0,1), (100,65), (255,255,255), -2)
paintWindow = cv2.rectangle(paintWindow, (0,80), (100,145), colors[0], -1)
paintWindow = cv2.rectangle(paintWindow, (0,160), (100,225), colors[1], -1)
paintWindow = cv2.rectangle(paintWindow, (0,240), (100,305), colors[2], -1)
paintWindow = cv2.rectangle(paintWindow, (0,320), (100,385), colors[3], -1)
paintWindow = cv2.rectangle(paintWindow, (0,400), (100,465), (0, 0,0), -2)

# Label the rectanglular boxes drawn on the image
cv2.putText(paintWindow, "Borrar", (9, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "Azul", (9, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "Verde", (9, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "Rojo", (9, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "Amarillo", (9, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA)
cv2.putText(paintWindow, "Guardar", (9, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)

# Create a window to display the above image (later)
cv2.namedWindow('Paint', cv2.WINDOW_AUTOSIZE)

# Load the video
camera = cv2.VideoCapture(0)

def nothing(*arg):
    pass

cv2.namedWindow('Tracking')
cv2.createTrackbar('Brightness', 'Tracking', 1, 255, nothing)
cv2.createTrackbar('Contrast', 'Tracking', 1, 255, nothing)

# Keep looping
while True:
    
    Brillo = cv2.getTrackbarPos('Brightness', 'Tracking')
    Contraste = cv2.getTrackbarPos('Contrast', 'Tracking')
    
    # Grab the current paintWindow
    (grabbed, frame) = camera.read()
    frame = cv2.addWeighted(frame, 1. + Contraste / 127., frame, 0, Brillo - Contraste)
    frame = cv2.flip(frame, 1)
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Check to see if we have reached the end of the video (useful when input is a video file not a live video stream)
    if not grabbed:
        break    
    
    # Add the same paint interface to the camera feed captured through the webcam (for ease of usage)
    frame = cv2.rectangle(frame, (0,1), (100,65), (255,255,255), -2)
    frame = cv2.rectangle(frame, (0,80), (100,145), colors[0], -1)
    frame = cv2.rectangle(frame, (0,160), (100,225), colors[1], -1)
    frame = cv2.rectangle(frame, (0,240), (100,305), colors[2], -1)
    
    
    frame = cv2.rectangle(frame, (0,320), (100,385), colors[3], -1)
    frame = cv2.rectangle(frame, (0,400), (100,465), (0,0,0), -2)
    cv2.putText(frame, "Borrar", (9, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
    cv2.putText(frame, "Azul", (9, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Verde", (9, 180), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Rojo", (9, 260), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Amarillo", (9, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2, cv2.LINE_AA)
    cv2.putText(frame, "Guardar", (9, 420), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2, cv2.LINE_AA)
    

 # Determine which pixels fall within the blue boundaries and then blur the binary image
    blueMask = cv2.inRange(hsv, blueLower, blueUpper)
    blueMask = cv2.erode(blueMask, kernel, iterations=2)
    blueMask = cv2.morphologyEx(blueMask, cv2.MORPH_OPEN, kernel)
    blueMask = cv2.dilate(blueMask, kernel, iterations=1)

    # Find contours in the image
    (_, cnts, _) = cv2.findContours(blueMask.copy(), cv2.RETR_EXTERNAL,
    	cv2.CHAIN_APPROX_SIMPLE)
    
 # Check to see if any contours (blue stuff) were found
    if len(cnts) > 0:
    	# Sort the contours and find the largest one -- we assume this contour correspondes to the area of the bottle cap
        cnt = sorted(cnts, key = cv2.contourArea, reverse = True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)
        # Draw the circle around the contour
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
        # Get the moments to calculate the center of the contour (in this case a circle)
        M = cv2.moments(cnt)
        center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))


        if center[0] <= 100:
            if 1 <= center[1] <= 65: # Clear All
                  # Empty all the point holders
                  bpoints = [deque(maxlen=512)]
                  gpoints = [deque(maxlen=512)]
                  rpoints = [deque(maxlen=512)]
                  ypoints = [deque(maxlen=512)]
                  # Reset the indices
                  bindex = 0
                  gindex = 0
                  rindex = 0
                  yindex = 0
                  # Make the frame all white again
                  paintWindow[:,99:,:] = 255
            # When the contour center touches a box, assign its appropriate color            
            elif 80 <= center[1] <= 145:
                  colorIndex = 0 # Blue
            elif 160 <= center[1] <= 225:
                  colorIndex = 1 # Green
            elif 240 <= center[1] <= 305:
                  colorIndex = 2 # Red
            elif 320 <= center[1] <= 385:
                    colorIndex = 3 # Yellow
            elif 400 <= center[1] <= 465:
                    cv2.imwrite( "saved.jpg", paintWindow );
                    #tkMessageBox.showinfo("Guardado","Imagen Guardada")
                    
        # Store the center (point) in its assigned color deque
        else :
            if colorIndex == 0:
                bpoints[bindex].appendleft(center)
            elif colorIndex == 1:
                gpoints[gindex].appendleft(center)
            elif colorIndex == 2:
                rpoints[rindex].appendleft(center)
            elif colorIndex == 3:
                ypoints[yindex].appendleft(center)
            
              
    # Draw lines of all the colors (Blue, Green, Red and Yellow)
    points = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(points)):
        for j in range(len(points[i])):
            for k in range(1, len(points[i][j])):
                if points[i][j][k - 1] is None or points[i][j][k] is None:
                    continue
                cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 5)
                cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 5)

    # Show the frame and the paintWindow image
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)

    # If the 'q' key is pressed, stop the loop
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
    
    
# Cleanup code
camera.release()
cv2.destroyAllWindows()