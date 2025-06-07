# message2task 🚀

**Turn your messages into actionable tasks — effortlessly.**

[Try the live app now!](https://message2task.onrender.com) 🌐

---

## What is message2task?

message2task is a sleek Flutter-powered application designed to help you **extract tasks from your messages** and manage them seamlessly. Whether it’s work reminders, event invites, or simple to-dos, message2task transforms your incoming messages into clear, organized tasks — so you never miss a beat.

---

## Features

- **Automatic task extraction** from messages with AI-powered parsing  
- **Easy task confirmation, editing, and deletion** with a simple interface  
- Persistent task management with **local storage** support  
- Real-time message fetching and updates  
- User-friendly interface with options to manually adjust task details  
- Access your confirmed tasks anytime via the dedicated page

---

## Live Demo

Check out the app live on [message2task.onrender.com](https://message2task.onrender.com) — no installation needed!

---

## Getting Started

Want to run the app locally or contribute? Here’s how:


## Installation

Follow these steps to set up and run the **Message2Task** project locally. This project includes a Python Flask backend and a Flutter frontend.

### Prerequisites

- Python 3.7+ installed
- Flutter SDK installed ([Flutter installation guide](https://flutter.dev/docs/get-started/install))
- Git installed

---

### 1. Clone the repository

```bash
git clone https://github.com/kate20031/Message2Task.git
cd Message2Task
```

### 2. Setup and run the backend (Python Flask)

It's recommended to use a virtual environment:

```
python3 -m venv venv
source venv/bin/activate        # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```
Set environment variables if necessary (check `.env` file).

Start the Flask backend server:

```bash
python app.py
```

By default, the backend will run on [http://localhost:5000](http://localhost:5000).




[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Flutter](https://img.shields.io/badge/Flutter-3.10.0-blue)](https://flutter.dev)
[![GitHub issues](https://img.shields.io/github/issues/kate20031/Message2Task)](https://github.com/kate20031/Message2Task/issues)
[![GitHub stars](https://img.shields.io/github/stars/kate20031/Message2Task)](https://github.com/kate20031/Message2Task/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/kate20031/Message2Task)](https://github.com/kate20031/Message2Task/network/members)

## How to Use

- Open the app and view your messages dashboard.
- New messages automatically convert into tasks with parsed details.
- Confirm tasks once reviewed or edit details like (for example) date/time manually.
- Delete tasks you no longer need.
- Visit the “Confirmed” page to see your saved tasks anytime.

## Contributing

Contributions and feedback are welcome! Feel free to open issues or submit pull requests.

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
