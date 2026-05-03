import re
import json
from openai import OpenAI
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# Clase que guarda y valida los datos principales del usuario
class PerfilUsuario: 
    def __init__(self, nombre, edad, sexo, peso, altura, nivel_actividad, objetivo, alergias, no_deseados):
        if not isinstance(nombre, str):
            raise TypeError("nombre debe ser del tipo str")
        if not isinstance(edad, int):
            raise TypeError("La edad debe de ser numerica")
        if edad < 0 or edad > 130: 
            raise ValueError("La edad debe de estar entre 0 y 130")
        if not isinstance(sexo, str):
            raise TypeError("El sexo debe ser del tipo str")
        if not isinstance(peso, (int, float)):
            raise TypeError("El peso debe ser un número unicamente")
        if peso <= 0:
            raise ValueError("El peso debe ser mayor a 0")
        if not isinstance(altura, (int, float)):
            raise TypeError("La altura debe ser un número")
        if altura <= 0:
            raise ValueError("La altura debe ser mayor a 0")
        if not isinstance(nivel_actividad, int):
            raise TypeError("El nivel de actividad debe ser un entero")
        if nivel_actividad < 1 or nivel_actividad > 3:
            raise ValueError("El nivel de actividad debe estar entre 1 y 3")
        if not isinstance(objetivo, str):
            raise TypeError("El objetivo debe ser texto")
        if not isinstance(alergias, list):
            raise TypeError("Las alergias deben ser una lista") 
        if not isinstance(no_deseados, list):
            raise TypeError("Los alimentos no deseados deben ser una lista")
    
        self.nombre = nombre 
        self.edad = edad 
        self.sexo = sexo 
        self.peso = peso 
        self.altura = altura 
        self.nivel_actividad = nivel_actividad
        self.objetivo = objetivo
        self.alergias = alergias
        self.no_deseados = no_deseados
    
    # Calcula el índice de masa corporal
    @property
    def imc(self): 
        return self.peso / (self.altura ** 2)

    # Interpreta el IMC del usuario
    def interpretar_imc(self): 
        if self.imc < 18.5: 
            return "bajo"
        elif self.imc < 25: 
            return "normal"
        elif self.imc < 30: 
            return "sobrepeso"
        else:
            return "obesidad"
  
    # Muestra los datos del usuario en consola
    def mostrar_perfil(self): 
        print("==== Perfil del Usuario ====\n")
        print(f"Nombre: {self.nombre}")
        print(f"Edad: {self.edad} años")
        print(f"Sexo: {self.sexo}")
        print(f"Peso: {self.peso} kg")
        print(f"Altura: {self.altura} m")
        print(f"Nivel de actividad: {self.nivel_actividad}")
        print(f"Objetivo: {self.objetivo}")
        print(f"Alergias: {', '.join(self.alergias) if self.alergias else 'Ninguna'}")
        print(f"Alimentos no deseados: {', '.join(self.no_deseados) if self.no_deseados else 'Ninguno'}")
        print(f"IMC: {round(self.imc, 3)}")
        print(f"Categoria de IMC: {self.interpretar_imc()}")


# Clase para representar un alimento individual
class Alimento:
    def __init__(self, nombre, cantidad):
        if not isinstance(nombre, str):
            raise TypeError("El nombre del alimento debe ser texto")
        if not isinstance(cantidad, str):
            raise TypeError("La cantidad debe ser texto")

        self.nombre = nombre
        self.cantidad = cantidad


# Clase para agrupar alimentos dentro de una comida
class Comida:
    def __init__(self, tipo, alimentos):
        if not isinstance(tipo, str):
            raise TypeError("El tipo de comida debe ser texto")
        if not isinstance(alimentos, list):
            raise TypeError("Los alimentos deben ser una lista")

        self.tipo = tipo
        self.alimentos = alimentos


# Clase que representa una dieta completa
class RegistrarDieta: 
    def __init__(self, nombre_dieta, calorias, proteinas, carbohidratos, grasas, descripcion, comidas=None):
        if not isinstance(nombre_dieta, str):
            raise TypeError("El nombre de la dieta debe ser texto")
        if not isinstance(calorias, (int, float)):
            raise TypeError("Las calorías deben ser un número")
        if calorias <= 0:
            raise ValueError("Las calorías deben ser mayores a 0")
        if not isinstance(proteinas, (int, float)):
            raise TypeError("Las proteínas deben ser un número")
        if proteinas < 0:
            raise ValueError("Las proteínas no pueden ser negativas")
        if not isinstance(carbohidratos, (int, float)):
            raise TypeError("Los carbohidratos deben ser un número")
        if carbohidratos < 0:
            raise ValueError("Los carbohidratos no pueden ser negativos")
        if not isinstance(grasas, (int, float)):
            raise TypeError("Las grasas deben ser un número")
        if grasas < 0:
            raise ValueError("Las grasas no pueden ser negativas")
        if not isinstance(descripcion, str):
            raise TypeError("La descripción debe ser texto")
        if comidas is not None and not isinstance(comidas, list):
            raise TypeError("Las comidas deben ser una lista")
            
        self.nombre_dieta = nombre_dieta
        self.calorias = calorias
        self.proteinas = proteinas
        self.carbohidratos = carbohidratos
        self.grasas = grasas
        self.descripcion = descripcion
        self.comidas = comidas if comidas is not None else []
        
    # Muestra la dieta en consola
    def mostrar_dieta(self):
        print("\n==== Plan dieta =====\n")
        print(f"Nombre: {self.nombre_dieta}")
        print(f"Calorías: {self.calorias} kcal")
        print(f"Proteínas: {self.proteinas} g")
        print(f"Carbohidratos: {self.carbohidratos} g")
        print(f"Grasas: {self.grasas} g")
        print(f"Descripción: {self.descripcion}")

        if self.comidas:
            print("\n==== Comidas ====")
            for comida in self.comidas:
                print(f"\n{comida.tipo}:")
                for alimento in comida.alimentos:
                    print(f"- {alimento.nombre}: {alimento.cantidad}")
        else:
            print("\nNo hay comidas detalladas registradas.")


# Clase encargada de generar dietas usando API o respaldo local
class GenerarDieta:
    def __init__(self, api_client=None):
        self.api_client = api_client

    # Intenta generar una dieta con API; si falla, usa dieta local
    def generar_dieta(self, perfil, dieta_anterior=None, accion=None, ultimo_registro=None):
        if self.api_client is not None:
            try:
                datos = self.api_client.generar_dieta(perfil, dieta_anterior, accion, ultimo_registro)  
                return self._convertir_respuesta_api(datos)
            except Exception as error:
                print(f"No se pudo usar la API: {error}")
                print("Se usará una dieta local de respaldo.")

        return self._generar_dieta_local(perfil)

    # Convierte la respuesta JSON de la API en objetos del sistema
    def _convertir_respuesta_api(self, datos):
        comidas = []

        for comida_data in datos.get("comidas", []):
            alimentos = []

            for alimento_data in comida_data.get("alimentos", []):
                alimento = Alimento(
                    alimento_data["nombre"],
                    alimento_data["cantidad"]
                )
                alimentos.append(alimento)

            comida = Comida(
                comida_data["tipo"],
                alimentos
            )
            comidas.append(comida)

        return RegistrarDieta(
            nombre_dieta=datos["nombre_dieta"],
            calorias=datos["calorias"],
            proteinas=datos["proteinas"],
            carbohidratos=datos["carbohidratos"],
            grasas=datos["grasas"],
            descripcion=datos["descripcion"],
            comidas=comidas
        )

    # Dieta de respaldo cuando no se usa la API
    def _generar_dieta_local(self, perfil):
        comidas = [
            Comida("Desayuno", [
                Alimento("Avena", "80 g"),
                Alimento("Plátano", "1 pieza"),
                Alimento("Leche", "250 ml")
            ]),
            Comida("Comida", [
                Alimento("Pollo", "180 g"),
                Alimento("Arroz", "150 g"),
                Alimento("Verduras", "100 g")
            ]),
            Comida("Cena", [
                Alimento("Huevo", "2 piezas"),
                Alimento("Pan integral", "2 rebanadas"),
                Alimento("Aguacate", "50 g")
            ])
        ]

        return RegistrarDieta(
            nombre_dieta="Dieta local de respaldo",
            calorias=2200,
            proteinas=130,
            carbohidratos=250,
            grasas=65,
            descripcion="Dieta temporal generada localmente mientras no se usa la API.",
            comidas=comidas
        )


# Clase que se comunica con la API para generar dietas personalizadas
class APIClienteDietas:
    def __init__(self, api_key=None, modelo="gpt-4.1-mini"):
        self.cliente = OpenAI(api_key=api_key)
        self.modelo = modelo

    # Genera una dieta usando el perfil, dieta anterior y progreso del usuario
    def generar_dieta(self, perfil, dieta_anterior=None, accion=None, ultimo_registro=None):
        info_dieta_anterior = ""

        if dieta_anterior is not None:
            info_dieta_anterior = f"""
        Dieta anterior:
        Nombre: {dieta_anterior.nombre_dieta}
        Calorías: {dieta_anterior.calorias}
        Proteínas: {dieta_anterior.proteinas}
        Carbohidratos: {dieta_anterior.carbohidratos}
        Grasas: {dieta_anterior.grasas}
        Descripción: {dieta_anterior.descripcion}
        
        Acción recomendada por el modelo: {accion}
        """

        info_progreso = ""

        if ultimo_registro is not None:
            info_progreso = f"""
        Último registro de progreso:
        Fecha: {ultimo_registro.fecha}
        Peso actual: {ultimo_registro.peso_actual}
        Cumplimiento: {ultimo_registro.cumplimiento}
        Actividad semanal: {ultimo_registro.actividad_semana}
        Síntomas: {ultimo_registro.sintomas}
        Observaciones del usuario: {ultimo_registro.observaciones}
        """
                
        prompt = f"""
Genera una dieta personalizada para este usuario.

Datos:
Edad: {perfil.edad}
Sexo: {perfil.sexo}
Peso: {perfil.peso}
Altura: {perfil.altura}
IMC: {round(perfil.imc, 2)}
Nivel de actividad: {perfil.nivel_actividad}
Objetivo: {perfil.objetivo}
Alergias: {perfil.alergias}
Alimentos no deseados: {perfil.no_deseados}
{info_dieta_anterior}
{info_progreso}

Devuelve únicamente JSON válido con esta estructura:
{{
  "nombre_dieta": "string",
  "calorias": 0,
  "proteinas": 0,
  "carbohidratos": 0,
  "grasas": 0,
  "descripcion": "string",
  "comidas": [
    {{
      "tipo": "Desayuno",
      "alimentos": [
        {{
          "nombre": "string",
          "cantidad": "string"
        }}
      ]
    }}
  ]
}}

Reglas:
- No incluyas alimentos de alergias.
- No incluyas alimentos no deseados.
- Incluye desayuno, comida y cena.
- Cada comida debe tener mínimo 3 alimentos.
- No generes dietas extremas ni irreales.
- Las calorías deben ser coherentes con el peso, altura y nivel de actividad.
- Ajusta las calorías totales según el objetivo del usuario.
- Toma en cuenta las observaciones del usuario.
- Si el usuario dice que es demasiada comida, reduce el volumen de alimentos sin descuidar el objetivo.
- Si el usuario dice que quedó con hambre, usa alimentos más saciantes.
- Si la acción recomendada es mantener pero hay observaciones negativas, realiza ajustes ligeros.
- Si hay síntomas, cambia la dieta automáticamente.
- Lo mas importante Responde SOLO JSON válido, SIN TEXTO EXTRA.
"""

        respuesta = self.cliente.responses.create(
            model=self.modelo,
            input=prompt
        )
        
        texto = respuesta.output_text.strip()
        texto = re.sub(r"```json\n?", "", texto)
        texto = re.sub(r"```", "", texto).strip()

        try:
            return json.loads(texto)
        except json.JSONDecodeError:
            print("Respuesta cruda de la API:")
            print(texto)
            raise ValueError("La API no devolvió JSON válido")


# Clase que guarda un registro de progreso del usuario
class RegistrarProgreso: 
    def __init__(self, fecha, peso_actual, cumplimiento, actividad_semana, sintomas, observaciones):
        if not isinstance(fecha, str):
            raise TypeError("La fecha debe ser texto")        
        if not isinstance(peso_actual, (int, float)):
            raise TypeError("El peso actual debe ser un número")        
        if not isinstance(cumplimiento, (int, float)):
            raise TypeError("El cumplimiento debe ser un número del 0 al 100")        
        if not isinstance(actividad_semana, int):
            raise TypeError("La actividad de la semana debe ser un entero")      
        if not isinstance(sintomas, list):
            raise TypeError("Los síntomas deben ser una lista")       
        if not isinstance(observaciones, str):
            raise TypeError("Las observaciones deben ser texto")        
        if peso_actual <= 0:
            raise ValueError("El peso actual debe ser mayor a 0")        
        if cumplimiento < 0 or cumplimiento > 100:
            raise ValueError("El cumplimiento debe estar entre 0 y 100")
        if actividad_semana < 1 or actividad_semana > 3:
            raise ValueError("La actividad semanal debe estar entre 1 y 3")  
                    
        self.fecha = fecha
        self.peso_actual = peso_actual
        self.cumplimiento = cumplimiento
        self.actividad_semana = actividad_semana
        self.sintomas = sintomas
        self.observaciones = observaciones

    # Muestra el registro de progreso en consola
    def mostrar_registro(self): 
        print("=== Registro de Progreso ===")
        print(f"Fecha: {self.fecha}")
        print(f"Peso actual: {self.peso_actual} kg")
        print(f"Cumplimiento: {self.cumplimiento}%")
        print(f"Actividad semanal: {self.actividad_semana}")
        print(f"Síntomas: {', '.join(self.sintomas) if self.sintomas else 'Ninguno'}")
        print(f"Observaciones: {self.observaciones}")


# Clase que almacena todos los registros de progreso
class HistorialProgreso: 
    def __init__(self):
        self.registros = []

    # Agrega un nuevo registro al historial
    def agregar_registro(self, registro): 
        self.registros.append(registro)  
        
    # Devuelve el último registro guardado
    def devolver_ultimo(self):
        if len(self.registros) == 0:
            return None
        return self.registros[-1]

    # Calcula el cambio total de peso desde el primer registro
    def calcular_cambio_peso(self): 
        if len(self.registros) < 2:
            return 0
        peso_registrado = self.registros[-1].peso_actual
        peso_inicial = self.registros[0].peso_actual
        return peso_registrado - peso_inicial 

    # Calcula el cambio entre los últimos dos registros
    def cambio_reciente(self): 
        if len(self.registros) < 2:
            return 0
        peso_registrado = self.registros[-1].peso_actual
        peso_anterior = self.registros[-2].peso_actual
        return peso_registrado - peso_anterior
    

# Clase que interpreta el progreso del usuario
class AnalizadorProgreso:
    
    def calcular_tendencia(self, historial):
        cambio = historial.calcular_cambio_peso()
        if cambio < 0:
            return "Progreso (bajando de peso)"
        elif cambio > 0:
            return "Aumento de peso"
        else:
            return "Sin cambios"

    def detectar_estancamiento(self, historial):
        cambio = historial.cambio_reciente()
        return cambio == 0

    def detectar_retroceso(self, historial):
        cambio = historial.cambio_reciente()
        return cambio > 0

    def generar_retroalimentacion(self, historial):
        if len(historial.registros) < 2:
            return "No hay suficientes datos para analizar"
        if self.detectar_retroceso(historial):
            return "Has subido de peso"
        if self.detectar_estancamiento(historial):
            return "Estás estancado, podrías necesitar ajustes"
        return "Has bajado de peso"
        

# Modelo que recomienda si mantener, ajustar o cambiar la dieta
class ModeloRetroalimentacion:
    def __init__(self):
        self.modelo = DecisionTreeClassifier(random_state=42)
        self.entrenado = False
        self.exactitud = None
        self._entrenar_modelo()

    # Genera datos de entrenamiento para el modelo
    def _generar_dataset(self):
        X = []
        y = []

        cambios = [-1, 0, 1]
        cumplimientos = [50, 65, 80, 90, 100]
        actividades = [1, 2, 3]
        sintomas_opciones = [0, 1]
        objetivos = [-1, 0, 1]

        for objetivo in objetivos:
            for cambio in cambios:
                for cumplimiento in cumplimientos:
                    for actividad in actividades:
                        for sintomas in sintomas_opciones:

                            if sintomas == 1:
                                accion = "cambiar"

                            elif objetivo == 1:
                                if cambio > 0 and cumplimiento >= 70:
                                    accion = "mantener"
                                elif cambio == 0:
                                    accion = "ajustar"
                                elif cambio < 0:
                                    accion = "cambiar"
                                else:
                                    accion = "ajustar"

                            elif objetivo == -1:
                                if cambio < 0 and cumplimiento >= 70:
                                    accion = "mantener"
                                elif cambio == 0:
                                    accion = "ajustar"
                                elif cambio > 0:
                                    accion = "cambiar"
                                else:
                                    accion = "ajustar"

                            else:
                                if cambio == 0:
                                    accion = "mantener"
                                elif abs(cambio) == 1 and cumplimiento >= 80:
                                    accion = "ajustar"
                                else:
                                    accion = "cambiar"

                            X.append([
                                cambio,
                                cumplimiento,
                                actividad,
                                sintomas,
                                objetivo
                            ])

                            y.append(accion)

        return X, y

    # Entrena el modelo con los datos generados
    def _entrenar_modelo(self):
        X, y = self._generar_dataset()

        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.25,
            random_state=42,
            stratify=y
        )

        self.modelo.fit(X_train, y_train)

        predicciones = self.modelo.predict(X_test)
        self.exactitud = accuracy_score(y_test, predicciones)

        self.entrenado = True

    # Convierte los datos reales del usuario en datos numéricos para el modelo
    def _procesar_datos(self, usuario, historial):
        if len(historial.registros) == 1:
            cambio = historial.devolver_ultimo().peso_actual - usuario.peso
        else:
            cambio = historial.cambio_reciente()

        if cambio > 0:
            cambio = 1
        elif cambio < 0:
            cambio = -1
        else:
            cambio = 0

        ultimo = historial.devolver_ultimo()

        cumplimiento = ultimo.cumplimiento
        actividad = ultimo.actividad_semana
        sintomas = 1 if ultimo.sintomas else 0

        objetivo = usuario.objetivo.lower()

        if "ganar" in objetivo:
            objetivo = 1
        elif "bajar" in objetivo:
            objetivo = -1
        else:
            objetivo = 0

        return [[
            cambio,
            cumplimiento,
            actividad,
            sintomas,
            objetivo
        ]]

    # Devuelve la acción recomendada por el modelo
    def recomendar_accion(self, usuario, historial):
        if len(historial.registros) == 0:
            return "sin_datos"
    
        if not self.entrenado:
            raise ValueError("El modelo no ha sido entrenado")
    
        datos = self._procesar_datos(usuario, historial)
        prediccion = self.modelo.predict(datos)
    
        return prediccion[0]

    def mostrar_exactitud(self):
        if self.exactitud is None:
            return "El modelo aún no ha sido evaluado"

        return f"Exactitud del modelo: {round(self.exactitud * 100, 2)}%"


# Clase principal que conecta todo el sistema
class SistemaNutricional: 
    def __init__(self, api_client=None):
        self.usuario = None
        self.dieta_actual = None
        self.historial = HistorialProgreso()
        self.generador_dieta = GenerarDieta(api_client)
        self.analizador = AnalizadorProgreso()
        self.modelo_retroalimentacion = ModeloRetroalimentacion()
        
    # Asigna un usuario al sistema
    def asignar_usuario(self, usuario):
        if not isinstance(usuario, PerfilUsuario):
            raise TypeError("Debe ser un objeto PerfilUsuario")
        self.usuario = usuario
        
    # Genera la primera dieta del usuario
    def generar_dieta_inicial(self):
        if self.usuario is None:
            raise ValueError("Primero debes asignar un usuario")

        self.dieta_actual = self.generador_dieta.generar_dieta(self.usuario)
        return self.dieta_actual

    # Registra un nuevo progreso en el historial
    def registrar_progreso(self, registro):
        if not isinstance(registro, RegistrarProgreso):
            raise TypeError("Debe ser un objeto RegistrarProgreso")
        self.historial.agregar_registro(registro)

    # Analiza si el usuario subió, bajó o mantuvo peso
    def analizar_usuario(self):
        if len(self.historial.registros) == 0:
            return "No hay registros de progreso"
    
        ultimo = self.historial.devolver_ultimo()
    
        if len(self.historial.registros) == 1:
            cambio = ultimo.peso_actual - self.usuario.peso
        else:
            cambio = self.historial.cambio_reciente()
    
        if cambio > 0:
            return "Has subido de peso"
        elif cambio < 0:
            return "Has bajado de peso"
        else:
            return "Te mantuviste en el mismo peso"

    # Obtiene la acción recomendada por el modelo
    def obtener_accion_recomendada(self):   
        if self.usuario is None:
            raise ValueError("No hay usuario asignado")

        return self.modelo_retroalimentacion.recomendar_accion(
            self.usuario,
            self.historial
        )

    # Actualiza la dieta usando el último progreso del usuario
    def actualizar_dieta(self):
        if self.usuario is None:
            raise ValueError("No hay usuario asignado")
    
        accion = self.obtener_accion_recomendada()
        ultimo_registro = self.historial.devolver_ultimo()
    
        self.dieta_actual = self.generador_dieta.generar_dieta(
            self.usuario,
            dieta_anterior=self.dieta_actual,
            accion=accion,
            ultimo_registro=ultimo_registro
        )
    
        return self.dieta_actual

    # Decide si mantener, ajustar o cambiar la dieta
    def evaluar_y_actualizar_dieta(self):
        accion = self.obtener_accion_recomendada()
        ultimo_registro = self.historial.devolver_ultimo()
    
        hay_observaciones = (
            ultimo_registro is not None
            and ultimo_registro.observaciones.strip() != ""
        )
    
        if accion == "sin_datos":
            return "No hay suficientes datos para tomar una decisión"
    
        if accion == "mantener" and not hay_observaciones:
            return "Se recomienda mantener la dieta actual"
    
        if accion == "mantener" and hay_observaciones:
            self.actualizar_dieta()
            return "Se recomienda mantener la dieta, pero se hicieron ajustes tomando en cuenta tus observaciones."
    
        if accion == "ajustar":
            self.actualizar_dieta()
            return "Se recomienda ajustar la dieta. Se generó una nueva dieta."
    
        if accion == "cambiar":
            self.actualizar_dieta()
            return "Se recomienda cambiar la dieta. Se generó una nueva dieta."

        return "No se pudo determinar una acción"

    # Muestra un resumen completo en consola
    def mostrar_resumen(self):
        print("\n===== RESUMEN DEL SISTEMA =====\n")
    
        if self.usuario is not None:
            self.usuario.mostrar_perfil()
        else:
            print("No hay usuario asignado")
    
        if self.dieta_actual is not None:
            self.dieta_actual.mostrar_dieta()
        else:
            print("No hay dieta asignada")
    
        if len(self.historial.registros) > 0:
            print("\n=== ÚLTIMO REGISTRO ===")
            self.historial.devolver_ultimo().mostrar_registro()
        else:
            print("\nNo hay registros de progreso")
    
        print("\n=== ANÁLISIS ===")
        print(self.analizar_usuario())
    
        print("\n=== ACCIÓN RECOMENDADA ===")
        print(self.obtener_accion_recomendada())
