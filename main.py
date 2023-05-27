from Graph import Graph
import urllib.request
import time


def get_data_from_web(instance):
    """
    Function for getting data from page http://www.cs.put.poznan.pl/mkasprzak/bio/ins/
    :param instance: instance name
    :return: data in list form
    """
    url = "http://www.cs.put.poznan.pl/mkasprzak/bio/ins/" + instance
    resource = urllib.request.urlopen(url)
    data = resource.read().decode('utf-8').split('\n')
    data.remove("")

    return data


def main():
    # Open instances file
    with open("instances.txt") as f:
        instances_name = [instance_name[:-1] for instance_name in f.readlines()]

    print("Nazwa instancji", "Czas trwania algorytmu", "Znalezione błędy pozytywne", "Oczekiwane błędy pozytywne",
          "Znalezione błędy negatywne", "Oczekiwane błędy negatywne", sep="\t")
    for name in instances_name:
        # Get data from web
        data = get_data_from_web(name)

        # Calculate l
        l = len(data[0])

        # Set default value
        positive = "-"
        negative = "-"

        # Calculate errors and n
        if '+' in name:
            n = int(name.split('.')[1].split('+')[0]) + l - 1
            positive = name.split('.')[1].split('+')[1]
        elif '-' in name:
            n = int(name.split('.')[1].split('-')[0]) + l - 1
            negative = name.split('.')[1].split('-')[1]

        calculation_time, positive_errors_detected, negative_errors_detected = calculate_time(data, n, l)

        print(name, calculation_time, positive_errors_detected, positive, negative_errors_detected, negative)


def calculate_time(data, n, l):
    G = Graph()
    G.load_data(data)

    start_time = time.time()
    best_path = G.shortest_cycle_path(n, l)
    end_time = time.time()

    pos, neg = G.calculate_errors(n, l, best_path)

    return end_time - start_time, pos, neg


if __name__ == "__main__":
    main()
