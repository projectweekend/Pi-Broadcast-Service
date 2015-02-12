from rabbit import Publisher


# Base class that Pi-Pin-Manager event handler classes can inherit from
class BroadcastEventBase(object):

    def __init__(self, rabbit_url, exchange, device_key):
        self._publisher = Publisher(rabbit_url, exchange)
        self._device_key = device_key

    def _broadcast(self, message):
        self._publisher.send(self._device_key, message)
