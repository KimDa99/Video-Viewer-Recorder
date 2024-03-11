import cv2 as cv
import numpy as np
from datetime import datetime

ESC_KEY = 27
SPACE_KEY = 32

def Init_Video(source):
    video = cv.VideoCapture(source)
    return video

def Draw_Text(img, is_recording, is_enlarged, is_fliped, is_contrast, is_brightness, contrast, brightness):
    frame_with_text = img.copy()

    # Draw a transparent rectangle
    overlay = frame_with_text.copy()
    cv.rectangle(overlay, (10, 10), (250, 45 + 20*7), color=(0, 0, 0), thickness=-1)
    cv.addWeighted(overlay, 0.6, frame_with_text, 1 - 0.6, 0, frame_with_text)

    ## Exit
    Exit_TextPlace = (20, 30)
    cv.putText(frame_with_text, '[ESC]: Exit', Exit_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255))

    ## Recording
    Recording_TextPlace = (20,30 + 20)
    if is_recording:
        cv.putText(frame_with_text, '[SPACE]: Recording', Recording_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 0, 0, 255))
    else:
        cv.putText(frame_with_text, '[SPACE]: NOT Recording', Recording_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

    ## Magnifying
    Recording_TextPlace = (20,30 + 20*2)
    if is_enlarged:
        cv.putText(frame_with_text, '[E]: Enlarging', Recording_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 0, 0, 255))
    else:
        cv.putText(frame_with_text, '[E]: Enlarge', Recording_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

    ## Fliped
    Fliped_TextPlace = (20, 30 + 20*3)
    if is_fliped:
        cv.putText(frame_with_text, '[F]: Fliped', Fliped_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 0, 0, 255))
    else:
        cv.putText(frame_with_text, '[F]: Flip', Fliped_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

    ## +/- Controlled:
    PlusMinus_TextPlace = (20, 30 + 20*4)
    cv.putText(frame_with_text, '[+/-] Controll:', PlusMinus_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255))    

    ## Contrast
    Contrast_TextPlace = (20, 30 + 20*5)
    if is_contrast:
        cv.putText(frame_with_text, '  [C]: Contrast ' + str(contrast), Contrast_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 0, 255, 255))
    else:
        cv.putText(frame_with_text, '  [C]: Contrast ' + str(contrast), Contrast_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))

    ## Brightness
    Brightness_TextPlace = (20, 30 + 20*6)
    if is_brightness:
        cv.putText(frame_with_text, '  [B]: Brightness ' + str(brightness), Brightness_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 0, 255, 255))
    else:
        cv.putText(frame_with_text, '  [B]: Brightness ' + str(brightness), Brightness_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, (255, 255, 255))
        
    ## Reset
    Reset_TextPlace = (20, 30 + 20*7)
    cv.putText(frame_with_text, '  [R]: Reset', Reset_TextPlace, cv.FONT_HERSHEY_DUPLEX, 0.5, ( 255, 255, 255))
        
    return frame_with_text

def Draw_and_Show(img, is_recording, is_enlarged, is_fliped, is_contrast, is_brightness, contrast, brightness, mouse_xy):

    targetImage = img.copy()
    targetImage = ( 1 + 0.1*contrast)*targetImage + brightness
    targetImage[targetImage < 0] = 0
    targetImage[targetImage > 255] = 255
    targetImage = targetImage.astype(np.uint8)

    if is_fliped:
        targetImage = cv.flip(targetImage, 1)
    if is_enlarged:
        targetImage = Enlarge(targetImage, mouse_xy)

    targetImage = Draw_Text(targetImage, is_recording, is_enlarged, is_fliped, is_contrast, is_brightness, contrast, brightness)

    cv.imshow('Preview', targetImage)   # Play video

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

def mouse_event_handler(event, x, y, flags, param):
    if event == cv.EVENT_MOUSEMOVE:
        param[0] = x
        param[1] = y

def Enlarge(img, mouse_xy, zoom_box_radius = 10, zoom_level = 5, zoom_box_margin = 10):
    img_copy = img.copy()
    img_height, img_width, *_ = img.shape

    if mouse_xy[0] >= zoom_box_radius and mouse_xy[0] < (img_width - zoom_box_radius) and \
    mouse_xy[1]>= zoom_box_radius and mouse_xy[1] < (img_height - zoom_box_radius):
        img_crop = img[mouse_xy[1]-zoom_box_radius : mouse_xy[1]+zoom_box_radius, \
                       mouse_xy[0] - zoom_box_radius : mouse_xy[0] + zoom_box_radius, :]
        zoom_box = cv.resize(img_crop, None, None, zoom_level, zoom_level)
        s = img_width - zoom_box_margin - len(zoom_box)
        e = img_width - zoom_box_margin
        u = zoom_box_margin
        v = zoom_box_margin + len(zoom_box)
        img_copy[u:v, s:e,:] = zoom_box

    return img_copy

is_recording = False
is_enlarged = False
is_fliped = False
is_contrast = False
is_brightness = False

contrast = 0
brightness = 0

target_fps = 30
target_fourcc = 'MJPG'
source = 'rtsp://210.99.70.120:1935/live/cctv001.stream'

video = Init_Video(source)  # Get Video source

if video.isOpened():
    target = cv.VideoWriter()

cv.namedWindow('Preview')    
mouse_xy = [-1, -1]
cv.setMouseCallback('Preview', mouse_event_handler, mouse_xy)

while True:
    valid, img = video.read()

    if not valid:
        print("Not Valid")
        break

    Draw_and_Show(img, is_recording, is_enlarged, is_fliped, is_contrast, is_brightness, contrast, brightness, mouse_xy)    # Draw What is needed and show
    Manage_Recording(is_recording, img, target,  target_fps, target_fourcc) # Record
    key = cv.waitKey(1)

    if key == ESC_KEY:
        break
    elif key == SPACE_KEY:
        is_recording = not is_recording
    elif key == ord('E') or key == ord('e'):
        is_enlarged = not is_enlarged
    elif key == ord('F') or key == ord('f'):
        is_fliped = not is_fliped
    elif key == ord('C') or key == ord('c'):
        is_contrast = True
        is_brightness = False
    elif key == ord('B') or key == ord('b'):
        is_contrast = False
        is_brightness = True
    elif key == ord('R') or key == ord('r'):
        is_contrast = False
        is_brightness = False
        contrast = 0
        brightness = 0
    elif key == ord('+') or key == ord('='):
        if is_contrast:
            contrast += 1
        if is_brightness:
            brightness += 1
    elif key == ord('-') or key == ord('_'):
        if is_contrast:
            contrast -= 1
        if is_brightness:
            brightness -= 1    

End_Program(video, target)