import ipaddress
from pythonping import ping


from netscan.lock import Lock
from netscan.network import LocalNetworks


class LocalNetworkPings:
    @property
    def lock(self):
        if self._lock is None:
            self._lock = Lock('pings')
        return self._lock

    def __init__(self):
        self._lock = None

    def make(self, do_network):
        do_network = ipaddress.IPv4Network(do_network, strict=True)

        successful_pings = []
        self.lock.acquire(timeout=0)
        try:
            networks = LocalNetworks.get_networks()
            found = False

            for network in networks:
                if network == do_network:
                    found = True
                    break

            if not found:
                raise ValueError(
                    'Given network is not found in local networks.'
                )

            for address in do_network:
                if address.is_multicast or \
                        address == do_network.broadcast_address:
                    continue

                ip = str(address)
                ping_result = ping(ip, timeout=2, count=1)
                if ping_result.success():
                    # print(f'Hit {ip}')
                    successful_pings.append(ip)
                else:
                    pass
                    # print(f'Miss {ip}')
        finally:
            self.lock.release()

        return successful_pings
