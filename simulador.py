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
from bacteria import Bacteria
import random

class SimuladorWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        super().__init__(application=app)
        self.set_title("Simulador Bacteriano")
        self.set_default_size(750, 800)

        self.colonia = None
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
        file_dialog = Gtk.FileDialog.new()
        file_dialog.set_title("Selecciona un archivo CSV")

        def on_response(dialog_ref, result):
            try:
                file = dialog_ref.open_finish(result)
                if file:
                    path = file.get_path()
                    
                    
                    self.colonia = Colonia(filas=10, columnas=10)
                    try:
                        df = pd.read_csv(path, encoding='utf-8')
                    except UnicodeDecodeError:
                        df = pd.read_csv(path, encoding='latin-1')
                    except Exception as e:
                        self.mostrar_mensaje(f"Error al leer el CSV: {e}")
                        return
                    columnas = [c.strip().lower() for c in df.columns]
                    df.columns = columnas
                    self.colonia.get_bacterias().clear()
                    grilla = self.colonia.get_ambiente().get_grilla()
                    
                    for i, row in df.iterrows():
                        b = Bacteria()
                        b.set_id(str(row.get('id', f"B{i}")))
                        b.set_raza(str(row.get('raza', 'Desconocida')))
                        try:
                            b.set_energia(int(row.get('energía', 50)))
                        except Exception:
                            b.set_energia(50)
                        b.set_estado(str(row.get('estado', 'Viva')).strip().lower() == 'viva')
                        b.set_resistente(str(row.get('resistente', 'No')).strip().lower() == 'si')
                        # Buscar una celda vacía aleatoria
                        vacias = [(x, y) for x in range(len(grilla)) for y in range(len(grilla[0])) if grilla[x][y] == 0]
                        if vacias:
                            x, y = random.choice(vacias)
                            self.colonia.agregar_bacteria(b, x, y)
                    self.pasos_realizados = 0
                    self.pasos_maximos = 0
                    self.boton_siguiente.set_sensitive(True)
                    self.canvas.set_visible(True)
                    self.actualizar_grilla()
            except Exception as e:
                self.mostrar_mensaje(f"Error al abrir archivo: {e}")

        file_dialog.open(self.get_root(), None, on_response)

    def importar_csv(self, filename):
        self.colonia = Colonia(filas=10, columnas=10)
        try:
            df = pd.read_csv(filename, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(filename, encoding='latin-1')
        except Exception as e:
            self.mostrar_mensaje(f"Error al leer el CSV: {e}")
            return
        columnas = [c.strip().lower() for c in df.columns]
        df.columns = columnas
        grilla = self.colonia.get_ambiente().get_grilla()
        for i, row in df.iterrows():
            b = Bacteria()
            b.set_id(str(row.get('id', f"B{i}")))
            b.set_raza(str(row.get('raza', 'Desconocida')))
            try:
                b.set_energia(int(row.get('energía', 50)))
            except Exception:
                b.set_energia(50)
            b.set_estado(str(row.get('estado', 'Viva')).strip().lower() == 'viva')
            b.set_resistente(str(row.get('resistente', 'No')).strip().lower() == 'si')
            # Buscar una celda vacía aleatoria
            vacias = [(x, y) for x in range(len(grilla)) for y in range(len(grilla[0])) if grilla[x][y] == 0]
            if vacias:
                x, y = random.choice(vacias)
                self.colonia.agregar_bacteria(b, x, y)
        self.pasos_realizados = 0
        self.pasos_maximos = 0
        self.boton_siguiente.set_sensitive(True)
        self.canvas.set_visible(True)
        self.actualizar_grilla()

    def mostrar_grafico_en_ventana(self, fig, titulo="Gráfico"):
        win = Gtk.Window(title=titulo)
        canvas = FigureCanvas(fig)
        win.set_child(canvas)
        win.set_default_size(600, 400)
        win.present()

    def on_graficar_resistencia(self, button):
        try:
            df = pd.read_csv("colonia_estado.csv", encoding="utf-8")
        except Exception:
            self.mostrar_mensaje("No se pudo leer el archivo colonia_estado.csv")
            return
        pasos = list(range(1, len(self.historial_resistentes)+1))
        fig, ax = plt.subplots()
        ax.plot(pasos, self.historial_resistentes, label="Resistentes (en simulación)")
        ax.set_xlabel("Paso")
        ax.set_ylabel("Cantidad de bacterias resistentes")
        ax.set_title("Evolución de bacterias resistentes")
        ax.legend()
        self.mostrar_grafico_en_ventana(fig, "Resistencia")

    def on_graficar_crecimiento(self, button):
        try:
            df = pd.read_csv("colonia_estado.csv", encoding="utf-8")
        except Exception:
            self.mostrar_mensaje("No se pudo leer el archivo colonia_estado.csv")
            return
        pasos = list(range(1, len(self.historial_vivas)+1))
        fig, ax = plt.subplots()
        ax.plot(pasos, self.historial_vivas, label="Vivas (en simulación)")
        ax.set_xlabel("Paso")
        ax.set_ylabel("Cantidad de bacterias vivas")
        ax.set_title("Crecimiento de la colonia bacteriana")
        ax.legend()
        self.mostrar_grafico_en_ventana(fig, "Crecimiento")

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
        # Colocar 3 bacterias iniciales en posiciones aleatorias y distintas
        grilla = self.colonia.get_ambiente().get_grilla()
        for _ in range(3):
            vacias = [(x, y) for x in range(len(grilla)) for y in range(len(grilla[0])) if grilla[x][y] == 0]
            if not vacias:
                break
            fila, col = random.choice(vacias)
            b = Bacteria()
            self.colonia.agregar_bacteria(b, fila, col)

        self.boton_siguiente.set_sensitive(True)
        self.canvas.set_visible(True)
        self.actualizar_grilla()

    def on_siguiente_paso(self, button):
        if self.pasos_realizados < self.pasos_maximos or self.pasos_maximos == 0:
            self.colonia.paso()
            self.pasos_realizados += 1
            # Guardar historial para graficar
            vivas, resistentes = self.contar_vivas_resistentes()
            self.historial_vivas.append(vivas)
            self.historial_resistentes.append(resistentes)
            # Exportar CSV automáticamente
            try:
                self.colonia.exportar_csv("colonia_estado.csv")
            except Exception as e:
                print(f"Error exportando CSV: {e}")
            self.actualizar_grilla()
        else:
            self.boton_siguiente.set_label("Simulación terminada")
            self.boton_siguiente.set_sensitive(False)

    def contar_vivas_resistentes(self):
        vivas, _, resistentes = self.colonia.reporte_estado()
        return vivas, resistentes

    def actualizar_grilla(self):
        self.ax.clear()  # Sobreescribe lo anterior

        grilla = np.array(self.colonia.get_ambiente().get_grilla())
        # Asegura que los valores estén en el rango 0-4 y sean enteros
        grilla = grilla.astype(int)
        # Colores: 0=Vacío, 1=Activa, 2=Muerta, 3=Resistente, 4=Biofilm
        colores = ["#e41a1c", "#4daf4a", "#ffed6f", "#ff7f00", "#bdbdbd"]  # 0-4
        cmap = ListedColormap(colores)

        # Para evitar que matplotlib asigne el color "incorrecto" a los valores fuera de rango
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
                    # Elige color de texto según fondo para mejor contraste
                    text_color = 'black' if val in [2, 4] else 'white'
                    self.ax.text(j, i, int(val), va='center', ha='center', color=text_color, fontsize=10, fontweight='bold')

        self.ax.set_xticks(np.arange(grilla.shape[1]))
        self.ax.set_yticks(np.arange(grilla.shape[0]))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])
        self.ax.grid(color='gray', linestyle='-', linewidth=0.5)

        self.ax.set_title(f"Paso {self.pasos_realizados} / {self.pasos_maximos}")

        self.figure.tight_layout()
        self.canvas.queue_draw()  #  fuerza actualización visual
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

    def do_window_removed(self, window):
        # Si no quedan ventanas, salir de la app
        if not self.get_windows():
            self.quit()

