import tkinter as tk
import authorization
import functions
import window
import time

spotify = authorization.auth().getToken()
if(spotify == False or spotify == None):
  spotify = authorization.auth().getToken()

try:
  window = window.create(spotify)
except:
  pass