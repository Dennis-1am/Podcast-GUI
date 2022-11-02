from cProfile import label
from ctypes import sizeof
from tkinter.tix import ButtonBox
from functions import *
import tkinter as tk #for GUI
from tkinter import Frame, Label, filedialog, Text, CENTER
from tkinter import ttk
from tkinter.messagebox import showerror
from threading import Thread
import requests
import os 
import xml.etree.ElementTree as XET
import pandas as pd 
import csv

#------------------RSS LINK------------------#
#https://feeds.captivate.fm/gogetters/
#------------------RSS LINK------------------#

#------------------Multi-Threading------------------#
# class async_Download(Thread):
#     def __init__(self, url):
#         super().__init__()
#         self.html = None
#         self.url = url

#     def run(self):
#         response = requests.get(self.url)
#         self.html = response.text
#------------------Multi-Threading------------------#

# Script for downloading podcasts(mp3) using rss feed(xml) tags, takes in the path to the rss feed

def get_Tags():
    tagsList = []
    attribList = []
    textList = []
    xmlPath = filedialog.askopenfilename(initialdir="/", title="Select Your RSS File", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    root = open_XML(xmlPath)
    for i in root.findall('./channel/item/'):
        tag = i.tag
        attrib = i.attrib
        text = i.text
        tagsList.append(tag)
        if text != None:
            textList.append(text)
        
    # print(tagsList)
    # print(textList)
    return tagsList, textList


def open_XML(xmlFile):
    tree = XET.parse(xmlFile)
    root = tree.getroot()
    return root
    
def download_PD(path):
    print_To_GUI("Downloading Podcast\n")
    root = open_XML(path) # call open_XML() to get root of the xml file

    podcastFolderPath = podcast_Folder() # Get the path to save the podcast
    for child in root.findall('./channel/item/'): #finds all tags in xml file under the item tag
        tag = child.tag
        if tag == 'enclosure':
            url = child.attrib.get('url')
            if url.find('/'): #finds the last '/' in the url
                fileName = url.rsplit('/', 1)[1] #gets the file name from the url
                filePath = os.path.join(podcastFolderPath, fileName) #creates a path for the file to be saved
            download = requests.get(url, allow_redirects=True) #downloads the file
            print_To_GUI(url + " has been downloaded\n") 
            open(filePath, 'wb').write(download.content) #writes the file to the path
    print_To_GUI("All podcasts have been downloaded\n") 
    download.close() #closes the connection to the server
    print_To_GUI("Connection Closed\n") #DEBUG, even when the request is closed, the app window still runs

#asks user to select a folder to save the podcasts
#askdirectory() only lets user select a folder
def podcast_Folder():
    podcastFolderPath = filedialog.askdirectory(initialdir="/", title="Select Where to Save the Podcasts")
    pdPathLabel = tk.Label(root, text="Save Podcasts Path: " + podcastFolderPath) # Create a label to display the path of the podcast folder
    pdPathLabel.pack()
    print(podcastFolderPath)
    return podcastFolderPath

#asks user to select the RSS xml file and save the path 
def select_RSS_Feed():
    xmlPath = filedialog.askopenfilename(initialdir="/", title="Select Your RSS File", filetypes=(("xml files", "*.xml"), ("all files", "*.*")))
    # Create a label to display the path of the rss feed
    xmlPathLabel = tk.Label(root, text="RSS Feed Path: " + xmlPath)
    xmlPathLabel.pack()
    print(xmlPath)

#asks user to select the folder to save the downloaded rss feed
def save_RSS_Feed():
    xmlPath = filedialog.askdirectory(initialdir="/", title="Select Where to Save the RSS Feed")
    xmlPathLabel = tk.Label(root, text="Save RSS Feed Path: " + xmlPath)
    xmlPathLabel.pack() # Create a label to display the path of the rss feed
    print(xmlPath)
    return xmlPath

# remove the default text from the entry box
def remove_PH(event):
    enterRSS.delete(0, "end")
    return None

# function to save the entered rss feed url to a string
def get_RSS_Entry(): 
    rssLink = enterRSS.get() # Get the RSS feed from the entry box
    print(rssLink) # DEBUG
    xmlPath = save_RSS_Feed() # Get the path to save the RSS feed, requires user input
    rssPath = download_RSS(rssLink, xmlPath) # Get the path to the downloaded RSS feed
    download_PD(rssPath) # Use the path of RSS feed for download podcast function

# function to download the rss feed from the url and return the path to the downloaded rss feed
def download_RSS(entry, xmlPath):
    response = requests.get(entry, allow_redirects=True)
    rssPath = os.path.join(xmlPath, "rss.xml")
    open(rssPath, 'wb').write(response.content) #writes the content of the rss feed to a specified file named podcast.xml
    print_To_GUI("RSS Feed has been downloaded\n")
    return rssPath 

# make a function to print terminal output to the GUI textbox
def print_To_GUI(text):
    print(text) # DEBUG     
    outputBox.insert("end", text + "")
    root.update()

root = tk.Tk() # holds the entire app
root.title("Podcast Downloader")
root.geometry("500x500")

#------------------Working On Styling------------------
# #Add some styling to the app
# style = ttk.Style()
# style.configure("Treeview",
#     background = "silver",
#     foreground = "black",
#     rowheight = 25,
#     fieldbackground = "silver")

# style.map('Treeview',
#     background = [('selected', 'blue')]) 

# my_tree = ttk.Treeview(root)
#------------------Working On Styling------------------
#attach the canvas to the root
frame = tk.Frame(root, bg="black") #pack the canvas to the root so it can be seen
frame.pack()

# frame = tk.Frame(root, bg="black") #create a frame
# frame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1) #place the frame in the root

# ----------------- Entry Section -----------------
# make an entry box for rss feed, add a float label in the entry box
enterRSS = tk.Entry(frame, width=20, borderwidth=5, bg="black", fg="white")

# ----------------- Entry Section -----------------

# ----------------- Text Box Section -----------------
# make a text box for terminal output
outputBox = tk.Text(frame, height=25, width=50, borderwidth=5, bg="black")
outputBox.pack(fill="both", expand=True, side="bottom")
# ----------------- Text Box Section -----------------

# ----------------- Object -----------------
obj = functions(root, enterRSS, outputBox) # create an object of the functions class
# ----------------- Object -----------------

# --------------  Buttons Section ----------------- 
#Select RSS Feed from File Button
tk.Button(frame, text="Select RSS Feed", padx=10, pady=5, fg="white", bg="black", command=obj.select_RSS_Feed).pack(side="top", fill="both", expand=True)

# Submit RSS Feed butt
tk.Button(frame, text="Submit RSS Feed", padx=10, pady=5, fg="white", bg="black", command=obj.get_RSS_Entry).pack(side="top", fill="both", expand=True)

# Get Tags Button
tk.Button(frame, text="Get Tags", padx=10, pady=5, fg="white", bg="black", command=obj.get_Tags).pack(side="top", fill="both", expand=True)


# Quit button
tk.Button(frame, text="Quit", padx=10, pady=5, fg="white", bg="black", command=root.destroy).pack(side="bottom", fill="both", expand=True)
# --------------  Buttons Section ----------------- 

#Create labels matching the selection of tags
#create a label and pack those label next to each other in a 2 by 2 grid
label1 = tk.Label(frame, text="Title", bg="black", fg="white").pack(side="top", fill=00, expand=True)
frame1 = tk.Frame(frame, bg="black")
tk.Label(frame1, text="Title", bg="black", fg="white").grid(row=0, column=0)

# pack t
# tk.Label(frame, text="Title", bg="black", fg="white").pack(side="top", expand=True)

# tk.Label(frame, text="Description", bg="black", fg="white").pack(side="top", expand=True)

# tk.Label(frame, text="Link", bg="black", fg="white").pack(side="top", expand=True)

# tk.Label(frame, text="PubDate", bg="black", fg="white").pack(side="top", expand=True)

# tk.Label(frame, text="Duration", bg="black", fg="white").pack(side="top", expand=True)

# tk.Label(frame, text="Enclosure", bg="black", fg="white").pack(side="top", expand=True)

# tk.Label(frame, text="Season", bg="black", fg="white").pack(side="top", expand=True)

# tk.Label(frame, text="Episode", bg="black", fg="white").pack(side="top", expand=True)

# Submit RSS Feed butt
tk.Button(frame, text="Submit RSS Feed", padx=10, pady=5, fg="white", bg="black", command=obj.get_RSS_Entry).pack(side="top", fill="both", expand=True)

# Quit button
tk.Button(frame, text="Quit", padx=10, pady=5, fg="white", bg="black", command=root.destroy).pack(side="bottom", fill="both", expand=True)
# --------------  Buttons Section ----------------- 

enterRSS.configure(justify=CENTER)
enterRSS.insert("end", "Enter RSS Feed Here")
enterRSS.bind("<Button-1>", obj.remove_PH)
enterRSS.pack(side="top", fill="both", expand=True)

root.mainloop() #similar to html, this is what keeps the window open