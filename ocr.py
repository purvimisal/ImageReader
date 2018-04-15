import Tkinter as tk
import pyscreenshot as ImageGrab
import os
import tkFileDialog
from gtts import gTTS 
import pyttsx
canvas_width = 500
canvas_height = 150

top = tk.Tk()
top.resizable(width=False, height=False)
top.geometry('{}x{}'.format(500, 500))
top.wm_title("IMAGE READER")

global extracted_text
extracted_text = ""

def ExitWindow(audio):
	audio.destroy()

def SubmitCallBack(feedback_entry, feedback_submit): #Calculate accuracy of the original text and extracted text (by ocrad) 
	global accuracy
	global extracted_text
	text = feedback_entry.get()
	text = text.lower()
	extracted_text = extracted_text.lower()
	count = 0
	na = len(extracted_text)
	nb = len(text)
	n = na
	if (nb < na):
		n = nb
	for i in range(0, n):
		if extracted_text[i] == text[i]:
			count += 1
	a = count * 100 / len(text)
	text_box = tk.Text(feedback_entry, height = 10, padx = 150, bg = 'lavender', font = 'bold')
	text_box.insert(tk.INSERT, 'Accuracy:\n\n')
	text_box.insert(tk.INSERT, str(a) + ' % ')
	text_box.pack(side = 'bottom')
	feedback_submit.destroy()

def CreateAudio(create_audio):
	global extracted_text
	extracted_text = extracted_text.lower()
	tts = gTTS(text = extracted_text, lang = 'en')
    	tts.save("audio1.mp3")
    	
    	
def PlayAudio(play_audio):
	global extracted_text
	voiceEngine = pyttsx.init()
	voiceEngine.setProperty('rate', 100)
	voiceEngine.say(extracted_text)
	voiceEngine.runAndWait()	

def FeedbackCallBack(upload): #Function to generate a Feedback page where original text can be entered
    feedback = tk.Tk()
    feedback.resizable(width=False, height=False)
    feedback.geometry('{}x{}'.format(500, 200))
    feedback.wm_title("Feedback Page")
    #upload.destroy()   
    feedback_entry = tk.Entry(feedback)
    feedback_submit = tk.Button(feedback,text='Enter',command=lambda:SubmitCallBack(feedback_entry,feedback_submit ))
    feedback_entry.pack()
    feedback_submit.pack()

def AudioCallBack(upload): #Function to  generate a page to create the audio file 
	audio = tk.Tk()
	audio.resizable(width=False, height=False)
    	audio.geometry('{}x{}'.format(500, 200))
    	audio.wm_title("Audio Page")
    	upload.destroy()
    	create_audio = tk.Button(audio, text= "Save mp3 file", command=lambda: CreateAudio(create_audio))
    	play_audio = tk.Button(audio, text= "Play mp3 file", command=lambda: PlayAudio(play_audio))
    	exit = tk.Button(audio, text= "Exit...", command=lambda: ExitWindow(audio))
    	create_audio.pack()
    	play_audio.pack()
    	exit.pack()

	
def BrowseCallBack(upload):
	global extracted_text
	file = tkFileDialog.askopenfile(parent=upload,mode='rb',title='Choose a file')
	check = file.name[-4:]
	if file != None and (check == '.png' or check == '.jpg'):  
		extracted_text = os.popen('pngtopnm ' + file.name[-9:] +' | ocrad').read()
		text_box = tk.Text(upload, height = 10, padx = 150, bg = 'lavender', font = 'bold')
		text_box.insert(tk.INSERT, 'Extracted Text:\n\n')
		text_box.insert(tk.INSERT, extracted_text)
		text_box.pack(side = 'bottom')      
		file.close()

	if check != '.png' and check != '.jpg':
		print("Error in selecting file. Please choose a png/jpg file")

def UploadCallBack(top):
    upload = tk.Tk()
    upload.resizable(width=False, height=False)
    upload.geometry('{}x{}'.format(500, 500))
    upload.wm_title("Uploader Page")
    uploader_text = tk.Text(upload, height = 5, padx = 150, bg = 'lavender', font = 'bold')
    uploader_text.insert(tk.INSERT, "Please choose a file")
    uploader_text.pack(side = 'top')
    Browse_button = tk.Button(upload, text = 'Browse', command = lambda: BrowseCallBack(upload), width = 20, height = 5)
    Browse_button.pack()
    Audio_button = tk.Button(upload, text = 'Create Audio', command = lambda: AudioCallBack(upload), width  =20, height = 5)
    Feedback_button = tk.Button(upload, text = 'Feedback', command = lambda: FeedbackCallBack(upload), width  =20, height = 5)
    Audio_button.pack()
    Feedback_button.pack()
    top.destroy()
    	

#B = tk.Button(top, text ="Writer", command = lambda: helloCallBack(top), width = 20, height = 20)
C = tk.Button(top, text = 'Uploader', command = lambda: UploadCallBack(top), width = 20, height = 10)

text = tk.Text(top, height = 5, padx = 150, bg = 'lavender', font = 'bold')
text.insert(tk.INSERT, "Image Reader Software \n\n\n\n Upload the image file:")
text.pack(side = 'top')


#B.pack(side = 'left')
C.pack(side = 'top')
top.mainloop()  

