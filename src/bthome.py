# BTHome MicroPython
# Construct Bluetooth Low Energy (BLE) advertising payloads for BTHome v2.
# See https://bthome.io for more about how BTHome communicates data.
# See https://github.com/DavesCodeMusings/BTHome-MicroPython for more about this module.
# Other interesting references are given as footnotes (e.g. [^1])

from micropython import const
from struct import pack


class BTHome:
    # Bluetooth Low Energy flags
    _ADVERT_FLAGS = bytes.fromhex(
        "020106"
    )  # length (02), flags indicator (01), flag bits (06) [^1]
    _SERVICE_DATA_UUID16 = 0x16
    _SERVICE_UUID16 = 0xFCD2  # 16-bit UUID reserved for BTHome. [^2]

    # BTHome specific flags
    _DEVICE_INFO_FLAGS = (
        0x40  # Currently hardcoded as: no encryption, regular updates, version 2
    )

    # Advertising size limit
    _ADVERT_PAYLOAD_MAX_BYTES = 31  # [^3]

    debug = False

    # Device name used in BLE advertisements.
    _local_name = ""

    # For most sensors defined below, the naming convention is:
    #   <const_name> ::= <property> "_" <data-type> "_x" <inverse of factor>
    # Example, temperature sint16 0.01 becomes:
    #   TEMPERATURE_SINT16_x100
    # Some properties have no factor, because it doesn't make sense for what's
    # being communicated. Examples: packet id, button press, firmware version.
    # The naming convention for these is simply:
    #   <const_name> ::= <property> "_" <data-type>
    # Binary sensors also have no factor and are alway represented as an
    # 8-bit unsigned integer.
    # For binary sensors (0x15 .. 0x2D), the naming convention is:
    #   <const_name> ::= <property> "_" BINARY
    # Example, "battery charging" becomes:
    #   BATTERY_CHARGING_BINARY
    #
    # See also: "Sensor Data" table at https://bthome.io/format/
    PACKET_ID_UINT8 = const(0x00)
    BATTERY_UINT8_X1 = const(0x01)  # %
    TEMPERATURE_SINT16_X100 = const(0x02)  # °C
    HUMIDITY_UINT16_X100 = const(0x03)  # %
    PRESSURE_UINT24_X100 = const(0x04)  # hPa
    ILLUMINANCE_UINT24_X100 = const(0x05)  # lux
    MASS_KG_UINT16_X100 = const(0x06)  # kg
    MASS_LB_UINT16_X100 = const(0x07)  # lb
    DEWPOINT_SINT16_X100 = const(0x08)  # °C
    COUNT_UINT8_X1 = const(0x09)
    ENERGY_UINT24_X1000 = const(0x0A)  # kWh
    POWER_UINT24_X100 = const(0x0B)  # W
    VOLTAGE_UINT16_X1000 = const(0x0C)  # V
    PM2_5_UINT16_X1 = const(0x0D)  # ug/m^3
    PM10_UINT16_X1 = const(0x0E)  # ug/m^3
    GENERIC_BOOLEAN = const(0x0F)  # 0 (False = Off) 1 (True = On)
    POWER_BINARY = const(0x10)  # 0 (False = Off) 1 (True = On)
    OPENING_BINARY = const(0x11)  # 0 (False = Closed) 1 (True = Open)
    CO2_UINT16_X1 = const(0x12)  # ppm
    TVOC_UINT16_X1 = const(0x13)  # ug/m^3
    MOISTURE_UINT16_X100 = const(0x14)  # %
    BATTERY_LOW_BINARY = const(0x15)  # 0 (False = Normal) 1 (True = Low)
    BATTERY_CHARGING_BINARY = const(0x16)  # 0 (False = Not Charging) 1 (True = Charging)
    CARBON_MONOXIDE_BINARY = const(0x17)  # 0 (False = Not detected) 1 (True = Detected)
    COLD_BINARY = const(0x18)  # 0 (False = Normal) 1 (True = Cold)
    CONNECTIVITY_BINARY = const(0x19)  # 0 (False = Disconnected) 1 (True = Connected)
    DOOR_BINARY = const(0x1A)  # 0 (False = Closed) 1 (True = Open)
    GARAGE_DOOR_BINARY = const(0x1B)  # 0 (False = Closed) 1 (True = Open)
    GAS_BINARY = const(0x1C)  # 0 (False = Clear) 1 (True = Detected)
    HEAT_BINARY = const(0x1D)  # 0 (False = Normal) 1 (True = Hot)
    LIGHT_BINARY = const(0x1E)  # 0 (False = No light) 1 (True = Light detected)
    LOCK_BINARY = const(0x1F)  # 0 (False = Locked) 1 (True = Unlocked)
    MOISTURE_BINARY = const(0x20)  # 0 (False = Dry) 1 (True = Wet)
    MOTION_BINARY = const(0x21)  # 0 (False = Clear) 1 (True = Detected)
    MOVING_BINARY = const(0x22)  # 0 (False = Not moving) 1 (True = Moving)
    OCCUPANCY_BINARY = const(0x23)  # 0 (False = Clear) 1 (True = Detected)
    PLUG_BINARY = const(0x24)  # 0 (False = Unplugged) 1 (True = Plugged in)
    PRESENCE_BINARY = const(0x25)  # 0 (False = Away) 1 (True = Home)
    PROBLEM_BINARY = const(0x26)  # 0 (False = OK) 1 (True = Problem)
    RUNNING_BINARY = const(0x27)  # 0 (False = Not Running) 1 (True = Running)
    SAFETY_BINARY = const(0x28)  # 0 (False = Unsafe) 1 (True = Safe)
    SMOKE_BINARY = const(0x29)  # 0 (False = Clear) 1 (True = Detected)
    SOUND_BINARY = const(0x2A)  # 0 (False = Clear) 1 (True = Detected)
    TAMPER_BINARY = const(0x2B)  # 0 (False = Off) 1 (True = On)
    VIBRATION_BINARY = const(0x2C)  # 0 (False = Clear) 1 (True = Detected)
    WINDOW_BINARY = const(0x2D)  # 0 (False = Closed) 1 (True = Open)
    HUMIDITY_UINT8_X1 = const(0x2E)  # %
    MOISTURE_UINT8_X1 = const(0x2F)  # %
    BUTTON_UINT8 = const(0x3A)  # 01 = press, 02 = long press, etc.
    DIMMER_UINT16 = const(0x03A)  # 01xx = rotate left xx steps, 02xx = rotate right xx steps
    COUNT_UINT16_X1 = const(0x3D)
    COUNT_UINT32_X1 = const(0x3E)
    ROTATION_SINT16_X10 = const(0x3F)  # °
    DISTANCE_MM_UINT16_X1 = const(0x40)  # mm
    DISTANCE_M_UINT16_X10 = const(0x41)  # m
    DURATION_UINT24_X1000 = const(0x42)  # s
    CURRENT_UINT16_X1000 = const(0x43)  # A
    SPEED_UINT16_X100 = const(0x44)  # m/s
    TEMPERATURE_SINT16_X10 = const(0x45)  # °C
    UV_INDEX_UINT8_X10 = const(0x46)
    VOLUME_L_UINT16_X10 = const(0x47)  # L
    VOLUME_ML_UINT16_X1 = const(0x48)  # mL
    VOLUME_FLOW_RATE_X1000 = const(0x49)  # m^3/hr
    VOLTAGE_UINT16_X10 = const(0x4A)  # V
    GAS_UINT24_X1000 = const(0x4B)  # m^3
    GAS_UINT32_X1000 = const(0x4C)  # m^3
    ENERGY_UINT32_X1000 = const(0x4D)  # kWh
    VOLUME_UINT32_X1000 = const(0x4E)  # L
    WATER_UINT32_X1000 = const(0x4F)  # L
    TIMESTAMP_UINT48_X1 = const(0x50)  # s
    ACCELERATION_UINT16_X1000 = const(0x51)  # m/s^2
    GYROSCOPE_UINT16_X1000 = const(0x52)  # °/s
    TEXT_BYTES = const(0x53)
    RAW_BYTES = const(0x54)
    VOLUME_STORAGE_UINT32_X1000 = const(0x55)  # L
    CONDUCTIVITY_UINT16_X1 = const(0x56)  # µS/cm
    TEMPERATURE_SINT8_X1 = const(0x57)  # °C
    # Skipping temperature 0x58 due to strange factor of 0.35
    COUNT_SINT8_X1 = const(0x59)
    COUNT_SINT16_X1 = const(0x5A)
    COUNT_SINT32_X1 = const(0x5B)
    POWER_SINT16_X100 = const(0x5C)  # W
    CURRENT_SINT16_X1000 = const(0x5D)  # A
    DIRECTION_UINT16_X100 = const(0x5E)  # °
    PRECIPITATION_UINT16_X1 = const(0x5F)  # mm
    CHANNEL_UINT8_X1 = const(0x60)

    # There is more than one way to represent most sensor properties. This
    # dictionary maps the object id to the property name.
    _object_id_properties = {
        PACKET_ID_UINT8: "packet_id",  # 0x00
        BATTERY_UINT8_X1: "battery",  # 0x01
        TEMPERATURE_SINT16_X100: "temperature",  # 0x02
        HUMIDITY_UINT16_X100: "humidity",  # 0x03
        PRESSURE_UINT24_X100: "pressure",  # 0x04
        ILLUMINANCE_UINT24_X100: "illuminance",  # 0x05
        MASS_KG_UINT16_X100: "mass",  # 0x06
        MASS_LB_UINT16_X100: "mass",  # 0x07
        DEWPOINT_SINT16_X100: "dewpoint",  # 0x08
        COUNT_UINT8_X1: "count",  # 0x09
        ENERGY_UINT24_X1000: "energy",  # 0x0A
        POWER_UINT24_X100: "power",  # 0x0B
        VOLTAGE_UINT16_X1000: "voltage",  # 0x0C
        PM2_5_UINT16_X1: "pm2.5",  # 0x0D
        PM10_UINT16_X1: "pm10",  # 0x0E
        GENERIC_BOOLEAN: "generic_boolean",  # 0x0F
        POWER_BINARY: "power_on",  # 0x10
        OPENING_BINARY: "opening",  # 0x11
        CO2_UINT16_X1: "co2",  # 0x12
        TVOC_UINT16_X1: "tvoc",  # 0x13
        MOISTURE_UINT16_X100: "moisture",  # 0x14
        BATTERY_LOW_BINARY: "battery_low",  # 0x15
        BATTERY_CHARGING_BINARY: "battery_charging",  # 0x16
        CARBON_MONOXIDE_BINARY: "carbon_monoxide",  # 0x17
        COLD_BINARY: "cold",  # 0x18
        CONNECTIVITY_BINARY: "connectivity",  # 0x19
        DOOR_BINARY: "door",  # 0x1A
        GARAGE_DOOR_BINARY: "garage_door",  # 0x1B
        GAS_BINARY: "gas_detected",  # 0x1C
        HEAT_BINARY: "heat",  # 0x1D
        LIGHT_BINARY: "light",  # 0x1E
        LOCK_BINARY: "lock",  # 0x1F
        MOISTURE_BINARY: "moisture_detected",  # 0x20
        MOTION_BINARY: "motion",  # 0x21
        MOVING_BINARY: "moving",  # 0x22
        OCCUPANCY_BINARY: "occupancy",  # 0x23
        PLUG_BINARY: "plug",  # 0x24
        PRESENCE_BINARY: "presence",  # 0x25
        PROBLEM_BINARY: "problem",  # 0x26
        RUNNING_BINARY: "running",  # 0x27
        SAFETY_BINARY: "safety",  # 0x28
        SMOKE_BINARY: "smoke",  # 0x29
        SOUND_BINARY: "sound",  # 0x2A
        TAMPER_BINARY: "tamper",  # 0x2B
        VIBRATION_BINARY: "vibration",  # 0x2C
        WINDOW_BINARY: "window",  # 0x2D
        HUMIDITY_UINT8_X1: "humidity",  # 0x2E
        MOISTURE_UINT8_X1: "moisture",  # 0x2F
        BUTTON_UINT8: "button",  # 0x3A
        DIMMER_UINT16: "dimmer",  # 0x3C
        COUNT_UINT16_X1: "count",  # 0x3D
        COUNT_UINT32_X1: "count",  # 0x3E
        ROTATION_SINT16_X10: "rotation",  # 0x3F
        DISTANCE_MM_UINT16_X1: "distance",  # 0x40
        DISTANCE_M_UINT16_X10: "distance",  # 0x41
        DURATION_UINT24_X1000: "duration",  # 0x42
        CURRENT_UINT16_X1000: "current",  # 0x43
        SPEED_UINT16_X100: "speed",  # 0x44
        TEMPERATURE_SINT16_X10: "temperature",  # 0x45
        UV_INDEX_UINT8_X10: "uv_index",  # 0x46
        VOLUME_L_UINT16_X10: "volume",  # 0x47
        VOLUME_ML_UINT16_X1: "volume",  # 0x48
        VOLUME_FLOW_RATE_X1000: "volume_flow_rate", # 0x49
        VOLTAGE_UINT16_X10: "voltage",  # 0x4A
        GAS_UINT24_X1000: "gas",  # 0x4B
        GAS_UINT32_X1000: "gas",  # 0x4C
        ENERGY_UINT32_X1000: "energy",  # 0x4D
        VOLUME_UINT32_X1000: "volume",  # 0x4E
        WATER_UINT32_X1000: "water",  # 0x4F
        TIMESTAMP_UINT48_X1: "timestamp",  # 0x50
        ACCELERATION_UINT16_X1000: "acceleration",  # 0x51
        GYROSCOPE_UINT16_X1000: "gyroscope",  # 0x52
        TEXT_BYTES: "text",  # 0x53
        RAW_BYTES: "raw",  # 0x54
        VOLUME_STORAGE_UINT32_X1000: "volume_storage",  # 0x55
        CONDUCTIVITY_UINT16_X1: "conductivity",  # 0x56
        TEMPERATURE_SINT8_X1: "temperature",  # 0x57
        # Skipping 0x58 temperature due to strange factor of 0.35
        COUNT_SINT8_X1: "count",  # 0x59
        COUNT_SINT16_X1: "count",  # 0x5A
        COUNT_SINT32_X1: "count",  # 0x5B
        POWER_SINT16_X100: "power",  # 0x5C
        CURRENT_SINT16_X1000: "current",  # 0x5D
        DIRECTION_UINT16_X100: "direction",  # 0x5E
        PRECIPITATION_UINT16_X1: "precipitation",  # 0x5F
        CHANNEL_UINT8_X1: "channel"  # 0x60
    }

    # Properties below are updated externally when sensor values are read.
    # See "Sensor Data" table at https://bthome.io/format/ Property column.
    # There is some overlap in property names in the BTHome format. For
    # example: moisture as in percent and moisture as in detected.
    # In these cases, the binary property will have the description of a
    # True condition to further describe the property. Examples are:
    # _charging, in the case of battery; _detected, in the case of gas,
    #  moisture, or motion.
    acceleration = 0
    battery = 0
    battery_low = False
    battery_charging = False
    carbon_monoxide = False
    channel = 0
    co2 = 0
    cold = False
    conductivity = 0
    connectivity = False
    count = 0
    current = 0
    dewpoint = 0
    direction = 0
    distance = 0
    door = False
    duration = 0
    energy = 0
    garage_door = False
    gas = 0
    gas_detected = False
    generic_boolean = False
    gyroscope = 0
    heat = False
    humidity = 0
    illuminance = 0
    light = False
    lock = False
    mass = 0
    moisture = 0
    moisture_detected = False
    motion = False
    moving = False
    opening = False
    plug = False
    presence = False
    pm10 = 0
    pm2_5 = 0
    power = 0
    power_on = False
    precipitation = 0
    pressure = 0
    problem = False
    raw = bytes()
    rotation = 0
    running = False
    safety = False
    speed = 0
    smoke = False
    sound = False
    tamper = False
    temperature = 0
    text = ""
    timestamp = 0
    tvoc = 0
    uv_index = 0
    vibration = False
    voltage = 0
    volume = 0
    volume_flow_rate = 0
    volume_storage = 0
    water = 0
    window = False

    def __init__(self, local_name="BTHome", debug=False):
        local_name = local_name[:10]  # Truncate to fit [^4]
        self._local_name = local_name
        self.debug = debug

    @property
    def local_name(self):
        return self._local_name

    @property
    def packet_id(self):
        self._packet_id += 1
        self._packet_id &= 0xFF  # Truncate to 8-bit max
        return self._packet_id

    # Technically, the functions below could be static methods, but @staticmethod
    # on a dictionary of functions only works with Python >3.10, and MicroPython
    # is based on 3.4. Also, __func__ and __get()__ workarounds throw errors in
    # MicroPython. [^5]

    # Binary flag (true/false, on/off)
    def _pack_binary(self, object_id, value):
        return pack("BB", object_id, 1 if (value is True) else 0)

    # 8-bit integer with scaling of 1 (no decimal places)
    def _pack_int8_x1(self, object_id, value):
        return pack("BB", object_id, round(value))

    # 8-bit integer with scaling of 10 (1 decimal place)
    def _pack_int8_x10(self, object_id, value):
        return pack("BB", object_id, round(value * 10))

    # 16-bit integer with scalling of 1 (no decimal places)
    def _pack_int16_x1(self, object_id, value):
        return pack("<BH", object_id, round(value))

    # 16-bit integer with scalling of 10 (1 decimal place)
    def _pack_int16_x10(self, object_id, value):
        return pack("<BH", object_id, round(value * 10))

    # 16-bit integer with scalling of 100 (2 decimal places)
    def _pack_int16_x100(self, object_id, value):
        return pack("<BH", object_id, round(value * 100))

    # 16-bit integer with scalling of 1000 (3 decimal places)
    def _pack_int16_x1000(self, object_id, value):
        return pack("<BH", object_id, round(value * 1000))

    # 24-bit integer with scaling of 100 (2 decimal places)
    def _pack_int24_x100(self, object_id, value):
        return pack("<BL", object_id, round(value * 100))[:-1]

    # 24-bit integer with scaling of 1000 (3 decimal places)
    def _pack_int24_x1000(self, object_id, value):
        return pack("<BL", object_id, round(value * 1000))[:-1]

    # 32-bit integer with scaling of 1 (no decimal places)
    def _pack_int32_x1(self, object_id, value):
        return pack("<BL", object_id, round(value))

    # 32-bit integer with scaling of 1000 (3 decimal places)
    def _pack_int32_x1000(self, object_id, value):
        return pack("<BL", object_id, round(value * 1000))

    # 48-bit integer with scaling of 1 (no decimal places)
    def _pack_int48_x1(self, object_id, value):
        return pack("<BQ", object_id, value)[:-2]

    def _pack_raw_text(self, object_id, value):
        packed_value = pack("B", object_id) + value.encode()
        packed_value = bytes([len(packed_value)]) + packed_value
        return packed_value

    _object_id_functions = {
        PACKET_ID_UINT8: _pack_int8_x1,  # 0x00
        BATTERY_UINT8_X1: _pack_int8_x1,  # 0x01
        TEMPERATURE_SINT16_X100: _pack_int16_x100,  # 0x02
        HUMIDITY_UINT16_X100: _pack_int16_x100,  # 0x03
        PRESSURE_UINT24_X100: _pack_int24_x100,  # 0x04
        ILLUMINANCE_UINT24_X100: _pack_int24_x100,  # 0x05
        MASS_KG_UINT16_X100: _pack_int16_x100,  # 0x06
        MASS_LB_UINT16_X100: _pack_int16_x100,  # 0x07
        DEWPOINT_SINT16_X100: _pack_int16_x100,  # 0x08
        COUNT_UINT8_X1: _pack_int8_x1,  # 0x09
        ENERGY_UINT24_X1000: _pack_int24_x1000,  # 0x0A
        POWER_UINT24_X100: _pack_int24_x100,  # 0x0B
        VOLTAGE_UINT16_X1000: _pack_int16_x1000,  # 0x0C
        PM2_5_UINT16_X1: _pack_int16_x1,  # 0x0D
        PM10_UINT16_X1: _pack_int16_x1,  # 0x0E
        GENERIC_BOOLEAN: _pack_binary,  # 0x0F
        POWER_BINARY: _pack_binary,  # 0x10
        OPENING_BINARY: _pack_binary,  # 0x11
        CO2_UINT16_X1: _pack_int16_x1,  # 0x12
        TVOC_UINT16_X1: _pack_int16_x1,
        MOISTURE_UINT16_X100: _pack_int16_x100,
        BATTERY_LOW_BINARY: _pack_binary,
        BATTERY_CHARGING_BINARY: _pack_binary,
        CARBON_MONOXIDE_BINARY: _pack_binary,
        COLD_BINARY: _pack_binary,
        CONNECTIVITY_BINARY: _pack_binary,
        DOOR_BINARY: _pack_binary,
        GARAGE_DOOR_BINARY: _pack_binary,
        GAS_BINARY: _pack_binary,
        HEAT_BINARY: _pack_binary,
        LIGHT_BINARY: _pack_binary,
        LOCK_BINARY: _pack_binary,
        MOISTURE_BINARY: _pack_binary,
        MOTION_BINARY: _pack_binary,
        MOVING_BINARY: _pack_binary,
        OCCUPANCY_BINARY: _pack_binary,
        PLUG_BINARY: _pack_binary,
        PRESENCE_BINARY: _pack_binary,
        PROBLEM_BINARY: _pack_binary,
        RUNNING_BINARY: _pack_binary,
        SAFETY_BINARY: _pack_binary,
        SMOKE_BINARY: _pack_binary,
        SOUND_BINARY: _pack_binary,
        TAMPER_BINARY: _pack_binary,
        VIBRATION_BINARY: _pack_binary,
        WINDOW_BINARY: _pack_binary,
        HUMIDITY_UINT8_X1: _pack_int8_x1,
        MOISTURE_UINT8_X1: _pack_int8_x1,
        BUTTON_UINT8: _pack_int8_x1,
        DIMMER_UINT16: _pack_int16_x1,
        COUNT_UINT16_X1: _pack_int16_x1,
        COUNT_UINT32_X1: _pack_int32_x1,
        ROTATION_SINT16_X10: _pack_int16_x10,
        DISTANCE_MM_UINT16_X1: _pack_int16_x1,
        DISTANCE_M_UINT16_X10: _pack_int16_x10,
        DURATION_UINT24_X1000: _pack_int24_x1000,
        CURRENT_UINT16_X1000: _pack_int16_x1000,
        SPEED_UINT16_X100: _pack_int16_x100,
        TEMPERATURE_SINT16_X10: _pack_int16_x10,
        UV_INDEX_UINT8_X10: _pack_int8_x10,
        VOLUME_L_UINT16_X10: _pack_int16_x10,
        VOLUME_ML_UINT16_X1: _pack_int16_x1,
        VOLUME_FLOW_RATE_X1000: _pack_int16_x1000,
        VOLTAGE_UINT16_X10: _pack_int16_x10,
        GAS_UINT24_X1000: _pack_int24_x1000,
        GAS_UINT32_X1000: _pack_int32_x1000,
        ENERGY_UINT32_X1000: _pack_int32_x1000,
        VOLUME_UINT32_X1000: _pack_int32_x1000,
        WATER_UINT32_X1000: _pack_int32_x1000,
        TIMESTAMP_UINT48_X1: _pack_int48_x1,
        ACCELERATION_UINT16_X1000: _pack_int16_x1000,
        GYROSCOPE_UINT16_X1000: _pack_int16_x1000,
        TEXT_BYTES: _pack_raw_text,
        RAW_BYTES: _pack_raw_text,
        VOLUME_STORAGE_UINT32_X1000: _pack_int32_x1000,
        CONDUCTIVITY_UINT16_X1: _pack_int16_x1,
        TEMPERATURE_SINT8_X1: _pack_int8_x1,
        COUNT_SINT8_X1: _pack_int8_x1,
        COUNT_SINT16_X1: _pack_int16_x1,
        COUNT_SINT32_X1: _pack_int32_x1,
        POWER_SINT16_X100: _pack_int16_x100,
        CURRENT_SINT16_X1000: _pack_int16_x1000,
        DIRECTION_UINT16_X100: _pack_int16_x100,
        PRECIPITATION_UINT16_X1: _pack_int16_x1,
        CHANNEL_UINT8_X1: _pack_int8_x1
    }

    # Concatenate an arbitrary number of sensor readings using parameters
    # of sensor data constants to indicate what's to be included.
    def pack_service_data(self, *args):
        service_data_bytes = pack("<H", BTHome._SERVICE_UUID16)
        service_data_bytes += pack("B", BTHome._DEVICE_INFO_FLAGS)
        for object_id in sorted(args):
            func = BTHome._object_id_functions[object_id]
            property = BTHome._object_id_properties[object_id]
            value = getattr(self, property)
            packed_representation = func(self, object_id, value)
            if self.debug:
                print("Using function:", func)
                print("Data property:", property)
                print("Data value:", value)
                print("Packed representation:", packed_representation.hex().upper())
            service_data_bytes += packed_representation
        return service_data_bytes

    def pack_advertisement(self, *args):
        service_data_bytes = self._pack_service_data(*args)
        advertisement_bytes = pack("B", BTHome._SERVICE_DATA_UUID16)  # indicates a 16-bit service UUID follows
        advertisement_bytes += self._ADVERT_FLAGS  # All BTHome adverts start this way.
        advertisement_bytes += self._pack_raw_text(0x09, self.local_name)  # 0x09 indicates complete name
        advertisement_bytes += pack("B", len(service_data_bytes)) + service_data_bytes
        if self.debug:
            print("BLE Advertisement:", advertisement_bytes.hex().upper())
            print("Advertisement Len:", len(advertisement_bytes))
        if len(advertisement_bytes) > BTHome._ADVERT_PAYLOAD_MAX_BYTES:
            raise ValueError("BLE advertisement exceeds max length")
        return advertisement_bytes


# This demo's values match what is used by the example at: https://bthome.io/format
# The advertisement printed here should match the example BTHome payload.
def demo():
    beacon = BTHome("DIY-sensor", debug=True)
    beacon.temperature = 25
    beacon.humidity = 50.55
    ble_advert = beacon.pack_advertisement(
        BTHome.TEMPERATURE_SINT16_X100, BTHome.HUMIDITY_UINT16_X100
    )
    return ble_advert


if __name__ == "__main__":
    demo()


# [^1]: https://community.silabs.com/s/article/kba-bt-0201-bluetooth-advertising-data-basics
# [^2]: https://bthome.io/images/License_Statement_-_BTHOME.pdf
# [^3]: https://github.com/orgs/micropython/discussions/12701
# [^4]: https://community.st.com/t5/stm32-mcus-wireless/ble-name-advertising/m-p/254711/highlight/true#M10645
# [^5]: https://stackoverflow.com/questions/41921255/staticmethod-object-is-not-callable
