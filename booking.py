import json
import threading
import time
import os

DATA_FILE = "data.json"
lock = threading.Lock()


def initialize_data(total_seats=10):
    if not os.path.exists(DATA_FILE):
        data = {
            "event_id": "EVT1001",
            "total_seats": total_seats,
            "seats": {str(i): None for i in range(1, total_seats + 1)}
        }
        with open(DATA_FILE, "w") as f:
            json.dump(data, f, indent=4)


def load_data():
    initialize_data()
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)


def get_available_seats():
    data = load_data()
    return [seat for seat, user in data["seats"].items() if user is None]


def book_seat(user_id):
    """Auto-assign first available seat"""
    with lock:
        data = load_data()

        if user_id in data["seats"].values():
            return f"User {user_id} already has a booking."

        for seat, user in data["seats"].items():
            if user is None:
                data["seats"][seat] = user_id
                save_data(data)
                return f"Seat {seat} successfully booked for user {user_id}."

        return "No seats available."


def book_specific_seat(user_id, seat_number):
    """User-selected seat booking with race-condition protection"""
    with lock:
        data = load_data()
        seat_number = str(seat_number)

        if seat_number not in data["seats"]:
            return f"Seat {seat_number} does not exist."

        if user_id in data["seats"].values():
            return f"User {user_id} already has a booking."

        if data["seats"][seat_number] is not None:
            return f"Seat {seat_number} is already booked."

        # Simulate real-world race window
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
    print("\nSeat Map:")
    for seat, user in sorted(data["seats"].items(), key=lambda x: int(x[0])):
        status = "Available" if user is None else f"Booked by {user}"
        print(f"Seat {seat}: {status}")
