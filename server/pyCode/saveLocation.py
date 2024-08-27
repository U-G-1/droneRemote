#------------------------------------------------------------------------------
#   드론 좌표 출력
#------------------------------------------------------------------------------

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
    
async def get_xy(drone):
    async for position in drone.telemetry.position():
        return position.latitude_deg, position.longitude_deg
    
async def get_z(drone):         # 드론 첫 위치의 절대 고도
    async for home in drone.telemetry.home():
        return home.absolute_altitude_m
    
async def get_d_z(drone):       # 드론 이동 후의 상대 고도
    async for position in drone.telemetry.position():
        return position.relative_altitude_m

async def calculate_absolute_altitude(drone):
    # Get the absolute altitude from home
    absolute_z = await get_z(drone)

     # Get the relative altitude
    relative_z = await get_d_z(drone)
    
    # Calculate the absolute altitude
    cal_z = absolute_z + relative_z
    return cal_z
    
def printArgs(n1,n2,n3):
    print(n1)
    print(n2)
    print(n3)

async def run():
    drone = System()
    # await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="serial///dev/ttyUSB0:921600") #드론용 연결 코드

    async for state in drone.core.connection_state():
        if state.is_connected:
            break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            break

    current_x, current_y = await get_xy(drone)
    current_total_z = await calculate_absolute_altitude(drone)

    printArgs(current_x, current_y, current_total_z)

    await drone.action.land()
    await asyncio.sleep(6)

    await drone.action.disarm()
      
if __name__ == "__main__":
    # Run the asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())