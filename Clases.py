class Persona():
	def __init__(self, DNI, nombre, edad):
		self.nombre = nombre
		self.edad = edad
		self.DNI = DNI

class Empleado(Persona):
	def __init__(self, categoria, antiguedad, DNI, nombre, edad, presentismo):
		super().__init__(DNI, nombre, edad)
		self.categoria = categoria
		self.antiguedad= antiguedad
		self.presentismo = presentismo

class Sueldo():
	def __init__(self, categoria, antiguedad, presentismo):
		self.categoria = categoria
		self.antiguedad = antiguedad
		self.presentismo = presentismo
