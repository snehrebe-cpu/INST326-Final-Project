"""Create routes between cities on a map."""
import sys
import argparse

class City:
    """
    Represent a city node in a map graph.
    
    Attributes:
        name (str): The name of the city.
        neighbors (dict): Dictionary where keys are City objects and
        values are tuples containing (distance:int, interstate:str).
    """
    def __init__(self, name):
        """
        Initialize a City object.
        
        Args:
            name (str): The name of the city.
        Side effects:
            Creates an empty neighbors dictionary.
        """
        self.name = name
        self.neighbors = {}

    def __repr__(self):
        """
        Return the string representation of the city.
        
        Returns:
            str: The city name.
        """
        return self.name
    
    def add_neighbor(self, neighbor, distance, interstate):
        """
        Connect this city with another city.
        
        Args:
            neighbor (City): Neighboring city.
            distance (int): Distance between cities.
            interstate (str): Interstate connecting the cities.
        Side effects:
            Adds both cities to each other's neighbor dictionaries.
        """
        if neighbor not in self.neighbors:
            self.neighbors[neighbor] = (distance, interstate)
        if self not in neighbor.neighbors:
            neighbor.neighbors[self] = (distance, interstate)

class Map:
    """
    Represent a graph of cities connected by roads.
    
    Attributes:
        cities (list): List of City objects in the map.
    """

    def __init__(self, relationships):
        """
        Initialize the Map from an adjacency list dictionary.
        
        Args:
            relationships (dict): Dictionary describing city connections.
        Side effects:
            Creates City objects and connects them using add_neighbor().
        """
        self.cities = []
        for city_name in relationships:
            if city_name not in [city.name for city in self.cities]:
                self.cities.append(City(city_name))
            city_index = [city.name for city in self.cities].index(city_name)
            city_obj = self.cities[city_index]
            for neighbor_name, distance, interstate in relationships[city_name]:
                if neighbor_name not in [city.name for city in self.cities]:
                    self.cities.append(City(neighbor_name))
                neighbor_index = [
                    city.name for city in self.cities
                ].index(neighbor_name)
                neighbor_obj = self.cities[neighbor_index]
                city_obj.add_neighbor(neighbor_obj, distance, interstate)

    def __repr__(self):
        """
        Return string representation of the map.
        
        Returns:
            str: List of cities.
        """
        return str(self.cities)

def bfs(graph, start, goal):
    """
    Perform Breadth First Search to find shortest path.
    
    Args:
        graph (Map): Map object representing the city graph.
        start (str): Starting city.
        goal (str): Destination city.
    Returns:
        list: List of city names representing the shortest route.
    """
    explored = []
    queue = [[start]]
    while queue:
        path = queue.pop(0)
        node = path[-1]
        if node not in explored:
            city_obj = None
            for city in graph.cities:
                if city.name == node:
                    city_obj = city
                    break
            neighbors = city_obj.neighbors
            for neighbor in neighbors:
                new_path = list(path)
                new_path.append(str(neighbor))
                queue.append(new_path)
                if str(neighbor) == goal:
                    return [str(city) for city in new_path]
            explored.append(node)
    print("No path found")
    return None

def main(start, destination, connections):
    """
    Generate driving instructions between two cities.
    
    Args:
        start (str): Starting city.
        destination (str): Destination city.
        connections (dict): Graph adjacency list.
    Returns:
        str: Driving instructions.
    """
    road_map = Map(connections)
    instructions = bfs(road_map, start, destination)
    output = ""
    try:
        for index, city in enumerate(instructions):
            if index == 0:
                line = f"Starting at {city}"
                print(line)
                output += line + "\n"
            if index < len(instructions) - 1:
                next_city = instructions[index + 1]
                city_obj = None
                for c in road_map.cities:
                    if c.name == city:
                        city_obj = c
                        break
                neighbors = {str(k): v for k, v in city_obj.neighbors.items()}
                distance, interstate = neighbors[next_city]
                line = (
                    f"Drive {distance} miles on {interstate} "
                    f"towards {next_city}, then"
                )
                print(line)
                output += line + "\n"
            else:
                line = "You will arrive at your destination"
                print(line)
                output += line
        return output
    except Exception:
        sys.exit()

def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """

    parser = argparse.ArgumentParser()
    
    parser.add_argument('--starting_city', type = str, help = 'The starting city in a route.')
    parser.add_argument('--destination_city', type = str, help = 'The destination city in a route.')
    
    args = parser.parse_args(args_list)
    
    return args

if __name__ == "__main__":
    
    connections = {  
        "Baltimore": [("Washington", 39, "95"), ("Philadelphia", 106, "95")],
        "Washington": [("Baltimore", 39, "95"), ("Fredericksburg", 53, "95"), ("Bedford", 137, "70"), ("Philadelphia", 139, "95")], 
        "Fredericksburg": [("Washington", 53, "95"), ("Richmond", 60, "95")],
        "Richmond": [("Charlottesville", 71, "64"), ("Williamsburg", 51, "64"), ("Durham", 151, "85"), ("Fredericksburg", 60, "95"), ("Raleigh", 171, "95")],
        "Durham": [("Richmond", 151, "85"), ("Raleigh", 29, "40"), ("Greensboro", 54, "40")],
        "Raleigh": [("Durham", 29, "40"), ("Wilmington", 129, "40"), ("Richmond", 171, "95")],
        "Greensboro": [("Charlotte", 92, "85"), ("Durham", 54, "40"), ("Ashville", 173, "40")],
        "Ashville": [("Greensboro", 173, "40"), ("Charlotte", 130, "40"), ("Knoxville", 116, "40"), ("Atlanta", 208, "85")],
        "Charlotte": [("Atlanta", 245, "85"), ("Ashville", 130, "40"), ("Greensboro", 92, "85")],
        "Jacksonville": [("Atlanta", 346, "75"), ("Tallahassee", 164, "10"), ("Daytona Beach", 86, "95")],
        "Daytona Beach": [("Orlando", 56, "4"), ("Miami", 95, "268"), ("Jacksonville", 86, "95")],
        "Orlando": [("Tampa", 94, "4"), ("Daytona Beach", 56, "4")],
        "Tampa": [("Miami", 281, "75"), ("Orlando", 94, "4"), ("Atlanta", 456, "75"), ("Tallahassee", 243, "98")],
        "Atlanta": [("Charlotte", 245, "85"), ("Ashville", 208, "85"), ("Chattanooga", 118, "75"), ("Macon", 83, "75"), ("Tampa", 456, "75"), ("Jacksonville", 346, "75"), ("Tallahassee", 273, "27") ],
        "Chattanooga": [("Atlanta", 118, "75"), ("Knoxville", 112, "75"), ("Nashville", 134, "24"), ("Birmingham", 148, "59")],
        "Knoxville": [("Chattanooga", 112,"75"), ("Lexington", 172, "75"), ("Nashville", 180, "40"), ("Ashville", 116, "40")],
        "Nashville": [("Knoxville", 180, "40"), ("Chattanooga", 134, "24"), ("Birmingam", 191, "65"), ("Memphis", 212, "40"), ("Louisville", 176, "65")],
        "Louisville": [("Nashville", 176, "65"), ("Cincinnati", 100, "71"), ("Indianapolis", 114, "65"), ("St. Louis", 260, "64"), ("Lexington", 78, "64") ],
        "Cincinnati": [("Louisville", 100, "71"), ("Indianapolis", 112, "74"), ("Columbus", 107, "71"), ("Lexington", 83, "75"), ("Detroit", 263, "75")],
        "Columbus": [("Cincinnati", 107, "71"), ("Indianapolis", 176, "70"), ("Cleveland", 143, "71"), ("Pittsburgh", 185, "70")],
        "Detroit": [("Cincinnati", 263, "75"), ("Chicago", 282, "94"), ("Mississauga", 218, "401")],
        "Cleveland":[("Chicago", 344, "90"), ("Columbus", 143, "71"), ("Youngstown", 75, "80"), ("Buffalo", 194, "90")],
        "Youngstown":[("Pittsburgh", 67, "76"), ("Cleveland", 75, "80")],
        "Indianapolis": [("Columbus", 176, "70"), ("Cincinnati", 112, "74"), ("St. Louis", 242, "70"), ("Chicago", 182, "65"), ("Louisville", 114, "65"), ("Mississauga", 498, "401")],
        "Pittsburgh": [("Columbus", 185, "70"), ("Youngstown", 67, "76"), ("Philadelphia", 305, "76"), ("New York", 389, "76"), ("Bedford", 107, "76")],
        "Bedford": [("Pittsburgh", 107, "76"), ("Washington", 137, "70")], 
        "Chicago": [("Indianapolis", 182, "65"), ("St. Louis", 297, "55"), ("Milwaukee", 92, "94"), ("Detroit", 282, "94"), ("Cleveland", 344, "90")],
        "New York": [("Philadelphia", 95, "95"), ("Albany", 156, "87"), ("Scranton", 121, "80"), ("Providence", 95, "181"), ("Pittsburgh", 389, "76")],
        "Scranton": [("Syracuse", 130, "81"), ("New York", 121, "80")],
        "Philadelphia": [("Washington", 139, "95"), ("Pittsburgh", 305, "76"), ("Baltimore", 106, "95"), ("New York", 95, "95")]
    }
    
    args = parse_args(sys.argv[1:])
    main(args.starting_city, args.destination_city, connections)