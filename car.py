from math import cos, radians, sin

class Car:
    """
    Represent a car with a position and a heading.

    Attributes:
        x (float): The x coordinate. Increases to the east.
        y (float): The y coordinate. Increases to the south.
        heading (float): Direction in degrees. 0 is north, 90 is east.
    """

    def __init__(self, x=0.0, y=0.0, heading=0.0):
        """
        Initialize a Car with a starting position and heading.

        Args:
            x (float): Starting x coordinate. Default 0.0.
            y (float): Starting y coordinate. Default 0.0.
            heading (float): Starting heading in degrees. Default 0.0.

        Side effects:
            Sets self.x, self.y, and self.heading.
        """
        self.x = x
        self.y = y
        self.heading = heading

    def turn(self, degrees):
        """
        Turn the car by a given number of degrees.

        Positive degrees turns clockwise.
        Negative degrees turns counterclockwise.

        Args:
            degrees (float): Degrees to turn.

        Side effects:
            Updates self.heading to stay in the range [0, 360).
        """
        self.heading = (self.heading + degrees) % 360

    def drive(self, distance):
        """
        Drive forward a given distance based on the current heading.

        Args:
            distance (float): Distance to drive.

        Side effects:
            Updates self.x and self.y.
        """
        heading_radians = radians(self.heading)

        # x increases to the east, so add the east-west component.
        self.x += distance * sin(heading_radians)

        # y increases to the south, so subtract the north-south component.
        self.y -= distance * cos(heading_radians)


def sanity_check():
    """
    Create a Car, perform a fixed sequence of moves, and print results.

    Returns:
        Car: The Car instance created and moved.

    Side effects:
        Prints the final location and heading to the console.
    """
    car = Car()

    car.turn(90.0)
    car.drive(10.0)
    car.turn(30.0)
    car.drive(20.0)

    print(f"Location: {car.x}, {car.y}")
    print(f"Heading: {car.heading}")

    return car


if __name__ == "__main__":
    sanity_check()