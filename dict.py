#for the dictionary data
import json
#for trying to help user when they accideently mispell a word
from difflib import get_close_matches
from tkinter import *
#for message box when exiting (messagebox)
from tkinter.messagebox import *
#for audio
import pyttsx3 as pp
#for speach to text
engine = pp.init()
#voices we will get we store it in the variable voice
voices = engine.getProperty('voices')
#sets what type of voice we want (0=male, 1=female)
engine.setProperty('voice', voices[1].id)


def wordaudio():
    #whatever the user puts as text the bot says it back
    engine.say(enterwordentry.get())
    engine.runAndWait()

def meaningaudio():
    #say what it is in the text area
    engine.say(textarea.get(1.0,END))
    engine.runAndWait()

#For the clear button. When the user clicks teh button it will refrence this functin and clear everything from the entry field and text area
def clear():
    #from start to beginning the text is cleared
    textarea.config(state=NORMAL)
    enterwordentry.delete(0, END)
    textarea.delete(1.0, END)
    textarea.config(state=DISABLED)

#For the exit button. When user clicks the button it will reference this function and exit the GUI. askyesno is method part of python
def iexit():
    res = askyesno('Confirm', 'Do you want to exit?')
    if res:
        #if res returns true 
        root.destroy()

    else:
        #if res returns false
        pass


meaning = ''
#To load data 
def search():
    global meaning
    textarea.delete(1.0, END)

    #our jason file is now in the data variable and able to be accessed
    data = json.load(open("data.json"))

    #Get the word the user input and make it lower case(b/c the jason file is all lowercase)
    word = enterwordentry.get()
    word = word.lower()
    #Will check if the word is in the data.jason file
    if word in data:
        #We want the meaning but not in a list so we store it in meaning
        meaning = data[word]
        #want to configure the textarea to be able to type again
        textarea.config(state=NORMAL)
        
    #If we mispell a word and we try to help user to correct it by using the "get_close_matches" method
    #word will be compared with the keys on the data file
    elif len(get_close_matches(word, data.keys())) > 0:
        #gets the closest match keys and assigns it to close_match and pass the 0 index to read eveything on the list
        close_match = get_close_matches(word, data.keys())[0]
        res = askyesno('Confirm', f'Did you mean {close_match} instead?')
        if res==True:
            #When user confirms has teh wrong word, delete the previous meaning and then match it with the correct definition
            meaning = data[close_match]
            textarea.delete(1.0, END)
            textarea.config(state=NORMAL)

        else:
            #When the user clicks no. Deleats eveything from the meaning area. Prints out a messagebox
            textarea.delete(1.0, END)
            showinfo("Information", "The word doesn't exist\nType a new word")
            #deleates eveything from the text area and allows user to input new word
            enterwordentry.delete(0,END)
            meaning = ''

    #If user types in random characters
    else:
        showerror("Error", "The word doesn't exist.")
    
    if meaning != '':
        if type(meaning) == list:
            for item in meaning:
                #display multplie meanings in seperate lines in the textarea
                textarea.insert(END, u'\u2022' + item + '\n\n')
                #doesn't allow user to change or type in the meaning area
                textarea.config(state=DISABLED)
        else:
            textarea.insert(END, meaning)

#----------------------------------UI----------------------------------------------------------------------------------------------
root = Tk()
#Size to the window. Don't want user to max window. Want window to show up in the same position
root.geometry('1000x626+100+100')
root.title('Caption-ary')
root.resizable(0, 0)

#Background
bgImg = PhotoImage(file='bg1.png')
bgLabel = Label(root, image=bgImg)
bgLabel.place(x=0, y=0)

#Enter Label
enterwordLabel = Label(root, text='Enter Word', font=('castellar', 29, 'bold'), fg='gold', bg='red3')
enterwordLabel.place(x=530, y=20)
#entry field can only type things in a single line. Entry text can be multiple lines. Justify shows blinking cursor in center.
enterwordentry = Entry(root, font=('arial', 23, 'bold'), bd=8, relief=FLAT, justify=CENTER)
enterwordentry.place(x=510, y=80)
#Cursor becomes automatically blinking vs clinking on it when UI pops up
enterwordentry.focus_set()

#Search Button
searchImg = PhotoImage(file='searchBttn.png')
#Cursor is changed to hand2. Active background is for when the user presses the button and teh color changes.
searchButton = Button(root, image=searchImg, bd=0, bg='black', activebackground='gold', cursor='hand2',
                      command=search)
searchButton.place(x=620, y=150)

#Mic Button
micimage = PhotoImage(file='MicBttn.png')
#command refrences the wordaudio function to hear the speech
micButton = Button(root, image=micimage, bd=0, bg='black', activebackground='gold', cursor='hand2',command=wordaudio)
micButton.place(x=710, y=153)

#Definition Label
definitionLabel = Label(root, text='Definition', font=('castellar', 29, 'bold'), fg='gold', bg='red3')
definitionLabel.place(x=580, y=240)

#Text Area
#wrap will show a complete word going to a new line vs going off the text area.
textarea = Text(root, font=('arial', 18, 'bold'), bd=8, relief=FLAT, height=8, width=34, wrap='word')
textarea.place(x=460, y=300)

#Mic Button to hear the defnition back
audioImg = PhotoImage(file='micBttn.png')
#command refrences the meaningaudio to get the defintion and say it to the user
audioButton = Button(root, image=audioImg, bd=0, bg='black', activebackground='gold', cursor='hand2',command=meaningaudio)
audioButton.place(x=530, y=555)

#Clear Button
clearImg = PhotoImage(file='clear.png')
#When user clicks on clear button, the command is used. We pass the refrence of the function clear
clearButton = Button(root, image=clearImg, bd=0, bg='black', activebackground='gold', cursor='hand2',
                     command=clear)
clearButton.place(x=660, y=555)

#Exit Button
exitImg = PhotoImage(file='exitBttn.png')
#When user clicks on exit button, the command is used. We pass the reference of the function iexit
exitButton = Button(root, image=exitImg, bd=0, bg='black', activebackground='gold', cursor='hand2',
                    command=iexit)
exitButton.place(x=790, y=555)

def enter_function(event):
    searchButton.invoke()


root.bind('<Return>', enter_function)

root.mainloop()
