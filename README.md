# BTHome-MicroPython
A MicroPython module to format sensor readings for BTHome BLE advertising payloads.

[![Build BTHome-MicroPython](https://github.com/DavesCodeMusings/BTHome-MicroPython/actions/workflows/build.yml/badge.svg?branch=main)](https://github.com/DavesCodeMusings/BTHome-MicroPython/actions/workflows/build.yml)

## What is it?
BTHome-MicroPython provides an easy way to send sensor readings from MicroPython-based microcontrollers, via Bluetooth Low Energy (BLE) advertisements, to home automation systems like Home Assistant that support the BTHome data format.

The sample main.py shows how to transmit mocked-up temperature and humidity data in BTHome format using this module.

## Why should I care?
While many popular Bluetooth devices can have their stock firmware flashed to use BTHome and therefore easily integrate with Home Assistant, this does not help the hobbyist who wants to create a DIY sensor using an easily learned language like MicroPython. With this module, you can create custom sensors that act as Bluetooth beacons. Where you take it from there is up to your imagination.

The use case I had in mind when creating this is an ESP32 that sits on my front porch and measures outdoor temperature, humidity, and sunlight levels. 

## Couldn't I just use ESPHome?
You could, but do you really want a device containing your WiFi credentials in an unsecured location outside your home? I don't. I'd rather broadcast BLE advertisements I can read from indoors. If the device sending them is lost or stolen, I'm out a few dollars, but no data is compromised.

## How can I use it?
Install this module and the aioble module to your microcontroller's /lib directory.

With mpremote's mip, it's like this:

```
mpremote connect PORT mip install github:DavesCodeMusings/BTHome-MicroPython
mpremote connect PORT mip install aioble-peripheral
```

Once you've got the modules installed, have a look at the code sample in [main.py](src/main.py) here in this repository.

Building your own sensor beacon boils down to this...
1. Import the bthome module.
2. Create a new instance of the BTHome class, passing in the device name you want.
3. Read the sensors and write their values to the BTHome properties you want to communicate.
4. Call the `pack_advertisement()` method with parameters to indicate what data to broadcast.
5. Send that advertising data to `aioble.advertise()`.

As MicroPython statements, those steps would be something like this:

```
from bthome import BTHome
beacon = BTHome("myBeacon")
beacon.temperature = dht.temperature()
beacon.humidity = dht.humidity()
advert = beacon.pack_advertisement(BTHome.TEMPERATURE_SINT16, BTHome.HUMIDITY_UINT16)
await aioble.advertise(BLE_ADV_INTERVAL_uS, adv_data=advert, connectable=False)
```

See [main.py](src/main.py) for a more robust example.

Values can also be set directly in the `pack_advertisement()` call by using a
tuple, useful for sending multiple values of the same type, for example a
device with two buttons could send the state like this:

```
advert = beacon.pack_advertisement(
  (BTHome.BUTTON_UINT8, BTHome.BUTTON_EVENT_NONE),
  (BTHome.BUTTON_UINT8, BTHome.BUTTON_EVENT_PRESS)
)
```

[Note](https://bthome.io/format/#:~:text=Multiple%20events%20of%20the%20same%20type)
that the state for all duplicated objects must always be sent and always in the
same order. Buttons and dimmer events have a `0` state to represent no change.

For buttons and dimmers it is advisable to set the trigger based device flag as
a hint to the receiver that the device might not be sending advertisements for
a long time:

```
beacon = BTHome("myBeacon", trigger_based=True)
```

## Will it run on Microcontroller X?
If the device has Bluetooth and can run recent versions of MicroPython, it should work.

## Can it do more than temperature and humidity?
My goal was to create an outdoor sensor to measure temperature, humidity, and illuminance so I could make automation decsions in Home Assistant. I've included nearly the entire list of object_ids described in the [BTHome v2 format](https://bthome.io/format), but those outside of temperature, humidity, and battery level are untested in real world scenarios.

## What about encryption?
Sorry. Although [BTHome offers encrypted communication](https://bthome.io/encryption/), the [MicroPython AES encryption](https://docs.micropython.org/en/latest/library/cryptolib.html) implementation does not support the CCM mode required for BTHome encryption.

## What other caveats should I be aware of?
The number of bytes reserved for BLE advertising is extremely limited. You get 31 bytes. That's it. And you have to subtract things like advertising flags, service UUID, and length bytes from that total. So in the end you get 17 bytes to split between device name and sensor data.

Because of this, device name is silently truncted to 10 characters in length. If you try naming your device _MySuperSensor_, you will end up with _MySuperSen_ instead.

If you try to pack too much sensor data, you'll get an exception. For example, using all 10 characters for a device name like _DIY-Sensor_ and communiating BATTERY_UINT8_X1, TEMPERATURE_SINT16_X100, HUMIDITY_UINT16_X100, and PRESSURE_UINT24_X100 will be enough to exceed the allowable advertising payload size and result in an exception. 

```
ValueError: BLE advertisement exceeds max length
```

If this happens, use the debugging output to determine the length of your advertising payload. You may be able to shorten the device name or limit the number of object IDs you're communicating to make it fit. 

## How can I help?
Test, test, test! I'm always happy to get bug reports in the [GitHub issues for the project](https://github.com/DavesCodeMusings/BTHome-MicroPython/issues). The more detail you give, the easier it is to find and fix.

As for enhancements, unless the BTHome format undergoes significant changes (like a v3 release) I can't imagine there's much to add.
