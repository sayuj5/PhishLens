import asyncio
from typing import Dict, Any, List
from backend.discovery.providers.base import BaseDiscoveryProvider
from backend.logger import discovery_logger

class TCPDiscoveryProvider(BaseDiscoveryProvider):
    """
    Pure Python asyncio based TCP Connect scanner.
    Suitable for fast, authorised port scanning and banner grabbing.
    """
    
    async def _check_port(self, ip: str, port: int, timeout_ms: int) -> bool:
        try:
            future = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(future, timeout=timeout_ms / 1000.0)
            writer.close()
            await writer.wait_closed()
            return True
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            return False

    async def is_reachable(self, ip: str, timeout_ms: int = 1000) -> bool:
        """
        TCP Ping: Checks a few common ports (22, 80, 443, 3389).
        If any respond, the host is reachable.
        """
        common_ports = [22, 80, 443, 445, 3389]
        tasks = [self._check_port(ip, port, timeout_ms) for port in common_ports]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return any(isinstance(r, bool) and r for r in results)

    async def scan_ports(self, ip: str, ports: List[int], timeout_ms: int = 1000) -> List[int]:
        open_ports = []
        # Batch tasks to avoid too many open file descriptors
        batch_size = 50
        for i in range(0, len(ports), batch_size):
            batch = ports[i:i+batch_size]
            tasks = [self._check_port(ip, port, timeout_ms) for port in batch]
            results = await asyncio.gather(*tasks, return_exceptions=True)
            for port, is_open in zip(batch, results):
                if isinstance(is_open, bool) and is_open:
                    open_ports.append(port)
        return open_ports

    async def grab_banner(self, ip: str, port: int, timeout_ms: int = 2000) -> str:
        banner = ""
        try:
            future = asyncio.open_connection(ip, port)
            reader, writer = await asyncio.wait_for(future, timeout=timeout_ms / 1000.0)
            
            # Send a generic probe (HTTP GET or just an empty newline) to trigger a response
            probe = b"HEAD / HTTP/1.0\r\n\r\n"
            writer.write(probe)
            await writer.drain()
            
            data = await asyncio.wait_for(reader.read(1024), timeout=timeout_ms / 1000.0)
            banner = data.decode('utf-8', errors='ignore').strip()
            
            writer.close()
            await writer.wait_closed()
        except (asyncio.TimeoutError, ConnectionRefusedError, OSError):
            pass
        return banner

    async def fingerprint_os(self, ip: str, open_ports: List[int]) -> Dict[str, Any]:
        """
        Basic OS guessing based on open ports.
        """
        os_guess = "Unknown"
        vendor = "Unknown"
        
        if 3389 in open_ports or 135 in open_ports or 445 in open_ports:
            os_guess = "Windows"
            vendor = "Microsoft"
        elif 22 in open_ports:
            os_guess = "Linux"
            vendor = "Unknown"
            
        return {"os": os_guess, "vendor": vendor}
