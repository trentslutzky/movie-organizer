import eel
import os
import sys

movie_file_types = ['mp4','mkv']

@eel.expose
def launchMovie(movie):
    # get movie file from folder
    movie_folder = 'H:\Movies\\'+movie+'\\'
    files = os.listdir(movie_folder)
    movie_path = ''
    for file in files:
        file_str = str(file)[-3:]
        if(file_str in movie_file_types):
            movie_path = 'H:\Movies\\'+movie+'\\'+file
            print(movie_path)
    print(movie_path)
    os.system('vlc -f '+'"'+movie_path+'"')
    

eel.init('site')
eel.start('index.html',size=(1000,1200))