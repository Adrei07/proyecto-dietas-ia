import os
import customtkinter as ctk
from sistema import (
    SistemaNutricional,
    PerfilUsuario,
    RegistrarProgreso,
    APIClienteDietas
)

# Configuracion

USAR_API = False  # Activa o desactiva uso de API
API_KEY = os.getenv("OPENAI_API_KEY")  # Obtiene la API key

ctk.set_appearance_mode("light")  # Tema claro
ctk.set_default_color_theme("green")  # Color verde

# Inicializa el sistema
if USAR_API:
    api = APIClienteDietas(api_key=API_KEY)
    sistema = SistemaNutricional(api_client=api)
else:
    sistema = SistemaNutricional()


# App

app = ctk.CTk()  # Crea ventana principal
app.geometry("850x700")
app.title("Sistema Nutricional")

# Funciones 

def limpiar_pantalla():
    # Borra todos los elementos de la ventana
    for widget in app.winfo_children():
        widget.destroy()


def lista_desde_texto(texto):
    # Convierte texto separado por comas en lista
    if texto.strip() == "":
        return []
    return [item.strip() for item in texto.split(",") if item.strip()]


def mostrar_mensaje(frame, texto):
    # Muestra un mensaje en pantalla
    label = ctk.CTkLabel(frame, text=texto, wraplength=650)
    label.pack(pady=10)
    return label


def texto_dieta(dieta):
    # Convierte la dieta en texto
    texto = ""
    texto += f"Nombre: {dieta.nombre_dieta}\n"
    texto += f"Calorías: {dieta.calorias} kcal\n"
    texto += f"Proteínas: {dieta.proteinas} g\n"
    texto += f"Carbohidratos: {dieta.carbohidratos} g\n"
    texto += f"Grasas: {dieta.grasas} g\n"
    texto += f"Descripción: {dieta.descripcion}\n\n"

    for comida in dieta.comidas:
        texto += f"{comida.tipo}:\n"
        for alimento in comida.alimentos:
            texto += f"- {alimento.nombre}: {alimento.cantidad}\n"
        texto += "\n"

    return texto


def crear_frame(titulo):
    # Crea un contenedor central
    limpiar_pantalla()

    frame = ctk.CTkFrame(app, width=700, height=600)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    titulo_label = ctk.CTkLabel(
        frame,
        text=titulo,
        font=("Arial", 26, "bold"),text_color="green")
    titulo_label.pack(pady=(25, 20))

    return frame


# Registro

def pantalla_registro():
    # Pantalla para ingresar datos del usuario
    frame = crear_frame("Sistema Nutricional")

    nombre_entry = ctk.CTkEntry(frame, placeholder_text="Nombre", width=320)
    nombre_entry.pack(pady=6)

    edad_entry = ctk.CTkEntry(frame, placeholder_text="Edad", width=320)
    edad_entry.pack(pady=6)

    sexo_menu = ctk.CTkOptionMenu(
        frame,
        values=["Masculino", "Femenino", "Otro"],
        width=320
    )
    sexo_menu.set("Selecciona sexo")
    sexo_menu.pack(pady=6)

    peso_entry = ctk.CTkEntry(frame, placeholder_text="Peso (kg)", width=320)
    peso_entry.pack(pady=6)

    altura_entry = ctk.CTkEntry(frame, placeholder_text="Altura (m)", width=320)
    altura_entry.pack(pady=6)

    actividad_menu = ctk.CTkOptionMenu(
        frame,
        values=["1 - Baja", "2 - Media", "3 - Alta"],
        width=320
    )
    actividad_menu.set("Selecciona nivel de actividad")
    actividad_menu.pack(pady=6)

    objetivo_menu = ctk.CTkOptionMenu(
        frame,
        values=["Ganar masa muscular", "Bajar peso", "Mantener peso"],
        width=320
    )
    objetivo_menu.set("Selecciona objetivo")
    objetivo_menu.pack(pady=6)

    alergias_entry = ctk.CTkEntry(
        frame,
        placeholder_text="Alergias separadas por coma",
        width=320
    )
    alergias_entry.pack(pady=6)

    no_deseados_entry = ctk.CTkEntry(
        frame,
        placeholder_text="Alimentos no deseados separados por coma",
        width=320
    )
    no_deseados_entry.pack(pady=6)

    resultado_label = ctk.CTkLabel(frame, text="", wraplength=500)
    resultado_label.pack(pady=10)

    def confirmar_usuario():
        # Valida y crea el usuario
        try:
            nombre = nombre_entry.get().strip()
            edad = int(edad_entry.get())
            sexo = sexo_menu.get()
            peso = float(peso_entry.get())
            altura = float(altura_entry.get())
            actividad_texto = actividad_menu.get()
            objetivo = objetivo_menu.get()
            alergias = lista_desde_texto(alergias_entry.get())
            no_deseados = lista_desde_texto(no_deseados_entry.get())

            if sexo == "Selecciona sexo":
                raise ValueError("Selecciona un sexo")

            if actividad_texto == "Selecciona nivel de actividad":
                raise ValueError("Selecciona un nivel de actividad")

            if objetivo == "Selecciona objetivo":
                raise ValueError("Selecciona un objetivo")

            nivel_actividad = int(actividad_texto[0])

            usuario = PerfilUsuario(
                nombre,
                edad,
                sexo,
                peso,
                altura,
                nivel_actividad,
                objetivo,
                alergias,
                no_deseados
            )

            sistema.asignar_usuario(usuario)
            sistema.generar_dieta_inicial()

            pantalla_dieta_inicial()

        except Exception as error:
            resultado_label.configure(text=f"Error: {error}")

    boton = ctk.CTkButton(
        frame,
        text="Confirmar información",
        command=confirmar_usuario,
        width=320
    )
    boton.pack(pady=15)
