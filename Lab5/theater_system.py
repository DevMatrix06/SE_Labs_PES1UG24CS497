"""Seat reservation system for a small movie theater."""
import json
import hashlib

# Global state
shows = {"SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
         "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []}}

def reserve_seat(show_id, seat_number, system_logs=None):
    """Reserve seat_number (1..seats) for show_id; return True if it was booked."""
    if system_logs is None:
        system_logs = []
    show = shows.get(show_id)
    if show is None:
        system_logs.append(f"Unknown show {show_id}")
        return False
    if not isinstance(seat_number, int) or not 1 <= seat_number <= show["seats"]:
        system_logs.append(f"Invalid seat {seat_number} for {show_id}")
        return False
    if seat_number in show["booked"]:
        system_logs.append(f"Seat {seat_number} already taken for {show_id}")
        return False
    show["booked"].append(seat_number)
    system_logs.append(f"Reserved seat {seat_number} for {show_id}")
    return True

def release_seat(show_id, seat_number):
    """Free a booked seat; return False if the show or booking does not exist."""
    try:
        shows[show_id]["booked"].remove(seat_number)
    except (KeyError, ValueError):
        return False
    return True

def ticket_code(show_id, seat_number):
    """Return a short ticket code derived from the show and seat."""
    return hashlib.sha256((show_id + str(seat_number)).encode()).hexdigest()[:8]

def dump_reservations(file="seats.json"):
    """Save all shows and their bookings to a JSON file."""
    with open(file, "w", encoding="utf-8") as f:
        json.dump(shows, f)

def load_reservations(file="seats.json"):
    """Replace the in-memory shows with the contents of a JSON file."""
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    shows.clear()
    shows.update(data)

def print_seating_summary():
    """Print the free seat count and booked seats for every show."""
    for show in shows.values():
        free = show["seats"] - len(show["booked"])
        print(f"{show['title']}: {free} seats free, booked = {show['booked']}")

def main():
    """Run a demo booking session and persist the result."""
    logs = []
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 5, logs)
    reserve_seat("SHOW-1", 25, logs)
    reserve_seat("SHOW-2", -1, logs)
    reserve_seat("SHOW-2", "A7", logs)
    release_seat("SHOW-2", 3)
    print("Ticket code:", ticket_code("SHOW-1", 5))
    raw = input("Seat number to book for SHOW-2 (Enter for 4): ").strip() or "4"
    try:
        reserve_seat("SHOW-2", int(raw), logs)
    except ValueError:
        logs.append(f"Invalid seat {raw} for SHOW-2: not a number")
    dump_reservations()
    load_reservations()
    print_seating_summary()
    print("\n".join(logs))

if __name__ == "__main__":
    main()
