
from pymavlink import mavutil

# 연결 설정 (UDP 연결 예시)
connection = mavutil.mavlink_connection('udp:127.0.0.1:14540')
connection.wait_heartbeat()

# 모드 설정
def set_mode(mode):
    mode_id = connection.mode_mapping()[mode]
    connection.mav.set_mode_send(connection.target_system, mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED, mode_id)

set_mode("GUIDED")
# def set_mode(mode):
#     if mode in connection.mode_mapping():
#         mode_id = connection.mode_mapping()[mode]
#         connection.mav.set_mode_send(
#             connection.target_system,
#             mavutil.mavlink.MAV_MODE_FLAG_CUSTOM_MODE_ENABLED,
#             mode_id
#         )
#     else:
#         print(f"Mode {mode} is not available.")

# 'OFFBOARD' 모드로 변경
set_mode('OFFBOARD')


# 이륙
def arm_and_takeoff(altitude):
    connection.arducopter_arm()
    connection.mav.command_long_send(
        connection.target_system, connection.target_component,
        mavutil.mavlink.MAV_CMD_NAV_TAKEOFF, 0, 0, 0, 0, 0, 0, altitude
    )

    while True:
        msg = connection.recv_match(type='GLOBAL_POSITION_INT', blocking=True)
        current_altitude = msg.relative_alt / 1000.0
        if current_altitude >= altitude * 0.95:
            break

arm_and_takeoff(10)

# 목표 좌표로 이동
def goto_position_target_global_int(lat, lon, alt):
    connection.mav.set_position_target_global_int_send(
        0, connection.target_system, connection.target_component,
        mavutil.mavlink.MAV_FRAME_GLOBAL_RELATIVE_ALT_INT, 0b0000111111111000,
        int(lat), int(lon), alt, 0, 0, 0, 0, 0, 0, 0, 0
    )

goto_position_target_global_int(37.7749 * 1e7, -122.4194 * 1e7, 20)

# 착륙
land()