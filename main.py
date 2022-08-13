from tkinter.tix import COLUMN
from tkinter.ttk import LabelFrame
from mido import MidiFile
import tkinter
from tkinter import Button, filedialog as tkfile
from tkinter import messagebox
from tkinter import ttk

root = tkinter.Tk()

root.title('MID -> ccMID | File Converter')

outputPath = "."

def selectInputFiles():
    global filePath
    filePath = tkfile.askopenfilenames(title="Open MIDI Files", filetypes =(("MIDI", "*.mid"),("All Files","*.*")))
    print(type(filePath))

def selectOutputFolder():
    global outputPath
    outputPath = tkfile.askdirectory(title="Open Output Folder")
    print(outputPath)

def convertButton():
    try:
        for i in filePath:
            convert(i, outputPath, "TEST", "ME")
    except Exception as e:
        messagebox.showerror("CONVERSION ERROR","ERROR DURING CONVERSION:\n{}".format(e))
    else:
        messagebox.showinfo("CONVERSION DONE","CONVERTED FILE(s)")
        
def limit_octave(note): #limits the note to 3 octaves
    if note < 43:
        while note < 43:
            note += 12
    elif note > 78:
        while note > 78:
            note -= 12
    return note

def convert(filename, outputPath, songname, author):
    file = open(outputPath+"/"+(filename.split("/")[-1])[0:-4]+".ccmid", "w") 

    file.write("meta start\n")  #start of metadata
    file.write("title {}\nauthor {}\n".format(songname,author))

    file.write("meta end\n")    #end of metadata
    file.write("music start\n")   #start of music

    mid = MidiFile(filename)#open midi file

    bpm = 120 # default if for some reason there is no tempo specified
    #get the tempo of the track, regardless of what track it is written in
    for i,track in enumerate(mid.tracks):
        for i, msg in enumerate(track):
            if msg.dict()['type']=="set_tempo":
                bpm = 60000000/msg.dict()['tempo']
                tpm = bpm*mid.ticks_per_beat #get ticks per minute
                tpt = (tpm/60)/20 #get ticks per tick
                break
        else:
            continue
        break

    for i, msg in enumerate(mid.tracks[0]):
        if msg.dict()['type']=="note_on":
            if msg.dict()['velocity'] == 0:
                file.write("off {} {}\n".format(limit_octave(msg.dict()['note']),round(msg.dict()['time']/tpt))) #write note off message
            else:
                file.write("on {} {}\n".format(limit_octave(msg.dict()['note']),round(msg.dict()['time']/tpt))) #write note on message
        if msg.dict()['type']=="note_off":
            file.write("off {} {}\n".format(limit_octave(msg.dict()['note']),round(msg.dict()['time']/tpt))) #write note off message
        if msg.dict()['type']=="set_tempo":
            bpm = 60000000/msg.dict()['tempo']  #adjust tempo if there are on the fly tempo changes
            tpm = bpm*mid.ticks_per_beat #get ticks per minute
            tpt = (tpm/60)/20 #get ticks per tick
            print("WARNING: Speed change while playing, this might not sound good")

    file.write("music end\n")   #end of music
    file.close()#close file


def loop():
    root.after(10,loop)

main = LabelFrame(root,text="CONVERTER")
main.grid(row=0,column=0)

Button(main,text="SELECT FILE(s)",command=selectInputFiles).grid(row=2,column=2,columnspan=1,sticky="NSWE")
Button(main,text="SELECT OUTPUT FOLDER",command=selectOutputFolder).grid(row=1,rowspan=2,columnspan=1,sticky="NSWE")

ttk.Separator(main, orient='vertical').grid(row=1,column=3,sticky="NSWE")

Button(main,text="START CONVERSION",command=convertButton).grid(row=1,column=4,rowspan=2,sticky="NSWE")

root.after(10,loop)
root.mainloop()