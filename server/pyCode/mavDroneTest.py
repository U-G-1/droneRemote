
import time
from pymavlink import mavutil

print("1. start")
def main():
    # 연결 설정 (UDP 연결 예시)
    print("start")
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
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            default_alt = msg.alt / 1000.0
        else:
            print("Waiting for GPS data...")


     # ARMING
    print("-- 3s 소요 Arming")
    connection.arducopter_arm()
    """connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 1)"""
    time.sleep(3)

    # 이륙
    def takeoff(altitude):
        print("-- 10s 소요: Taking off")
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 10, 0, 0, 0, 0, 0, altitude
        )

        while True:
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            current_altitude = msg.relative_alt / 1000.0
            if current_altitude >= altitude * 0.95:
                break

    takeoff(10)
    time.sleep(3)

    # 점으로 이동
    # 목표 좌표로 이동
def goto_position_target_global_int(lat, lon, alt):
    connection.mav.set_position_target_global_int_send(
        0, connection.target_system, connection.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, 0b0000111111111000,
        int(lat), int(lon), alt, 0, 0, 0, 0, 0, 0, 0, 0
    )

goto_position_target_global_int(37.7749 * 1e7, -122.4194 * 1e7, 20)



    # 착륙
    def land():
        print("-- 10s 소요: Landing")
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, default_alt
        )

        while True:
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            current_altitude = msg.relative_alt / 1000.0
            if current_altitude >= default_alt * 0.95:
                break

    land()
    time.sleep(3)
    
    print("-- Disarm")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0
    )

    if __name__ == "__main__":
        print("start in main")
        main()