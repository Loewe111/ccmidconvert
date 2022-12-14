# ccmidconvert
A MIDI (.mid) to .ccmid converter. ccmid is a file format that stores midi data in plain text

# What is .ccmid/ccMIDI
ccMIDI is a file format i created to read midi data with computers from the minecraft mod Computercraft. It is MIDI data stored in plaintext format, it is also very readable and easy to parse.

# Layout of ccMIDI files
ccMIDI files have a meta header at the top of the file, they include info like the title of the song. a header starts with a **{header name} start** and ends with a **{header name} end** so an example for a meta header is:

> meta start  
> title bestSongEver  
> author me  
> meta end  

The music header contains all the music data, currently there are only two commands:

> on {note} {duration}  
> off {note} {duration}  

The duration is measured in Ticks (1 Tick = 1/20 sec)  
Music header look like this:

> music start  
> on 56 10  
> off 56 10  
> on 57 0  
> on 56 0  
> on 55 10  
> off 57 5  
> off 56 0  
> off 55 10  
> music end  

# What does the converter do

With the converter you can take one or more MIDI (.mid) files and convert them to ccMIDI (.ccmid) files  
If you convert multiple files at once, the converter will automaticaly choose the midi track. If you want to select the track yourself, you need to convert the files one at a time.

![grafik](https://user-images.githubusercontent.com/78087018/184494254-416d1ead-7ce5-43a2-b364-f829591726c6.png)

The converter currently sets the title to the filename and author to unknown, if you want to change it, just open the .ccmid file in an text editor.  

# To-Do

- Add support for multiple tracks in one file  
- Add support for other message types
