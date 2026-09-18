import tkinter as tk

#URL del repositorio de github: https://github.com/Genaro-P/LaboIV_1--Alonso_Genaro
#Integrantes: Giuliano Alonso Giambelluca, Perez Genaro.

ventana = tk.Tk()
ventana.title("Calculadora de determinantes/Sistemas lineales")
ventana.geometry("600x300")

'''
Los frames son widgets que pueden contener otros widgets, separando los que estan
dentro del widget padre (ventana) y los posicionamos con .place().
Debido a que dentro de un mismo widget no podemos usar .grid() para algunos
widgets y .pack() para otros al mismo tiempo, pero si se puede dentro de widgets
spearados. 
Ademas, el .place() nos da un control mas versatil para el posicionamiento, 
siempre que no intentemos redimensionar el widget padre, ya que sino se hace un lio.
'''

frame_matrix = tk.Frame(ventana, relief= "groove", borderwidth= 2)
frame_matrix.place(relx= 0.5, rely= 0.4, anchor= "center")

#Voy a hacer el grid principal dentro del frame 1, que contendra todo el tema de la matriz
tk.Label(frame_matrix, text= "A.x = b", font= ("times new roman", 12)).grid(row=0, column=0, columnspan= 10)

#No es necesario inicializar variables para ubicar widgets sencillos
tk.Label(frame_matrix, text= "Matriz A", font= ("times new roman", 10)).grid(row=1,column=0, columnspan=6,padx= 50)
tk.Label(frame_matrix, text= "Vector b", font= ("times new roman", 10)).grid(row=1, column=6)
tk.Label(frame_matrix, text= "Vector x", font= ("times new roman", 10)).grid(row=1, column=7)


'''
Para crear las entrys, puedo hacer una lista que contenga cada variable e identificarla 
con el indice para usar get() cada vez que sea necesario.
Estaria util hacer que sea una lista bidimensional para usar dos indices enves de uno,
pero no creo que sea posible.
'''


'''
Esta funcion se la puede asignar a cada entrada para que se ejecute al suceder algun evento,
el evento en cuestion aca es el '<FocusOut>' que es cada vez que el usuario sale de la entrada, osea,
cuando con el mouse selecciona otra cosa y deja de escribir ahi.

Despues, podriamos hacer que esta misma funcion haga aparecer un carte que diga 
"NO PONGAS LETRAS HIJO DE ****" o algo asi
'''

label_notdigit = tk.Label(ventana, text= "", font= ("times new roman", 12))
label_notdigit.pack(anchor= "s", side= "bottom")
def digit(event):
    try:
        event.widget.get().strip() #El metodo .strip() remueve los espacios del string de la entrada
    except:
        if(event.widget.get().strip() != ""):
            label_notdigit.config(text= "Por favor, no ingreses letras.")
        event.widget.delete(0, tk.END)
    else:
        label_notdigit.config(text= "")

#Lista de widgets de tipo Entrada:
entradas_A = [] #Entradas de la matriz A
entradas_b = [] #Creo que queda claro
labels_x = [] #Carteles para cada resultado de x 

for i in range(6):
    if(i>0):
        entradas_A.append([]) #Creo una lista nueva en cada componente, haciendola una lista bidimensional
        entradas_b.append(tk.Entry(frame_matrix, width= 6))
        entradas_b[i-1].grid(row= 2+i, column= 6, padx= 12, pady= 2)
        entradas_b[i-1].bind("<KeyRelease>", digit)
        entradas_b[i-1].bind("<FocusOut>", digit)
        labels_x.append(tk.Label(frame_matrix, text= "", width= 6, relief= "ridge"))
        labels_x[i-1].grid(row= 2+i, column= 7, padx= 2, pady= 2)
    for j in range(6):
        if((i==0) != (j==0)): #Esto es, basicamente, un XOR
            if(j!=0):
                tk.Label(frame_matrix, text= j-1, font= ("times new roman", 8)
                         ).grid(row= 2+i, column=j)
            else:
                tk.Label(frame_matrix, text= i-1, font= ("times new roman", 8)
                         ).grid(row= 2+i, column=j)
        else:
            if(i==0 and j==0):
                tk.Label(frame_matrix, text= "", font= ("times new roman", 8)
                        ).grid(row= 2+i, column=j)
            else:
                #Aca ingreso a cada nueva entrada en la lista
                entradas_A[i-1].append(tk.Entry(frame_matrix, width = 6))
                #Aca ubico la entrada mas reciente en el grid, si hago las dos
                #cosas en la misma linea, la lista obtendra un objeto tipo None
                entradas_A[i-1][j-1].grid(row= 2+i, column= j, padx= 2, pady= 2)
                entradas_A[i-1][j-1].bind("<KeyRelease>", digit)
                entradas_A[i-1][j-1].bind("<FocusOut>", digit)
    
'''
Ahora la lista para acceder a cada entrada es bidimensional y funciona igual que en C

Olvide mencionar que, decidi que nuestra matriz tenga un alcance de hasta 5x5. Si queres lo podemos
reducir a 4x4 que seria lo minimo necesario.
'''
dimension_actual = 2 

def obtener_dimension_actual():
    return dimension_actual
#Investiguemos como borrar los valores de las entradas

#Este frame tendria todos los botones de abajo, para calcular cosas y borrar valores
frame_buttons = tk.Frame(ventana, relief= "groove", borderwidth= 2)
frame_buttons.place(relx= 1, rely= 0.5, anchor= "e")

def borrar():
    for i in range(5):
        entradas_b[i].delete(0, tk.END)
        for j in range(5):
            entradas_A[i][j].delete(0, tk.END)

# --- Lógica Matemática (Ejemplo recursivo o por cofactores) ---
def obtener_matriz_datos(dim):
    """Extrae los valores numéricos de la GUI según la dimensión seleccionada"""
    matriz = []
    for i in range(dim):
        fila = []
        for j in range(dim):
            val = entradas_A[i][j].get().strip()
            fila.append(float(val) if val else 0.0)
        matriz.append(fila)
    return matriz

def calcular_det_recursivo(m):
    """Calcula el determinante de una matriz cuadrada de cualquier tamaño"""
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
        # Asumiendo una dimensión activa (p. ej. 3 para 3x3)
        dim = obtener_dimension_actual() 
        A = obtener_matriz_datos(dim)
        res = calcular_det_recursivo(A)
        
        # Muestra el resultado formateado a 2 decimales
        label_det.config(text=f"{res:.2f}")
    except ValueError:
        label_notdigit.config(text="Asegurate de completar los campos con números válidos.")
        


button_delete = tk.Button(frame_buttons, text= "Borrar valores", font= ("times new roman", 8),command= borrar
                          ).pack(padx=2, pady= 5)
button_sist = tk.Button(frame_buttons, text= "Calcular solucion x", font= ("times new roman", 8)
                        ).pack(padx= 2, pady= 5)
#button_det = tk.Button(frame_buttons, text= "Calcular det.", font= ("times new roman", 8)
#                       ).pack(padx= 2, pady= 5)
tk.Label(frame_buttons, text= "Determinante:", font= ("times new roman", 8)).pack(padx=2, pady= 5)
#label_det = tk.Label(frame_buttons, text= "", relief= "ridge", font= ("times new roman", 8), borderwidth= 2, width= 8
#                     ).pack(padx= 2, pady= 5)

label_det = tk.Label(frame_buttons, text="", relief="ridge", font=("times new roman", 8), borderwidth=2, width=8)
label_det.pack(padx=2, pady=5)

button_det = tk.Button(frame_buttons, text="Calcular det.", font=("times new roman", 8), command=evento_calcular_determinante)
button_det.pack(padx=2, pady=5)

#Frame para la seccion de sleccion de dimensiones de la matriz y vectores

frame_dimensions = tk.Frame(ventana, relief = "groove", borderwidth= 2)
frame_dimensions.place(relx= 0.05, rely= 0.5, anchor= "w")

'''tk.Label(frame_dimensions, text= "Dimensiones: ", font= ("times new roman", 8)
         ).grid(row=0, column=0, columnspan= 2)
for i in range(4):
    tk.Label(frame_dimensions, text= f"{i+2} X {i+2}"
             ).grid(row= i+1, column= 0)'''
             
tk.Label(frame_dimensions, text= "Dimensiones: ", font= ("times new roman", 8)
         ).pack(padx= 2, pady= 5)
dimensions = []
def pressed(event,dim):
    global dimension_actual
    dimension_actual = dim
    
    for i in range(4):
        dimensions[i].config(background= "white")
    event.widget.config(background= "grey")
for i in range(4):
    dimensions.append(tk.Button(frame_dimensions, text= f"{i+2} x {i+2}", font= ("times new roman", 8), 
    relief= "sunken", background= "white"))
    dimensions[i].bind("<Button-1>", lambda event, dim=i+2: pressed(event,dim))
    dimensions[i].pack(padx= 2, pady= 2)
#







ventana.mainloop()
