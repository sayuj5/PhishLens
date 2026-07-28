import threading
from scapy.all import sniff
from queue import Queue

class Sniffer:
    def __init__(self, interface: str, packet_queue: Queue):
        self.interface = interface
        self.packet_queue = packet_queue
        self.running = False
        self.thread = None

    def _capture(self):
        # We don't store packets in memory to prevent OOM. We just pass to queue.
        # store=False is critical for long-running captures.
        sniff(iface=self.interface, prn=self._process_packet, store=False, stop_filter=self._should_stop)

    def _process_packet(self, packet):
        if self.running:
            self.packet_queue.put(packet)

    def _should_stop(self, packet) -> bool:
        return not self.running

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self._capture, daemon=True)
        self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join(timeout=2.0)
