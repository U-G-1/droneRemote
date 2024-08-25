#------------------------------------------------------------------------------
#   드론 이동 테스트
#   위로 10m, 앞으로 10m
#   작동 종료의 두번째 경우 -> 성공
#------------------------------------------------------------------------------

import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
    
async def get_xy(drone):
    async for position in drone.telemetry.position():
        return position.latitude_deg, position.longitude_deg
    
async def get_z(drone):
    async for home in drone.telemetry.home():
        return home.absolute_altitude_m
    
def printArgs(n1,n2,n3):
    print(n1)
    print(n2)
    print(n3)

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    async for state in drone.core.connection_state():
        if state.is_connected:
            flag = True
            break

    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            flag = True
            break

    await drone.action.arm()
    
    await drone.action.takeoff()
    await asyncio.sleep(10)

    #await wait_until_altitude_reached(drone, target_altitude=1.0)
    #await asyncio.sleep(5)

    current_x, current_y = await get_xy(drone)
    current_z = await get_z(drone)
    
    # 드론을 특정 글로벌 좌표로 이동
    
    t_z = current_z + 15.0
    
    await drone.action.goto_location(current_x, current_y, t_z, 0)
    await asyncio.sleep(15)
    
    """await wait_until_reached_global_position(drone, current_x, current_y, current_z)
    await asyncio.sleep(5)"""

    current_x, current_y = await get_xy(drone)
    current_z = await get_z(drone)

    printArgs(current_x, current_y, current_z)

    await drone.action.land()
    await asyncio.sleep(15)

    await drone.action.disarm()

async def wait_until_altitude_reached(drone, target_altitude, tolerance=0.5):
    async for home in drone.telemetry.home():
        current_alt = home.absolute_altitude_m
        alt_diff = abs(current_alt - target_altitude)

        if alt_diff <= tolerance:
            break

        await asyncio.sleep(1)  # 1초마다 고도 확인

async def wait_until_reached_global_position(drone, target_lat, target_lon, target_alt, tolerance=0.5):
    """
    드론이 목표 위치에 도달할 때까지 대기하는 함수
    """
    print("Waiting for the drone to reach the target position...")
    async for position in drone.telemetry.position():
        current_lat = position.latitude_deg
        current_lon = position.longitude_deg

    async for home in drone.telemetry.home():
        current_alt = home.absolute_altitude_m

        lat_diff = abs(current_lat - target_lat)
        lon_diff = abs(current_lon - target_lon)
        alt_diff = abs(current_alt - target_alt)

        if lat_diff <= tolerance and lon_diff <= tolerance and alt_diff <= tolerance:
            break

        await asyncio.sleep(0.5)  # 1초마다 위치 확인
        
if __name__ == "__main__":
    # Run the asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())