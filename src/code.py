import os

import adafruit_requests
import board
import mdns
import wifi
from adafruit_connection_manager import get_radio_socketpool, get_radio_ssl_context
from adafruit_httpserver import GET, OPTIONS, POST, Request, Response, Server

import gui

mdns_server = mdns.Server(wifi.radio)
mdns_server.hostname = os.getenv("SOUNDTHING_HOSTNAME", "soundthing.local")
mdns_server.instance_name = os.getenv("SOUNDTHING_NAME", "SoundThing")

pool = get_radio_socketpool(wifi.radio)
ssl_context = get_radio_ssl_context(wifi.radio)
server = Server(pool, debug=True)
server.headers = {
    "Access-Control-Allow-Origin": "https://soundcloud.com",
    "Access-Control-Request-Method": "POST",
    # "Access-Control-Request-Headers": "",
}


@server.route("/track-info", [OPTIONS], append_slash=True)
def cors(request: Request):
    return Response(request)

@server.route("/track-info", [GET], append_slash=True)
def info(request: Request):
    info = ui.get_track_info()
    artist = info["artist"]
    track = info["track"]
    return Response(request, f"Now Playing: {artist} - {track}")

@server.route("/track-info", [POST], append_slash=True)
def base(request: Request):
    """
    Serve a default static plain text message.
    """
    info = request.json()
    artist = info.get("artist", "Unknown Artist")
    track = info.get("title", "Unknown Title")
    image = info.get("image", "")

    ui.set_track_info(artist, track)
    if image:
        with client.get(image) as response:
            if response.status_code == 200:
                print(f"size: {len(response.content)}")
                ui.render_artwork(response.content)
    return Response(request, f"Now Playing: {artist} - {track}")


client = adafruit_requests.Session(pool, ssl_context)
ui = gui.GUI(width=board.DISPLAY.width, height=board.DISPLAY.height)

board.DISPLAY.root_group = ui

ip = str(wifi.radio.ipv4_address)
port = os.getenv("SOUNDTHING_PORT", 80)
server.start(ip, port)
mdns_server.advertise_service(service_type="_http", protocol="_tcp", port=int(port))

print(f"Listening: {ip}:{port}")

while True:
    try:
        ui.update()
        pool_result = server.poll()
    except OSError as error:
        print(error)

