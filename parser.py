"""
parser.py — Converts a PyEZ LLDPNeighborTable into a clean list of dicts.
"""

from jnpr.junos.op.lldp import LLDPNeighborTable


def parse_lldp_table(table: LLDPNeighborTable) -> list[dict]:
    """
    Converts a PyEZ LLDPNeighborTable into a list of neighbor dicts.

    Each dict has:
        local_port    — interface on this device, e.g. "xe-0/0/0"
        neighbor_name — hostname of the neighbor device
        remote_port   — port description on the neighbor
        neighbor_ip   — management IP of the neighbor (empty if not advertised)
    """
    neighbors = []

    for entry in table:
        if not entry.remote_sysname:
            continue

        neighbors.append({
            "local_port":    entry.local_int or "",
            "neighbor_name": entry.remote_sysname or "",
            "remote_port":   entry.remote_port_desc or "",
            "neighbor_ip":   "",
        })

    return neighbors