import cgi
import lyriclib

modstring = ''
for module in lyriclib.mods_version:
	modstring = modstring + str(module) + str(lyriclib.mods_version[module])
	
import datastore
storeapi = datastore.Store()
form = cgi.FieldStorage()

try:
	title = form['title'].value
	artist = form['artist'].value
	error = False
except KeyError:
	error = True

def site(artist, title):
	api = lyriclib.lyricsapi.API(artist, title, sources=[lyriclib.sing365])
	lyric = api.get()
	if lyric != None:
		storeapi.add(artist, title, lyric, siteID=api.siteID, siteVersion=modstring)
		printLyric(lyric, api.siteID)

def printLyric(lyric, source):
	if source != None and lyric != None:
		print '\nSource: ' + source + '\n'
		print lyric

if error == False:
	data = storeapi.get(artist, title)
	if data != None:
		#Si le datastore a des informations
		
		#On les recupere
		lyric = data.lyric
		siteID = data.siteID
		siteVersion = data.siteVersion

		#Si le siteVersion est different du modstring, on appelle site()
		if siteVersion != modstring:
			site(artist, title)
		else:
			#Si le siteVersion ne differe pas, on affiche
			printLyric(lyric, siteID)
	else:
		#Le datastore n'a pas de donnees
		site(artist, title)