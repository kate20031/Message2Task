# Message2Task 🚀

**Turn messages into tasks — simple, fast, automatic.**

[👉 Try it online](https://message2task.onrender.com)

---

## 🔍 What is it?

**Message2Task** is a web application built with Flask (Python) that automatically extracts tasks from messages and allows you to manage them through an intuitive interface. You can edit, confirm, or delete tasks right in your browser.

---

## ⚙️ Features

* 📩 **Real-time message reception**
* 🤖 **AI-based message parsing** into formatted tasks
* ✅ One-click task confirmation
* ✏️ Edit task date, time, and details
* 🗑️ Delete unnecessary tasks
* 💾 Local saving of confirmed tasks (via LocalStorage)
* 🔄 Manual "Refresh" button
* 👀 "Confirmed" page to view saved tasks

---

## 🌐 Live Demo

[🔗 https://message2task.onrender.com](https://message2task.onrender.com)

---

## 🛠️ Installation & Run

### 1. Clone the repository

```bash
git clone https://github.com/kate20031/Message2Task.git
cd Message2Task
```

### 2. Backend setup & run (Flask)

It is recommended to use a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Check the `.env` file and set environment variables as needed.

Run the Flask server:

```bash
python app.py
```

📍 By default, the server runs at: [http://localhost:5000](http://localhost:5000)

---

## 🧪 How to Use

1. Go to the main page of the app
2. Log in or register
3. On the Dashboard, you'll see messages converted into tasks
4. If needed — click **Edit** to modify (e.g., date or time)
5. After editing, click **Save**, then **Confirm**
6. To delete a task — click **Delete**
7. To view saved tasks, click **Confirmed**

---

## 🧹 Project Structure

```
Message2Task/
├── app.py                # Main Flask application
├── templates/            # HTML templates (Jinja2)
│   ├── dashboard.html
│   ├── login.html
│   ├── register.html
│   └── confirmed.html
├── static/css/           # Frontend styles
│   └── style.css
├── routes/               # API routes
├── utils/                # Utility helpers
├── models.py             # Database models
├── ai_task_extractor.py  # Parsing messages into tasks
├── strategy_*.py         # AI processing strategies
└── requirements.txt      # Python dependencies
```

---

## 🤠 Prerequisites

* Python 3.7+
* pip
* Git

---

## 🤝 Contribution

Pull Requests, Issues, and feedback are welcome!
Want to add a new feature or found a bug? — You’re welcome 👇

👉 [GitHub Issues](https://github.com/kate20031/Message2Task/issues)

---

## 📄 License

This project is licensed under the **Apache-2.0** license.
See the  [LICENSE](LICENSE) file for details.

---

💡 Made with ❤️ by [@kate20031](https://github.com/kate20031)
