import csv
import sys
import math

from util import Node, StackFrontier, QueueFrontier

# Maps names to a set of corresponding person_ids
names = {}

# Maps person_ids to a dictionary of: name, birth, movies (a set of movie_ids)
people = {}

# Maps movie_ids to a dictionary of: title, year, stars (a set of person_ids)
movies = {}


def load_data(directory):
    """
    Load data from CSV files into memory.
    """
    # Load people
    with open(f"{directory}/people.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            people[row["id"]] = {
                "name": row["name"],
                "birth": row["birth"],
                "movies": set()
            }
            if row["name"].lower() not in names:
                names[row["name"].lower()] = {row["id"]}
            else:
                names[row["name"].lower()].add(row["id"])

    # Load movies
    with open(f"{directory}/movies.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            movies[row["id"]] = {
                "title": row["title"],
                "year": row["year"],
                "stars": set()
            }

    # Load stars
    with open(f"{directory}/stars.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                people[row["person_id"]]["movies"].add(row["movie_id"])
                movies[row["movie_id"]]["stars"].add(row["person_id"])
            except KeyError:
                pass


def main():
    if len(sys.argv) > 2:
        sys.exit("Usage: python degrees.py [directory]")
    directory = sys.argv[1] if len(sys.argv) == 2 else "large"

    # Load data from files into memory
    print("Loading data...")
    load_data(directory)
    print("Data loaded.")

    source = person_id_for_name(input("Name: "))
    if source is None:
        sys.exit("Person not found.")
    target = person_id_for_name(input("Name: "))
    if target is None:
        sys.exit("Person not found.")

    path = shortest_path(source, target)

    if path is None:
        print("Not connected.")
    else:
        degrees = len(path)
        print(f"{degrees} degrees of separation.")
        path = [(None, source)] + path
        for i in range(degrees):
            person1 = people[path[i][1]]["name"]
            person2 = people[path[i + 1][1]]["name"]
            movie = movies[path[i + 1][0]]["title"]
            print(f"{i + 1}: {person1} and {person2} starred in {movie}")


def check_if_goal(node, target):
    # If this is the target we seek
    # Add the path to target to solutions list
    if node.state == target:
        path = []
        targetNode = node
        while targetNode.parent is not None:
            path.append(targetNode.action)
            targetNode = targetNode.parent
        path.reverse()
        return path
    return None

def shortest_path(source, target):
    """
    Returns the shortest list of (movie_id, person_id) pairs
    that connect the source to the target.

    If no possible path, returns None.
    """

    # Set source as root node
    start = Node(state=source, parent=None, action=None)

    # Initialize frontier with a Queue.
    # We use breadth-first search and hence a queue to ensure
    # that we find the most optimal (shortest) solution
    
    frontier = StackFrontier()
    
    # Set of visited nodes
    explored_people = set()

    # List of solutions
    solutions = []

    goal = check_if_goal(start, target)

    if goal is not None: 
        return goal

    # Add root node to frontier
    frontier.add(start)

    # Repeat until frontier is empty
    while True:
        if frontier.empty():
            break
        # Get the first node in the queue
        node = frontier.remove()
        # Mark the current node as explored by adding it to explored set
        explored_people.add(node.state)

        if len(explored_people) % 1000 == 0:
            print(len(explored_people))
        
        # Add node's neighbors to frontier
        for movie, person in neighbors_for_person(node.state):
            if person is not node.state and not frontier.contains_state(
                    person) and person not in explored_people:
                Child = Node(state=person, parent=node, action=(movie, person))
                path = check_if_goal(Child, target)
                if path is not None:
                    explored_people.add(Child.state)
                    solutions.append(path)
                else:
                    frontier.add(Child)

    # If we have 0 solutions return None
    if len(solutions) == 0:
        return None
    # Otherwise loop through all solutions and return one of the shortest ones
    else:
        shortest_distance = None
        for path in solutions:
            if shortest_distance is None or \
               len(shortest_distance) >= len(path):
                shortest_distance = path
        return shortest_distance


def person_id_for_name(name):
    """
    Returns the IMDB id for a person's name,
    resolving ambiguities as needed.
    """
    person_ids = list(names.get(name.lower(), set()))
    if len(person_ids) == 0:
        return None
    elif len(person_ids) > 1:
        print(f"Which '{name}'?")
        for person_id in person_ids:
            person = people[person_id]
            name = person["name"]
            birth = person["birth"]
            print(f"ID: {person_id}, Name: {name}, Birth: {birth}")
        try:
            person_id = input("Intended Person ID: ")
            if person_id in person_ids:
                return person_id
        except ValueError:
            pass
        return None
    else:
        return person_ids[0]


def neighbors_for_person(person_id):
    """
    Returns (movie_id, person_id) pairs for people
    who starred with a given person.
    """
    movie_ids = people[person_id]["movies"]
    neighbors = set()
    for movie_id in movie_ids:
        for person_id in movies[movie_id]["stars"]:
            neighbors.add((movie_id, person_id))
    return neighbors


if __name__ == "__main__":
    main()
