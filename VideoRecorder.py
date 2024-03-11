import cv2 as cv
from datetime import datetime

ESC_KEY = 27
SPACE_KEY = 32

def Init_Video(source):
    video = cv.VideoCapture(source)
    return video

def Draw_and_Show(img, is_recording):
    frame_with_text = img.copy()    

    ## Recording
    Recording_TextPlace = (50,50)
    if is_recording:
        cv.putText(frame_with_text, 'Recording', Recording_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 0, 0, 255))
    else:
        cv.putText(frame_with_text, 'NOT Recording', Recording_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 0))

    cv.imshow('Preview', frame_with_text)   # Play video

def Record(img, target, target_fps, target_fourcc):
    if not target.isOpened():
        target_file = datetime.now().strftime("%Y%m%d_%H%M%S") + '.avi'
        h,w,*_ = img.shape
        is_color = (img.ndim >2) and (img.shape[2]>1)
        target.open(target_file, cv.VideoWriter_fourcc(*target_fourcc), target_fps, (w,h), is_color)        
    
    target.write(img)        
    return

def End_Program(video, target):
    video.release()  # Release the video capture object
    target.release()
    cv.destroyAllWindows()

    print("Ends program")

def Manage_Recording(is_recording, img, target, target_fps, target_fourcc):
    if is_recording:
        Record(img, target, target_fps, target_fourcc)
    elif target.isOpened(): # Close when the recording is done
        target.release()

# To Do
# [] Zoom in Mouse Area : Z
# [] Flip: F
# [] Image Subtraction: S
# [] Filters: +/-
    # [] Contrast: C
    # [] Brightness: B
    # [] Rotate: R
# [] Reset: T

is_recording = False
target_fps = 30
target_fourcc = 'MJPG'
source = 'rtsp://210.99.70.120:1935/live/cctv001.stream'

video = Init_Video(source)  # Get Video source

if video.isOpened():
    target = cv.VideoWriter()

while True:
    valid, img = video.read()

    if not valid:
        print("Not Valid")
        break

    if key == ESC_KEY: # Exit: ESC
        break
    elif key == SPACE_KEY:   # Record on/off: Space
        if is_recording == True:
            is_recording = False
        else:
            is_recording = True

    Draw_and_Show(img, is_recording)    # Draw What is needed and show
    Manage_Recording(is_recording, img, target,  target_fps, target_fourcc) # Record
    key = cv.waitKey(1)

End_Program(video, target)