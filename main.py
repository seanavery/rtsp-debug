#!/usr/bin/env python3
from typing import Mapping
from viam.proto.common import ResourceName
from typing_extensions import Self
import asyncio
from viam.components.sensor import Sensor
from viam.proto.app.robot import ModuleConfig
from viam.module.types import Reconfigurable
from viam.resource.base import ResourceBase
from viam.module.module import Module
from viam.resource.registry import Registry, ResourceCreatorRegistration

class MySensor(Sensor, Reconfigurable):
    MODEL = "seanavery:rtsp-debug:sensor"
    
    @classmethod
    def new(cls, config: ModuleConfig, dependencies: Mapping[ResourceName, ResourceBase]) -> Self:
        print("Creating a new instance of MySensor with config:", config)
        my_class = cls(config.name)
        my_class.reconfigure(config, dependencies)
        return my_class
    
    def reconfigure(self, config: ModuleConfig, dependencies: Mapping[ResourceName, ResourceBase]):
        return
    @classmethod
    def validate(cls, config: ModuleConfig) -> tuple[list[str], list[str]]:
        return [], []

    async def get_readings(self, **kwargs):
        return {"ok": True}
    
async def main():
    Registry.register_resource_creator(Sensor.API, MySensor.MODEL, ResourceCreatorRegistration(MySensor.new, MySensor.validate))
    module = Module.from_args()
    module.add_model_from_registry(Sensor.API, MySensor.MODEL)
    await module.start()

if __name__ == '__main__':
    asyncio.run(main())
    
