# actuators.py

import asyncio


async def vibrate_all(self, strength, time):
    for device in self.client.devices.values():
        for actuator in device.actuators:
            await actuator.command(strength)
        await asyncio.sleep(time)
        for actuator in device.actuators:
            await actuator.command(0)


async def vibrate_one(device, strength, time):
    for actuator in device.actuators:
        await actuator.command(strength)
    await asyncio.sleep(time)
    for actuator in device.actuators:
        await actuator.command(0)


async def linear_actuators(self, strength, time):
    for device in self.client.devices.values():
        for linear_actuator in device.linear_actuators:
            await linear_actuator.command(time * 1000, strength)


async def rotatory_actuators(self, strength, time):
    for device in self.client.devices.values():
        for rotatory_actuator in device.rotatory_actuators:
            await rotatory_actuator.command(strength, True)
            await asyncio.sleep(time)
            await rotatory_actuator.command(0, True)
