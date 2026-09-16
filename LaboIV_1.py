import tkinter as tk

#URL del repositorio de github: https://github.com/Genaro-P/LaboIV_1--Alonso_Genaro
#Integrantes: Alonso Giambelluca, Perez Genaro.

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

frame_matrix = tk.Frame(ventana, relief= "solid", borderwidth= 2)
frame_matrix.place(relx= 0.5, rely= 0, anchor= "n")

#Voy a hacer el grid principal dentro del frame 1, que contendra todo el tema de la matriz
label_main = tk.Label(frame_matrix, text= "A.x = b", font= ("times new roman", 12))
label_main.grid(row=0, column=0, columnspan= 10)

#No es necesario inicializar variables para ubicar widgets sencillos
tk.Label(frame_matrix, text= "Matriz A", font= ("times new roman", 10)).grid(row=1,column=0, columnspan=6,padx= 50)
tk.Label(frame_matrix, text= "Vector b", font= ("times new roman", 10)).grid(row=1, column=6)
tk.Label(frame_matrix, text= "Vector x", font= ("times new roman", 10)).grid(row=1, column=7)

'''Para crear las entrys, puedo hacer una lista que contenga cada variable e identificarla 
con el indice para usar get() cada vez que sea necesario.
Estaria util hacer que sea una lista bidimensional para usar dos indices enves de uno,
pero no creo que sea posible.
'''

#Lista de widgets de tipo Entrada:
entradas_A = [] #Entradas de la matriz A
entradas_b = [] #Creo que queda claro

'''
Esta funcion se la puede asignar a cada entrada para que se ejecute al suceder algun evento,
el evento en cuestion aca es el '<FocusOut>' que es cada vez que el usuario sale de la entrada, osea,
cuando con el mouse selecciona otra cosa y deja de escribir ahi.

Despues, podriamos hacer que esta misma funcion haga aparecer un carte que diga 
"NO PONGAS LETRAS HIJO DE ****" o algo asi
'''

def digit(event):
    try:
        int(event.widget.get().strip()) #El metodo .strip() remueve los espacios del string de la entrada
    except:
        event.widget.delete(0, tk.END)
        event.widget.insert(tk.END, "0")

for i in range(6):
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
                entradas_A.append(tk.Entry(frame_matrix, width = 4))
                #Aca ubico la entrada mas reciente en el grid, si hago las dos
                #cosas en la misma linea, la lista obtendra un objeto tipo None
                entradas_A[len(entradas_A)-1].grid(row= 2+i, column= j, padx= 2, pady= 2)
                entradas_A[len(entradas_A)-1].bind("<FocusOut>", digit)
    if(i>0):
        entradas_b.append(tk.Entry(frame_matrix, width= 4))
        entradas_b[len(entradas_b)-1].grid(row= 2+i, column= 6, padx= 2, pady= 2)
        entradas_b[len(entradas_b)-1].bind("<FocusOut>", digit)
    
                
'''Las entradas se crean de izquierda a derecha, desde la primera fila, osea, que
si queres acceder a la entry de la 3ra fila (de la matriz, no de la grid) y 2da columna
tendrias que acceder a entradas[(3-1)x5 + 2 -1]. El menos 1 es porque los indices empiezan desde el 0.
3-1 y 2-1 reflejan los valores reales que tomarian 'i' y 'j'.

Olvide mencionar que, decidi que nuestra matriz tenga un alcance de hasta 5x5. Si queres lo podemos
reducir a 4x4 que seria lo minimo necesario.
'''
#Investiguemos como borrar los valores de las entradas

#Este frame tendria todos los botones de abajo, para calcular cosas y borrar valores
frame_buttons = tk.Frame(ventana, relief= "solid", borderwidth= 2)
frame_buttons.place(relx= 0.95, rely= 0.5, anchor= "e")

def borrar():
    for i in range(5):
        entradas_b[i].delete(0, tk.END)
        for j in range(5):
            entradas_A[i*5 + j].delete(0, tk.END)


button_delete = tk.Button(frame_buttons, text= "Borrar valores", command= borrar
                          ).pack(padx=2, pady= 5)
button_det = tk.Button(frame_buttons, text= "Calcular det."
                       ).pack(padx= 2, pady= 5)
button_sist = tk.Button(frame_buttons, text= "Calcular solucion x"
                        ).pack(padx= 2, pady= 5)
tk.Label(frame_buttons, text= "Determinante:").pack(padx=2, pady= 5)
label_det = tk.Label(frame_buttons, text= "", relief= "ridge", borderwidth= 2, width= 8
                     ).pack(padx= 2, pady= 5)







ventana.mainloop()