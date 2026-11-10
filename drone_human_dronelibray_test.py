# this Codes test different drone commands using  available Tello EDU drone libraries
from djitellopy import Tello
import cv2
import threading
import time 
stream_ready=threading.Event()
keep_running=True

#get the drone Status data 
def get_drone_status(drone):
 battery=drone.get_battery()
 avgtemp=drone.get_temperature()
 return battery,avgtemp


# stream the drone camera feed and display drone status data on the screen
def video_stream (drone):
 width=860 # wit=dth image 
 height=540#  Height image 
 print("#"*100,"\nVIDEO STREAM  STARTING \n","#"*100)
 my_stream=drone.get_frame_read()
 stream_ready.set()
 while keep_running:
   my_frame=my_stream.frame
   battery,avgtemp=get_drone_status(drone)
   cv2.putText(my_frame,f"Battery: {battery}%",(20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
   cv2.putText(my_frame,f'Temperature:{avgtemp} Celcius',(20,125),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)

   img=cv2.resize(my_frame,(width,height))
   cv2.imshow("Drone_Camera", img)
   if cv2.waitKey(1) & 0xFF==ord(' '):
    break
   
#drone flight execution 
def drone_flight(drone):
 
 stream_ready.wait() #wait for the stream video to start 
 print("Starting Drone flight")
 time.sleep(8)
 drone.takeoff()
 drone.move_forward(20)
 time.sleep(2)
 drone.rotate_clockwise(90)
 time.sleep(2)
 drone.move_forward(20)
 time.sleep(2)
 drone.rotate_clockwise(90)
 time.sleep(2)
 drone.move_forward(20)
 time.sleep(2)
 drone.land()
 time.sleep(8)
 global keep_running
 keep_running=False


#main function 
def main():
 my_drone=Tello()
 my_drone.connect()
 print("#"*100,"\nDrone Connected \n","#"*100)
 my_drone.streamon()
 stream_thread=threading.Thread(target=video_stream, args=(my_drone,))
 stream_thread.start()
 flight_thread=threading.Thread(target=drone_flight, args=(my_drone,))
 flight_thread.start()
 flight_thread.join() # waith Until the done_flight functions is executed. 
 print("Drone Flight Terminated.....Rebotting Drone")
 my_drone.reboot()

if __name__=="__main__":
 main()
    