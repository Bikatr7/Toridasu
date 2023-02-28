import os

from time import sleep
from pytube import YouTube
from pytube.cli import on_progress 

os.system("title " + "SYVD")


sleep(.2)

try: 
    gui.getWindowsWithTitle("SYVD")[0].minimize()
except:
    pass

link = input("Please enter the link of the youtube video you wish to download\n")

try:
    
    yt = YouTube(link,on_progress_callback=on_progress)
    os.system('cls')
    
except:
    
    print("\nVideo is Invalid or Unavailable\n")
    os.system('pause')
    exit()
          
else:
    video = yt.streams.get_highest_resolution()
    video.download(os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')) ## gets path to desktop
    print("(:")
