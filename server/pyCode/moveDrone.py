"""
드론 이륙 테스트
무장 -> 절대좌표 추정 -> 시동 -> 좌표값받아오기 -> 착륙 -> 무장해제
"""

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

async def wait_until_landed(drone):
    async for in_air in drone.telemetry.in_air():
        if not in_air:
            print("-- Landing complete")
            break
        await asyncio.sleep(0.5) 
        
def printArgs(n1,n2,n3):
    print(n1)
    print(n2)
    print(n3)

async def run():
    drone = System()
    #await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="serial///dev/ttyUSB0:921600") #드론용 연결 코드

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

    print("-- 3s 소요 Arming")
    await drone.action.arm()
    await asyncio.sleep(3)

    print("-- 15s 소요: Taking off")
    await drone.action.takeoff()
    await asyncio.sleep(15)

    variables = {}
    
    try:
        """if len(sys.argv) < 4 * 3 + 1:
            print("인자가 부족합니다. 12개의 좌표 인자가 필요합니다.")
            return"""

        for i in range(4):
            float_x = float(sys.argv[i*3+1])
            float_y = float(sys.argv[i*3+2])
            float_z = float(sys.argv[i*3+3])
            variables[f"float_x_{i+1}"] = float_x
            variables[f"float_y_{i+1}"] = float_y
            variables[f"float_z_{i+1}"] = float_z

            print(f" 받아온 값 float(sys.argv[{i*3+1}]): {float_x}, float_x_{i+1}: {variables[f'float_x_{i+1}']}")
            print(f" 받아온 값 float(sys.argv[{i*3+2}]): {float_y}, float_y_{i+1}: {variables[f'float_y_{i+1}']}")
            print(f" 받아온 값 float(sys.argv[{i*3+3}]): {float_z}, float_z_{i+1}: {variables[f'float_z_{i+1}']}")
    except ValueError:
        print("올바른 숫자 형식이 아닙니다.")
        return

    for i in range(1, 5):
        print(f"-- 30s 소요 Moving to waypoint {i}")
        print(f"서버로부터 받은 좌표 / {variables[f'float_x_{i}']}, {variables[f'float_y_{i}']}, {variables[f'float_z_{i}']}")
        await drone.action.goto_location(variables[f"float_x_{i}"], variables[f"float_y_{i}"], variables[f"float_z_{i}"], 0)
        await asyncio.sleep(30)

    print("-- 30s 소요 Landing")
    await drone.action.land()
    await asyncio.sleep(30)
    
    await wait_until_landed(drone)
    
    print("-- Disarming the drone")  #추가
    await drone.action.disarm()

    print("Drone is disarmed and the script is done.")
     
if __name__ == "__main__":
    # Run the asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())