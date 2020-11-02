from imdb import IMDb
from time import sleep
import os
import urllib.request
import json
import argparse
from colorama import init,Fore
from shutil import copyfile

path = 'H:\Movies'

# create an instance of the IMDb class
ia = IMDb()

refresh = True

def scan_library():
    print(Fore.YELLOW + 'SCANNING MOVIE LIBRARY ' + path + Fore.RESET)

    movies = os.listdir(path)

    for f_movie in movies:
        # current path for movie
        current_path = 'H:\Movies\\'+str(f_movie)
        # check if it is a movie folder
        if(os.path.isdir(current_path)):
            # check for cover art in folder
            files = os.listdir(current_path)
            if('info.json' in files and not refresh):
                print(Fore.CYAN + f_movie + Fore.YELLOW)
                print('    Already Scanned!')
            
            else:
                print(Fore.CYAN + f_movie + Fore.RESET)
                vid_file = os.listdir(current_path)[0]
                title = str(f_movie)
                imdb_search = ia.search_movie(title)
                movie_id = imdb_search[0].movieID
                movie = ia.get_movie(movie_id)

                try: rating = movie['rating']
                except: rating = ''
                try: year = movie['year']
                except: year = ''
                try: director = str(movie['director'][0])
                except: director = ''
                try: cast = (str(movie['cast'][0])+', '
                                +str(movie['cast'][1])+', '
                                +str(movie['cast'][2]))
                except: cast = ''
                try: 
                    plot = str(movie['plot'][0])
                    plot = plot.split('::')[0]
                except: plot = ''
                
                #initialize dict
                movie_dict = {
                    'title':str(f_movie),
                    'year':year,
                    'id':movie_id,
                    'rating':rating,
                    'director':director,
                    'cast':cast,
                    'plot':plot
                }
                
                json_path = current_path+'\info.json'
                with open(json_path, 'w') as outfile:  
                    json.dump(movie_dict, outfile) 
    jsifyMovies()

def updateCoverImages():
    movies = os.listdir(path)
    site_covers_path = 'H:\movie-organizer\site\covers'
    covers_js_path = 'H:\movie-organizer\site\covers.js'

    # open the covers js file for reference inside the js app
    c = open(covers_js_path,"w")
    c.write('covers = [\n')

    for f_movie in movies:
        # get path to movie folder then image name
        cover_path = site_covers_path + '\\' + str(f_movie) + '.jpg'
        image_file = str(f_movie)+'.jpg'
        cover_path_etc = "    'covers/"+image_file+"',\n"
        
        c.write(cover_path_etc)        

        # convert to string array for logic
        covers = os.listdir(site_covers_path)
        str_covers = []
        for cov in covers:
            str_covers.append(str(cov))

        #no cover image in folder? download from imdb
        if (image_file not in str_covers):
            print(Fore.GREEN,'Add Image: ',cover_path)
            imdb_search = ia.search_movie(f_movie)
            movie_id = imdb_search[0].movieID
            movie = ia.get_movie(movie_id)
            try:
                cover = movie['cover url']
                urllib.request.urlretrieve(cover,cover_path)
            except:
                print(Fore.RED,'Cover not found! Using blank cover.')
                copyfile('H:\movie-organizer\\blank.jpg', cover_path)
        
        else:
            print(Fore.CYAN + 'covers/'+image_file + Fore.RESET + ' exists!')

    c.write(']')
    c.close()

def updateLargeCoverImages():
    movies = os.listdir(path)
    site_covers_path = 'H:\movie-organizer\site\covers_l'
    covers_js_path = 'H:\movie-organizer\site\covers_l.js'

    # open the covers js file for reference inside the js app
    c = open(covers_js_path,"w")
    c.write('covers = [\n')

    for f_movie in movies:
        # get path to movie folder then image name
        cover_path = site_covers_path + '\\' + str(f_movie) + '.jpg'
        image_file = str(f_movie)+'.jpg'
        cover_path_etc = "    'covers_l/"+image_file+"',\n"
        
        c.write(cover_path_etc)        

        # convert to string array for logic
        covers = os.listdir(site_covers_path)
        str_covers = []
        for cov in covers:
            str_covers.append(str(cov))

        #no cover image in folder? download from imdb
        if (image_file not in str_covers):
            print(Fore.GREEN,'Add Image: ',cover_path)
            imdb_search = ia.search_movie(f_movie)
            movie_id = imdb_search[0].movieID
            movie = ia.get_movie(movie_id)
            try:
                cover = movie['full-size cover url']
                urllib.request.urlretrieve(cover,cover_path)
            except:
                print(Fore.RED,'Cover not found! Using blank cover.')
                copyfile('H:\movie-organizer\\blank.jpg', cover_path)
        
        else:
            print(Fore.CYAN + 'covers/'+image_file + Fore.RESET + ' exists!')

    c.write(']')
    c.close()

def jsifyMovies():
    movies = os.listdir(path)
    movies_js_path = 'H:\movie-organizer\site\movies.js'
    
    j = open(movies_js_path,"w")

    for movie in movies:
        # get variable name for jsifying
        movie_var = str(movie).replace(' ','_')
        movie_var=movie_var[:-7]

        # get movie info from json file in movie folder
        json_path = ('H:\\Movies\\'+movie+'\\info.json')
        f = open(json_path)
        info = json.load(f) # info
        f.close()

        # append the js array to the movies.js file
        j.write('Info_'+movie_var+'= [\n')
        j.write("    '"+info['title']+"',\n")
        j.write("    '"+str(info['year'])+"',\n")
        j.write("    '"+info['director']+"',\n")
        j.write("    '"+info['id']+"',\n")
        j.write("    '"+info['cast']+"',\n")
        j.write('    "'+info['plot']+'",\n')
        j.write(']\n\n')
    
    j.close()

def main():
    scan_library()

if __name__ == '__main__':
    main()