from PIL import Image 
import pytesseract as pyt
import cv2
import numpy as np
from STT import stt_min,tts

def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

def remove_noise(image):
    return cv2.medianBlur(image,5)
 
def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def dilate(image):
    kernel = np.ones((2,1),np.uint8)
    return cv2.dilate(image, kernel, iterations = 1)

def erode(image):
    kernel = np.ones((2,1),np.uint8)
    return cv2.erode(image, kernel, iterations = 1)

def opening(image):
    kernel = np.ones((5,5),np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

def canny(image):
    return cv2.Canny(image, 100, 200)

def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED) 

def ocr(image):

    gray = get_grayscale(image)
    gray = cv2.bitwise_not(gray)

    img = erode(image)
    img = dilate(image)

    custom_config = r'-l eng --oem 3 --psm 6'
    output = pyt.image_to_string(img, config = custom_config)
    
    read_short = output.split("\n")
    tts(read_short[0])

    for i in range(len(output)):
        
        if output[i] == "\n":
            tts("Do you want to continue reading?")
            operation = stt_min(3)
            if operation == "yes":
                tts(output)
                break
            else:
                tts("Goodbye")
                break
	

    


