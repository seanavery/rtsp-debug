# `rtsp-debug` sensor component

This service is design to find corrupted video and images produced by the [viamrtsp](https://github.com/viam-modules/viamrtsp) module.

To run, you first need to add [blurry-classifier](https://github.com/viam-modules/blurry-classifier) service to your robot.

## Attributes

``` json
{
    "camera": "<camera_component_name>",
    "vision": "<vision_service_name>"
}
```
