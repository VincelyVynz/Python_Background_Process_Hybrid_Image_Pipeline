# Hybrid Image Pipeline (Asyncio + Threading + Multiprocessing) in Python

## Overview

This project demonstrates a hybrid approach to concurrency in Python, combining **asyncio**, **threading**, and **multiprocessing**. The pipeline downloads images from the web, saves them in multiple formats, and applies CPU-heavy transformations like resizing and grayscale conversion.

- **Asyncio** → downloads images concurrently
- **Threading** → saves images in multiple formats without blocking
- **Multiprocessing** → performs CPU-intensive image processing

---

## Features

- Concurrent image downloading using asyncio and aiohttp
- Threaded saving of images in multiple formats (PNG, JPEG, WEBP)
- Multiprocessing for transformations:
  - Grayscale conversion
  - Resize


---

## Folder Structure

| File/Folder       | Description                               |
|------------------|-------------------------------------------|
| input_urls.txt    | List of image URLs to download            |
| downloaded/       | Asyncio downloads (raw images)            |
| saved_formats/    | Threaded saves in multiple formats        |
| processed/        | Multiprocessing results                    |
| pipeline.py       | Main project code                          |
| requirements.txt  | Dependencies (aiohttp, Pillow/OpenCV)     |
| README.md         | Project explanation                        |



---

## Setup

1. Clone the repository:

   git clone <your-repo-url>
   cd hybrid_image_pipeline

2. Create a virtual environment (recommended):

   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   venv\Scripts\activate     # Windows

3. Install dependencies:

   pip install -r requirements.txt

---

## Usage

1. Add image URLs to `input_urls.txt`, one per line.
2. Run the pipeline:

   python pipeline.py

3. Check the output folders:

   - `downloaded/` → raw downloaded images
   - `saved_formats/` → images in multiple formats
   - `processed/` → transformed images



---

## Notes

- Designed to showcase Python concurrency models in one cohesive project
- Demonstrates **why and where** each model is suitable
