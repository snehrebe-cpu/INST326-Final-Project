import rpn

def evaluate(expr):
    """ Evaluate a postfix expression from a file and return the results 
    
    Args: 
        expr (str): string containing a postfix expression
    Returns: 
        float: returns the floated value of the expression
    """
    stack = []
    tokens = expr.strip().split()
    
    for token in tokens:
        try:
            stack.append(float(token))
        except ValueError:
            y = stack.pop()
            x = stack.pop()
            if token == "+":
                stack.append(x + y)
            elif token == "-":
                stack.append(x - y)
            elif token == "*":
                stack.append(x * y)
            elif token == "/":
                stack.append(x / y)
    return stack.pop()

def main(filename):
    """ Read the postfix expressions from a file 
    
    Args: 
        filename (str): specifies file with the post fix expressions
    
    Side effects: 
        prints the expressions and their results
    """
    with open(filename, "r", encoding="utf-8") as infile:
        for line in infile:
            line = line.strip()
            if line:
                result = evaluate(line)
                print(f"{line} = {result}")


    
def parse_args(arglist):
    """ Process command line arguments.
    
    Expect one mandatory argument (a file containing postfix expressions).
    
    Args:
        arglist (list of str): arguments from the command line.
    
    Returns:
        namespace: the parsed arguments, as a namespace.
    """
    parser = ArgumentParser()
    parser.add_argument("file", help="file containing reverse polish notation")
    args = parser.parse_args(arglist)
    return args


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.file)
