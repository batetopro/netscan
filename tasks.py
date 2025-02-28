import json


from invoke import task


from netscan.arp import ArpCollector
from netscan.dns import ReverseDnsResolver
from netscan.network import LocalNetworks
from netscan.pings import LocalNetworkPings


def print_result(result):
    print(json.dumps(result, indent=4))


@task
def arp(c):
    collector = ArpCollector()
    result = collector.run()
    print_result(result)


@task
def dns(c, ip):
    resolver = ReverseDnsResolver()
    result = resolver.lookup(ip)
    print_result(result)


@task
def networks(c):
    local_networks = LocalNetworks()
    result = [str(n) for n in local_networks.get_networks()] 
    print_result(result)


@task
def pings(c, network):
    runner = LocalNetworkPings()
    result = runner.make(network)
    print_result(result)
