# 🎓 **SPPU StudyPortal IT** 🖇️

<div align="center">

![GitHub stars](https://img.shields.io/github/stars/Pratikshinde99/StudyPortal_IT?style=social)
![GitHub forks](https://img.shields.io/github/forks/Pratikshinde99/StudyPortal_IT?style=social)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-2.x-000000?style=flat&logo=flask&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-Atlas-47A248?style=flat&logo=mongodb&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

**A premium, enterprise-grade study portal for Information Technology students at Savitribai Phule Pune University (SPPU). Features a modern high-performance design, secure admin analytics, and optimized PDF delivery.**

[🚀 Live Demo](#) • [📖 Documentation](#-features) • [🐛 Report Bug](https://github.com/Pratikshinde99/StudyPortal_IT/issues) • [👨‍💻 Author](#-contact)

</div>

---

## ✨ **Key Features**

### 🌟 **Student Experience**
- **Modern Dark UI**: A balanced, eye-friendly interface built with high-performance CSS and smooth micro-animations.
- **Enterprise Spacing**: A spacious, professional layout that eliminates "clutter" and focuses on readability.
- **Real-Time Toasts**: Instant "Added to Favorites ❤️" and status notifications for a seamless session.
- **Curated Curriculum**: Structured access to study materials for all 8 semesters of the IT engineering department.
- **Search Engine**: Dynamic search to find any subject or document instantly across the entire portal.

### 👨‍💼 **Admin & Analytics**
- **Data-Driven Dashboard**: High-impact administrative center with percentage-based content distribution stats.
- **Secure File Hub**: Upload, Manage, and Delete study materials directly through a protected admin workflow.
- **MongoDB GridFS Integration**: Optimized binary storage for large PDF files, ensuring zero-latency material delivery.
- **Session Protection**: Strict authentication with themed logout confirmations to prevent accidental session termination.

---

## 🛠️ **Tech Stack**

| Layer | Technology |
|---|---|
| **Frontend** | Vanilla HTML5 & CSS3 (Advanced Aesthetic), Modern ES6+ JavaScript |
| **Backend** | Python 3.11, Flask Framework |
| **Database** | MongoDB Atlas (Cloud) with GridFS |
| **Security** | Flask-Talisman (HTTPS Enforcement), Session-Based Auth, Bcrypt Hashing |
| **Deployment** | Render (Production Optimized) |

---

## 📂 **Project Structure**

```bash
StudyPortal_IT/
├── backend/
│   └── app/               # Flask Application Factory & Logic
│       ├── extensions.py  # DB Extensions Init
│       └── routes.py      # Core Application Routing
├── frontend/
│   ├── static/            # Stylesheets & Premium Assets
│   └── templates/         # Jinja2 HTML Templates
├── main.py                # Production Entry Point
├── render.yaml            # Render Cloud Deployment Configuration
├── requirements.txt       # Project Dependencies
└── runtime.txt            # Python Versioning
```

---

## 🚀 **Quick Setup**

### **1. Clone & Initialize**
```bash
git clone https://github.com/Pratikshinde99/StudyPortal_IT.git
cd StudyPortal_IT
```

### **2. Virtual Environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/macOS
source venv/bin/activate
```

### **3. Dependencies**
```bash
pip install -r requirements.txt
```

### **4. Environment Config**
Create a `.env` file in the root (this file is ignored by git for security):
```env
MONGODB_URI=your_atlas_connection_string
SECRET_KEY=your_secure_random_key
ADMIN_USERNAME=your_admin
ADMIN_PASSWORD=your_password
```

### **5. Run Locally**
```bash
python main.py
```

---

## 🔒 **Security Standards**
- **0 Hardcoded Credentials**: All secrets are managed via environment variables.
- **HTTPS Enforcement**: Talisman middleware enabled for live production environments.
- **CORS & CSP Protected**: High-standard security headers to protect student data.

---

## 👨‍💻 **Contact**

**Pratik Shinde**  
🖇️ **GitHub**: [@Pratikshinde99](https://github.com/Pratikshinde99/)  
📧 **Email**: [ps175581@gmail.com](mailto:ps175581@gmail.com)

---

<div align="center">

**Made with ❤️ for SPPU IT Students**
[⬆ Back to Top](#-sppu-studyportal-it-🖇️)

</div>
