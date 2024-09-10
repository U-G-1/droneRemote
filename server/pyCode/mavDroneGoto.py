
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

def get_drone_mode(connection):
    # HEARTBEAT 메시지 수신 대기
    print("Waiting for a heartbeat to check the mode...")
    heartbeat = connection.recv_match(type='HEARTBEAT', blocking=True)
    
    # 현재 모드 가져오기
    custom_mode = heartbeat.custom_mode
    base_mode = heartbeat.base_mode

    # 모드 맵핑 가져오기
    mode_mapping = connection.mode_mapping()
    
    # 현재 모드 탐색
    current_mode = None
    for mode_name, mode_id in mode_mapping.items():
        if mode_id == custom_mode:
            current_mode = mode_name
            break
    
    # 현재 모드 출력
    if current_mode:
        print(f"Current drone mode: {current_mode}")
    else:
        print("Unable to determine the current drone mode.")


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
        time.sleep(10)

    takeoff(10)
    time.sleep(5)

    def setmode():
        connection.mav.set_mode_send(
        connection.target_system,   # uint8_t (시스템 ID): 비행 모드를 설정할 시스템의 ID
        connection.MAV_MODE_GUIDED_ARMED,            # uint32_t (모드): 비행 모드 (비트 플래그 형식으로 설정)
        0      # uint32_t (커스텀 모드): 특정 커스텀 모드 (일반적으로 사용하지 않음)
    )
        
    #setmode()

    def set_guided_mode():
    # 모드를 GUIDED로 변경
        connection.set_mode_loiter()

    set_guided_mode()
    time.sleep(5)

    get_drone_mode(connection)
    time.sleep(5)
    
    # 점으로 이동
    def goto(lat, lon, alt):
        print("goto 시작")
       
        connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_NAV_WAYPOINT, 0, 5, 0, 0, 0, int(lat * 1e7), int(lon * 1e7),  alt
        )
        time.sleep(15)
 
    goto(37.54725695650923, 127.12157164094592, 20)
    
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