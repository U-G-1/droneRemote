#!/usr/bin/env python3

import asyncio

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def run():

    drone = System()
    #await drone.connect(system_address="udp://:14540") #시뮬레이션 용 연결 코드
    await drone.connect(system_address="serial///dev/ttyUSB0:921600") #드론용 연결 코드

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
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