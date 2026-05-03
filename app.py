import customtkinter as ctk
from sistema import (
    SistemaNutricional,
    PerfilUsuario,
    RegistrarProgreso,
    APIClienteDietas
)

#Configuracion

USAR_API = False

API_KEY = "API KEY"
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

if USAR_API:
    api = APIClienteDietas(api_key=API_KEY)
    sistema = SistemaNutricional(api_client=api)
else:
    sistema = SistemaNutricional()


#App

app = ctk.CTk()
app.geometry("850x700")
app.title("Sistema Nutricional")

#Funciones 

def limpiar_pantalla():
    for widget in app.winfo_children():
        widget.destroy()


def lista_desde_texto(texto):
    if texto.strip() == "":
        return []
    return [item.strip() for item in texto.split(",") if item.strip()]


def mostrar_mensaje(frame, texto):
    label = ctk.CTkLabel(frame, text=texto, wraplength=650)
    label.pack(pady=10)
    return label


def texto_dieta(dieta):
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
    limpiar_pantalla()

    frame = ctk.CTkFrame(app, width=700, height=600)
    frame.place(relx=0.5, rely=0.5, anchor="center")

    titulo_label = ctk.CTkLabel(
        frame,
        text=titulo,
        font=("Arial", 26, "bold"),text_color="green")
    titulo_label.pack(pady=(25, 20))

    return frame


#Registro n

def pantalla_registro():
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


# =========================
# PANTALLA 2: DIETA INICIAL
# =========================

def pantalla_dieta_inicial():
    frame = crear_frame("Dieta Generada")

    textbox = ctk.CTkTextbox(frame, width=650, height=390)
    textbox.pack(pady=10)

    textbox.insert("1.0", texto_dieta(sistema.dieta_actual))
    textbox.configure(state="disabled")

    boton_progreso = ctk.CTkButton(
        frame,
        text="Registrar progreso",
        command=pantalla_registrar_progreso,
        width=300
    )
    boton_progreso.pack(pady=15)


# =========================
# PANTALLA 3: REGISTRAR PROGRESO
# =========================

def pantalla_registrar_progreso():
    frame = crear_frame("Registrar Progreso")

    fecha_entry = ctk.CTkEntry(frame, placeholder_text="Fecha (YYYY-MM-DD)", width=320)
    fecha_entry.pack(pady=6)

    peso_entry = ctk.CTkEntry(frame, placeholder_text="Peso actual (kg)", width=320)
    peso_entry.pack(pady=6)

    actividad_menu = ctk.CTkOptionMenu(
        frame,
        values=["1 - Baja", "2 - Media", "3 - Alta"],
        width=320
    )
    actividad_menu.set("Actividad de la semana")
    actividad_menu.pack(pady=6)

    cumplimiento_label = ctk.CTkLabel(frame, text="Cumplimiento: 80%")
    cumplimiento_label.pack(pady=(12, 0))

    cumplimiento_slider = ctk.CTkSlider(
        frame,
        from_=0,
        to=100,
        width=320
    )
    cumplimiento_slider.set(80)
    cumplimiento_slider.pack(pady=6)

    def actualizar_slider(value):
        cumplimiento_label.configure(text=f"Cumplimiento: {int(value)}%")

    cumplimiento_slider.configure(command=actualizar_slider)

    sintomas_label = ctk.CTkLabel(frame, text="Síntomas")
    sintomas_label.pack(pady=(15, 5))

    sintomas_vars = {
        "Mareo": ctk.BooleanVar(),
        "Dolor de cabeza": ctk.BooleanVar(),
        "Fatiga": ctk.BooleanVar(),
        "Náusea": ctk.BooleanVar(),
        "Dolor estomacal": ctk.BooleanVar()
    }

    sintomas_frame = ctk.CTkFrame(frame)
    sintomas_frame.pack(pady=5)

    for sintoma, var in sintomas_vars.items():
        checkbox = ctk.CTkCheckBox(
            sintomas_frame,
            text=sintoma,
            variable=var
        )
        checkbox.pack(anchor="w", padx=15, pady=3)

    observaciones_entry = ctk.CTkEntry(
        frame,
        placeholder_text="Observaciones",
        width=320
    )
    observaciones_entry.pack(pady=10)

    resultado_label = ctk.CTkLabel(frame, text="", wraplength=500)
    resultado_label.pack(pady=8)

    def guardar_progreso():
        try:
            fecha = fecha_entry.get().strip()
            peso_actual = float(peso_entry.get())
            actividad_texto = actividad_menu.get()

            if actividad_texto == "Actividad de la semana":
                raise ValueError("Selecciona actividad semanal")

            actividad = int(actividad_texto[0])
            cumplimiento = int(cumplimiento_slider.get())

            sintomas = [
                sintoma
                for sintoma, var in sintomas_vars.items()
                if var.get()
            ]

            observaciones = observaciones_entry.get().strip()

            registro = RegistrarProgreso(
                fecha,
                peso_actual,
                cumplimiento,
                actividad,
                sintomas,
                observaciones
            )

            sistema.registrar_progreso(registro)

            pantalla_resumen()

        except Exception as error:
            resultado_label.configure(text=f"Error: {error}")

    boton = ctk.CTkButton(
        frame,
        text="Guardar progreso",
        command=guardar_progreso,
        width=320
    )
    boton.pack(pady=15)


#Resumen 

def pantalla_resumen():
    frame = crear_frame("Resumen del Progreso")

    texto = ""

    texto += f"Usuario: {sistema.usuario.nombre}\n"
    texto += f"Objetivo: {sistema.usuario.objetivo}\n"
    texto += f"IMC: {round(sistema.usuario.imc, 2)}\n\n"

    ultimo = sistema.historial.devolver_ultimo()

    if ultimo:
        texto += "Último registro:\n"
        texto += f"Fecha: {ultimo.fecha}\n"
        texto += f"Peso actual: {ultimo.peso_actual} kg\n"
        texto += f"Cumplimiento: {ultimo.cumplimiento}%\n"
        texto += f"Actividad semanal: {ultimo.actividad_semana}\n"
        texto += f"Síntomas: {', '.join(ultimo.sintomas) if ultimo.sintomas else 'Ninguno'}\n"
        texto += f"Observaciones: {ultimo.observaciones}\n\n"

    texto += f"Análisis: {sistema.analizar_usuario()}\n"
    texto += f"Acción recomendada: {sistema.obtener_accion_recomendada()}\n"

    textbox = ctk.CTkTextbox(frame, width=650, height=350)
    textbox.pack(pady=10)
    textbox.insert("1.0", texto)
    textbox.configure(state="disabled")

    boton_evaluar = ctk.CTkButton(
        frame,
        text="Evaluar y actualizar dieta",
        command=pantalla_evaluar_dieta,
        width=300
    )
    boton_evaluar.pack(pady=10)

    boton_otro = ctk.CTkButton(
        frame,
        text="Registrar otro progreso",
        command=pantalla_registrar_progreso,
        width=300
    )
    boton_otro.pack(pady=5)
    
    boton_historial = ctk.CTkButton(
    frame,
    text="Ver historial completo",
    command=pantalla_historial,
    width=300
    )
    boton_historial.pack(pady=5)

#Evaluar y actualizar 

def pantalla_evaluar_dieta():
    frame = crear_frame("Evaluación de Dieta")

    resultado = sistema.evaluar_y_actualizar_dieta()

    texto = resultado + "\n\n"
    texto += "Dieta actual:\n\n"
    texto += texto_dieta(sistema.dieta_actual)

    textbox = ctk.CTkTextbox(frame, width=650, height=420)
    textbox.pack(pady=10)
    textbox.insert("1.0", texto)
    textbox.configure(state="disabled")

    boton_progreso = ctk.CTkButton(
        frame,
        text="Registrar nuevo progreso",
        command=pantalla_registrar_progreso,
        width=300
    )
    boton_progreso.pack(pady=10)

    boton_inicio = ctk.CTkButton(
        frame,
        text="Volver al inicio",
        command=pantalla_registro,
        width=300
    )
    boton_inicio.pack(pady=5)

def pantalla_historial():
    frame = crear_frame("Historial de Progreso")

    texto = ""

    if len(sistema.historial.registros) > 0:
        for i, registro in enumerate(sistema.historial.registros, 1):
            texto += f"Registro #{i}\n"
            texto += f"Fecha: {registro.fecha}\n"
            texto += f"Peso: {registro.peso_actual} kg\n"
            texto += f"Cumplimiento: {registro.cumplimiento}%\n"
            texto += f"Actividad: {registro.actividad_semana}\n"
            texto += f"Síntomas: {', '.join(registro.sintomas) if registro.sintomas else 'Ninguno'}\n"
            texto += f"Observaciones: {registro.observaciones}\n"
            texto += "-" * 30 + "\n\n"
    else:
        texto = "No hay registros aún"

    textbox = ctk.CTkTextbox(frame, width=650, height=450)
    textbox.pack(pady=10)

    textbox.insert("1.0", texto)
    textbox.configure(state="disabled")

    boton_volver = ctk.CTkButton(
        frame,
        text="Volver",
        command=pantalla_resumen,
        width=300
    )
    boton_volver.pack(pady=10)

#Inicio 

pantalla_registro()
app.mainloop()
