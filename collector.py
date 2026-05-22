"""
collector.py — Collects LLDP neighbor data and loopback IPs from all switches.
"""

from jnpr.junos.op.lldp import LLDPNeighborTable

import config
from connector import get_device
from parser import parse_lldp_table


def get_loopback_ip(dev) -> str:
    """
    Fetches the loopback IP address (lo0.0) from a switch.

    Returns the IP as a string (e.g. "10.255.0.1"), or empty string
    if no loopback IP is found.
    """
    raw = dev.rpc.get_interface_information(terse=True)

    # Find lo0.0 logical interface and extract its inet ifa-local
    for logical in raw.xpath(
        "//*[local-name()='logical-interface']"
        "[*[local-name()='name'][normalize-space()='lo0.0']]"
    ):
        result = logical.xpath(
            ".//*[local-name()='address-family']"
            "[*[local-name()='address-family-name'][normalize-space()='inet']]"
            "//*[local-name()='ifa-local']"
        )
        if result:
            return result[0].text.strip()

    return ""


def collect_topology() -> tuple[dict, dict]:
    """
    Connects to every switch in config.ROUTERS, fetches LLDP neighbors
    and loopback IPs, and returns both as a tuple.

    Returns:
        topology: { "Switch-1": [ {neighbor dict}, ... ], ... }
        ips:      { "Switch-1": "10.255.0.1", ... }
    """
    topology = {}
    ips      = {}

    for router in config.ROUTERS:
        name = router["name"]
        host = router["host"]
        port = router["port"]

        print(f"  Connecting to {name} ({host}:{port})...")
        dev = get_device(host, port)

        if dev is None:
            topology[name] = config.STATIC_TOPOLOGY.get(name, [])
            ips[name]      = ""
            print(f"  [FALLBACK] {name} — using static topology")
            continue

        table = LLDPNeighborTable(dev)
        table.get()
        neighbors = parse_lldp_table(table)

        loopback = get_loopback_ip(dev)
        dev.close()

        if neighbors:
            topology[name] = neighbors
            print(f"  [LIVE] {name} — {len(neighbors)} neighbor(s) | loopback: {loopback or 'none'}")
        else:
            topology[name] = config.STATIC_TOPOLOGY.get(name, [])
            print(f"  [FALLBACK] {name} — LLDP returned empty, using static topology")

        ips[name] = loopback

    return topology, ips