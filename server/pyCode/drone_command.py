"""
Example of how to connect pymavlink to an autopilot via an UDP master
"""

# Disable "Bare exception" warning
# pylint: disable=W0702

import time
import sys
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
master = mavutil.mavlink_connection('udp:0.0.0.0:14550')

# Make sure the master is valid
master.wait_heartbeat()

# Get some information !
while True:
    command = int(input("enter menu\n1. get gps data\n2. arm\n3. takeoff\n4. land\n5. disarm\n\n11. get mode\n12.change mode\n\n20. move drone\n----------\n"))
    
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
        try:
            hb = master.recv_match(type='HEARTBEAT', blocking=True)
            print("base mode:", hb.base_mode,"\n")
            print("custom mode:", hb.custom_mode,"\n")
            print("mode:", mavutil.mode_string_v10(hb),"\n")
        except:
            print("get mode data failed")
            pass

    elif(command==3): # takeoff
        master.mav.command_long_send(
            master.target_system, master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 5, 0, 0, 0, 37.5479590, 127.1197123, 10
        )
        print('Takeoff!\n\n')
        try:
            hb = master.recv_match(type='HEARTBEAT', blocking=True)
            print("base mode:", hb.base_mode,"\n")
            print("custom mode:", hb.custom_mode,"\n")
            print("mode:", mavutil.mode_string_v10(hb),"\n")
        except:
            print("get mode data failed")
            pass
        # time.sleep(10)

    elif(command==4): # land
        master.mav.command_long_send(
            master.target_system, master.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 37.5479590, 127.1197123, 33
        )
        print('Land!\n\n')
        try:
            hb = master.recv_match(type='HEARTBEAT', blocking=True)
            print("base mode:", hb.base_mode,"\n")
            print("custom mode:", hb.custom_mode,"\n")
            print("mode:", mavutil.mode_string_v10(hb),"\n")
        except:
            print("get mode data failed")
            pass
        # time.sleep(10)

    elif(command==5): # disarm
        master.mav.command_long_send(
            master.target_system,
            master.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
            0,
            0, 0, 0, 0, 0, 0, 0)
        print('Disarmed!\n\n')
        try:
            hb = master.recv_match(type='HEARTBEAT', blocking=True)
            print("base mode:", hb.base_mode,"\n")
            print("custom mode:", hb.custom_mode,"\n")
            print("mode:", mavutil.mode_string_v10(hb),"\n")
        except:
            print("get mode data failed")
            pass

        # wait until disarming confirmed
        print("Waiting for the vehicle to disarm")
        master.motors_disarmed_wait()
        print('Disarmed!\n\n')

    elif(command==11): # get mode
        try:
            hb = master.recv_match(type='HEARTBEAT', blocking=True)
            print("base mode:", hb.base_mode,"\n")
            print("custom mode:", hb.custom_mode,"\n")
            print("mode:", mavutil.mode_string_v10(hb),"\n")
        except:
            print("get mode data failed")
            pass

    elif(command == 12):  # Change  mode
        """
        usable mode
        'MANUAL', 'STABILIZED', 'ACRO', 'RATTITUDE', 'ALTCTL', 'POSCTL', 'LOITER', 'MISSION', 'RTL', 'LAND', 'RTGS', 'FOLLOWME', 'OFFBOARD', 'TAKEOFF'
        """
        modes = ['MANUAL', 'STABILIZED', 'ACRO', 'RATTITUDE', 'ALTCTL', 'POSCTL', 'LOITER', 'MISSION', 'RTL', 'LAND', 'RTGS', 'FOLLOWME', 'OFFBOARD', 'TAKEOFF']
        mode_num = int(input("enter mode what you want\n1. 'MANUAL'\n2. 'STABILIZED'\n3. 'ACRO'\n4. 'RATTITUDE'\n5. 'ALTCTL'\n6. 'POSCTL'\n7. 'LOITER'\n8. 'MISSION'\n9. 'RTL'\n10. 'LAND'\n11. 'RTGS'\n12. 'FOLLOWME'\n13. 'OFFBOARD'\n14. 'TAKEOFF'\n"))
        if(mode_num>0 and mode_num<15):
            mode = modes[mode_num-1]
        else:
            print("invalid number entered. try again")
            break
        # 모드가 유효한지 확인
        if mode not in master.mode_mapping():
            print('Unknown mode: {}'.format(mode))
            print('Try:', list(master.mode_mapping().keys()))
            exit(1)

        # 모드 ID 가져오기 (튜플의 첫 번째 요소 사용)
        mode_id = master.mode_mapping()[mode]

        for _ in range(10):
            # 비행 모드 전환 명령 전송
            master.mav.command_long_send(
                master.target_system,  # target_system
                master.target_component,  # target_component
                mavutil.mavlink.MAV_CMD_DO_SET_MODE,  # Command to set mode
                0,  # Confirmation
                mode_id[0],  # base_mode
                mode_id[1],  # custom_mode (OFFBOARD mode ID)
                mode_id[2], 
                0, 0, 0, 0)  # Unused parameters

            
            print(f"Trying to switch to {mode} mode...")
            ack_msg = master.recv_match(type='COMMAND_ACK', blocking=True)
            ack_msg = ack_msg.to_dict()
            if ack_msg['command'] == mavutil.mavlink.MAV_CMD_DO_SET_MODE:
                if ack_msg['result'] == 0:  # Success
                    print("Mode changed successfully.")
                    break
                else:
                    print("Mode change failed, retrying...")
            time.sleep(1)  # 1초 대기 후 재시도
            
    elif(command==20): #move drone
        # GPS 좌표 설정 (목표 위도, 경도, 고도)
        # 37.5479590, 127.1197123
        target_lat = 37.5478690  # 위도 (10^-7 단위)
        target_lon = 127.1197123  # 경도 (10^-7 단위)
        target_alt = 10  # 고도 (미터, AMSL)

        # 비행 모드 전환 명령 전송
        master.mav.command_long_send(
            master.target_system,  # target_system
            master.target_component,  # target_component
            mavutil.mavlink.MAV_CMD_DO_REPOSITION,  # Command to set mode
            0, 0, 0, 0, 0, target_lat, target_lon, target_alt)  # Unused parameters