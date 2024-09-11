"""
Example of how to connect pymavlink to an autopilot via an UDP master
"""

# Disable "Bare exception" warning
# pylint: disable=W0702

import time
# Import mavutil
from pymavlink import mavutil

# Create the master
#  If using a companion computer
#  the default master is available
#  at ip 192.168.2.1 and the port 14550
# Note: The master is done with 'udpin' and not 'udpout'.
#  You can check in http:192.168.2.2:2770/mavproxy that the communication made for 14550
#  uses a 'udpbcast' (client) and not 'udpin' (server).
#  If you want to use QGroundControl in parallel with your python script,
#  it's possible to add a new output port in http:192.168.2.2:2770/mavproxy as a new line.
#  E.g: --out udpbcast:192.168.2.255:yourport
master = mavutil.mavlink_master('udp:0.0.0.0:14550')

# Make sure the master is valid
master.wait_heartbeat()

# Get some information !
while True:
    command = int(input("enter menu\n1. get gps data\n2. arm\n3. disarm\n4. takeoff\n5. land"))
    
    if(command==1): # get gps
        try:
            print(master.recv_match(type='GPS_RAW_INT', blocking=True).to_dict(), "\n\n")
        except:
            print("get GPS data failed")
            pass
        
    elif(command==2): # arm
        # Arm
        # master.arducopter_arm() or:
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            1, 0, 0, 0, 0, 0, 0)

        # wait until arming confirmed (can manually check with master.motors_armed())
        print("Waiting for the vehicle to arm")
        master.motors_armed_wait()
        print('Armed!\n\n')

    elif(command==3): # disarm
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0)

    elif(command==4): # takeoff
        master.mav.command_long_send(
            master.target_system, master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 5, 0, 0, 0, 37.5479590, 127.1197123, 10
        )
        time.sleep(15)

    elif(command==5): # land
        master.mav.command_long_send(
            master.target_system, master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 37.62608777661077, 127.08914052989549, 33
        )
        time.sleep(30)

        # wait until disarming confirmed
        print("Waiting for the vehicle to disarm")
        master.motors_disarmed_wait()
        print('Disarmed!\n\n')
