"""Use the Babylonian method to approximate the square root of a positive
number."""


from argparse import ArgumentParser
import sys


# Replace this comment with your implementation of the sqrt_b() function.


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
