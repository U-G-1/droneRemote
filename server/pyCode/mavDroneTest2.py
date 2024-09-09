import time
from pymavlink import mavutil

# 드론과 연결 설정 (MAVLink)
connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')

# Heartbeat 수신 대기 (드론과의 연결 확인)
connection.wait_heartbeat()
print("Heartbeat received from system (system %u component %u)" % (connection.target_system, connection.target_component))

# 드론 상태 확인 함수
def check_drone_status():
    """ 드론 상태 확인 """
    print("\nChecking drone status...\n")
    
    # 배터리 상태 확인
    if 'SYS_STATUS' in connection.messages:
        battery_status = connection.messages['SYS_STATUS']
        print(f"Battery Voltage: {battery_status.voltage_battery / 1000.0}V")
        print(f"Battery Current: {battery_status.current_battery / 100.0}A")
        print(f"Battery Remaining: {battery_status.battery_remaining}%")
    else:
        print("No battery data available.")

    # GPS 상태 확인
    if 'GPS_RAW_INT' in connection.messages:
        gps_status = connection.messages['GPS_RAW_INT']
        print(f"GPS Fix Type: {gps_status.fix_type}")
        print(f"Latitude: {gps_status.lat / 1e7}")
        print(f"Longitude: {gps_status.lon / 1e7}")
        print(f"Altitude: {gps_status.alt / 1000.0}m")
        print(f"Satellites Visible: {gps_status.satellites_visible}")
    else:
        print("No GPS data available.")

    # 자세(Attitude) 상태 확인
    if 'ATTITUDE' in connection.messages:
        attitude_status = connection.messages['ATTITUDE']
        print(f"Roll: {attitude_status.roll} radians")
        print(f"Pitch: {attitude_status.pitch} radians")
        print(f"Yaw: {attitude_status.yaw} radians")
    else:
        print("No attitude data available.")

# 주기적으로 드론 상태 확인 (5초마다 확인)
while True:
    check_drone_status()
    time.sleep(5)
