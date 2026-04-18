"""Determine how two people in a family are related.

Do: read a JSON family dataset, build people and connections, then print
the kinship term for two given names using the lowest common relative (LCR).

Attributes:
    (none)
"""

from __future__ import annotations
import json
import sys
from argparse import ArgumentParser
from collections import deque
from typing import Dict, Iterable, List, Optional, Set, Tuple

try:
    from relationships import relationships as REL_MAP
except Exception as exc:
    raise RuntimeError(
        "Could not import relationships.relationships. Ensure relationships.py is in the same folder."
    ) from exc


class Person:
    """A person in the family dataset.

    Attributes:
        name (str): Unique identifier (also used as display name).
        gender (str): 'f', 'm', or 'n'.
        parents (List[Person]): List of this person's parents (0, 1, or 2).
        spouse (Optional[Person]): Spouse if any, else None.
    """

    def __init__(self, name: str, gender: str) -> None:
        """Initialize a Person.

        Args:
            name (str): Person's name.
            gender (str): 'f', 'm', or 'n'.

        Returns:
            None

        Side effects:
            Creates attributes: name, gender, parents (empty list), spouse (None).

        Raises:
            None
        """
        self.name: str = name
        self.gender: str = gender
        self.parents: List["Person"] = []   
        self.spouse: Optional["Person"] = None

    def __hash__(self) -> int:
        """Hash by name so Person can be used as a dict/set key.

        Args:
            (none)

        Returns:
            int: Hash of the person's name.

        Side effects:
            None

        Raises:
            None
        """
        return hash(self.name)

    def add_parent(self, parent: "Person") -> None:
        """Add a parent connection.

        Args:
            parent (Person): The parent to add.

        Returns:
            None

        Side effects:
            Appends to self.parents if not already present.

        Raises:
            None
        """
        if parent not in self.parents:
            self.parents.append(parent)

    def set_spouse(self, partner: "Person") -> None:
        """Set spouse connection (mutual).

        Args:
            partner (Person): The spouse to set.

        Returns:
            None

        Side effects:
            Sets self.spouse and partner.spouse.

        Raises:
            None
        """
        self.spouse = partner
        if partner.spouse is not self:
            partner.spouse = self

    def connections(self) -> Dict["Person", str]:
        """Return shortest paths from self to relatives via P/S edges.

        Do:
            Breadth-first search over the family graph where edges are:
              * to each parent ('P')
              * to a single spouse ('S'), used at most once in any path

        Args:
            (none)

        Returns:
            Dict[Person, str]: Mapping of reachable person → path string
            composed of 'P' and/or 'S'. Includes self mapped to "".

        Side effects:
            None

        Raises:
            None
        """
        q: deque[Tuple["Person", str]] = deque([(self, "")])
        seen: Dict["Person", str] = {self: ""}

        while q:
            current, path = q.popleft()

            def enqueue(nei: Optional["Person"], step: str) -> None:
                if nei is None:
                    return
                if step == "S" and path.count("S") >= 1:
                    return
                new_path = path + step
                if (nei not in seen) or (len(new_path) < len(seen[nei])):
                    seen[nei] = new_path
                    q.append((nei, new_path))
            for p in current.parents:
                enqueue(p, "P")
            enqueue(current.spouse, "S")

        return seen

    def relation_to(self, other: "Person") -> Optional[str]:
        """Return kinship term for how self is related to another person.

        Args:
            other (Person): The other person.

        Returns:
            Optional[str]: A kinship term (e.g., "aunt") or "distant relative"
            if the LCR path is not in REL_MAP; None if there is no shared relative.

        Side effects:
            None

        Raises:
            None
        """
        c1 = self.connections()
        c2 = other.connections()
        shared: Set["Person"] = set(c1.keys()) & set(c2.keys())
        if not shared:
            return None

        combos: Dict[str, int] = {f"{c1[r]}:{c2[r]}": len(c1[r]) + len(c2[r]) for r in shared}
        lcr_key = min(sorted(combos.keys()), key=lambda k: combos[k])

        terms = REL_MAP.get(lcr_key)
        if terms is None:
            return "distant relative"
        return terms.get(self.gender, "distant relative")


class Family:
    """A collection of Person objects and their relations.

    Attributes:
        people (Dict[str, Person]): Map of name → Person for all individuals.
    """

    def __init__(self, data: dict) -> None:
        """Initialize a Family from parsed JSON data.

        Args:
            data (dict): JSON-like dict with keys:
                - "individuals": {name: gender}
                - "parents": {child: [parent1, parent2, ...]}
                - "couples": [[nameA, nameB], ...]

        Returns:
            None

        Side effects:
            Creates Person objects, connects parent and spouse relationships.

        Raises:
            None
        """
        self.people: Dict[str, Person] = {}
        for name, gender in data.get("individuals", {}).items():
            self.people[name] = Person(name=name, gender=gender)

        for child, plist in data.get("parents", {}).items():
            child_obj = self.people.get(child)
            if not child_obj:
                continue
            for pname in plist:
                parent_obj = self.people.get(pname)
                if parent_obj:
                    child_obj.add_parent(parent_obj)

        for pair in data.get("couples", []):
            if not isinstance(pair, (list, tuple)) or len(pair) != 2:
                continue
            a, b = pair
            pa = self.people.get(a)
            pb = self.people.get(b)
            if pa and pb:
                pa.set_spouse(pb)

    def relation(self, name1: str, name2: str) -> Optional[str]:
        """Return kinship term for how name1 is related to name2.

        Args:
            name1 (str): The subject whose relation to name2 is requested.
            name2 (str): The reference person.

        Returns:
            Optional[str]: A term if both exist; "distant relative" may appear
            via Person.relation_to(); None if one or both names are unknown
            or there is no shared relative.

        Side effects:
            None

        Raises:
            None
        """
        p1 = self.people.get(name1)
        p2 = self.people.get(name2)
        if not p1 or not p2:
            return None
        return p1.relation_to(p2)


def main(filepath: str, name1: str, name2: str) -> None:
    """Read JSON, compute how name1 is related to name2, and print it.

    Args:
        filepath (str): Path to JSON family data (e.g., "family.json").
        name1 (str): Subject person (how this person is related to name2).
        name2 (str): Reference person.

    Returns:
        None

    Side effects:
        Prints one line to stdout in the format:
            "<name1> is not related to <name2>"
        or
            "<name1> is <name2>'s <term>"

    Raises:
        FileNotFoundError: If filepath does not exist.
        json.JSONDecodeError: If the JSON is malformed.
    """
    with open(filepath, "r", encoding="utf-8") as f:
        familydata = json.load(f)
    fam = Family(familydata)
    term = fam.relation(name1, name2)
    if term is None:
        print(f"{name1} is not related to {name2}")
    else:
        print(f"{name1} is {name2}'s {term}")


def parse_args(arglist: Iterable[str]):
    """Parse command-line arguments.

    Args:
        arglist (Iterable[str]): Arguments excluding the program name.

    Returns:
        argparse.Namespace: Parsed args with attributes:
            - filepath
            - name1
            - name2

    Side effects:
        None

    Raises:
        SystemExit: If required args are missing (raised by argparse).
    """
    parser = ArgumentParser()
    parser.add_argument("filepath", help="Path to JSON family data file (e.g., family.json)")
    parser.add_argument("name1", help="First person (how this person is related to name2)")
    parser.add_argument("name2", help="Second person")
    return parser.parse_args(list(arglist))


if __name__ == "__main__":
    args = parse_args(sys.argv[1:])
    main(args.filepath, args.name1, args.name2)