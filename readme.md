<p align="center">
  <img src="logo.png" width="100" alt="miniTCP logo" />
</p>

<h1 align="center">miniTCP</h1>

<p align="center"><em>A minimal, reliable transport built on top of UDP — for learning and prototyping.</em></p>

---

## What this is

miniTCP is a compact, educational implementation of a TCP-like reliable transport implemented over plain UDP sockets.  
It demonstrates the core ideas behind TCP — connection handshake, sequence numbers, ACKs, retransmission and reassembly — in a short, readable Python codebase.

> This is a learning tool, not a production protocol.

---

## Files

- `toy_tcp_sender.py` — client (sends data)
- `toy_tcp_receiver.py` — server (receives, reorders, ACKs)
- `README.md` — this file

---

## Key ideas (TL;DR)

- **Handshake**: SYN → SYN-ACK → ACK to establish initial sequence numbers.  
- **Sequence numbers**: byte-based offsets to place packets in the stream.  
- **ACKs**: receiver sends back the next expected byte (cumulative ACK).  
- **Retransmit**: sender resends when ACK times out.  
- **Reassembly buffer**: receiver stores out-of-order packets and delivers them in order.

---

## Run the demo

Open two terminals.

**1. Start the receiver**
```bash
python3 toy_tcp_receiver.py
