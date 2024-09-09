"""
    MAVPROXY로 GPS 출력 코드
"""

import time
import asyncio
from pymavlink import mavutil

def main():
    # 드론과 연결 설정 (MAVLink)
    connection = mavutil.mavlink_connection('udp:127.0.0.1:14540')
    #connection = mavutil.mavlink_connection('serial///dev/ttyUSB0:921600')

    # Heartbeat 수신 대기 (드론과의 연결 확인)
    print("Connecting to the drone...")
    connection.wait_heartbeat()
    if connection.target_system and connection.target_component:
        print("-- Connected to drone!")
    else:
        print("Failed to connect to the drone.")

    
    print("Waiting for drone to have a global position estimate...")

    msg = connection.recv_match(type='GPS_RAW_INT', blocking=True)
    if msg:
        gps_status = msg
                
        # 위도, 경도, 고도가 유효한지 확인
        if gps_status.fix_type >= 2:  # 2 = 2D fix, 3 = 3D fix
            print("-- Global position state is good enough for flying.")

            print(f"{gps_status.lat}, {gps_status.lon}, {gps_status.alt}")
                    
        else:
            print("Waiting for GPS data...")

# 주기적으로 드론 상태 확인 (5초마다 확인)
if __name__ == "__main__":
    main()
