import cgi
import sing365

form = cgi.FieldStorage()
try:
	title = form['title'].value
	artist = form['artist'].value
	error = False
except KeyError:
	error = True

if error == False:
	api = sing365.Sing365(artist, title)
	print api.getLyric()
