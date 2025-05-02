import yaml
from graphviz import Digraph
from collections import defaultdict

type_styles = {
    "router": {"shape": "box", "style": "filled", "fillcolor": "lightblue"},
    "switch": {"shape": "ellipse", "style": "filled", "fillcolor": "lightgreen"},
    "pc": {"shape": "circle", "style": "filled", "fillcolor": "lightgray"}
}

with open("network.yaml", "r") as f:
    data = yaml.safe_load(f)

nodes = data.get("nodes", [])
edges = data.get("edges", [])

groups = defaultdict(list)
for node in nodes:
    group = node.get("group", None)
    if group:
        groups[group].append(node)

dot = Digraph(comment="Network Topology", format="svg")
dot.attr(rankdir="LR")

for node in nodes:
    if not node.get("group"):
        style = type_styles.get(node.get("type"), {})
        dot.node(node["id"], node["label"], **style)

for group_name, group_nodes in groups.items():
    with dot.subgraph(name=f"cluster_{group_name}") as sub:
        sub.attr(label=group_name)
        for node in group_nodes:
            style = type_styles.get(node.get("type"), {})
            sub.node(node["id"], node["label"], **style)

for edge in edges:
    dot.edge(edge["from"], edge["to"], label=edge.get("label", ""))

dot.render("output/topology", view=False)
print("SVG構成図をoutput/topology.svgに出力しました")