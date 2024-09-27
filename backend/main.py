from fastapi import FastAPI, Response, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from video_code import video_code
import json
import zipfile
from starlette.responses import FileResponse
from fastapi.responses import JSONResponse
import os

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins= ["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
 
@app.get("/")
async def read_root():
    return{"root":"Accessed successfully"}

 
@app.get("/download") 
async def download(url: str) -> Response:
    
    file_path, file_name_list = video_code.download(url)
    print(file_path)
    response_data = {"Song Names": file_name_list}  # Create a dictionary with the response data
    return Response(content=json.dumps(response_data), media_type="application/json")  # Return JSON response



@app.get("/zip_download")
async def generate_zip_file(background_tasks: BackgroundTasks):
    download_dir = "./Downloads"
    zip_filename = "./Downloads/downloaded_songs.zip"

    # Get a list of all files in the Downloads folder
    files = [f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
    total_files = len(files)

    if total_files == 0:
        return JSONResponse(content={"message": "No files found in the Downloads folder."}, status_code=404)

    # Create a zip file and write all files into it with progress
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for i, file in enumerate(files):
            file_path = os.path.join(download_dir, file)
            zipf.write(file_path, arcname=file)  # Use arcname to store just the filename, not the full path
            print(f"Zipping file {i + 1} of {total_files}: {file}")

    print("All files zipped successfully!")

       # Delete the ZIP file after response
    def cleanup():
        os.remove(zip_filename)
        print(f"Deleted {zip_filename}")
        
        # Delete the individual files that were zipped
        for file in files:
            file_path = os.path.join(download_dir, file)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

    background_tasks.add_task(cleanup)
    
    # Return a downloadable URL for the zip file
    return FileResponse(zip_filename, media_type="application/octet-stream", filename="downloaded_songs.zip")

