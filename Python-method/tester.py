from Graph import Graph

n = 10
l = 3
negative = 2
positive = 1


def validate_path(path, ideal_path):
    print("This is cost between two vertexes in result sequences:")
    for i in range(len(path)-1):
        element_start = path[i]
        element_end = path[i+1]
        element_start_label = element_start.split("-")[0]
        element_end_label = element_end.split("-")[0]

        jump_cost = len(element_start_label)
        for j in range(len(element_start_label)-1, 0, -1):
            if element_start_label[-j:] == element_end_label[:j]:
                jump_cost = len(element_start_label)-j
                break

        print(element_start_label, f"-{jump_cost}->", element_end_label)

    print("\nCompare two DNA:")
    print("DNA from algorithm:\t", end="")
    alg_dna = []
    for element in path:
        alg_dna.append(element.split("-")[0])
        print(element.split("-")[0], end=" ")
    print()

    ideal_dna = []
    print("Ideal DNA:\t\t\t", end="")
    for i in range(len(ideal_path)-l+1):
        ideal_dna.append(ideal_path[i:i+l])
        print(ideal_path[i:i+l], end=" ")
    print()

    print(end="\t\t\t\t\t")
    for ideal, alg in zip(ideal_dna, alg_dna):
        if ideal == alg:
            print("\t", end="")
        else:
            print(" ^  ", end="")
    print()


def main():
    G = Graph()
    random_dna = G.random_data_generator(n, l, negative = negative, positive=positive)
    print(G)
    path = G.shortest_cycle_path(n, l)
    print("-"*20)
    validate_path(path, random_dna)

    pos, neg = G.calculate_errors(n, l, path)
    print("Obliczone błędy negatywne", neg)
    print("Obliczone błędy pozytywne", pos)


if __name__ == "__main__":
    main()
