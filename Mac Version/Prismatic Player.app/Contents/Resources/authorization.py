import sys
import os
import spotipy
import spotipy.util as util
import tkinter as tk
from tkinter import messagebox
import csv
import time
from PIL import ImageTk, Image, ImageStat, ImageFilter
import webbrowser



# circle animation
# create adverttisement window
# play now screen
# splice if title is too long


class auth:
  def __init__(this):
    this.window = tk.Tk()
    # this.window.minsize(600, 400)
    this.window.title("Prismatic Player Setup")
    this.window.config(bg = '#0f0f0f')
    this.introduction = tk.Canvas(this.window, bg = '#0f0f0f', bd=0, highlightthickness=0, width = 500, height = 275)
    this.introduction.grid(row = 0, column = 0, columnspan = 2)
    image = Image.open("photos/spotify.png")
    image = image.resize((100, 100), Image.ANTIALIAS)
    global img
    img = ImageTk.PhotoImage(image)
    this.introduction.create_image((250, 25), image=img, anchor='n', tags="spotifyImage")
    this.introduction.create_text((250,165), text='Prismatic Player', fill= "white", font=("Circular", 30))
    this.introduction.create_text((250,195), text='By: Justin Lee', fill= "white", font=("Circular", 15))
    this.introduction.create_text((250,235), text='To begin the setup, please enter your username', fill= "white", font=("Circular", 15))
    # this.spotifyImage = this.introduction.create_image()
    # 
    # this.spotifyImage = tk.Label(this.window, image=img, bd=0, highlightthickness=0, bg = '#0f0f0f').grid(row = 0, column = 1)
    # this.spotifyImage = img

    # helpButton = tk.Button(this.window, text = "Help", command = this.help).grid(row=0)
    this.privacyButton = tk.Button(this.window, text = "Privacy Policy", width = 10, font=("Circular", 16), relief = 'flat', command = this.privacyPolicyLaunch, borderwidth=0, highlightthickness = 0, bd = 0)
    this.privacyButton.grid(row = 0, column = 1, sticky = 'ne', padx = (10,10), pady = (10,10))

    this.username      = tk.StringVar()
    this.client_id     = tk.StringVar()
    this.client_secret = tk.StringVar()
    this.redirect_url  = tk.StringVar()
    this.callback_url  = tk.StringVar()

    this.client_id.set(''.join(chr(i) for i in [99, 55, 100, 101, 48, 55, 56, 48, 57, 100, 54, 101, 52, 100, 51, 54, 57, 99, 98, 51, 50, 100, 56, 57, 48, 56, 99, 100, 48, 50, 100, 100]))
    this.client_secret.set(''.join(chr(i) for i in [101, 53, 102, 56, 48, 102, 54, 52, 48, 54, 57, 55, 52, 57, 57, 57, 97, 57, 55, 97, 56, 97, 51, 102, 101, 50, 99, 101, 52, 102, 49, 99]))
    this.redirect_url.set("prismatic-player-login://callback")

    this.usernameCavas = tk.Canvas(this.window, bg = '#0f0f0f', bd=0, highlightthickness=0, width = 500, height = 300)
    this.usernameCavas.grid(row = 1, column = 0, columnspan = 2)

    this.usernameText       = tk.Label(this.usernameCavas, text="Username:", bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row = 0, column = 0, pady=(0,5))
    this.usernameEntry      = tk.Entry(this.usernameCavas, insertbackground = '#1ed761', width = 15, bg = '#0f0f0f', fg = 'white', font=("Circular", 16), highlightcolor = '#1ed761', relief='flat',textvariable = this.username).grid(row = 0, column = 1, pady=(0,5))
    
    this.submitButton = tk.Button(this.window, text = "Submit", width = 10, font=("Circular", 16), relief = 'flat', command = this.setAuth, borderwidth=0, highlightthickness = 0, bd = 0)
    this.submitButton.grid(row = 3, columnspan = 2, pady=(15,15))
    this.window.bind('<Button-1>', this.removeScroll)
    
    

    if (os.path.exists('authData.csv')):
      with open('authData.csv', newline='') as csvfile:
        reader =  csv.DictReader(csvfile)
        data = list(reader)[0]
        username = data.get('username')
      if(not os.path.exists(".cache-" + username)):
        try:
          os.remove('authData.csv')
        except:
          pass
    



    # this.usernameEntry     
    # this.client_idEntry    
    # this.client_secretEntry
    # this.redirect_urlEnrty 
    # this.callback_urlEntry 



    this.code = ""
    this.initialRun = True
    this.authDataCreated = False
  def removeScroll(this, event):
    try:
      this.privacyPolicyCanvas.unbind_all('<MouseWheel>')
      this.privacyPolicyCanvas.unbind_all("<Down>")
      this.privacyPolicyCanvas.unbind_all("<Up>")
    except:
      pass
  def privacyPolicyLaunch(this):
    try:
      this.privacyPolicyWindow.destroy()
      this.privacyPolicyWindow = tk.Toplevel()
      this.privacyPolicyWindow.resizable(False, False)
      this.privacyPolicyWindow.title('Privacy Policy')
      this.privacyPolicyWindow.geometry("%dx%d+%d+%d" % (500, 440, 500, 0))
      this.privacyPolicyWindow.config(bg = '#0f0f0f')
      this.privacyPolicyCanvas = tk.Canvas(this.privacyPolicyWindow, width=500, height = 440, bg = '#0f0f0f', bd=0, highlightthickness=0)
      this.scroll_y = tk.Scrollbar(this.privacyPolicyWindow, orient="vertical", command=this.privacyPolicyCanvas.yview)
      this.frame = tk.Frame(this.privacyPolicyCanvas, bg = '#0f0f0f')
      this.frame.pack(expand= True)

      tk.Label(this.frame, text= 'Privacy Policy', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
      tk.Label(this.frame, text= ' Prismatic Player does not collect users data, however ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' it pulls requests from a Spotify server, to gain ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' necessary information. The information accessed  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' includes the song that is currently playing, user ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' information, and the ability to modify the user\'s ' , justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' playback state (play, pause, skip, etc.)', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' If you do not feel safe in allowing Prismatic Player ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' to access this type of information but still want to  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' use the app, you can create your own sever using the  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' Advanced Setup! ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()

      advancedSetup = tk.Button(this.frame, text = "Advanced Setup", command = this.advancedSetup, width = 20, font=("Circular", 16), relief = 'flat', borderwidth=0, highlightthickness = 0, bd = 0).pack()
      this.container = this.privacyPolicyCanvas.create_window(0, 0, width = 500, height = 440, anchor='nw', window=this.frame, tags= 'frame')
      this.privacyPolicyCanvas.update_idletasks()
      this.privacyPolicyCanvas.configure(scrollregion=this.privacyPolicyCanvas.bbox('all'), yscrollcommand=this.scroll_y.set)
      this.privacyPolicyCanvas.pack(fill='both', expand=True, side='left')
      this.scroll_y.pack(fill='y', side='right')
      this.privacyPolicyWindow.bind('<Button-1>', this.addScroll)
      this.addScroll('')
    except:
      this.privacyPolicyWindow = tk.Toplevel()
      this.privacyPolicyWindow.title('Privacy Policy')
      this.privacyPolicyWindow.resizable(False, False)
      this.privacyPolicyWindow.geometry("%dx%d+%d+%d" % (500, 440, 500, 0))
      this.privacyPolicyWindow.config(bg = '#0f0f0f')
      this.privacyPolicyCanvas = tk.Canvas(this.privacyPolicyWindow, width=500, height = 440, bg = '#0f0f0f', bd=0, highlightthickness=0)
      this.scroll_y = tk.Scrollbar(this.privacyPolicyWindow, orient="vertical", command=this.privacyPolicyCanvas.yview)
      this.frame = tk.Frame(this.privacyPolicyCanvas, bg = '#0f0f0f')
      this.frame.pack(expand= True)

      tk.Label(this.frame, text= 'Privacy Policy', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
      tk.Label(this.frame, text= ' Prismatic Player does not collect users data, however ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' it pulls requests from a Spotify server, to gain ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' necessary information. The information accessed  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' includes the song that is currently playing, user ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' information, and the ability to modify the user\'s ' , justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' playback state (play, pause, skip, etc.)', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' If you do not feel safe in allowing Prismatic Player ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' to access this type of information but still want to  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' use the app, you can create your own sever using the  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= ' Advanced Setup! ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
      tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()

      advancedSetup = tk.Button(this.frame, text = "Advanced Setup", command = this.advancedSetup, width = 20, font=("Circular", 16), relief = 'flat', borderwidth=0, highlightthickness = 0, bd = 0).pack()
      this.container = this.privacyPolicyCanvas.create_window(0, 0, width = 500, height = 440, anchor='nw', window=this.frame, tags= 'frame')
      this.privacyPolicyCanvas.update_idletasks()
      this.privacyPolicyCanvas.configure(scrollregion=this.privacyPolicyCanvas.bbox('all'), yscrollcommand=this.scroll_y.set)
      this.privacyPolicyCanvas.pack(fill='both', expand=True, side='left')
      this.scroll_y.pack(fill='y', side='right')
      this.privacyPolicyWindow.bind('<Button-1>', this.addScroll)
      this.addScroll('')
  def addScroll(this, event):
    this.privacyPolicyCanvas.bind_all("<MouseWheel>", this._on_mousewheel)
    this.privacyPolicyCanvas.bind_all("<Down>", this.arrowKeys)
    this.privacyPolicyCanvas.bind_all("<Up>", this.arrowKeys)
  def arrowKeys(this, event):
    if(event.keysym == 'Down'):
      direction = 1
    elif(event.keysym == 'Up'):
      direction = -1
    this.privacyPolicyCanvas.yview_scroll(direction, "units")
  def _on_mousewheel(this, event):
    direction = -1*(event.delta/120)
    if(direction < 0):
      direction = -1
    else:
      direction = 1
    this.privacyPolicyCanvas.yview_scroll(direction, "units")
  def advancedSetup(this):
    this.privacyPolicyCanvas.itemconfigure(this.container, height = 3275)
    this.privacyPolicyCanvas.update_idletasks()


    
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= 'Welcome to the Advanced Setup!', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 30)).pack()
    tk.Label(this.frame, text= ' Follow these steps to create your own Spotify server! ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' 1. Click the link below or open a web browser and navigate to  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    link = tk.Label(this.frame, text= ' https://developer.spotify.com/dashboard/login ', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16))
    link.pack()
    link.bind("<Button-1>", lambda e: webbrowser.open_new("https://developer.spotify.com/dashboard/login"))
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    
    image = Image.open("photos/"+str(1)+".png")
    image = image.resize((450, 250), Image.ANTIALIAS)
    newImg = ImageTk.PhotoImage(image)
    img1 = tk.Label(this.frame, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
    img1.pack()
    img1.image = newImg

    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' 2. Login with your spotify account and accept the ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' Terms of Service ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' 3. After accepting the Terms of Service, you will see ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' your Dashboard. Click the CREATE AN APP Button. ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    
    image = Image.open("photos/"+str(2)+".png")
    image = image.resize((450, 250), Image.ANTIALIAS)
    newImg = ImageTk.PhotoImage(image)
    img1 = tk.Label(this.frame, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
    img1.pack()
    img1.image = newImg

    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' 4. Name the App Prismatic Player, fill in any description, ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' and click the two checkboxes. ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()


    image = Image.open("photos/"+str(3)+".png")
    image = image.resize((450, 250), Image.ANTIALIAS)
    newImg = ImageTk.PhotoImage(image)
    img1 = tk.Label(this.frame, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
    img1.pack()
    img1.image = newImg

    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' 5. After clicking Create, you will see your app homepage. ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' Click SHOW CLIENT SECRET to reveal your client secret ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' Copy and Paste the Client Id and Client Secret into ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' the Prismatic Player setup. ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    
    image = Image.open("photos/"+str(4)+".png")
    image = image.resize((450, 250), Image.ANTIALIAS)
    newImg = ImageTk.PhotoImage(image)
    img1 = tk.Label(this.frame, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
    img1.pack()
    img1.image = newImg

    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' 6. After copy and pasting the values, navigate back to ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' your app homepage and click the EDIT SETTINGS Button. ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' In the Redirect URIs entry, type in: ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' prismatic-player-login://callback ', justify = 'center', bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' and click ADD. Scroll to the bottom and click SAVE.', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    
    image = Image.open("photos/"+str(4)+".png")
    image = image.resize((450, 250), Image.ANTIALIAS)
    newImg = ImageTk.PhotoImage(image)
    img1 = tk.Label(this.frame, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
    img1.pack()
    img1.image = newImg

    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()

    image = Image.open("photos/"+str(6)+".png")
    image = image.resize((450, 250), Image.ANTIALIAS)
    newImg = ImageTk.PhotoImage(image)
    img1 = tk.Label(this.frame, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
    img1.pack()
    img1.image = newImg

    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()

    image = Image.open("photos/"+str(8)+".png")
    image = image.resize((450, 250), Image.ANTIALIAS)
    newImg = ImageTk.PhotoImage(image)
    img1 = tk.Label(this.frame, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
    img1.pack()
    img1.image = newImg

    
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' 7. Congratulations! You now have created your own Spotify ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' App Server! Click Submit in the Prismatic Player Setup ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= ' and follow the last step. ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    tk.Label(this.frame, text= '  ', justify = 'center', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).pack()
    this.privacyPolicyCanvas.configure(scrollregion=this.privacyPolicyCanvas.bbox('all'), yscrollcommand=this.scroll_y.set)
    this.privacyPolicyCanvas.yview_scroll(10, "units")





    this.advancedSetupCanvas = tk.Canvas(this.window, bg = '#0f0f0f', bd=0, highlightthickness=0, width = 500, height = 300)
    this.advancedSetupCanvas.grid(row = 2, column = 0, columnspan = 2)
    this.client_idText      = tk.Label(this.advancedSetupCanvas, text="Client Id:", bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row=2, pady=(5,5))
    this.client_idEntry     = tk.Entry(this.advancedSetupCanvas, insertbackground = '#1ed761', width = 30, bg = '#0f0f0f', fg = 'white', font=("Circular", 16), highlightcolor = '#1ed761', relief='flat', textvariable = this.client_id).grid(row=2, column=1, pady=(5,5))
    
    this.client_secretText  = tk.Label(this.advancedSetupCanvas, text="Client Secret:", bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row=3, pady=(5,5))
    this.client_secretEntry = tk.Entry(this.advancedSetupCanvas, insertbackground = '#1ed761', width = 30, bg = '#0f0f0f', fg = 'white', font=("Circular", 16), highlightcolor = '#1ed761', relief='flat', textvariable = this.client_secret).grid(row=3, column=1, pady=(5,5))
    
    this.redirect_URLText   = tk.Label(this.advancedSetupCanvas, text="Redirect URI:", bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row=4, pady=(5,5))
    this.redirect_urlEnrty  = tk.Entry(this.advancedSetupCanvas, insertbackground = '#1ed761', width = 30, bg = '#0f0f0f', fg = 'white', font=("Circular", 16), highlightcolor = '#1ed761', relief='flat', textvariable = this.redirect_url).grid(row=4, column=1, pady=(5,5))
    
    this.client_id.set("")
    this.client_secret.set("")
    this.redirect_url.set("prismatic-player-login://callback")
  def setAuth(this):
    this.callback_urlCanvas = tk.Canvas(this.window, bg = '#0f0f0f', bd=0, highlightthickness=0, width = 500, height = 300)
    this.callback_urlCanvas.grid(row = 6, column = 0, columnspan = 2)

    this.callback_urlInstructions = tk.Label(this.callback_urlCanvas, text='After logging into your spotify account and clicking agree,', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 0, columnspan = 2)
    tk.Label(this.callback_urlCanvas, text='you will be directed to a blank website.', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 1, columnspan = 2)
    tk.Label(this.callback_urlCanvas, text='Please Copy and Paste the Url into the                                       ', bg = '#0f0f0f', fg = 'white', font=("Circular", 16)).grid(row = 2, columnspan = 2)
    this.callback_urlHighlight = tk.Label(this.callback_urlCanvas, text='Callback Url Entry!', bg = '#0f0f0f', fg = '#34a1eb', font="Circular 16 underline")
    this.callback_urlHighlight.grid(row = 2, columnspan = 2, sticky ='e', padx=(0,14))
    this.callback_urlHighlight.bind('<Button-1>', this.openCallbackHelp)
    this.callback_urlText   = tk.Label(this.callback_urlCanvas, text="Callback URL:", bg = '#0f0f0f', fg = '#1ed761', font=("Circular", 16)).grid(row=6, column=0, pady=(15,0), sticky='e')
    this.callback_urlEntry  = tk.Entry(this.callback_urlCanvas, insertbackground = '#1ed761',width = 30, bg = '#0f0f0f', fg = 'white', font=("Circular", 16), highlightcolor = '#1ed761', relief='flat', textvariable = this.callback_url).grid(row=6, column=1,pady=(15,0), sticky='w')
    
    this.sendButton = tk.Button(this.callback_urlCanvas, text = "Send URL", command = this.sendURL, width = 10, font=("Circular", 16), relief = 'flat', borderwidth=0, highlightthickness = 0, bd = 0)
    this.sendButton.grid(row=7, columnspan=2, pady=(15,15))

    this.authDataCreated = True
    append_write = 'w'
    authData = open('authData.csv',append_write)
    authData.write("username,client_id,client_secret,redirect_url" + "\n" +
              this.username.get() + "," + 
              this.client_id.get() + "," + 
              this.client_secret.get() + "," + 
              this.redirect_url.get())
    authData.close()
    this.getToken()
  def openCallbackHelp(this, event):
    try:
      this.callbackHelp.destroy()
      this.callbackHelp = tk.Toplevel()
      this.callbackHelp.geometry("%dx%d+%d+%d" % (720, 400, 500, 0))
      this.callbackHelp.resizable(False, False)
      this.callbackHelp.title('Help')
      image = Image.open("photos/help.png")
      image = image.resize((720, 400), Image.ANTIALIAS)
      newImg = ImageTk.PhotoImage(image)
      img1 = tk.Label(this.callbackHelp, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
      img1.pack()
      img1.image = newImg
    except:  
      this.callbackHelp = tk.Toplevel()
      this.callbackHelp.geometry("%dx%d+%d+%d" % (720, 400, 500, 0))
      this.callbackHelp.resizable(False, False)
      this.callbackHelp.title('Help')
      image = Image.open("photos/help.png")
      image = image.resize((720, 400), Image.ANTIALIAS)
      newImg = ImageTk.PhotoImage(image)
      img1 = tk.Label(this.callbackHelp, image = newImg, bd = 0, borderwidth=0, highlightthickness = 0, bg = '#0f0f0f')
      img1.pack()
      img1.image = newImg
  def getToken(this):
    if (not os.path.exists('authData.csv')):
      this.window.mainloop()
      if(this.authDataCreated == True and this.initialRun == False):
        pass
      else:
        try:
          os.remove('authData.csv')
        except:
          pass
      return this.initialRun
    elif(os.path.exists('authData.csv')):
      with open('authData.csv', newline='') as csvfile:
        reader =  csv.DictReader(csvfile)
        data = list(reader)[0]
        username = data.get('username')
        client_id = data.get('client_id')
        client_secret = data.get('client_secret')
        redirect_url = data.get('redirect_url')
      scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-read-private'
      cache_path = ".cache-" + username

      if(os.path.exists(cache_path)):
        this.window.update_idletasks()
        this.window.destroy()
        token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_url)
        spotify = spotipy.Spotify(auth=token)
        
        return spotify
      elif(this.code == ""):
        try:
          this.sp_oauth = spotipy.SpotifyOAuth(client_id,client_secret,redirect_url,scope=scope,cache_path=cache_path,show_dialog=False)
          this.sp_oauth.get_auth_response()
        except:
          os.remove('authData.csv')
          messagebox.showwarning(title="ColorFlow", message="Did not receive correct data.\nPlease try again.")
          this.window.destroy()
          sys.exit()
      else:
        try:
          this.initialRun = False
          token = this.sp_oauth.get_access_token(this.code, as_dict=False)
          messagebox.showinfo(title=None, message='Succesfully Authenticated!')
          this.window.destroy()

        except:
          os.remove('authData.csv')
          messagebox.showwarning(title="ColorFlow", message="Did not receive correct data.\nPlease try again.")
          this.window.destroy()
          sys.exit()
  def sendURL(this):
    try:
      this.callbackHelp.destroy()
    except:
      pass
    code = this.callback_url.get()
    string = this.redirect_url.get() + "/?code="
    this.code = code.replace(string,"")
    this.getToken()

def clearCache():
  with open('authData.csv', newline='') as csvfile:
    reader =  csv.DictReader(csvfile)
    data = list(reader)[0]
    username = data.get('username')
  fileName = ".cache-"+ str(username)
  os.remove(fileName)
  os.remove('authData.csv')
def refreshToken():
  with open('authData.csv', newline='') as csvfile:
    reader =  csv.DictReader(csvfile)
    data = list(reader)[0]
    username = data.get('username')
    client_id = data.get('client_id')
    client_secret = data.get('client_secret')
    redirect_url = data.get('redirect_url')
  scope = 'user-read-currently-playing user-read-playback-state user-modify-playback-state playlist-read-private'
  token = util.prompt_for_user_token(username,scope,client_id=client_id,client_secret=client_secret,redirect_uri=redirect_url)
  spotify = spotipy.Spotify(auth=token)
  return spotify





