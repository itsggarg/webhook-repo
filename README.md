
# 🚀 GitHub Webhook Receiver

<div align="center">

![GitHub Webhook Receiver](https://img.shields.io/badge/GitHub-Webhook%20Receiver-181717?style=for-the-badge&logo=github)
![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.3.2-000000?style=for-the-badge&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=for-the-badge&logo=mongodb&logoColor=white)

A real-time GitHub webhook receiver that captures repository events (Push, Pull Request, Merge) and displays them in a beautiful, auto-updating UI.

[Live Demo](https://webhook-repo-73u8.onrender.com) | [Report Bug](https://github.com/itsggarg/webhook-repo/issues) | [Request Feature](https://github.com/itsggarg/webhook-repo/issues)

</div>

---

## 📋 Table of Contents

- [Features](#-features)
- [Demo](#-demo)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [Configuration](#-configuration)
- [Deployment](#-deployment)
- [Testing](#-Testing)
- [Webhook Events](#-webhook-events)
- [Contributing](#-contributing)
- [License](#-license)

## ✨ Features

- 🔄 **Real-time Updates** - UI auto-refreshes every 15 seconds
- 📊 **Event Tracking** - Captures Push, Pull Request, and Merge events
- 🔐 **Secure** - Webhook signature verification
- 💾 **Persistent Storage** - MongoDB Atlas integration
- 🎨 **Clean UI** - Responsive and modern interface
- 🚀 **Production Ready** - Deployed on Render with 99.9% uptime
- 📱 **Mobile Friendly** - Fully responsive design

## 🎥 Demo

<div align="center">

### Live Application: [https://webhook-repo-73u8.onrender.com](https://webhook-repo-73u8.onrender.com)
![Screenshot 2025-07-03 011732](https://github.com/user-attachments/assets/b3294d2d-cf5b-43f5-90f8-6c0f9bca381b)


</div>

## 🏗 Architecture

```mermaid
graph TD
    %% Subgraph: GitHub
    subgraph GitHub
        A[GitHub Repository]
    end

    %% Subgraph: Backend
    subgraph Backend
        B[Flask Server]
        C[Signature Verification]
        D[Event Processing]
        E[MongoDB Atlas]
        F[REST API]
    end

    %% Subgraph: Frontend
    subgraph Frontend
        G[Web UI]
    end

    %% Vertical flow (Top to Bottom)
    A -->|Webhook POST| B
    B --> C
    C --> D
    D --> E
    E --> F
    F -->|Polling every 15s| G

    %% Minimalist styles (white text, transparent background)
    style A fill:transparent,stroke:#ffffff,color:#ffffff,stroke-width:2px
    style B fill:transparent,stroke:#ffffff,color:#ffffff,stroke-width:2px
    style C fill:transparent,stroke:#ffffff,color:#ffffff,stroke-width:2px
    style D fill:transparent,stroke:#ffffff,color:#ffffff,stroke-width:2px
    style E fill:transparent,stroke:#ffffff,color:#ffffff,stroke-width:2px
    style F fill:transparent,stroke:#ffffff,color:#ffffff,stroke-width:2px
    style G fill:transparent,stroke:#ffffff,color:#ffffff,stroke-width:2px
    click A "https://github.com/itsggarg/webhook-repo" "View GitHub Repo"
    click G "https://webhook-repo-73u8.onrender.com" "View Web UI"
```

## 🛠 Tech Stack
<table> <tr> <td align="center" width="96"> <img src="https://skillicons.dev/icons?i=python" width="48" height="48" alt="Python" /> <br>Python </td> <td align="center" width="96"> <img src="https://skillicons.dev/icons?i=flask" width="48" height="48" alt="Flask" /> <br>Flask </td> <td align="center" width="96"> <img src="https://skillicons.dev/icons?i=mongodb" width="48" height="48" alt="MongoDB" /> <br>MongoDB </td> <td align="center" width="96"> <img src="https://skillicons.dev/icons?i=js" width="48" height="48" alt="JavaScript" /> <br>JavaScript </td> <td align="center" width="96"> <img src="https://skillicons.dev/icons?i=html" width="48" height="48" alt="HTML5" /> <br>HTML5 </td> <td align="center" width="96"> <img src="https://skillicons.dev/icons?i=css" width="48" height="48" alt="CSS3" /> <br>CSS3 </td> </tr> </table>


### Backend

| Package         | Version | Description                       |
|-----------------|---------|-----------------------------------|
| Flask           | 2.3.2   | Web framework                     |
| PyMongo         | 4.4.1   | MongoDB driver                    |
| Gunicorn        | 21.2.0  | WSGI HTTP Server                  |
| python-dotenv   | 1.0.0   | Environment variable management   |

### 🎨 Frontend

| Technology         | Description                          |
|--------------------|--------------------------------------|
| Vanilla JavaScript | No framework dependencies            |
| CSS3               | Modern, responsive styling           |
| Fetch API          | For polling updates                  |

### Infrastructure

| Service            | Description                          |
|--------------------|--------------------------------------|
| MongoDB Atlas      | Cloud database                       |
| Render             | Cloud hosting platform               |
| GitHub Webhooks    | Event source                         |


## 📦 Installation

### ✅ Prerequisites

- Python 3.8 or higher  
- MongoDB (local instance or [MongoDB Atlas](https://www.mongodb.com/cloud/atlas))  
- Git

### 🛠️ Local Development Setup

#### 1. Clone the repository

```bash
git clone https://github.com/itsggarg/webhook-repo.git
cd webhook-repo
```

#### 2. Create and activate a virtual environment

```bash
python -m venv venv
#On Windows:
venv\Scripts\activate
#On macOS/Linux:
source venv/bin/activate
```

#### 3. Install dependencies

```bash
pip install -r requirements.txt
```

#### 4. Set up environment variables

```env
SECRET_KEY=your-secret-key-here
MONGO_URI=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MONGO_DB_NAME=github_webhooks
WEBHOOK_SECRET=your-webhook-secret-here
```

#### 5. Run the Application
```bash
python run.py
```

#### 6. Access the application
Open your browser and navigate to: http://localhost:5000

## ⚙️ Configuration

### 🔐 Environment Variables

| Variable         | Description                        | Required | Default           |
|------------------|------------------------------------|----------|-------------------|
| `SECRET_KEY`     | Flask secret key for sessions      | ✅ Yes   | None              |
| `MONGO_URI`      | MongoDB connection string          | ✅ Yes   | None              |
| `MONGO_DB_NAME`  | Database name                      | ✅ Yes   | `github_webhooks` |
| `WEBHOOK_SECRET` | GitHub webhook secret              | ✅ Yes   | None              |


### 🗄️ MongoDB Schema

```json
{
  "_id": "ObjectId",            // Unique id for all events
  "request_id": "string",       // Commit hash or PR ID
  "author": "string",           // GitHub username
  "action": "string",           // PUSH, PULL_REQUEST, or MERGE
  "from_branch": "string",      // Source branch (PR/Merge only)
  "to_branch": "string",        // Target branch
  "timestamp": "string"         // ISO 8601 format
}
```
### 🔧 GitHub Webhook Configuration

1. Go to your repository's **Settings → Webhooks**
2. Click **"Add webhook"**
3. Configure the following:

   - **Payload URL**:  
     `https://your-app-url/webhook/receiver`

   - **Content type**:  
     `application/json`

   - **Secret**:  
     Your webhook secret (must match `WEBHOOK_SECRET` in `.env`)

   - **Events**:  
     ✅ Select **"Pushes"**  
     ✅ Select **"Pull requests"**


## 🚀 Deployment

### ▶️ Deploy to Render

1. **Fork this repository**
2. **Create a Render account** at [render.com](https://render.com)
3. **Create a new Web Service**
4. **Connect your GitHub account**
   - Select your forked repository
   - Use the following settings:

     | Setting          | Value                          |
     |------------------|--------------------------------|
     | Name             | `github-webhook-receiver`      |
     | Environment      | `Python`                       |
     | Build Command    | `pip install -r requirements.txt` |
     | Start Command    | `gunicorn run:app`             |

5. **Add environment variables** in the Render dashboard (`.env` values)
6. ✅ Click **Deploy!**  
   Your app will be live at:  
   `https://your-app.onrender.com`

## 🧪 Testing

### Local Testing with ngrok

1. Install [ngrok](https://www.google.com/url?sa=E&q=https%3A%2F%2Fngrok.com%2F)
2. Run your Flask app: python app.py
3. In another terminal: ngrok http 5000
4. Use the ngrok URL for your GitHub webhook

### Manual Testing
```bash

# test_webhook.py
import requests
import json

webhook_url = "http://localhost:5000/webhook"
headers = {
    "X-GitHub-Event": "push",
    "Content-Type": "application/json"
}

payload = {
    "ref": "refs/heads/main",
    "after": "abc123",
    "pusher": {"name": "testuser"}
}

response = requests.post(webhook_url, json=payload, headers=headers)
print(response.status_code, response.json())
```

## 🛠️ Development Guidelines

- Follow [PEP 8](https://peps.python.org/pep-0008/) for Python code
- Add comments for complex logic
- Update documentation for new features
- Write tests for new functionality

---

## 📄 License

This project is licensed under the **MIT License** – see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Govind Garg**

- GitHub: [itsggarg](https://github.com/itsggarg)
- Project Link: [webhook-repo](https://github.com/itsggarg/webhook-repo)

---

## 🙏 Acknowledgments

- [Flask Documentation](https://flask.palletsprojects.com/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [GitHub Webhooks Guide](https://docs.github.com/en/webhooks)
- [Render Documentation](https://render.com/docs)

---

<div align="center">

Made with ❤️ by **Govind Garg**

⭐ Star this repository if you find it helpful!

</div>
