# BTHome-MicroPython
A MicroPython module to format sensor readings for BTHome BLE advertising payloads.

## What is it?
BTHome-MicroPython provides an easy way to send sensor readings, via Bluetooth Low Energy (BLE) advertisements, to home automation systems like Home Assistant. The sample main.py shows how to collect temperature and humidity data and make it available to Home Assistant with the BTHome integration.

The use case I had in mind when creating this is an ESP32 that sits on my front porch and measures outdoor temperature, humidity, and sunlight levels. 

## Why should I care?
While many popular Bluetooth devices can have their stock firmware flashed to use BTHome and therefore easily integrate with Home Assistant, this does not help the hobbyist who wants to create a DIY sensor using an easily learned language like MicroPython. With this module, you can create custom sensors that act as Bluetooth beacons. Where you take it from there is up to your imagination.

## Couldn't I just use ESPHome?
You could, but do you really want a device containing your WiFi credentials in an unsecured location outside your home? I don't. I'd rather broadcast BLE advertisements I can read from indoors. If the device sending them is lost or stolen, I'm out a few dollars, but no data is compromised.

## How can I use it?
Copy bthome.py (or bthome.mpy) to your microcontroller's /lib directory and install MicroPython's aioble module (specifically the peripheral portion, but you can also install the entire module.)

With mip, it's like this:

```
mpremote connect PORT mip install github:DavesCodeMusings/BTHome-MicroPython
mpremote connect PORT mip install aioble-peripheral
```

Once you've got the modules installed, have a look at the code sample in [main.py](main.py) here in this repository.

Building your own sensor beacon boils down to this...
1. Import the bthome module
2. Set the device name you want
3. Write the sensor readings to the bthome variables you're using
4. Call bthome.pack_advertisement() with parameters to indicate which data to broadcast
5. Send that advertising data to `aioble.advertise()`

As MicroPython statements, those steps are:

```
import bthome
bthome.device_name = "myBeacon"
bthome.temperature = dht.temperature()
bthome.humidity = dht.humidity()
adv_data = bthome.pack_advertisement(bthome.TEMPERATURE_SINT16, bthome.HUMIDITY_UINT16)
```

See [main.py](main.py) for a more robust example.

## Will it run on Microcontroller X?
If the device has Bluetooth and can run recent versions of MicroPython, it should work. You may need to adjust a few things in the example main.py. It uses some ESP32 specific stuff in parts of the debugging output.

## Can it do more than temperature and humidity?
My goal was to create an outdoor sensor to measure temperature, humidity, and illuminance so I could make automation decsions in Home Assistant. I've included barometric pressure and battery level in the initial release, but they are untested. If the need arises, I may add other data specified in the BTHome format. You are also free to fork the code and add your own.
