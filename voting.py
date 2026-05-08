

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
vote_data = os.path.join(BASE_DIR, "vote_data.txt")
id_data = os.path.join(BASE_DIR, "id_data.txt")

parties = [
    "BJP",
    "Congress",
    "AAP",
    "BSP",
    "CPI(M)",
    "CPI",
    "TMC",
    "RJD",
    "NPP",
    "LJP"
]

voted_id = []


def _load_voted_ids() -> set[str]:
    if not os.path.exists(id_data):
        return set()
    with open(id_data, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f.read().splitlines() if line.strip())


def cast_vote(*, name: str, voter_id: str, choice: int) -> str:
    """
    Records a vote for the selected party and stores voter_id to prevent re-voting.
    Returns selected party name on success.
    Raises ValueError for validation errors.
    """
    voter_id = (voter_id or "").strip()
    name = (name or "").strip()

    if len(voter_id) != 16:
        raise ValueError("Wrong ID (ID must be exactly 16 characters).")

    voted_ids = _load_voted_ids()
    if voter_id in voted_ids:
        raise ValueError("You already voted.")

    if not (1 <= choice <= len(parties)):
        raise ValueError("Invalid choice.")

    party = parties[choice - 1]

    with open(vote_data, "a", encoding="utf-8") as f:
        f.write(party + "\n")

    with open(id_data, "a", encoding="utf-8") as f:
        f.write(voter_id + "\n")

    return party


def get_results() -> dict[str, int]:
    if not os.path.exists(vote_data):
        return {p: 0 for p in parties}
    with open(vote_data, "r", encoding="utf-8") as f:
        votes = [line.strip() for line in f.read().splitlines() if line.strip()]
    return {p: votes.count(p) for p in parties}


def run_cli() -> None:
    voted_ids = _load_voted_ids()

    name = input("Enter name : ")
    voter_id = input("Enter ID : ")

    if len(voter_id) != 16:
        print("Wrong ID")
        return

    if voter_id in voted_ids:
        print("You already voted")
        return

    print("\n--- VOTE LIST ---")
    for i in range(len(parties)):
        print(i + 1, parties[i])

    print(f"{len(parties) + 1} RESULT")

    try:
        choice = int(input("Enter choice : "))
    except ValueError:
        print("Invalid choice")
        return

    if choice == len(parties) + 1:
        results = get_results()
        if all(v == 0 for v in results.values()):
            print("No votes yet")
            return

        print("\n--- RESULTS ---")
        for p in parties:
            print(p, ":", results[p])
        return

    try:
        party = cast_vote(name=name, voter_id=voter_id, choice=choice)
        print("Vote saved for", party)
        print("Thank you", name)
    except ValueError as e:
        print(str(e))


if __name__ == "__main__":
    run_cli()
