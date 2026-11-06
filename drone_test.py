import time
import sys
import threading
from djitellopy import Tello

# Global flag to check if emergency landing was triggered
emergency_triggered = False

def emergency_stop_listener(drone):
    """Listens for manual keyboard input to kill flight and land instantly."""
    global emergency_triggered
    print("\n🛑 EMERGENCY SYSTEM ACTIVE: Press [Enter] at any time to land the drone immediately!")
    
    # Wait for the user to press Enter in the console
    input()
    
    emergency_triggered = True
    print("\n⚠️ EMERGENCY KEY PRESSED! Overriding flight sequence...")
    try:
        drone.land()
        print("✅ Emergency landing command sent.")
    except Exception as e:
        print(f"Error during emergency landing: {e}")
    sys.exit(0)

def run_controlled_flight():
    global emergency_triggered
    
    # 1. Initialize and connect
    drone = Tello()
    try:
        drone.connect()
    except Exception as e:
        print(f"❌ Connection failed: {e}. Check your Tello Wi-Fi network.")
        return

    # Check battery before takeoff
    battery = drone.get_battery()
    print(f"🔋 Starting Battery: {battery}%")
    if battery < 20:
        print("❌ Battery too low for safe flight test. Recharge first!")
        return

    # 2. Start the emergency safety thread
    safety_thread = threading.Thread(target=emergency_stop_listener, args=(drone,), daemon=True)
    safety_thread.start()

    try:
        # Step 1: Take Off
        print("\n🚀 Step 1: Taking off...")
        drone.takeoff()
        if emergency_triggered: return

        # Step 2: Hover for 5 seconds
        print("⏰ Step 2: Hovering in place for 5 seconds...")
        for i in range(5, 0, -1):
            if emergency_triggered: return
            print(f"   Hovering... {i}")
            time.sleep(1)

        # Step 3: Move forward 30 cm
        print("➡️ Step 3: Moving forward 30 cm...")
        if not emergency_triggered:
            drone.move_forward(30)  # Value must be between 20-500 cm
         #step4: Circle 
        print("➡️ Step 5: Circling  50 cm around...")
        print('Starting smooth circle...')

# send_rc_control parameters: (left_right, forward_backward, up_down, yaw)
# Speeds range from -100 to 100.
# We set forward speed to 40 and yaw (spin right) speed to 40.
        drone.send_rc_control(0, 40, 0, 40)

# Keep streaming those speeds for 6 seconds to complete the circle
# (Adjust this time based on battery/wind to hit a perfect 360)
        time.sleep(20)

        print('Stopping circle...')
# CRITICAL: Tell the drone to stop moving before landing,
# otherwise it will keep drifting due to inertia!
        drone.send_rc_control(0, 0, 0, 0)
        time.sleep(1)

        # Step 5: Land Safely
        print("🛬 Step 4: Test complete. Landing...")
        if not emergency_triggered:
            drone.land()
        print("🏁 Flight finished successfully!")
        

    except Exception as e:
        print(f"\n❌ Flight error encountered: {e}")
        print("Attempting safety landing...")
        try:
            drone.land()
        except:
            pass

if __name__ == "__main__":
    run_controlled_flight()

