# File: docs/install_guide.md

# 🧠 CerebroMesh Installation Guide

Welcome to CerebroMesh — the cognitive API mesh that evolves, scales, explains, and heals itself. This guide will walk you through setting up CerebroMesh locally, on Docker, or deploying to the cloud.

---

## 🔧 Requirements

- Python 3.10+
- Node.js 18+ (for frontend)
- Docker (optional)
- Cloudflare account (for edge deployment)
- Local quantized LLM model (e.g., `mistral_quantized.gguf`)
- Virtual environment recommended (venv or conda)

---

## 🐍 Backend Setup (FastAPI)

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-org/cerebromesh.git
   cd cerebromesh
