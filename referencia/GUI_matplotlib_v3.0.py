from tkinter import ttk
import tkinter as tk
import serial
import threading
import matplotlib
import time
matplotlib.use("TkAgg")
#from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from serial.tools import list_ports
import matplotlib.animation as animation
import matplotlib.pyplot as plt
from matplotlib import style
style.use('ggplot')

#Creo archivo log con fecha y hora por titulo
dia = time.strftime("%d")
mes = time.strftime("%m")
year= time.strftime("%Y")
hora= time.strftime("%H")
minuto= time.strftime("%M")
segundo= time.strftime("%S")
nombre = ('log_{}_{}_{}_{}_{}_{}.txt').format(dia,mes,year,hora,minuto,segundo)
log_txt=open(nombre,"w")

#Creo la ventana principal
app = tk.Tk()
app.resizable(width=True, height=True)
app.title("DosiApp")
app.geometry('900x700')



#Etiqueta comando
lbl = tk.Label(app, text="Command")
lbl.place(relx=0.71,rely=0.585)
#Etiqueta puerto
lbl3=tk.Label(app,text='No port selected')
lbl3.place(relx=0.79,rely=0.70)
#Entrada de texto
txt = tk.Entry(app,width=10)
txt.place(relx=0.79,rely=0.585)
#Boton autoscroll
app.CheckVar = tk.BooleanVar(app)
auto_scroll=tk.Checkbutton(app,text='Autoscroll',variable=app.CheckVar,onvalue=1,offvalue=0,height=6,width = 6)
auto_scroll.place(relx=0.79,rely=0.76)

#Boton sensor1 
CheckVar_A = tk.BooleanVar(app)
DAC_A=tk.Checkbutton(app,text='Plot A',variable=CheckVar_A,onvalue=1,offvalue=0)
DAC_A.place(relx=0.71,rely=0.84)
#Boton sensor2
CheckVar_B = tk.BooleanVar(app)
DAC_B=tk.Checkbutton(app,text='Plot B',variable=CheckVar_B,onvalue=1,offvalue=0)
DAC_B.place(relx=0.87,rely=0.84)


# create a Frame for the Text and Scrollbar
txt_frm = tk.Frame(app, width=600, height=280)
txt_frm.pack(fill="both", expand=True)
txt_frm.place(relx=0.01,rely=0.585, relwidth=0.68, relheight=0.4)
# ensure a consistent GUI size
txt_frm.grid_propagate(False)
# implement stretchability
txt_frm.grid_rowconfigure(0, weight=1)
txt_frm.grid_columnconfigure(0, weight=1)
# create a Text widget
cmd = tk.Text(txt_frm, borderwidth=3, relief="sunken")
cmd.config(font=("consolas", 11), undo=True, wrap='none')
cmd.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

scrollbX = tk.Scrollbar(txt_frm, orient="horizontal",command=cmd.xview)
scrollbX.grid(row=1, column=0, sticky='nsew')

# create a Scrollbar and associate it with txt (Y)
scrollbY = tk.Scrollbar(txt_frm, command=cmd.yview)
scrollbY.grid(row=0, column=1, sticky='nsew')

scrollbX.config(command=cmd.xview)
scrollbY.config(command=cmd.yview)

#Frame para las graficas
graf_frm = tk.Frame(app, width=880, height=800)
graf_frm.pack(fill="both", expand=True)
graf_frm.place(relx=0.01,rely=0.01, relwidth=0.98, relheight=0.55)

#notebook para las pestañas
graf = ttk.Notebook(graf_frm)

graf_a = ttk.Frame(graf)
graf.add(graf_a, text='A')
graf.pack(expand=1, fill='both')
figA = plt.Figure(figsize=(14.6, 6.2), dpi=60)
canvasA = FigureCanvasTkAgg(figA, master=graf_a)  # A tk.DrawingArea.
canvasA.draw()
canvasA.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

graf_b = ttk.Frame(graf)
graf.add(graf_b, text='B')
graf.pack(expand=1, fill='both')
figB = plt.Figure(figsize=(14.6, 6.2), dpi=60)
canvasB = FigureCanvasTkAgg(figB, master=graf_b)  # A tk.DrawingArea.
canvasB.draw()
canvasB.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)


#variables globales
error= False
leer=False
conectado=False
cont=False
var=False
stop=False
dato=""
dataXA = [] # Array's para guardar los datos
dataXB = []
dataY = []
activo=""
out=figA

#Definicion del boton ayuda
def clicked2():
#al pulsar ayuda muestra los comandos disponibles
    tk.messagebox.showinfo('Available ports', 
      'Turn on led ------------------------------------  1\n'
      'Turn off led ------------------------------------  0\n'
      'Blink led ----------------------------------------  B\n'
      'Calibrate DAC ---------------------------------  C\n'
      'Measure all channels ------------------------  M\n'
      'Measure one channel ------------------------  m\n'
      'Measure with DC sweep----------------------  b\n'
      'Measure ADC -----------------------------------  *\n'
      'Increase DAC -----------------------------------  + \n'
      'Decrease DAC ----------------------------------   -\n'
      'Selec. DAC A ------------------------------------  A \n'
      'Selec. DAC B ------------------------------------  B')

btn2 = tk.Button(app, text="Help", command=clicked2)
btn2.place(relx=0.87,rely=0.64)


#definicion del boton conectar
def clicked3():

    global conectado
    if (conectado==True): #si esta conectado al pulsar el boton cerramos el puerto
        conectado=False
        btn3.config(text='Conect')
        lbl3.config(text='No port selected')
        pCOM.close()
        log_txt.close()
        
    else: #si no está conectado listamos los puertos y los mostramos en otra ventana
        puertos=list()
        a = list_ports.comports()
        for i in range(len(a)):   
            puertos.append(a[i].device)
        btn3.config(text='Disconnect')
        conect = tk.Tk()
        conect.title("Conect")
        conect.geometry('150x300')
        
        #abrimos puerto seleccionado y se cierra la ventana
        def clicked4():
            global conectado, pCOM, label_btn,lbl3
            puerto=[lista_puertos.get(i) for i in lista_puertos.curselection()]
            lbl3.config(text=puerto)
            conectado=True
            pCOM = serial.Serial((lbl3['text']),baudrate=115200)
            conect.destroy()
            
        btn4 = tk.Button(conect, text="OK", command=clicked4,height=1,width = 5)
        btn4.place(x=50,y=250)
        lbl2=tk.Label(conect,text="Available ports:")
        lbl2.place(x=10,y=10)
        lista_puertos= tk.Listbox(conect)
        lista_puertos.place(x=10,y=30)
        lista_puertos.insert(0,*puertos)
    
  
btn3 = tk.Button(app, text='Conect', command=clicked3)
btn3.place(relx=0.75,rely=0.64)


#Funcion leer lineas 
def readLine(ser):
    global  dataX, dataY, cont, var
    str = ""
    while 1:
        ch = ser.read().decode('ASCII')
        if(ch == '\n'): #si el dato leido es \n devuelve el dato
            if (var==True):
                cont=True
            var=True
            break
        str += ch
            
    return str

#Funcion para leer de forma contina con hilo
def read_from_port(ser):
    ser.flushInput() #limpiamos el buffer
    ser.flushOutput()
    global leer,dataY,dataXA,dataXB,dato,cont,error
    while leer:
        if stop:
            break
        dato = readLine(pCOM)
        #print(dato)
        if (cont==True): #leemos para representar la grafica
            dataY.append(int(dato[0:5]))
            dataXA.append(int(dato[12:17]))
            dataXB.append(int(dato[18:23]))
  
        cmd.insert(tk.END,dato) #presentamos los datos por pantalla
        log_txt.write(dato)
        log_txt.write('\n')
        if (error==True):
            cmd.insert(tk.END,'\t')
            cmd.insert(tk.END,"Warning")
            error=False
        cmd.insert(tk.END,'\n')
        if (app.CheckVar.get()==1): #comprobamos el autoscroll
            cmd.see(tk.END)
    
def medida_continua():
    global leer,cont,dato,thread1,var,stop, dataY,dataXA,dataXB
    if (leer): #Si esta leyendo 
         stop=True
         leer = False                
    else:       #Si se pide que empiece a leer se inicializan todas la variables
        stop=False
        leer = True
        cont=False
        var=False
        dato=""
        dataXA = [] 
        dataXB = []
        dataY = []
        thread1.start()
            
#Boton enviar
def clicked5():
    global leer,cont,dato,pCOM,thread1,conectado,var,stop, dataY,dataXA,dataXB
    thread1 = threading.Thread(target=read_from_port, args=(pCOM,))
    leido=txt.get()
    comando=str.encode(leido)
    txt.delete ( 0, tk.END )
    if (conectado==True):
        if (pCOM.is_open == False):
            pCOM.open()
        
        if (leido=='1'): #Encender leed
            pCOM.write(comando)
            
        elif (leido=='0'): #Apagar led
            pCOM.write(comando)
            
        elif (leido=='B'): #Blink led
            pCOM.write(comando)
            
        elif (leido=='C'): #Calibrar DAC
            pCOM.write(comando)
            
        elif (leido=='M'): #Medir todos los canales
            pCOM.write(comando)
            medida_continua()
                
        elif (leido=='m'): #Medir un canal
            pCOM.write(comando)
            dato=readLine(pCOM)
            cmd.insert(tk.END,dato)
            cmd.insert(tk.END,'\n')
            if (app.CheckVar.get()==1):
                cmd.see(tk.END)
                
        elif (leido=='b'): #Medida continua con barrido en DC
            pCOM.write(comando)
            medida_continua()

                
        elif (leido=='*'): #Medir ADC
            pCOM.write(comando)
            dato=readLine(pCOM)
            cmd.insert(tk.END,dato)
            cmd.insert(tk.END,'\n')
            if (app.CheckVar.get()==1):
                cmd.see(tk.END)
                
        elif (leido=='+'): #Incrementar DAC
            
            pCOM.write(comando)
            dato=readLine(pCOM)
            cmd.insert(tk.END,dato)
            cmd.insert(tk.END,'\n')
            if (app.CheckVar.get()==1):
                cmd.see(tk.END)
                
        elif (leido=='-'): #Decrementar DAC
            
            pCOM.write(comando)
            dato=readLine(pCOM)
            cmd.insert(tk.END,dato)
            cmd.insert(tk.END,'\n')
            if (app.CheckVar.get()==1):
                cmd.see(tk.END)
                
        elif (leido=='A'): #Seleccionar DAC A
            pCOM.write(comando)
            dato=readLine(pCOM)
            cmd.insert(tk.END,dato)
            cmd.insert(tk.END,'\n')
            if (app.CheckVar.get()==1):
                cmd.see(tk.END)
        elif (leido=='B'): #Seleccionar DAC B
            pCOM.write(comando)
            dato=readLine(pCOM)
            cmd.insert(tk.END,dato)
            cmd.insert(tk.END,'\n')
            if (app.CheckVar.get()==1):
                cmd.see(tk.END)
        else: #si el comando enviado no es ninguno de los disponibles lo indicamos por pantalla
            cmd.insert(tk.END,'Command not available')
            cmd.insert(tk.END,'\n')
            if (app.CheckVar.get()==1):
                cmd.see(tk.END)
    else:
        cmd.insert(tk.END,'Not connected \n')
    
btn5 = tk.Button(app, text="Send", command=clicked5)
btn5.place(relx=0.90,rely=0.582)

def animate(i): #funcion para pintar las graficas
    global dataXA,dataY,dataXB,error,dataXC,dataXD,dataXE,dataXF,dataXG,dataXH
    #compruebo que no hay errores en el tamaño de los vectores
    graf_act()
    if len(dataY)!=len(dataXA) or len(dataY)!=len(dataXB):
        error=True
        if len(dataY)>len(dataXA):
            print("Perdida de dato en XA")
            aux= ([len (dataXA)-1] + [len (dataXA)-2]) /2
            dataXA.append(aux)
        elif len(dataY)>len(dataXB):
            print("Perdida de dato en XB")
            aux= ([len (dataXB)-1] + [len (dataXB)-2]) /2
            dataXB.append(aux)
        elif len(dataY)<len(dataXA) or len(dataY)<len(dataXB):
            print("Perdida de dato en Y")
            aux= [len (dataY)-1]
            dataY.append(aux+1)
            
    figA.clear()    
    figB.clear() 
    
    if (CheckVar_A.get()==1):
       ax=figA.subplots(1, sharex=True, sharey=True, gridspec_kw={'hspace': 0.1})
       ax.clear()
       ax.set(xlabel='Time(s)',ylabel='ADC A')
       ax.plot(dataY,dataXA,'ro')       
    if (CheckVar_B.get()==1):
       bx=figB.subplots(1, sharex=True, sharey=True, gridspec_kw={'hspace': 0.1})
       bx.clear()
       bx.set(xlabel='Time(s)',ylabel='ADC B')
       bx.plot(dataY,dataXB,'ro')



#boton clear all
def clicked6():
    global dataXA,dataXB,dataXC,dataXD,dataXE,dataXF,dataXG,dataXH,dataY
    cmd.delete('1.0', tk.END)
    figA.clear()    
    figB.clear() 
    dataXA=[]
    dataXB=[]
    dataY=[]

btn6 = tk.Button(app, text="Clear all", command=clicked6)
btn6.place(relx=0.87,rely=0.755)

def select_all(event=None):
    cmd.tag_add('sel', '1.0', 'end')
    return "break"

cmd.bind('<Control-A>', select_all)
cmd.bind('<Control-a>', select_all)

def graf_act():
    global out
    activo=graf.select()
    aux= activo[len (activo)-1]  

    if aux=='e':
        out=figA
    if aux=='2':
        out=figB
    return out

#boton select all
def clicked7():
    select_all()

btn7 = tk.Button(app, text="Select all", command=clicked7)
btn7.place(relx=0.725,rely=0.755)

#llamada a refrescar la grafica cada segundo

ani = animation.FuncAnimation(out, animate, interval=1000)

app.mainloop()