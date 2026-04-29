<div align="center">

<img src="https://img.shields.io/badge/BridalVision-AI-ff69b4?style=for-the-badge&logo=data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI+PHBhdGggZmlsbD0id2hpdGUiIGQ9Ik0xMiAyQzYuNDggMiAyIDYuNDggMiAxMnM0LjQ4IDEwIDEwIDEwIDEwLTQuNDggMTAtMTBTMTcuNTIgMiAxMiAyem0tMiAxNWwtNS01IDEuNDEtMS40MUwxMCAxNC4xN2w3LjU5LTcuNTlMMTkgOGwtOSA5eiIvPjwvc3ZnPg==" alt="BridalVision AI" />

# 👰 BridalVision AI

### AI-Powered Virtual Bridal Dress Try-On Service

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688?style=flat-square&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![fal.ai](https://img.shields.io/badge/fal.ai-IDM--VTON-6C63FF?style=flat-square)](https://fal.ai)
[![License](https://img.shields.io/badge/License-Proprietary-red?style=flat-square)](LICENSE)
[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen?style=flat-square)](/)

> **"ঘরে বসে ড্রিম ড্রেস পরে দেখুন — বিয়ের দিনের আগেই।"**  
> *Try on your dream bridal dress before the big day — from the comfort of your home.*

</div>

---

## 📖 Overview

**BridalVision AI** is a state-of-the-art virtual try-on service built exclusively for the bridal industry. Powered by **fal.ai IDM-VTON** (Improved Diffusion Model for Virtual Try-On), it allows brides to upload a full-body photo and instantly see a hyper-realistic preview of themselves wearing any chosen bridal dress.

This repository contains the **AI microservice module only**. It is designed to be integrated with a Django backend by a backend developer who handles authentication, database, email delivery, and deployment.

---

## 🌸 The Problem We Solve

| Pain Point | Traditional Experience | BridalVision AI |
|---|---|---|
| 🕐 **Time** | Weeks visiting boutiques | Instant AI preview |
| 💰 **Cost** | Travel + appointment fees | One upload, unlimited inspiration |
| 📍 **Distance** | Must visit in-person | Works from anywhere |
| 😰 **Decision fatigue** | Dozens of physical try-ons | Narrow choices digitally first |
| 📈 **Boutique conversion** | Low online engagement | Higher appointment intent |

Most bridal websites still show **static photos only**. By integrating a virtual try-on experience, boutiques can:
- Capture leads earlier in the decision journey
- Increase online-to-appointment conversion rates
- Position their brand as modern and tech-forward

---

## ✨ Key Features

- 🖼️ **Smart Photo Upload** — Validates and preprocesses human photos (JPG, PNG, WEBP, BMP, TIFF, GIF)
- 👗 **Dress-by-URL Selection** — Accepts any garment image URL from the boutique catalog
- 🤖 **IDM-VTON Integration** — Hyper-realistic fitting with full body & pose preservation
- 💡 **Lighting Control** — Studio, outdoor, church, or default rendering
- 👰 **Style Presets** — Ball gown, A-line, mermaid, sheath, lace, off-shoulder
- 🔒 **Session Limit Enforcement** — Max 3 try-ons per session (configurable)
- 🌐 **Background-Neutral Output** — Clean results ready for UI placement
- 🔐 **Zero Image Storage** — No user photos stored; full GDPR-friendly architecture
- ⚡ **Async API** — Non-blocking fal.ai calls for fast response times

---

## 🏗️ Project Structure

```
Bridal-Vision-AI/
│
├── 📁 app/
│   ├── 📁 api/
│   │   └── endpoints.py          # FastAPI routes (/health, /tryon)
│   ├── 📁 core/
│   │   ├── config.py             # Settings & environment variables
│   │   └── prompts.py            # Prompt engineering utilities
│   ├── 📁 services/
│   │   └── fal_service.py        # Core fal.ai IDM-VTON wrapper
│   └── 📁 utils/
│       ├── image_utils.py        # Photo validation & upload helpers
│       └── session_utils.py      # Session limit logic (3/session)
│
├── 📁 tests/                     # Pytest test suite
├── 📁 docs/                      # Additional documentation
│
├── main.py                       # FastAPI application entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variable template
└── .gitignore
```

---

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- A valid [fal.ai](https://fal.ai) API key
- pip or a virtual environment manager

---

### Step 1 — Clone & Create Virtual Environment

```bash
git clone https://gitlab.betopialimited.com/join-venture-ai/bridal-vision-ai.git
cd bridal-vision-ai

# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python -m venv venv
source venv/bin/activate
```

### Step 2 — Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3 — Configure Environment Variables

```bash
# Windows
copy .env.example .env

# macOS / Linux
cp .env.example .env
```

Open `.env` and set your fal.ai API key:

```env
FAL_KEY=your_fal_api_key_here
```

> **Get your key at:** [https://fal.ai/dashboard](https://fal.ai/dashboard)

### Step 4 — Run the AI Service

```bash
uvicorn main:app --reload --port 8001
```

### Step 5 — Explore the Docs

```
http://localhost:8001/docs      → Swagger UI (interactive)
http://localhost:8001/redoc     → ReDoc (clean reference)
http://localhost:8001/          → Service health root
```

---

## 📡 API Reference

### `GET /api/health`

Simple health check to verify the service is running.

**Response:**
```json
{
  "status": "ok",
  "service": "BridalVision AI"
}
```

---

### `POST /api/tryon`

Submit a virtual try-on request via multipart form upload.

**Form Fields:**

| Field | Type | Required | Description |
|---|---|---|---|
| `session_id` | `string` | ✅ Yes | Unique session identifier from backend |
| `garment_image_url` | `string` | ✅ Yes | Public URL of the selected dress image |
| `human_image` | `file` | ✅ Yes | Full-body photo of the bride (max 5 MB) |
| `dress_style` | `string` | ❌ Optional | `ball_gown` / `a_line` / `mermaid` / `sheath` / `lace` / `off_shoulder` |
| `lighting` | `string` | ❌ Optional | `studio` / `outdoor` / `church` |

**Supported Image Formats:**  
`JPG` · `JPEG` · `PNG` · `WEBP` · `BMP` · `TIFF` · `GIF` *(non-animated)*

> Non-JPEG/PNG images are automatically converted to PNG before sending to fal.ai.

---

**✅ Success Response `(200 OK)`:**
```json
{
  "success": true,
  "result_image_url": "https://fal.ai/results/abc123...",
  "tries_remaining": 2,
  "message": "Your virtual try-on is ready!"
}
```

**⛔ Session Limit Reached `(200 OK)`:**
```json
{
  "success": false,
  "result_image_url": null,
  "tries_remaining": 0,
  "message": "You have reached the maximum of 3 try-ons for this session."
}
```

**❌ Validation Error `(400 Bad Request)`:**
```json
{
  "detail": "Invalid image format. Supported formats: JPG, PNG, WEBP, BMP, TIFF, GIF."
}
```

---

## 🔒 Privacy & GDPR

BridalVision AI was designed with privacy-first principles:

| Concern | How We Handle It |
|---|---|
| 🖼️ **Image Storage** | **No images stored** by this module |
| 🔗 **Data Transfer** | Images sent to fal.ai via **temporary URLs only** |
| 🧠 **Session Data** | Session counts are **in-memory only** (cleared on restart) |
| 📋 **Retention Policy** | Backend team is responsible for GDPR compliance, deletion, and email delivery |

---

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run with coverage report
pytest tests/ --cov=app --cov-report=term-missing
```

---

## 📦 Tech Stack

| Layer | Technology | Version |
|---|---|---|
| 🌐 Web Framework | FastAPI | 0.111.0 |
| ⚡ ASGI Server | Uvicorn | 0.29.0 |
| 🤖 AI / Try-On | fal.ai (IDM-VTON) | fal-client 0.4.1 |
| 🖼️ Image Processing | Pillow | 10.3.0 |
| 🔧 Env Config | python-dotenv | 1.0.1 |
| 📋 Form Data | python-multipart | 0.0.9 |
| 🧪 Testing | pytest + httpx | 8.2.0 / 0.27.0 |

---

## 🗺️ Roadmap

- [x] Core fal.ai IDM-VTON integration
- [x] Photo validation and multi-format support
- [x] Session limit enforcement
- [x] Dress style & lighting preset prompts
- [x] Clean API with Swagger docs
- [ ] Redis-based persistent session tracking
- [ ] Webhook support for async result delivery
- [ ] Admin analytics endpoint (try-on counts by session)
- [ ] Multi-garment try-on (e.g. veil + dress)
- [ ] Mobile-optimized image resizing pipeline

---

## 🤝 Integration Guide (For Backend Developers)

This FastAPI service is designed to run **alongside** a Django backend. Recommended integration:

```python
# In Django's urls.py — mount the FastAPI app via ASGI/reverse proxy

# OR run separately and proxy via nginx:
# location /ai/ {
#     proxy_pass http://127.0.0.1:8001/;
# }
```

The backend must:
1. Generate a `session_id` per user session and pass it to `/api/tryon`
2. Relay the `result_image_url` to the frontend or store it
3. Handle email delivery of the result image
4. Enforce GDPR deletion policies for user data

---

## 👨‍💻 Author

<div align="center">

**Shahidul Islam**  
*Jr. AI Engineer*  
🏢 **Betopia Group / Join Venture AI** — Dhaka, Bangladesh

[![Email](https://img.shields.io/badge/Contact-Email-D44638?style=flat-square&logo=gmail&logoColor=white)](mailto:shahidul@betopiagroup.com)
[![Company](https://img.shields.io/badge/Company-Betopia%20Group-0A66C2?style=flat-square)](https://betopiagroup.com)

</div>

---

## 📄 License

This project is **proprietary software** owned by **Betopia Group / Join Venture AI**.  
Unauthorized copying, distribution, or modification is strictly prohibited.

---

<div align="center">

Made with ❤️ for brides everywhere · © 2026 Betopia Group

</div>
