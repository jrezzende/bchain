import socket
from blockchain_api import app


def check_port_available(port_attempt):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.bind(('0.0.0.0', port_attempt))
    except socket.error:
        s.close()
        return True

    s.close()
    return False


if __name__ == '__main__':
    port = 5000

    while check_port_available(port):
        port += 1

    app.run(host='0.0.0.0', port=port, threaded=True, use_reloader=False)
