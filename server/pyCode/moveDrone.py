#!/usr/bin/env python3

import asyncio
import time
import sys

from mavsdk import System
from mavsdk.offboard import (OffboardError, PositionNedYaw)

async def get_current_position(drone):
    async for position in drone.telemetry.position():
        return position.latitude_deg, position.longitude_deg, position.relative_altitude_m

async def run():

    drone = System()
    await drone.connect(system_address="udp://:14540") #시뮬레이션 용 연결 코드
    #await drone.connect(system_address="serial///dev/ttyUSB0:921600") #드론용 연결 코드

    async for state in drone.core.connection_state():
        if state.is_connected:
            flag = True
            break

    try:
        # sys.argv로부터 값을 받아와서 float으로 변환
        float_x = float(sys.argv[1])
        float_y = float(sys.argv[2])
        float_z = float(sys.argv[3])
    except ValueError:
        print("올바른 숫자 형식이 아닙니다.")

    current_x, current_y, current_z = await get_current_position(drone)

    print(f"  직접 받아온 현재 GPS: ({current_x}, {current_y}, {current_z})")
    print(f"  서버로 받아온 현재 GPS: ({float_x}, {float_y}, {float_z})")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())