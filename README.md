# MusicBlocks AI Contributor 🎵🤖

[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.95%2B-green)](https://fastapi.tiangolo.com/)

**Empowering music education through AI-powered sound generation**  
*Integrate cutting-edge audio AI models directly into MusicBlocks' sampler widget*

![MusicBlocks AI Interface](https://via.placeholder.com/800x400?text=AI+Sample+Generator+Interface)

## 🚀 Features

- **AI-Powered Sound Generation**
  - Generate instrument samples from text prompts ("jazzy piano", "ethereal synth")
  - Transform existing recordings with AI effects
  - Support for MusicGen, AudioLDM2, and Stable Audio models

- **Educator-Focused Platform**
  - Contribution pathway visualization
  - Mentorship program integration
  - Student progress tracking

- **Technical Highlights**
  - FastAPI backend with model orchestration
  - React-based frontend with Tone.js integration
  - GPU-accelerated inference pipeline

## ⚙️ Installation

### Prerequisites
- Python 3.11+
- Node.js 16+
- Docker 24+
- NVIDIA GPU (3050ti)

### Setup
```bash
# Clone repository
git clone https://github.com/CoDIngDEMon018/MusicBlocks-AI-Contributor
cd MusicBlocks-AI-Contributor

# Frontend setup
cd frontend
npm install
cp .env.example .env

# Backend setup
cd ../backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Start services
docker-compose up -d  # Starts Redis and Postgres
npm run dev  # Frontend
uvicorn main:app --reload  # Backend
