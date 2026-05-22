"""
config.py — Central configuration for the LLDP Visualizer.
No credentials or IPs should ever appear in any other file.
"""

# Router inventory
# Add or remove routers here. Every other module reads from this list.
ROUTERS = [
    {"host": "YOUR_HOST_IP", "port": 22, "name": "Switch-1"},
    {"host": "YOUR_HOST_IP", "port": 22, "name": "Switch-2"},
    {"host": "YOUR_HOST_IP", "port": 22, "name": "Switch-3"},
    {"host": "YOUR_HOST_IP", "port": 22, "name": "Switch-4"},
]

# Hardcoded topology fallback
STATIC_TOPOLOGY = {
    "Switch-1": [
        {"local_port": "xe-0/0/0", "neighbor_name": "Switch-2", "remote_port": "to Switch-1", "neighbor_ip": ""},
        {"local_port": "xe-0/0/2", "neighbor_name": "Switch-3", "remote_port": "to Switch-1", "neighbor_ip": ""},
        {"local_port": "xe-0/0/1", "neighbor_name": "Switch-4", "remote_port": "to Switch-1", "neighbor_ip": ""},
    ],
    "Switch-2": [
        {"local_port": "xe-0/0/0", "neighbor_name": "Switch-1", "remote_port": "to Switch-2", "neighbor_ip": ""},
        {"local_port": "xe-0/0/1", "neighbor_name": "Switch-3", "remote_port": "to Switch-2", "neighbor_ip": ""},
        {"local_port": "xe-0/0/2", "neighbor_name": "Switch-4", "remote_port": "to Switch-2", "neighbor_ip": ""},
    ],
    "Switch-3": [
        {"local_port": "xe-0/0/2", "neighbor_name": "Switch-1", "remote_port": "to Switch-3", "neighbor_ip": ""},
        {"local_port": "xe-0/0/1", "neighbor_name": "Switch-2", "remote_port": "to Switch-3", "neighbor_ip": ""},
        {"local_port": "xe-0/0/0", "neighbor_name": "Switch-4", "remote_port": "to Switch-3", "neighbor_ip": ""},
    ],
    "Switch-4": [
        {"local_port": "xe-0/0/1", "neighbor_name": "Switch-1", "remote_port": "to Switch-4", "neighbor_ip": ""},
        {"local_port": "xe-0/0/2", "neighbor_name": "Switch-2", "remote_port": "to Switch-4", "neighbor_ip": ""},
        {"local_port": "xe-0/0/0", "neighbor_name": "Switch-3", "remote_port": "to Switch-4", "neighbor_ip": ""},
    ],
}

# NETCONF / SSH credentials
USERNAME = "your_username"
PASSWORD = "your_password"

# Output settings
OUTPUT_FILENAME = "lldp_topology"   # no extension — Graphviz adds it
OUTPUT_FORMAT   = "png"             # "png", "pdf", or "svg"

# Graphviz layout engine
# "neato"  → physics-based, good for network diagrams (recommended)
# "dot"    → top-down tree, better for hierarchies
GRAPH_ENGINE = "neato"