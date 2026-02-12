import json
import threading
import time

DATA_FILE = "data.json"
lock = threading.Lock()


def load_data():
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_available_seats():
    data = load_data()
    return [seat for seat, user in data["seats"].items() if user is None]


def book_specific_seat(user_id, seat_number):
    with lock:
        data = load_data()

        seat_number = str(seat_number)

        # Seat existence
        if seat_number not in data["seats"]:
            return f"Seat {seat_number} does not exist."

        # Prevent double booking by same user
        if user_id in data["seats"].values():
            return f"User {user_id} already has a booking."

        # Seat availability
        if data["seats"][seat_number] is not None:
            return f"Seat {seat_number} is already booked."

        # Simulate processing delay (real-world race condition)
        time.sleep(0.1)

        data["seats"][seat_number] = user_id
        save_data(data)

        return f"Seat {seat_number} successfully booked for user {user_id}."


def cancel_booking(user_id):
    with lock:
        data = load_data()

        for seat, user in data["seats"].items():
            if user == user_id:
                data["seats"][seat] = None
                save_data(data)
                return f"Booking for user {user_id} on seat {seat} cancelled."

        return f"No booking found for user {user_id}."


def show_seat_map():
    data = load_data()
    for seat, user in sorted(data["seats"].items(), key=lambda x: int(x[0])):
        status = "Available" if user is None else f"Booked by {user}"
        print(f"Seat {seat}: {status}")
