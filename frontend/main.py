import streamlit as st
import json
import requests
import os

@st.fragment
def create_download_buttons(response_list):
    for song in json.loads(response_list.text):
            if os.path.isfile(song):  # Check if the file exists locally
                with open(song, 'rb') as file:
                    st.download_button(song[12:-4], file, key=song, file_name=song[12:])
            else:
                st.error(f"File {song} not found on server.")


st.title("Easy Youtube Downloader")
st.divider()

video_url = str(st.text_input("Enter the Youtube video URL", key="url"))

if not "songs_available" in st.session_state:
    st.session_state["songs_available"] = False

if st.button("Get songs"):
    with st.spinner():  # Display spinner while fetching data
        response = requests.get("http://api:8000/download", params={"url": video_url})

        if response.status_code == 200:  # Check if the request was successful
            st.session_state["songs_available"] = True  # Set the session state variable to indicate that songs are available   
            
            result = json.loads(response.text)
            song_names = result['Song Names']  # Retrieve the 'Song Names' list from the JSON response
            for song in song_names:  # Iterate over each song name and display it
                st.write(song) 
           
            
                
        else:
            st.error(f"Failed to download video. Status code: {response.status_code}")
    
st.divider()

if st.button("Download ZIP", disabled=not st.session_state["songs_available"]):
    with st.spinner("Zipping files..."):
        response = requests.get("http://api:8000/zip_download" )
        
        if response.status_code == 200:
            # Save the zip file content as a file
            zip_filename = "downloaded_songs.zip"
            
            with open(zip_filename, "wb") as f:
                f.write(response.content)
            
            # Provide a download button for the zip file
            with open(zip_filename, "rb") as f:
                st.download_button(
                    label="Download ZIP File",
                    data=f,
                    file_name=zip_filename,
                    mime="application/octet-stream"
                )
        else:
            st.error("Failed to download the zip file.")
        
       



