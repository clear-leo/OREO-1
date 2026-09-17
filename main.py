import ttkbootstrap as ttk
import tkinter as tk
from PIL import Image, ImageTk

root = ttk.App(title="App proyectadisima", theme="bootstrap-dark")
root.attributes("-fullscreen", True)
root.configure(background="#021D29")


class Information(ttk.Frame):
    
    def __init__(self, master):
        #CHANGEME
        self.WIDTH = 1850
        self.HEIGHT = 1080 
        self.pais = ttk.StringVar()
        self.info_pais = ttk.StringVar()
        self.imagen_pais = "stupid" + ".png"
        self.info_pais.set("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.")
        self.pais.set("Pais placeholder")
        # --
        self.master = master

        super().__init__(master, padding=16)
        self.pack(fill='both', expand=True)

        self.__build_info()

    def __build_info(self):
        frame = ttk.LabelFrame(self, text="País seleccionado", padding=12)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, textvariable=self.pais, font=("Arial", 50, "bold"), anchor="center").grid(row=0, column=0, sticky='nsew', pady=20)
        ttk.Label(frame, textvariable=self.info_pais, font=("Arial", 24), anchor="w", wraplength=self.WIDTH).grid(row=1, column=0, sticky='nsew', pady=20)

        imagen = Image.open(self.imagen_pais)
        imagen_tk = ImageTk.PhotoImage(imagen)

        label_imagen = ttk.Label(frame, image=imagen_tk, anchor="center")
        label_imagen.image = imagen_tk  # type: ignore[attr-defined]
        label_imagen.grid(row=3, column=0, sticky='nsew', pady=20)

    def __CHANGEME(self):
        print("hi")
        self.master.after(100, self.__CHANGEME)

    def run(self):
        self.master.after(100, self.__CHANGEME)
        self.master.mainloop()
        




Information(root).run()