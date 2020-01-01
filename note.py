__author__ = 'Michael_Xiao'
# -*- encoding: utf8 -*-

from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import *
import os

root =Tk()
root.title('Notebook')
root.geometry('800x500')

filename = ''

def newfile():
	global filename
	root.title('new')
	filename = None
	textPad.delete(1.0,END)
	
def openfile():
	global filename
	filename = askopenfilename(defaultextension = '.txt')
	if filename == '':
		filename = None
	else:
		root.title(os.path.abspath(filename))
		textPad.delete(1.0,END)
		f = open(filename,'r')
		textPad.insert(1.0,f.read())
		f.close()

def savefile():
	global filename
	try:
		f = open(filename,'w')
		msg = textPad.get(1.0,END)
		f.write(msg)
		f.close()
	except:
		saveasfile()
		
def saveasfile():
	f = asksaveasfilename(initialfile='new.txt',defaultextension='.txt')
	global filename
	filename = f
	fh = open(f,'w')
	msg = textPad.get(1.0,END)
	fh.write(msg)
	fh.close()
	root.title(os.path.abspath(f))
	
def redo():
	textPad.event_generate('<<Redo>>')

def undo():
	textPad.event_generate('<<Undo>>')

def cut():
	textPad.event_generate('<<Cut>>')
	
def copy():
	textPad.event_generate('<<Copy>>')
	
def paste():
	textPad.event_generate('<<Paste>>')

def select_all():
	textPad.tag_add('sel','1.0',END)

def search_file():
	textPad.tag_config('match',background='#BDFCC9')
	textPad.tag_remove('match','1.0',END)
	searchstr = fw.get()
	pos_start = textPad.search(searchstr,1.0)
	pos_stop = '%s + %dc' % (pos_start,len(searchstr))
	i = 1
	contents = textPad.get(1.0,END)
	a = len(contents)
	count = 0
	while i < a:
		if pos_start == '':
			_error = Toplevel(root)
			_error.geometry('170x50+300+250')
			_error.title('ERROR')
			Label(_error,text='No Found').grid(row=0,column=0,padx=5)
			i = a + 1
		else:
			textPad.tag_add('match',pos_start,pos_stop)
			pos_start = textPad.search(searchstr,pos_stop)
			pos_stop = '%s + %dc' % (pos_start,len(searchstr))
			i += 1
	for j in range(a):
		if searchstr == contents[j:j+len(searchstr)]: 
			count += 1
	topsearch.title(str(count)+' fit')
	
def find_file():
	global topsearch
	topsearch = Toplevel(root)
	topsearch.geometry('250x30+200+250')
	topsearch.title('Search')
	Label(topsearch,text='Find').grid(row=0,column=0,padx=5)
	global fw
	fw = StringVar()
	entry = Entry(topsearch,width=20,textvariable=fw)
	entry.grid(row=0,column=1,padx=5)
	entry.focus_set()
	Button(topsearch,text='find',command=search_file).grid(row=0,column=3,padx=5)
	def close_search():
		textPad.tag_remove('match','1.0',END)
		topsearch.destroy()
	topsearch.protocol('WM_DELETE_WINDOW',close_search)
	
def about():
	AboutMessage = '''
Author	: Michael_Xiao
Create	: 2017-02-06
Version	: 0.1 Beta
	'''
	showinfo('information',AboutMessage)
	

#Create menu
menubar = Menu(root)
root.config(menu=menubar) 

filemenu = Menu(menubar,tearoff=True)
filemenu.add_command(label='New file',command=newfile,accelerator='Ctrl + N')
filemenu.add_command(label='Open',command=openfile,accelerator='Ctrl + O')
filemenu.add_command(label='Save',command=savefile,accelerator='Ctrl + S')
filemenu.add_command(label='Save As',command=saveasfile,accelerator='Ctrl + Shift + S')
filemenu.add_command(label='Quit',command=root.quit,accelerator='Ctrl + Q')
menubar.add_cascade(label='File', menu=filemenu)

editmenu = Menu(menubar,tearoff=True)
editmenu.add_command(label='Undo',command=undo,accelerator='Ctrl + Z')
editmenu.add_command(label='Redo',command=redo,accelerator='Ctrl + Shift + Z')
editmenu.add_separator()
editmenu.add_command(label='Cut',command=cut,accelerator='Ctrl + x')
editmenu.add_command(label='Copy',command=copy,accelerator='Ctrl + C')
editmenu.add_command(label='Paste',command=paste,accelerator='Ctrl + v')
editmenu.add_separator()
editmenu.add_command(label='Select All',command=select_all,accelerator='Ctrl + A')
editmenu.add_command(label='Find',command=find_file,accelerator='Ctrl + F')
menubar.add_cascade(label='Edit', menu=editmenu)

helpmenu = Menu(menubar,tearoff=False)
helpmenu.add_command(label='About',command=about)
menubar.add_cascade(label='Help',menu=helpmenu)

#Status
status = Label(root,text='Ln20',bd=1,relief=SUNKEN,anchor=W)
status.pack(side=BOTTOM,fill=X)
	
#Linenumber&Text
lnlabel = Label(root,width=2,bg='#F0F8FF')
lnlabel.pack(side=LEFT,fill=Y)

textPad = Text(root,undo=True)
textPad.pack(expand=YES,fill=BOTH)

scroll = Scrollbar(textPad)
textPad.config(yscrollcommand=scroll.set)
scroll.config(command=textPad.yview)
scroll.pack(side=RIGHT,fill=Y)

root.mainloop()
