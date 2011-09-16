from google.appengine.ext import db
class Store:
#The Store class allows to wrap common lyric's storage operations with the GAE Datastore

    def add(self, artist, title, lyric, siteID=None, siteVersion=None):
        #add function must be call to add a lyric in the lyrics database
        #siteID should be an identifier for the site where the lyrics come from
        #siteVersion must be these site python API version.
        api = Lyrics()
        api.artist = artist
        api.title = title
        api.lyric = lyric
        api.siteID = siteID
        api.siteVersion = siteVersion
        api.put()
    
    def get(self, artist, title):
        #Retrieve the lyrics from the datastore
        query = db.GqlQuery('SELECT * FROM Lyrics WHERE artist = :1 AND title = :2', artist, title)
        result = query.fetch(query.count(None))
        count = len(result)
        try:
            return result[count-1]
        except:
            return None

class Lyrics(db.Model):
    #Lyrics table, heritates from GAE API.
    artist = db.StringProperty()
    title = db.StringProperty()
    lyric = db.TextProperty()
    siteID = db.StringProperty()
    siteVersion = db.IntegerProperty()