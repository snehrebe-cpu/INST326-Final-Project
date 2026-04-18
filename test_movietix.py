import sys
import test_movietix as mt

def ticket_price(age: int) -> int:
    """Return ticket price (USD) based on age."""
    return (5 if age <= 12 else
            8 if age <= 64 else
            6)

if __name__ == "__main__":
    try:
        age = int(sys.argv[1])
    except IndexError:
        print("Please provide your age as a command-line argument")
    except ValueError:
        print("Please provide your age as an integer as the first command-line argument")
    else:
        print("You would pay", ticket_price(age), "dollars")
        
def test_ticket_price_happy_path():
    assert mt.ticket_price(10) == 5
    assert mt.ticket_price(30) == 8
    assert mt.ticket_price(70) == 6

def test_ticket_price_edge_cases():
    assert mt.ticket_price(12) == 5
    assert mt.ticket_price(13) == 8
    assert mt.ticket_price(64) == 8
    assert mt.ticket_price(65) == 6