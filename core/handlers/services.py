import socket

IP = "192.168.0.167"
PORT = 8000


def calc_cs(data):
    cs = 0
    for b in data:
        cs ^= b
    return cs


def build_packet(cmd, door=0x01, data=None):
    if data is None:
        data = []

    packet = [0x02, 0xA0, cmd, 0xFF, door]

    length = len(data)
    packet.append(length & 0xFF)
    packet.append((length >> 8) & 0xFF)

    packet.extend(data)

    packet.append(calc_cs(packet))
    packet.append(0x03)

    return bytearray(packet)


def send_packet(cmd):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((IP, PORT))
        sock.send(cmd)
        resp = sock.recv(1024)
        return resp.hex()
    except Exception as e:
        return str(e)
    finally:
        sock.close()


def add_card_to_device(
    card_number,
    pin,
    index,
    expire_year,
    expire_month,
    expire_day
):
    pin = str(pin).zfill(4)

    card_bytes = [
        card_number & 0xFF,
        (card_number >> 8) & 0xFF,
        (card_number >> 16) & 0xFF,
        (card_number >> 24) & 0xFF
    ]

    pin_bytes = [int(x) for x in pin]

    packet_data = []

    # Index
    packet_data.append(index & 0xFF)
    packet_data.append((index >> 8) & 0xFF)

    # Card + PIN
    packet_data.extend(card_bytes)
    packet_data.extend(pin_bytes)

    # Reserved
    packet_data.extend([0x01, 0x00])
    packet_data.extend([0x00, 0x00])

    # Expiry
    packet_data.extend([
        expire_year - 2000,
        expire_month,
        expire_day,
        23,
        59
    ])

    # Enable
    packet_data.append(0x01)

    packet = build_packet(0x62, 0x01, packet_data)

    return send_packet(packet)