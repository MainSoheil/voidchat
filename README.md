# VOIDCHAT 🕳️💬

Anonymous, real‑time chat platform with ephemeral rooms.  
Built with **FastAPI**, **SQLite**, **WebSockets**, and a **React** frontend.

## ✨ Features

- 🔒 **Anonymous** – users are identified only by their IP address.
- 🚪 **Rooms** – join a room by a unique key.
- ⚡ **Real‑time** – WebSocket‑based messaging with instant broadcasting.
- 🧹 **Ephemeral** – messages are deleted when the last user leaves a room.
- 📜 **History** – fetch the last 100 messages of a room via REST API.
- 🌐 **IP‑based identity** – messages are aligned to “You” vs “Anonymous”.

## 🛠 Tech Stack

| Layer       | Technology                           |
|-------------|--------------------------------------|
| Backend     | FastAPI, Uvicorn, SQLite, Pydantic   |
| Frontend    | React, TypeScript, Tailwind CSS      |
| State       | Zustand (for room key)               |
| Realtime    | WebSockets                           |

## 📁 Project Structure

> *Adjust the actual folder structure if yours differs.*

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- Node.js 16+
- npm or yarn

### 1. Clone the repository

```bash
git clone https://github.com/your-username/voidchat.git
cd voidchat