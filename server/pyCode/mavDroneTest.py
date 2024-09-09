import time
from pymavlink import mavutil

def main():
    # 연결 설정 (UDP 연결 예시)
    print("start")
    connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')

    # Heartbeat 수신 대기 (드론과의 연결 확인)
    print("Connecting to the drone...")
    connection.wait_heartbeat(timeout=30)
    
    if connection.target_system and connection.target_component:
        print("-- Connected to drone!")
    else:
        print("Failed to connect to the drone.")
        return

    print("Waiting for drone to have a global position estimate...")
    msg = connection.recv_match(type='GPS_RAW_INT', blocking=True)
    if msg:
        gps_status = msg  
        if gps_status.fix_type >= 2:  # 2 = 2D fix, 3 = 3D fix
            print("-- Global position state is good enough for flying.")
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                default_alt = msg.alt / 1000.0
        else:
            print("Waiting for GPS data...")

    # ARMING
    print("-- 3s 소요 Arming")
    connection.arducopter_arm()
    time.sleep(3)

    # 이륙
    def takeoff(altitude):
        print("-- 10s 소요: Taking off")
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, altitude
        )

        while True:
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                current_altitude = msg.relative_alt / 1000.0
                if current_altitude >= altitude * 0.95:
                    break

    takeoff(10)
    time.sleep(3)

    # 착륙
    def land():
        print("-- 10s 소요: Landing")
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, default_alt
        )

        while True:
            msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
            if msg:
                current_altitude = msg.relative_alt / 1000.0
                if current_altitude <= default_alt * 0.05:
                    break

    land()
    time.sleep(3)
    
    print("-- Disarm")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0
    )

if __name__ == "__main__":
    main()