from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import io

#This script is used to scrape the Academy Rewards database for 
#nominees and winners in the Best Film and Best Animated Feature
#categories.  The Best Animated Feature category has only existed since
#2001, so we'll only pull winners from 2001 onwards.  
#The site we are scraping is mostly run via JavaScript, so we need to
#use Selenium to scrape the site.  Since we are using Selenium with
#Chrome, we will include the proper driver (chromedriver.exe) in the
#project directory.  For any other browser except Firefox, you will have 
#to download the appropriate driver and include it in the same folder 
#as this script. No driver is necessary if you decide to use Firefox.
#Whichever browser you use, replace webdriver.Chrome() below with
#Webdriver.<browser name>().  Chrome and Firefox are recommended.

browser = webdriver.Chrome() #replace with .Firefox(), or with the browser of your choice
url = "http://awardsdatabase.oscars.org/Search/GetResults?query=%7B%22AwardCategory%22:[%226%22,%2219%22],%22Sort%22:%223-Award%20Category-Chron%22,%22Search%22:%22Basic%22%7D"
browser.get(url) #navigate to the page
innerHTML = browser.execute_script("return document.body.innerHTML") #returns the inner HTML as a string
soup = BeautifulSoup(innerHTML)
with io.open("oscarsdata.csv", 'w', newline='', encoding="utf-8") as oscarfile:
	oscarwriter = csv.writer(oscarfile, delimiter=",")
	headings = ["movie", "year", "category", "nominee", "winner"]
	oscarwriter.writerow(headings)
	#For all divs with an attribute "awards-result-chron", which is the result for each year
	for result in soup.find_all("div", "awards-result-chron"): 
		year = int(result.div.div.a.text[0:4]) #get the year of the award ceremony
		if year < 2001:
			continue #skip this result if the year is before 2001
		for category in result.find_all("div", "result-subgroup"):
			catname = category.div.div.a.text
			for nominee in category.find_all("div", "result-details"):
				movie = nominee.div.div.div.a.text
				if nominee("span") == []:
					oscarwriter.writerow([movie]+[year]+[catname]+[1]+[0])
				else:
					oscarwriter.writerow([movie]+[year]+[catname]+[0]+[1])