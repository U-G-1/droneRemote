#------------------------------------------------------------------------------
#   드론 이동 테스트
#   위로 10m, 앞으로 10m
#   작동 종료의 두번째 경우 -> 성공
#------------------------------------------------------------------------------

import asyncio
import sys
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)
    
async def get_xy(drone):
    async for position in drone.telemetry.position():
        return position.latitude_deg, position.longitude_deg
    
async def get_z(drone):
    async for home in drone.telemetry.home():
        return home.absolute_altitude_m
    
async def get_d_z(drone):
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
    await asyncio.sleep(3)

    print("-- Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(5)

    try:
        float_x = float(sys.argv[1])
        float_y = float(sys.argv[2])
        float_z = float(sys.argv[3])
    except ValueError:
        print("올바른 숫자 형식이 아닙니다.")

    print(f"  서버로부터 받은 좌표 / {float_x}, {float_y}, {float_z} )")
    
    await drone.action.goto_location(float_x, float_y, float_z, 0)
    await asyncio.sleep(10)

    print("-- Landing")
    await drone.action.land()
    await asyncio.sleep(10)

    print("-- Disarming the drone")  #추가
    await drone.action.disarm()

    print("Drone is disarmed and the script is done.")

async def wait_until_altitude_reached(drone, target_altitude, tolerance=0.5):
    """
    드론이 목표 고도에 도달할 때까지 대기하는 함수
    """
    print("Waiting for the drone to reach the target altitude...")
    async for position in drone.telemetry.position():
        current_alt = position.relative_altitude_m
        alt_diff = abs(current_alt - target_altitude)

        if alt_diff <= tolerance:
            print("Target altitude reached!")
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
            print("Target position reached!")
            break

        await asyncio.sleep(0.5)  # 1초마다 위치 확인
        
if __name__ == "__main__":
    # Run the asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())