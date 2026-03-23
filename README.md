# Telegram Course Registration Bot

A bilingual Telegram bot built for class registration and student follow-up.

This project was created for a real learning workflow where students register for courses through Telegram, choose their language, submit their details, get connected to a real admin, and continue through a structured enrollment process. The bot is designed to reduce repetitive manual work while still keeping the human trust element that students often need.

It currently supports English and Amharic, stores data in SQLite, syncs registrations to Google Sheets, notifies the admin in Telegram, and tracks installment-based payment progress.

---

## What this bot does

The bot helps manage the student registration process from start to follow-up.

### Student side
- Choose language: English or Amharic
- Read FAQs
- Browse available classes
- Register for a class through a guided form
- Submit:
  - full name
  - department
  - phone number
- Receive a registration reference code
- Get connected to a real admin through Telegram
- Receive status updates after registration
- Receive payment-progress updates for installment-based courses

### Admin side
- Get notified when a new student registers
- View registration details directly in Telegram
- Set course duration:
  - 2 months
  - 3 months
  - 4 months
- Update operational status:
  - contacted
  - payment pending
  - joined
  - cancelled
- Record installment payments using `+1 Payment`
- Automatically sync updates to Google Sheets

### Data side
- Save registrations in SQLite
- Sync rows to Google Sheets
- Update payment progress and status consistently

---

## Why this project exists

This bot was built for a real educational registration workflow, especially for courses where:

- students often ask the same questions repeatedly
- admin work becomes messy in private chat
- trust matters, especially around payment
- support is needed in both English and Amharic
- payment may happen monthly rather than once

The goal was not just to build a Telegram bot, but to build a practical enrollment workflow system that a real admin can use.

---

## Main features

- Bilingual interface (English / Amharic)
- Inline-menu navigation
- FAQ section
- Guided FSM registration form
- Ethiopia-aware phone validation
- Registration reference codes
- SQLite persistence
- Google Sheets synchronization
- Admin notification in Telegram
- Student status notifications
- Installment payment tracking
- Human handoff to a real admin

---

## Tech stack

- Python
- aiogram
- SQLAlchemy
- SQLite
- Google Sheets API
- gspread
- DBeaver (for local database inspection)

---

## Project structure

```text
app/
├── config/
├── database/
├── handlers/
├── i18n/
├── keyboards/
├── services/
├── states/
├── utils/
run.py