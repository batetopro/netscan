import json


from invoke import task


from netscan.arp import ArpCollector
from netscan.dns import ReverseDnsResolver
from netscan.network import LocalNetworks
from netscan.pings import LocalNetworkPings


@task
def arp(c):
    collector = ArpCollector()
    result = collector.run()
    print(json.dumps(result))


@task
def dns(c, ip):
    resolver = ReverseDnsResolver()
    result = resolver.lookup(ip)
    print(json.dumps(result))


@task
def networks(c):
    local_networks = LocalNetworks()
    print(
        json.dumps(
            [str(n) for n in local_networks.get_networks()]
        )
    )


@task
def pings(c, network):
    runner = LocalNetworkPings()
    result = runner.make(network)
    print(json.dumps(result))
