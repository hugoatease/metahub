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

class Fetcher:
#Parent-class for the site-specific fetching modules
    def __init__(self, artist, title):
        artist = artist.encode('utf-8')
        title = title.encode('utf-8')
        self.artist = artist
        self.title = title
        
    def unicode(self, lyric):
        if lyric != None:
            ulyric = lyric.decode('utf-8')
            ulyric = unicode(ulyric)
            return ulyric
        else:
            return None
        
    def get(self):
        return self.lyrics
 
class API:
    def __init__(self, artist, title, sources=None):
        import metahub, sing365
        if sources == None:
            self.sources = [metahub, sing365]
        self.artist = artist
        self.title = title

    def get(self):
        for source in self.sources:
            api = source.Fetch(self.artist, self.title)
            results = api.get()
            if results != None:
                if len(results) > 1:
                    self.results = results
                    self.siteID = source.__siteID__
                    self.version = source.__version__
                    break
        try:
            return self.results
        except:
            self.results = None
            self.siteID = None
            self.version = None
            return None

if __name__ == '__main__':
    artist = raw_input('Artist: ')
    title = raw_input('Title: ')
    api = API(artist, title)
    api.get()
    print api.results
    print 'SiteID: ', api.siteID
    print 'Version: ', api.version
    print type(api.results)