import ttkbootstrap as ttk
import tkinter as tk
from PIL import Image, ImageTk
import time

from Serial import Serial

root = ttk.App(title="App proyectadisima", theme="bootstrap-dark")
root.attributes("-fullscreen", True)
root.configure(background="#021D29")


class Information(ttk.Frame):
    
    def __init__(self, master):
        self.WIDTH = 1850
        self.HEIGHT = 1080 
        self.serial = Serial(9600)

        #CHANGEME
        # Aqui esta toda la información que vamos a cambiar para añadir el Serial.
        self.pais = ttk.StringVar()
        self.info_pais = ttk.StringVar()
        self.imagen_pais = "placeholders/stupid.png"
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


        # Es probable que esta lógica la cambie, y es más probable que esta lógica sea obsoleta cuando
        # - añademos el cambio dinámico.
        imagen = Image.open(self.imagen_pais)
        imagen_tk = ImageTk.PhotoImage(imagen)

        label_imagen = ttk.Label(frame, image=imagen_tk, anchor="center")
        label_imagen.image = imagen_tk  # type: ignore[attr-defined]
        label_imagen.grid(row=3, column=0, sticky='nsew', pady=20)

    # Función para probar la idea de una funcion recurrente que revise si hemos recibido un mensaje por serial.
    # O la logica se hace aquí o se hace dentro de otra función. Probablemente otra función quizas hasta -
    # - otro archivo, preferiblemente eso.
    def __update_country(self): 
        try:
            if self.serial.is_ready():
                self.pais.set(self.serial.read_country())
            self.master.after(100, self.__update_country)
        except RuntimeError:
            print("Serial disconnected or closed unexpectedly.")
            #add later
            

    def run(self):
        self.master.after(100, self.__update_country)
        self.master.mainloop()


Information(root).run()