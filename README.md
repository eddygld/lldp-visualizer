# LLDP Network Visualizer

A Python automation tool that discovers network topology using the Link Layer
Discovery Protocol (LLDP) and renders it as a graphical diagram. Built for
Juniper network devices using the PyEZ library and Graphviz.

---

## Project Structure

```
lldp_visualizer/
├── config.py        → Device inventory, credentials, output settings, static topology fallback
├── connector.py     → Opens and closes PyEZ Device sessions
├── collector.py     → Fetches LLDP neighbors and loopback IPs from each device
├── parser.py        → Converts PyEZ LLDPNeighborTable into clean Python dicts
├── graph.py         → Builds and renders the Graphviz network diagram
├── main.py          → Entry point — runs the full pipeline
└── requirements.txt → Python dependencies
```

---

## Requirements

### Python dependencies
```bash
pip install -r requirements.txt
```

### Graphviz system binary
The Python `graphviz` package is a wrapper — the Graphviz binary must also
be installed on your system.

```bash
# macOS
brew install graphviz

# Ubuntu / Debian
sudo apt install graphviz
```

Verify the installation:
```bash
dot -V
```

---

## Configuration

All settings live in `config.py`. Edit this file before running.

```python
# Device inventory
ROUTERS = [
    {"host": "66.129.235.201", "port": 46034, "name": "Switch-1"},
    {"host": "66.129.235.201", "port": 46038, "name": "Switch-2"},
    {"host": "66.129.235.201", "port": 46042, "name": "Switch-3"},
    {"host": "66.129.235.201", "port": 46046, "name": "Switch-4"},
]

# Credentials
USERNAME = "jcluser"
PASSWORD = "Juniper1234"

# Output
OUTPUT_FILENAME = "lldp_topology"
OUTPUT_FORMAT   = "png"           # "png", "pdf", or "svg"
```

> **Note:** Device names in `ROUTERS` must exactly match the hostnames
> advertised by the devices via LLDP. If they don't match, neighbor nodes
> will appear as separate unconnected nodes in the diagram.

---

## Usage

```bash
python3 main.py
```

The tool will:
1. Connect to each device via NETCONF/SSH
2. Collect LLDP neighbor information using PyEZ's `LLDPNeighborTable`
3. Retrieve the loopback IP address from each device
4. Render a network diagram and save it as `lldp_topology.png`

### Example output
```
==================================================
  LLDP Network Visualizer
==================================================

[Stage 1] Collecting LLDP topology and interface IPs...
  Connecting to Switch-1 (66.129.235.201:46034)...
  [LIVE] Switch-1 — 3 neighbor(s) | loopback: 10.255.0.1
  Connecting to Switch-2 (66.129.235.201:46038)...
  [LIVE] Switch-2 — 3 neighbor(s) | loopback: 10.255.0.2
  ...

[Stage 2] Rendering graph...
  Graph saved to: lldp_topology.png

Done.
```

---

## Enable LLDP on Juniper Devices

LLDP must be enabled on each device before running the tool.
On each device (Junos CLI):

```
configure
set protocols lldp interface all
commit
exit
```

Wait 30–60 seconds for neighbor tables to populate, then verify:

```
show lldp neighbors
show lldp statistics
```

---

## Troubleshooting

**`[FALLBACK]` shown instead of `[LIVE]`**
The device connected but returned no LLDP neighbors. Check that:
- LLDP is enabled on the device (`show lldp`)
- Enough time has passed for neighbor discovery (at least 60 seconds)
- The virtual lab environment forwards Layer 2 multicast frames

The tool automatically falls back to `config.STATIC_TOPOLOGY` in this case.
The static topology uses the same data format as live collection so the
diagram renders correctly either way.

**`[TIMEOUT]` or `[CONNECT ERROR]`**
The device is unreachable. Check that:
- The host IP and port in `config.py` are correct
- NETCONF is enabled on the device:
  ```
  set system services netconf ssh
  commit
  ```
- You can SSH into the device manually on the configured port

**Extra nodes appearing in the diagram**
Device names in `config.ROUTERS` do not match the hostnames advertised
via LLDP. Run `show lldp neighbors` on a device and check the
`System name` column — update `config.ROUTERS` to match exactly.

**`ValueError: Unknown field`in parser.py**
The PyEZ `LLDPNeighborTable` field names vary by Junos version. Run
`check_lldp_fields.py` to inspect the correct field names for your
devices and update `parser.py` accordingly.

---

## Known Limitations

- Juniper vMX routers in the Juniper vLabs hosted environment do not forward
  Layer 2 multicast frames between virtual instances, preventing live LLDP
  discovery. The static topology fallback in `config.py` can be used instead.
- The vQFX interconnect interfaces (`xe-0/0/x`) operate as Layer 2 switch
  ports and carry no IP addresses. Loopback IPs are displayed on node labels
  as the Layer 3 device identifier instead.
