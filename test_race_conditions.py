import threading
import json
from booking import book_specific_seat, load_data

TEST_SEAT = 1


def reset_data():
    data = {
        "event_id": "EVT1001",
        "total_seats": 10,
        "seats": {str(i): None for i in range(1, 11)}
    }
    with open("data.json", "w") as f:
        json.dump(data, f, indent=4)


def attempt_booking(user_id, results):
    result = book_specific_seat(user_id, TEST_SEAT)
    results.append(result)


def test_concurrent_booking_same_seat():
    reset_data()

    results = []
    threads = []

    for i in range(5):
        t = threading.Thread(
            target=attempt_booking,
            args=(f"user{i}", results)
        )
        threads.append(t)

    for t in threads:
        t.start()

    for t in threads:
        t.join()

    print("\nBooking Results:")
    for r in results:
        print(r)

    data = load_data()
    booked_users = [u for u in data["seats"].values() if u is not None]

    assert len(booked_users) == 1, "More than one user booked the same seat!"
    print("\n✅ Race condition test passed: Only one booking succeeded.")


if __name__ == "__main__":
    test_concurrent_booking_same_seat()
