from tkinter import *
from tkinter import messagebox
from Clases import *
from Categorias import *
import sqlite3


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
			empleado=Empleado(lista[4],lista[3],lista[0],lista[1],lista[2],lista[5])
			sueldo=Sueldo(empleado.categoria,empleado.antiguedad,empleado.presentismo)
			liquidar(sueldo,empleado)
			miConexion.commit()
		except IndexError:
			messagebox.showwarning("Busqueda no existente","No existe el DNI indicado en la BBDD")
	except sqlite3.OperationalError:
		pass
		

def actualizarRegistro():
	miConexion=sqlite3.connect("EMPLEADOS")
	miCursor=miConexion.cursor()
	try:
		datos=PRESENTISMO.get()
		miCursor.execute("UPDATE EMPLEADOS SET PRESENTISMO=? WHERE DNI =" + DNI.get(), (datos))
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

def liquidar(sueldo,empleado):
	descuentoSueldo=lambda sueldo,porsentaje:(sueldo/100) * porsentaje

	sueldoBase=sueldosCategorias[str(sueldo.categoria)]
	sueldoBruto=sueldoBase
	nombre_dniLabel=Label(liquidacionFrame,text="Nombre del empleado:  " + empleado.nombre + " | DNI: " + empleado.DNI)
	nombre_dniLabel.grid(row=1,column=3,pady=10,padx=10)
	categoria_antiguedadLabel=Label(liquidacionFrame,text="Categoria: " + str(empleado.categoria) + " | Antiguedad: " + str(empleado.antiguedad))
	categoria_antiguedadLabel.grid(row=2,column=3,pady=10,padx=10)
	cabeceraLabel=Label(liquidacionFrame,text="	     			REMUNERACIONES	   DESCUENTOS")
	cabeceraLabel.grid(row=3,column=3,pady=10,padx=10)
	basicoLabel=Label(liquidacionFrame,text="+Basico:			"+ str(sueldoBase))
	basicoLabel.grid(row=4,column=3,pady=10,padx=10)
	if sueldo.presentismo == 1:
		sueldoBruto=sueldoBase+(sueldoBase/10)
		presentismoLabel=Label(liquidacionFrame,text="+Presentismo: 		"+ str(sueldoBase/10))
		presentismoLabel.grid(row=5,column=3,pady=10,padx=10)
	if sueldo.antiguedad > 0:
		sueldoBruto = sueldoBase + (sueldoBase/100)*(sueldo.antiguedad*2)
		antiguedadLabel=Label(liquidacionFrame,text="+Antiguedad:		"+ str((sueldoBase/100)*(sueldo.antiguedad*2)))
		antiguedadLabel.grid(row=6,column=3,pady=10,padx=10)
	sueldoNeto = sueldoBruto
	jubilacion = descuentoSueldo(sueldoBruto,11)
	sueldoNeto-= jubilacion
	jubilacionLabel=Label(liquidacionFrame,text="- Jubilacion: 						"+ str(jubilacion))
	jubilacionLabel.grid(row=7,column=3,pady=10,padx=10)
	sueldoNeto-= descuentoSueldo(sueldoBruto,2.5)
	obraSocialLabel=Label(liquidacionFrame,text="- Obra Social: 						"+ str(descuentoSueldo(sueldoBruto,2.5)))
	obraSocialLabel.grid(row=8,column=3,pady=10,padx=10)
	sueldoNeto-= descuentoSueldo(sueldoBruto,3)
	sindicatoLabel=Label(liquidacionFrame,text="- Sindicato: 						"+ str(round(descuentoSueldo(sueldoBruto,3),2)))
	sindicatoLabel.grid(row=9,column=3,pady=10,padx=10)
	brutoLabel=Label(liquidacionFrame,text="Sueldo Bruto: 		"+ str(sueldoBruto))
	brutoLabel.grid(row=10,column=3,pady=10,padx=10)
	netoLabel=Label(liquidacionFrame,text="Sueldo Neto: 						"+ str(round(sueldoNeto,2)))
	netoLabel.grid(row=11,column=3,pady=10,padx=10)

# ---------Entrys--------------------

DNI=StringVar()
PRESENTISMO=StringVar()
PRESENTISMO.set(0)
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



root.mainloop()
