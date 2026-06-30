from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
import shutil
import subprocess
import uuid
from pathlib import Path
from fastapi import HTTPException
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/test")
def root():
    return {"status": "running"}


@app.post("/image-to-pdf/")
async def image_to_pdf(file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        temp_dir = Path("/tmp")
        unique_id = uuid.uuid4().hex
        input_path = temp_dir / f"{unique_id}_{file.filename}"
        output_path = temp_dir / f"{unique_id}.pdf"

        # Save uploaded file
        with open(input_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        logger.info(f"Processing image: {input_path}")
        
        # Run OCRmyPDF with more verbose output
        result = subprocess.run(
            ["ocrmypdf", "--image-dpi", "100", "--deskew", "--rotate-pages", "--verbose", "2", str(input_path), str(output_path)],
            capture_output=True,
            text=True,
            check=True
        )
        
        logger.info(f"OCR completed successfully: {output_path}")
        
        # Check if output file exists
        if not output_path.exists():
            raise HTTPException(status_code=500, detail="PDF file was not created")
        
        return FileResponse(
            output_path, 
            media_type="application/pdf", 
            filename="output.pdf"
        )

    except subprocess.CalledProcessError as e:
        logger.error(f"OCR failed with exit code {e.returncode}")
        logger.error(f"stdout: {e.stdout}")
        logger.error(f"stderr: {e.stderr}")
        raise HTTPException(
            status_code=500, 
            detail=f"OCR failed: {e.stderr or str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
    finally:
        # Clean up input file
        if 'input_path' in locals() and input_path.exists():
            input_path.unlink()