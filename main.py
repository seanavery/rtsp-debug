#!/usr/bin/env python3
from typing import Mapping, Dict, Any
from viam.proto.common import ResourceName
from viam.utils import ValueTypes, struct_to_dict
from typing_extensions import Self
import asyncio
from viam.components.sensor import Sensor
from viam.proto.app.robot import ModuleConfig
from viam.module.types import Reconfigurable
from viam.resource.base import ResourceBase
from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration
from viam.services.vision import VisionClient

class MySensor(Sensor, Reconfigurable):
    MODEL = "seanavery:rtsp-debug:sensor"
    
    @classmethod
    def new(cls, config: ModuleConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        print("Creating a new instance of MySensor with config:", config)
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        asyncio.create_task(my_class.poll_img())
        return my_class
    
    def reconfigure(self, config: ModuleConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        attributes = struct_to_dict(config.attributes)
        if "vision" not in attributes:
            raise ValueError("MySensor requires a 'vision' attribute in the configuration.")
        if "camera" not in attributes:
            raise ValueError("MySensor requires a 'camera' attribute in the configuration.")
        self.camera_name = attributes["camera"]
        self.vc = dependencies[VisionClient.get_resource_name(attributes["vision"])]

    @classmethod
    def validate(cls, config: ModuleConfig) -> tuple[list[str], list[str]]:
        return [], []

    async def get_readings(self, **kwargs):
        return {"ok": True}
    
    async def poll_img(self):
        while True:
            print("Polling image from camera:", self.camera_name)
            try:
                result = await self.vc.capture_all_from_camera(
                    camera_name=self.camera_name,
                    return_image=True,
                    return_classifications=True,
                    return_detections=False,
                    return_object_point_clouds=False,
                    extra=None,
                    timeout=5.0
                )
                print("Capture result:", result)
            except Exception as e:
                print("Error during capture_all_from_camera:", e)
            await asyncio.sleep(1)
    
async def main():
    Registry.register_resource_creator(Sensor.API, MySensor.MODEL, ResourceCreatorRegistration(MySensor.new, MySensor.validate))
    module = Module.from_args()
    module.add_model_from_registry(Sensor.API, MySensor.MODEL)
    await module.start()

if __name__ == '__main__':
    asyncio.run(main())
    
