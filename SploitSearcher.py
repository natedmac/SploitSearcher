#! /usr/bin/python
#SploitSearcher.py
#url for search http://www.exploit-db.com/search/?action=search&filter_page=1&filter_description=&filter_exploit_text=%s&filter_author=&filter_platform=0&filter_type=0&filter_lang_id=0&filter_port=&filter_osvdb=&filter_cve= (%searchstring)
#%20 for url encoded space.
#url for downloading archive - http://www.exploit-db.com/archive.tar.bz2

import sys,os,urllib,re,csv


try:
    import bs4
except:
    print "Failed to load beautifulsoup4. Use easy_install beautifulsoup4 to install it"
try:
    import mechanize
except:
    print "Failed to load mechanize. Use easy_install mechanize to install it"
try:
    import argparse
except:
    print "Failed to load argparse. Use easy_install argparse to install it"

parser = argparse.ArgumentParser(description="This tool is designed to search the Exploit-DB archives locally. However it does have the option to search the site. Site searching should only be used when a local copy of the archive cannot be installed.")
parser.add_argument("-r", "--remote", action="store_true", dest="remote", help="This is to provide remote search functionality. This is only to be used when you cannot search a local copy of the db. This only is a freetext search.")
parser.add_argument("-s", "--Searchterm", action="store", dest="Searchterm", help="This is the searchterm for what you are looking for.")
parser.add_argument("--install", action="store_true",dest="install",help="This will download and extract a local copy of the exploitDB to where the script was ran. Create a subfolder for this script and archive to be installed to.")
parser.add_argument("-l","--local",action="store_true",dest="local",help="This will search the localcopy of the archive and return the exploit information")
args = parser.parse_args()



def main():
  if args.remote is True:
		searchExploitDB()
	if args.install is True:
		installDB()
	if args.local is True:
		localsearch()


def searchExploitDB():
	url = "http://www.exploit-db.com/search/?action=search&filter_page=1&filter_description=&filter_exploit_text=%s&filter_author=&filter_platform=0&filter_type=0&filter_lang_id=0&filter_port=&filter_osvdb=&filter_cve=" % (args.Searchterm)
	br = mechanize.Browser()
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	response = br.open(url)
	soup = bs4.BeautifulSoup(response.read())
	
	for vulns in soup.find_all('a'):
		description = re.search(r'<a href="(http://www.exploit-db.com/exploits/.+)">(.+)</a>',str(vulns))
		if description:
			print description.group(2)
			print description.group(1)
	
		
		
def installDB():
	urllib.urlretrieve("http://www.exploit-db.com/archive.tar.bz2", "archive.tar.bz2")
	os.system("tar -jxvf archive.tar.bz2")
	os.system("chmod +r files.csv")


def localsearch():
	searchdata = str(args.Searchterm)
	data = csv.reader(open('files.csv'))
	fields = data.next()
	for row in data:
		if searchdata.lower() in str(row[2]).lower() :
			results = "Description: " + row[2] + " Affected Platform: " + row[5] + " Port: " + row[7] + "\nFile: " + row[1] +"\n"
			print results

if __name__ == "__main__":
    main()
