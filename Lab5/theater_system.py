import json
import os
import hashlib

# Global state
shows = {"SHOW-1": {"title": "Interstellar", "seats": 20, "booked": []},
         "SHOW-2": {"title": "Dangal", "seats": 10, "booked": []}}

def reserve_seat(show_id, seat_number, system_logs=[]):
    show = shows[show_id]
    if seat_number in show["booked"]:
        system_logs.append("Seat %s already taken for %s" % (seat_number, show_id))
        return False
    show["booked"].append(seat_number)
    system_logs.append("Reserved seat %s for %s" % (seat_number, show_id))
    return True

def release_seat(show_id, seat_number):
    try:
        shows[show_id]["booked"].remove(seat_number)
    except:
        pass

def ticket_code(show_id, seat_number):
    return hashlib.md5((show_id + str(seat_number)).encode()).hexdigest()[:8]

def dump_reservations(file="seats.json"):
    f = open(file, "w")
    f.write(json.dumps(shows))

def load_reservations(file="seats.json"):
    global shows
    f = open(file, "r")
    data = f.read()
    shows = json.loads(data)

def printSeatingSummary():
    for s in shows:
        free = shows[s]["seats"] - len(shows[s]["booked"])
        print(shows[s]["title"] + ": " + str(free) + " seats free, booked = " + str(shows[s]["booked"]))

def main():
    reserve_seat("SHOW-1", 5)
    reserve_seat("SHOW-1", 5)
    reserve_seat("SHOW-1", 25)
    reserve_seat("SHOW-2", -1)
    reserve_seat("SHOW-2", "A7")
    release_seat("SHOW-2", 3)
    print("Ticket code:", ticket_code("SHOW-1", 5))
    seat = input("Seat number to book for SHOW-2 (Enter for 4): ") or "4"
    reserve_seat("SHOW-2", seat)
    dump_reservations()
    load_reservations()
    printSeatingSummary()
    os.chmod("seats.json", 0o777)

main()
