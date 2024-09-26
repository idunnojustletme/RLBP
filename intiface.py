# intiface.py

import asyncio
import logging
from logging import NullHandler
from typing import Any, Optional

from buttplug import Client, Device, ProtocolSpec, WebsocketConnector

from actuators import vibrate_all, vibrate_one
from load_config import load_config
from server import get_score_increase


class IntifaceManager:
    def __init__(self, gui: Any):
        self.gui: Any = gui
        self.client: Optional[Client] = None
        self.connector: Optional[WebsocketConnector] = None

        self.previous_score_increase = None

    async def config(self) -> None:
        self.config = load_config()
        self.intiface_ip = self.config["intiface_ip"]
        self.max_power = self.config["max_power"]
        self.max_time = self.config["max_time"]
        self.min_power = self.config["min_power"]
        self.min_time = self.config["min_time"]
        self.power_divider = self.config["power_divider"]
        self.time_divider = self.config["time_divider"]
        self.min_score = self.config["min_score"]

    async def create_client(self) -> None:
        self.client = Client(
            "RLBP",
            ProtocolSpec.v3,
        )

        self.connector = WebsocketConnector(
            self.intiface_ip,
            # Silence, default logger!
            logger=logging.getLogger().addHandler(NullHandler()),
        )
        try:
            await self.client.connect(self.connector)
        except Exception as e:
            print(f"{e}")
            self.gui.print("Unable to connect to Intiface")
            return
        self.gui.print("Connected to Intiface")

    async def disconnect(self) -> None:
        if self.client and self.client.connected:
            await self.client.disconnect()
            print("Disconnecting from Intiface")

    async def reconnect(self) -> None:
        if self.client:
            if not self.client.connected:
                self.gui.print("Attempting to connect to Intiface")
            else:
                await self.client.disconnect()
                self.gui.print("Disconnected from Intiface")

            try:
                await self.client.connect(self.connector)
                if self.client.connected:
                    self.gui.print("Connected to Intiface")
                else:
                    self.gui.print("Unable to connect to Intiface")
            except Exception as e:
                print(f"{e}")
                self.gui.print("Unable to connect to Intiface")

    async def test_all_devices(self):
        if self.client.connected:
            if self.client.devices:
                for device in self.client.devices.values():
                    await self.test_one_device(device)
            else:
                self.gui.print(
                    "No devices found, use Intiface to manage your devices"
                )
        else:
            self.gui.print("Not connected to Intiface")

    async def test_one_device(self, device: Device) -> None:
        time = 1
        power = 0.5

        self.gui.print(f"Testing {device.name}")
        if device.actuators:
            self.gui.print(
                f"{len(device.actuators)} generic actuator(s) found"
            )
            self.gui.print("Activating for 1 second at 50% power")
            self.gui.print(f"[{time = }] [{power = }]")
            asyncio.create_task(vibrate_one(device, power, time))
        elif device.linear_actuators:
            self.gui.print(
                f"{len(device.linear_actuators)} linear actuator(s) found, these are unsupported in RLBP"
            )
        elif device.rotatory_actuators:
            self.gui.print(
                f"{len(device.rotatory_actuators)} rotatory actuator(s) found, these are unsupported in RLBP"
            )
        else:
            self.gui.print(
                "No actuators found, somehow. Try reconnecting your device"
            )

    async def stop_vibrate(self):
        self.gui.print("Stopping current vibration")
        asyncio.create_task(vibrate_all(self, 0, 0))

    async def score_vibrate(self):
        self.gui.print("Starting Vibrations :3")
        while True:
            score_increase = get_score_increase()
            if (
                score_increase is not None
                and score_increase != self.previous_score_increase
                and score_increase >= self.min_score
            ):
                self.gui.print("\n")
                self.gui.print(f"Score increased by {score_increase}")
                power = score_increase / self.power_divider
                time = score_increase / self.time_divider
                power = max(self.min_power, min(self.max_power, power))
                time = max(self.min_time, min(self.max_time, time))
                if self.client.devices:
                    self.gui.print(
                        f"Activating at {power * 100:.0f}% for {time:.1f} seconds"
                    )
                    asyncio.create_task(vibrate_all(self, power, time))

            self.previous_score_increase = score_increase
            await asyncio.sleep(0.1)
