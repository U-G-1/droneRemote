#------------------------------------------------------------------------------
#   드론 이동 테스트
#   위로 10m, 앞으로 10m
#   작동 종료의 두번째 경우 -> 성공
#------------------------------------------------------------------------------

import asyncio
import sys
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    """print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break"""

    print("-- Arming")
    await drone.action.arm()
    
    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed \
                with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return
    
    get_x = sys.argv[1]
    get_y = sys.argv[2]
    get_z = sys.argv[3]

    try:
        float_x = sys.argv[1]
        float_y = sys.argv[2]
        float_z = sys.argv[3]
    except ValueError:
        print("올바른 숫자 형식이 아닙니다.")

    print("-- Go 0m North, 0m East, -10m Down \
            within local coordinate system")
    await drone.offboard.set_position_ned(
            PositionNedYaw(float_x, float_y, float_z, 0.0))
    await asyncio.sleep(5)

    print("-- return home\
          #1 Set the original coordinate to 0 ") # 아예 좌표를 0으로 처리
    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(5)

    print("-- Landing")
    await drone.action.land()
    await asyncio.sleep(5)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed \
                with error code: {error._result.result}")
    
    await asyncio.sleep(10)
    print("-- Disarming the drone")  #추가
    await drone.action.disarm()

    print("Drone is disarmed and the script is done.")
        
if __name__ == "__main__":
    # Run the asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
