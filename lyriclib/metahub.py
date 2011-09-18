#!/usr/bin/python
'''TuneHub Lyrics Library.
    Copyright (C) 2011  Hugo Caille
    
    Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:
    1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
    2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer
    in the documentation and/or other materials provided with the distribution.
    3. The name of the author may not be used to endorse or promote products derived from this software without specific prior written permission.
    
    THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
    OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
    SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
    PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE
    OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
    '''
    
import lyricsapi
import urllib2

__siteID__ = 'MetaHub'
__version__ = 1
__author__ = 'Hugo Caille'

class Fetch(lyricsapi.Fetcher):
       
    def makeURL(self):
        artist = urllib2.quote(self.artist)
        title = urllib2.quote(self.title)
        url = 'https://tunehubmeta.appspot.com/get?artist=' + artist + '&title=' + title
        self.url = url
        return url

    def getLyric(self):
        url = self.makeURL()
        try:
            page = urllib2.urlopen(url)
            lyrics = page.read()
            if len(lyrics) < 6:
                lyrics = None
        except:
            lyrics = None
        
        self.lyrics = lyrics
        return lyrics
    
    def get(self):
        self.getLyric()
        if self.lyrics == None:
            return None
        else:
            lyrics = self.unicode(self.lyrics)
            return lyrics
    
if __name__ == '__main__':
    artist = raw_input('Artist: ')
    title = raw_input('Title: ')
    api = Fetch(artist, title)
    print api.get()
    print type(api.lyrics)