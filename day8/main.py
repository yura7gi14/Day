import yaml
from graphviz import Digraph

# YAML読み込み
with open("test.yaml", "r") as f:
    data = yaml.safe_load(f)

nodes = data.get("nodes", [])
edges = data.get("edges", [])

# グラフ生成
dot = Digraph(comment="Network Topology", format="png")
dot.attr(rankdir="LR")  # 左→右に表示（見やすい）

# ノード追加
for node in nodes:
    dot.node(node["id"], node["label"])

# エッジ追加
for edge in edges:
    dot.edge(edge["from"], edge["to"])

# 出力
dot.render("output/topology", view=False)
