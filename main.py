import ttkbootstrap as ttk
import json
from PIL import Image, ImageTk
from queue import Empty

from Serial import Serial
from Voice import Voice

root = ttk.App(title="App proyectadisima", theme="bootstrap-dark")
root.attributes("-fullscreen", True)
root.configure(background="#021D29")


class Information(ttk.Frame):
    
    def __init__(self, master):
        self.WIDTH = 1920
        self.HEIGHT = 1080 
        self.voice = Voice(16000)
        self.voice.start()
        self.serial = Serial(115200)
        
        with open("data.json", "r", encoding="utf-8") as file:
            self.datos = json.load(file)

        #CHANGEME
        # Aqui esta toda la información que vamos a cambiar para añadir el Serial.
        self.pais = ttk.StringVar()
        self.info_top = ttk.StringVar()
        self.info_bottom = ttk.StringVar()
        self.info_top.set("Empieza por escogiendo un continente.")
        self.info_bottom.set("")
        self.pais.set("Bienvenido!")
        # --

        self.master = master

        super().__init__(master, padding=16)
        self.pack(fill='both', expand=True)

        self.__build_info()

    def __build_info(self):
        self.frame = ttk.LabelFrame(self, text="País seleccionado", padding=12)
        frame = self.frame
        frame.columnconfigure(2, weight=1)
        frame.rowconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        frame.pack(fill='both', expand=True)

        ttk.Label(frame, textvariable=self.pais, font=("Arial", 100, "bold"), anchor="center").grid(row=0, column=0, sticky='ew', pady=0)
        ttk.Label(frame, textvariable=self.info_top, font=("Arial", 30), anchor="center", wraplength=self.WIDTH/2).grid(row=1, column=0, sticky='ew', pady=10)

        self.label_imagen = ttk.Label(self.frame, anchor="center")
        self.label_imagen.grid(row=1, column=2)

        ttk.Label(frame, textvariable=self.info_bottom, font=("Arial", 30), anchor="center", wraplength=self.WIDTH/2).grid(row=3, column=0, pady=5)


    def __load_image(self, path):
        imagen = Image.open(path)
        imagen_tk = ImageTk.PhotoImage(imagen)

        self.label_imagen.configure(image=imagen_tk)
        self.label_imagen.image = imagen_tk  # type: ignore[attr-defined]


    # Función para probar la idea de una funcion recurrente que revise si hemos recibido un mensaje por serial.
    # O la logica se hace aquí o se hace dentro de otra función. Probablemente otra función quizas hasta -
    # - otro archivo, preferiblemente eso.
    def __update_country(self): 
        try:
            pais = self.voice.read_country()
            if pais and pais in self.datos:
                self.pais.set(self.datos[pais]["nombre"])
                self.info_top.set(self.datos[pais]["info_top"])
                self.info_bottom.set(self.datos[pais]["info_bottom"])
                self.__load_image(self.datos[pais]["imagen"])
                self.serial.writeLine(self.datos[pais].get("angulo"))
        except Empty:
            pass
        self.master.after(200, self.__update_country)
            

    def run(self):
        self.master.after(200, self.__update_country)
        self.master.mainloop()


Information(root).run()