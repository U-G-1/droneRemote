#------------------------------------------------------------------------------
#   드론 이동 테스트
#   위로 10m, 앞으로 10m
#   작동 종료의 두번째 경우 -> 성공
#------------------------------------------------------------------------------

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def get_position_ned(drone):
    async for position_velocity_ned in drone.telemetry.position_velocity_ned():
        position = position_velocity_ned.position
        return position.north_m, position.east_m, position.down_m

def printArgs(n1,n2,n3):
    print(n1)
    print(n2)
    print(n3)

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            flaat = True        
            break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            flag = True
            break

    await drone.action.arm()

    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    try:
        await drone.offboard.start()
    except OffboardError as error:
        await drone.action.disarm()
        return

    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0 -1.0, 0.0))
    await asyncio.sleep(5)

    current_x, current_y, current_z = await get_position_ned(drone)

    await printArgs(current_x, current_y, current_z)

    await drone.action.land()
    await asyncio.sleep(10)

    await drone.action.disarm()

if __name__ == "__main__":
    # Run the asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
