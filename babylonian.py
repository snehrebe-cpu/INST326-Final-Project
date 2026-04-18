"""Use the Babylonian method to approximate the square root of a positive
number."""

from argparse import ArgumentParser
import sys

def sqrt_b(s, p=1e-10):
    """Approximate the square roof of a positive number
    
    Args:
    s = number that we weant to square root
    p = precision value
    x = appriximation of the square root
    
    Returns:
        y = square root value 
    """
    x = 2
    y = (x + s/ x) / 2
    
    x = s / 2 if s > 1 else 1.0
    
    while s > 0: 
        y = (x + s / x) / 2
        if abs (y-x) < p:
            return y 
        x = y

def parse_args(arglist):
    """Parse command-line arguments.
    
    Expect one required argument (a positive number whose square root the user
    wants to calculate) and one optional parameter (a precision, specified by
    the short flag -p or the long flag --precision). Both values
    are floats. The default precision is 0.0000000001 (1e-10).
    
    Args:
        arglist (list of str): list of command-line arguments.
        
    Returns:
        namespace: a namespace with attributes "number" and "precision". The
        value of each of these attributes will be a float.
    """
    parser = ArgumentParser()
    parser.add_argument("number", type=float,
                        help="number to compute the square root of")
    parser.add_argument("-p", "--precision", type=float, default=0.0000000001)
    return parser.parse_args(arglist)


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    print(f"The square root of {args.number} is approximately"
          f" {sqrt_b(args.number, args.precision)}")
