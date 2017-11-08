import websocket
import _thread as thread  # via stackoverflow.com/a/3353841/2474159
import sys


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    print('Connected to ' + ws.url)

    def run():
        while True:
            command = input('> ')  # catch arrow-keys up/down and implement command-history TODO
            if command == 'quit' or command == 'quit()' or command == 'exit':
                ws.close()
                break
            ws.send(command)
    thread.start_new_thread(run, ())


if __name__ == "__main__":  # via github.com/websocket-client/websocket-client#long-lived-connection
    if len(sys.argv) > 1:  # 0 is always own filename
        url = sys.argv[1]
    else:
        print('Enter the WebSocket URL:')
        url = input()
    if not url.startswith('ws://'):
        url = 'ws://' + url

    socket = websocket.WebSocketApp(url, on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
    socket.run_forever()
