
import time
import threading
from pymavlink import mavutil

def send_heartbeat(master):
        while True:
            master.mav.heartbeat_send(
                mavutil.mavlink.MAV_TYPE_GCS,  # Ground Control Station 타입
                mavutil.mavlink.MAV_AUTOPILOT_INVALID, 
                0, 0, 4)
            time.sleep(1)  # 1초마다 heartbeat 전송

def main():
    # 연결 설정 (UDP 연결 예시)
    connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')
    #connection = mavutil.mavlink_connection('serial///dev/ttyUSB0:921600')

   # Heartbeat 수신 대기 (드론과의 연결 확인)
    print("Connecting to the drone...")
    connection.wait_heartbeat(20)
    if connection.target_system and connection.target_component:
        print("-- Connected to drone!")
    else:
        print("Failed to connect to the drone.")

     # Heartbeat 쓰레드 실행
    heartbeat_thread = threading.Thread(target=send_heartbeat, args=(connection,))
    heartbeat_thread.daemon = True  # 메인 프로그램 종료 시 쓰레드도 종료되도록 설정
    heartbeat_thread.start()

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

    time.sleep(5)

    # set_mode("Stabilize")
    def set_mode(mode):
        mode_mapping = connection.mode_mapping()  # 모드 매핑을 가져옵니다
        if mode in mode_mapping:
            mode_id = mode_mapping[mode]  # 모드 ID를 가져옵니다
            connection.mav.set_mode_send(
                connection.target_system,  # 드론의 시스템 ID
                mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,  # 사용자 정의 모드 플래그
                mode_id  # 사용자 정의 모드 ID
            )
            print(f"Mode set to {mode}.")
        else:
            print(f"Mode {mode} is not available.")

    # 'Stabilize' 모드로 변경
    set_mode('Stabilize')

     # ARMING
    print("-- 3s 소요 Arming")
    connection.arducopter_arm()
    """connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 1)"""
    time.sleep(5)

    # 이륙
    def takeoff(altitude):
        print("-- 10s 소요: Taking off")
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 5, 0, 0, 0, 37.5479590, 127.1197123, altitude
        )
        time.sleep(5)

    takeoff(10)
    time.sleep(5)

    
    # 점으로 이동
    def goto(lat, lon, alt):
        print("goto 시작")
        connection.mav.set_position_target_global_int_send(
        0,  # 시간 (timestamp) - 일반적으로 0으로 설정
        connection.target_system,  # 시스템 ID
        connection.target_component,  # 컴포넌트 ID
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT,  # 프레임 타입
        0b0000111111110000,  # 속성 플래그 (위치만 설정)
        int(lat * 1e7),  # lat_int: int32_t, 목표 위도 (단위: 1e-7 degrees)
        int(lon * 1e7),  # lon_int: int32_t, 목표 경도 (단위: 1e-7 degrees)
        int(alt * 1000), 
        0, 0, 0,  # 속도 (vx, vy, vz) - 이동 속도 설정 안 함
        0, 0, 0,  # 가속도 (ax, ay, az) - 가속도 설정 안 함
        0, 0  # yaw, yaw rate - 회전 관련 설정 안 함 
        )
        time.sleep(15)
    

    goto(37.54759682966823, 127.11961450028555, 20)
    
    # 착륙
    def land():
        print("-- 10s 소요: Landing")
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_LAND, 0, 0, 0, 0, 0, 37.5479590, 127.1197123, 7
        )

    land()
    time.sleep(5)
    
    print("-- Disarm")
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,0,0,0,0,0,0,0,0
    )

if __name__ == "__main__":
    main()