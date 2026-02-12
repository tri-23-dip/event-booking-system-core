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
    return data["total_seats"] - len(data["booked_seats"])


def book_seat(user_id):
    with lock:
        data = load_data()

        if user_id in data["booked_seats"]:
            return f"User {user_id} already has a booking."

        if len(data["booked_seats"]) >= data["total_seats"]:
            return "No seats available."

        data["booked_seats"].append(user_id)
        save_data(data)

        return f"Seat booked successfully for user {user_id}."


def cancel_booking(user_id):
    with lock:
        data = load_data()

        if user_id not in data["booked_seats"]:
            return f"No booking found for user {user_id}."

        data["booked_seats"].remove(user_id)
        save_data(data)

        return f"Booking cancelled for user {user_id}."


if __name__ == "__main__":
    print(book_seat("user1"))
    print(book_seat("user2"))
    print(get_available_seats())
    print(cancel_booking("user1"))
    print(get_available_seats())
