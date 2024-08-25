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
    
    try:
        # sys.argv로부터 값을 받아와서 float으로 변환
        float_x = float(sys.argv[1])
        float_y = float(sys.argv[2])
        float_z = float(sys.argv[3])
    except ValueError:
        print("올바른 숫자 형식이 아닙니다.")
    
    print("-- Go 0m North, 0m East, -1m Down \
            within local coordinate system")
    await drone.offboard.set_position_ned(
            PositionNedYaw(float_x, float_y, float_z, 0.0))
    await asyncio.sleep(5)

    print("-- Landing")
    await drone.action.land()
    await asyncio.sleep(10)
    
    print("-- Disarming the drone")  #추가
    await drone.action.disarm()

    print("Drone is disarmed and the script is done.")
        
if __name__ == "__main__":
    # Run the asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
