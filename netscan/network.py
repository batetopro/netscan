import ipaddress
from socket import AddressFamily


import psutil


class LocalNetworks:
    @classmethod
    def get_adapters_up(cls):
        up_adapters = set()

        for name, info in psutil.net_if_stats().items():
            if info.isup:
                up_adapters.add(name)

        return up_adapters

    @classmethod
    def get_networks(cls):
        result = list()

        adapters_up = cls.get_adapters_up()

        for name, addresses in psutil.net_if_addrs().items():
            if name not in adapters_up:
                continue

            for address in addresses:
                if address.family != AddressFamily.AF_INET:
                    continue

                a = ipaddress.IPv4Address(address.address)
                if a.is_loopback or address.netmask is None:
                    continue

                network = ipaddress.IPv4Network(
                    "{}/{}".format(address.address, address.netmask),
                    strict=False
                )
                result.append(network)

        return result
