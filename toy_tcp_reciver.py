import socket
import json

receiver = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
receiver.bind(("127.0.0.1", 9000))

def recv_packet():
    data, addr = receiver.recvfrom(4096)
    return json.loads(data.decode()), addr

def send_packet(pkt, addr):
    receiver.sendto(json.dumps(pkt).encode(), addr)

print("Receiver running on 127.0.0.1:9000")

# ---- Handshake ----
pkt, addr = recv_packet()

if pkt["flags"] == "SYN":
    client_isn = pkt["seq"]
    my_isn = 5000
    print("Got SYN")

    send_packet({"seq": my_isn, "ack": client_isn+1, "flags": "SYN-ACK", "data": ""}, addr)
    print("Sent SYN-ACK")

    pkt, addr = recv_packet()
    if pkt["flags"] == "ACK":
        print("Handshake complete")

expected_seq = client_isn + 1
buffer = {}

print("\n=== READY TO RECEIVE DATA ===\n")

# ---- Data Receive Loop ----
while True:
    pkt, addr = recv_packet()

    if pkt["flags"] == "DATA":
        seq = pkt["seq"]
        data = pkt["data"]

        if seq == expected_seq:
            print(f"Delivered: {data}")
            expected_seq += len(data)

            # Deliver buffered packets
            while expected_seq in buffer:
                print(f"Delivered from buffer: {buffer[expected_seq]}")
                expected_seq += len(buffer[expected_seq])
                del buffer[expected_seq]

        elif seq > expected_seq:
            print(f"Out-of-order → Stored: {data}")
            buffer[seq] = data

        else:
            print("Duplicate ignored")

        # Always send ACK
        send_packet({"seq": 0, "ack": expected_seq, "flags": "ACK", "data": ""}, addr)
