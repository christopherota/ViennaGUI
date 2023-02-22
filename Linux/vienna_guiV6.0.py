#This is a GUI program for the top three commonly used
#Vienna RNA programs, RNAfold, RNAalifold, and RNAplfold.
#This program is for Linux only

#Import modules for main GUI program
import vienna_config_v1
import os, sys, subprocess, shutil, time
import tkinter as tk
import io
import webbrowser
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile
from PIL import Image, ImageTk
from PIL.PngImagePlugin import PngInfo
from io import BytesIO
import requests
import urllib.request





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
    if rbtn.get()==1:
       #if txt_seq is showing do the following
       if txt_seq.winfo_ismapped() == True:
	  print ("sequence length: ",len(txt_seq.get(1.0, "end-1c")))
          with open ("input.txt", "w") as usr_inp:
            usr_inp.write(txt_seq.get(1.0, "end-1c").replace('\n',''))
          os.system("RNAfold < input.txt")
          print ("Finished one sequence")
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
          
    elif rbtn.get()==2:
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
def open_help():
    webbrowser.open_new('https://github.com/christopherota/ViennaGUI/blob/fcc4c8bf59847437cc5aaa1c8fba28f27335e1c7/Linux/Table%20of%20Contents.pdf?raw=true')

    
#splash screen window dimmensions, labels, and text
def splash_screen():

    splash_root = tk.Tk()


    splash_root.title("ViennaRNA")
    splash_root.config(bg='#36454f')

    splash_img = 'https://github.com/christopherota/ViennaGUI/blob/main/Linux/RNAimg.png?raw=true'
    with urllib.request.urlopen(splash_img) as u:
        raw_data = u.read()
    im = Image.open(BytesIO(raw_data))
    img1 = ImageTk.PhotoImage(im)
    img_label = tk.Label(splash_root, image=img1)
    img_label.image = img1
    img_label.pack(side="top", fill="both", expand=True)


    splash_label = Label(splash_root, text="Welcome to ViennaRNA", font=30, background='#36454f', fg='white')
    splash_label.pack(side="top", fill="both", expand=True)

    label = tk.Label(splash_root, text="Loading...", font=("Helvetica", 24), bg='#36454f', fg='white')
    label.pack(side="top", fill="both", expand=True)

#limits splash screen to 5 seconds and moves to main_window protocol to close and open main window.
    splash_root.after(4000,main_window)
    splash_root.after(4100,splash_root.destroy)


#function to open main window after destroying splash screen
#Main GUI window title and dimensions
#The GUI uses grid as the geometry
    
def main_window():

    
    window = tk.Tk()
    window.title ("ViennaRNA Package")
    window.config(bg='#36454f')
    
    #Variables for checkbutton and radio button
    cb = IntVar()
    rbtn = IntVar()

#Additional details for main GUI window
#Welcome and enter sequence labels on main GUI window
    prg_title = Label(window, text="Welcome to Vienna RNA Program",
       font=("Times New Roman", 14),bg='#36454f', fg="white").grid(
       row=0, columnspan=15, padx=5, pady=5)
       
    prg_choice1 = Radiobutton(window, text="RNAfold", variable=rbtn,
       value=1, command=fold_pl_select, bg='#36454f', fg="white")
    prg_choice1.grid(row=1, column=3)
       
    prg_choice2 = Radiobutton(window, text="RNAalifold", variable=rbtn,
       value=2, command=aln_select, bg='#36454f', fg="white")
    prg_choice2.grid(row=1, column=4, padx=3, pady=3)

    prg_choice3 = Radiobutton(window, text="RNAplfold", variable=rbtn,
       value=3, command=fold_pl_select, bg='#36454f', fg="white") 
    prg_choice3.grid(row=1, column=5)
    rbtn.set(1)

    lbl_seq = Label(window, text="Enter RNA sequence: ",
       font=("Times New Roman", 12), bg='#36454f', fg="white").grid(
       row=2, columnspan=15, padx=5, pady=5)

#Text box and go button on main GUI window
    global txt_seq, go_btn, inp_seq, quit_btn
    global cb_file, browse_box, browse_btn, browse_btn2

    txt_seq = Text(window, width=40, height=10)
    txt_seq.grid(row=4, column=1, columnspan=5, padx=5, pady=25)
    inp_seq = txt_seq.get(1.0, "end-1c")

    go_btn = Button(window, text="Go", command=go_event, highlightbackground='#36454f').grid(row=4, column=7, padx=5, pady=10)


#Checkbutton and browse on main GUI window
    cb_file = Checkbutton(window, text="To upload file, check box", variable=cb,command= isChecked, bg='#36454f',fg='white')
    cb_file.grid(row=6, column=1, columnspan=5, sticky=W, padx=5, pady=5)  
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

    help_button = tk.Button(window, text="Help", highlightbackground='#36454f', command=open_help)
    help_button.grid(row=0, column=7, padx=3, pady=3)
    
#Quit button on main GUI window to delete tmp and close program
    quit_btn = Button(window, text="Quit", command=quit_prg, highlightbackground='#36454f')
    quit_btn.grid(row=6, column=7, padx=5, pady=5)



#When closing by clicking X, delete tmp and close program
    window.protocol("WM_DELETE_WINDOW", quit_prg)


splash_screen()









