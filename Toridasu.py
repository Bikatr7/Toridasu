## built-in modules
import os
import time

## third-party modules
import pytube
import pytube.cli

##-------------------start-of-clear_console()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def clear_console():

    """

    Clears the console screen\n

    Parameters:\n
    None\n

    Returns:\n
    None\n
    
    """

    os.system('cls' if os.name == 'nt' else 'clear')

##-------------------start-of-create_playlist_folder()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def create_playlist_folder(playlist_title):

    """
    
    Creates a folder on the desktop with the playlist title\n

    Parameters:\n
    playlist_title (str): The title of the playlist\n

    Returns:\n
    playlist_folder (str): The path of the playlist folder\n

    """

    sanitized_title = playlist_title.replace('/', '_')

    playlist_folder = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop', sanitized_title)

    os.makedirs(playlist_folder, exist_ok=True)

    return playlist_folder

##-------------------start-of-download_video()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def download_video(url, destination):

    """

    Downloads a video from a given url in a playlist\n

    Parameters:\n
    url (str): The url of the video\n

    Returns:\n
    None\n

    """

    try:

        yt = pytube.YouTube(url, on_progress_callback=pytube.cli.on_progress)
        video = yt.streams.get_highest_resolution()

        video.download(destination)

        print("Downloaded: ", yt.title)

    except:
        print("Failed to download: ", url)

##-------------------start-of-download_playlist()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def download_playlist(playlist_url):

    """

    Downloads all videos in a playlist\n

    Parameters:\n
    playlist_url (str): The url of the playlist\n

    Returns:\n
    None\n

    """

    playlist = pytube.Playlist(playlist_url)
    clear_console()
    playlist_folder = create_playlist_folder(playlist.title())
    
    for video_url in playlist.video_urls:
        download_video(video_url, playlist_folder)
    
    print("\nAll videos have been downloaded successfully in the playlist folder!")

##-------------------start-of-download_single_video()-----------------------------------------------------------------------------------------------------------------------------------------------------------

def download_single_video(video_url):

    """

    Downloads a single video not in a playlist\n

    Parameters:\n
    video_url (str): The url of the video\n

    Returns:\n
    None\n

    """

    yt = pytube.YouTube(video_url, on_progress_callback=pytube.cli.on_progress)

    clear_console()

    video = yt.streams.get_highest_resolution()

    video.download(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop'))

    print("Downloaded: ", yt.title)

##-------------------start-of-main()-----------------------------------------------------------------------------------------------------------------------------------------------------------
os.system("title " + "Toridasu")

time.sleep(.2)

link = input("Please enter the link of the YouTube video or playlist you wish to download\n")

try:

    if("playlist?list=" in link):
        download_playlist(link)
    else:
        download_single_video(link)
except:
    print("\nVideo or Playlist is Invalid or Unavailable\n")
