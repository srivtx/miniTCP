import socket
import json
import time

sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver_addr = ("127.0.0.1", 9000)

def send_packet(pkt):
    sender.sendto(json.dumps(pkt).encode(), receiver_addr)

def recv_packet(timeout=2):
    sender.settimeout(timeout)
    try:
        data, _ = sender.recvfrom(4096)
        return json.loads(data.decode())
    except socket.timeout:
        return None

# ---- Handshake ----
ISN = 1000
send_packet({"seq": ISN, "ack": 0, "flags": "SYN", "data": ""})
print("Sent SYN")

resp = recv_packet()
if resp and resp["flags"] == "SYN-ACK":
    server_isn = resp["seq"]
    print("Received SYN-ACK")

send_packet({"seq": ISN+1, "ack": server_isn+1, "flags": "ACK", "data": ""})
print("Handshake complete")

send_seq = ISN + 1

# ---- Send function ----
def send_data(data):
    global send_seq
    pkt = {"seq": send_seq, "ack": 0, "flags": "DATA", "data": data}
    send_packet(pkt)
    print(f"\nSent DATA: {data} with seq={send_seq}")

    expected_ack = send_seq + len(data)
    send_seq = expected_ack

    # Wait for ACK
    resp = recv_packet(timeout=1)
    if resp:
        print("Got ACK:", resp["ack"])
        return True
    else:
        print("Timeout → Resending...")
        send_packet(pkt)
        resp = recv_packet(timeout=1)
        if resp:
            print("Got ACK after retry:", resp["ack"])
        return False

# ---- Demonstration ----
send_data("ABCD")
send_data("EFGH")
send_data("IJKL")
