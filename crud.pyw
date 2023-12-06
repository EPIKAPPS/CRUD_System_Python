import tkinter as tk
from tkinter import messagebox, ttk
import pymysql

# Conexión a la base de datos
conexion = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="test"
)

# Crear cursor
cursor = conexion.cursor()

# Función para crear un nuevo registro
def crear_registro(event=None):
    # Obtener los valores de los campos de entrada
    nombre = nombre_entry.get()
    edad = edad_entry.get()

    # Validar que se hayan ingresado ambos campos
    if nombre and edad:
        try:
            # Crear el nuevo registro
            cursor.execute("INSERT INTO personas (nombre, edad) VALUES (%s, %s)", (nombre, edad))
            conexion.commit()
            nombre_entry.delete(0, "end")  # Borra el texto ingresado en el campo de nombre
            edad_entry.delete(0, "end")  # Borra el texto ingresado en el campo de edad
            messagebox.showinfo("Éxito", "Registro creado con éxito.")
            leer_registros()
        except Exception as e:
            # Mostrar un mensaje de error si no se pudo crear el registro
            messagebox.showerror("Error", f"No se pudo crear el registro. Error: {str(e)}")
    else:
        # Mostrar un mensaje si no se ingresó nombre o edad
        messagebox.showwarning("Advertencia", "Por favor, ingrese nombre y edad.")

# Función para leer registros y actualizar la tabla
def leer_registros():
    try:
        # Leer los registros
        cursor.execute("SELECT * FROM personas")
        registros = cursor.fetchall()

        # Limpiar la tabla antes de actualizar
        for row in tabla.get_children():
            tabla.delete(row)

        # Actualizar la tabla con nuevos registros
        for registro in registros:
            tabla.insert("", "end", values=registro)
    except Exception as e:
        print(f"No se pudieron leer los registros. Error: {str(e)}")

# Función para editar un registro
def editar_registro(event=None):
    # Obtener el ID del registro seleccionado
    seleccion = tabla.selection()
    if seleccion:
        # Obtener los valores de los campos de entrada
        id_seleccionado = seleccion[0]
        nombre_actual = tabla.item(id_seleccionado, "values")[1]
        edad_actual = tabla.item(id_seleccionado, "values")[2]

        # Mostrar la ventana de datos para editar el registro
        mostrar_datos(id_seleccionado, nombre_actual, edad_actual)

    else:
        # Mostrar un mensaje si no se seleccionó un registro
        messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para editar.")


# Función para eliminar un registro
def eliminar_registro(event=None):
    seleccion = tabla.selection()
    if seleccion:
        # Obtener el ID del registro seleccionado
        id_seleccionado = seleccion[0]       
        id_ = tabla.item(id_seleccionado, "values")[0]

        # Mostrar cuadro de diálogo de confirmación
        respuesta = messagebox.askquestion("Confirmar eliminación", f"¿Estás seguro de que quieres eliminar el registro con ID {id_}?")
        if respuesta == "yes":
            try:
                # Eliminar el registro
                cursor.execute("DELETE FROM personas WHERE id=%s", (id_,))
                conexion.commit()
                messagebox.showinfo("Éxito", f"Registro con ID {id_} ha sido eliminado con éxito.")
                leer_registros()
            except Exception as e:
                # Mostrar un mensaje de error si no se pudo eliminar el registro
                messagebox.showerror("Error", f"No se pudo eliminar el registro. Error: {str(e)}")
        else:
            # Mostrar un mensaje si se canceló la eliminación
            messagebox.showinfo("Cancelado", "Eliminación cancelada.")
    else:
        # Mostrar un mensaje si no se seleccionó ninguño
        messagebox.showwarning("Advertencia", "Por favor, selecciona un registro para eliminar.")


# Función para mostrar la ventana de datos
def mostrar_datos(id, nombre, edad):
    # Crear la ventana de datos
    ventana_datos = tk.Toplevel()
    ventana_datos.title("Editar Registro")
    
    # Obtener las dimensiones de la pantalla
    ancho_pantalla = ventana_datos.winfo_screenwidth()
    alto_pantalla = ventana_datos.winfo_screenheight()
    
    # Calcular las coordenadas x e y para centrar la ventana
    x = (ancho_pantalla - 400) // 2
    y = (alto_pantalla - 200) // 2
    
    # Establecer las coordenadas de la ventana
    ventana_datos.geometry(f"400x200+{x}+{y}")
 
    seleccion = tabla.selection()

    id_seleccionado = seleccion[0]
    id_ = tabla.item(id_seleccionado, "values")[0]
    
    # Crear etiquetas y campos de entrada para mostrar los datos
    etiqueta_ID = tk.Label(ventana_datos, text="ID: " + id_, bg="#daed9f")
    etiqueta_ID.pack()
    etiqueta_nombre = tk.Label(ventana_datos, text="Nombre:")
    etiqueta_nombre.pack()
    entrada_nombre_valor = tk.Entry(ventana_datos)
    entrada_nombre_valor.pack()
    entrada_nombre_valor.insert(0, nombre)
    etiqueta_edad = tk.Label(ventana_datos, text="Edad:")
    etiqueta_edad.pack()
    entrada_edad_valor = tk.Entry(ventana_datos)
    entrada_edad_valor.pack()
    entrada_edad_valor.insert(0, edad)

    # Función para actualizar los datos
    def actualizar_datos():
        # Obtener los valores de los campos de entrada
        nuevo_nombre = entrada_nombre_valor.get()
        nueva_edad = entrada_edad_valor.get()

        seleccion = tabla.selection()

        # Obtener el ID del registro seleccionado
        id_seleccionado = seleccion[0]
        id_ = tabla.item(id_seleccionado, "values")[0]

        if nuevo_nombre and nueva_edad:
            try:
                # Actualizar el registro
                cursor.execute("UPDATE personas SET nombre=%s, edad=%s WHERE id=%s", (nuevo_nombre, nueva_edad, id_))
                conexion.commit()
                nombre_entry.delete(0, "end")  # Borra el texto ingresado en el campo de nombre
                edad_entry.delete(0, "end")  # Borra el texto ingresado en el campo de edad
                messagebox.showinfo("Éxito", "Registro con ID " + id_ + " ha sido actualizado con éxito.")
                leer_registros()
                # cerrar ventana de datos
                ventana_datos.destroy()
            except Exception as e:
                # Mostrar un mensaje de error si no se pudo actualizar el registro
                messagebox.showerror("Error", f"No se pudo actualizar el registro. Error: {str(e)}")
        else:
            # Mostrar un mensaje si no se ingresó nombre o edad
            messagebox.showwarning("Advertencia", "Por favor, ingrese nombre y edad.")

    # Crear el botón de actualización
    boton_actualizar = tk.Button(ventana_datos, text="Actualizar", command=actualizar_datos)
    boton_actualizar.pack()

    

# Interfaz gráfica con Tkinter
app = tk.Tk()
app.title("Sistema CRUD")
app.geometry("300x400")
# bloquea el tamaño de la ventana
app.resizable(False, False)

# Widgets
nombre_label = tk.Label(app, text="Nombre:")
nombre_label.pack()

nombre_entry = tk.Entry(app)
nombre_entry.pack()

edad_label = tk.Label(app, text="Edad:")
edad_label.pack()

edad_entry = tk.Entry(app)
edad_entry.pack()

crear_button = tk.Button(app, text="Crear Registro", command=crear_registro)
crear_button.pack(pady=10)

edad_label = tk.Label(app, text="Editar registro: Doble clic\nEliminar registro: Botón Suprimir", font=("Verdana", 7), justify="left")
edad_label.pack()

# Configuración del Treeview para mostrar los registros
columnas = ("ID", "Nombre", "Edad")
tabla = ttk.Treeview(app, columns=columnas, show="headings")

# Configuración de encabezados
for col in columnas:
    tabla.heading(col, text=col)
    tabla.column(col, width=70)  # Ajusta el ancho de las columnas según sea necesario

# Agrega una barra de desplazamiento vertical
scrollbar = ttk.Scrollbar(app, orient="vertical", command=tabla.yview)
tabla.configure(yscroll=scrollbar.set)

scrollbar.pack(side="right", fill="y")
tabla.pack()

# Configura la altura máxima de la lista
max_height = 200
tabla.configure(height=max_height)

# Eventos de clic en los registros para editar y eliminar
tabla.bind("<Double-1>", editar_registro)
tabla.bind("<Delete>", eliminar_registro)

# Eventos de teclado ENTER para crear y editar
nombre_entry.bind("<Return>", crear_registro)
edad_entry.bind("<Return>", crear_registro)

# Lee e inicializa los registros al inicio
leer_registros()

# Ejecuta la aplicación
app.mainloop()

# Cierra la conexión al salir de la aplicación
conexion.close()
