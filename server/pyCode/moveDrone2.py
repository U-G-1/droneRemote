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

def parse_coordinates(arguments):
    """
    서버로부터 받은 좌표를 파싱하여 x, y, z 값을 묶어서 반환
    arguments: sys.argv[1:]로 전달된 좌표값 리스트
    """
    coordinates = []
    for i in range(0, len(arguments), 3):
        x = float(arguments[i])
        y = float(arguments[i+1])
        z = float(arguments[i+2])
        coordinates.append((x, y, z))  # x, y, z를 한 묶음으로 저장
    return coordinates

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
    await drone.connect(system_address="udp://:14540")
    #connect(system_address="serial///dev/ttyUSB0:921600") #드론용 연결 코드

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

     # 서버로부터 좌표값 받기
    print("-- Parsing coordinates from server")
    arguments = sys.argv[1:]  # 서버로부터 전달받은 좌표값 리스트
    coordinates = parse_coordinates(arguments)

    # 좌표 이동
    print("-- Moving to specified coordinates")
    for x, y, z in coordinates:
         await drone.action.goto_location(x, y, z, 0)
         await asyncio.sleep(10)

    """for idx, (x, y, z) in enumerate(coordinates):
        try:
            print(f"-- Moving to Point {idx + 1}: x={x}, y={y}, z={z}")
            await drone.action.goto_location(x, y, z, 0)

            # 이동 완료 확인
            while True:
                async for position in drone.telemetry.position():
                    current_lat = position.latitude_deg
                    current_lon = position.longitude_deg
                    altitude = position.relative_altitude_m

                    # 목표 지점 근처에 도달했는지 확인 (임계값 설정)
                    if (
                        abs(current_lat - x) < 0.00005 and
                        abs(current_lon - y) < 0.00005 and
                        abs(altitude - z) < 1.0
                    ):
                        print(f"--- Reached Point {idx + 1}")
                        break

                # 다음 좌표로 이동
                await asyncio.sleep(1)

        except Exception as e:
            print(f"!!! Error at Point {idx + 1}: {e}")
            continue
"""
         
    await asyncio.sleep(10)

    print("-- 20s 소요 Landing")
    await drone.action.land()
    await asyncio.sleep(20)

    await wait_until_landed(drone)
    
    print("-- Disarming the drone")  #추가
    await drone.action.disarm()

    print("Drone is disarmed and the script is done.")
     
if __name__ == "__main__":
    # Run the asyncio loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())