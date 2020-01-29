# homeassistant-wavin
Home assistant integration for Wavin AHC9000 via USB RS485

## Installation/Setup

1. Download
2. Unzip
3. Move to custom_components folder in homeassistant configuration folder
4. Modify configuration.yaml

```
wavin:
  tty: /dev/ttyUSB0
  
thermostats: 
  - name: "kitchen"
    sensor_channel: 0
    room_channel: 0
  - name: "diningroom"
    sensor_channel: 1
    room_channel: 1
  - name: "tvroom"
    sensor_channel: 2
    room_channel: 2
  - name: "hall"
    sensor_channel: 3
    room_channel: 3
  - name: "bedroom"
    sensor_channel: 4
    room_channel: 4
```

5. Reboot

## Thanks to

My buddy Palle Ravn for creating the library communicating with the AHC9000
https://github.com/paller/wavin-controller

Munklinde for providing a screenshot and installation/configuration example
