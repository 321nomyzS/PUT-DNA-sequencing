class Graph:
    def __init__(self):
        self.incident_list = {}

    def __str__(self):
        result = ""
        for key in self.incident_list.keys():
            result += f"{key} -> {self.incident_list[key]}\n"
        return result

    def load_data(self, source):
        for element in source:
            self.incident_list.update({self._create_label(element): []})
        self._generate_graph()

    def load_data_file(self, filename):
        with open(filename, "r") as f:
            sequences = f.readlines()

        for i in range(len(sequences)):
            if sequences[i][-1] == '\n':
                sequences[i] = sequences[i][:-1]

        self.load_data(sequences)

    def _create_label(self, element):
        key_list = list(self.incident_list.keys())
        for i in range(len(key_list)):
            key_list[i] = key_list[i].split("-")[0]

        element_count = key_list.count(element)
        return f"{element}-{element_count}"

    def _generate_graph(self):
        vertex_list = list(self.incident_list.keys())

        for i in range(len(vertex_list)):
            for j in range(len(vertex_list)):
                vertex_label_1 = vertex_list[i].split('-')[0]
                vertex_label_2 = vertex_list[j].split('-')[0]

                if vertex_label_1 == vertex_label_2:
                    continue

                for k in range(len(vertex_label_1)-1, 0, -1):
                    if vertex_label_1[-k:] == vertex_label_2[:k]:
                        self.incident_list[vertex_list[i]].append((vertex_list[j], len(vertex_label_1)-k))

    def shortest_cycle_path(self):
        import random
        n = len(self.incident_list)
        visited = []
        best_path = []

        def dfs(current, length, path):
            nonlocal best_path

            visited.append(current)
            path.append(current)

            if len(path) == n:
                # jeśli odwiedziliśmy wszystkie wierzchołki, to dodajemy koszt podróży powrotnej do kosztu
                length += self.incident_list[current][0][1]
                best_path = path.copy()

            elif not best_path:
                min_cost = float("inf")
                min_neighbor = None
                for neighbor, cost in self.incident_list[current]:
                    if neighbor not in visited and cost < min_cost:
                        min_cost = cost
                        min_neighbor = neighbor
                if min_neighbor:
                    dfs(min_neighbor, length + min_cost, path)

            visited.remove(current)
            path.pop()

        while best_path is None or best_path == []:
            start = random.choice(list(self.incident_list.keys()))
            dfs(start, 0, [])
        return best_path


# Expected output: ACCCGCCGCCACCCGCCGCCACCCGCCGCCACCCGCCGCC
G = Graph()
G.load_data_file("dna.txt")
path = G.shortest_cycle_path()

dna = ""
for element in path:
    dna += element[0]

print(dna)
