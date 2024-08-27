#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540") #시뮬레이션 용 연결 코드
    #await drone.connect(system_address="serial///dev/ttyUSB0:921600") 드론용 연결 코드

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break
            
    #서버에서 이거 없애는 거 확인 필요
    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break
    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break        

    print("-- Arming")
    await drone.action.arm()

    await asyncio.sleep(5)
    
    print("-- Disarming the drone")
    await drone.action.disarm()

    print("Drone is disarmed and the script is done.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())