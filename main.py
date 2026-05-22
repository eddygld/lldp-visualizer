"""
main.py — Entry point for the LLDP Network Visualizer.

Pipeline:
    collector.py → connect to switches, fetch LLDP neighbors + loopback IPs
    graph.py     → draw and save the network diagram
"""

import config
import collector
import graph


def main():
    print("=" * 50)
    print("  LLDP Network Visualizer")
    print("=" * 50)

    print("\n[Stage 1] Collecting LLDP topology and interface IPs...")
    topology, ips = collector.collect_topology()

    print("\n  Summary:")
    for name, neighbors in topology.items():
        print(f"    {name} ({ips.get(name) or 'no loopback'}): {len(neighbors)} neighbor(s)")
        for n in neighbors:
            print(f"      -> {n['neighbor_name']} "
                  f"| {n['local_port']} <-> {n['remote_port']}")

    print("\n[Stage 2] Rendering graph...")
    graph.build_graph(topology, ips)
    print(f"\n  Graph saved to: {config.OUTPUT_FILENAME}.{config.OUTPUT_FORMAT}")
    print("\nDone.")


if __name__ == "__main__":
    main()