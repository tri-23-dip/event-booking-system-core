# 🎟️ Event Booking System Core

## Overview
A lightweight yet robust backend core for an event seat booking system, designed with **booking consistency, explicit seat allocation, and concurrency safety** in mind.

This project focuses on **business logic and state management**, keeping the implementation simple while modeling real-world constraints found in ticketing systems.

---

## 🚀 Features

- ✅ Explicit seat numbering (Seat 1 → N)
- 🎟️ User-selected seat booking
- 🔁 Booking cancellation
- 🚫 Double-booking prevention
- 🔒 Thread-safe operations using locks
- 🧪 Unit tests simulating race conditions
- 💾 JSON-based persistent state (DB-ready design)

---

## 🧠 Design Highlights

- **Single source of truth** via `data.json`
- **Atomic-style operations**: read → validate → write
- **Concurrency-style thinking** using thread locks
- Logic easily portable to SQL / NoSQL databases
- Clean separation of state and business rules

---

## 🛠 Tech Stack

- Python
- JSON
- Threading (for concurrency simulation)

---

## 📁 Project Structure

