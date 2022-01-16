from tkinter import *
from tkinter import messagebox
import sqlite3

# -------Funciones_SQL-----------------------

global miConexion
global miCursor

def conectarBBDD():
	try:
		miConexion=sqlite3.connect("EMPLEADOS")
		miCursor=miConexion.cursor()
		miCursor.execute('''
			CREATE TABLE EMPLEADOS(
			ID INTEGER PRIMARY KEY AUTOINCREMENT,
			DNI VARCHAR(20),
			NOMBRE VARCHAR(30),
			EDAD VARCHAR(20),
			CATEGORIA VARCHAR(20),
			ANTIGUEDAD VARCHAR(20),
			PRESENTISMO VARCHAR(20)
			)
			''')
	except sqlite3.OperationalError:
		messagebox.showwarning("BBDD ya existente","Usted ya esta conctado")
	finally:
		messagebox.showinfo("Conectar","Se a establecido la conexion")


def crearRegistro():
	miConexion=sqlite3.connect("EMPLEADOS")
	miCursor=miConexion.cursor()
	miCursor.execute("INSERT INTO EMPLEADOS VALUES(NULL, '" + DNI.get() + "','" + NOMBRE.get() + "','" + EDAD.get() + "','" + CATEGORIA.get() + "','" + ANTIGUEDAD.get()+ "', NULL)")
	miConexion.commit()
	messagebox.showinfo("CREATE_SQL","Se a insertado exitosamente su registro")

def leerRegistro():
	miConexion=sqlite3.connect("EMPLEADOS")
	miCursor=miConexion.cursor()
	ElUsuario=[]
	try:
		miCursor.execute("SELECT * FROM EMPLEADOS WHERE DNI=" + DNI.get())
		ElUsuario=miCursor.fetchall()
		for usuario in ElUsuario:
			DNI.set(usuario[1])
			NOMBRE.set(usuario[2])
			EDAD.set(usuario[3])
			CATEGORIA.set(usuario[4])
			ANTIGUEDAD.set(usuario[5])
			PRESENTISMO.set(int(usuario[6]))
		miConexion.commit()
	except sqlite3.OperationalError:
		messagebox.showwarning("Campo vacío","Por favor rellene el campo DNI")
	if ElUsuario == [] :
		messagebox.showwarning("Busqueda no existente","No existe el DNI indicado en la BBDD")

def actualizarRegistro():
	miConexion=sqlite3.connect("EMPLEADOS")
	miCursor=miConexion.cursor()
	miCursor.execute("UPDATE EMPLEADOS SET NOMBRE='" + NOMBRE.get() + "', EDAD='" + EDAD.get() + "', CATEGORIA='" + CATEGORIA.get() + "', ANTIGUEDAD='" + ANTIGUEDAD.get() + "', PRESENTISMO=NULL'" + "' WHERE DNI=" + DNI.get())
	miConexion.commit()
	messagebox.showinfo("UPDATE_SQL","Se a actualizado exitosamente su registro")

def borrarRegistro():
	miConexion=sqlite3.connect("EMPLEADOS")
	miCursor=miConexion.cursor()
	valor=messagebox.askquestion("DELETE_SQL","Esta seguro que quiere eliminar este registro?")
	if valor == "yes":
		miCursor.execute("DELETE FROM EMPLEADOS WHERE DNI=" + DNI.get())
		miConexion.commit()
	messagebox.showinfo("DELETE_SQL","Se a eliminado exitosamente su registro")

# -----Interfaz-Grafica--------------------------------------------


# -----Root--------------------------------

root=Tk()
root.title("Registro de Empleados")

# -----Frames--------------------------------

contenedor=Frame(root)
contenedor.pack()
superiorFrame=Frame(contenedor)
superiorFrame.grid(row=1,column=1,pady=10,padx=10)
inferiorFrame=Frame(contenedor)
inferiorFrame.grid(row=2,column=1,pady=10,padx=10)
# -----------Menu----------------------------

def limpiarCampos():
	DNI.set("")
	NOMBRE.set("")
	EDAD.set("")
	CATEGORIA.set("")
	ANTIGUEDAD.set("")
	PRESENTISMO.set(0)

def salirAplicacion():
	valor=messagebox.askquestion("Salir","Desea salir de la aplicacion")
	if valor == "yes":
		root.destroy()

barraMenu=Menu(root)
root.config(menu=barraMenu)
conectarMenu=Menu(barraMenu,tearoff=0)
conectarMenu.add_command(label="Conectar", command=conectarBBDD)
conectarMenu.add_command(label="Salir",command=salirAplicacion)

borrarMenu=Menu(barraMenu,tearoff=0)
borrarMenu.add_command(label="Borrar",command=limpiarCampos)

CRUDMenu=Menu(barraMenu,tearoff=0)
CRUDMenu.add_command(label="Crear",command=crearRegistro)
CRUDMenu.add_command(label="Leer",command=leerRegistro)
CRUDMenu.add_command(label="Actualizar",command=actualizarRegistro)
CRUDMenu.add_command(label="Borrar", command=borrarRegistro)

ayudaMenu=Menu(barraMenu,tearoff=0)
ayudaMenu.add_command(label="Licencia")
ayudaMenu.add_command(label="Acerca de...")

barraMenu.add_cascade(label="Conectar",menu=conectarMenu)
barraMenu.add_cascade(label="CRUD",menu=CRUDMenu)
barraMenu.add_cascade(label="Borrar",menu=borrarMenu)
barraMenu.add_cascade(label="Ayuda",menu=ayudaMenu)

# ----------Labels---------------------------
DNILabel=Label(superiorFrame,text="DNI:")
DNILabel.grid(row=1,column=1,pady=10,padx=10)

NOMBRELabel=Label(superiorFrame,text="NOMBRE:")
NOMBRELabel.grid(row=2,column=1,pady=10,padx=10)

EDADLabel=Label(superiorFrame,text="EDAD:")
EDADLabel.grid(row=3,column=1,pady=10,padx=10)

CATEGORIALabel=Label(superiorFrame,text="CATEGORIA:")
CATEGORIALabel.grid(row=4,column=1,pady=10,padx=10)

ANTIGUEDADLabel=Label(superiorFrame,text="ANTIGUEDAD:")
ANTIGUEDADLabel.grid(row=5,column=1,pady=10,padx=10)

PRESENTISMOLabel=Label(superiorFrame,text="PRESENTISMO:")
PRESENTISMOLabel.grid(row=6,column=1,pady=10,padx=10)
# ---------Entrys--------------------

DNI=StringVar()
NOMBRE=StringVar()
EDAD=StringVar()
CATEGORIA=StringVar()
ANTIGUEDAD=StringVar()
PRESENTISMO=StringVar()

DNIEntry=Entry(superiorFrame, textvariable=DNI)
DNIEntry.grid(row=1,column=2,pady=10,padx=10)

NOMBREEntry=Entry(superiorFrame, textvariable=NOMBRE)
NOMBREEntry.grid(row=2,column=2,pady=10,padx=10)

EDADEntry=Entry(superiorFrame, textvariable=EDAD)
EDADEntry.grid(row=3,column=2,pady=10,padx=10)

ANTIGUEDADEntry=Entry(superiorFrame, textvariable=ANTIGUEDAD)
ANTIGUEDADEntry.grid(row=4,column=2,pady=10,padx=10)

CATEGORIAEntry=Entry(superiorFrame, textvariable=CATEGORIA)
CATEGORIAEntry.grid(row=5,column=2,pady=10,padx=10)

presentismoRadio1=Radiobutton(superiorFrame,text="Liquidar Presentismo",variable=PRESENTISMO,value=True)
presentismoRadio1.grid(row=6,column=2,pady=10,padx=10)
presentismoRadio2=Radiobutton(superiorFrame,text="No Liquidar Presentismo",variable=PRESENTISMO,value=False)
presentismoRadio2.grid(row=7,column=2,pady=10,padx=10)
# ----------Buttons----------------
createButton=Button(inferiorFrame,text="Create",command=crearRegistro)
createButton.grid(row=1,column=1,pady=10,padx=10)

readButton=Button(inferiorFrame,text="Read",command=leerRegistro)
readButton.grid(row=1,column=2,pady=10,padx=10)

updateButton=Button(inferiorFrame,text="Update", command=actualizarRegistro)
updateButton.grid(row=1,column=3,pady=10,padx=10)

deleteButton=Button(inferiorFrame,text="Delete", command=borrarRegistro)
deleteButton.grid(row=1,column=4,pady=10,padx=10)


limpiarCampos()
root.mainloop()
