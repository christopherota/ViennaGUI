#This is a GUI program for the top three commonly used
#Vienna RNA programs, RNAfold, RNAalifold, and RNAplfold.
#This program is for Linux only

#Import modules for main GUI program
import vienna_config_v2
import os, sys, subprocess, shutil, time, threading
import tkinter as tk
import io
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from PIL.PngImagePlugin import PngInfo
from io import BytesIO
from tkinter import ttk
import requests
import urllib.request
import socket






#Define functions for the GUI

#This function shows the widget on the window 
def display(widget1):
    widget1.grid()

#This function hides the widget on the window
def remove(widget1):
    widget1.grid_remove()

#This function opens the browse window and allows only fasta
#and text files to be used. When file selected add to the
#textbox
def browse():    
    file = askopenfile(mode='rb', title='Choose a file',
    filetypes=(('fasta files','*.fa *.fasta *.fna *.ffn *.faa *.frn'),
               ('text files','*.txt')))
    
    global filepath
    filepath = ""
    if file:
        filepath = os.path.abspath(file.name)
        #print (filepath)
        browse_box.delete(0, 'end')
        browse_box.insert(0, filepath)
        
#This function opens browse window for alignment files only.
#This is specific to RNAalifold
def browse_aln():    
    file = askopenfile(mode='rb', title='Choose a file',
    filetypes=(('Clustal files','*.aln'), ('Stockholm', '*.sto *.stk'),
               ('fasta files','*.fa *.fasta *.fna *.ffn *.faa *.frn'),
               ('MAF files', '*.maf')))
    
    global filepath
    filepath = ""
    if file:
        filepath = os.path.abspath(file.name)
        #print (filepath)
        browse_box.delete(0, 'end')
        browse_box.insert(0, filepath)


#This function dictates what happens when the checkbutton widget
#is checked. When checked, hide large textbox and show the browse
#box and the browse button. When unchecked, hide browse box and
#browse button
def isChecked():
    if cb.get():
        
        remove(txt_seq)
        display(browse_box)
        browse_box.delete(0, 'end')
        display(browse_btn)

                                
    else:
        remove(browse_box)
        remove(browse_btn)
        display(txt_seq)

#This function will display widgets for RNAfold program
def fold_pl_select():
    if txt_seq.winfo_ismapped() == True and cb_file.winfo_ismapped() == True:
       remove(browse_box)
       remove(browse_btn2)
       remove(browse_btn)
       cb.set(0)
       print("textbox present")
       print("checkbox present")
       
    elif browse_box.winfo_ismapped() == True:
       remove(browse_box)
       remove(browse_btn2)
       remove(browse_btn)
       display(txt_seq)
       cb.set(0)
       display(cb_file)
          #cb_file.grid(row=6, column=1, columnspan=5, 
          #             sticky=W, padx=5, pady=5)
             
    else:
       cb.set(0)
       print("nothing to change")
          #cb_file.grid(row=6, column=1, columnspan=5, sticky=W, padx=5, pady=5)
          
#This function will display widgets for RNAalifold program
def aln_select():
    remove(txt_seq)
    remove(cb_file)
    
    display(browse_box)
    browse_box.delete(0, 'end')
    display(browse_btn2)
    

#This function will give output after the go button is pressed, 
#depending on input from text box or opening file
def go_event():
    global program
    global user_input
# This line edited by Andy
    if Combo.get()== "RNAfold":
       if txt_seq.winfo_ismapped() == True:
          with open ("input.txt", "w") as usr_inp:
            usr_inp.write(txt_seq.get(1.0, "end-1c"))
          subprocess.run(["RNAfold", "input.txt"])  
          #find the ps file
          find_file()
          #open the ps file on canvas      
          open_file()
          program = "RNAfold"
          user_input = "text"
            
       #else do this instead
       else:
          subprocess.run(["RNAfold", filepath])
          #find the ps file
          find_file()
          
          #open the ps file on canvas      
          open_file()
          program = "RNAfold"
          user_input = "file"
          
      #This line edited by Andy    
    elif Combo.get()=="RNAalifold":
       subprocess.run(["RNAalifold", filepath])
       #find the ps file
       find_file()
       #display the output in terminal     
       #print (output)
       #open the ps file on canvas      
       open_file()
       program = "RNAalifold"
       user_input = "file"
       
    else:   
       #if txt_seq is showing do the following
       if txt_seq.winfo_ismapped() == True:
          with open ("input.txt", "w") as usr_inp:
            usr_inp.write(txt_seq.get(1.0, "end-1c"))
          output = subprocess.run("RNAplfold < input.txt", shell=True)
          #find the ps file
          find_file()
          #display the output in terminal  
          #print (output)
          #open the ps file on canvas      
          open_file()
          program = "RNAplfold"
          user_input = "text"
            
       #else do this instead
       else:
          subprocess.run("RNAplfold < %s" %filepath,
                        shell=True)
          #find the ps file
          find_file()
          #display the output in terminal     
          #print (output)
          #open the ps file on canvas      
          open_file()    
          program = "RNAplfold"
          user_input = "file"
        
#This function will find all .ps files within tmp folder
def find_file():
    global find_ps
    find_ps = []
    list_dir = os.listdir()
    for x in list_dir:
       if x.endswith(".ps"):
          find_ps.append(x)
    
    #sort the list by time ascending
    find_ps = sorted(find_ps, key=os.path.getmtime)
    #returns a list of all ps files
    return find_ps

#This function will open ps file in a different window
def open_file():
    ps_window = Toplevel(window)
    #Toplevel window title and dimensions
    ps_window.title("Output")
    
    #make ps_loc global
    global ps_loc
    ps_loc = ""
    print(find_ps)
    for y in find_ps:
       ps_loc = os.path.join(os.getcwd(),y)
        
    #Open the ps file    
    img_open = Image.open(ps_loc)
    img_w, img_h = img_open.size
    
    global img
    img = ImageTk.PhotoImage(img_open)
    
    #Create a blank canvas
    ps_canvas = Canvas(ps_window, width = img_w, height = img_h, 
                       bg= "white", highlightthickness=0)
    
    #Paste the ps file onto the canvas
    ps_canvas.create_image(0, 0, anchor="nw", image=img)
    ps_canvas.grid()
    
    #add a download button so the images can be downloaded
    download_btn = Button(ps_window, text='Save', width=5, height=1, bd='5', command=save_image)
    download_btn.place(x=img_w-75, y=0, anchor="nw")
    
#This function will download the output
def save_image():
	image = Image.open(ps_loc)
	metadata = PngInfo()
	metadata.add_text("program",program)
	metadata.add_text("user input",user_input)
	size = width, height = image.size
	file_path = filedialog.askdirectory()
	path = os.path.join(file_path, 'photo')
	image.save(path + '_ViennaRNA.png', pnginfo=metadata)
	del image

#Function to quit the program and check if user is sure they want to quit
def quit_prg():
    if messagebox.askokcancel("Quit", 
        "Quitting will delete files\nDo you want to quit?"):
        #change out of directory
        os.chdir('..')
        #remove tmp directory
        shutil.rmtree(os.path.join(os.getcwd(),'tmp'))
        #remove main GUI window
        window.destroy()

#function for help button command to pull url from web
#def open_help():
 #   webbrowser.open_new('https://github.com/christopherota/ViennaGUI/blob/fcc4c8bf59847437cc5aaa1c8fba28f27335e1c7/Linux/Table%20of%20Contents.pdf?raw=true')

#function for help button command to pull help document from file directory as backup
def open_help():
	helpdoc_path = 'helpdoc.pdf'
	helpdoc_path = os.path.join(os.path.dirname(__file__), helpdoc_path)
	webbrowser.open_new(helpdoc_path)
    
#function to destroy the splash screen after loading has occured
def destroy():
	splash_root.destroy()
	
#class and functions for loading bar on splash screen	
class LoadingBar(tk.Frame):
	def __init__(self, parent, width, height, bg_color, fg_color):
		tk.Frame.__init__(self, parent, width=width, height=height, bg=bg_color)
		self.width=width
		self.height=height
		self.fg_color=fg_color
		self.create_widgets()
		
	def create_widgets(self):
		self.loading_bar = tk.Canvas(self, width=self.width, height=self.height, bg=self['bg'])
		self.loading_bar.pack(fill='both',expand=True)
		self.loading_bar.create_rectangle(0,0,0,self.height, fill=self.fg_color, outline=self.fg_color, tags=('loading_bar',))
	
	def update_loading_bar(self, progress):
		self.loading_bar.coords('loading_bar', 0,0, int(progress * self.width), self.height)

# Function to connect to internet host for help document scraping redundancy
# Define a function to check for an internet connection
def check_internet():
    try:
        # Attempt to connect to a well-known internet host
        socket.create_connection(("www.google.com", 80))
        return True
    except OSError:
        pass
    return False

#Andy Code start
def click(event):
	global RNAlabel
	
	for option in options:
		if Combo.get() == "RNAalifold":
			command = aln_select()
		else:
			command = fold_pl_select()
		


# Andy new code end
		
#splash screen window dimmensions, labels, and text
def splash_screen():

    splash_root = tk.Tk()


    splash_root.title("ViennaRNA")
    splash_root.config(bg='#36454f')
    splash_root.geometry("600x600")

    splashimg_path = 'RNAimg.png'
    splashimg_path = os.path.join(os.path.dirname(__file__), splashimg_path)
    splash_img = 'https://github.com/christopherota/ViennaGUI/blob/main/Linux/RNAimg.png?raw=true'
    

#error handling of RNAimg for splash screen. 
    try:
    	with urllib.request.urlopen(splash_img) as u:
        	raw_data = u.read()
    	im = Image.open(BytesIO(raw_data))
    	img1 = ImageTk.PhotoImage(im)
    	img_label = tk.Label(splash_root, image=img1)
    	img_label.image = img1
    	img_label.pack(side="top", fill="both", expand=True)
    except:
    	
    	im = Image.open(splashimg_path)
    	img1 = ImageTk.PhotoImage(im)
    	img_label = tk.Label(splash_root, image=img1)
    	img_label.image = img1
    	img_label.pack(side="top", fill="both", expand=True)
    	


    splash_label = Label(splash_root, text="ViennaRNA GUI", font=30, background='#36454f', fg='white')
    splash_label.pack(side="top", fill="both", expand=True)
    
    # Create the text box and scroll bar for terminal output box
    text_box = Text(splash_root, width=40, height=10)
    scrollbar = tk.Scrollbar(splash_root, command=text_box.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_box.configure(yscrollcommand=scrollbar.set)
	
    text_box.pack(side="top", fill="both", expand=True)

#temp output file for storing terminal output text to feed into tkinter text box.  
    tempoutput_path = 'tempoutput.txt'
    tempoutput_path = os.path.join(os.path.dirname(__file__), tempoutput_path)
    
    with open(tempoutput_path, "r") as f:
    	contents = f.read()
    	text_box.insert(tk.END, contents)
    

    label = tk.Label(splash_root, text="Loading...", font=("Helvetica", 24), bg='#36454f', fg='white')
    label.pack(side="top", fill="both", expand=True)
    

#loading bar

    if __name__ == '__main__':
    	Loading_bar = LoadingBar(splash_root, width=300, height=30, bg_color='#36454f', fg_color='black')
    	Loading_bar.pack()
    	for i in range(10001):
    		Loading_bar.update_loading_bar(i/10000)
    		splash_root.update()

    splash_root.destroy()

splash_screen()

#Main GUI window title and dimensions
#The GUI uses grid as the geometry manager
window = Tk()
window.title ("ViennaRNA GUI")
window.config(bg='#36454f')
window.geometry("450x450")


#Variables for checkbutton and radio button
cb = IntVar()
rbtn = IntVar()

#Additional details for main GUI window
#Welcome and enter sequence labels on main GUI window
prg_title = Label(window, text="Welcome to Vienna RNA GUI",
       font=("Times New Roman", 14), bg='#36454f', fg='white').grid(
       row=0, columnspan=15, padx=5, pady=5)

prg_select_label = Label(window, text="Please Select Program Below:",
       font=("Times New Roman", 14), bg='#36454f', fg='white').grid(
       row=1, columnspan=15, padx=5, pady=5)
       



lbl_seq = Label(window, text="Enter RNA sequence: ",
       font=("Times New Roman", 12), bg='#36454f', fg='white').grid(
       row=3, columnspan=15, padx=5, pady=5)

#Text box and go button on main GUI window
global txt_seq, go_btn, inp_seq, quit_btn
global cb_file, browse_box, browse_btn, browse_btn2

txt_seq = Text(window, width=40, height=10)
txt_seq.grid(row=4, column=1, columnspan=5, padx=5, pady=25)
inp_seq = txt_seq.get(1.0, "end-1c")

go_btn = Button(window, text="Go", command=go_event, highlightbackground ='#36454f' )
go_btn.grid(row=4, column=7, padx=5, pady=10)     


#Checkbutton and browse on main GUI window
cb_file = Checkbutton(window, text="To upload file, check box", variable=cb, 
                      command= isChecked, bg='#36454f', fg='white')
cb_file.grid(row=6, column=1, columnspan=5, padx=5, pady=5)  
cb.set(0)

browse_box = Entry(window, width = 40)
browse_box.grid(row=3, column=1, columnspan=6, padx=5, pady=5)
remove(browse_box)

browse_btn =  Button(window, text="Browse", command=browse)
browse_btn.grid(row=3, column=7, sticky=W, padx=5, pady=5)
remove(browse_btn)

browse_btn2 = Button(window, text="Browse", command=browse_aln)
browse_btn2.grid(row=3, column=7, sticky=W, padx=5, pady=5)
remove(browse_btn2)


help_button = tk.Button(window, text="Help",highlightbackground ='#36454f', command=open_help)
help_button.grid(row=0, column=7, padx=3, pady=3)

#andy code
options = [" ","RNAfold"," ", "RNAalifold"," ", "RNAplfold"]

Combo = ttk.Combobox(window, values = options)
Combo.set("Select Program")
Combo.bind("<<ComboboxSelected>>", click)
Combo.grid(row=2, columnspan=25, padx=10, pady=10)

#andy code
	

    
#Quit button on main GUI window to delete tmp and close program
quit_btn = Button(window, text="Quit", command=quit_prg, highlightbackground ='#36454f')
quit_btn.grid(row=6, column=7, padx=5, pady=5)

#When closing by clicking X, delete tmp and close program
window.protocol("WM_DELETE_WINDOW", quit_prg)


window.mainloop()
#

