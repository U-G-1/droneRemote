import time
from MAVProxy.modules.lib import mp_module
from MAVProxy.modules.lib import mp_util
from MAVProxy.modules.lib.mp_settings import MPSetting

# MAVProxy module class
class DroneStatusModule(mp_module.MPModule):
    def __init__(self, mpstate):
        """ Initialize module """
        super(DroneStatusModule, self).__init__(mpstate, "drone_status", "Check drone status")

        # 상태 정보 확인 주기 (5초마다 확인)
        self.add_command('checkstatus', self.cmd_checkstatus, "Check the drone's status")

    def cmd_checkstatus(self, args):
        """ 드론 상태 확인 """
        print("\nChecking drone status...\n")
        
        # 배터리 상태 출력
        battery_status = self.master.messages['SYS_STATUS']
        print(f"Battery Voltage: {battery_status.voltage_battery / 1000.0}V")
        print(f"Battery Current: {battery_status.current_battery / 100.0}A")
        print(f"Battery Remaining: {battery_status.battery_remaining}%")
        
        # GPS 상태 출력
        if 'GPS_RAW_INT' in self.master.messages:
            gps_status = self.master.messages['GPS_RAW_INT']
            print(f"GPS Fix Type: {gps_status.fix_type}")
            print(f"Latitude: {gps_status.lat / 1e7}")
            print(f"Longitude: {gps_status.lon / 1e7}")
            print(f"Altitude: {gps_status.alt / 1000.0}m")
            print(f"Satellites Visible: {gps_status.satellites_visible}")
        else:
            print("No GPS data available.")
        
        # 자세(Attitude) 상태 출력
        attitude_status = self.master.messages['ATTITUDE']
        print(f"Roll: {attitude_status.roll} radians")
        print(f"Pitch: {attitude_status.pitch} radians")
        print(f"Yaw: {attitude_status.yaw} radians")

# Module setup
def init(mpstate):
    """ 모듈 초기화 함수 """
    return DroneStatusModule(mpstate)