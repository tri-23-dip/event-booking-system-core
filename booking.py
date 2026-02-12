import json
import threading

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


def book_seat(user_id):
    with lock:
        data = load_data()

        # Prevent double booking
        if user_id in data["seats"].values():
            return f"User {user_id} already has a booked seat."

        # Find first available seat
        for seat, user in data["seats"].items():
            if user is None:
                data["seats"][seat] = user_id
                save_data(data)
                return f"Seat {seat} successfully booked for user {user_id}."

        return "No seats available."


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
    for seat, user in data["seats"].items():
        status = "Available" if user is None else f"Booked by {user}"
        print(f"Seat {seat}: {status}")


if __name__ == "__main__":
    print(book_seat("user1"))
    print(book_seat("user2"))
    print(book_seat("user1"))  # conflict test
    show_seat_map()
    print(cancel_booking("user1"))
    show_seat_map()
