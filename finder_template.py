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

        item = parts[0]
        location = parts[1]
        date = parts[2]
        time = parts[3]

        if item == name:
            return f"The {item} were found in the {location} and were placed there on {date} at {time}"

    raise ValueError(f"Sorry, could not find your item named {name} within the database")
    pass

def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as arguments
    
    Args:
        args_list (list) : the list of strings from the command promptg
        
    Returns:
        args (ArgumentParser)
    """
    #For the sake of readability it is important to insert comments all throughout.
    #Complicated operations get a few lines of comments before the operations commence.
    #Non-obvious ones get comments at the end of the line.
    #For example:
    #This function uses the argparse module in order to parse command line arguments.
    parser = argparse.ArgumentParser() #Create an ArgumentParser object.
    
    #Then we will add arguments to this parser object.
    #In this case, we have a required positional argument.
    #Followed by an optional keyword argument which contains a default value.
    parser.add_argument('object', type=str, help="Please enter the name that we are searching for.")
    
    args = parser.parse_args(args_list) #We need to parse the list of command line arguments using this object.
    
    return args

if __name__ == "__main__":
    
    #If name == main statements are statements that basically ask:
    #Is the current script being run natively or as a module?

    #It the script is being run as a module, the block of code under this will not beexecuted.
    #If the script is being run natively, the block of code below this will be executed.

    arguments = parse_args(sys.argv[1:]) #Pass in the list of command line arguments to the parse_args function.
    
    #The returned object is an object with those command line arguments as attributes of an object.
    #We will pass both of these arguments into the main function.
    #Note that you do not need a main function, but you might find it helpfull.
    #You do want to make sure to have minimal code under the 'if __name__ == "__main__":' statement.

    print(main(arguments.object))