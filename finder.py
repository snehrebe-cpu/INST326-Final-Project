import sys
import argparse

HOME_DATABASE = """shoes,floor,8/23/23,10:00am
papers,cubbard,7/23/23,1:00am
picture frames,wall,6/23/23,10:00pm
tshirts,cubbard,1/13/23,9:00am
soccer balls,basket,2/9/22,12:00pm
kitchen tables,floor,3/23/23,4:00pm
cabinets,corner,5/30/23,10:30pm"""

def main(name):
    rows = HOME_DATABASE.split("\n")

    for row in rows:

        parts = row.split(",")

        item_name = parts[0]
        location = parts[1]
        date_last_moved = parts[2]
        time_last_moved = parts[3]

        if item_name == name:
            return f"The {item_name} were found in the {location} and were placed there on {date_last_moved} at {time_last_moved}"

    raise ValueError(f"Sorry, could not find your item named {name} within the database")
pass

def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command promptg
        
    Returns:
        args (ArgumentParser)
    """
    parser = argparse.ArgumentParser() 
  
    parser.add_argument('object', type=str, help="Please enter the name that we are searching for.")
    
    args = parser.parse_args(args_list) 
    
    return args

if __name__ == "__main__":
    arguments = parse_args(sys.argv[1:]) 
    print(main(arguments.object))