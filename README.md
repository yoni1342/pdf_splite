# PDF to PNG Converter API

This is a FastAPI-based service that converts PDF files to PNG images and returns them as a ZIP file.

## Features

- Upload PDF files
- Convert PDF pages to PNG images
- Automatically compress PNG images into a ZIP file
- Download converted images as a ZIP file
- Automatic cleanup of temporary files after 1 hour

## Requirements

- Docker
- Docker Compose

## Running the Application

### Using Docker Compose (Recommended)

1. Create temp directory:
```bash
mkdir -p temp
```

2. Start the service:
```bash
docker-compose up -d
```

3. Stop the service:
```bash
docker-compose down
```

### Using Docker directly

1. Build the Docker image:
```bash
docker build -t pdf-converter .
```

2. Run the container:
```bash
docker run -p 8000:8000 pdf-converter
```

The API will be available at http://localhost:8000

## API Usage

### Convert PDF to PNG Images

**Endpoint:** `POST /convert/`

Use this endpoint to upload a PDF file and receive a ZIP file containing PNG images of each page.

You can test the API using:
- The interactive API documentation at http://localhost:8000/docs
- cURL:
```bash
curl -X POST -F "pdf_file=@your_pdf.pdf" http://localhost:8000/convert/ --output converted_images.zip
```

## Cleanup Service

The application includes an automatic cleanup service that:
- Runs every hour
- Removes temporary files older than 1 hour
- Helps manage disk space automatically
- Logs cleanup activities to the container's log

## Error Handling

The API will return appropriate error messages if:
- The uploaded file is not a valid PDF
- There are issues during the conversion process
- Any system-level errors occur during processing
