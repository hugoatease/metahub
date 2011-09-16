import cgi
import sing365
import datastore
storeapi = datastore.Store()
form = cgi.FieldStorage()

try:
	title = form['title'].value
	artist = form['artist'].value
	error = False
except KeyError:
	error = True

def site():
	global artist, title
	api = sing365.Sing365(artist, title)
	lyric = api.getLyric()
	storeapi.add(artist, title, lyric, siteID='Sing365', siteVersion=sing365.__version__)
	print lyric

if error == False:
	data = storeapi.get(artist, title)
	is_data = False
	has_lyric = False
	if data != None:
		print data.lyric
		is_data = True
		has_lyric = True
	
	if is_data:
		if data.siteVersion < sing365.__version__:
			if has_lyric != True:
				site()
	else:
		if has_lyric != True:
			site()