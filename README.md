# Event Booking System Core

## Overview
A lightweight backend core for managing event seat bookings with consistency and conflict prevention.

## Features
- Seat availability tracking
- Booking and cancellation
- Conflict prevention using locking
- JSON-based persistent state

## Tech Stack
- Python
- JSON

## How It Works
- `data.json` stores event and booking state
- `booking.py` handles all business logic
- Thread lock ensures booking consistency

## How to Run
```bash
python booking.py
