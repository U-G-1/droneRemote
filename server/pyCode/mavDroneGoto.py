from pymavlink import mavutil

# MAVProxy 드론 연결
master = mavutil.mavlink_connection('tcp:127.0.0.1:5750')

# 연결 후 heartbeat 확인 (연결 확인)
master.wait_heartbeat()

# GUIDED 모드로 전환
master.set_mode_auto()

# 드론 무장 (arming)
master.arducopter_arm()

# 특정 위치로 이동 (위도, 경도, 고도)
latitude = 37.54725695650923
longitude = 127.12157164094592
altitude = 20

master.mav.mission_item_send(
    master.target_system,
    master.target_component,
    0,
    mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT,
    mavutil.mavlink.MAV_CMD_NAV_WAYPOINT,
    0, 0, 0, 0, 0, 0,
    latitude, longitude, altitude
)

# 명령 실행 후 대기
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_DO_CHANGE_SPEED,
    0,
    1,    # 속도 유형 (1 = 속도, 0 = 속도 유지)
    5,    # 목표 속도 (m/s)
    -1,   # 속도 유지
    0, 0, 0, 0
)