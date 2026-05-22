"""
graph.py — Builds and renders the LLDP network diagram using Graphviz.
"""

from graphviz import Graph

import config

# Fixed positions for each switch — defines the square layout.
# Format is "x,y!" — the "!" pins the node so neato won't move it.
NODE_POSITIONS = {
    "Switch-1": "0,2!",
    "Switch-2": "4,2!",
    "Switch-3": "0,0!",
    "Switch-4": "4,0!",
}


def build_graph(topology: dict, ips: dict) -> Graph:
    """
    Constructs and renders an undirected Graphviz network diagram.

    Nodes  = switches, labelled with name + loopback IP
    Edges  = LLDP neighbor links, with interface labels at each end
    Output = image file at config.OUTPUT_FILENAME.config.OUTPUT_FORMAT

    Uses frozenset to deduplicate edges — since LLDP is symmetric,
    both Switch-1 and Switch-2 report each other. Without dedup,
    every link would be drawn twice.
    """
    dot = Graph(
        name="LLDP Network Topology",
        engine="neato",
        graph_attr={
            "overlap": "false",
            "splines": "false",
            "pad":     "0.5",
            "sep":     "+25",
        },
        node_attr={
            "shape":     "box",
            "style":     "filled",
            "fillcolor": "#D0E4F7",
            "fontname":  "Helvetica",
            "fontsize":  "11",
            "width":     "1.4",
        },
        edge_attr={
            "fontname":      "Helvetica",
            "fontsize":      "8",
            "color":         "#555555",
            "labelfontsize": "8",
            "labeldistance": "2.5",
            "labelangle":    "20",
        },
    )

    # Add nodes — label shows switch name + loopback IP below
    for router in config.ROUTERS:
        name     = router["name"]
        pos      = NODE_POSITIONS.get(name, "0,0!")
        loopback = ips.get(name, "")
        label    = f"{name}\n{loopback}" if loopback else name
        dot.node(name, label, pos=pos)

    # Add edges — deduplicated with frozenset
    drawn_edges = set()
    for router_name, neighbors in topology.items():
        for n in neighbors:
            edge_key = frozenset([router_name, n["neighbor_name"]])
            if edge_key in drawn_edges:
                continue
            drawn_edges.add(edge_key)

            dot.edge(
                router_name,
                n["neighbor_name"],
                taillabel=n["local_port"],
                headlabel=n["remote_port"],
            )

    dot.render(filename=config.OUTPUT_FILENAME, format=config.OUTPUT_FORMAT, cleanup=True)