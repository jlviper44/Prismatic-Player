import tkinter as tk
from PIL import ImageTk, Image
from tkinter import StringVar, IntVar
import os
import requests
from io import BytesIO
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
import functions
import time
import authorization
import numpy as np
from tkinter import messagebox
import subprocess
import io

class create:
  def __init__(this, spotify):
    this.spotify = spotify
    try:
      currentSong = functions.getCurrentSong(this.spotify)
    except:
      exit()
    if(currentSong == None):
      # print("No Song Playing")
      this.isPlaying = False
    else:
      this.isPlaying = True
      
    this.songData = functions.song(spotify, currentSong)
    this.window = tk.Tk()

    this.window.wm_attributes('-fullscreen','true') 
    this.window.title("Prismatic Player")
    this.screen_width = this.window.winfo_screenwidth()
    this.screen_height = this.window.winfo_screenheight()
    # this.screen_width = 1440
    # this.screen_height = 900
    # this.screen_width = 800
    # this.screen_height = 1340      
    # this.screen_width = 500
    # this.screen_height = 800
    this.window.minsize(this.screen_width, this.screen_height)
    # print(screen_width,screen_height)
    this.orientation = ""
    if(this.screen_width >= this.screen_height):
      this.orientation = "horizontal"
      this.scale = this.screen_height/900
    elif(this.screen_width * 4/3>= this.screen_height):
      this.orientation = "horizontal"
      this.scale = this.screen_height/1100
    else:
      this.orientation = "vertical"
      this.scale = this.screen_width/700

    rgb = ["","",""]
    rgb = this.songData.getRgb()
    this.rgbMain = rgb[0]
    this.rgbSecond = rgb[1]
    this.rgbThird = rgb[2]
    this.img = this.songData.getAlbumArtwork(this.scale, 0)

    this.animationFrame = 0
    this.updateRate = 25

    if(not os.path.exists('initial_run.txt')):
      initRun = open('initial_run.txt','w')
      initRun.close()
      this.timeClick('')
      
    this.window.configure(bg=this.rgbMain)
    this.createTitle(this.isPlaying)
    this.createArtwork(this.isPlaying)
    this.createTime(this.isPlaying)
    this.createSong(True)
    this.loadAnimation()
    this.loadPlaylistInfo()

    this.window.bind('<Key>',this.event)
    this.window.after(this.updateRate, this.update)
    this.window.after(10, this.animation)
    this.window.after(1000, this.updateTime)
    this.window.bind('<Command-q>', this.quit)    
    this.window.mainloop()
  def quit(this, event):
    this.window.destroy()
  def createTitle(this, isPlaying):
    if(this.orientation == "horizontal"):
      this.canvasTitle = tk.Canvas(width=this.screen_width, height=int(this.screen_height/7.2), bg=this.rgbMain,bd=0, highlightthickness=0)
      this.canvasTitle.pack()
      
      this.playbackName = this.canvasTitle.create_text((int(25 * this.scale),int(50 * this.scale)),fill=this.rgbSecond,font=("Circular", int(40 * this.scale)), text=this.songData.getPlaybackSource(this.orientation)[0], anchor='w', tags = 'playbackName')
      this.playbackArtist = this.canvasTitle.create_text((int(25 * this.scale),int(100 * this.scale)),fill=this.rgbThird,font=("Circular", int(20 * this.scale)), text=this.songData.getPlaybackSource(this.orientation)[1], anchor='w')
      this.canvasTitle.tag_bind('playbackName','<Button-1>',this.playlistNameClick)
      this.canvasTitle.tag_bind('playbackName','<Enter>',lambda event, a='playbackName': this.mouseEnter(a))
      this.canvasTitle.tag_bind('playbackName','<Leave>',lambda event, a='playbackName': this.mouseLeave(a))
      t = "e"
      if(int(time.strftime("%I")) < 10):
        t = str(int(time.strftime("%I")))+time.strftime(":%M %p")
      else:
        t = time.strftime("%I:%M %p")
      this.timeText = StringVar()
      this.timeText.set(t)
      this.time = tk.Label(this.canvasTitle, textvariable = this.timeText)
      this.time.config(font=("Circular", int(75 * this.scale)), bg=this.rgbMain, fg=this.rgbSecond)
      this.time.pack()
      this.time.bind('<Button-1>',this.timeClick)
      this.time.bind('<Enter>', lambda event, a = 'time': this.mouseEnter(a))
      this.time.bind('<Leave>', lambda event, a = 'time': this.mouseLeave(a))

      this.canvasTitle.create_window((int(this.screen_width - (25 * this.scale)),int(60 * this.scale)),window=this.time, anchor='e')
    else:
      this.canvasTitle = tk.Canvas(width=this.screen_width, height=int(this.screen_height/6), bg=this.rgbMain,bd=0, highlightthickness=0)
      this.canvasTitle.pack()
      
      t = "e"
      if(int(time.strftime("%I")) < 10):
        t = str(int(time.strftime("%I")))+time.strftime(":%M %p")
      else:
        t = time.strftime("%I:%M %p")
      this.timeText = StringVar()
      this.timeText.set(t)
      this.time = tk.Label(this.canvasTitle, textvariable = this.timeText)
      this.time.config(font=("Circular", int(75 * this.scale)), bg=this.rgbMain, fg=this.rgbSecond)
      this.time.pack() 
      this.time.bind('<Button-1>',this.timeClick)

      this.playbackName = this.canvasTitle.create_text((int(this.screen_width/2),int(125 * this.scale)),fill=this.rgbSecond,font=("Circular", int(25 * this.scale)), text=this.songData.getPlaybackSource(this.orientation)[0], anchor='center', tags = 'playbackName')
      this.playbackArtist = this.canvasTitle.create_text((int(this.screen_width/2),int(120 * this.scale)),fill=this.rgbThird,font=("Circular", int(20 * this.scale)), text=this.songData.getPlaybackSource(this.orientation)[1], anchor='w')
      this.canvasTitle.tag_bind('playbackName','<Button-1>',this.playlistNameClick)
      this.canvasTitle.tag_bind('playbackName','<Enter>',lambda event, a='playbackName': this.mouseEnter(a))
      this.canvasTitle.tag_bind('playbackName','<Leave>',lambda event, a='playbackName': this.mouseLeave(a))

      this.canvasTitle.create_window((int(this.screen_width/2),int(this.screen_height/20)),window=this.time, anchor='center')
  def createArtwork(this, isPlaying):
    if(this.orientation == "horizontal"):
      this.canvasArtworkWrapper = tk.Canvas(width=this.screen_width, height=int(this.screen_height/1.5), bg=this.rgbMain,bd=0, highlightthickness=0)
      this.canvasArtworkWrapper.pack()
      
      width = (this.screen_width - int(600 * this.scale))/4
      height = this.screen_height/1.5/2
      back = [width - 2*this.scale, height - 30*this.scale, width, height - 30*this.scale, width, height, width + 40*this.scale, height - 30*this.scale, width + 40*this.scale, height + 30*this.scale, width, height, width, height + 30*this.scale, width - 2*this.scale, height + 30*this.scale]
      width = this.screen_width - width
      skip = [width + 2*this.scale, height + 30*this.scale, width, height + 30*this.scale, width, height, width - 40*this.scale, height + 30*this.scale, width - 40*this.scale, height - 30*this.scale, width, height, width, height - 30*this.scale, width + 2*this.scale, height - 30*this.scale]
      width = int(this.screen_width/2)

      leftUnderlayArc  = this.canvasArtworkWrapper.create_arc(width - 32*this.scale - 97*this.scale, height + 32*this.scale, width + 32*this.scale - 97*this.scale, height - 32*this.scale,start=90 , extent=180, style='chord', width = 5*this.scale, outline=this.rgbSecond, fill=this.rgbSecond, tags='arcUnderlay')    
      rightUnderlayArc = this.canvasArtworkWrapper.create_arc(width - 32*this.scale + 97*this.scale, height + 32*this.scale, width + 32*this.scale + 97*this.scale, height - 32*this.scale,start=270, extent=180, style='chord', width = 5*this.scale, outline=this.rgbSecond, fill=this.rgbSecond, tags='arcUnderlay')
      # bottomUnderlayLine = this.canvasArtworkWrapper.create_line(width - 97*this.scale, height + 32*this.scale, width + 97*this.scale, height + 32*this.scale, fill=this.rgbThird, width = 5*this.scale, tags='buttonUnderlay')
      # upperUnderlayLine  = this.canvasArtworkWrapper.create_line(width - 97*this.scale, height - 32*this.scale, width + 97*this.scale, height - 32*this.scale, fill=this.rgbThird, width = 5*this.scale, tags='buttonUnderlay')
      middleUnderlay = this.canvasArtworkWrapper.create_rectangle(width - 97*this.scale, height + 32*this.scale,width + 97*this.scale, height - 32*this.scale,fill=this.rgbSecond, outline=this.rgbSecond,width = 5*this.scale, tags='buttonUnderlay')

      pause = [width + 30*this.scale,height+30*this.scale,width - 30*this.scale,height+30*this.scale,width - 30*this.scale,height-30*this.scale,width + 30*this.scale,height-30*this.scale]
      this.pauseButton = this.canvasArtworkWrapper.create_polygon(pause, fill="", outline="", width=5*this.scale, tags="pauseButtonOutline")
      this.pauseRight = this.canvasArtworkWrapper.create_polygon([width + 10*this.scale,height+17*this.scale,width + 10*this.scale,height-17*this.scale], fill=this.rgbMain, outline=this.rgbMain, width=10*this.scale, tags="pauseButton")
      this.pauseLeft = this.canvasArtworkWrapper.create_polygon([width - 10*this.scale,height+17*this.scale,width - 10*this.scale,height-17*this.scale], fill=this.rgbMain, outline=this.rgbMain, width=10*this.scale, tags="pauseButton")
      this.canvasArtworkWrapper.tag_bind("pauseButton", "<Button-1>",this.pauseButtonClick)
      this.canvasArtworkWrapper.tag_bind("pauseButtonOutline", "<Button-1>",this.pauseButtonClick)

      this.backButton = this.canvasArtworkWrapper.create_polygon(back, fill=this.rgbThird, outline=this.rgbThird, width=10*this.scale, tags="backButton")
      this.canvasArtworkWrapper.tag_bind("backButton", "<Button-1>",this.backButtonClick)
      this.canvasArtworkWrapper.tag_bind('backButton','<Enter>',lambda event, a='backButton': this.mouseEnter(a))
      this.canvasArtworkWrapper.tag_bind('backButton','<Leave>',lambda event, a='backButton': this.mouseLeave(a))
      this.skipButton = this.canvasArtworkWrapper.create_polygon(skip, fill=this.rgbThird, outline=this.rgbThird, width=10*this.scale, tags="skipButton")
      this.canvasArtworkWrapper.tag_bind("skipButton", "<Button-1>",this.skipButtonClick)
      this.canvasArtworkWrapper.tag_bind('skipButton','<Enter>',lambda event, a='skipButton': this.mouseEnter(a))
      this.canvasArtworkWrapper.tag_bind('skipButton','<Leave>',lambda event, a='skipButton': this.mouseLeave(a))

      this.canvasArtwork = tk.Canvas(width=int(600 * this.scale), height=int(600 * this.scale), bg=this.rgbMain,bd=0, highlightthickness=0)   
      this.canvasArtwork.pack()
      this.canvasArtwork.create_image((int(600 * this.scale/2),int(600 * this.scale/2)), image=this.img, anchor='center', tags="artwork")
      this.canvasArtwork.tag_bind("artwork", "<Button-1>", this.pauseButtonClick)
      this.canvasArtwork.create_arc(int(-10 * this.scale), int(-10 * this.scale), int(100 * this.scale), int(100 * this.scale), tags="border", start=90,  extent=90, style='arc', width=int(this.scale * 20), outline=this.rgbMain)
      this.canvasArtwork.create_arc(int(610 * this.scale), int(-10 * this.scale), int(500 * this.scale), int(100 * this.scale), tags="border", start=0,   extent=90, style='arc', width=int(this.scale * 20), outline=this.rgbMain)
      this.canvasArtwork.create_arc(int(610 * this.scale), int(608 * this.scale), int(500 * this.scale), int(500 * this.scale), tags="border", start=270, extent=90, style='arc', width=int(this.scale * 20), outline=this.rgbMain)
      this.canvasArtwork.create_arc(int(-10 * this.scale), int(608 * this.scale), int(100 * this.scale), int(500 * this.scale), tags="border", start=180, extent=90, style='arc', width=int(this.scale * 20), outline=this.rgbMain)
      this.canvasArtworkWrapper.create_window(this.screen_width/2,int(this.screen_height/1.5)/2,window=this.canvasArtwork, anchor='center')
    else:

      this.canvasArtworkWrapper = tk.Canvas(width=this.screen_width, height=int(this.screen_height*6.25/10), bg=this.rgbMain,bd=0, highlightthickness=0)
      this.canvasArtworkWrapper.pack()
      
      width = int(this.screen_width/2 - 100 *this.scale)
      height = int(615 * this.scale) + (int(this.screen_height*6.25/10) - int(615 * this.scale))/2
      back = [width - 2*this.scale, height - 20*this.scale, width, height - 20*this.scale, width, height, width + 30*this.scale, height - 20*this.scale, width + 30*this.scale, height + 20*this.scale, width, height, width, height + 20*this.scale, width - 2*this.scale, height + 20*this.scale]
      width = this.screen_width - width
      skip = [width + 2*this.scale, height + 20*this.scale, width, height + 20*this.scale, width, height, width - 30*this.scale, height + 20*this.scale, width - 30*this.scale, height - 20*this.scale, width, height, width, height - 20*this.scale, width + 2*this.scale, height - 20*this.scale]
      width = int(this.screen_width/2)

      leftUnderlayArc  = this.canvasArtworkWrapper.create_arc(width - 32*this.scale - 97*this.scale, height + 32*this.scale, width + 32*this.scale - 97*this.scale, height - 32*this.scale,start=90 , extent=180, style='chord', width = 5*this.scale, outline=this.rgbSecond, fill=this.rgbSecond, tags='arcUnderlay')    
      rightUnderlayArc = this.canvasArtworkWrapper.create_arc(width - 32*this.scale + 97*this.scale, height + 32*this.scale, width + 32*this.scale + 97*this.scale, height - 32*this.scale,start=270, extent=180, style='chord', width = 5*this.scale, outline=this.rgbSecond, fill=this.rgbSecond, tags='arcUnderlay')
      # bottomUnderlayLine = this.canvasArtworkWrapper.create_line(width - 97*this.scale, height + 32*this.scale, width + 97*this.scale, height + 32*this.scale, fill=this.rgbThird, width = 5*this.scale, tags='buttonUnderlay')
      # upperUnderlayLine  = this.canvasArtworkWrapper.create_line(width - 97*this.scale, height - 32*this.scale, width + 97*this.scale, height - 32*this.scale, fill=this.rgbThird, width = 5*this.scale, tags='buttonUnderlay')
      middleUnderlay = this.canvasArtworkWrapper.create_rectangle(width - 97*this.scale, height + 32*this.scale,width + 97*this.scale, height - 32*this.scale,fill=this.rgbSecond, outline=this.rgbSecond,width = 5*this.scale, tags='buttonUnderlay')

      pause = [width + 30*this.scale,height+30*this.scale,width - 30*this.scale,height+30*this.scale,width - 30*this.scale,height-30*this.scale,width + 30*this.scale,height-30*this.scale]
      this.pauseButton = this.canvasArtworkWrapper.create_polygon(pause, fill="", outline="", width=5*this.scale, tags="pauseButtonOutline")
      this.pauseRight = this.canvasArtworkWrapper.create_polygon([width + 10*this.scale,height+17*this.scale,width + 10*this.scale,height-17*this.scale], fill=this.rgbMain, outline=this.rgbMain, width=10*this.scale, tags="pauseButton")
      this.pauseLeft = this.canvasArtworkWrapper.create_polygon([width - 10*this.scale,height+17*this.scale,width - 10*this.scale,height-17*this.scale], fill=this.rgbMain, outline=this.rgbMain, width=10*this.scale, tags="pauseButton")
      this.canvasArtworkWrapper.tag_bind("pauseButton", "<Button-1>",this.pauseButtonClick)
      this.canvasArtworkWrapper.tag_bind("pauseButtonOutline", "<Button-1>",this.pauseButtonClick)

      this.backButton = this.canvasArtworkWrapper.create_polygon(back, fill=this.rgbMain, outline=this.rgbMain, width=5*this.scale, tags="backButton")
      this.canvasArtworkWrapper.tag_bind("backButton", "<Button-1>",this.backButtonClick)
      this.skipButton = this.canvasArtworkWrapper.create_polygon(skip, fill=this.rgbMain, outline=this.rgbMain, width=5*this.scale, tags="skipButton")
      this.canvasArtworkWrapper.tag_bind("skipButton", "<Button-1>",this.skipButtonClick)
      
      if(this.isPlaying != True):
        this.canvasArtworkWrapper.itemconfig("backButton", fill='black', outline='black')
        this.canvasArtworkWrapper.itemconfig("skipButton", fill='black', outline='black')
        this.canvasArtworkWrapper.itemconfig("pauseButton", fill='black', outline='black')
        this.canvasArtworkWrapper.itemconfig("arcUnderlay", fill='black', outline = 'black')
        this.canvasArtworkWrapper.itemconfig("buttonUnderlay", fill = 'black', outline = 'black')
        this.canvasArtworkWrapper.itemconfig("backButton", fill='black', outline='black')
        this.canvasArtworkWrapper.itemconfig("skipButton", fill='black', outline='black')

      this.canvasArtwork = tk.Canvas(width=int(600 * this.scale), height=int(600 * this.scale), bg=this.rgbMain,bd=0, highlightthickness=0)   
      this.canvasArtwork.pack()
      this.canvasArtwork.create_image((int(600 * this.scale/2), int(600 * this.scale/2)), image=this.img, anchor='center', tags="artwork")
      this.canvasArtwork.create_arc(int(-10 * this.scale), int(-10 * this.scale), int(100 * this.scale), int(100 * this.scale), tags="border", start=90,  extent=90, style='arc', width=int(this.scale * 20), outline=this.rgbMain)
      this.canvasArtwork.create_arc(int(610 * this.scale), int(-10 * this.scale), int(500 * this.scale), int(100 * this.scale), tags="border", start=0,   extent=90, style='arc', width=int(this.scale * 20), outline=this.rgbMain)
      this.canvasArtwork.create_arc(int(610 * this.scale), int(610 * this.scale), int(500 * this.scale), int(500 * this.scale), tags="border", start=270, extent=90, style='arc', width=int(this.scale * 20), outline=this.rgbMain)
      this.canvasArtwork.create_arc(int(-10 * this.scale), int(610 * this.scale), int(100 * this.scale), int(500 * this.scale), tags="border", start=180, extent=90, style='arc', width=int(this.scale * 20), outline=this.rgbMain)
      this.canvasArtworkWrapper.create_window(this.screen_width/2,5 * this.scale,window=this.canvasArtwork, anchor='n')
  def createTime(this, isPlaying):
    if(this.orientation == "horizontal"):
      this.timeWrapper = tk.Canvas(width=this.screen_width, height=int(65 * this.scale), bg=this.rgbMain,bd=0, highlightthickness=0)
      this.timeWrapper.pack()

      this.canvasTimeBar = tk.Canvas(width=int(700 * this.scale), height=int(65 * this.scale), bg=this.rgbMain,bd=0, highlightthickness=0)
      this.canvasTimeBar.pack()

      points = [20 * this.scale, int(20 * this.scale), 680*this.scale, int(20 * this.scale)]
      this.timeBarUnderlay = this.canvasTimeBar.create_line(points, width=int(4 * this.scale), tags="timeBarUnderlay", fill=this.rgbThird, capstyle='round')

      points = [20 * this.scale, int(20 * this.scale), 660*this.scale * this.songData.getTimeBar() + 20 * this.scale, int(20 * this.scale)]
      this.timeBar = this.canvasTimeBar.create_line(points, width=int(4 * this.scale), tags="timeBar", fill=this.rgbSecond, capstyle='round')
      
      r = int(this.scale * 5)
      points = [660*this.scale * this.songData.getTimeBar() + 20 * this.scale-r, int(20 * this.scale)-r, 
                660*this.scale * this.songData.getTimeBar() + 20 * this.scale+r, int(20 * this.scale)+r]
      if(this.isPlaying != True):
        this.timeCircle = this.canvasTimeBar.create_oval(points,tags="timeCircle", outline='black', fill='black')
      else:
        this.timeCircle = this.canvasTimeBar.create_oval(points,tags="timeCircle", outline=this.rgbSecond, fill=this.rgbSecond)
      
      this.songCurrentTime = this.canvasTimeBar.create_text((40 * this.scale, int(42 * this.scale)),fill=this.rgbSecond,font=("Circular", int(15 * this.scale)), text=this.songData.getCurrentTime())
      this.songTotalTime = this.canvasTimeBar.create_text((int(660 * this.scale), int(42 * this.scale)),fill=this.rgbSecond,font=("Circular", int(15 * this.scale)), text=this.songData.getTotalTime())

      this.timeWrapper.create_window(this.screen_width/2,int(30 * this.scale),window=this.canvasTimeBar, anchor='center')
      
      this.canvasTimeBar.tag_bind("timeBar","<Button-1>",this.onTimeBarClick)
      this.canvasTimeBar.tag_bind("timeBarUnderlay","<Button-1>",this.onTimeBarClick)
    else:
      this.timeWrapper = tk.Canvas(width=this.screen_width, height=int(80 * this.scale), bg=this.rgbMain,bd=0, highlightthickness=0)
      this.timeWrapper.pack()

      this.canvasTimeBar = tk.Canvas(width=int(700 * this.scale), height=int(65 * this.scale), bg=this.rgbMain,bd=0, highlightthickness=0)
      this.canvasTimeBar.pack()
      
      points = [20 * this.scale, int(20 * this.scale), 680*this.scale, int(20 * this.scale)]
      this.timeBarUnderlay = this.canvasTimeBar.create_line(points, width=int(5 * this.scale), tags="timeBarUnderlay", fill=this.rgbThird, capstyle='round')

      points = [20 * this.scale, int(20 * this.scale), 660*this.scale * this.songData.getTimeBar() + 20 * this.scale, int(20 * this.scale)]
      this.timeBar = this.canvasTimeBar.create_line(points, width=int(5 * this.scale), tags="timeBar", fill=this.rgbSecond, capstyle='round')
      
      r = int(this.scale * 5)
      points = [660*this.scale * this.songData.getTimeBar() + 20 * this.scale-r, int(20 * this.scale)-r, 
                660*this.scale * this.songData.getTimeBar() + 20 * this.scale+r, int(20 * this.scale)+r]
      if(this.isPlaying != True):
        this.timeCircle = this.canvasTimeBar.create_oval(points,tags="timeCircle", outline='black', fill='black')
      else:
        this.timeCircle = this.canvasTimeBar.create_oval(points,tags="timeCircle", outline=this.rgbSecond, fill=this.rgbSecond)
      
      this.songCurrentTime = this.canvasTimeBar.create_text((40*this.scale, int(42 * this.scale)),fill=this.rgbSecond,font=("Circular", int(20 * this.scale)), text=this.songData.getCurrentTime())
      this.songTotalTime = this.canvasTimeBar.create_text((int(660 * this.scale), int(42 * this.scale)),fill=this.rgbSecond,font=("Circular", int(20 * this.scale)), text=this.songData.getTotalTime())

      this.timeWrapper.create_window(this.screen_width/2,int(30 * this.scale),window=this.canvasTimeBar, anchor='center')
      
      this.canvasTimeBar.tag_bind("timeBar","<Button-1>",this.onTimeBarClick)
      this.canvasTimeBar.tag_bind("timeBarUnderlay","<Button-1>",this.onTimeBarClick)
  def createSong(this, isPlaying):
    if(this.orientation == "horizontal"):
      this.songTitleText = StringVar()
      this.songTitleText.set(this.songData.name)
      this.songTitle = tk.Label(this.window, textvariable = this.songTitleText)
      this.songTitle.config(font=("Circular", int(32 * this.scale)), background= this.rgbMain, fg=this.rgbSecond)
      this.songTitle.pack()

      this.songArtistText = StringVar()
      this.songArtistText.set(this.songData.artist)
      this.songArtist = tk.Label(this.window, textvariable = this.songArtistText)
      this.songArtist.config(font=("Circular", int(20 * this.scale)),background= this.rgbMain, fg=this.rgbThird)
      this.songArtist.pack()
    else:
      this.songTitleText = StringVar()
      this.songTitleText.set(this.songData.name)
      this.songTitle = tk.Label(this.window, textvariable = this.songTitleText)
      this.songTitle.config(font=("Circular", int(35 * this.scale)), background= this.rgbMain, fg=this.rgbSecond)
      this.songTitle.pack()

      this.songArtistText = StringVar()
      this.songArtistText.set(this.songData.artist)
      this.songArtist = tk.Label(this.window, textvariable = this.songArtistText)
      this.songArtist.config(font=("Circular", int(25 * this.scale)),background= this.rgbMain, fg=this.rgbThird)
      this.songArtist.pack()
  def mouseEnter(this, object):
    if(object == 'playbackName'):
      this.canvasTitle.itemconfig(this.playbackName,fill='#1ed761')
    elif(object == 'time'):
      this.time.config(fg='#1ed761')
    elif(object == 'backButton'):
      if(this.isPlaying == True):
        this.canvasArtworkWrapper.itemconfig("backButton", fill='#1ed761', outline='#1ed761')
    elif(object == 'skipButton'):
      if(this.isPlaying == True):
        this.canvasArtworkWrapper.itemconfig("skipButton", fill='#1ed761', outline='#1ed761')
  def mouseLeave(this, object):
    if(object == 'playbackName'):
      this.canvasTitle.itemconfig(this.playbackName,fill=this.rgbSecond)
    elif(object == 'time'):
      this.time.config(fg=this.rgbSecond)
    elif(object == 'backButton'):
      this.canvasArtworkWrapper.itemconfig("backButton", fill=this.rgbThird, outline=this.rgbThird)
    elif(object == 'skipButton'):
      this.canvasArtworkWrapper.itemconfig("skipButton", fill=this.rgbThird, outline=this.rgbThird)
  def loadAnimation(this):
    # int(600 * this.scale)
    if(int(600 * this.scale) >= 1000):
      this.animationAdJpg = np.load('photos/Ad/Ad_1000.npy', allow_pickle=True)
      this.animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_1000.npy', allow_pickle=True)
    elif(int(600 * this.scale) >= 800):
      this.animationAdJpg = np.load('photos/Ad/Ad_800.npy', allow_pickle=True)
      this.animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_800.npy', allow_pickle=True)
    elif(int(600 * this.scale) >= 600):
      this.animationAdJpg = np.load('photos/Ad/Ad_600.npy', allow_pickle=True)
      this.animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_600.npy', allow_pickle=True)
    elif(int(600 * this.scale) >= 400):
      this.animationAdJpg = np.load('photos/Ad/Ad_400.npy', allow_pickle=True)
      this.animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_400.npy', allow_pickle=True)
    else:
      this.animationAdJpg = np.load('photos/Ad/Ad_200.npy', allow_pickle=True)
      this.animationLoadingJpg = np.load('photos/LoadingScreen/LoadingScreen_200.npy', allow_pickle=True)
  def loadPlaylistInfo(this):
    this.playlistInfo = []
    user = this.spotify.me().get('id')
    if(not os.path.exists('photos/PlaylistInfo.npy')):
      playlistImg = {}
      for playlist in this.spotify.user_playlists(user).get('items'):
        try:
          response = requests.get(playlist['images'][0]['url'])
          img_data = response.content
          img = Image.open(BytesIO(img_data), mode = 'r')
          img = img.resize((80, 80), Image.ANTIALIAS)
          imgByteArr = io.BytesIO()
          img.save(imgByteArr, format='GIF')
          
          playlistImg.update({playlist['id']: imgByteArr.getvalue()})
          if(len(playlist['name']) > 30):
            playlistName = playlist['name'][0:30] + '...'
          else:
            playlistName = playlist['name']
          photo = tk.PhotoImage(data = imgByteArr.getvalue())
          current_playlist = {'name' : playlistName,
                                'id' : playlist['id'],
                                'image' : photo,
                                'songCount' : playlist['tracks']['total']}
          this.playlistInfo.append(current_playlist)
        except:
          pass
      x = np.array([playlistImg])
      x.dump('photos/PlaylistInfo.npy')
        
    else:
      playlistImg = np.load('photos/PlaylistInfo.npy', allow_pickle=True)
      for playlist in this.spotify.user_playlists(user).get('items'):
        try:
          if playlist['id'] in playlistImg[0]:
            if(len(playlist['name']) > 30):
              playlistName = playlist['name'][0:30] + '...'
            else:
              playlistName = playlist['name']
            photo = tk.PhotoImage(data = playlistImg[0][playlist['id']])
            current_playlist = {'name' : playlistName,
                                  'id' : playlist['id'],
                                  'image' : photo,
                                  'songCount' : playlist['tracks']['total']}
            this.playlistInfo.append(current_playlist)
          else:
            response = requests.get(playlist['images'][0]['url'])
            img_data = response.content
            img = Image.open(BytesIO(img_data), mode = 'r')
            img = img.resize((80, 80), Image.ANTIALIAS)
            imgByteArr = io.BytesIO()
            img.save(imgByteArr, format='GIF')
            playlistImg[0].update({playlist['id']: imgByteArr.getvalue()})
            
            if(len(playlist['name']) > 30):
              playlistName = playlist['name'][0:30] + '...'
            else:
              playlistName = playlist['name']
            photo = tk.PhotoImage(data = imgByteArr.getvalue())
            current_playlist = {'name' : playlistName,
                                  'id' : playlist['id'],
                                  'image' : photo,
                                  'songCount' : playlist['tracks']['total']}
            this.playlistInfo.append(current_playlist)
            os.remove('photos/PlaylistInfo.npy')
            x = np.array([playlistImg[0]])
            x.dump('photos/PlaylistInfo.npy')
        except:
          pass
        # else:
        #   response = requests.get(playlist['images'][0]['url'])
        #   img_data = response.content
        #   img = Image.open(BytesIO(img_data), mode = 'r')
        #   img = img.resize((80, 80), Image.ANTIALIAS)
        #   imgByteArr = io.BytesIO()
        #   img.save(imgByteArr, format='GIF')

    # this.playlistInfo = []
    # user = this.spotify.me().get('id')
    # for playlist in this.spotify.user_playlists(user).get('items'):
    #   response = requests.get(playlist['images'][0]['url'])
    #   img_data = response.content
    #   image = Image.open(BytesIO(img_data))
    #   image = image.resize((80, 80), Image.ANTIALIAS)
    #   img = ImageTk.PhotoImage(image)
    #   if(len(playlist['name']) > 30):
    #     playlistName = playlist['name'][0:30] + '...'
    #   else:
    #     playlistName = playlist['name']
    #   current_playlist = {'name' : playlistName,
    #                   'id' : playlist['id'],
    #                   'image' : img,
    #                   'songCount' : playlist['tracks']['total']}
    #   this.playlistInfo.append(current_playlist)
  def playlistNameClick(this, event):
    try:
      this.playMenu.destroy()
      this.playMenu = tk.Toplevel()
      this.playMenu.title('Playlist Menu')
      this.playMenu.geometry("%dx%d+%d+%d" % (600, 350, this.screen_width/2 - 300, this.screen_height/2 - 175))
      this.playMenu.resizable(False, False)
      this.playMenu.config(bg = '#0f0f0f')
      this.playMenuCanvas = tk.Canvas(this.playMenu, width=600, height = 350, bg = '#0f0f0f', bd=0, highlightthickness=0)
      this.playMenuScroll_y = tk.Scrollbar(this.playMenu, orient="vertical", command=this.playMenuCanvas.yview)
      this.playMenuFrame = tk.Frame(this.playMenuCanvas, bg = '#0f0f0f')
      this.playMenuFrame.pack(expand= True)

      try:
        devices = this.spotify.devices().get('devices')[0]['name']
        # if(len(devices) == 0):
        #    os.system("open -a /Applications/Spotify.app --hide ")
        #    this.playlistNameClick('')
        tk.Label(this.playMenuFrame, text='Playlists', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
        # playlists = this.spotify.user_playlists(user).get('items')

        for playlist in this.playlistInfo:
          canvas = tk.Canvas(this.playMenuFrame, width = 600, bg = '#0f0f0f', height = 90, bd=0, highlightthickness=0)
          canvas.create_image((100,45), image=playlist['image'], anchor='center')
          canvas.create_text((200,45),fill='white',font=("Circular", 16), text = playlist['name'], anchor='w')
          canvas.create_text((500,45),fill='white',font=("Circular", 16), text = str(playlist['songCount']) + ' songs', anchor='w')
          canvas.bind('<Button-1>',lambda event, a=playlist['id']: this.playlistClick(a))
          # tk.Label(canvas, text= playlist['name'], justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
          # tk.Label(canvas, text= playlist['name'], justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = i, column = 0, sticky = 'w')
          # tk.Label(canvas, text= playlist['name'], justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = i, column = 1, sticky = 'n')
          # tk.Label(canvas, text= playlist['tracks']['total'], justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = i, column = 2, sticky = 'e')
          canvas.pack()
        height = len(this.playlistInfo) * 90 + 50
      except:
        tk.Label(this.playMenuFrame, text= 'No devices found!', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
        tk.Label(this.playMenuFrame, text= 'Open spotify on a device to load playlists.', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
        height = 350


      this.playMenuContainer = this.playMenuCanvas.create_window(0, 0, width = 600, height = height, anchor='nw', window=this.playMenuFrame, tags= 'frame')
      this.playMenuCanvas.update_idletasks()
      this.playMenuCanvas.configure(scrollregion=this.playMenuCanvas.bbox('all'), yscrollcommand=this.playMenuScroll_y.set)
      this.playMenuCanvas.pack(fill='both', expand=True, side='left')
      this.playMenuScroll_y.pack(fill='y', side='right')
      this.playMenuCanvas.bind_all("<MouseWheel>", this._on_mousewheel)
      this.playMenuCanvas.bind_all("<Down>", this.arrowKeys)
      this.playMenuCanvas.bind_all("<Up>", this.arrowKeys)
    except:
      this.playMenu = tk.Toplevel()
      this.playMenu.title('Playlist Menu')
      this.playMenu.geometry("%dx%d+%d+%d" % (600, 350, this.screen_width/2 - 300, this.screen_height/2 - 175))
      this.playMenu.resizable(False, False)
      this.playMenu.config(bg = '#0f0f0f')
      this.playMenuCanvas = tk.Canvas(this.playMenu, width=600, height = 350, bg = '#0f0f0f', bd=0, highlightthickness=0)
      this.playMenuScroll_y = tk.Scrollbar(this.playMenu, orient="vertical", command=this.playMenuCanvas.yview)
      this.playMenuFrame = tk.Frame(this.playMenuCanvas, bg = '#0f0f0f')
      this.playMenuFrame.pack(expand= True)

      try:
        devices = this.spotify.devices().get('devices')[0]['name']
        # print(devices)
        # if(len(devices) == 0):
        #   print(len(devices))
           # os.system("open -a /Applications/Spotify.app --hide ")
           # this.playlistNameClick('')
        tk.Label(this.playMenuFrame, text='Playlists', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
        # playlists = this.spotify.user_playlists(user).get('items')

        for playlist in this.playlistInfo:
          canvas = tk.Canvas(this.playMenuFrame, width = 600, bg = '#0f0f0f', height = 90, bd=0, highlightthickness=0)
          canvas.create_image((100,45), image=playlist['image'], anchor='center')
          canvas.create_text((200,45),fill='white',font=("Circular", 16), text = playlist['name'], anchor='w')
          canvas.create_text((500,45),fill='white',font=("Circular", 16), text = str(playlist['songCount']) + ' songs', anchor='w')
          canvas.bind('<Button-1>',lambda event, a=playlist['id']: this.playlistClick(a))
          # tk.Label(canvas, text= playlist['name'], justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
          # tk.Label(canvas, text= playlist['name'], justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = i, column = 0, sticky = 'w')
          # tk.Label(canvas, text= playlist['name'], justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = i, column = 1, sticky = 'n')
          # tk.Label(canvas, text= playlist['tracks']['total'], justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = i, column = 2, sticky = 'e')
          canvas.pack()
        height = len(this.playlistInfo) * 90 + 50
      except:
        tk.Label(this.playMenuFrame, text= 'No devices found!', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
        tk.Label(this.playMenuFrame, text= 'Open spotify on a device to load playlists.', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
        height = 350


      this.playMenuContainer = this.playMenuCanvas.create_window(0, 0, width = 600, height = height, anchor='nw', window=this.playMenuFrame, tags= 'frame')
      this.playMenuCanvas.update_idletasks()
      this.playMenuCanvas.configure(scrollregion=this.playMenuCanvas.bbox('all'), yscrollcommand=this.playMenuScroll_y.set)
      this.playMenuCanvas.pack(fill='both', expand=True, side='left')
      this.playMenuScroll_y.pack(fill='y', side='right')
      this.playMenuCanvas.bind_all("<MouseWheel>", this._on_mousewheel)
      this.playMenuCanvas.bind_all("<Down>", this.arrowKeys)
      this.playMenuCanvas.bind_all("<Up>", this.arrowKeys)
  def playlistClick(this, id):
    uri = 'spotify:playlist:' + id
    # print(this.spotify.devices().get('devices')[0]['id'])
    try:
      this.spotify.start_playback(context_uri = uri)
    except:
      try:
        device = this.spotify.devices().get('devices')[0]['id']
        # device = '9d0970db0e1989f5f6945b97ea9454a0e7d18706'
        this.spotify.start_playback(device, context_uri = uri)
      except:
        messagebox.showwarning(title="Warning", message="No devices found!")
    this.playMenu.destroy()
    this.updateNewSong()
  def arrowKeys(this, event):
    try:
      if(event.keysym == 'Down'):
        direction = 1
      elif(event.keysym == 'Up'):
        direction = -1
      this.playMenuCanvas.yview_scroll(direction, "units")
    except:
      pass
  def _on_mousewheel(this, event):
    direction = -1*(event.delta/120)
    if(direction < 0):
      direction = -1
    else:
      direction = 1
    this.playMenuCanvas.yview_scroll(direction, "units")
  def timeClick(this, event):
    try:
      this.controlMenu.destroy()

      this.controlMenu = tk.Toplevel()
      this.controlMenu.title('Control Menu')
      this.controlMenu.geometry("%dx%d+%d+%d" % (600, 350, this.screen_width/2 - 300, this.screen_height/2 - 175))
      this.controlMenu.resizable(False, False)
      this.controlMenu.config(bg = '#0f0f0f')
      tk.Label(this.controlMenu, text= 'Controls', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
      tk.Label(this.controlMenu, text= ' Click the time to refrence this window ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.controlMenu, text = ' ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 6)).pack()
      tk.Label(this.controlMenu, text = ' NOTE: Playback Controls require a Spotify Premium Account', justify = 'center', bg = '#0f0f0f', fg = '#FF0000', font=("Circular", 20)).pack()
      canvas1 = tk.Canvas(this.controlMenu, bg = '#0f0f0f', bd=0, highlightthickness=0)
      canvas1.pack()
      tk.Label(canvas1, text= ' Left Arrow ',  justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 0, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Skip Song',      justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 0, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' Right Arrow ', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 0, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Previous Song ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 0, column = 3, sticky = 'w')

      tk.Label(canvas1, text= ' Up Arrow ',      justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 1, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Increase Volume ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 1, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' Down Arrow ',    justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 1, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Decrease Volume ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 1, column = 3, sticky = 'w')
 
      tk.Label(canvas1, text= ' S Key ',            justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 2, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Toggle Shuffle ',     justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 2, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' R Key ',            justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 2, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Toggle Repeat ',      justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 2, column = 3, sticky = 'w')

      tk.Label(canvas1, text= ' ? Key ',     justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 3, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Open Control Menu ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 3, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' Space Bar ',     justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 3, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Play/Pause ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 3, column = 3, sticky = 'w')
      
      tk.Label(canvas1, text= ' P Key ',                  justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 4, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Open Playlist Menu ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 4, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' ESC ',                  justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 4, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Close Prismatic Player ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 4, column = 3, sticky = 'w')
      tk.Label(this.controlMenu, text = ' ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()

      this.clearCacheButton = tk.Button(this.controlMenu, text = "Logout of your Account", command = this.clearCache, width = 20, font=("Circular", 16), relief = 'flat', borderwidth=0, highlightthickness = 0, bd = 0)
      this.clearCacheButton.pack()
      tk.Label(this.controlMenu, text= ' Use this button to change accounts or reenter account info. ', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).pack() 
      
    except:
      this.controlMenu = tk.Toplevel()
      this.controlMenu.title('Control Menu')
      this.controlMenu.geometry("%dx%d+%d+%d" % (600, 350, this.screen_width/2 - 300, this.screen_height/2 - 175))
      this.controlMenu.resizable(False, False)
      this.controlMenu.config(bg = '#0f0f0f')
      tk.Label(this.controlMenu, text= 'Controls', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
      tk.Label(this.controlMenu, text= ' Click the time to refrence this window ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.controlMenu, text = ' ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 6)).pack()
      tk.Label(this.controlMenu, text = ' NOTE: Playback Controls require a Spotify Premium Account', justify = 'center', bg = '#0f0f0f', fg = '#FF0000', font=("Circular", 20)).pack()
      canvas1 = tk.Canvas(this.controlMenu, bg = '#0f0f0f', bd=0, highlightthickness=0)
      canvas1.pack()
      tk.Label(canvas1, text= ' Left Arrow ',  justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 0, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Skip Song',      justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 0, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' Right Arrow ', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 0, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Previous Song ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 0, column = 3, sticky = 'w')

      tk.Label(canvas1, text= ' Up Arrow ',      justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 1, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Increase Volume ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 1, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' Down Arrow ',    justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 1, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Decrease Volume ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 1, column = 3, sticky = 'w')
 
      tk.Label(canvas1, text= ' S Key ',            justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 2, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Toggle Shuffle ',     justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 2, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' R Key ',            justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 2, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Toggle Repeat ',      justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 2, column = 3, sticky = 'w')

      tk.Label(canvas1, text= ' ? Key ',     justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 3, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Open Control Menu ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 3, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' Space Bar ',     justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 3, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Play/Pause ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 3, column = 3, sticky = 'w')
      
      tk.Label(canvas1, text= ' P Key ',                  justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 4, column = 0, sticky = 'e')
      tk.Label(canvas1, text= ' Open Playlist Menu ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 4, column = 1, sticky = 'w')
      tk.Label(canvas1, text= ' ESC ',                  justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 4, column = 2, sticky = 'e')
      tk.Label(canvas1, text= ' Close Prismatic Player ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 4, column = 3, sticky = 'w')
      tk.Label(this.controlMenu, text = ' ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()

      this.clearCacheButton = tk.Button(this.controlMenu, text = "Logout of your Account", command = this.clearCache, width = 20, font=("Circular", 16), relief = 'flat', borderwidth=0, highlightthickness = 0, bd = 0)
      this.clearCacheButton.pack()
      tk.Label(this.controlMenu, text= ' Use this button to change accounts or reenter account info. ', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).pack() 
  def clearCache(this):
    authorization.clearCache()
    try:
      os.remove('initial_run.txt')
    except:
      pass
    this.window.destroy()
  def pauseButtonClick(this,event):
    try:
      state = functions.togglePlayback(this.spotify)
      this.togglePlayIcon(state)
    except:
      pass
  def togglePlayIcon(this,state):
    try:
      width = int(this.screen_width/2)
      height = int(615 * this.scale) + (int(this.screen_height*6.25/10) - int(615 * this.scale))/2

      if(state == False):
        this.canvasArtworkWrapper.coords(this.pauseLeft,[width - 10*this.scale,height+17*this.scale,width - 10*this.scale,height-17*this.scale,width + 12*this.scale, height])
        this.canvasArtworkWrapper.itemconfig(this.pauseRight,fill=this.rgbSecond, outline=this.rgbSecond)
      else:
        this.canvasArtworkWrapper.coords(this.pauseLeft,[width - 10*this.scale,height+17*this.scale,width - 10*this.scale,height-17*this.scale])
        this.canvasArtworkWrapper.itemconfig(this.pauseRight,fill=this.rgbMain, outline=this.rgbMain)
      if(this.isPlaying != True):
        this.canvasArtworkWrapper.itemconfig(this.pauseRight,fill='black', outline='black')
    except:
      pass
  def backButtonClick(this,event):
    try:
      functions.previousPlayback(this.spotify)
    except:
      pass
  def skipButtonClick(this,event):
    try:
      functions.skipPlayback(this.spotify) 
    except:
      pass
  def onTimeBarClick(this,eventextentx):
    try:
      global xe
      xe = eventextentx.x - 20 * this.scale
      percent = xe / (int(660 * this.scale)) - 0.0075
      if(percent < 0):
        percent = 0
      functions.seekPlayback(this.spotify, percent)
    except:
      pass
  def event(this, event):
    if(event.keysym == "Left"):
      functions.previousPlayback(this.spotify)
    elif(event.keysym == "Right"):
      functions.skipPlayback(this.spotify)
    elif(event.keysym == "space"):
      this.pauseButtonClick('')
    elif(event.keysym == "Up"):
      functions.changeVolume(this.spotify, "increseVolume")
    elif(event.keysym == "Down"):
      functions.changeVolume(this.spotify, "decreaseVolume")
    elif(event.keysym == "s"):
      functions.toggleShuffle(this.spotify)
    elif(event.keysym == "r"):
      functions.toggleRepeat(this.spotify)
    elif(event.keysym == "Escape"):
      this.window.destroy()
    elif(event.keysym == 'slash'):
      this.timeClick('')
    elif(event.keysym == 'question'):
      this.timeClick('')
    elif(event.keysym == 'p'):
      this.playlistNameClick('')
  def update(this):
    try:
      currentSong = functions.getCurrentSong(this.spotify)
      song2 = functions.song(this.spotify, currentSong)
      this.isPlaying = song2.isPlaying
      if(song2.name != this.songData.name):
        this.songData = song2
        this.updateNewSong()
        this.updateRate = 15
        this.animationFrame = 0
      this.songData = song2
      # del song2
      r = (5 * this.scale)
      this.togglePlayIcon(this.songData.getPlaybackState())
      this.canvasTimeBar.coords("timeBar", (int(20 * this.scale), int(20 * this.scale), 660*this.scale * this.songData.getTimeBar() + 20 * this.scale, int(20 * this.scale)))
      this.canvasTimeBar.coords("timeCircle", (660*this.scale * this.songData.getTimeBar() + 20 * this.scale-r, int(20 * this.scale)-r , 660*this.scale * this.songData.getTimeBar() + 20 * this.scale+r, int(20 * this.scale)+r))
      this.canvasTimeBar.itemconfig(this.songCurrentTime,fill=this.rgbSecond, text=this.songData.getCurrentTime())
      this.canvasTimeBar.itemconfig(this.songTotalTime,fill=this.rgbSecond, text=this.songData.getTotalTime())
      this.window.after(this.updateRate, this.update)
    except:
      this.spotify = authorization.refreshToken()
      this.window.after(this.updateRate, this.update)
  def animation(this):
    global img3
    # currentSong = functions.getCurrentSong(this.spotify)
    if(this.isPlaying == 'none'):
      this.updateRate = 1000
      img3 = tk.PhotoImage(data = this.animationLoadingJpg[this.animationFrame])
      this.canvasArtwork.itemconfig('artwork', image = img3)
      this.animationFrame += 1
      if(this.animationFrame == len(this.animationLoadingJpg)):
        this.animationFrame = 0
    elif(this.isPlaying == 'ad'):
      this.updateRate = 1000
      img3 = tk.PhotoImage(data = this.animationAdJpg[this.animationFrame])
      this.canvasArtwork.itemconfig('artwork', image = img3)
      this.animationFrame += 1
      if(this.animationFrame == len(this.animationLoadingJpg)):
        this.animationFrame = 0
    this.window.after(20, this.animation)
  def updateNewSong(this):
    rgb = ["","",""]
    rgb = this.songData.getRgb()
    this.rgbMain = rgb[0]
    this.rgbSecond = rgb[1]
    this.rgbThird = rgb[2]
    
    this.window.config(bg=this.rgbMain)
    this.canvasTitle.config(bg=this.rgbMain)
    this.canvasTitle.itemconfig(this.playbackName,fill=this.rgbSecond, text=this.songData.getPlaybackSource(this.orientation)[0])
    this.canvasTitle.itemconfig(this.playbackArtist,fill=this.rgbThird, text=this.songData.getPlaybackSource(this.orientation)[1])
    this.time.config(bg=this.rgbMain, fg=this.rgbSecond)

    this.timeWrapper.config(bg=this.rgbMain)
    this.canvasTimeBar.config(bg=this.rgbMain)
    this.canvasTimeBar.itemconfig(this.timeBarUnderlay, fill=this.rgbThird)
    this.canvasTimeBar.itemconfig(this.timeBar, fill=this.rgbSecond)
    this.canvasTimeBar.itemconfig(this.timeCircle, fill=this.rgbSecond, outline=this.rgbSecond)

    this.canvasArtworkWrapper.config(bg=this.rgbMain)
    if(this.orientation == "horizontal"):
      this.canvasArtworkWrapper.itemconfig("pauseButton", fill=this.rgbSecond, outline=this.rgbSecond)
      this.canvasArtworkWrapper.itemconfig("arcUnderlay", outline = this.rgbThird)
      this.canvasArtworkWrapper.itemconfig("buttonUnderlay", fill = this.rgbThird)

      this.canvasArtworkWrapper.itemconfig("backButton", fill=this.rgbSecond, outline=this.rgbSecond)
      this.canvasArtworkWrapper.itemconfig("skipButton", fill=this.rgbSecond, outline=this.rgbSecond)
    else:
      this.canvasArtworkWrapper.itemconfig("pauseButton", fill=this.rgbMain, outline=this.rgbMain)
      this.canvasArtworkWrapper.itemconfig("arcUnderlay", fill=this.rgbSecond, outline = this.rgbSecond)
      this.canvasArtworkWrapper.itemconfig("buttonUnderlay", fill = this.rgbSecond, outline = this.rgbSecond)

      this.canvasArtworkWrapper.itemconfig("backButton", fill=this.rgbMain, outline=this.rgbMain)
      this.canvasArtworkWrapper.itemconfig("skipButton", fill=this.rgbMain, outline=this.rgbMain)



    if(this.isPlaying != True):
      this.canvasTimeBar.itemconfig(this.timeCircle, fill='black', outline='black')
      this.canvasArtworkWrapper.itemconfig("backButton", fill='black', outline='black')
      this.canvasArtworkWrapper.itemconfig("skipButton", fill='black', outline='black')
      this.canvasArtworkWrapper.itemconfig("pauseButton", fill='black', outline='black')
      this.canvasArtworkWrapper.itemconfig("arcUnderlay", fill='black', outline = 'black')
      this.canvasArtworkWrapper.itemconfig("buttonUnderlay", fill = 'black', outline = 'black')
      this.canvasArtworkWrapper.itemconfig("backButton", fill='black', outline='black')
      this.canvasArtworkWrapper.itemconfig("skipButton", fill='black', outline='black')


    this.canvasArtwork.itemconfig("border", outline=this.rgbMain)
    this.canvasArtwork.config(bg=this.rgbMain)

    this.songTitle.config(bg=this.rgbMain, fg=this.rgbSecond)
    this.songArtist.config(bg=this.rgbMain, fg=this.rgbThird)
    this.songTitleText.set(this.songData.name)
    this.songArtistText.set(this.songData.artist)
    global img2
    img2 = this.songData.getAlbumArtwork(this.scale, this.animationFrame)
    this.canvasArtwork.itemconfig("artwork", image=img2)
  def updateTime(this):
    t = "e"
    if(int(time.strftime("%I")) < 10):
      t = str(int(time.strftime("%I")))+time.strftime(":%M %p")
    else:
      t = time.strftime("%I:%M %p")
    this.timeText.set(t)
    this.window.after(1000, this.updateTime)

