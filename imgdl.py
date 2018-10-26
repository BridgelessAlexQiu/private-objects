from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from sys import platform
import csv

#Proof of concept flickr downloader using selenium webdriver. (pip install selenium)
#This assumes that the download link will be available which is not always the case.
#Should be further extended and automated to be able to dynamically take photo ids and download them.


#Set chromedriver path. Use exe if windows, binary if linux
driverPath = "./chromedriver.exe"
if platform.startswith('linux'):
    driverPath = "./chromedriver"
	
totalUndownloadable = 0 #Number of images with downloads disabled/unavailable.

browser = webdriver.Chrome(executable_path=driverPath) #Set the browser to use. 
print "Loading page"

#--------------------------Read CSV function--------------------------#
def read_csv(path : "csv file path") -> "dict - id : privacy setting":
	"""
	before calling this function.
	Make sure the category titles and extra lines at the end of the csv file is removed
	"""
	#dict - id : privacy setting
	id_privacy = {}
	with open(path) as f:
		reader = csv.reader(f, delimiter = '\t')
		for row in reader:
			id_privacy[row[0]] = row[3]
	return id_privacy

#--------------------download_img function-------------------------------#
def download_img(ids : "dict - id : privacy setting"):
	for key in ids:
		photoID = key
		browser.get('https://flickr.com/photo.gne?id='+photoID) #Navigate to the page by using the link that accepts only photo ids.

		newurl = browser.current_url #Get the new url. Navigating to the link above will ultimately resolve the url to its 'proper' url.
		newurl = newurl +"/sizes/o" #Append the url with the link to the original size (o) download page.
		browser.get(newurl) #Navigate there.

		downloadText = "Download the Original size of this photo" #This is the text on the download link.

		try:
		    browser.find_element_by_link_text(downloadText).click() #Click the link. Unless otherwise configured, chrome will save 
									    #this link automatically into the downloads folder.
		except:
		    print "Cannot download image " + photoID                #If the browser is unable to find this link, skip this image and document which id was unavailable.
		    totalUndownloadable = totalUndownloadable + 1

		#Print statistics regarding undownloadable images.
		print "Could not download " + str(totalUndownloadable) + " images. ("+str((totalUndownloadable/99281)*100)+"%)"

#Todo close the browser with browser.quit(). Doing so here quits the browser before the download is complete.
