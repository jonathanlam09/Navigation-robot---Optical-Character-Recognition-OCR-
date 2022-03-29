import imutils                              #Image processing library with various function
from imutils.video import VideoStream       #Import videostream function from imutils library
from imutils.video import FPS               #Import frame per second function from imutils library
import pytesseract                          #Import pytesseract library for character detection function
import cv2                                  #Import Opencv for image preprocessing functions
import time                                 #Import time for time related functions
import re

user_bed = []                               #Assign variable "user_bed" to an empty function

while True:                                 #Initiate infinite while loop
    patient = input("Enter Bed Num\n")      #Prompt user input and assigned input to variable "patient"
    if (patient == "q"):                    #Initiate if function with condition if input = q
        break                               #Break while loop
    user_bed.append(str(patient))           #Convert input value to string data type and append into user_bed 
print(user_bed)                             #Print list with appended inputs

print("[INFO] starting video stream")           
vs = VideoStream(src=0).start()                 #Declare VideoStream source and start running into variable "vs"
time.sleep(5.0)                                 #Delay 2s
fps = FPS().start() 
                       #Call FPS function and start for VideoStream purpose

def extraction():
    while True:                                      #Initiate infinite while loop
        frame = vs.read()                               #Read function to read each frame 
        frame = imutils.resize(frame, width=500)        #Resize frame
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)   #Convert frame to gray scale

        _, binary_image = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU)  #Enhance gray scale pixel contrast
            
        final_image = cv2.copyMakeBorder(binary_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=(255, 255, 255)) 
        #Add padding
        cv2.imshow('final', final_image)                                                                            
        #Display processed frame
        txt = pytesseract.image_to_string(final_image, config='--psm 13 --oem 1 -c tessedit_char_whitelist=0123456789')
        #Extract characters from final_image and configure all 3 flags for pytesseract library
        list = re.findall(r'\d+', txt)
        print(list)

        if (list != []):                                    #Initiate if with condition
            if list[0] in user_bed:                         #Initiate nested if condition
                vs.stop()                                   #Stop VideoStream
                fps.stop()                                  #Stop frames
                cv2.destroyAllWindows()                     #Destroy all windows
                print ("Arrived at Bed " + list[0] + ". Door open, 60s till door close.")   #Print arrived bed number
                user_bed.remove(list[0])                    #Remove detected bed number from list
                time.sleep(5.0)                             #5s delay
                print("Restarting VideoStream")             #Print restarting video stream
                vs.start()                                  #Start VideoStreaming
                fps.start()                                 #Start FPS
                extraction()                                #Go to extraction function

        key = cv2.waitKey(1) & 0xFF                         #Declare key to call opencv wait key function
        if key == ord('q'):                                 #If key is 'q'
            break                                           #Break infinite while loop
extraction()                                                #Run extraction function
fps.update()                                                #Update FPS
fps.stop()                                                  #Stop frames
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))  #Print total frame run time
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))       #Print approximate FPS during run time
cv2.destroyAllWindows()                                     #Destroy all windows
vs.stop()                                                   #Stop Video Stream

