from bacteria import Bacteria
from ambiente import Ambiente

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gio

class MainSimulador(Gtk.Application):
    def __init__(self):
        super().__init__(application_id="org.simulador.ColoniaUI")
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        self.ventana = Gtk.ApplicationWindow(application=app)
        self.ventana.set_title("Simulador de Colonia Bacteriana")
        self.ventana.set_default_size(600, 400)

        # HeaderBar
        header = Gtk.HeaderBar()
        header.set_title_widget(Gtk.Label(label="Simulador Bacteriano"))
        header.set_show_title_buttons(True)

        #Aqui se plantea la lista desplegable de opciones
        menu = Gio.Menu()
        menu.append("Importar CSV", "app.importar")
        menu.append("Graficar Resultados", "app.graficar")
        menu_btn = Gtk.MenuButton()
        menu_btn.set_icon_name("open-menu-symbolic")
        menu_btn.set_menu_model(menu)
        header.pack_end(menu_btn)

        self.ventana.set_titlebar(header)

        # Acciones del menú 
        importar_action = Gio.SimpleAction.new("importar", None)
        importar_action.connect("activate", self.on_importar)
        self.add_action(importar_action)

        graficar_action = Gio.SimpleAction.new("graficar", None)
        graficar_action.connect("activate", self.on_graficar)
        self.add_action(graficar_action)

       
        caja_principal = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=10, margin_bottom=10, margin_start=10, margin_end=10)

        self.etiqueta_estado = Gtk.Label(label="Aquí se mostrará la simulación de la colonia.")
        caja_principal.append(self.etiqueta_estado)

        boton_siguiente = Gtk.Button(label="Siguiente Paso")
        boton_siguiente.set_halign(Gtk.Align.END)
        boton_siguiente.set_valign(Gtk.Align.END)
        boton_siguiente.connect("clicked", self.on_siguiente_paso)
        caja_principal.append(boton_siguiente)

        self.ventana.set_child(caja_principal)
        self.ventana.present()

    def on_importar(self, action, param):
        print("[MENU] Importar CSV seleccionado")

    def on_graficar(self, action, param):
        print("[MENU] Graficar resultados seleccionado")
    #Sirve para testear si funciona el Boton XDD
    def on_siguiente_paso(self, button):
        print("[BOTON] Siguiente paso de simulación ejecutado")
        self.etiqueta_estado.set_text("Simulación: siguiente paso ejecutado")

if __name__ == "__main__":
    app = MainSimulador()
    app.run()