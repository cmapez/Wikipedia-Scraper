#pip install -r requirements.txt

import requests
from bs4 import BeautifulSoup as bs
import os
import re


#using beautifulsoup to scrape data
def Scrape(url,dtatext):

    data = requests.get(url).text

    soup = bs(data,"html.parser")


    #finding all paragraphs of text on wikipedia page
    for textdata in soup.find_all('p'):
        dtatext += str((textdata.getText())+"\n")

    return dtatext


#initialize scrape
def StartScrape():
    #base URL for wikipedia
    urlcore = "https://en.wikipedia.org/wiki/"

    searching = True

    while searching:
        article = input("Input Article Title: ")

        url = urlcore+article.lower()
        dtatxt=""
        errorstring = "Other reasons this message may be displayed:"
        #call scrape function to collect text from page
        newdata = Scrape(url,dtatxt)
        #check if page exists
        if errorstring not in newdata:
            print("Scrape successful!\n")
            searching = False
            return(newdata)
        else:
            print("Error, Webpage not found. Please Retry.\n")

#main for user selection and control
def Main():
    text = ""
    checkperiod = "."
    running = True
    #allows for multiple scrapes at a time
    while running:
        choice = input("Would you like to scrape ,save , print, analyze or quit ? ")
        #handles scraping
        if choice.lower() == "scrape":
            text = StartScrape()
        #saves data to a file of choosing
        elif choice.lower() == "save" and text:
            fname = input("What would you like to name this file? ")
            #if they do not clarify the file type it becomes a .txt file
            if checkperiod not in fname:
                fname += ".txt"
            file = open(os.getcwd() + "/" +fname,"w")
            #dump data to file
            file.write(text)
            file.close()
            #return output
            print("file saved as: " + fname + " to " + str(os.getcwd())+"\n")
        #prints website text
        elif choice.lower() == "print" and text:
            print(text)

        #returns number of occurences of most common words
        elif choice.lower() == "analyze" and text:
            print("Analysis of text: \n")
            
            d = dict()
            textdata = text.replace("\n"," ")
            textdata = re.sub(r"\([^[]]*\)", "", textdata)
            textdata = re.sub("[^\w\s]", "", textdata)
            textdata = textdata.upper()
            texttable = textdata.split(" ")
            for word in texttable:
                if word in d:
                    if word != " ":
                        d[word] = d[word]+1
                else:
                    d[word] = 1
            newdict = dict(sorted(d.items(),reverse=True,key=lambda item: item[1]))

            print("\nThe most common words in this article are: \n".upper())
            for i,key in enumerate(list(newdict.keys())):
                if(i < 10):
                    print(key, ":", newdict[key])
        #quits the program
        elif choice.lower() == quit:
            running = False
            return
        #error for if users have not scraped yet
        elif (choice.lower() == "save" or choice.lower() == "print" or choice.lower() == "analyze") and not text:
            print("Please Scrape Data First!\n")
        #error if false command is entered
        else:
            print("Sorry, that is not a command \n")




if __name__ == "__main__":
    Main()


