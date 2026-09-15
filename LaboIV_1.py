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
                entradas_A.append(tk.Entry(frame_matrix, width = 3
                        ).grid(row= 2+i, column= j))
    if(i>0):
        entradas_b.append(tk.Entry(frame_matrix, width= 3
                ).grid(row= 2+i, column= 6))
    
                
'''Las entradas se crean de izquierda a derecha, desde la primera fila, osea, que
si queres acceder a la entry de la 3ra fila (de la matriz, no de la grid) y 2da columna
tendrias que acceder a entradas[(3-1)x5 + 2 -1]. El menos 1 es porque los indices empiezan desde el 0.

Olvide mencionar que, decidi que nuestra matriz tenga un alcance de hasta 5x5. Si queres lo podemos
reducir a 4x4 que seria lo minimo necesario.
'''
        






ventana.mainloop()