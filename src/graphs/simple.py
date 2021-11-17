nodes = list("ABCDE")

boundary_nodes = ["A", "E"]
entry_points = {char: 1 for char in boundary_nodes}
exit_points = {char: 1 for char in boundary_nodes}

edges = [
    ["A", "B", 20],
    ["B", "C", 40],
    ["C", "D", 10],
    ["B", "E", 30],
    ["C", "E", 30]
]
