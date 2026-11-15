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

# color tracking ariables set up
stream_ready=threading.Event()
keep_running=True
emergency_stop=True
target_data=(0,0,0)
tracking_mode= False

# drone_voice command set up 
cmd_end_time =0
cmd_speed=[0,0,0,0]

####### Voice Model Variables####
model = Model(r"C:\Users\princ\Documents\Project\computerscience\PYTHON\Model")
allowed_commands = [
    "take off",
    "land",
    "forward",
    "backward",
    " go left",
    "go right",
    "go up",
    "go down",
    "turn right",
    "turn left",
    "flip back" ,
    "stop",
    "follow",
    'unfollow',
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
 while keep_running:
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
 stream.stop_stream()
 stream.close()
 mic.terminate()

#################################voice command  ################################
def voice_commands(drone,text):
  stream_ready.wait()
  global tracking_mode
  global cmd_speed
  global cmd_end_time
  dist = distance(text) 
  duration=dist/40
  rot_duration=dist/22
  text = text.lower()
  try:       
    if "take off" in text:
        drone.takeoff()
    elif "land" in text:
        drone.land()
    elif "forward" in text:
        cmd_speed=[0,40,0,0]
        cmd_end_time = time.time() + duration
    elif  "backward" in text:
         cmd_speed=[0,-40,0,0]
         cmd_end_time = time.time() + duration
    elif "go up" in text :
        cmd_speed=[0,0,40,0]
        cmd_end_time = time.time() + duration
    elif "go down" in text :
        cmd_speed=[0,0,-40,0]
        cmd_end_time = time.time() + duration
    elif "turn right" in  text:
        cmd_speed=[0,0,0,40]
        cmd_end_time = time.time() + rot_duration
    elif "turn left" in  text:
        cmd_speed=[0,0,0,-40]
        cmd_end_time = time.time() + rot_duration
    elif "go left" in text:
        cmd_speed=[-40,0,0,0]
        cmd_end_time = time.time() + duration
    elif "go right" in text:
         cmd_speed=[40,0,0,0]
         cmd_end_time = time.time() + duration
    elif "unfollow" in text:
        tracking_mode=False
        cmd_speed=(0,0,0,0)
        cmd_end_time=0
    elif "follow" in text:
       tracking_mode=True
    elif"stop" in  text:
           drone.send_rc_control(0,0,0,0)
           print("stopping drone")
           cmd_speed=(0,0,0,0)
           cmd_end_time=0
    else:
        print("Command not recognized.")


  except  djitellopy.tello.TelloException:
        pass 

################## drone flight function 
def drone_flight(drone):
    stream_ready.wait()
    global tracking_mode 
    global cmd_speed
    global cmd_end_time
    while keep_running:
      if not tracking_mode:
         drone.send_rc_control(*cmd_speed)
         if time.time()>= cmd_end_time and cmd_end_time !=0:  
             drone.send_rc_control(0,0,0,0)
             cmd_speed=(0,0,0,0)
             cmd_end_time=0
      time.sleep(0.04)

######### distance finder function         
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
    return 60

###### Video stream function ######
def video_stream (drone):
 global keep_running
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
         if tracking_mode:
          cv2.rectangle(my_frame,(x,y),(x+w,y+h),(0,0,255),3) #draws the rectangle on my_frame 
          cv2.circle(my_frame,(cx,cy,),5,(0,255,0),-1)
          ###############aesthetic added 
   if tracking_mode:
    cv2.rectangle(my_frame,(2,2),(width-2,height-2),(0,0,255),3)
    cv2.rectangle(my_frame,(220,120),(320,220),(255,255,0),1) # Cyan center deadzone box
    cv2.line(my_frame,(260,170),(280,170),(255,255,0),1) # Horizontal crosshair
    cv2.line(my_frame,(270,160),(270,180),(255,255,0),1) # Vertical crosshair
    cv2.rectangle(my_frame,(355, 15),(530, 45),(0, 0, 180),-1)
    cv2.putText(my_frame," TRACKING MODE ON",(362, 35),cv2.FONT_HERSHEY_SIMPLEX,0.45,(255, 255, 255),2,cv2.LINE_AA)
   else:
    cv2.rectangle(my_frame,(355, 15),(530, 45),(40, 40, 40),-1)
    cv2.putText(my_frame," VOICE MODE",(362, 35),cv2.FONT_HERSHEY_SIMPLEX,0.45,(255, 255, 255),2,cv2.LINE_AA) 
   target_data=(cx,cy,area)
   cv2.imshow("Masqued_video",mask)
   cv2.imshow("Drone_camera",my_frame)
   wait_key=cv2.waitKey(1) &0xFF
   if wait_key==ord('q'):
      tracking_mode=False
   elif wait_key==ord('e'):
      keep_running=False
      drone.send_rc_control(0,0,0,0) 
 drone.streamoff() 
 cv2.destroyAllWindows() 

############################ color tracking function##############################
def drone_color_tracking(drone):
  stream_ready.wait()
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
     if area >400:
     #rotational speed 
      if cx < (center_x-50):
       yaw_speed-=49
      elif cx>(center_x+50):
       yaw_speed+=49
     #vertical speed 
      if  cy<(center_y-50):
       vertical_speed+=30
      elif  cy>(center_y+50):
       vertical_speed-=30
      if   area <8000:
       fwd_speed=25
      elif area >35000:
       fwd_speed-=25
     drone.send_rc_control(horizontal_speed, fwd_speed, vertical_speed,yaw_speed)
     print(horizontal_speed, fwd_speed, vertical_speed,yaw_speed)
   time.sleep(0.04)
   
   
#get the drone Status data s
def get_drone_status(drone):
 battery=drone.get_battery()
 avgtemp=drone.get_temperature()
 return battery,avgtemp

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
   flight_thread=threading.Thread(target=drone_flight,args=(my_drone,))
   flight_thread.start()
  except djitellopy.tello.TelloException:
   print("#"*100,"\n CONNECTION ERROR.. CHECK DRONE CONNECTION  \n","#"*100)
if __name__=="__main__":
 main()
   
