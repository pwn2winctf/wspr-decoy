#!/usr/bin/env python3
import websocket
import traceback
import _thread as thread
import json
import time

def on_message(ws, message):
    message = json.loads(message)
    if isinstance(message, dict) and message.get('type') == 'update':
        for spot in message['value']:
            if spot['callsign'] == 'PU2UID':
                if spot['mode'] != 'WSPR':
                    ws._result = 0
                elif spot['band'] != '40m':
                    ws._result = 0
                elif spot['location']['locator'] != 'GG68':
                    ws._result = 0
                elif time.time() - spot['lastseen']/1000. > 630:
                    ws._result = -1
                else:
                    ws._result = 1
                ws.close()


def on_open(ws):
    ws.send("SERVER DE CLIENT client=map.js type=map")

    def timeout(*_):
        time.sleep(3)
        ws.close()
    thread.start_new_thread(timeout, ())


def solve(chall_addr='pu2uid.duckdns.org', chall_port=443):
    try:
        ws = websocket.WebSocketApp("wss://{}:{}/ws/".format(chall_addr, chall_port),
                                    on_open=on_open,
                                    on_message=on_message)
        ws._result = -1
        ws.run_forever()
        return ws._result
    except:
        traceback.print_exc()
        return -1


if __name__ == "__main__":
    print(solve())
