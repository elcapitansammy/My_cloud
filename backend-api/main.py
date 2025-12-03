import cv2
from fastapi import FastAPI
from fastapi import File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
import os
import shutil
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

BASE_DIR = "C:/Users"  # safe base directory

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/list")
def list_files(path: str = ""):
    try:
        """List files in a directory relative to BASE_DIR."""
        full_path = os.path.join(BASE_DIR, path)
        return {"files": os.listdir(full_path)}
    except Exception as e:
        return {"error": str(e)}


@app.get("/read")
def read_file(path: str):
    try:
        """Read a file relative to BASE_DIR."""
        full_path = os.path.join(BASE_DIR, path)
        with open(full_path, 'r') as file:
            content = file.read()
        return {"content": content}
    except Exception as e:
        return {"error": str(e)}


@app.get("/download")
def download_file(path: str):
    """Return a file without forcing download (preview works)."""
    try:
        full_path = os.path.join(BASE_DIR, path)

        if not os.path.isfile(full_path):
            return JSONResponse({"error": "File not found"}, status_code=404)

        # No filename=... → Browser decides (preview allowed)
        return FileResponse(full_path)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)


@app.post("/delete")
def delete_file(path: str):
    try:
        """Delete a file or directory relative to BASE_DIR."""
        full_path = os.path.join(BASE_DIR, path)
        if os.path.isfile(full_path):
            os.remove(full_path)
            return {"status": "File deleted"}
        elif os.path.isdir(full_path):
            shutil.rmtree(full_path)
            return {"status": "Directory deleted"}
        else:
            return {"error": "File or directory not found"}
    except Exception as e:
        return {"error": str(e)}


@app.post("/upload")
async def upload_file(file: UploadFile = File(...), destination: str = ""):
    try:
        """Upload a file to a specified destination path in BASE_DIR."""
        destination_path = os.path.join(BASE_DIR, destination, file.filename)
        os.makedirs(os.path.dirname(destination_path), exist_ok=True)  # Ensure destination directory exists
        with open(destination_path, "wb") as buffer:
            buffer.write(await file.read())
        return {"status": "File uploaded", "filename": file.filename, "destination": destination_path}
    except Exception as e:
        return {"error": str(e)}
    
import tempfile


@app.get("/thumbnail")
def generate_thumbnail(path: str):
    try:
        full_path = os.path.join(BASE_DIR, path)

        if not os.path.isfile(full_path):
            return JSONResponse({"error": "File not found"}, status_code=404)

        ext = path.split(".")[-1].lower()
        if ext not in ["mp4", "mov", "avi", "mkv", "webm"]:
            return JSONResponse({"error": "Not a video"}, status_code=400)

        # Store thumbnails in a fixed cache folder inside BASE_DIR
        thumb_path = os.path.join(tempfile.gettempdir(), path.replace("/", "_") + ".png")
        os.makedirs(os.path.dirname(thumb_path), exist_ok=True)

        # Generate only if it doesn’t exist yet
        if not os.path.isfile(thumb_path):
            video = cv2.VideoCapture(full_path)
            video.set(cv2.CAP_PROP_POS_MSEC, 500)  # 0.5 second frame
            success, frame = video.read()
            if success:
                cv2.imwrite(thumb_path, frame)
            video.release()

        if not os.path.isfile(thumb_path):
            return JSONResponse({"error": "Could not generate thumbnail"}, status_code=500)

        return FileResponse(thumb_path)

    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
    
@app.post("/create-directory")
def create_directory(path: str):
    try:
        """Create a directory relative to BASE_DIR."""
        full_path = os.path.join(BASE_DIR, path)
        os.makedirs(full_path, exist_ok=True)
        return {"status": "Directory created", "path": full_path}
    except Exception as e:
        return {"error": str(e)}
