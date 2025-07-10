# 🚉 Multilingual Translation Engine for Station Announcements

A Python-based desktop application designed to eliminate language barriers at transportation hubs. The system translates station announcements into multiple Indian languages in real-time using the **Google Translation API** and converts them to speech using the **Google Text-to-Speech API**, ensuring accessibility for all passengers.

---

## 📌 Problem Statement

In multilingual countries like India, most station announcements are made in one or two dominant languages. This causes confusion and inconvenience for passengers who do not understand those languages. Our system bridges this gap with real-time multilingual announcements.

---

## 🎯 Features

- 📝 **Manual Announcement Input** – Station staff can enter announcements via a simple form.
- 🌐 **Language Selection** – Select source and multiple target languages (Hindi, Marathi, Tamil, Bengali, etc.).
- 🔄 **Real-Time Translation** – Translates announcements using Google Translation API.
- 🔊 **Audio Announcements** – Converts translated text to speech using Google TTS API.
- 🖥️ **Visual Display** – Shows translated announcements on-screen.
- ♿ **Inclusive Design** – Audio + visual outputs improve accessibility for hearing or visually impaired users.

---

## 🛠️ Tech Stack

| Layer                     | Technology                            |
|---------------------------|----------------------------------------|
| Programming Language      | Python                                 |
| GUI                       | Tkinter                                |
| Translation API           | Google Cloud Translation API           |
| Text-to-Speech            | Google Cloud Text-to-Speech API        |
| UI Design (Planning)      | Canva, Figma                           |

---

## ⚙️ Install Dependencies
pip install -r requirements.txt

### Clone the Repository

```bash
git clone https://github.com/sarushinde302/multilingual-announcement-engine.git
cd multilingual-announcement-engine
