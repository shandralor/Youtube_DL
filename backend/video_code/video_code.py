import os
from pytubefix import YouTube, Playlist
from pytubefix.cli import on_progress
import time
import random

def download_video(video_url, output_directory):
    retry = 0
    max_retries = 3

    while retry < max_retries:
        try:
            yt = YouTube(video_url, client='WEB_CREATOR', on_progress_callback=on_progress)
            ys = yt.streams.get_audio_only()
            print(f'Downloading video: {yt.title}')
            ys.download(output_path=output_directory, mp3=True)
            return ys.title

        except Exception as e:
            print(f'An error occurred: {e}')

            # Wait for a random interval between 1-5 seconds before retrying
            time.sleep(random.uniform(1, 5))

            retry += 1

def download(url=None):
    if url is None:  # If no URL was passed, prompt the user to enter one
        url = input('Enter the URL of the YouTube video or playlist: ')
        
    playlist_passed = 'playlist' in url
    song_names = []

    output_dir = os.path.join(os.getcwd(), 'Downloads') 

    if not os.path.exists(output_dir):  
        os.makedirs(output_dir)
    try:
        if playlist_passed:
            
            print('Downloading playlist')
            pl = Playlist(url, client='WEB_CREATOR')                     
            
            for video_url in pl.video_urls:
               
                title = download_video(video_url, output_dir)
                song_names.append(title) 
        else:
            title = download_video(url, output_dir)
            song_names.append(title)
    except Exception as e:
        print(f'An error occurred: {e}')
        song_names.append(f"Error downloading {title}")
    
    print('Download complete.')   
    return(output_dir, song_names )
    