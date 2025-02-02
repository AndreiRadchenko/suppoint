# class GPIOSensor(SensorEntity):
#     def __init__(self, name, gpio_pin):
#         self._name = name
#         self._gpio_pin = gpio_pin
#         self._state = None
#         self._stop_event = threading.Event()
#         self._chip = Chip(GPIO_CHIP)

#         # Configure line settings with edge detection and pull-up bias
#         line_settings = LineSettings(
#             edge_detection=Edge.BOTH,
#             direction=Direction.INPUT
#             bias=Bias.PULL_UP,
#             debounce_period=timedelta(milliseconds=50),
#         )

#         # Request the line for event monitoring
#         self._lines = self._chip.request_lines(
#             consumer=self._name,
#             config={self._gpio_pin: line_settings},
#         )

#         # Start thread to listen for events
#         self._thread = threading.Thread(target=self._listen_for_events)
#         self._thread.daemon = True
#         self._thread.start()

#     @property
#     def name(self):
#         return self._name

#     @property
#     def state(self):
#         return self._state

#     def _listen_for_events(self):
#         """Listen for GPIO edge events."""
#         while not self._stop_event.is_set():
#             try:
#                 events = self._lines.read_edge_events()
#                 for event in events:
#                     self._state = "off" if event.event_type == Edge.RISING else "on"
#                     _LOGGER.info(f"GPIO Sensor {self._gpio_pin} state changed to {self._state}")
#                     self.schedule_update_ha_state()
#             except Exception as e:
#                 _LOGGER.error(f"Error reading GPIO pin {self._gpio_pin}: {e}")

#     def update(self):
#         """No-op as events update the state."""
#         pass

#     def __del__(self):
#         """Ensure cleanup on object deletion."""
#         self._stop_event.set()
#         self._thread.join()
#         self._lines.release()


import logging
from datetime import timedelta
from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.event import async_track_time_interval
from gpiod import Chip, LineSettings
from gpiod.line import Direction, Value, Bias

_LOGGER = logging.getLogger(__name__)

GPIO_PINS = [4, 3, 7, 13, 14, 10]
GPIO_CHIP = "/dev/gpiochip2"
UPDATE_INTERVAL = timedelta(seconds=1)  # Update every 1 second

class GPIOSensor(SensorEntity):
    def __init__(self, hass, name, gpio_pin):
        self._name = name
        self._gpio_pin = gpio_pin
        self._state = None

        # Open GPIO chip and request line as input
        self._chip = Chip(GPIO_CHIP)
        line_settings = LineSettings(bias=Bias.PULL_UP, direction=Direction.INPUT)
        self._lines = self._chip.request_lines(
            consumer=self._name,
            config={self._gpio_pin: line_settings},
        )

        # Schedule periodic updates
        async_track_time_interval(hass, self.async_update_state, UPDATE_INTERVAL)

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    async def async_update_state(self, _):
        try:
            # Read the GPIO value (0 or 1)
            value = self._lines.get_value(self._gpio_pin)
            self._state = "open" if value == Value.ACTIVE else "close"
            _LOGGER.info(f"GPIO Sensor {self._gpio_pin} updated to {self._state}")
            self.async_write_ha_state()
        except Exception as e:
            _LOGGER.error(f"Error reading GPIO pin {self._gpio_pin}: {e}")

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    sensors = []
    num = 1  # Initialize outside the loop
    for pin in GPIO_PINS:
        sensors.append(GPIOSensor(hass, f"GPIO Sensor {num}", pin))  # Provide hass argument
        num += 1  # Increment for each sensor
    async_add_entities(sensors)
