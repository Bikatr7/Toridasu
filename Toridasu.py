import datetime
import os
import time
import pytube
import pytube.cli

# Global counters and list for tracking downloads
total_downloads = 0
failed_downloads = []

##-------------------start-of-clear_console()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def clear_console() -> None:

    """

    Clears the console screen.

    """

    os.system('cls' if(os.name == 'nt') else 'clear')

##-------------------start-of-create_playlist_folder()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def create_playlist_folder(playlist_title:str) -> str:

    """

    Creates a folder on the desktop with the playlist title.

    Parameters:
    playlist_title (str) : The title of the playlist.

    Returns:
    playlist_folder (str) : The path of the playlist folder.

    """

    sanitized_title = playlist_title.replace('/', '_')

    playlist_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', sanitized_title)

    os.makedirs(playlist_folder, exist_ok=True)

    return playlist_folder

##-------------------start-of-download_video()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def download_video(url:str, destination:str, download_number:int) -> None:

    """

    Downloads a video from a given url in a playlist.

    Parameters:
    url (str) : The url of the video.
    destination (str) : The destination folder for the video.
    download_number (int) : The sequence number of the download.

    """

    global total_downloads

    try:

        yt = pytube.YouTube(url, on_progress_callback=pytube.cli.on_progress)
        video = yt.streams.get_highest_resolution()

        assert video != None

        ## Generate a unique filename to avoid overwriting
        base_filename = video.default_filename.rsplit('.', 1)[0]
        file_extension = video.default_filename.rsplit('.', 1)[1]
        unique_filename = f"{base_filename}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.{file_extension}"
        
        ## Check if file already exists
        if(not os.path.exists(os.path.join(destination, unique_filename))):

            video.download(destination, filename=unique_filename, skip_existing=False, max_retries=5)
            print(f"Downloaded ({download_number}): ", yt.title)
            total_downloads += 1

        else:
            print(f"File already exists, skipping ({download_number}) : ", yt.title)

    except Exception as e:
        print("Failed to download: ", url, "due to ", str(e))
        failed_downloads.append(url)

##-------------------start-of-download_playlist()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def download_playlist(playlist_url:str) -> None:

    """

    Downloads all videos in a playlist.

    Parameters:
    playlist_url (str) : The url of the playlist.

    """

    playlist = pytube.Playlist(playlist_url)

    clear_console()

    playlist_folder = create_playlist_folder(playlist.title)

    download_number = 1

    for video_url in playlist.video_urls:
        download_video(video_url, playlist_folder, download_number)
        download_number += 1

    print(f"\nTotal videos downloaded: {total_downloads}")

    if(failed_downloads):
        print(f"\nFailed downloads ({len(failed_downloads)}):")
        for failed_url in failed_downloads:
            print(failed_url)

##-------------------start-of-download_single_video()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def download_single_video(video_url:str) -> None:

    """

    Downloads a single video not in a playlist.

    Parameters:
    video_url (str ): The url of the video.

    Returns:
    None
    """

    clear_console()

    destination = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')

    download_video(video_url, destination, 1) ## download_number is 1 because it is a single video

    print(f"\nTotal videos downloaded: {total_downloads}")

    if(failed_downloads):
        print(f"\nFailed downloads ({len(failed_downloads)}):")

        for failed_url in failed_downloads:
            print(failed_url)

##-------------------start-of-main()-----------------------------------------------------------------------------------------------------------------------------------------------------------

os.system("title " + "Toridasu")

time.sleep(.2)

link = input("Please enter the link of the YouTube video or playlist you wish to download\n")

try:

    assert link != "q"

    if("playlist?list=") in link:
        download_playlist(link)
    else:
        download_single_video(link)

except AssertionError:
    exit()
    
except Exception as e:
    print("\nVideo or Playlist is Invalid or Unavailable\n\n" + str(e))

os.system('pause')
