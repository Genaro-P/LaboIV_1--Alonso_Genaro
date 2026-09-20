import tkinter as tk
import copy

#URL del repositorio de github: https://github.com/Genaro-P/LaboIV_1--Alonso_Genaro
#Integrantes: Giuliano Alonso Giambelluca, Perez Genaro.

#Ventana principal
ventana = tk.Tk()
ventana.title("Calculadora de determinantes/Sistemas lineales")
ventana.geometry("720x300")

#Frame (subventana) para la grid principal donde pondremos la matriz y los vectores
frame_matrix = tk.Frame(ventana, relief= "groove", borderwidth= 2)
frame_matrix.place(relx= 0.5, rely= 0.4, anchor= "center")

tk.Label(frame_matrix, text= "A.x = b", font= ("times new roman", 12)).grid(row=0, column=0, columnspan= 10)

#No es necesario inicializar variables para ubicar widgets sencillos
tk.Label(frame_matrix, text= "Matriz A", font= ("times new roman", 10)).grid(row=1,column=0, columnspan=6,padx= 50)
tk.Label(frame_matrix, text= "Vector b", font= ("times new roman", 10)).grid(row=1, column=6)
tk.Label(frame_matrix, text= "Vector x", font= ("times new roman", 10)).grid(row=1, column=7)

#Cartel que le advierte al usuario de solo ingresar digitos, signo negativo o decimal
label_notdigit = tk.Label(ventana, text= "", font= ("times new roman", 12))
label_notdigit.pack(anchor= "s", side= "bottom")

#El evento analizado es cuando el usuario suelta la tecla que presiono para ingresar los numeros
def digit(event):
    try:
        if not ((44 < event.keycode) and (event.keycode<58) and event.keycode != 47):
            raise ValueError
    except ValueError:
        #Saltea el caso de entrada vacia
        if(event.widget.get().strip() != ""):
            label_notdigit.config(text= "Por favor, solo ingresa digitos o los \n simbolos correctos.")
        #Borra cualquier contenido de la entrada
        event.widget.delete(0, tk.END)
    else:
        label_notdigit.config(text= "")

#Listas de widgets:
entradas_A = [] #Entradas de la matriz A
entradas_b = [] #Entradas del vector b
labels_x = [] #Carteles para cada resultado de x 

#Este 'for' crea la grid a partir de la row = 2,
#donde estan los carteles indicando las filas/columnas y las entradas de valores
for i in range(6):
    if(i>0):
        #Creamos una lista nueva en cada componente de entradas_A, haciendola una lista bidimensional
        entradas_A.append([]) 
        #Esto ingresa una nueva entrada en la lista del vector b y la ubica en la 
        #grid, si hacemos las dos cosas en la misma linea, la lista obtendra un objeto tipo 'None'
        entradas_b.append(tk.Entry(frame_matrix, width= 6))
        entradas_b[i-1].grid(row= 2+i, column= 6, padx= 12, pady= 2)
        #Esto enlaza la funcion 'digit' al evento mencionado anteriormente
        entradas_b[i-1].bind("<KeyRelease>", digit)
        labels_x.append(tk.Label(frame_matrix, text= "", width= 6, relief= "ridge"))
        labels_x[i-1].grid(row= 2+i, column= 7, padx= 2, pady= 2)
    for j in range(6):
        if((i==0) != (j==0)): 
            if(j!=0):
                tk.Label(frame_matrix, text= j-1, font= ("times new roman", 8)
                         ).grid(row= 2+i, column=j)
            else:
                tk.Label(frame_matrix, text= i-1, font= ("times new roman", 8)
                         ).grid(row= 2+i, column=j)
        else:
            if(i==0 and j==0):
                #Crea un cartel vacio, nada mas para ocupar espacio
                tk.Label(frame_matrix, text= "", font= ("times new roman", 8)
                        ).grid(row= 2+i, column=j)
            else:
                #Entradas para matriz A
                entradas_A[i-1].append(tk.Entry(frame_matrix, width = 6))
                entradas_A[i-1][j-1].grid(row= 2+i, column= j, padx= 2, pady= 2)
                entradas_A[i-1][j-1].bind("<KeyRelease>", digit)
    

#Este frame contiene todos los botones de calculo que el usuario hara sobre los 
#vectores/matrices, ubicados a la derecha de la ventana
frame_buttons = tk.Frame(ventana, relief= "groove", borderwidth= 2)
frame_buttons.place(relx= 0.95, rely= 0.5, anchor= "e")

dimension_actual = 5 #Dimension del calculo por defecto, despues se cambia

#Funcion para el boton de "Borrar valores"
def borrar():
    for i in range(5):
        entradas_b[i].delete(0, tk.END)
        labels_x[i].config(text="")
        for j in range(5):
            entradas_A[i][j].delete(0, tk.END)

#Funcion para el boton de "Rellenar con 0", aunque las entradas vacias tambien 
#se consideran como cero en los calculos
def ceros():
    for i in range(5):
        if(entradas_b[i].get() == ""):
            entradas_b[i].insert(tk.END, "0")
        for j in range(5):
            if(entradas_A[i][j].get() == ""):
                entradas_A[i][j].insert(tk.END, "0")

#Conjunto de funciones para el calculo de la determinante
def obtener_dimension_actual():
    return dimension_actual

def obtener_matriz_datos(dim):
    """Extrae los valores numericos de la GUI segun la dimension seleccionada"""
    matriz = []
    for i in range(dim):
        fila = []
        for j in range(dim):
            val = entradas_A[i][j].get().strip()
            fila.append(float(val) if val else 0.0)
        matriz.append(fila)
    return matriz

def calcular_det_recursivo(m):
    """Calcula el determinante de una matriz cuadrada de cualquier tamanio"""
    if len(m) == 1:
        return m[0][0]
    if len(m) == 2:
        return m[0][0]*m[1][1] - m[0][1]*m[1][0]
    det = 0
    for c in range(len(m)):
        submatriz = [fila[:c] + fila[c+1:] for fila in m[1:]]
        det += ((-1) ** c) * m[0][c] * calcular_det_recursivo(submatriz)
    return det

def evento_calcular_determinante():
    try:
        # Asumiendo una dimension activa (p. ej. 3 para 3x3)
        dim = obtener_dimension_actual() 
        A = obtener_matriz_datos(dim)
        res = calcular_det_recursivo(A)
        # Muestra el resultado formateado a 2 decimales
        label_det.config(text= f"{res:.2f}")
    except ValueError:
        label_notdigit.config(text="Asegurate de completar los campos con numeros validos.")
        

#Conjunto de funciones para el calculo del sistema de 
#ecuaciones lineales con la regla de Cramer
def obtener_vector_b(dim):
    """Extrae el vector b desde la GUI segun la dimension seleccionada"""
    b = []
    for i in range(dim):
        val = entradas_b[i].get().strip()
        b.append(float(val) if val else 0.0)
    return b

def calcular_solucion():
    try:
        dim = obtener_dimension_actual()
        A = obtener_matriz_datos(dim)
        b = obtener_vector_b(dim)
        #1. Determinante principal
        det_A = calcular_det_recursivo(A)
        #Actualizar el Label del determinante principal en la GUI
        label_det.config(text=f"{det_A:.2f}")
        #Validar caso especial: Sistema no determinado / Sin solucion unica
        #usamos el |Det(A)|<1e-9 porque la aritmetica de punto flotante no es precisa del todo
        #y con esto evitamos que una matriz sin solucion pase por una que si la tiene 
        if abs(det_A) < 1e-9:
            label_notdigit.config(text="El det(A) es 0. El sistema no tiene solucion o no es unica.")
            for i in range(5):
                labels_x[i].config(text="")
            return
        label_notdigit.config(text="")
        #2. Regla de Cramer: reemplazar cada columna por el vector b
        for j in range(dim):
            #Copia profunda de A para no alterar la matriz original
            A_j = copy.deepcopy(A)
            for i in range(dim):
                A_j[i][j] = b[i]
                
            det_A_j = calcular_det_recursivo(A_j)
            x_j = det_A_j / det_A
            
            #Mostrar resultado en el Label correspondiente de la GUI
            labels_x[j].config(text=f"{x_j:.3f}")
        #Limpiar los labels de x sobrantes (si dim < 5)
        for k in range(dim, 5):
            labels_x[k].config(text="")
    except ValueError:
        label_notdigit.config(text="Asegurate de completar los campos con numeros validos.")

#Extension de la funcion 'pressed'
def actualizar_interfaz_dimension():
    dim = obtener_dimension_actual()
    #Recorremos todas las filas y columnas posibles (hasta 5x5)
    for i in range(5):
        #Habilitar / Deshabilitar vector b y vector x
        if i < dim:
            entradas_b[i].config(state="normal", bg="white")
            labels_x[i].config(bg= "white")
        else:
            entradas_b[i].config(state="disabled", disabledbackground="#d9d9d9")
            labels_x[i].config(bg= "#d9d9d9")
        for j in range(5):
            #Habilitar / Deshabilitar elementos de la matriz A
            if i < dim and j < dim:
                entradas_A[i][j].config(state="normal", bg="white")
            else:
                entradas_A[i][j].config(
                    state="disabled", 
                    disabledbackground="#d9d9d9"  # Color gris mas oscuro
                )

#Boton "Borrar valores"
button_delete = tk.Button(frame_buttons, text= "Borrar valores", font= ("times new roman", 8),command= borrar
                          ).pack(padx=2, pady= 5)
#Boton "Rellenar con 0"
button_ceros = tk.Button(frame_buttons, text= "Rellenar con 0", font= ("times new roman", 8), command= ceros
                         ).pack(padx= 2, pady= 5)
#Boton para resolver el sistema de ecuaciones
button_sist = tk.Button(frame_buttons, text= "Calcular solucion x", font= ("times new roman", 8), command= calcular_solucion
                        ).pack(padx= 2, pady= 5)
#Boton para calcular la determinante
button_det = tk.Button(frame_buttons, text="Calcular det.", font=("times new roman", 8), command=evento_calcular_determinante
                       ).pack(padx=2, pady=5)
#Cartel extra
tk.Label(frame_buttons, text= "Determinante:", font= ("times new roman", 8)).pack(padx=2, pady= 5)
#Cartel que muestra la det. calculada
label_det = tk.Label(frame_buttons, text="", relief="ridge", font=("times new roman", 8), borderwidth=2, width=8)
label_det.pack(padx=2, pady=5)


#Frame para la seleccion de dimensiones de la matriz y vectores, ubicado a la izquierda
frame_dimensions = tk.Frame(ventana, relief = "groove", borderwidth= 2)
frame_dimensions.place(relx= 0.05, rely= 0.5, anchor= "w")

tk.Label(frame_dimensions, text= "Dimensiones: ", font= ("times new roman", 8)
         ).pack(padx= 2, pady= 5)

#Lista para los botones que seleccionan la dimension con la que se trabaja
dimensions = []

#Funcion para recolorear los widgets y cambiar los calculos al cambiar la dimension
def pressed(event,dim):
    global dimension_actual
    dimension_actual = dim
    for i in range(4):
        dimensions[i].config(background= "white")
    event.widget.config(background= "grey")
    #Actualizamos el estado visual de los Entrys de la matriz A y el vector b
    actualizar_interfaz_dimension()

for i in range(4):
    dimensions.append(tk.Button(frame_dimensions, text= f"{i+2} x {i+2}", font= ("times new roman", 8), 
    relief= "sunken", background= "white"))
    #Debemos asignar la funcion al boton como 'bind' para que nos permita 
    #ver cual boton colorear al actualizar la dimension
    dimensions[i].bind("<Button-1>", lambda event, dim=i+2: pressed(event,dim))
    dimensions[i].pack(padx= 2, pady= 2)
    if (i==3):
        #La dimension elegida por defecto es de 5x5
        dimensions[i].config(background= "grey")


#Finalmente...
ventana.mainloop()