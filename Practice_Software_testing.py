import sys
import Practice_Software_testing as fp
from math import isclose

def faculty_parking(income):
    """ Determine the cost of faculty parking based on a faculty member's annual salary. """
    return (494 if income < 30_001 else
            559 if income < 45_001 else
            627 if income < 60_001 else
            932 if income < 80_001 else
            986)

if __name__ == "__main__":
    try:
        income = int(sys.argv[1])
    except IndexError:
        print("Please provide your income as a command-line argument")
        raise SystemExit(1)
    except ValueError:
        print("Please provide your income as an integer as the first command-line argument")
        raise SystemExit(1)

    print("You would pay", faculty_parking(income), "for an annual parking pass")

def test_faculty_parking_happy_path():
    """ some happy path cases to test faculty_parking() """
    assert fp.faculty_parking(25_000) == 494
    assert fp.faculty_parking(40_000) == 559
    assert fp.faculty_parking(50_000) == 627
    assert fp.faculty_parking(70_000) == 932
    assert fp.faculty_parking(90_000) == 986

def test_faculty_parking_edge_cases():
    """ some edge cases to test faculty_parking() """
    assert fp.faculty_parking(30_000) == 494
    assert fp.faculty_parking(30_001) == 559

def test_float_comparison():
    assert isclose(1/3, (10/3)/10)