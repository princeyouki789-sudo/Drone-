from djitellopy import Tello
import cv2
import threading
import time 
import numpy as np 
import djitellopy
import pyaudiowpatch
import json
import sys
from vosk import Model, KaldiRecognizer


############################################## Variables#######################################e####################################
#####DRONE Variables######
#color detection
lower_value=np.array([85,80,50])
upper_value=np.array([125,255,255])
#Variables set up
stream_ready=threading.Event()
keep_running=True
emergency_stop=True
target_data=(0,0,0)
tracking_mode= False

####### Voice Model Variables####
model = Model(r"C:\Users\princ\Documents\Project\computerscience\PYTHON\Model")
allowed_commands = [
    "take off",
    "land",
    "forward",
    "backward",
    "left",
    "right",
    "up",
    "down",
    "rotate clockwise",
    "rotate counterclockwise",
    "flip back" ,
    "stop",
    "follow",
     "twenty", "thirty", "forty", "fifty", "sixty", "eighty", "one hundred",
    "centimeters",
        "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety",
    "one hundred", "one hundred and ten", "one hundred and twenty", "one hundred and thirty",
    "one hundred and forty", "one hundred and fifty", "one hundred and sixty",
    "one hundred and seventy", "one hundred and eighty", "one hundred and ninety",
    "two hundred", "two hundred and ten", "two hundred and twenty", "two hundred and thirty",
    "two hundred and forty", "two hundred and fifty", "two hundred and sixty",
    "two hundred and seventy", "two hundred and eighty", "two hundred and ninety",
    "three hundred", "three hundred and ten", "three hundred and twenty",
    "three hundred and thirty", "three hundred and forty", "three hundred and fifty",
    "three hundred and sixty", "three hundred and seventy", "three hundred and eighty",
    "three hundred and ninety", "four hundred", "four hundred and ten",
    "four hundred and twenty", "four hundred and thirty", "four hundred and forty",
    "four hundred and fifty", "four hundred and sixty", "four hundred and seventy",
    "four hundred and eighty", "four hundred and ninety", "five hundred",
    "[unk]"
]

recognizer = KaldiRecognizer(model, 16000, json.dumps(allowed_commands))
#################################################################################################################
#####################voice function #############################################




def voice(drone):
 stream_ready.wait()
 mic = pyaudiowpatch.PyAudio()
 stream = mic.open(format=pyaudiowpatch.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=4096)
 print("#"*100,"\n AUDIO RECORD STARTING \n","#"*100)
 while True:
    try:
        data = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            spoken_text = (result.get("text", ""))
            print(spoken_text)
            if spoken_text:
                voice_commands(drone, spoken_text)
    except OSError:
       pass 
    
    
#################################voice command  ################################
def voice_commands(drone,text):
 stream_ready.wait()
 while True:
  global tracking_mode
  dist = distance(text) or 30
  duration=dist/40
  text = text.lower()
  cmd_end_time = 0
  yaw_speed=0
  vertical_speed=0
  fwd_speed=0
  horizontal_speed=0
  try:       
    if "take off" in text:
        drone.takeoff()
    elif "land" in text:
        drone.land()

    elif "forward" in text:
        fwd_speed=+40
    elif  "backward" in text:
        print(f"Moving backward {dist} cm")
        fwd_speed-=40
    elif "up" in text :
        vertical_speed+=40
    elif "down" in text :
        vertical_speed-=40
    elif "left" in text:
         horizontal_speed-=40
    elif "right" in text:
        horizontal_speed+=40
    elif "rotate clockwise" in  text:
        yaw_speed=40
    elif "rotate counterclockwise" in  text:
        yaw_speed=-40
    elif "flip forward" in text:
        drone.flip_forward()
    # elif "flip back" in text:
    #     drone.flip_back()
    #     print("Flipping back")
    # elif "flip left" in text:
    #     drone.flip_left()
    #     print("Flipping left")
    # elif "flip right" in text:
    #     drone.flip_right()
    #     print("Flipping right")
    elif "follow off" in text:
        tracking_mode=False
    elif "follow" in text:
       tracking_mode=True
       break
    elif"stop" in  text:
           drone.send_rc_control(0,0,0,0)
           print("stopping drone")
    else:
        print("Command not recognized.")
    drone.send_rc_control(horizontal_speed, fwd_speed, vertical_speed,yaw_speed)
    print(horizontal_speed, fwd_speed, vertical_speed,yaw_speed)
    time.sleep(0.04)
  #################### no distance provided##########################
   # else:
   #  while True:
   #      if "forward" in text:
   #         drone.send_rc_control(0,20,0,0)
   #         print("moving forward")  
   #      elif "back" in text or "backward" in text:
   #             print("Moving backward")
   #             drone.send_rc_control(0,-20,0,0)
   #      elif "up" in text or "climb" in text: 
   #             print("Going up")
   #             drone.send_rc_control(0,0,20,0)
   #      elif "down" in text or "descend" in text:
   #            print('going down')
   #            drone.send_rc_control(0,0,-20,0)
   #      elif "left" in text:
   #             drone.send_rc_control(-20,0,0,0)
   #      elif "right" in text:
   #              drone.send_rc_control(20,0,0,0)
   #      elif "rotate clockwise" in text or "turn right" in text:
   #             drone.send_rc_control(0,0,0,20)
   #             print("Rotating clockwise 90 degrees")
   #      elif "rotate counterclockwise" in text or "turn left" in text:
   #             drone.send_rc_control(0,0,0,-20)
   #             print("Rotating counterclockwise 90 degrees")
   #      elif"stop" in text or" hold" in text or "hover" in text:
   #         drone.send_rc_control(0,0,0,0)
   #      else:
   #              print("###Command not recognized.")
   # time.sleep(0.05)
  except  djitellopy.tello.TelloException:
        pass 
        

def distance(spoken_text):
# word to number Dictionary
    wtn = {"twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60, "seventy": 70, "eighty": 80, "ninety": 90, "one hundred": 100,
            "one hundred and ten": 110, "one hundred and twenty": 120, "one hundred and thirty": 130, "one hundred and forty": 140, 
            "one hundred and fifty": 150, "one hundred and sixty": 160, "one hundred and seventy": 170, "one hundred and eighty": 180,
            "one hundred and ninety": 190, "two hundred": 200, "two hundred and ten": 210, "two hundred and twenty": 220,
            "two hundred and thirty": 230, "two hundred and forty": 240, "two hundred and fifty": 250, "two hundred and sixty": 260,
            "two hundred and seventy": 270, "two hundred and eighty": 280, "two hundred and ninety": 290, "three hundred": 300, 
            "three hundred and ten": 310, "three hundred and twenty": 320,
            "three hundred and thirty": 330, "three hundred and forty": 340, "three hundred and fifty": 350, "three hundred and sixty": 360,
            "three hundred and seventy": 370, "three hundred and eighty": 380, "three hundred and ninety": 390, "four hundred": 400,
            "four hundred and ten": 410, "four hundred and twenty": 420, "four hundred and thirty": 430, "four hundred and forty": 440,
            "four hundred and fifty": 450, "four hundred and sixty": 460, "four hundred and seventy": 470, "four hundred and eighty": 480,
            "four hundred and ninety": 490, "five hundred": 500}
    wtn1=sorted(wtn,reverse=True,key=len)
    for word in wtn1:
       if word in spoken_text.lower():
        return wtn[word]
    return 30 
###### Video stream function ######
def video_stream (drone):
 width= 540
 height=340 
 print("#"*100,"\nVIDEO STREAM  STARTING \n","#"*100)
 my_stream=drone.get_frame_read()
 stream_ready.set() # Gives the green signal for the drone flight functions to start
 cv2.namedWindow("Drone_camera")
 cv2.namedWindow("Masqued_video")
 cv2.moveWindow("Drone_camera",50,100)
 cv2.moveWindow("Masqued_video",600,100)
 while keep_running:
   global target_data 
   global tracking_mode
   cx,cy,area=0,0,0
   my_frame=my_stream.frame
   my_frame= cv2.resize(my_frame,(width,height))
   my_frame=cv2.cvtColor(my_frame,cv2.COLOR_RGB2BGR)
   battery,avgtemp=get_drone_status(drone)
   cv2.putText(my_frame,f"Battery: {battery}%",(20,40),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)
   cv2.putText(my_frame,f'Temperature: {avgtemp} Celcius',(20,80),cv2.FONT_HERSHEY_SIMPLEX,0.5,(0,255,0),2)

   img=cv2.cvtColor(my_frame,cv2.COLOR_BGR2HSV) #convert your image into a HSV format
   mask=cv2.inRange(img,lower_value,upper_value) #get the filter balck and white image 
   contours,h = cv2.findContours(mask,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) # get coordinates of tthe tracking object 
   if len(contours)!=0:
     max_object=max(contours,key=cv2.contourArea)
     area=cv2.contourArea(max_object)
     if cv2.contourArea(max_object)>500: #calculate area of the rectangle surrounding the object 
         x,y,w,h=cv2.boundingRect(max_object) #get the rectangular coordinates of the shape 
         cx=x+w//2
         cy=y+h//2
         cv2.rectangle(my_frame,(x,y),(x+w,y+h),(0,0,255),3) #draws the rectangle on my_frame 
         cv2.circle(my_frame,(cx,cy,),5,(0,255,0),-1)
   target_data=(cx,cy,area)
   cv2.imshow("Masqued_video",mask)
   cv2.imshow("Drone_camera",my_frame)
   wait_key=cv2.waitKey(1) &0xFF
   if wait_key==ord('q'):
      tracking_mode=False
   elif wait_key==ord('e'):
     sys.exit() 
 drone.streamoff() 
 cv2.destroyAllWindows() 
 
############################ color tracking function##############################
def drone_color_tracking(drone):
  global keep_running
  while keep_running:
   center_x=270
   center_y=170
   yaw_speed=0
   vertical_speed=0
   fwd_speed=0
   horizontal_speed=0
   if tracking_mode:
     global target_data
     cx,cy,area=target_data
     if area >500:
     #rotational speed 
      if cx < (center_x-50):
       yaw_speed-=40
      elif cx>(center_x+50):
       yaw_speed+=40
     #vertical speed 
      if  cy<(center_y-50):
       vertical_speed+=40
      elif  cy>(center_y+50):
       vertical_speed-=40
      if   area <8000:
       fwd_speed=+40
      elif area >35000:
       fwd_speed-=40
     drone.send_rc_control(horizontal_speed, fwd_speed, vertical_speed,yaw_speed)
     print(horizontal_speed, fwd_speed, vertical_speed,yaw_speed)
     time.sleep(0.04)
   else:
      break 

#get the drone Status data s
def get_drone_status(drone):
 battery=drone.get_battery()
 avgtemp=drone.get_temperature()
 return battery,avgtemp


# #drone flight execution  function 
# def drone_flight(drone):
 
#  stream_ready.wait() #wait for the stream video to start 
#  print("Starting Drone flight")
#  time.sleep(8)
#  drone.takeoff()
#  drone.move_forward(20)
#  time.sleep(2)
#  drone.rotate_clockwise(90)
#  time.sleep(2)
#  drone.move_forward(20)
#  time.sleep(2)
#  drone.rotate_clockwise(90)
#  time.sleep(2)
#  drone.move_forward(20)
#  time.sleep(2)
#  drone.land()
#  time.sleep(8)
#  global keep_running
#  keep_running=False
 


#main function 
def main():
 try:
  my_drone=Tello()
  my_drone.connect()
  print("#"*100,"\nDrone Connected \n","#"*100)
  my_drone.streamon()
  stream_thread=threading.Thread(target=video_stream, args=(my_drone,))
  stream_thread.start()
  tracking_thread=threading.Thread(target=drone_color_tracking,args=(my_drone,))
  tracking_thread.start()
  voice_thread=threading.Thread(target=voice,args=(my_drone,))
  voice_thread.start()
  command_thread=threading.Thread(target=voice_commands,args=(my_drone,))
  command_thread.start()

#  flight_thread.join() # waith Until the done_flight functions is executed before excecuting the follwing commands 
# print("Drone Flight Terminated.....Rebotting Drone")
 #my_drone.reboot()
 except djitellopy.tello.TelloException:
   print("#"*100,"\n CONNECTION ERROR.. CHECK DRONE CONNECTION  \n","#"*100)
if __name__=="__main__":
 main()
   


