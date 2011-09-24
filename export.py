'''This script allows CSV exporting of lyrics.
To retrieve lyrics from this script, client should make a POST request
containing a CSV file with rows : Artist, Title'''

import cgi #Used to retrieve client parameters.
import datastore #Used to retrieve lyrics from GAE DataStore
import csv #Used to parse and write CSV

import zlib

class VirtualFile:
    '''This class aims has a similar behaviour as file() object. It's used as an interface for csv module in writing operations.'''
    def __init__(self):
        self.csv = str()
        
    def write(self, str):
        self.csv = self.csv + str
            
    def get(self, compress=True):
        if compress:
            csvdata = zlib.compress(self.csv)
        else:
            csvdata = self.csv
        return csvdata

def stripinput(str):
    lines = str.split('\n')
    inputlist = []
    for line in lines:
        line = line + '\n'
        inputlist.append(line)
    return inputlist

class Export:
    
    def __init__(self, filter):
        self.filter = filter
        self.store = datastore.Store()
        
    def getData(self):
        results = []
        for item in self.filter:
            data = self.store.get(item['Artist'], item['Title'])
            results.append(data)
        
        self.results = results
        return results
        
    def parse(self, results):
        data = []
        for item in results:
            try:
                dic = {'Artist' : item.artist, 'Title' : item.title, 'Lyric' : item.lyric, 'SiteID' : item.siteID, 'date' : item.date}
                print dic
                data.append(dic)
            except:
                pass
            
        return data
    
    def writecsv(self, data, compress = True):
        file = VirtualFile()
        csvapi = csv.writer(file)
        csvapi.writerow(['Artist', 'Title', 'Lyric', 'SiteID', 'date'])
        
        for item in data:
            try:
                csvapi.writerow([item['Artist'], item['Title'], item['Lyric'], item['SiteID'], item['date']])
            except:
                pass
            
        csvdata = file.get(compress)
        return csvdata
    
    def run(self):
        results = self.getData()
        data = self.parse(results)
        csvdata = self.writecsv(data, compress = False)
        return csvdata
    
class Filter:
    def __init__(self, inputcsv):
        self.csv = inputcsv
    
    def readcsv(self):
        csvapi = csv.reader(stripinput(self.csv))
        toc = csvapi.next()
        if toc[0] == 'Artist':
            first = 'Artist'
        elif toc[0] == 'Title':
            first == 'Title'
        else:
            print 'Wrong CSV inputed. Please try again with "Artist" as first row and "Title" as second.'
        
        results = []
        for line in csvapi:
            try:
                if first == 'Artist':
                    data = {'Artist' : line[0], 'Title' : line[1]}
                if first == 'Title':
                    data = {'Artist' : line[1], 'Title' : line[0]}
            
                results.append(data)
            except:
                pass
                
        return results
    
form = cgi.FieldStorage()
inputcsv = form['csv'].value
filterapi = Filter(inputcsv)
filter = filterapi.readcsv()
exportapi = Export(filter)
print exportapi.run()