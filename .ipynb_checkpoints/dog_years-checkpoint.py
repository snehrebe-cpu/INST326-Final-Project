import sys


def dog_years(age):
    # year 1 -> 15 years
    # year 2 -> 9 years
    # year 3+ -> 5 years each
    return (
        0 if age == 0 else
        15 if age == 1 else
        24 if age == 2 else 24 + 5 * (age - 2)
    )
    
    
if __name__ == "__main__":
    age = int(sys.argv[1])
    human_age = dog_years(age)
    print(f"a {age}-year-old dog is equivalent to a {human_age}-year-old"
          f" person")