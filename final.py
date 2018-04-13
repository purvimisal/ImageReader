import tkinter as tk
import pyscreenshot as ImageGrab
import os
from tkinter import filedialog

canvas_width = 500
canvas_height = 150

top = tk.Tk()
top.resizable(width=False, height=False)
top.geometry('{}x{}'.format(500, 500))
top.wm_title("OCR Software")

global extracted_text
extracted_text = ""

def SubmitCallBack(feedback_entry, feedback_submit):
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
	text_box = tk.Text(feedback_entry, height = 10, padx = 150, bg = 'light grey', font = 'bold')
	text_box.insert(tk.INSERT, 'Accuracy:\n\n')
	text_box.insert(tk.INSERT, str(a) + ' % ')
	text_box.pack(side = 'bottom')
	feedback_submit.destroy()


def FeedbackCallBack(upload):
    feedback = tk.Tk()
    feedback.resizable(width=False, height=False)
    feedback.geometry('{}x{}'.format(500, 200))
    feedback.wm_title("Feedback Page")
    upload.destroy()   
    feedback_entry = tk.Entry(feedback)
    feedback_submit = tk.Button(feedback,text='Enter',command=lambda:SubmitCallBack(feedback_entry,feedback_submit ))
    feedback_entry.pack()
    feedback_submit.pack()


def HandwritingCallBack(master):
	global extracted_text
	master.destroy()
	handwriting_window = tk.Tk()
	handwriting_window.resizable(width=False, height=False)
	handwriting_window.wm_title('Handwriting Recognition')
	handwriting_window.geometry('{}x{}'.format(500, 200))
	   
	extracted_text = os.popen('pngtopnm lala.png | ocrad').read()
	Feedback_button = tk.Button(handwriting_window, text = 'Feedback', command = lambda: FeedbackCallBack(handwriting_window))
	Feedback_button.pack()
	text_box = tk.Text(handwriting_window, height = 10, padx = 150, bg = 'light grey', font = 'bold')
	text_box.insert(tk.INSERT, 'Extracted Text:\n\n')
	text_box.insert(tk.INSERT, extracted_text)
	text_box.pack(side = 'bottom')	
	
def helloCallBack(top):
	top.destroy()
	def paint( event ):
	   python_green = "#476042"
	   x1, y1 = ( event.x - 1 ), ( event.y - 1 )
	   x2, y2 = ( event.x + 1 ), ( event.y + 1 )
	   w.create_oval( x1, y1, x2, y2, fill = python_green )

	master = tk.Tk()
	master.title( "Enter text using a mouse" )
	w = tk.Canvas(master, 
		   width=canvas_width, 
		   height=canvas_height)
	w.pack(expand = 'yes', fill = 'both')
	w.bind( "<B1-Motion>", paint )

	message = tk.Label( master, text = "Press and Drag the mouse to draw" )
	message.pack( side = 'bottom' )
	def quit(event):                           
	    import sys; sys.exit() 

	widget = tk.Button(master, text='QUIT')
	widget.pack()
	widget.bind('<Button-1>', quit) 

	def button_clear(event):
		w.delete("all")

	def saveim(event):
		im = ImageGrab.grab(bbox=(425, 245, 925, 396))
		im.save('lala.png')
		

	widget = tk.Button(master, text='Done')
	widget.pack()
	widget.bind('<Button-1>', saveim)
	
	widget = tk.Button(master, text='clear')
	widget.pack()
	widget.bind('<Button-1>', button_clear)
	
	Analyse_Button = tk.Button(master, text ="Run OCR", command = lambda: HandwritingCallBack(master))
	Analyse_Button.pack()
	
	w.update()	
	widget.mainloop()


def BrowseCallBack(upload):
	global extracted_text
	file = filedialog.askopenfile(parent=upload,mode='rb',title='Choose a file')
	check = file.name[-4:]
	if file != None and (check == '.png' or check == '.jpg'):  
		extracted_text = os.popen('pngtopnm ' + file.name[-9:] +' | ocrad').read()
		text_box = tk.Text(upload, height = 10, padx = 150, bg = 'light grey', font = 'bold')
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
    uploader_text = tk.Text(upload, height = 5, padx = 150, bg = 'light grey', font = 'bold')
    uploader_text.insert(tk.INSERT, "Please choose a file")
    uploader_text.pack(side = 'top')
    Browse_button = tk.Button(upload, text = 'Browse', command = lambda: BrowseCallBack(upload), width = 20, height = 5)
    Browse_button.pack()
    Feedback_button = tk.Button(upload, text = 'Feedback', command = lambda: FeedbackCallBack(upload), width  =20, height = 5)
    Feedback_button.pack()
    top.destroy()
    	

B = tk.Button(top, text ="Writer", command = lambda: helloCallBack(top), width = 20, height = 20)
C = tk.Button(top, text = 'Uploader', command = lambda: UploadCallBack(top), width = 20, height = 20)

text = tk.Text(top, height = 5, padx = 150, bg = 'light grey', font = 'bold')
text.insert(tk.INSERT, "Please choose an option")
text.pack(side = 'top')


B.pack(side = 'left')
C.pack(side = 'right')

top.mainloop()  
 
