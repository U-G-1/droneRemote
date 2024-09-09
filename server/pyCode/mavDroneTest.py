import time
from pymavlink import mavutil

def main():
    # 연결 설정 (UDP 연결 예시)
    connection = mavutil.mavlink_connection('udp:127.0.0.1:14540')
    #connection = mavutil.mavlink_connection('serial:///dev/ttyUSB0:921600')

    # Heartbeat 수신 대기 (드론과의 연결 확인)
    print("Connecting to the drone...")
    connection.wait_heartbeat(10)
    if connection.target_system and connection.target_component:
        print("-- Connected to drone!")
    else:
        print("Failed to connect to the drone.")
        return

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
            return

    # ARMING
    print("-- 3s 소요 Arming")
    connection.arducopter_arm()
    time.sleep(3)

    # 이륙 함수 정의
    def takeoff(altitude):
        print("-- 10s 소요: Taking off")
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, 0, altitude
        )

    # 착륙 함수 정의
    def land():
        print("-- 10s 소요: Landing")
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 0, 0, 0
        )

    takeoff(10)  # 10m 고도로 이륙
    time.sleep(10)  # 충분한 시간 대기

    land()  # 착륙 명령
    time.sleep(10)

    # Disarm
    print("-- Disarm")
    connection.mav.command_long_send(
        connection.target_system, connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 0, 0, 0, 0, 0, 0, 0
    )

if __name__ == "__main__":
    main()
