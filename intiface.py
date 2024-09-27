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
        config = load_config(self)
        self.min_vibe_strength = config["min_vibe_strength"]
        self.max_vibe_strength = config["max_vibe_strength"]
        self.min_vibe_time = config["min_vibe_time"]
        self.max_vibe_time = config["max_vibe_time"]
        self.vibe_strength_divider = config["vibe_strength_divider"]
        self.vibe_time_divider = config["vibe_time_divider"]
        self.min_vibe_score = config["min_vibe_score"]
        self.intiface_ip = config["intiface_ip"]

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
        strength = 0.5

        self.gui.print(f"Testing {device.name}")
        if device.actuators:
            self.gui.print(
                f"{len(device.actuators)} generic actuator(s) found"
            )
            self.gui.print("Activating for 1 second at 50% strength")
            self.gui.print(f"[{time = }] [{strength = }]")
            asyncio.create_task(vibrate_one(device, strength, time))
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
                and score_increase >= self.min_vibe_score
            ):
                self.gui.print("\n")
                self.gui.print(f"Score increased by {score_increase}")
                strength = score_increase / self.vibe_strength_divider
                time = score_increase / self.vibe_time_divider
                strength = max(
                    self.min_vibe_strength,
                    min(self.max_vibe_strength, strength),
                )
                time = max(self.min_vibe_time, min(self.max_vibe_time, time))
                if self.client.devices:
                    print(f"{strength / 100}")
                    self.gui.print(
                        f"Activating at {strength:.0f}% for {time:.1f} seconds"
                    )
                    # strength needs to be a float between 0.0 and 1.0
                    asyncio.create_task(
                        vibrate_all(self, strength / 100, time)
                    )

            self.previous_score_increase = score_increase
            await asyncio.sleep(0.1)
