import os
import shutil
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.responses import FileResponse
from pdf2image import convert_from_bytes
import tempfile
from pathlib import Path

app = FastAPI(title="PDF to PNG Converter")

@app.post("/convert/")
async def convert_pdf_to_png(background_tasks: BackgroundTasks, pdf_file: UploadFile = File(...)):
    temp_dir = "/temp"  # Use the mounted directory
    png_dir = Path(temp_dir) / "pngs"
    png_dir.mkdir(parents=True, exist_ok=True)
    zip_dir = Path(temp_dir) / "zip"
    zip_dir.mkdir(parents=True, exist_ok=True)
    zip_path = zip_dir / "images.zip"
    
    pdf_content = await pdf_file.read()
    
    try:
        images = convert_from_bytes(pdf_content)
        for i, image in enumerate(images):
            image_path = png_dir / f"page_{i + 1}.png"
            image.save(str(image_path), "PNG")
        
        # Create ZIP file
        shutil.make_archive(str(zip_path.with_suffix('')), 'zip', str(png_dir))
        zip_file_path = zip_path.with_suffix('.zip')

        # Check if the ZIP file exists before attempting to return it
        if not zip_file_path.exists():
            return {"error": "ZIP file was not created successfully."}

        # Schedule cleanup of temporary files after response is sent
        background_tasks.add_task(cleanup_temp_files, temp_dir)

        return FileResponse(
            path=str(zip_file_path),
            filename="converted_images.zip",
            media_type="application/zip"
        )
    except Exception as e:
        return {"error": str(e)}

def cleanup_temp_files(temp_dir):
    # Iterate over all files and directories within temp_dir
    for filename in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, filename)
        try:
            # Check if it's a file or a directory
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or link
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Recursively remove directories
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 