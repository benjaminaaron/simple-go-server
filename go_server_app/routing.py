from channels.routing import route
from .consumers import ws_connect, ws_message, ws_disconnect


channel_routing = [
    route("websocket.connect", ws_connect),  # path=r"^/(?P<some_id>[a-zA-Z0-9_]+)/$"
    route("websocket.receive", ws_message),
    route("websocket.disconnect", ws_disconnect),
]
