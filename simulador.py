import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np

from colonia import Colonia
from bacteria import Bacteria

class SimuladorWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Simulador Bacteriano")
        self.set_default_size(750, 800)

        self.colonia = None
        self.pasos_realizados = 0
        self.pasos_maximos = 0

        self.layout = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)
        self.set_child(self.layout)

        # Entrada para número de pasos
        entrada_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        self.entrada_pasos = Gtk.Entry()
        self.entrada_pasos.set_placeholder_text("Cantidad de pasos")
        self.boton_iniciar = Gtk.Button(label="Iniciar Simulación")
        self.boton_iniciar.connect("clicked", self.on_iniciar_simulacion)
        entrada_box.append(self.entrada_pasos)
        entrada_box.append(self.boton_iniciar)

        self.layout.append(entrada_box)

        # Canvas de matplotlib
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvas(self.figure)
        self.layout.append(self.canvas)
        self.canvas.set_visible(False)

        # Botón siguiente paso
        self.boton_siguiente = Gtk.Button(label="Siguiente Paso")
        self.boton_siguiente.set_sensitive(False)
        self.boton_siguiente.connect("clicked", self.on_siguiente_paso)
        self.layout.append(self.boton_siguiente)

    def on_iniciar_simulacion(self, button):
        try:
            self.pasos_maximos = int(self.entrada_pasos.get_text())
            if self.pasos_maximos <= 0:
                raise ValueError
        except ValueError:
            self.entrada_pasos.set_text("")
            self.entrada_pasos.set_placeholder_text("Ingresa un número válido (>0)")
            return

        self.pasos_realizados = 0
        self.colonia = Colonia(filas=10, columnas=10)
        for fila, col in [(1, 1), (2, 2), (3, 3)]:
            b = Bacteria()
            self.colonia.agregar_bacteria(b, fila, col)

        self.boton_siguiente.set_sensitive(True)
        self.canvas.set_visible(True)
        self.actualizar_grilla()

    def on_siguiente_paso(self, button):
        if self.pasos_realizados < self.pasos_maximos:
            self.colonia.paso()
            self.pasos_realizados += 1
            self.actualizar_grilla()
        else:
            self.boton_siguiente.set_label("Simulación terminada")
            self.boton_siguiente.set_sensitive(False)

    def actualizar_grilla(self):
        self.ax.clear()  # ← borra todo lo anterior

        grilla = np.array(self.colonia.get_ambiente().get_grilla())
        colores = ["#e41a1c", "#4daf4a", "#ffed6f", "#ff7f00", "#bdbdbd"]  # 0-4
        cmap = ListedColormap(colores)

        self.ax.matshow(grilla, cmap=cmap)

        leyenda = [
            Patch(facecolor=colores[0], label="Vacío (0)"),
            Patch(facecolor=colores[1], label="Activa (1)"),
            Patch(facecolor=colores[2], label="Muerta (2)"),
            Patch(facecolor=colores[3], label="Resistente (3)"),
            Patch(facecolor=colores[4], label="Biofilm (4)"),
        ]
        self.ax.legend(handles=leyenda, loc='upper right', bbox_to_anchor=(1.45, 1))

        for i in range(grilla.shape[0]):
            for j in range(grilla.shape[1]):
                val = grilla[i, j]
                if val > 0:
                    self.ax.text(j, i, int(val), va='center', ha='center', color='white')

        self.ax.set_xticks(np.arange(grilla.shape[1]))
        self.ax.set_yticks(np.arange(grilla.shape[0]))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.grid(color='gray', linestyle='-', linewidth=0.5)

        # 🆕 Título con paso actualizado
        self.ax.set_title(f"Paso {self.pasos_realizados} / {self.pasos_maximos}")

        self.figure.tight_layout()
        self.canvas.queue_draw()  # ← fuerza actualización visual

    
    def do_shutdown(self):
        print("Shutdown")
        Gtk.Application.do_shutdown(self)


class SimuladorApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.bioinfo.simulador-grilla")

    def do_activate(self):
        win = SimuladorWindow(self)
        win.present()

if __name__ == "__main__":
    app = SimuladorApp()
    app.run()
