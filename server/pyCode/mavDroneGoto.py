
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

     # ARMING
    print("-- 3s 소요 Arming")
    connection.arducopter_arm()
    """connection.mav.command_long_send(
            connection.target_system, connection.target_component,
            mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM, 1)"""
    time.sleep(5)

    def set_guided_mode(master):
        # MAV_MODE_FLAG_CUSTOM_MODE_ENABLED = 1 << 7 플래그 사용
        custom_mode = mavutil.mavlink.MAV_MODE_GUIDED
        master.mav.set_mode_send(
            master.target_system,
            mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,  # Custom 모드 플래그
            custom_mode  # GUIDED 모드로 전환
        )
        # 응답 대기
        ack = master.recv_match(type='COMMAND_ACK', blocking=True)
        print(ack)
    
    set_guided_mode(connection)

    connection.mav.mission_item_send(
        connection.target_system,
        connection.target_component,
        0,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
        mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
        0, 0, 0, 0, 0, 0,
        37.54725695650923, 127.12157164094592, 20
    )

    # 명령 실행 후 대기
    connection.mav.command_long_send(
        connection.target_system,
        connection.target_component,
        mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED,
        0,
        1,    # 속도 유형 (1 = 속도, 0 = 속도 유지)
        5,    # 목표 속도 (m/s)
        -1,   # 속도 유지
        0, 0, 0, 0
    )

if __name__ == "__main__":
    main()