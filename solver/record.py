#!/usr/bin/env python3
import websocket
import sys


def on_message(ws, message):
    if isinstance(message, bytes) and message[0] == 2:
        # audio data
        ws.f.write(message[1:])


def on_open(ws):
    ws.send('SERVER DE CLIENT client=openwebrx.js type=receiver')
    ws.send(
        '{"type":"connectionproperties","params":{"output_rate":12000,"hd_output_rate":48000}}')
    ws.send('{"type":"dspcontrol","params":{"low_cut":300,"high_cut":3000,"offset_freq":38600,"mod":"usb","dmr_filter":3,"squelch_level":-150,"secondary_mod":false}}')
    ws.send('{"type":"dspcontrol","action":"start"}')
    ws.send('{"type":"dspcontrol","params":{"secondary_offset_freq":1000}}')


def main(filename, chall_addr='pu2uid.duckdns.org', chall_port=443):
    ws = websocket.WebSocketApp("wss://{}:{}/ws/".format(chall_addr, chall_port),
                                on_open=on_open,
                                on_message=on_message)
    ws.f = open(filename, 'wb')
    ws.run_forever()


if __name__ == "__main__":
    main(sys.argv[1])
