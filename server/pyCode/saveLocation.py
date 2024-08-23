#!/usr/bin/env python3

#------------------------------------------------------------------------------
#   서버 전송 테스트
#------------------------------------------------------------------------------

import asyncio
import time
from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

"""async def print_position(drone):
    async for position in drone.telemetry.position():
        print(f"    위도 - {position.latitude_deg} m, 경도 - {position.longitude_deg} m, 이륙 고도 - {position.relative_altitude_m}")"""

async def get_position(drone):
    async for position in drone.telemetry.position():
        return position

def printArgs(n1,n2,n3):
    print(n1)
    print(n2)
    print(n3)

x = ""
y = ""
z = ""

async def run():

    drone = System()
    #await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="serial///dev/ttyUSB0:921600")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break
    
    print("-- Arming")
    await drone.action.arm()
    await asyncio.sleep(3)

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

    print(" #1 위로 올라가서 좌표 출력")
    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0, -1.0, 0.0))
    
    await asyncio.sleep(5)

    position = await get_position(drone)
    x = position.latitude_deg
    y = position.longitude_deg
    z = position.relative_altitude_m

    print(f"  Position - {x} m, {y} m, {z} m")

    print("-- return home\
          #1 Set the original coordinate to 0 ") # 아예 좌표를 0으로 처리
    await drone.offboard.set_position_ned(
            PositionNedYaw(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(5)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed \
                with error code: {error._result.result}")
           
    print("-- Disarming the drone")
    await drone.action.disarm()

    print("Drone is disarmed and the script is done.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())

    printArgs(x,y,z)