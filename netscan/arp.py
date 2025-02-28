import os
import subprocess


from netscan.dns import ReverseDnsResolver
from netscan.lock import Lock


class ArpCollector:
    @property
    def lock(self):
        if self._lock is None:
            self._lock = Lock('arp')
        return self._lock

    @property
    def reverse_resolver(self):
        if self._reverse_resolver is None:
            self._reverse_resolver = ReverseDnsResolver()
        return self._reverse_resolver

    def __init__(self):
        self._lock = None
        self._reverse_resolver = None

    def run(self):
        self.lock.acquire(timeout=0)

        try:
            if os.name == 'nt':
                result = collect_arp_windows()
            else:
                result = collect_arp_linux()

            for record in result:
                record['dns_lookup'] = self.reverse_resolver.lookup(
                    record['address']
                )
        finally:
            self.lock.release()

        return result


def collect_arp_windows():
    command = "arp -a"
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=None,
        shell=True
    )

    data = process.communicate()[0].decode()
    result = []

    current_interface = None
    current_mask = None
    for line in data.splitlines():
        if not line:
            continue

        if line.startswith('Interface: '):
            current_interface, current_mask = \
                line[len('Interface: '):].split(' --- ', 1)
            continue

        if line.strip().startswith('Internet Address'):
            continue

        address, physical_address, address_type = line.strip().split()

        if physical_address == 'ff-ff-ff-ff-ff-ff':
            continue

        if physical_address.startswith('01-00-5e-'):
            continue

        result.append({
            'interface': current_interface,
            'mask': current_mask,
            'address': address,
            'physical_address': physical_address,
            'type': address_type,
        })

    return result


def collect_arp_linux():
    command = "arp -e"
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=None,
        shell=True
    )

    data = process.communicate()[0].decode()

    result = []
    for line in data.splitlines():
        if not line.strip():
            continue
        if line.startswith('Address'):
            continue

        parts = line.split()
        if len(parts) == 5:
            record = {
                'interface': parts[4],
                'mask': parts[3],
                'address': parts[0],
                'physical_address': parts[2],
                'type': parts[1],
            }
            result.append(record)

    return result
