class RegistrarDieta: 
    def __init__(self,nombre_dieta:str,calorias:int|float, proteinas:int|float, carbohidratos:int|float,grasas:int|float, descripcion:str):
        
        if not isinstance(nombre_dieta, str):
            raise TypeError("El nombre de la dieta debe ser texto")
        if not isinstance(calorias, (int, float)):
            raise TypeError("Las calorías deben ser un número")
        if not isinstance(proteinas, (int, float)):
            raise TypeError("Las proteínas deben ser un número")
        if not isinstance(carbohidratos, (int, float)):
            raise TypeError("Los carbohidratos deben ser un número")
        if not isinstance(grasas, (int, float)):
            raise TypeError("Las grasas deben ser un número")
        if not isinstance(descripcion, str):
            raise TypeError("La descripción debe ser texto")
            
        self.nombre_dieta = nombre_dieta
        self.calorias = calorias
        self.proteinas = proteinas
        self.carbohidratos = carbohidratos
        self.grasas = grasas
        self.descripcion = descripcion
        
    def mostrar_dieta(self):
        print("\n====Plan dieta=====\n")
        print(f"Nombre: {self.nombre_dieta}")
        print(f"Calorías: {self.calorias}kcal")
        print(f"Proteínas: {self.proteinas} g")
        print(f"Carbohidratos: {self.carbohidratos} g")
        print(f"Grasas: {self.grasas} g")
        print(f"Descripción: {self.descripcion}")
