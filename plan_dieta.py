class PerfilUsuario: 
  def __init__(self, nombre, edad, sexo, peso, altura, nivel_actividad, objetivo, alergias, no_deseados):
    if not isinstance(nombre, str):
        raise TypeError("nombre debe ser del tipo str")
    if not isinstance(edad, int):
        raise TypeError("nombre debe ser del tipo str")
    if edad<0 and edad>130: 
        raise ValueError("La edad debe de estar entre 0 y 130")
    if not isinstance(sexo, str):
        raise TypeError("nombre debe ser del tipo str")
    if not isinstance(sexo, str):
        raise TypeError("nombre debe ser ")
    if not isinstance(peso, (int, float)):
         raise TypeError("El peso debe ser un número unicamente")
    if not isinstance(altura, (int, float)):
        raise TypeError("La altura debe ser un número")
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
    
  @property
  def imc(self): 
      if self.altura == 0: #En caso de que la altura sea 0 retornamos 0 para evitar invalidación
          return 0
      imc = self.peso/self.altura**2
      return imc 

  def interpretar_imc(self): 
    
      if self.imc<18.5: 
          return "bajo"
      elif self.imc<25: 
          return "normal"
      elif self.imc<30: 
          return "sobre peso"
      else:
          return "obesidad"
  
  def mostrar_perfil(self): 
      print("====Perfil del Usuario====\n")
      print(f"Nombre: {self.nombre}")
      print(f"Edad: {self.edad}años")
      print(f"Sexo: {self.sexo}")
      print(f"Peso: {self.peso}kg")
      print(f"Altura: {self.altura}m")
      print(f"Nivel de actividad: {self.nivel_actividad}")
      print(f"Objetivo: {self.objetivo}")
      print(f"Alergias: {", ".join(self.alergias)}")
      print(f"Alimentos no deseados: {", ".join(self.no_deseados)}")
      print(f"IMC: {round(self.imc,3)}")
      print(f"Categoria de IMC: {self.interpretar_imc()}")
