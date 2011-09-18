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
import urllib
import urllib2

__siteID__ = 'Sing365'
__version__ = 1
__author__ = 'Hugo Caille'

class Fetch(lyricsapi.Fetcher):

    def keywords(self):
        self.keywords = self.artist + ' ' + self.title

    def search(self):
        keywords = self.keywords
        
        quoted = urllib.quote_plus(keywords)
        
        opener = urllib2.build_opener()
        headers = [('Referer', 'http://sing365.com/index.html'), ('Host', 'seek.sing365.com'), ('Accept-Language', 'en;q=1.0'), ('Accept-Encoding', 'gzip, compress, bzip, bzip2, deflate'), ('Accept', 'text/html, text/*;q=0.5, image/*'), ('User-Agent', 'w3m/0.5.3')]
        opener.addheaders = headers
        
        url = 'http://seek.sing365.com/cgi-bin/s.cgi?q=' + quoted + '&submit=go'
        request = opener.open(url)
        
        data = request.read()
        opener.close()
        
        toreturn = {'url': url, 'data': data}
        self.searchurl = url
        self.searchdata = data
        return toreturn
    
    def parseSearch(self):
        data = self.searchdata
        results=True
        result1 = None
        
        table = data.split('<table>')
        try:
            table = table[1]
            result1 = table.split('<td><b>1.</b></td>')
        except IndexError:
            results = False
            result1 = None
        
        
        try:
            if result1 != None:
                result1 = result1[1]
            else:
                results = False
        except IndexError:
            results = False
        
        if results == True:    
            link1 = result1.split('/music/lyric.nsf/')
            link1part1 = link1[0]
            link1part2 = link1[1]
            link1part1 = link1part1.split('<a href="')
            part1 = link1part1[1]
            
            link1part2 = link1part2.split('"')
            
            part2 = link1part2[0]
        
            url = part1 + '/music/lyric.nsf/' + part2
            
            self.lyricurl = url
            return url
        else:
            self.lyricurl = None
            return None
    
    def getLyricUrl(self):
        if self.lyricurl != None:
            lyricurl = self.lyricurl
            searchurl = self.searchurl
            
            opener = urllib2.build_opener()
            headers = [('Referer', searchurl), ('Host', 'www.sing365.com'), ('Accept-Language', 'en;q=1.0'), ('Accept-Encoding', 'gzip, compress, bzip, bzip2, deflate'), ('Accept', 'text/html, text/*;q=0.5, image/*'), ('User-Agent', 'w3m/0.5.3')]
            opener.addheaders = headers
            
            request = opener.open(lyricurl)
            data = request.read()
            request.close()
            
            self.lyricdata = data
            return data
        
        else:
            self.lyricdata = None
            return None

    
    def parseLyricPage(self):
        if self.lyricdata != None:
            data = self.lyricdata
            trim = data.split('<img src=http://www.sing365.com/images/phone2.gif border=0><br><br>')
            try:
                trim = trim[1]
                trim = trim.split('<br><img src=')
                html = trim[0]
                lines = html.split('<br>')
                lyrics = ''
                
                for line in lines:
                    lyrics = lyrics + line
                
                self.lyrics = lyrics
                return lyrics
            except:
                self.lyrics = None
                return None
        else:
            self.lyrics = None
            return None
        

    
    def get(self):
        try:
            self.keywords()
            self.search()
            self.parseSearch()
            self.getLyricUrl()
            self.parseLyricPage()
            lyrics = self.unicode(self.lyrics)
        except:
            lyrics = None
        return lyrics
        
if __name__ == '__main__':
    artist = raw_input('Artist: ')
    title = raw_input('Title: ')
    api = Fetch(artist, title)
    print api.get()