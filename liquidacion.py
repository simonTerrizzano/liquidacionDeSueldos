from tkinter import *
from tkinter import messagebox
import sqlite3




# -------Clases-----------------------


sueldosCategorias={"1": 82000.0, "2": 78000.0, "3": 75000.0, "4": 72500.0, "5": 69000.0}

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
	def estadoEmpleado(self):
		print("Nombre: {} \nEdad {} años\nCategoria: {} \nAntiguedad: {} años \n".format(self.nombre, self.edad, self.categoria,self.antiguedad))

class Sueldo():
	def __init__(self, categoria, antiguedad, presentismo):
		self.categoria = categoria
		self.antiguedad = antiguedad
		self.presentismo = presentismo
	def liquidarSueldo(self):

		def descuentoSueldo(sueldo, porsentaje):
			descuento = (sueldo/100) * porsentaje
			return descuento

		sueldoBase=sueldosCategorias[str(self.categoria)]
		sueldoBruto=sueldoBase
		cabeceraLabel=Label(liquidacionFrame,text="     			REMUNERACIONES	   DESCUENTOS")
		cabeceraLabel.grid(row=1,column=3,pady=10,padx=10)
		basicoLabel=Label(liquidacionFrame,text="+Basico:			"+ str(sueldoBase))
		basicoLabel.grid(row=2,column=3,pady=10,padx=10)
		if self.presentismo != 1:
			sueldoBruto=sueldoBase+(sueldoBase/10)
			presentismoLabel=Label(liquidacionFrame,text="+Presentismo: 		"+ str(sueldoBase/10))
			presentismoLabel.grid(row=3,column=3,pady=10,padx=10)
		if self.antiguedad > 0:
			sueldoBruto = sueldoBase + (sueldoBase/100)*(self.antiguedad*2)
			antiguedadLabel=Label(liquidacionFrame,text="+Antiguedad:		"+ str((sueldoBase/100)*(self.antiguedad*2)))
			antiguedadLabel.grid(row=4,column=3,pady=10,padx=10)
		sueldoNeto = sueldoBruto
		jubilacion = descuentoSueldo(sueldoBruto,11)
		sueldoNeto-= jubilacion
		jubilacionLabel=Label(liquidacionFrame,text="- Jubilacion: 						"+ str(jubilacion))
		jubilacionLabel.grid(row=5,column=3,pady=10,padx=10)
		sueldoNeto-= descuentoSueldo(sueldoBruto,2.5)
		obraSocialLabel=Label(liquidacionFrame,text="- Obra Social: 						"+ str(descuentoSueldo(sueldoBruto,2.5)))
		obraSocialLabel.grid(row=6,column=3,pady=10,padx=10)
		sueldoNeto-= descuentoSueldo(sueldoBruto,3)
		sindicatoLabel=Label(liquidacionFrame,text="- Sindicato: 						"+ str(round(descuentoSueldo(sueldoBruto,3),2)))
		sindicatoLabel.grid(row=7,column=3,pady=10,padx=10)
		brutoLabel=Label(liquidacionFrame,text="Sueldo Bruto: 		"+ str(sueldoBruto))
		brutoLabel.grid(row=8,column=3,pady=10,padx=10)
		netoLabel=Label(liquidacionFrame,text="Sueldo Neto: 						"+ str(round(sueldoNeto,2)))
		netoLabel.grid(row=9,column=3,pady=10,padx=10)


# -------Funciones_SQL-----------------------

global miConexion
global miCursor


def leerRegistro():
	actualizarRegistro()

	miConexion=sqlite3.connect("EMPLEADOS")
	miCursor=miConexion.cursor()
	ElUsuario=[]
	try:
		miCursor.execute("SELECT * FROM EMPLEADOS WHERE DNI=" + DNI.get())
		ElUsuario=miCursor.fetchall()
		global lista
		lista=[]
		try:
			for usuario in ElUsuario:
				lista.append(usuario[1])
				lista.append(usuario[2])
				lista.append(usuario[3])
				lista.append(int(usuario[4]))
				lista.append(int(usuario[5]))
				lista.append(int(usuario[6]))
			empleado=Empleado(lista[3],lista[4],lista[0],lista[1],lista[2],lista[5])
			sueldo=Sueldo(empleado.categoria,empleado.antiguedad,empleado.presentismo)
			sueldo.liquidarSueldo()
			miConexion.commit()
		except IndexError:
			messagebox.showwarning("Busqueda no existente","No existe el DNI indicado en la BBDD")
	except sqlite3.OperationalError:
		pass
		

def actualizarRegistro():
	miConexion=sqlite3.connect("EMPLEADOS")
	miCursor=miConexion.cursor()
	try:
		miCursor.execute("UPDATE EMPLEADOS SET PRESENTISMO='" + PRESENTISMO.get() + "' WHERE DNI=" + DNI.get())
		miConexion.commit()
	except sqlite3.OperationalError:
		messagebox.showwarning("CAMPO ERRONEO","Por favor ingrese un DNI valido")


# -------Interfaz-Grafica-----------------------

root=Tk()
root.title("Liquidación de Sueldos")

# -----Frames--------------------------------

contenedor=Frame(root)
contenedor.pack()
liquidacionFrame=Frame(contenedor)
liquidacionFrame.grid(row=1,column=2,pady=10,padx=10)

# ----------Label---------------------------

NOMBRE=StringVar()
CATEGORIA=StringVar()
EDAD=StringVar()
ANTIGUEDAD=StringVar()

DNILabel=Label(liquidacionFrame,text="DNI:")
DNILabel.grid(row=1,column=1,pady=10,padx=10)

# ---------Entrys--------------------

DNI=StringVar()
PRESENTISMO=StringVar()

DNIEntry=Entry(liquidacionFrame, textvariable=DNI)
DNIEntry.grid(row=1,column=2,pady=10,padx=10)

# ----------RadioButtons----------------

presentismoRadio1=Radiobutton(liquidacionFrame,text="Liquidar Presentismo",variable=PRESENTISMO,value=True)
presentismoRadio1.grid(row=3,column=1,pady=10,padx=10)
presentismoRadio2=Radiobutton(liquidacionFrame,text="No Liquidar Presentismo",variable=PRESENTISMO,value=False)
presentismoRadio2.grid(row=4,column=1,pady=10,padx=10)

# ----------Buttons----------------
liquidarButton=Button(liquidacionFrame,text="Liquidar",command=leerRegistro)
liquidarButton.grid(row=5,column=1,pady=10,padx=10)



PRESENTISMO.set(0)
root.mainloop()
