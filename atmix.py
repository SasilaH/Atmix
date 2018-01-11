import pprint
import sys
import time
from datetime import date
from random import randint

import spotipy
import spotipy.util as util


today = str(date.today())
PName = "Today's Atmix (%s)" % (today)




if len(sys.argv) > 1:
    username = sys.argv[1]
else:
    print("Invalid Input! Usage: %s username" % (sys.argv[0]))
    sys.exit()

print("Thanks for using Atmix!\n")

print("Please rank the following types of locations based on how much time you would spend at each of them today.\n")

print("Locations can be ranked from 0 to 5 (with 5 being the largest).\n")



#rHome = float(input("How much time will you spend at Home today? [Enter 0 to 5]: "))
rPTransport = float(input("How much time will you spend on Transportation today? [Enter 0 to 5]: ")) 
rOffice = float(input("How much time will you spend at an Office today? [Enter 0 to 5]: "))
rGym = float(input("How much time will you spend at the Gym today? [Enter 0 to 5]: "))
rSchool = float(input("How much time will you spend at School (or any other Educational Setting) today? [Enter 0 to 5]: "))


Sum = rPTransport + rOffice + rGym + rSchool #+ rHome
#wHome = rHome/Sum
WPTransport = rPTransport/Sum
wOffice = rOffice/Sum
wGym = rGym/Sum
wSchool = rSchool/Sum



scope = 'playlist-modify-public playlist-modify-private user-follow-modify user-follow-read playlist-read-collaborative'
token = util.prompt_for_user_token(username,scope)

if token:
    sp = spotipy.Spotify(auth=token)
    sp.trace = False



    newPlaylist = sp.user_playlist_create(username, PName, public=True)
    playlistID = newPlaylist['id']
    trackList = []

    print("\nAtmix will now generate an atmospheric playlist based on your preferences.\n")

    def tracks(Index, weight):
    	Tlist = []
    	
    	RecReference = ['Home', 'road-trip', 'chill', 'work-out', 'study']
    	NonRecReference = ['Home', 'travel', 'chill', 'workout', 'focus']
    	CatName = RecReference[Index]
    	catListsID = NonRecReference[Index]
    	
    	playlistSize = randint(40,50)
    	
    	RecSeeds = sp.recommendation_genre_seeds()
    	SeedList = RecSeeds['genres']    	
    	
    	if (CatName == 'Home'):
    		Toptracks = sp.current_user_top_tracks(limit=100, offset=0, time_range='medium_term')

    		for x in range(1,(int(weight*playlistSize))):
    			HomeRand = randint(0,99)
    			for i, item in enumerate(Toptracks['items']):
    				if (i == HomeRand and not item['id'] in Tlist):
    					Tlist.append(item['id'])
    					break
    				elif (i == HomeRand and item['id'] in Tlist):
    					HomeRand = randint(0,99)


    	elif (CatName in SeedList):
    		catRec = sp.recommendations(seed_artists=None, seed_genres=[CatName], seed_tracks=None, limit=100, country=None)

    		for x in range(1,(int(weight*playlistSize))):
    			RecRand = randint(0,99)
    			for i, item in enumerate(catRec['tracks']):
    				if (i == RecRand and not item['id'] in Tlist):
    					Tlist.append(item['id'])
    					break
    				elif (i == RecRand and item['id'] in Tlist):
    					CatRand = randint(0,99)
    	
    	else:
    		catLists = sp.category_playlists(category_id=catListsID, country=None, limit=20, offset=0)

    		listNo = randint(0,19)
    			
    		for i, item in enumerate(catLists['playlists']['items']):
    			if i == listNo:
    				importPlayID = item['id']
    				importUserID = item['owner']['id']
    				listsongs = sp.user_playlist_tracks(importUserID, importUserID)
    				
    				for x in range(1,(int(weight*playlistSize))):
    					songRand = randint(0,50)
    					for i, item in enumerate(listsongs['items']['track']):
    						if (i == songRand and not item['id'] in Tlist):
    							Tlist.append(item['id'])
    							break
    						elif (i == songRand and item['id'] in Tlist):
    							songRand = randint(0,50)

    	return Tlist

    #trackList += tracks(0,wHome)
    print("(Doing the dishes...)\n")
    trackList += tracks(1,WPTransport)
    print("(Stuck in trafic...)\n")
    trackList += tracks(2,wOffice)
    print("(Finishing a team project...)\n")
    trackList += tracks(3,wGym)
    print("(Setting new workout goals...)\n")
    trackList += tracks(4,wSchool)
    print("(Studying hard...)\n")

    sp.user_playlist_add_tracks(username, playlistID, trackList, position = 0)

    print("And we're done.\n")
    print("Enjoy!\n")


else:
    print("Can't get token for", username)


