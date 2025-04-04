# BTHome-MicroPython
A MicroPython module to format sensor readings for BTHome BLE advertising payloads.

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

Once you've got the modules installed, have a look at the code sample in [main.py](main.py) here in this repository.

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

See [main.py](main.py) for a more robust example.

## Will it run on Microcontroller X?
If the device has Bluetooth and can run recent versions of MicroPython, it should work.

## What about encryption?
Sorry. Although [BTHome offers encrypted communication](https://bthome.io/encryption/), the [MicroPython AES encryption](https://docs.micropython.org/en/latest/library/cryptolib.html) implementation does not support the CCM mode required for BTHome encryption.

## Can it do more than temperature and humidity?
My goal was to create an outdoor sensor to measure temperature, humidity, and illuminance so I could make automation decsions in Home Assistant. I've included nearly the entire list of object_ids described in the [BTHome v2 format](https://bthome.io/format), but those outside of temperature, humidity, and battery level are untested in real world scenarios.

## How can I help?
Test, test, test! I'm always happy to get bug reports in the [GitHub issues for the project](https://github.com/DavesCodeMusings/BTHome-MicroPython/issues). The more detail you give, the easier it is to find and fix.

As for enhancements, unless the BTHome format undergoes significant changes (like a v3 release) I can't imagine there's much to add.
