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
        j = 0
        vertex_list = list(self.incident_list.keys())

        for i in range(len(vertex_list)):
            main_loop_label = "main_loop"
            for j in range(len(vertex_list)):
                vertex_label_1 = vertex_list[i].split('-')[0]
                vertex_label_2 = vertex_list[j].split('-')[0]

                if i == j:
                    continue
                self.incident_list[vertex_list[i]].append((vertex_list[j], len(vertex_label_1)))

                for k in range(len(vertex_label_1)-1, 0, -1):
                    if vertex_label_1[-k:] == vertex_label_2[:k]:
                        self.incident_list[vertex_list[i]].append((vertex_list[j], len(vertex_label_1)-k))
                        j = len(vertex_list)
                        break

        for vertex in vertex_list:
            self.incident_list[vertex] = sorted(self.incident_list[vertex], key=lambda x: x[1])

    def shortest_cycle_path(self, n, l):
        import random
        visited = []
        best_path = []
        start_vertexes = list(self.incident_list.keys())

        def dfs(current, length, path):
            nonlocal best_path

            visited.append(current)
            path.append(current)
            if length == n-l and len(path) > len(best_path):
                best_path = path.copy()

            else:
                for vertex, cost in self.incident_list[current]:
                    if vertex not in visited:
                        dfs(vertex, length+cost, path)

            visited.remove(current)
            path.pop()

        while len(start_vertexes) != 0:
            start = random.choice(start_vertexes)
            start_vertexes.remove(start)
            dfs(start, 0, [])
        return best_path

    def random_data_generator(self, n, l, positive=0, negative=0):
        import random
        alphabet = ['A', 'C', 'G', 'T']
        random_dna = ""
        sequences = []

        for _ in range(n):
            random_dna += random.choice(alphabet)

        for i in range(len(random_dna)-l+1):
            sequences.append(random_dna[i:i+l])

        random.shuffle(sequences)
        sequences = sequences[negative:]

        for _ in range(positive):
            random_seq = ""
            for _ in range(l):
                random_seq += random.choice(alphabet)
            sequences.append(random_seq)

        random.shuffle(sequences)
        self.load_data(sequences)

        return random_dna

    def calculate_errors(self, n, l, best_path):
        negative = (n - l + 1) - len(best_path)
        positive = len(self.incident_list.keys()) - len(best_path)

        return positive, negative