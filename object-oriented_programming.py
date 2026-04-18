from pathlib import Path

class TaskBoard:
    def __init__(self, name: str, base: str = "."):
        self.name = name
        self.root = Path(base) / name        # uses Path and "/" join
        self.teammates: dict[str, "TaskBoard"] = {}
        self.inbox: list[tuple[str, str]] = []

    def add_teammate(self, other: "TaskBoard") -> None:
        self.teammates[other.name] = other

    def receive(self, sender: "TaskBoard", task: str) -> None:
        self.inbox.append((sender.name, task))

    def assign(self, who: str, task: str) -> None:
        if who not in self.teammates:
            raise ValueError(f"{who!r} not in teammates")
        self.teammates[who].receive(self, task)

    def read_tasks(self) -> None:
        if not self.inbox:
            print("No new tasks.")
            return
        for sender, text in self.inbox:
            print(f"Task from {sender}: {text}")
        self.inbox = []

if __name__ == "__main__":
    # pathlib.Path features on this script
    script = Path(__file__)
    print("name:", script.name, "suffix:", script.suffix, "parent:", script.parent)
    print("exists?", script.exists())
    print("py files here:", [p.name for p in script.parent.glob("*.py")])

    # Use the class
    a = TaskBoard("Alice")
    b = TaskBoard("Bob")
    a.add_teammate(b); b.add_teammate(a)
    a.assign("Bob", "Review PR #42.")
    a.assign("Bob", "Draft sprint notes.")
    b.read_tasks()