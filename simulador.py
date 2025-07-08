import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_gtk4agg import FigureCanvasGTK4Agg as FigureCanvas
from matplotlib.colors import ListedColormap
from matplotlib.patches import Patch
import numpy as np
import pandas as pd
from colonia import Colonia


class SimuladorWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Simulador Bacteriano")
        self.set_default_size(750, 800)

        self.colonia = None  # Aqui se crea la variable vacia de self.colonia, la cual se iniciará como none
        self.pasos_realizados = 0
        self.pasos_maximos = 0

        # HeaderBar
        self.headerbar = Gtk.HeaderBar()
        self.headerbar.set_show_title_buttons(True)
        self.set_titlebar(self.headerbar)

        # Menú desplegable
        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_icon_name("open-menu-symbolic")
        self.headerbar.pack_end(self.menu_button)

        # Crear el menú
        self.menu = Gtk.Popover()
        self.menu_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6, margin_top=6, margin_bottom=6, margin_start=6, margin_end=6)
        self.menu.set_child(self.menu_box)
        self.menu_button.set_popover(self.menu)

        # Opción: Importar CSV
        self.btn_importar_csv = Gtk.Button(label="Importar CSV")
        self.btn_importar_csv.connect("clicked", self.on_importar_csv)
        self.menu_box.append(self.btn_importar_csv)

        # Opción: Graficar Resistencia
        self.btn_graficar_resistencia = Gtk.Button(label="Graficar Resistencia")
        self.btn_graficar_resistencia.connect("clicked", self.on_graficar_resistencia)
        self.menu_box.append(self.btn_graficar_resistencia)

        # Opción: Graficar Crecimiento
        self.btn_graficar_crecimiento = Gtk.Button(label="Graficar Crecimiento")
        self.btn_graficar_crecimiento.connect("clicked", self.on_graficar_crecimiento)
        self.menu_box.append(self.btn_graficar_crecimiento)
        # Layout principal
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
        # Historial
        self.historial_vivas = []
        self.historial_resistentes = []
    def on_importar_csv(self, button):
        # Importa bacterias desde un archivo CSV
        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_title("Selecciona un archivo CSV")

        def on_response(dialog_ref, result):
            try:
                file = dialog_ref.open_finish(result)
                if not file:
                    return
                path = file.get_path()
                self.colonia = Colonia(filas=10, columnas=10)
                try:
                    df = pd.read_csv(path, encoding='utf-8')
                except:
                    df = pd.read_csv(path, encoding='latin-1')
                df.columns = [c.strip().lower() for c in df.columns]
                self.colonia.get_bacterias().clear()
                for i, row in df.iterrows():
                    # Aquí se crea y configura cada bacteria en la colonia (Colonia.agregar_bacteria y métodos de Bacteria)
                    datos = {
                        'id': str(row.get('id', f"B{i}")),
                        'raza': str(row.get('raza', 'Espiroqueta')),
                        'energia': int(row.get('energía', 50)) if str(row.get('energía', 50)).isdigit() else 50,
                        'estado': str(row.get('estado', 'Viva')).strip().lower() == 'viva',
                        'resistente': str(row.get('resistente', 'No')).strip().lower() == 'si'
                    }
                    if self.colonia.agregar_bacteria(tipo=datos['raza']):
                        b = self.colonia.get_bacterias()[-1]  # 
                        b.set_id(datos['id'])
                        b.set_raza(datos['raza'])
                        b.set_energia(datos['energia'])
                        b.set_estado(datos['estado'])
                        b.set_resistente(datos['resistente'])
                self.pasos_realizados = 0
                self.pasos_maximos = 0
                self.boton_siguiente.set_sensitive(True)
                self.canvas.set_visible(True)
                self.actualizar_grilla()
            except Exception as e:
                print(f"Error al abrir archivo: {e}")

        file_dialog.open(self.get_root(), None, on_response)

    def mostrar_grafico_en_ventana(self, fig, titulo="Gráfico"):
        win = Gtk.Window(title=titulo)
        canvas = FigureCanvas(fig)
        win.set_child(canvas)
        win.set_default_size(600, 400)
        win.present()

    def on_graficar_resistencia(self, button):
        pasos = list(range(1, len(self.historial_resistentes)+1))
        fig, ax = plt.subplots()
        ax.plot(pasos, self.historial_resistentes, label="Resistentes (en simulación)")
        ax.set_xlabel("Paso")
        ax.set_ylabel("Cantidad de bacterias resistentes")
        ax.set_title("Evolución de bacterias resistentes")
        ax.legend()
        self.mostrar_grafico_en_ventana(fig, "Resistencia")

    def on_graficar_crecimiento(self, button):
        pasos = list(range(1, len(self.historial_vivas)+1))
        fig, ax = plt.subplots()
        ax.plot(pasos, self.historial_vivas, label="Vivas (en simulación)")
        ax.set_xlabel("Paso")
        ax.set_ylabel("Cantidad de bacterias vivas")
        ax.set_title("Crecimiento de la colonia bacteriana")
        ax.legend()
        self.mostrar_grafico_en_ventana(fig, "Crecimiento")

    def on_iniciar_simulacion(self, _):
        # Inicia la simulación con 3 bacterias
        try:
            self.pasos_maximos = int(self.entrada_pasos.get_text())
        except:
            self.entrada_pasos.set_text("")
            self.entrada_pasos.set_placeholder_text("Ingresa un número válido (>0)")
            return
        if self.pasos_maximos <= 0:
            self.entrada_pasos.set_text("")
            self.entrada_pasos.set_placeholder_text("Ingresa un número válido (>0)")
            return
        self.pasos_realizados = 0
        self.colonia = Colonia(filas=10, columnas=10)  # Se crea una nueva colonia (Colonia)
        for _ in range(3):
            self.colonia.agregar_bacteria()  # Se agregan bacterias a la colonia (Colonia.agregar_bacteria)
        self.boton_siguiente.set_sensitive(True)
        self.canvas.set_visible(True)
        self.actualizar_grilla()

    def on_siguiente_paso(self, _):
        # Avanza un paso en la simulación
        if self.pasos_realizados < self.pasos_maximos or self.pasos_maximos == 0:
            self.colonia.paso()  # Avanza la simulación (Colonia.paso)
            self.pasos_realizados += 1
            vivas, resistentes = self.contar_vivas_resistentes()
            self.historial_vivas.append(vivas)
            self.historial_resistentes.append(resistentes)
            try:
                self.colonia.exportar_csv("colonia_estado.csv")  # Exporta el estado de la colonia (Colonia.exportar_csv)
            except:
                pass
            self.actualizar_grilla()
        else:
            self.boton_siguiente.set_label("Simulación terminada")
            self.boton_siguiente.set_sensitive(False)

    def contar_vivas_resistentes(self):
        vivas, _, resistentes = self.colonia.reporte_estado()  #Obtiene el estado de la colonia (Colonia.reporte_estado)
        return vivas, resistentes

    def actualizar_grilla(self):
        self.ax.clear()  # Sobreescribe lo anterior

        grilla = np.array(self.colonia.get_ambiente().get_grilla())  # Obtiene la grilla del ambiente (Colonia.get_ambiente, Ambiente.get_grilla)
        # Asegura que los valores estén en el rango 0-4 y sean enteros
        grilla = grilla.astype(int)
        # Colores: 0=Vacío, 1=Activa, 2=Muerta, 3=Resistente
        colores = ["#e41a1c", "#4daf4a", "#ffed6f", "#ff7f00", "#bdbdbd"]  # 0-4
        cmap = ListedColormap(colores)

        self.ax.imshow(grilla, cmap=cmap, vmin=0, vmax=4)

        colores = [
            Patch(facecolor=colores[0], label="Vacío (0)"),
            Patch(facecolor=colores[1], label="Activa (1)"),
            Patch(facecolor=colores[2], label="Muerta (2)"),
            Patch(facecolor=colores[3], label="Resistente (3)")
        ]
        self.ax.legend(handles=colores, loc='upper right', bbox_to_anchor=(1.45, 1))

        for i in range(grilla.shape[0]):
            for j in range(grilla.shape[1]):
                val = grilla[i, j]
                if val > 0:
                    text_color = 'black' if val in [2, 4] else 'white'
                    self.ax.text(j, i, int(val), va='center', ha='center', color=text_color, fontsize=10, fontweight='bold')

        self.ax.set_xticks(np.arange(grilla.shape[1]))
        self.ax.set_yticks(np.arange(grilla.shape[0]))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.grid(color='gray', linestyle='-', linewidth=0.5)

        self.ax.set_title(f"Paso {self.pasos_realizados} / {self.pasos_maximos}")

        self.figure.tight_layout()
        self.canvas.queue_draw()  #  Fuerza actualización visual
    def do_close_request(self):
        app = self.get_application()
        if app:
            app.quit()
        return False



class SimuladorApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.simulador-grilla")

    def do_activate(self):
        win = SimuladorWindow(self)
        win.present()


