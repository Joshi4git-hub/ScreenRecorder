import cv2 import numpy as np from datetime import datetime import mss import mss.tools from win32api import GetSystemMetrics 
 
# Informing the user we’re getting ready for recording  print("Let’s start capturing your screen and webcam”) 
 
# Get screen resolution screen_width = GetSystemMetrics(0) screen_height = GetSystemMetrics(1) print(f"Detected screen resolution: {screen_width}x{screen_height}") 
 
# Set filename with timestamp timestamp = datetime.now().strftime("%Y-%m-%d %H-%M-%S") output_filename = f"recording_{timestamp}.mp4" 
 
# Define video writer using mp4 codec fourcc = cv2.VideoWriter_fourcc(*'mp4v') video_writer = cv2.VideoWriter(output_filename, fourcc, 30.0, (screen_width, screen_height))  # 30 FPS for smoothness 
 
# Initialize webcam webcam = cv2.VideoCapture(0) if not webcam.isOpened(): 
    print("Error: Unable to access webcam.") 
    exit() 
 
# Define webcam overlay size (relative to screen size if you want it dynamic) overlay_width = 320 overlay_height = 240 
 
# Initialize MSS for fast screen capture sct = mss.mss() 
 
# Screen capture area (full screen) monitor = {"top": 0, "left": 0, "width": screen_width, "height": screen_height} 
 
# Start recording loop try:     while True: 
        # Capture screen using MSS         screen = sct.grab(monitor)         screen_frame = np.array(screen) 
        screen_frame = cv2.cvtColor(screen_frame, cv2.COLOR_BGRA2BGR)  # Remove alpha channel if any 
 
        # Capture webcam frame         ret, webcam_frame = webcam.read() 
        if not ret: 
            print("Warning: Webcam frame not captured.") 
            break 
 
        # Resize webcam frame for overlay         webcam_small = cv2.resize(webcam_frame, (overlay_width, overlay_height)) 
 
        # Create a rounded corner rectangle for webcam overlay (optional, for animation style) 
        webcam_small = cv2.copyMakeBorder(webcam_small, 2, 2, 2, 2, cv2.BORDER_CONSTANT, value=[255, 255, 255]) 
 
        # Overlay webcam onto the screen capture (top-left corner)         screen_frame[10:10 + overlay_height, 10:10 + overlay_width] = webcam_small 
 
        # Display the output in a window         cv2.imshow('Live Recording (Press S to Stop)', screen_frame) 
 
        # Save the frame to output file         video_writer.write(screen_frame) 
 
        # Exit if 's' is pressed         if cv2.waitKey(1) & 0xFF == ord('s'):             print("Recording stopped by user.")             break 
 
except KeyboardInterrupt: 
    print("Recording interrupted by user.") 
 
finally: 
    # Release all resources     webcam.release()     video_writer.release()     cv2.destroyAllWindows()     print(f"Recording saved as: {output_filename}") 
