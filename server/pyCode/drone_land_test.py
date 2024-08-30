"""
드론 이륙 테스트
"""

import asyncio
from mavsdk import System

async def run():

    print("Connected to the server.")

    drone = System()
    #await drone.connect(system_address="udp://:14540")
    await drone.connect(system_address="serial///dev/ttyUSB0:921600") #드론용 연결 코드

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"Drone discovered!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("Global position estimate ok")
            break

    print("-- Arming")
    await drone.action.arm()
    
    await asyncio.sleep(3)
    
    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(30)

    print("-- Landing")
    await drone.action.land()

    await asyncio.sleep(30)

    print("-- Disarming the drone")  #추가
    await drone.action.disarm()

    print("Drone is disarmed and the script is done.")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
