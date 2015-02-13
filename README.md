## Install it

```
pip install Pi-Broadcast-Service
```


## GPIO basic broadcast service

The GPIO basic broadcast service (`pi_broadcast_service.GPIOBasicBroadcastService`) makes it easy to broadcast a message to RabbitMQ when pin events are detected.

### Configuring the GPIO basic broadcast service

A config file, written in [YAML](http://en.wikipedia.org/wiki/YAML), is used to define the initial pin setup. If a pin is not defined here it will not be used by **Pi-Broadcast-Service**. You can save this file anywhere since you will provide a path to it in your code. The following snippet shows an example configuration file:

```yaml
18:
  mode: IN
  event: RISING
  handler: broadcast
  bounce: 200
22:
  mode: IN
  event: FALLING
  handler: broadcast
  bounce: 200
24:
  mode: IN
  event: BOTH
  handler: broadcast
  bounce: 200
```

* Add a numbered element for each pin to enable
* `mode` - This service only uses pins defined as `IN`. (Required)
* `event` - The event you want to wait for on the pin. Accepted values are: `RISING`, `FALLING`, `BOTH`.
* `handler` - This is used in combination with an `event` to designate the function to call when that `event` happens. With `pi_broadcast_service.GPIOBasicBroadcastService` this value must be set to `broadcast`.
* `bounce` - This can be used when an `event` is defined to prevent multiple handler calls being fired accidentally. The value is the number of milliseconds to wait before detecting another `event`.

For more available options, like pull up/down resistors, see documentation for the [Pi-Pin-Manager configuration file](https://github.com/projectweekend/Pi-Pin-Manager#notes).

### Starting the basic GPIO service

This part runs on your Raspberry Pi. It initializes the desired GPIO pins, connects to RabbitMQ, waits for the defined pin events, and then sends out a message when an event happens. The message is sent to the RabbitMQ broker on an exchange named `gpio_broadcast`, with a routing key that matches the `device_key` value used to crteate the service instance.

```python
from pi_broadcast_service import GPIOBasicBroadcastService


# The RabbitMQ connection string
RABBIT_URL='some_actual_connection_string'

# A unique string you make up to identify a single Raspberry Pi
DEVICE_KEY='my_awesome_raspberry_pi'

# Path to the config file referenced in the section above
PIN_CONFIG = '/path/to/config/file.yml'

gpio_broadcast_service = GPIOBasicBroadcastService(
    rabbit_url=RABBIT_URL,
    device_key=DEVICE_KEY,
    pin_config=PIN_CONFIG)

gpio_broadcast_service.start()
```


## GPIO custom broadcast service

The GPIO custom broadcast service (`pi_broadcast_service.GPIOCustomBroadcastService`) functions in almost the same way as the basic version. The difference with this version is that it is up to you to implement your own event handler class. Your custom event handler will need to inherit from `pi_broadcast_service.GPIOCustomBroadcastEventHandler` for you to access to the `broadcast` method from inside you own custom handler methods.

### Configuring the GPIO custom broadcast service

This is the same as the basic version, using the YAML file, except you will name your own `handler` for each pin. Each `handler` name must correspond to a method name in your custom event handler class.

### Starting the custom GPIO service

This part runs on your Raspberry Pi. It initializes the desired GPIO pins, connects to RabbitMQ, waits for the defined pin events, and then executes one of your custom handler methods when an event happens. The message is sent to the RabbitMQ broker on an exchange named `gpio_broadcast`, with a routing key that matches the `device_key` value used to crteate the service instance.

```python
from pi_broadcast_service import GPIOCustomBroadcastService, GPIOCustomBroadcastEventHandler


# The RabbitMQ connection string
RABBIT_URL='some_actual_connection_string'

# A unique string you make up to identify a single Raspberry Pi
DEVICE_KEY='my_awesome_raspberry_pi'

# Path to the config file referenced in the section above
PIN_CONFIG = '/path/to/config/file.yml'

class MyEventHandler(GPIOCustomBroadcastEventHandler):

    def do_something(self, pin_number):
        # Build my_custom_message as a dictionary then use self.broadcast()
        return self.broadcast(my_custom_message)

gpio_broadcast_service = GPIOCustomBroadcastService(
    rabbit_url=RABBIT_URL,
    device_key=DEVICE_KEY,
    pin_config=PIN_CONFIG,
    event_handler=MyEventHandler)

gpio_broadcast_service.start()

```

