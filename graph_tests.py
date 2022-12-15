import graph as gr

nodes = {i: None for i in range(10)}
G = gr.Graph(nodes)

G.add_edge(0, 1, 6)
G.add_edge(1, 4, 11)
G.add_edge(4, 5, 3)
G.add_edge(0, 3, 18)
G.add_edge(0, 2, 8)
G.add_edge(2, 3, 9)
G.add_edge(5, 3, 4)
G.add_edge(5, 2, 7)

dj = G.single_source_shortest_parth(0)
print(list(dj.get_path(3)))
print(dj.get_distance(3))
