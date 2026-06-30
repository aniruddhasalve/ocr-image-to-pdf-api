# Image to PDF (OCR)

A small [FastAPI](https://fastapi.tiangolo.com/) service that accepts an image upload and returns a searchable PDF. Conversion and text recognition are handled by [OCRmyPDF](https://ocrmypdf.readthedocs.io/) (Tesseract OCR, deskew, auto-rotate).

## Features

- Upload a single image (PNG, JPEG, etc.) and receive a PDF with embedded OCR text
- Automatic deskew and page rotation
- Health-check endpoint for monitoring
- Docker support for easy setup on any platform

## API

| Method | Endpoint         | Description                          |
|--------|------------------|--------------------------------------|
| GET    | `/test`          | Health check — returns `{"status": "running"}` |
| POST   | `/image-to-pdf/` | Upload an image file, get a PDF back |

### Example request

```bash
curl -X POST "http://localhost:5656/image-to-pdf/" \
  -F "file=@/path/to/your/image.png" \
  -o output.pdf
```

Interactive API docs are available at `http://localhost:5656/docs` when needed.

## Prerequisites

- **Docker** (recommended) — [Docker Desktop](https://www.docker.com/products/docker-desktop/) on Windows/Mac, or Docker Engine on Linux
- **Local install** — Python 3.10+, Tesseract OCR, Ghostscript, and Poppler

---

## Running with Docker (Linux, macOS, Windows)

Docker is the easiest way to run this project on all platforms.

### Build the image

```bash
docker build -t image-to-pdf .
```

### Run the container

```bash
docker run -d -p 5656:5656 --name image-to-pdf image-to-pdf
```

The service listens on **port 5656**.

### Verify it is running

```bash
curl http://localhost:5656/test
```

Expected response:

```json
{"status": "running"}
```

### Stop and remove the container

```bash
docker stop image-to-pdf
docker rm image-to-pdf
```

---

## Running locally (without Docker)

Use this if you prefer a native Python setup. The app writes temporary files to `/tmp`, so **local runs are best on Linux and macOS**. On Windows, use Docker or WSL2.

### Linux (Debian / Ubuntu)

Install system dependencies:

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr tesseract-ocr-eng ghostscript poppler-utils libmagic1
```

Set up Python and start the server:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
uvicorn main:app --host 0.0.0.0 --port 5656
```

### macOS

Install system dependencies with Homebrew:

```bash
brew install tesseract ghostscript poppler
```

Set up Python and start the server:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd app
uvicorn main:app --host 0.0.0.0 --port 5656
```

### Windows

**Recommended:** use Docker (see above).

For a native install you need Python 3.10+, [Tesseract for Windows](https://github.com/UB-Mannheim/tesseract/wiki), Ghostscript, and Poppler. The app uses `/tmp` for temporary files, which is not available on native Windows — use **WSL2** or Docker instead.

If using WSL2, follow the Linux instructions inside your WSL terminal.

---

## Project structure

```
.
├── app/
│   └── main.py          # FastAPI application
├── Dockerfile           # Container image definition
├── LICENSE              # MIT License
├── requirements.txt     # Python dependencies
└── README.md
```

## Tech stack

- [FastAPI](https://fastapi.tiangolo.com/) — web framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [OCRmyPDF](https://ocrmypdf.readthedocs.io/) — image-to-PDF with OCR
- [Tesseract](https://github.com/tesseract-ocr/tesseract) — OCR engine

## License

This project is licensed under the [MIT License](LICENSE).
