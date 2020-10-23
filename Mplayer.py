import os
import pickle
import tkinter as tk
from tkinter import filedialog
from tkinter import PhotoImage
from pygame import mixer


# ----------------------------- Main -------------------------------------------
window = tk.Tk()
window.geometry('630x430')
window.wm_title('Arkhann Mplayer')
window.iconbitmap('./images/mplay.ico')
#imagenes
img = PhotoImage(file='images/music.gif')
next_ = PhotoImage(file = 'images/next.gif')
prev = PhotoImage(file='images/previous.gif')
play = PhotoImage(file='images/play.gif')
pause = PhotoImage(file='images/pause.gif')
btn_stop = PhotoImage(file='images/stop.png')

#clase mplayer para el reproducto de mp3
class MPlayer(tk.Frame):
	def __init__(self, master=None):
		super().__init__(master)
		self.master = master
		self.pack()
		mixer.init()

		if os.path.exists('canciones.mkm'):
			with open('canciones.mkm', 'rb') as fb:
				self.lista_repro = pickle.load(fb)
		else:
			self.lista_repro=[]

		self.current = 0
		self.paused = True
		self.played = False
		self.stop=True

		self.frames()
		self.cuadro_pista()
		self.panel_de_controle()
		self.panel_lista()

	def frames(self):
		self.pista = tk.Label(self, text='Nombre de Pista',font = ("comic sans",16), bg="grey", fg ="white", bd=5)
		self.pista.config(width =410, height=300)
		self.pista.grid(row=0, column=0,padx=10)

		self.listaPista = tk.LabelFrame(self, text=f'Total Pistas: {str(len(self.lista_repro))}',font=("comic sans",15),bg="grey",fg="white",bd=5)
		self.listaPista.config(width=190,height=400)
		self.listaPista.grid(row=0, column=1, rowspan=3, pady=5)

		self.controles = tk.Label(self,font=("comic sans",16),bg="white",fg="white",bd=2)
		self.controles.config(width = 410, height = 80)
		self.controles.grid(row=2, column=0,pady=5,padx=10)

	def cuadro_pista(self):
		self.canvas = tk.Label(self.pista, image = img)
		self.canvas.configure(width=400, height=240)
		self.canvas.grid(row=0,column=0)

		self.titulo = tk.Label(self.pista, font=("comic sans",15),bg="white",fg="dark blue")
		self.titulo['text'] = '©Sn.Lionel90'
		self.titulo.config(width=30, height=1)
		self.titulo.grid(row=1,column=0,padx=10)

	#def trackbar(self):

	#panel de control
	def panel_de_controle(self):
		self.abrirFichero = tk.Button(self.controles, bg='green', fg='white', font=10)
		self.abrirFichero ['text'] = 'Abrir Fishero'
		self.abrirFichero['command'] = self.Open_file
		self.abrirFichero .grid(row=0, column=0, padx=10)

		self.previo = tk.Button(self.controles, image = prev)
		self.previo['command'] = self.cancion_ant
		self.previo.grid(row=0,column=1)

		self.pausa = tk.Button(self.controles, image = pause)
		self.pausa['command'] = self.cancion_pausa
		self.pausa.grid(row=0,column=2)

		self.sijiente = tk.Button(self.controles, image = next_)
		self.sijiente['command'] = self.cancion_sig
		self.sijiente.grid(row=0,column=3)

		self.stop_btn = tk.Button(self.controles, image = btn_stop)
		self.stop_btn['command']= self.detener
		self.stop_btn.grid(row=0,column=4)

		self.volumen = tk.DoubleVar(self)
		self.controlcillo = tk.Scale(self.controles, from_=20, to = 0, orient = tk.VERTICAL)
		self.controlcillo['variable'] = self.volumen
		self.controlcillo.set(8)
		mixer.music.set_volume(0.8)
		self.controlcillo.grid(row=0, column=5, pady=5)
		self.controlcillo['command'] = self.cambio_volumen

#Lista de repoduccion
	def panel_lista(self):
		self.deslisante = tk.Scrollbar(self.listaPista, orient=tk.VERTICAL)
		self.deslisante.grid(row=0,column=1, rowspan=5, sticky='ns')

		self.listilla = tk.Listbox(self.listaPista, selectmode=tk.SINGLE,yscrollcommand=self.deslisante.set, selectbackground='sky blue')
		self.enumerate_songs()
		self.listilla.config(height=22)
		self.listilla.bind('<Double-1>', self.play) 

		self.deslisante.config(command=self.listilla.yview)
		self.listilla.grid(row=0, column=0, rowspan=5)

#------Apertura de archivo y guarado en la playlist
	def Open_file(self):
		print('©Sn.Lionel90')
		self.milista2 = []
		carpeta = filedialog.askdirectory()
		for root_, dirs, files in os.walk(carpeta):
			for file in files:
				if os.path.splitext(file)[1] == '.mp3':
					path = (root_ + '/' + file).replace('\\','/')
					self.milista2.append(path)
		with open('canciones.mkm', 'wb') as fibi:
			pickle.dump(self.milista2, fibi)
		self.lista_repro = self.milista2
		self.listaPista['text'] = f'Total pistas: -{str(len(self.lista_repro))}'
		self.listilla.delete(0,tk.END)
		self.enumerate_songs()

	def enumerate_songs(self):
			for index, song in enumerate(self.lista_repro):
				self.listilla.insert(index, os.path.basename(song))

	#-----------Panel de control de reproduccion--------
	def cambio_volumen(self, event=None):
		self.v = self.volumen.get()
		mixer.music.set_volume(self.v / 10)

	def detener(self,event=None):
		if event is not None:
			self.stop=True
			mixer.music.stop()

	def play(self, event=None):
		if event is not None:
			self.current = self.listilla.curselection()[0]
			for i in range(len(self.lista_repro)):
				self.listilla.itemconfigure(i, bg="navajo white")
		mixer.music.load(self.lista_repro[self.current])
		self.titulo['anchor'] = 'w'
		self.titulo['text'] = os.path.basename(self.lista_repro[self.current])

		self.pausa['image'] = play
		self.paused=False
		self.played=True
		self.listilla.activate(self.current)
		self.listilla.itemconfigure(self.current, bg='sky blue')

		mixer.music.play()

	def cancion_pausa(self):
		if not self.paused:
			self.paused = True
			mixer.music.pause()
			self.pausa['image'] = pause
		
		else:
			if self.played==False:
				self.play()
			self.paused=False
			mixer.music.unpause()
			self.pausa['image'] = play

	def cancion_ant(self):
		if self.current > 0:
			self.current -= 1
		else:
			self.current = 0
		self.listilla.itemconfigure(self.current + 1, bg='white')
		self.play()

	def cancion_sig(self):
		if self.current < len(self.lista_repro) - 1:
			self.current += 1
		else:
			self.current = 0
		self.listilla.itemconfigure(self.current - 1, bg='white')
		self.play()

	def salir(self):
		exit(0)

app = MPlayer(master=window)
app.mainloop()
