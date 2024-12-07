###################         INICIO  
import inspect
import os
from pathlib import Path
  
import mysql.connector                                       # Importo interfaz con mysql      

import tkinter as tk            # Importo tkinter como tk

from tkinter import filedialog

from tkinter.filedialog import asksaveasfile

import openpyxl 

from tkinter import scrolledtext 

from PIL import ImageTk, Image 

from tkinter import ttk

from os.path import exists

from tkcalendar import Calendar

import datetime

directorio_actual= os.path.dirname(__file__)                          # Se define el directorio donde esta guardado el archivo.py
directorio_raiz=os.path.normpath(os.path.split(directorio_actual)[0]) # si los archivos adjuntos van a estar en otra carpeta modificarlo 


raiz = tk.Tk()           #  Tk() esta definido en la bilioteca de tekinter , lo hago sobre tk y lo asigno a raiz
                            # Con esto creo la ventana principal
                            
raiz.title("COLOQUIA")     # Le pongo encabezado COLOQUIA  al cuadro raiz        


menu = tk.Menu()                                #   Creo contenedor de menu 

###########################################################################################################
########################################        FUNCIONES GENERALES         ###############################
###########################################################################################################



#                   (marco_datos,self.datos_demograficos,self.nombres_demograficos) 
def lista_vertical(ventana_origen,lista_valores,lista_nombres):       #lista vertica con nombre valor en cada linea 
        #list_nombres=("NOMBRE","APELLIDO","ESTADO","LOCALIDAD","CP","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")
        #list_indices=(1,2,3,4,5,6,7,8,9,10,11,12)
        nom=[]
        om=[]
        j=0
        for bot in lista_valores:
            nom.append(0)
            om.append(0)    
            om[j]=tk.LabelFrame(ventana_origen,bg=("lavender blush"if j%2==0 else  "azure"))
            om[j].config(width=80, height=1)
            om[j].columnconfigure(0,weight=1)
            om[j].columnconfigure(1,weight=1)
            nom[j]=tk.Label(om[j],text=lista_nombres[j],justify="left",anchor="w",bg=("lavender blush"if j%2==0 else "azure"))                      
            om[j].grid(row=j+3,column=0,columnspan=2)
            nom[j].grid(row=j+3,column=0)
            nom[j]=tk.Label(om[j],text=lista_valores[j],justify="left",anchor="w",bg=("lavender blush"if j%2==0 else "azure"))
            nom[j].grid(row=j+3,column=1)      
            j+=1

#
def funcion_etiquetas(ventana,inicio,fila,*args): ## Crea una fila de etiquetas que comienzan en columna inicio y fila fila       
    s=inicio                                        ## Los nombres de las etiquetas son mayusculas que estan en los arg
    for nombre in args:
        nom=nombre
        ventana.columnconfigure(s,weight=1)
        nombre = tk.Label(ventana,text=nom.upper())
        nombre.grid(row=fila,column=s)
        s+=1
#        
def crear_lista_seleccion(ventana,cursor1,funcion,*args2):       ### Muestra lista seleccionable en el orden de los indices
                                                                    #print(cursor1) con boton seleccionar al principio de la linea
    i=2                                                           # resultados de busqueda sql en cursor1
    boton_n=[]                                                      # comandos de los botones funcion(id)
    prof_n=[]       
    for bd in cursor1:        #bd[0] es el id de la entidad    
        k=0            
        boton_n.append(0)
        prof_n.append(0)
        boton_n[k]=tk.Button(ventana,text="Seleccionar",command= lambda c= bd[0],func=funcion: func(c))
        boton_n[k].grid(row=i,column=k)    # bd[0] elemento 0 de cursor1, llama a funcion con argumento bd[0]        
        for indice in range(1,len(args2)):
            k+=1
            prof_n.append(0)      
            prof_n[k-1] = tk.Label(ventana,text=bd[indice])
            prof_n[k-1].grid(row=i,column=k)                
        i+=1

def pago_profesor(id_tarifa,cantidad_alumnos):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select tarifaProfesor from cuadroTarifario where idTarifa = %a and cantidadAlumnos =%a"%(id_tarifa,cantidad_alumnos) )    ## Consulta sql 
            val=list(cursor1)
            conexion1.close()
            if val==[]:
                pago=0
            else:
                pago=float(val[0][0])
            return pago
    
def seleccionar_fechas(fecha_inicio,fecha_fin,ventana) :   
    def seleccionar_inicio():
        cal = Calendar(ventana, font="Arial 14", selectmode='day', locale='en_US',
                            disabledforeground='red',
                        cursor="hand1",date_pattern ="y-mm-dd")            
        cal.grid(row=2,column=3)
        def tomar_fecha():
            cal.destroy()
            boton.destroy()
            fecha_inicio.set(cal.get_date())
        boton=tk.Button(ventana, text = "Aplicar",command = tomar_fecha)
        boton.grid(row=2,column=2)
    
        
    def seleccionar_fin(): 
        cal = Calendar(ventana, font="Arial 14", selectmode='day', locale='en_US',
                            disabledforeground='red',
                        cursor="hand1",date_pattern ="y-mm-dd")            
        cal.grid(row=2,column=7)
        def tomar_fecha():
            cal.destroy()
            boton.destroy()
            nonlocal fecha_fin
            fecha_fin.set(cal.get_date())
        boton=tk.Button(ventana, text = "Aplicar",command = tomar_fecha)
        boton.grid(row=2,column=6)        
    cartel_inicio=tk.Label(ventana,text="FECHA INICIO")    
    cartel_inicio.grid(row=0, column=0,sticky="nw",padx=10,pady=15)
    cartel_mostrar_inicio= tk.Label(ventana,textvariable=fecha_inicio)
    cartel_mostrar_inicio.grid(row=0, column=1,sticky="nw",padx=10,pady=15)
    bot_seleccionar_inicio=tk.Button(ventana,text="Seleccionar",command=seleccionar_inicio)
    bot_seleccionar_inicio.grid(row=0, column=2,sticky="nw",padx=10,pady=15)
    espacio=tk.Label(ventana,text="                               ")
    espacio.grid(row=0, column=3,sticky="nw",padx=10,pady=15)
    cartel_fin=tk.Label(ventana,text="FECHA FIN")    
    cartel_fin.grid(row=0, column=4,sticky="nw",padx=15,pady=15)
    cartel_mostrar_fin= tk.Label(ventana,textvariable=fecha_fin)
    cartel_mostrar_fin.grid(row=0, column=5,sticky="nw",padx=10,pady=15)
    bot_seleccionar_fin=tk.Button(ventana,text="Seleccionar",command=seleccionar_fin)
    bot_seleccionar_fin.grid(row=0, column=6,sticky="nw",padx=10,pady=15)
    
    
def deseleccionar(lista_botones):
    for bot in lista_botones:
        #if bot!=boton:
        bot.grid_forget()  

def cancelar(marco,bot,cartel):
    cartel.destroy()
    marco.destroy()
    bot.destroy()
    inicio()
            


########################################################################################################################################
###########################################         CLASSES        ####################################################################  ########################################################################################################################################



        # id:  id de la entidad a crear
        # nombre_tabla: nombre de la tabla sql donde estan los datos de la entidad
        # nombre_entidad: nombre que aparece en los titulos de las paginas
        # titulos: vector donde estan los nombres de las columas de las tablas a mostrar
        # columnas: nombre de las columnas de la tabla sql de la entidad
        # alias_columnas: nombre con el que me voy a referir al contenido de las columnas. Lo llamo con self.'alias'
        # columnas_con_dependencias: nombre de las columnas que refieren a otras tablas
        # columnas_depnedientes: nombre de las columnas de las otras tablas que son referidas (foreign keys)
        # columnas_objetivo: columnas que continenen los valores que quiero buscar
        # tablas_dependientes: nombre de las tablas que refieren las dependencias
        # alias_dependientes: nombre que va a referir a la dependencia
        # datos_demograficos: nombres de los valores que se consideran datos demograficos cargados en la forma self.xxx
        # nombres_demograficos: nombre para poner en la lista que muestra los datos demograficos
        # columnas_demograficas: nombre de las columnas que contienen los valores demograficos
        
#################################################      class Entidad_con_direccion    #################################################  
        
class Entidad_con_direccion:
    def __init__(self,id,nombre_tabla,nombre_entidad,carpeta_foto,columnas,alias_columnas,columnas_con_dependencias,columnas_depnedientes,columnas_objetivo,tablas_dependientes,alias_dependientes,datos_demograficos,nombres_demograficos,columnas_demograficas): 
    
        self.id=id
        self.tabla=nombre_tabla
        self.entidad=nombre_entidad
        self.datos_demograficos=datos_demograficos
        self.nombres_demograficos=nombres_demograficos
        self.nombre_id=columnas[0]
        self.columnas_demograficas=columnas_demograficas   
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")        
        cursor1.execute("select * from "+self.tabla+" where "+columnas[0]+" = %s" %self.id)    ## Consulta sql datos entidad id
        datos=list(cursor1)        #Creo lista cursor
        self.carpeta_foto=carpeta_foto
        
        i=0                     #cargo los valores en sus alias
        for a in alias_columnas:      
            carga_columna_tabla=("self."+alias_columnas[i] +" = %r" % datos[0][i] )
            exec(carga_columna_tabla)
            i+=1
        conexion1.close()    
        i=0
                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        for a in columnas_depnedientes:  
            query=("select "+columnas_objetivo[i]+"  from "+self.tabla +" inner join "+tablas_dependientes[i] +" on "+self.tabla+"."+columnas_con_dependencias[i]+" = "+tablas_dependientes[i] +"."+columnas_depnedientes[i]+" where "+columnas[0]+" = " +str(self.id))    ## Consulta sql nombre dependencias  
            cursor1.execute(query)            
            nombre_dep=list(cursor1)
            carga_columna_dependientes=("self."+alias_dependientes[i] +" = %r" % nombre_dep[0][0] )
            exec(carga_columna_dependientes) 
            i+=1
        conexion1.close()
        valores_demograficos=[]
        for a in self.datos_demograficos:       #Calculo los valores de los datos demograficos y los guardo en "valores_demograficos"
            valores_demograficos.append(eval(a )) 
        self.valores_demograficos=valores_demograficos                 

    def mostrar_foto(self,vent,texto):
        foto_frame=tk.LabelFrame(vent,text=texto)             ###   Foto      ###
        foto_frame.config(width=40, height=60)
        #foto_frame.grid(row=1,column=0)
        self.foto_frame=foto_frame
            
        nombre_foto=self.foto
        carpeta_foto=os.path.normpath(self.carpeta_foto)
        if nombre_foto=="--":
            direccion_foto=os.path.normpath(os.path.join(directorio_raiz,carpeta_foto,"Default.jpg")) 
        else:
            direccion_foto=os.path.normpath(os.path.join(os.path.join(directorio_raiz,carpeta_foto,nombre_foto)))
        load = Image.open(direccion_foto)   #Muestro foto                 
        juanjo=load.resize((150,150))
        render = ImageTk.PhotoImage(juanjo)    
        img = tk.Label(foto_frame, image=render)
        img.image = render
        img.grid(row=0,column=0)
        return foto_frame     

    def mostrar_datos(self,vent):
        marco_datos=tk.LabelFrame(vent,text="Datos")           ###  Marco Datos   
        marco_datos.config(width=80, height=10)
        marco_datos.config(padx=10, pady=2)
        lista_vertical(marco_datos,self.valores_demograficos,self.nombres_demograficos)
        return marco_datos 
    
    
    def mostrar(self):            
        vent= tk.Toplevel()                ### Abro nueva ventana
        vent.title("Datos "+self.nombre)          
        vent.state("zoomed")                                          
        self.vent=vent
        texto=self.nombre                      ###  Nombre  
        nombre=tk.Label(vent,text=texto,justify="left",anchor="w")
        nombre.grid(row=1,column=1,columnspan=3)
        nombre.config(font=('Arial', 22))
        nombre.config(width=30,height=5)
        nombre.config(padx=0, pady=10)
        self.vent_nombre=nombre         
        
        foto=self.mostrar_foto(vent,texto)
        foto.grid(row=1,column=0)
        datos=self.mostrar_datos(vent)
        datos.grid(row=3,column=0)
        

        marco_observaciones=tk.LabelFrame(vent,text="Observaciones")           ###  Marco observaciones  
        marco_observaciones.config(width=80, height=10)
        marco_observaciones.config(padx=10, pady=2)
        marco_observaciones.grid(row=4,column=0,columnspan=5)
        observacion=self.observaciones
        if len(observacion)<2:
            observacion="-----"
        observaciones=tk.Label(marco_observaciones,text=self.observaciones)          ###  Observaciones ###
        observaciones.config(width=120, height=5)
        observaciones.grid(row=20,column=0,rowspan=5) 
    
    def lista_vertical_modificar(self,ventana_origen,nombres_combo):
        nom=[]
        om=[]
        nome=[]
        j=0        
        for bot in self.nombres_demograficos:
            nom.append(tk.LabelFrame(ventana_origen))
            om.append(0) 
            nome.append(0)   
            om[j]=tk.LabelFrame(ventana_origen,bg=("lavender blush"if j%2==0 else  "azure"))
            om[j].config(width=80, height=1)
            om[j].columnconfigure(0,weight=1)
            om[j].columnconfigure(1,weight=1)
            nome[j]=tk.Label(om[j],text=self.nombres_demograficos[j],justify="left",anchor="w",bg=("lavender blush"if j%2==0 else "azure"))                      
            om[j].grid(row=j+3,column=0,columnspan=2)
            nome[j].grid(row=j+3,column=0)
            combo=1000
            for k in range(0,len(nombres_combo)):
                if bot in nombres_combo[k][0]:
                    combo=k
            if combo!=1000:    
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")    
                cursor1.execute("select "+nombres_combo[combo][1]+ " from "+nombres_combo[combo][2])
                lista=list(cursor1)
                lista_valores=[l[0] for l in lista]
                nom[j]=ttk.Combobox(om[j], state="readonly",values=lista_valores)
                indice=lista_valores.index((nombres_combo[combo][3]))
                nom[j].current(indice)
                nom[j].grid(row=j+3,column=1)
                combo=1000
                conexion1.close() 
            else:
                if j==(len(self.nombres_demograficos)-1):      # El elemento "Activo" no lo modifico desde aca
                    nom[j]=tk.Label(om[j],justify="left",bg=("white"))            
                    nom[j].configure(text=self.valores_demograficos[j])                        
                    nom[j].grid(row=j+3,column=2)  
                else:
                    nom[j]=tk.Entry(om[j],justify="left",bg=("white"))
                    nom[j].insert(0,self.valores_demograficos[j])                        
                    nom[j].grid(row=j+3,column=2)            
            j+=1               

        def salvar():
            j=0            
            for i in range(0,len(self.valores_demograficos)-1):
                self.valores_demograficos[j] =nom[j].get()
                j+=1            
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")                                                        
            query=("select idLocalidad from localidades where localidad = %a"%self.localidad)           
            cursor1.execute(query)
            self.id_localidad=(list(cursor1))[0][0]             
            i=0
            for m in self.datos_demograficos:                
                query2=0
                if self.datos_demograficos[i]=="self.estado":                  
                    self.estado=nom[i].get()
                    query=("select idEstado from estados where estado = %a"%self.estado)           
                    cursor1.execute(query)                    
                    self.id_estado=(list(cursor1))[0][0]            
                    query2=("update "+self.tabla+" set idEstado =%a where "%self.id_estado+self.nombre_id+" = %a"%self.id)                    
                    cursor1.execute(query2)
                    conexion1.commit()
                elif self.datos_demograficos[i]=="self.localidad":
                    self.localidad=nom[i].get()                                            
                    query=("select idLocalidad from localidades where localidad = %a"%self.localidad)           
                    cursor1.execute(query)
                    self.id_localidad=(list(cursor1))[0][0]     
                    query2=("update "+self.tabla+" set idLocalidad = %a where "%self.id_localidad+self.nombre_id+" = %a" %self.id)
                    cursor1.execute(query2)
                    conexion1.commit()                       
                else:                    
                    query2=("update "+self.tabla+" set "+self.columnas_demograficas[i]+" = %a"%self.valores_demograficos[i]+" where " +self.nombre_id+" = %a" %self.id)
                    
                    cursor1.execute(query2)
                    conexion1.commit()                    
                    pass
                i+=1            
            cursor1.execute("update "+self.tabla+" set idEstado = %a where "%self.id_estado+self.nombre_id+" = %a" %self.id)
            conexion1.commit()             
            cursor1.execute("update "+self.tabla+" set idLocalidad = %a where "%self.id_localidad+self.nombre_id+" = %a" %self.id)
            conexion1.commit()
            conexion1.close()    ## Cierro conexion     
       
        bot_grabar=tk.Button(ventana_origen,text="Grabar",command=lambda:salvar())
        bot_grabar.grid(row=j+4,column=0)        
    
    def modificar(self):                
        vent_modificar= tk.Toplevel()                ### Abro nueva ventana que muestra datos  para modificar
        self.vent_modificar=vent_modificar
        vent_modificar.title("Datos "+self.entidad)
        vent_modificar.state("zoomed")                                                                
        texto="Id "+self.entidad+": "+str(self.id)       ###  Id
        nombre_=tk.Label(vent_modificar,text=texto,justify="left",anchor="w")
        nombre_.grid(row=1,column=2,columnspan=2)
        nombre_.config(font=('Arial', 22))
        nombre_.config(width=30,height=5)
        nombre_.config(padx=0, pady=10)
        
        foto_frame=tk.LabelFrame(vent_modificar,text=texto)             ###   Marco foto      ###
        foto_frame.config(width=40, height=60)
        foto_frame.grid(row=1,column=0,sticky="n")            
        nombre_foto=self.foto
        if nombre_foto=="--":    #Si no hay cargada ninguna foto pongo default
            direccion_foto=os.path.join(directorio_raiz,self.carpeta_foto,"Default.jpg") 
        else:
            direccion_foto=os.path.join(directorio_raiz,self.carpeta_foto,nombre_foto)
        load = Image.open(direccion_foto)   #Muestro foto                      
        
        def administrar_foto(funcion):  ## Funcion para seleccionar y guardar foto             
            if funcion =="seleccionar":    
                file_path = filedialog.askopenfile(parent=vent_modificar) 
                self.foto=file_path
                foto=os.path.basename(file_path.name)
                load = Image.open(self.foto.name)      # Abro foto              
                juanjo=load.resize((200,200))           # Ajusto tamaño
                render = ImageTk.PhotoImage(juanjo)        # Muestro foto
                img = tk.Label(foto_frame, image=render)
                img.image = render
                img.grid(row=0,column=0)         
            
            if funcion=="guardar":
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")                                                        
                query=("update "+self.tabla+" set foto = '"+str(os.path.basename(self.foto.name))+"' where "+self.nombre_id+" =%r"%(self.id))# consulta para guardar valor 0 en
                cursor1.execute(query) 
                conexion1.commit()     ###  Hay que poner esto para que se modifique en la base de datos en la base de datos            
                conexion1.close()    ## Cierro conexion
                #self.direccion_adjunto=os.path.basename(file_path.name)
                carpeta_foto=os.path.normpath(self.carpeta_foto) 
                ruta_origen=os.path.normpath(self.foto.name)
                ruta_destino=os.path.join(directorio_raiz,os.path.normpath(carpeta_foto),os.path.normpath(os.path.basename(self.foto.name)))
                comando='copy "'+ ruta_origen + '" "'+ ruta_destino+'"'
                os.system(comando)
                print("COMANDO ",comando)
                self.foto=os.path.basename(self.foto.name)
                vent_modificar.destroy()                
                self.modificar()                 

        bot_guardar=tk.Button(vent_modificar,text="Guardar foto",command=lambda : administrar_foto("guardar")) #Boton guardar foto
        bot_guardar.grid(row=1,column=0,rowspan=2,sticky="ne",pady=226,padx=60)
        bot_cargar=tk.Button(vent_modificar,text="Cargar foto",command=lambda :administrar_foto("seleccionar"))#Boton seleccionar foto
        bot_cargar.grid(row=1,column=0,rowspan=2,sticky="nw",pady=226,padx=55)      
            
        load = Image.open(direccion_foto)      # Abro foto              
        juanjo=load.resize((200,200))           # Ajusto tamaño
        render = ImageTk.PhotoImage(juanjo)        # Muestro foto
        img = tk.Label(foto_frame, image=render)
        img.image = render
        img.grid(row=0,column=0)     
  
        marco_datos=tk.LabelFrame(vent_modificar,text="Datos")           ###  Marco Datos   
        marco_datos.config(width=80, height=10)
        marco_datos.config(padx=10, pady=2)
        marco_datos.grid(row=2,column=0,rowspan=2,pady=30,padx=20,sticky="nw")        
        
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")    
        cursor1.execute("select estado from estados")
        est=list(cursor1)
        estado=[e[0] for e in est]
            
        cursor1.execute("select localidad from localidades")
        loc=list(cursor1)
        localidad=[q[0] for q in loc] 
        lista_valores=[]
        lista_valores.append(estado)
        lista_valores.append(localidad)    
        
        self.lista_vertical_modificar(marco_datos,(("Estado","estado","estados",self.estado),("Localidad","localidad","localidades",self.localidad)))
        def restablecer_modificar():
            self.vent_modificar.destroy()
            self.modificar()
            
        cancelar_bot=tk.Button(marco_datos,text="Cancelar",command=restablecer_modificar)
        cancelar_bot.grid(row=16, column=1)

       
        marco_observaciones=tk.LabelFrame(vent_modificar,text="Observaciones")           ###  Marco observaciones  
        marco_observaciones.config(width=100, height=9)
        marco_observaciones.grid(row=2,column=2,columnspan=3,pady=135,sticky="Nw",padx=260)
        observacion=self.observaciones
        if len(observacion)<2:
            observacion="-----"
        
        observaciones = tk.Text(marco_observaciones, wrap=tk.WORD,width=40, height=6,font=("Times New Roman", 15))
        observaciones.insert("1.0",self.observaciones) 
        observaciones.grid(row=0,column=0,rowspan=1,columnspan=2)
                
        conexion1.close()    ## Cierro conexion 

        def grabar_observaciones():        
            ingreso =observaciones.get("1.0", "end - 1 chars")        
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")
            query=("update "+self.tabla+"  set observaciones = %a where "%ingreso+self.nombre_id+"=%a"%self.id)            
            cursor1.execute(query)
            conexion1.commit()
            conexion1.close()    ## Cierro conexion                 
            self.observaciones=ingreso
        bot_grab_observaciones=(tk.Button(marco_observaciones,text="Grabar",command=grabar_observaciones))
        bot_grab_observaciones.grid(row=3,column=0)
        cancelar_bot=tk.Button(marco_observaciones,text="Cancelar",command=restablecer_modificar)
        cancelar_bot.grid(row=3, column=1)
        
        
################################################        class Profesor      #########################################################

class Profesor(Entidad_con_direccion):
    def __init__(self,id):
        vent=super().__init__(id,"profesores","profesor","Enlaces_coloquia/Fotos_Prof/",("idProfesor","nombreMateria","programa","activo"),("id","nombre","apellido","id_estado","id_localidad","calle","numero","piso","departamento","codigo_postal","telefono","mail","activo","disponibilidad","anio","cuatrimestre","observaciones","foto"),("idEstado","idLocalidad"),("idEstado","idLocalidad"),("estado","localidad"),("estados","localidades"),("estado","localidad"),("self.nombre","self.apellido","self.estado","self.localidad","self.calle","self.numero","self.piso","self.departamento","self.codigo_postal","self.telefono","self.mail","self.activo"),("Nombre","Apellido","Estado","Localidad","Calle","Numero","Piso","Departamento","Codigo postal","Telefono","Mail","Activo"),("nombreProfesor","apellidoProfesor","idEstado","idLocalidad","calle","numero","piso","departamento","codigoPostal","telefono","mail","activo"))
                        
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        x=cursor1.execute("select nombreMateria  from materias inner join materiasProfesores on materias.idMateria = materiasprofesores.idMateria where materiasprofesores.idProfesor =%d and materiasProfesores.idRelacion = 1 and materiasProfesores.activo=1"%self.id)    ## Consulta sql         
        materias_s=list(cursor1)             # Guardo las materias que puede dictar en materias_si
        materias_si=[]
        materias_si=[g[0] for g in materias_s]
        self.materias_si=materias_si       

        x=cursor1.execute("select nombreMateria  from materias inner join materiasProfesores on materias.idMateria = materiasprofesores.idMateria where materiasprofesores.idProfesor =%d and materiasProfesores.idRelacion = 0 and materiasProfesores.activo=1"%self.id)    ## Consulta sql        
        materias_n=list(cursor1)             # Guardo las materias que no puede dictar en materias_no
        materias_no=[]        
        materias_no=[g[0] for g in materias_n]          
        self.materias_no=materias_no
        conexion1.close()    ## Cierro conexion        
    
    def mostrar(self):
        super().mostrar()
        self.vent.title("Datos "+self.nombre+" "+self.apellido)
        self.vent_nombre.config(text=self.nombre+" "+self.apellido)      
        self.foto_frame.config(text=self.nombre+" "+self.apellido)
        self.vent.title("Datos "+self.nombre+" "+self.apellido)
        
        marco_disponibilidad=tk.LabelFrame(self.vent,text="Disponibilidad")         ### Disponibilidad  
        marco_disponibilidad.config(width=70, height=15)
        marco_disponibilidad.grid(row=1,column=4)
        disponibilidad=self.disponibilidad
        if len(disponibilidad)<2:
            disponibilidad="-----"
        disponib=tk.Label(marco_disponibilidad,text=disponibilidad)
        disponib.config(width=70, height=9)    
        disponib.grid(row=4,column=3)

        
        marco_si=tk.LabelFrame(self.vent,text="Materias que puede dictar")           ###  Marco Materias que si
        marco_si.config(width=80, height=10)
        marco_si.config(padx=10, pady=2)
        marco_si.grid(row=3,column=1)
        j=0                                                                                 ## materias 
        mat=[]        
        for i in self.materias_si: 
            mat.append(0)  
            mat[j]=tk.Label(marco_si,text=self.materias_si[j])
            mat[j].grid(row=j,column=0) 
            j+=1                                                                                   
        if j==0:
            mat=tk.Label(marco_si,text="-----") 
            mat.grid(row=0,column=0)        
                
        marco_no=tk.LabelFrame(self.vent,text="Materias que no puede dictar")           ###  Materias que no   
        marco_no.config(width=80, height=10)
        marco_no.config(padx=10, pady=2)
        marco_no.grid(row=3,column=2)
        j=0                                                                                 ## materias 
        mat=[]
        for i in self.materias_no: 
            mat.append(0)  
            mat[j]=tk.Label(marco_no,text=self.materias_no[j])
            mat[j].grid(row=j,column=0) 
            j+=1                     
        if j==0:
            mat=tk.Label(marco_no,text="-----")
            mat.grid(row=0,column=0)
        

   
    def modificar(self):
        super().modificar()        
                                                                          
        def eliminar_materia(mat):    #Para eliminar la materia le pongo activo =0 en materiasProfesores (anulo esa relacion)
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")
            cursor1.execute("select  idMateria from materias where nombreMateria =%r" %mat) #busco idMateria
            fr=list(cursor1)
            id_mat=fr[0][0]
            cursor1.execute("update materiasProfesores set activo = 0 where idProfesor=%r  and idMateria=%r "%(self.id,id_mat))
            conexion1.commit()
            conexion1.close()    ## Cierro conexion
            self.vent_modificar.destroy()
            modificar_prof(self.id) 
            
        marco_disponibilidad=tk.LabelFrame(self.vent_modificar,text="Disponibilidad")         ### Disponibilidad  
        marco_disponibilidad.config(width=270, height=15)
        marco_disponibilidad.grid(row=1,column=3,columnspan =2,padx=0,sticky="nw")
        disponibilidad=self.disponibilidad
        if len(disponibilidad)<2:               # Si no hay nada cargado muestro ---
            disponibilidad="-----"    
        disponib = tk.Text(marco_disponibilidad, wrap=tk.WORD,width=40, height=8,font=("Times New Roman", 15))
        disponib.insert("1.0",disponibilidad)   
        disponib.grid(row=2,column=0,columnspan=2,sticky="n")
        cartel_anio=tk.Label(marco_disponibilidad,text="Año")
        cartel_anio.grid(column=3,row=2,sticky="n",pady=10)    
        disponib_anio=tk.Entry(marco_disponibilidad,justify="left",bg=("white"),width=4)
        disponib_anio.insert(0,"Año")
        disponib_anio.grid(column=3,row=2,sticky="n",pady=30)
        
        cartel_cuat=tk.Label(marco_disponibilidad,text="Cuatrimestre")
        cartel_cuat.grid(column=3,row=2,sticky="n",pady=70,rowspan=2)    
        disponib_cuat=tk.Entry(marco_disponibilidad,justify="left",bg=("white"),width=1)
        disponib_cuat.insert(0,"Cuatrimestre")
        disponib_cuat.grid(column=3,row=2,sticky="n",pady=90,rowspan=3)      
        
        def grabar_disponibilidad():        
            ingreso=disponib.get("1.0", "end - 1 chars")
            self.disponibilidad =ingreso       
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")
            query=("update profesores set disponibilidad = %a where idProfesor=%a"%(ingreso,self.id))
            cursor1.execute(query)
            conexion1.commit()
            conexion1.close()    ## Cierro conexion
        
        bot_grab_disponibilidad=(tk.Button(marco_disponibilidad,text="Grabar",command=grabar_disponibilidad))
        
        def restablecer_modificar():
            self.vent_modificar.destroy()
            self.modificar()
            
        bot_grab_disponibilidad.grid(row=3,column=0,sticky="N")
        cancelar_bot=tk.Button(marco_disponibilidad,text="Cancelar",command=restablecer_modificar)
        cancelar_bot.grid(row=3, column=1)
        j=0
              
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        x=cursor1.execute("select nombreMateria  from materias where activo =1")    ## Consulta sql para total materias activas

        materias_t=list(cursor1)
        materias_tot=[]
        materias_tot=[h[0] for h in materias_t]
        conexion1.close()
        
                ##### materias_agregar Lista de materias para agregar (son las totales menos la ya seleccionadas)
        materias_agregar= [j for j in materias_tot]
        for a in self.materias_si:
            if a in materias_agregar:
                materias_agregar.remove(a)
        for a in self.materias_no:
            if a in materias_agregar:
                materias_agregar.remove(a)
        m=0        
            
        marco_si=tk.LabelFrame(self.vent_modificar,text="Materias que puede dictar")           ###  Marco Materias que si
        marco_si.config(width=80, height=10)
        marco_si.config(padx=10, pady=2)
        marco_si.grid(row=2,column=2,rowspan=1,pady=60,padx=40,sticky="nw")
        j=0                                                                                 ## materias 
        mat=[]
        bot=[]
    
        for i in self.materias_si:                           #Agrego boton para elimiar materia de la lista (completar funcion)
            mat.append(0)
            bot.append(0)
            bot[j]=tk.Button(marco_si,text="Eliminar", command=lambda z=j:eliminar_materia(self.materias_si[z]))
            bot[j].grid(row=j, column=0)  
            mat[j]=tk.Label(marco_si,text=self.materias_si[j])
            mat[j].grid(row=j,column=1) 
            j+=1                                                                                   
        if j==0:                            # Si no hay ninguna materia que si muestro ----
            mat=tk.Label(marco_si,text="-----") 
            mat.grid(row=0,column=0)              
        
        marco_no=tk.LabelFrame(self.vent_modificar,text="Materias que no puede dictar")           ###  Materias que no   
        marco_no.config(width=80, height=10)
        marco_no.grid(row=2,column=4,rowspan=1,pady=60,padx=220,sticky="nw")
        j=0                                                                                 ## materias 
        r=0
        mat=[]
        bot=[]
        for i in self.materias_no:               #Agrega boton eliminar a cada elemento de la lista materias_no
            mat.append(0)
            bot.append(0)
            bot[j]=tk.Button(marco_no,text="Eliminar", command=lambda z=j:eliminar_materia(self.materias_no[z]))# Cambiar aca y eliminar directo de la bd
            
            bot[j].grid(row=j, column=0)    
            mat[j]=tk.Label(marco_no,text=self.materias_no[j])
            mat[j].grid(row=j,column=1) 
            j+=1                     
        if j==0:                # Si no hay ningun elemento en le lista pone -----
            mat=tk.Label(marco_no,text="-----") 
            mat.grid(row=0,column=0)
        
        agregar_si=tk.Button(marco_si,text="")# Necesito poner boton vacio para agregar materia a la lista que no ya que lo modifico mas adelante
        agregar_si.grid(row=j+1, column=0)
        
        agregar_no=tk.Button(marco_no,text="")# Necesito poner boton vacio para agregar materia a la lista que no ya que lo modifico mas adelante
        agregar_no.grid(row=j+1, column=0)   
        
        n=0
        def agregar_materia(p,ventana):
            def guardar_materia_si(mat):
                    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                    cursor1= conexion1.cursor()
                    cursor1.execute("use test_values")
                    x=cursor1.execute("select  idMateria from materias where nombreMateria =%r" %mat) #busco idMateria
                    fr=list(cursor1)
                    id_mat=fr[0][0]                
                    cursor1.execute("insert into materiasProfesores(idProfesor,idMateria,idRelacion,activo) values(%a,%a,1,1) "%(self.id,id_mat)) 
                    conexion1.commit()
                    conexion1.close()    ## Cierro conexion
                    self.vent_modificar.destroy()
                    modificar_prof(self.id)
                    
            def guardar_materia_no(mat):
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")
                x=cursor1.execute("select  idMateria from materias where nombreMateria =%r" %mat) #busco idMateria
                fr=list(cursor1)
                id_mat=fr[0][0]          
                cursor1.execute("insert into materiasProfesores(idProfesor,idMateria,idRelacion,activo) values(%a,%a,0,1) "%(self.id,id_mat)) 
                conexion1.commit()
                conexion1.close()    ## Cierro conexion
                self.vent_modificar.destroy()
                modificar_prof(self.id)    
                    
            n=1

            combo=ttk.Combobox(ventana, state="readonly",values=materias_agregar) 
            combo.grid(row=0,column=2)
            
            if p==2:                         
                agregar_si.config(text="Guardar",command=lambda:guardar_materia_si (combo.get()))
                cancelar_bot=tk.Button(marco_si,text="Cancelar",command=restablecer_modificar)
                cancelar_bot.grid(row=j+1, column=1)
            
            
            if p==0:                     
                agregar_no.config(text="Guardar",command=lambda:guardar_materia_no (combo.get()))
                cancelar_bot=tk.Button(marco_no,text="Cancelar",command=restablecer_modificar)
                cancelar_bot.grid(row=j+1, column=1)
                
        if n==0:
            agregar_si.config(text="Agregar", command=lambda:agregar_materia(2,marco_si))#Agregar materia_no muestra desplegable a la derecha(column2)
            agregar_si.grid(row=j+1, column=0)                    
        
        if n==0:
            agregar_no.config(text="Agregar", command=lambda:agregar_materia(0,marco_no))#Agregar materia_no muestra desplegable a la derecha(column2)
            agregar_no.grid(row=j+1, column=0)         
        
        
#########################################################   class Escuela   ##########################################################
        
class Escuela(Entidad_con_direccion):
    def __init__(self,id):
        
        vent=super().__init__(id,"escuelas","escuela","Enlaces_coloquia/Fotos_Escuelas/",("idEscuela","nombreMateria","programa","activo"),("id","nombre","id_estado","id_localidad","calle","numero","piso","departamento","codigo_postal","telefono","mail","activo","observaciones","foto"),("idEstado","idLocalidad"),("idEstado","idLocalidad"),("estado","localidad"),("estados","localidades"),("estado","localidad"),("self.nombre","self.estado","self.localidad","self.calle","self.numero","self.piso","self.departamento","self.codigo_postal","self.telefono","self.mail","self.activo"),("Nombre","Estado","Localidad","Calle","Numero","Piso","Departamento","Codigo postal","Telefono","Mail","Activo"),("nombreEscuela","idEstado","idLocalidad","calle","numero","piso","departamento","codigoPostal","telefono","mail","activo"))
        self.apellido=""

####################################################     class Mat    #################################################################

class Mat:
        # id:  id de la entidad a crear
        # nombre_tabla: nombre de la tabla sql donde estan los datos de la entidad
        # titulos: vector donde estan los nombres de las columas de las tablas a mostrar
        # nombre_entidad: nombre que aparece en los titulos de las paginas
        # nombre_adjunto: nombre que aparece en la pantalla del archivo adjunto
        # nombre_id_sql: nombre de la columna 0 de la tabla sql donde se guarda el id de la entidad
        # nombre_mat_sql: nombre de la columna 1 de la tabla sql donde se guarda el nombre de la entidad
        # nombre_direccion_adjunto_sql: nombre de la columna 2 de la tabla sql donde se guarda el adjunto de la entidad
        # direccion_carpeta: direccion de la carpeta donde estan los archivos adjuntos
    def __init__(self,id,nombre_tabla,titulos,nombre_entidad,nombre_adjunto,nombre_id_sql,nombre_mat_sql,nombre_direccion_adjunto_sql,direccion_carpeta):
        self.id=id
        self.titulos=titulos
        self.tabla=nombre_tabla        
        self.nombre_adjunto=nombre_adjunto
        self.entidad=nombre_entidad
        self.nombre_id_sql=nombre_id_sql
        self.nombre_mat_sql=nombre_mat_sql
        self.nombre_direccion_adjunto_sql=nombre_direccion_adjunto_sql
        self.direccion_carpeta = direccion_carpeta              
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        query="select * from "+self.tabla+" where  "+self.nombre_id_sql+" =%a"%(id)
        cursor1.execute(query) 
        lis=list(cursor1)
        cursor1.close()        
        self.id,self.nombre,self.direccion_adjunto,self.activo =lis[0]  # Diferenciar para materias y materiales
        conexion1.close()
           
    def grabar(self):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")                
            query=("update "+self.tabla+" set "+self.nombre_mat_sql+" = %a"%self.nombre+" , "+self.nombre_direccion_adjunto_sql+" = %a"%self.direccion_adjunto+" , activo= %a"%self.activo+"  where  "+self.nombre_id_sql+" =%a "%(self.id ))
            cursor1.execute(query) 
            conexion1.commit()
            conexion1.close() 
       
    def mostrar_mat(self):    
        vent_mat= tk.Toplevel()                ### Abro nueva ventana
        vent_mat.title(self.entidad)
        self.vent_mat=vent_mat
        vent_mat.state("zoomed")            
        nombre_mat=tk.Label(vent_mat,text=self.nombre,justify="left",anchor="w")
        nombre_mat.grid(row=0,column=1,columnspan=1,sticky="nw",padx=20)
        nombre_mat.config(font=('Arial', 22))
        nombre_mat.config(width=20,height=5)
        nombre_mat.config(padx=0, pady=10)
        mat_activo=tk.Label(vent_mat,text="Activo= "+str(self.activo) )
        mat_activo.grid(row=1,column=1,columnspan=1,sticky="nw",padx=20)                
        marco_mat=tk.LabelFrame(vent_mat,text=self.nombre_adjunto)         ### Materia  
        marco_mat.config(width=470, height=550)
        marco_mat.grid(row=0,column=2,columnspan =1,rowspan=2,padx=0,sticky="nwse")
        file_path =os.path.join(directorio_raiz,self.direccion_carpeta ,self.direccion_adjunto)  
        file_exists = exists(file_path)    
        if file_exists:        
            archivo=open(file_path,"r",errors="ignore")
        else: 
            archivo=open(os.path.join(directorio_raiz,self.direccion_carpeta ,"Default.txt") ,"r",errors="ignore")     
        contenido=(archivo.read())
        etiqueta_mat_contenido=tk.Label(marco_mat,text=contenido)
        etiqueta_mat_contenido.grid(sticky="NSWE")
        
    #
    def modificar_mat(self):
        vent_mat_modificacion= tk.Toplevel()           
        vent_mat_modificacion.title(self.entidad)
        vent_mat_modificacion.state("zoomed")
        etiqueta_id_mat=tk.Label(vent_mat_modificacion,text="Id:  %a"%self.id,justify="left",anchor="w")
        etiqueta_id_mat.grid(row=0,column=1,columnspan=1,sticky="nw",padx=0)   
        etiqueta_nombre_mat=tk.Label(vent_mat_modificacion,text="Nombre %a"%self.entidad,justify="left",anchor="w")
        etiqueta_nombre_mat.grid(row=1,column=1,columnspan=1,sticky="nw",padx=0)     
        nombre_mat=tk.Entry(vent_mat_modificacion)
        nombre_mat.insert(0,self.nombre)
        nombre_mat.grid(row=1,column=1,columnspan=1,sticky="nw",padx=50)            
        mat_activo=tk.Label(vent_mat_modificacion,text="Activo= "+str(self.activo) )
        mat_activo.grid(row=2,column=1,columnspan=1,sticky="nw",padx=20)            
        def grabar_nombre_mat():
            self.nombre=nombre_mat.get()
            self.grabar()
        
        bot_nombre_mat_grabar=tk.Button(vent_mat_modificacion,text="Grabar nombre",command=grabar_nombre_mat)
        bot_nombre_mat_grabar.grid(row=1,column=1,columnspan=1,sticky="nw",pady=30)
                
        marco_materia=tk.LabelFrame(vent_mat_modificacion,text=self.nombre_adjunto)         ### Materia  
        marco_materia.config(width=470, height=550)
        marco_materia.grid(row=1,column=2,columnspan =2,rowspan=5,padx=0,sticky="nwse")
        file_path =os.path.join(directorio_raiz,self.direccion_carpeta ,self.direccion_adjunto)      
        file_exists = exists(file_path)        
         
        if file_exists:        
            archivo=open(file_path,"r",errors="ignore")
        else: 
            archivo=open(os.path.join(directorio_raiz,self.direccion_carpeta ,"Default.txt") ,"r",errors="ignore")       
        contenido=(archivo.read())
        etiqueta_mat_contenido=tk.Label(marco_materia,text=contenido)
        etiqueta_mat_contenido.grid(sticky="NSWE") 
        
        def cargar_archivo():
            file_path = filedialog.askopenfile(parent=vent_mat_modificacion,filetypes=[("Text files","*.txt")])         
            arvhivo=open(file_path.name,"r",errors="ignore")        
            contenido=(arvhivo.read())            
            def guardar_programa():
                self.direccion_adjunto=os.path.basename(file_path.name) 
                ruta_origen=os.path.normpath(file_path.name)
                ruta_destino=os.path.join(directorio_raiz,"Enlaces_coloquia\Materiales",os.path.basename(file_path.name))
                comando='copy "'+ ruta_origen + '" "'+ ruta_destino+'"'
                os.system(comando)
                self.grabar()
                vent_mat_modificacion.destroy()
                self.modificar_mat()
            
            bot_grabar=tk.Button(vent_mat_modificacion,text="Guardar "+ self.nombre_adjunto,command=lambda: guardar_programa())
            bot_grabar.grid(row=1,column=1,sticky="NW",pady=90)
            etiqueta_mat_contenido=tk.Label(marco_materia,text=contenido)
            etiqueta_mat_contenido.grid(sticky="NSWE")   
            
            
        bot_cargar=tk.Button(vent_mat_modificacion,text="Cargar "+ self.nombre_adjunto,command=cargar_archivo)
        bot_cargar.grid(row=2,column=1,sticky="NW",pady=50) 
        
        
        

#######################################################     class Materia(Mat)      ################################################

class Materia(Mat):
    def __init__(self,id):
        super().__init__(id,"materias",("Nombre materia","Programa","Activo"),"Materias","Programa","idMateria","nombreMateria","programa",os.path.join(directorio_raiz,"/Enlaces_coloquia/Programas_materias"))

    def agregar(self,vent_mat_modificacion):
        def cambiar_material(id_materiaMaterial):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select materiasMateriales.activo  from materiasMateriales where idMateriaMaterial=%a"%id_materiaMaterial )    ## Consulta sql
            valor=list(cursor1)
            activ=valor[0][0]
            if activ==0:
                nuevo_valor=1
            else:
                nuevo_valor=0
            cursor1.execute("update materiasMateriales set activo =%a   where idMateriaMaterial=%a"%(nuevo_valor,id_materiaMaterial ) )
            conexion1.commit()
            conexion1.close()    ## Cierro conexion
            vent_mat_modificacion.destroy()
            self.modificar_mat()
                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")        
        cursor1.execute("select idMateriaMaterial,materiasMateriales.idMaterial,nombreMaterial,materiasMateriales.activo  from materiasMateriales inner join materiales on materiasMateriales.idMaterial=materiales.idMaterial where materiasMateriales.idMateria=%a and materiasMateriales.activo=1"%self.id )    ## Consulta sql
        
        etiqueta_materiales=tk.LabelFrame(vent_mat_modificacion,text="QUITAR MATERIALES UTILIZADOS EN ESTA MATERIA")
        etiqueta_materiales.grid(row=1,column=6,sticky="w",padx=90)                               
        funcion_etiquetas(etiqueta_materiales,1,1,"id material","nombre material","activo")   
        crear_lista_seleccion(etiqueta_materiales,cursor1,cambiar_material,1,2,3,4) 
        
        conexion1.close()    ## Cierro conexion     
        def grabar(combo_materiales):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select idMaterial from materiasMateriales where idMateria=%a"%self.id)# where activo=1" )    ## Consulta sql
            val=list(cursor1)
            lista=[l[0]for l in val ]
            id_seleccion=(str(combo_materiales.get()))[:2]
            comparacion=int(id_seleccion)
            if comparacion in lista:
                cursor1.execute("update materiasMateriales set activo =1 where idMaterial=%a and idMateria=%a"%(comparacion,self.id))
                conexion1.commit()
            else:
                cursor1.execute("insert into materiasMateriales (idMateria,idmaterial,activo) values(%a,%a,1)"%(self.id,combo_materiales.get()))
                conexion1.commit()
            conexion1.close()
            vent_mat_modificacion.destroy()
            self.modificar_mat()
        def agregar_material(bot_agregar_material):
            bot_agregar_material.config(text="Grabar", command=lambda:grabar(combo_materiales))
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select idMaterial,nombreMaterial from materiales where activo=1")# where activo=1" )    ## Consulta sql
            val=list(cursor1)
            id_materiales=[i[0]for i in val]
            cursor1.execute("select idMaterial from materiasMateriales where idMateria=%a and materiasMateriales.activo=1"%self.id)
            valores=list(cursor1)
            id_materiasMateriales=[i[0]for i in valores]
            id_materiales_agregar=[]
            materiales_agregar=[]
            for elemento in id_materiales:
                if elemento not in id_materiasMateriales:
                    id_materiales_agregar.append(elemento)
            for id in id_materiales_agregar:
                cursor1.execute("select idMaterial,nombreMaterial from materiales where idMaterial=%a"%id)
                val=list(cursor1)
                materiales_agregar.append(val[0])
            conexion1.close()    ## Cierro conexion  
            combo_materiales=ttk.Combobox(vent_mat_modificacion, state="readonly",values=materiales_agregar) 
            combo_materiales.grid(row=3,column=6,sticky="w")
            pass
        bot_agregar_material=tk.Button(vent_mat_modificacion,text="Agrgar material ",command=lambda:agregar_material(bot_agregar_material))
        bot_agregar_material.grid(row=3,column=5,sticky="NW",pady=50)  
        

#######################################################     class Material(Mat)     #################################################   
        
class Material(Mat):
    def __init__(self,id):
        super().__init__(id,"materiales",("Nombre material","Descripcion","Activo"),"Materiales","Descripcion","idMaterial","nombreMaterial","descripcion",os.path.join(directorio_raiz,"Enlaces_coloquia/Fotos_Escuelas"))
        
        

######################################################      class Alumno()      ###################################################
            
class Alumno():
    def __init__(self,id_alumno):
        self.id=id_alumno                      
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        cursor1.execute("select * from alumnos where idMaterial =%a"%id_alumno) 
        lis=list(cursor1)
        conexion1.close()
        self.id,self.nombre,self.direccion,self.activo =lis[0]
        
        def grabar(self):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")
            query="update materiales set nombreMaterial=%a , programa=%a ,activo=%a where idMaterial =%a " %(self.nombre,self.direccion,self.activo,self.id)
            cursor1.execute(query) 
            conexion1.commit()
            conexion1.close()        




################################################         class Tarifas     ################################################ 
    
class Tarifa:
    def __init__(self,id_tarifa):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")        
        cursor1.execute("select * from tarifas where idTarifa = %a"%id_tarifa )    ## Consulta sql 
        val=list(cursor1)
        conexion1.close()
        self.id=val[0][0]
        self.nombre= val[0][1]
        self.descripcion = val[0][2]
        self.tarifa_colegio= val[0][3]
        self.tarifa_materiales= val[0][4]
        self.gasto_materiales= val[0][5]
        self.valor_hora_acompaniamiento=val[0][6]
        self.hora_anterior= val[0][7]
        self.hora_posterior= val[0][8]
        self.valor_hora_asistente= val[0][9]
        self.asistente=val [0][10]
        self.minima_cant_alumnos= val[0][11]
        self.maxima_cant_alumnos= val[0][12]
        self.activo= val[0][13]
        
        
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
        self.pago_profesor_alumnos={}
        self.entrada_pago_profesor_alumnos={}
        for alumnos in range(self.minima_cant_alumnos,self.maxima_cant_alumnos+1):            
            consulta=("select tarifaProfesor from cuadroTarifario where idTarifa = %a and cantidadAlumnos=%a"%(self.id,alumnos) )    ## 
            cursor1.execute(consulta)
            sam=list(cursor1)
            if len(sam):    
                self.pago_profesor_alumnos[alumnos]=sam[0][0]
            else:
                self.pago_profesor_alumnos[alumnos]=0
            valores=0
        conexion1.close() 
        
        
    def mostrar(self):
        vent_mostrar= tk.Toplevel()                ### Abro nueva ventana que muestra datos  para modificar
        self.vent_mostrar=vent_mostrar
        vent_mostrar.title("Tarifa "+str(self.id))
        vent_mostrar.state("zoomed")    

        vent_mostrar.columnconfigure(7,weight=1)    
        cartel_nom_tarif=tk.Label(vent_mostrar,text="Nombre: ")
        cartel_nom_tarif.grid(row=0,column=0)
        nom_terifa=tk.Label(vent_mostrar,text=self.nombre)
        nom_terifa.grid(row=0,column=1)
        etiqueta_tarifas=tk.LabelFrame(vent_mostrar)     
        etiqueta_tarifas.config(width=800, height=100)
        etiqueta_tarifas.config(text="Tarifa por alumno")
        etiqueta_tarifas.grid(row=3,column=0,columnspan=6,rowspan=3,sticky="nwes")
        etiqueta_tarifa_colegio=tk.Label(etiqueta_tarifas,text="Colegio: ")
        etiqueta_tarifa_colegio.grid(row=0,column=0)
        tarifa_colegio=tk.Label(etiqueta_tarifas,text=self.tarifa_colegio)
        tarifa_colegio.grid(row=0,column=1)
        etiqutea_tarifa_materiales=tk.Label(etiqueta_tarifas,text="Materiales: ")
        etiqutea_tarifa_materiales.grid(row=0,column=2)
        tarifa_materiales=tk.Label(etiqueta_tarifas,text=self.tarifa_materiales)
        tarifa_materiales.grid(row=0,column=3)
        etiqueta_gasto_materiales=tk.Label(etiqueta_tarifas,text="Gasto materiales: ")
        etiqueta_gasto_materiales.grid(row=0,column=4)
        gasto_materiales=tk.Label(etiqueta_tarifas,text=self.gasto_materiales)
        gasto_materiales.grid(row=0,column=5)
        etiqueta_asistente=tk.Label(vent_mostrar,text="Asistente: ")
        etiqueta_asistente.grid(row=8,column=0)
        asistente=ttk.Label(vent_mostrar, text= "SI" if self.asistente==1 else "NO")    
        asistente.grid(row=8,column=1)
        if self.asistente==1:
            etiqueta_valor_asistente=tk.Label(vent_mostrar,text="Tarifa asistente: ")
            etiqueta_valor_asistente.grid(row=9,column=0)
            valor_asistente=tk.Label(vent_mostrar,text=self.valor_hora_asistente)
            valor_asistente.grid(row=9,column=1)   
        etiqueta_hora_anterior=tk.Label(vent_mostrar,text="Hora previa: ")
        etiqueta_hora_anterior.grid(row=10,column=0)
        hora_anterior=ttk.Label(vent_mostrar,text="SI" if self.hora_anterior==1 else "NO")
        hora_anterior.grid(row=10,column=1)
        etiqueta_hora_posterior=tk.Label(vent_mostrar,text="Hora posterior: ")
        etiqueta_hora_posterior.grid(row=11,column=0)
        hora_posterior=ttk.Label(vent_mostrar,text="SI" if self.hora_posterior==1 else "NO")    
        hora_posterior.grid(row=11,column=1)
        if self.hora_anterior==1 or self.hora_posterior==1:
            etiqueta_valor_acompaniamiento=tk.Label(vent_mostrar,text="Tarifa acompañamiento: ")
            etiqueta_valor_acompaniamiento.grid(row=12,column=0)
            valor_acompaniamiento=tk.Label(vent_mostrar,text=self.valor_hora_acompaniamiento)
            valor_acompaniamiento.grid(row=12,column=1)
        etiqueta_minimo_alumnos=tk.Label(vent_mostrar,text="Cantidad minima de alumnos: ")
        etiqueta_minimo_alumnos.grid(row=13,column=0)
        minimo_alumnos=tk.Label(vent_mostrar,text=self.minima_cant_alumnos)
        minimo_alumnos.grid(row=13,column=1)        
        etiqueta_maximo_alumnos=tk.Label(vent_mostrar,text="Cantidad maxima de alumnos: ")
        etiqueta_maximo_alumnos.grid(row=14,column=0)
        maximo_alumnos=tk.Label(vent_mostrar,text=self.maxima_cant_alumnos)
        maximo_alumnos.grid(row=14,column=1)      
        cartel_activo=tk.Label(vent_mostrar,text="Activo: ")
        cartel_activo.grid(row=15,column=0)
        activo=ttk.Label(vent_mostrar,text="SI" if self.activo==1 else "NO")     
        activo.grid(row=15,column=1)
        
        cuadro_tarifas=tk.LabelFrame(vent_mostrar)
        cuadro_tarifas.config(width=1200, height=100)
        cuadro_tarifas.config(text="Cuadro resumen")        
        cuadro_tarifas.grid(row=16,column=0,columnspan=8,rowspan=3,sticky="nwes")
        cuadro_tarifas.columnconfigure(0,weight=1)
        cuadro_tarifas.columnconfigure(1,weight=1)
        cuadro_tarifas.columnconfigure(2,weight=1)
        cuadro_tarifas.columnconfigure(3,weight=1)
        cuadro_tarifas.columnconfigure(4,weight=1)
        cuadro_tarifas.columnconfigure(5,weight=1)
        cuadro_tarifas.columnconfigure(6,weight=1)
        cuadro_tarifas.columnconfigure(7,weight=1)
        col=0
        cant_alumnos=tk.Label(cuadro_tarifas,text="Cantidad alumnos")
        cant_alumnos.grid(row=0,column=col)
        col+=1
        tarifa_escuela=tk.Label(cuadro_tarifas,text="Escuela paga")
        tarifa_escuela.grid(row=0,column=col)
        col+=1
        tarifa_profesor=tk.Label(cuadro_tarifas,text="Profesor clase")
        tarifa_profesor.grid(row=0,column=col)
        col+=1
        if self.hora_anterior==1 or self.hora_posterior==1:
            prof_acompaniamiento=tk.Label(cuadro_tarifas,text="Profesor acompañamiento")
            prof_acompaniamiento.grid(row=0,column=col)
            col+=1
        if self.asistente==1:
            aux=tk.Label(cuadro_tarifas,text="Asistente")
            aux.grid(row=0,column=col)
            col+=1
        materiales=tk.Label(cuadro_tarifas,text="Materiales")
        materiales.grid(row=0,column=col)
        col+=1
        gasto_materiales_=tk.Label(cuadro_tarifas,text="Gasto materiales")
        gasto_materiales_.grid(row=0,column=col)
        col+=1
        coloq=tk.Label(cuadro_tarifas,text="Coloquia")
        coloq.grid(row=0,column=col)
               
                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
    
        fila=1
        if self.maxima_cant_alumnos:
            for alumnos in range(self.minima_cant_alumnos,self.maxima_cant_alumnos+1):          
                col=0
                al=tk.Label(cuadro_tarifas,text=alumnos)
                al.grid(row=fila,column=col)
                col+=1
                total_escuela=round((alumnos*self.tarifa_colegio+self.valor_hora_acompaniamiento*self.hora_anterior+self.valor_hora_acompaniamiento*self.hora_posterior),2)
                esc=tk.Label(cuadro_tarifas,text=total_escuela)
                esc.grid(row=fila,column=col)
                col+=1
                    
                self.entrada_pago_profesor_alumnos[alumnos]=tk.Label(cuadro_tarifas,text=self.pago_profesor_alumnos[alumnos])
                self.entrada_pago_profesor_alumnos[alumnos].grid(row=fila,column=col)
                        
                col+=1
                acompaniamiento=0
                if self.hora_anterior==1 or self.hora_posterior==1:
                    acompaniamiento=self.valor_hora_acompaniamiento
                    acomp=tk.Label(cuadro_tarifas,text=self.valor_hora_acompaniamiento)
                    if self.hora_anterior==1 and self.hora_posterior==1:
                        acompaniamiento=self.valor_hora_acompaniamiento*2
                        acomp.config(text=self.valor_hora_acompaniamiento*2)
                    acomp.grid(row=fila,column=col)
                    col+=1            
                if self.asistente==1:
                    asist=tk.Label(cuadro_tarifas,text=self.valor_hora_asistente)
                    asist.grid(row=fila,column=col)
                    col+=1
                mate_tarifa=tk.Label(cuadro_tarifas,text=alumnos*self.tarifa_materiales)
                mate_tarifa.grid(row=fila,column=col)
                col+=1
                mate_gasto=tk.Label(cuadro_tarifas,text=round((alumnos*self.gasto_materiales),2))
                mate_gasto.grid(row=fila,column=col)
                col+=1
                
                total_coloquia=round((total_escuela -  self.pago_profesor_alumnos[alumnos]  -acompaniamiento -self.valor_hora_asistente -self.gasto_materiales*alumnos),2)
                print("Pago coloquia ")
                coloqu=tk.Label(cuadro_tarifas,text=total_coloquia)
                coloqu.grid(row=fila,column=col)                              
                fila+=1
            conexion1.close()     
        
    def modificar(self):
                     
        vent_modificar= tk.Toplevel()                ### Abro nueva ventana que muestra datos  para modificar
        self.vent_modificar=vent_modificar
        vent_modificar.title("Tarifa "+str(self.id))
        vent_modificar.state("zoomed")    

        vent_modificar.columnconfigure(7,weight=1)    
        nom_tarif=tk.Label(vent_modificar,text="Nombre: ")
        nom_tarif.grid(row=0,column=0)
        entrada_nom_terifa=tk.Entry(vent_modificar)
        entrada_nom_terifa.insert(0,self.nombre)
        entrada_nom_terifa.grid(row=0,column=1)
        etiqueta_tarifas=tk.LabelFrame(vent_modificar)     
        etiqueta_tarifas.config(width=800, height=100)
        etiqueta_tarifas.config(text="Tarifa por alumno")
        etiqueta_tarifas.grid(row=3,column=0,columnspan=6,rowspan=3,sticky="nwes")
        tar_colegio=tk.Label(etiqueta_tarifas,text="Colegio: ")
        tar_colegio.grid(row=0,column=0)
        entrada_tar_colegio=tk.Entry(etiqueta_tarifas)
        entrada_tar_colegio.insert(0,self.tarifa_colegio)
        entrada_tar_colegio.grid(row=0,column=1)
        tar_materiales=tk.Label(etiqueta_tarifas,text="Materiales: ")
        tar_materiales.grid(row=0,column=2)
        entrada_tar_materiales=tk.Entry(etiqueta_tarifas)
        entrada_tar_materiales.insert(0,self.tarifa_materiales)
        entrada_tar_materiales.grid(row=0,column=3)
        gasto_materiales=tk.Label(etiqueta_tarifas,text="Gasto materiales: ")
        gasto_materiales.grid(row=0,column=4)
        entrada_gasto_materiales=tk.Entry(etiqueta_tarifas)
        entrada_gasto_materiales.insert(0,self.gasto_materiales)
        entrada_gasto_materiales.grid(row=0,column=5)
        asistente=tk.Label(vent_modificar,text="Asistente: ")
        asistente.grid(row=8,column=0)
        entrada_asistente=ttk.Combobox(vent_modificar, state="readonly",values=("SI","NO"))
        entrada_asistente.set("SI") if self.asistente==1 else entrada_asistente.set("NO")      
        entrada_asistente.grid(row=8,column=1)
        entrada_valor_asistente=tk.Entry(vent_modificar)
        if self.asistente==1:
            valor_asistente=tk.Label(vent_modificar,text="Tarifa asistente: ")
            valor_asistente.grid(row=9,column=0)
            entrada_valor_asistente.grid(row=9,column=1)
            entrada_valor_asistente.insert(0,self.valor_hora_asistente)        
        hora_anterior=tk.Label(vent_modificar,text="Hora previa: ")
        hora_anterior.grid(row=10,column=0)
        entrada_hora_anterior=ttk.Combobox(vent_modificar, state="readonly",values=("SI","NO"))
        entrada_hora_anterior.set("SI") if self.hora_anterior==1 else entrada_hora_anterior.set("NO")      
        entrada_hora_anterior.grid(row=10,column=1)
        hora_posterior=tk.Label(vent_modificar,text="Hora posterior: ")
        hora_posterior.grid(row=11,column=0)
        entrada_hora_posterior=ttk.Combobox(vent_modificar, state="readonly",values=("SI","NO"))
        entrada_hora_posterior.set("SI") if self.hora_posterior==1 else entrada_hora_posterior.set("NO")      
        entrada_hora_posterior.grid(row=11,column=1)
        entrada_valor_acompaniamiento=tk.Entry(vent_modificar)
        if self.hora_anterior==1 or self.hora_posterior==1:
            valor_acompaniamiento=tk.Label(vent_modificar,text="Tarifa acompañamiento: ")
            valor_acompaniamiento.grid(row=12,column=0)
            entrada_valor_acompaniamiento.grid(row=12,column=1)
            entrada_valor_acompaniamiento.insert(0,self.valor_hora_acompaniamiento)
        minimo_alumnos=tk.Label(vent_modificar,text="Cantidad minima de alumnos: ")
        minimo_alumnos.grid(row=13,column=0)
        entrada_minimo_alumnos=tk.Entry(vent_modificar)
        entrada_minimo_alumnos.insert(0,self.minima_cant_alumnos)
        entrada_minimo_alumnos.grid(row=13,column=1)        
        maximo_alumnos=tk.Label(vent_modificar,text="Cantidad maxima de alumnos: ")
        maximo_alumnos.grid(row=14,column=0)
        entrada_mmaximo_alumnos=tk.Entry(vent_modificar)
        entrada_mmaximo_alumnos.insert(0,self.maxima_cant_alumnos)
        entrada_mmaximo_alumnos.grid(row=14,column=1)      
        activo=tk.Label(vent_modificar,text="Activo: ")
        activo.grid(row=15,column=0)
        entrada_activo=ttk.Combobox(vent_modificar, state="readonly",values=("SI","NO"))
        entrada_activo.set("SI") if self.activo==1 else entrada_activo.set("NO")      
        entrada_activo.grid(row=15,column=1)
        
        cuadro_tarifas=tk.LabelFrame(vent_modificar)
        cuadro_tarifas.config(width=1200, height=100)
        cuadro_tarifas.config(text="Cuadro resumen")        
        cuadro_tarifas.grid(row=16,column=0,columnspan=8,rowspan=3,sticky="nwes")
        cuadro_tarifas.columnconfigure(0,weight=1)
        cuadro_tarifas.columnconfigure(1,weight=1)
        cuadro_tarifas.columnconfigure(2,weight=1)
        cuadro_tarifas.columnconfigure(3,weight=1)
        cuadro_tarifas.columnconfigure(4,weight=1)
        cuadro_tarifas.columnconfigure(5,weight=1)
        cuadro_tarifas.columnconfigure(6,weight=1)
        cuadro_tarifas.columnconfigure(7,weight=1)
        col=0
        cant_alumnos=tk.Label(cuadro_tarifas,text="Cantidad alumnos")
        cant_alumnos.grid(row=0,column=col)
        col+=1
        tarifa_escuela=tk.Label(cuadro_tarifas,text="Escuela paga")
        tarifa_escuela.grid(row=0,column=col)
        col+=1
        tarifa_profesor=tk.Label(cuadro_tarifas,text="Profesor clase")
        tarifa_profesor.grid(row=0,column=col)
        col+=1
        if self.hora_anterior==1 or self.hora_posterior==1:
            prof_acompaniamiento=tk.Label(cuadro_tarifas,text="Profesor acompañamiento")
            prof_acompaniamiento.grid(row=0,column=col)
            col+=1
        if self.asistente==1:
            aux=tk.Label(cuadro_tarifas,text="Asistente")
            aux.grid(row=0,column=col)
            col+=1
        materiales=tk.Label(cuadro_tarifas,text="Materiales")
        materiales.grid(row=0,column=col)
        col+=1
        gasto_materiales_=tk.Label(cuadro_tarifas,text="Gasto materiales")
        gasto_materiales_.grid(row=0,column=col)
        col+=1
        coloq=tk.Label(cuadro_tarifas,text="Coloquia")
        coloq.grid(row=0,column=col)
               
                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
    
        fila=1
        if self.maxima_cant_alumnos:
            for alumnos in range(self.minima_cant_alumnos,self.maxima_cant_alumnos+1):          
                col=0
                al=tk.Label(cuadro_tarifas,text=alumnos)
                al.grid(row=fila,column=col)
                col+=1
                total_escuela=round((alumnos*self.tarifa_colegio+self.valor_hora_acompaniamiento*self.hora_anterior+self.valor_hora_acompaniamiento*self.hora_posterior),2)
                esc=tk.Label(cuadro_tarifas,text=total_escuela)
                esc.grid(row=fila,column=col)
                col+=1
                    
                self.entrada_pago_profesor_alumnos[alumnos]=tk.Entry(cuadro_tarifas)
                self.entrada_pago_profesor_alumnos[alumnos].insert(0, self.pago_profesor_alumnos[alumnos]) 
                self.entrada_pago_profesor_alumnos[alumnos].grid(row=fila,column=col)
                        
                col+=1
                acompaniamiento=0
                if self.hora_anterior==1 or self.hora_posterior==1:
                    acompaniamiento=self.valor_hora_acompaniamiento
                    acomp=tk.Label(cuadro_tarifas,text=self.valor_hora_acompaniamiento)
                    if self.hora_anterior==1 and self.hora_posterior==1:
                        acompaniamiento=self.valor_hora_acompaniamiento*2
                        acomp.config(text=self.valor_hora_acompaniamiento*2)
                    acomp.grid(row=fila,column=col)
                    col+=1            
                if self.asistente==1:
                    asist=tk.Label(cuadro_tarifas,text=self.valor_hora_asistente)
                    asist.grid(row=fila,column=col)
                    col+=1
                mate_tarifa=tk.Label(cuadro_tarifas,text=alumnos*self.tarifa_materiales)
                mate_tarifa.grid(row=fila,column=col)
                col+=1
                mate_gasto=tk.Label(cuadro_tarifas,text=round((alumnos*self.gasto_materiales),2))
                mate_gasto.grid(row=fila,column=col)
                col+=1
                
                total_coloquia=round((total_escuela -  self.pago_profesor_alumnos[alumnos]  -acompaniamiento -self.valor_hora_asistente -self.gasto_materiales*alumnos),2)
                
                coloqu=tk.Label(cuadro_tarifas,text=total_coloquia)
                coloqu.grid(row=fila,column=col)                              
                fila+=1
            conexion1.close() 
            
        def aplicar(cuadro_tarifas,entrada_valor_asistente):
            self.nombre=entrada_nom_terifa.get()
            self.tarifa_colegio=round(float(entrada_tar_colegio.get()), 2)
            self.tarifa_materiales=round(float(entrada_tar_materiales.get()), 2)
            self.gasto_materiales=round(float(entrada_gasto_materiales.get()), 2)
            if entrada_asistente.get()=="SI":
                self.asistente=1
                try:
                    x=entrada_valor_asistente.get()
                except:
                    entrada_valor_asistente.grid(row=9,column=1)
                    entrada_valor_asistente.insert(0,self.valor_hora_asistente)  
                if  x=='' :
                    x=0
                self.valor_hora_asistente=round(float(x), 2)
            else:
                self.asistente=0
                
            if entrada_hora_anterior.get()=="SI":
                self.hora_anterior=1
                f=entrada_valor_acompaniamiento.get()
                if entrada_valor_acompaniamiento.get()=='':
                   f=0 
                self.valor_hora_acompaniamiento=round(float(f), 2)
            else:
                self.hora_anterior=0   
                         
            if entrada_hora_posterior.get()=="SI":
                self.hora_posterior=1
                f=entrada_valor_acompaniamiento.get()
                if entrada_valor_acompaniamiento.get()=='':
                   f=0 
                self.valor_hora_acompaniamiento=round(float(f), 2)
            else:
                self.hora_posterior=0
                
            self.minima_cant_alumnos=int(entrada_minimo_alumnos.get()) 
            self.maxima_cant_alumnos=int(entrada_mmaximo_alumnos.get())
            self.activo=1 if (entrada_activo.get()=="SI") else 0 
            
            for alumnos in range(self.minima_cant_alumnos,self.maxima_cant_alumnos+1):
                try:
                    self.pago_profesor_alumnos[alumnos]=round(float(self.entrada_pago_profesor_alumnos[alumnos].get()), 2)
                except:
                    self.pago_profesor_alumnos[alumnos]=0
                    self.entrada_pago_profesor_alumnos[alumnos]=tk.Entry(cuadro_tarifas)
                    self.entrada_pago_profesor_alumnos[alumnos].insert(0, self.pago_profesor_alumnos[alumnos])
                else:
                     self.pago_profesor_alumnos[alumnos]=round(float(self.entrada_pago_profesor_alumnos[alumnos].get()), 2) 
            cuadro_tarifas.destroy()
            cuadro_tarifas=tk.LabelFrame(vent_modificar)
            cuadro_tarifas.config(width=1200, height=100)
            cuadro_tarifas.config(text="Cuadro resumen")        
            cuadro_tarifas.grid(row=16,column=0,columnspan=8,rowspan=3,sticky="nwes")
            cuadro_tarifas.columnconfigure(0,weight=1)
            cuadro_tarifas.columnconfigure(1,weight=1)
            cuadro_tarifas.columnconfigure(2,weight=1)
            cuadro_tarifas.columnconfigure(3,weight=1)
            cuadro_tarifas.columnconfigure(4,weight=1)
            cuadro_tarifas.columnconfigure(5,weight=1)
            cuadro_tarifas.columnconfigure(6,weight=1)
            cuadro_tarifas.columnconfigure(7,weight=1)
            col=0
            cant_alumnos=tk.Label(cuadro_tarifas,text="Cantidad alumnos")
            cant_alumnos.grid(row=0,column=col)
            col+=1
            tarifa_escuela=tk.Label(cuadro_tarifas,text="Escuela paga")
            tarifa_escuela.grid(row=0,column=col)
            col+=1
            tarifa_profesor=tk.Label(cuadro_tarifas,text="Profesor clase")
            tarifa_profesor.grid(row=0,column=col)
            col+=1
            if self.hora_anterior==1 or self.hora_posterior==1:
                prof_acompaniamiento=tk.Label(cuadro_tarifas,text="Profesor acompañamiento")
                prof_acompaniamiento.grid(row=0,column=col)
                col+=1
            if self.asistente==1:
                aux=tk.Label(cuadro_tarifas,text="Asistente")
                aux.grid(row=0,column=col)
                col+=1
            materiales=tk.Label(cuadro_tarifas,text="Materiales")
            materiales.grid(row=0,column=col)
            col+=1
            gasto_materiales_=tk.Label(cuadro_tarifas,text="Gasto materiales")
            gasto_materiales_.grid(row=0,column=col)
            col+=1
            coloq=tk.Label(cuadro_tarifas,text="Coloquia")
            coloq.grid(row=0,column=col)
                
            fila=1
            
            for alumnos in range(self.minima_cant_alumnos,self.maxima_cant_alumnos+1):
                col=0
                al=tk.Label(cuadro_tarifas,text=alumnos)
                al.grid(row=fila,column=col)
                col+=1
                total_escuela=round((alumnos*self.tarifa_colegio+self.valor_hora_acompaniamiento*self.hora_anterior+self.valor_hora_acompaniamiento*self.hora_posterior),2)
                esc=tk.Label(cuadro_tarifas,text=total_escuela)
                esc.grid(row=fila,column=col)
                col+=1
                    
                self.entrada_pago_profesor_alumnos[alumnos]=tk.Entry(cuadro_tarifas)
                self.entrada_pago_profesor_alumnos[alumnos].insert(0, self.pago_profesor_alumnos[alumnos]) 
                self.entrada_pago_profesor_alumnos[alumnos].grid(row=fila,column=col)
                        
                col+=1
                acompaniamiento=0
                if self.hora_anterior==1 or self.hora_posterior==1:
                    acompaniamiento=self.valor_hora_acompaniamiento
                    acomp=tk.Label(cuadro_tarifas,text=self.valor_hora_acompaniamiento)
                    if self.hora_anterior==1 and self.hora_posterior==1:
                        acompaniamiento=self.valor_hora_acompaniamiento*2
                        acomp.config(text=self.valor_hora_acompaniamiento*2)
                    acomp.grid(row=fila,column=col)
                    col+=1            
                if self.asistente==1:
                    asist=tk.Label(cuadro_tarifas,text=self.valor_hora_asistente)
                    asist.grid(row=fila,column=col)
                    col+=1
                mate_tarifa=tk.Label(cuadro_tarifas,text=alumnos*self.tarifa_materiales)
                mate_tarifa.grid(row=fila,column=col)
                col+=1
                mate_gasto=tk.Label(cuadro_tarifas,text=round((alumnos*self.gasto_materiales),2))
                mate_gasto.grid(row=fila,column=col)
                col+=1
                
                total_coloquia=round((total_escuela -  self.pago_profesor_alumnos[alumnos]  -acompaniamiento -self.valor_hora_asistente -self.gasto_materiales*alumnos),2)
                
                coloqu=tk.Label(cuadro_tarifas,text=total_coloquia)
                coloqu.grid(row=fila,column=col)                              
                fila+=1
            
            vent_modificar.destroy()
            self.modificar()   
            conexion1.close() 
            
        bot_aplicar=tk.Button(vent_modificar,text="Aplicar",command=lambda: aplicar(cuadro_tarifas,entrada_valor_asistente))
        bot_aplicar.grid(row=19,column=4)
        
        def cancelar():
            vent_modificar.destroy()
            tarifa1=Tarifa(self.id)
            tarifa1.modificar()                 
        bot_aplicar=tk.Button(vent_modificar,text="Cancelar",command=cancelar)
        bot_aplicar.grid(row=19,column=5)
        
        def grabar():                
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values") 
            consulta=("update tarifas set nombreTarifa =%a where idTarifa = %a"%(self.nombre,self.id)) 
            cursor1.execute(consulta)                   
            conexion1.commit()
            cursor1.execute("update tarifas set tarifaColegio =%a where idTarifa = %a"%(self.tarifa_colegio,self.id))                   
            conexion1.commit()
            cursor1.execute("update tarifas set tarifaMateriales =%a where idTarifa = %a"%(self.tarifa_materiales,self.id))                   
            conexion1.commit()
            cursor1.execute("update tarifas set gastoMatriales =%a where idTarifa = %a"%(self.gasto_materiales,self.id))                   
            conexion1.commit()
            cursor1.execute("update tarifas set asistente =%a where idTarifa = %a"%(self.asistente,self.id))                   
            conexion1.commit()
            if self.asistente==1:
                cursor1.execute("update tarifas set valorHoraAsistente =%a where idTarifa = %a"%(self.valor_hora_asistente,self.id))                   
                conexion1.commit()
            cursor1.execute("update tarifas set horaAnterior =%a where idTarifa = %a"%(self.hora_anterior,self.id))                   
            conexion1.commit()
            cursor1.execute("update tarifas set horaPosterior =%a where idTarifa = %a"%(self.hora_posterior,self.id))                   
            conexion1.commit()            
            if self.hora_anterior or self.hora_posterior:
                cursor1.execute("update tarifas set valorAcompaniamiento =%a where idTarifa = %a"%(self.valor_hora_acompaniamiento,self.id))                   
                conexion1.commit()
            cursor1.execute("update tarifas set minimaCantAlumnos =%a where idTarifa = %a"%(self.minima_cant_alumnos,self.id))                   
            conexion1.commit()
            cursor1.execute("update tarifas set maximaCantAlumnos =%a where idTarifa = %a"%(self.maxima_cant_alumnos,self.id))                   
            conexion1.commit() 
            cursor1.execute("update tarifas set activo =%a where idTarifa = %a"%(self.activo,self.id))                   
            conexion1.commit()   
            for alumnos in range(self.minima_cant_alumnos,self.maxima_cant_alumnos+1):
                query=("select id from cuadroTarifario where  idTarifa = %a and cantidadAlumnos= %a"%(self.id,alumnos)) 
                cursor1.execute(query)
                tar=list(cursor1)
                if tar!=[]:
                    cursor1.execute("update cuadroTarifario set tarifaProfesor = %a where idTarifa = %a and cantidadAlumnos= %a"%(self.pago_profesor_alumnos[alumnos],self.id,alumnos)) 
                else:
                    query=("insert into cuadroTarifario (idTarifa,cantidadAlumnos,tarifaProfesor) values (%a,%a,%a)"%(self.id,alumnos,self.pago_profesor_alumnos[alumnos]) ) 
                    cursor1.execute(query)
                conexion1.commit()
            
              
            
            conexion1.close()
            pass
        bot_aplicar=tk.Button(vent_modificar,text="Grabar",command=grabar)
        bot_aplicar.grid(row=19,column=6)
      



################################################         class Cursadas     ################################################          

class Cursadas:
    def __init__(self,cursada_id):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")        
        cursor1.execute("select * from cursadas where idCursada = %a"%cursada_id )    ## Consulta sql 
        self.cursadas_variables=("id","id_materia","id_escuela","id_profesor","id_asistente","id_anio","cuatrimestre","id_dia","id_hora_inicio","id_hora_fin","id_tarifa","fecha_inicio","fecha_fin","cantidad_alumnos","activo")        
        k=0
        cur=list(cursor1)
        for i in self.cursadas_variables:            
            jts=("self."+i+" = %r" % cur[0][k])       
            exec(jts)
            k+=1
        self.profesor=Profesor(self.id_profesor)
        self.asistente=Profesor(self.id_asistente)
        self.materia=Materia(self.id_materia)
        self.escuela=Escuela(self.id_escuela)
        self.tarifa=Tarifa(self.id_tarifa)
        cursor1.execute("select dia from dias where dias.idDia= "+str(self.id_dia)) #selecciono el dia que le corresponde al idDia
        self.dia=list(cursor1)[0][0]
        cursor1.execute("select horainicio from horainicio where horainicio.idHorainicio= "+str(self.id_hora_inicio)) #selecciono hora que le corresponde al idHorainicio
        self.hora_inicio=list(cursor1)[0][0]
        cursor1.execute("select horafin from horafin where horafin.idHorafin= "+str(self.id_hora_fin)) #selecciono hora que le corresponde al idHorafin
        self.hora_fin=list(cursor1)[0][0]
        cursor1.execute("select anio from anios where anios.idAnio= "+str(self.id_anio)) #selecciono el año que corresponde idAño
        self.anio=list(cursor1)[0][0]
        conexion1.close()    ## Cierro conexion 

    def modificar(self):
        def seleccionar_materia(bot_materia_nombre):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select nombreMateria from materias  where activo = 1" )    ## Consulta sql
            materias=list(cursor1)
            materias_agregar=[i[0] for i in materias]
            combo_materias=ttk.Combobox(vent_cursada_modificacion, state="readonly",font=("arial",20),values=materias_agregar) 
            conexion1.close() 
            def leer():
                self.materia.nombre=combo_materias.get()
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")        
                cursor1.execute("select idMateria from materias  where nombreMateria = %a"%self.materia.nombre )    ## Consulta sql
                mat=list(cursor1)
                self.materia=Materia(mat[0][0])
                self.id_materia= self.materia.id    
                conexion1.close()               
                vent_cursada_modificacion.destroy()
                self.modificar()
            bot_materia_nombre.config(text="Aplicar",bg="pale green",command=leer)
            combo_materias.grid(row=0,column=1,sticky="nwe",pady=0)
             
        def seleccionar_anio(bot_anio):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select anio from anios" )    ## Consulta sql
            anios=list(cursor1)
            anios_agregar=[i[0] for i in anios]
            combo_anios=ttk.Combobox(vent_cursada_modificacion, state="readonly",font=("arial",20),values=anios_agregar) 
            conexion1.close() 
            def leer():
                self.anio=combo_anios.get()
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")        
                cursor1.execute("select idAnio from anios  where anio = %a"%self.anio )    ## Consulta sql
                an=list(cursor1)
                self.id_anio=an[0][0]
                conexion1.close()               
                vent_cursada_modificacion.destroy()
                self.modificar()
            bot_anio.config(text="Aplicar",bg="pale green",command=leer)
            combo_anios.grid(row=2,column=1,sticky="nwe",pady=0)

        def seleccionar_cuatrimestre(bot_cuatrimestre):
            combo_cuatrimestres=ttk.Combobox(vent_cursada_modificacion, state="readonly",font=("arial",20),values=(1,2)) 
            def leer():
                self.cuatrimestre=combo_cuatrimestres.get()              
                vent_cursada_modificacion.destroy()
                self.modificar()
            bot_cuatrimestre.config(text="Aplicar",bg="pale green",command=leer)
            combo_cuatrimestres.grid(row=3,column=1,sticky="nwe",pady=0)

            
        def seleccionar_horainicio(bot_hora_inicio):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select horainicio from horainicio where activo=1" )    ## Consulta sql
            hinic=list(cursor1)
            hinic_agregar=[i[0] for i in hinic]
            hinic_agregar.append("Seleccionar otra hora")
            combo_hinic=ttk.Combobox(vent_cursada_modificacion, state="readonly",font=("arial",20),values=hinic_agregar) 
            conexion1.close()
            def leer():
                self.hora_inicio=combo_hinic.get()
                if self.hora_inicio=="Seleccionar otra hora":
                    horas_lista_gral()
                else:
                    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                    cursor1= conexion1.cursor()
                    cursor1.execute("use test_values")        
                    cursor1.execute("select idHorainicio from horainicio  where horainicio = %a"%self.hora_inicio )    ## Consulta sql
                    hi=list(cursor1)
                    self.id_hora_inicio=hi[0][0]
                    conexion1.close()               
                vent_cursada_modificacion.destroy()
                self.modificar() 
                    
            bot_hora_inicio.config(text="Aplicar",bg="pale green",command=leer)
            combo_hinic.grid(row=5,column=1,sticky="nwe",pady=0)  
            
        def seleccionar_horafin(bot_hora_fin):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select horafin from horafin where activo =1" )    ## Consulta sql
            hfin=list(cursor1)
            hfin_agregar=[i[0] for i in hfin]
            hfin_agregar.append("Seleccionar otra hora")
            combo_hfin=ttk.Combobox(vent_cursada_modificacion, state="readonly",font=("arial",20),values=hfin_agregar) 
            conexion1.close() 
            def leer():
                self.hora_fin=combo_hfin.get()
                if self.hora_fin=="Seleccionar otra hora":
                    horas_lista_gral()
                else:
                    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                    cursor1= conexion1.cursor()
                    cursor1.execute("use test_values")        
                    cursor1.execute("select idHorafin from horafin  where horafin = %a"%self.hora_fin )    ## Consulta sql
                    hf=list(cursor1)
                    self.id_hora_fin=hf[0][0]
                    conexion1.close()               
                    vent_cursada_modificacion.destroy()
                    self.modificar()
            bot_hora_fin.config(text="Aplicar",bg="pale green",command=leer)
            combo_hfin.grid(row=6,column=1,sticky="nwe",pady=0)            
                                               

        def seleccionar_fecha_inicio(bot_fecha_inicio,dia): 
            cal = Calendar(vent_cursada_modificacion, font="Arial 14", selectmode='day', locale='en_US',
                        disabledforeground='red',
                    cursor="hand1")            
            cal.grid(row=7,column=1)
            def grabar_fecha():
                self.fecha_inicio=datetime.datetime.strptime(cal.get_date(), '%m/%d/%y')
                self.fecha_inicio=self.fecha_inicio.date()
                self.anio=int((datetime.datetime.strptime(cal.get_date(), '%m/%d/%y')).year)
                print("Anio ",self.anio)
                self.id_dia=(((datetime.datetime.strptime(cal.get_date(), '%m/%d/%y')).weekday())+1)
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")        
                cursor1.execute("select dia from dias  where idDia = %a"%self.id_dia )    ## Consulta sql
                an=list(cursor1)
                self.dia=an[0][0]
                cursor1.execute("select idAnio from anios  where anio = %a"%self.anio )    ## Consulta sql
                an=list(cursor1)
                self.id_anio=an[0][0]
                conexion1.close()        
                vent_cursada_modificacion.destroy()
                self.modificar()
            bot_fecha_inicio.config(text="Seleccionar",command=grabar_fecha,bg="pale green")
            bot_fecha_inicio.grid(row=7,column=0,sticky="we",pady=15) 
            print ("Dia de la semana ",(datetime.datetime.strptime(cal.get_date(), '%m/%d/%y')).weekday())
            return cal.get_date()
    
            
        def seleccionar_fecha_fin(bot_fecha_fin):         
            cal = Calendar(vent_cursada_modificacion, font="Arial 14", selectmode='day', locale='en_US',
                        disabledforeground='red',
                    cursor="hand1")            
            cal.grid(row=8,column=1)
            def grabar_fecha():
                self.fecha_fin=datetime.datetime.strptime(cal.get_date(), '%m/%d/%y')
                self.fecha_fin=self.fecha_fin.date()
                vent_cursada_modificacion.destroy()
                self.modificar()
            bot_fecha_fin.config(text="Seleccionar",command=grabar_fecha,bg="pale green")
            bot_fecha_fin.grid(row=8,column=0,sticky="we",pady=15) 
            return cal.get_date()
            
        def seleccionar_docente(bot_docente,funcion):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select idProfesor,nombreProfesor,apellidoProfesor from profesores where activo= 1" )    ## Consulta sql
            docentes=list(cursor1)
            docentes_agregar=[str(i[0])+"  "+i[1]+" "+i[2] for i in docentes]
            combo_docentes=ttk.Combobox(vent_cursada_modificacion, state="readonly",font=("arial",20),values=docentes_agregar) 
            def leer():
                docente=combo_docentes.get()
                if funcion =="profesor":
                    self.profesor=Profesor(docente[0:3]) # en prof[0:3] esta id_profesor 
                    self.id_profesor= self.profesor.id
                elif funcion=="asistente" :
                    self.asistente=Profesor(docente[0:3]) # en prof[0:3] esta id_profesor 
                    self.id_asitente= self.asistente.id    
                vent_cursada_modificacion.destroy()
                self.modificar()
            bot_docente.config(text="Aplicar",bg="pale green",command=leer)
            combo_docentes.grid(row=2,column=4,sticky="nwe",pady=0,rowspan=2)
            conexion1.close()   
                      
        def seleccionar_escuela(bot_escuela):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select nombreEscuela from escuelas where activo =1" )    ## Consulta sql
            esc=list(cursor1)
            esc_agregar=[i[0] for i in esc]
            combo_escuela=ttk.Combobox(vent_cursada_modificacion, state="readonly",font=("arial",20),values=esc_agregar) 
            conexion1.close() 
            def leer():
                self.escuela=combo_escuela.get()
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")        
                cursor1.execute("select idEscuela from escuelas  where nombreescuela = %a"%self.escuela )    ## Consulta sql
                hf=list(cursor1)
                self.escuela=Escuela(hf[0][0])
                conexion1.close()  
                self.id_escuela= self.escuela.id  
                vent_cursada_modificacion.destroy()
                self.modificar()
            bot_escuela.config(text="Aplicar",bg="pale green",command=leer)
            combo_escuela.grid(row=2,column=6,sticky="nwe",pady=0)            
                                               
        def grabar():            
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")  
                m=0
                nombres_tabla=["idMateria","idEscuela","idProfesor","idAsistente","idAnio","cuatrimestre","idDia","idHoraInicio","idHoraFin","idTarifa","fechaInicio","fechaFin","cantidadAlumnos","activo"]
                cursadas_variables=("id_materia","id_escuela","id_profesor","id_asistente","id_anio","cuatrimestre","id_dia","id_hora_inicio","id_hora_fin","id_tarifa","fecha_inicio","fecha_fin","cantidad_alumnos","activo")   
                for i in cursadas_variables:            
                    jts=("self."+i)                    
                    if eval(jts)!=None:
                        
                        if jts=="self.fecha_inicio"or jts=="self.fecha_fin":                      
                            query=("update cursadas set "+nombres_tabla[m]+" = %a where idCursada= %a "%(datetime.date.strftime(eval(jts),'%Y-%m-%d'),self.id))
                        elif jts=="self.id_tarifa":
                            # self.tarifa=
                            query=("update cursadas set idTarifa =%a where idCursada= %a"%(self.tarifa.id,self.id))
                        else:                        
                            query=("update cursadas set "+nombres_tabla[m]+" = "+str(eval(jts))+" where idCursada= %a "%(self.id))
                        cursor1.execute(query)
                        conexion1.commit()
                        m+=1
                conexion1.close()
                vent_cursada_modificacion.destroy()
                self.modificar()                        
        def reset():
            vent_cursada_modificacion.destroy()
            cursada1=Cursadas(self.id)
            cursada1.modificar()
        def seleccionar_tarifa(tarifa):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")        
            cursor1.execute("select idTarifa,nombreTarifa,descripcion from tarifas" )    ## Consulta sql
            tarifas=list(cursor1)
            tarifas_agregar=[(str(i[0])+"  : "+str(i[1])+"  : "+str(i[2])) for i in tarifas]
            combo_tarifas=ttk.Combobox(vent_cursada_modificacion, state="readonly",font=("arial",20),values=tarifas_agregar) 
            conexion1.close() 
            
            tarifa.config(text="SDFSD")
            
            def leer():
                indice=combo_tarifas.get().find(" ")
                nueva_tarifa=int((combo_tarifas.get())[:indice])
                self.tarifa=Tarifa(nueva_tarifa)
                tarifa.config(text=self.tarifa.id)
                self.id
                combo_tarifas.destroy()         
                bot_tarifa.config(text="Tarifa",bg="light blue",command=lambda:seleccionar_tarifa(tarifa))
                
            bot_tarifa.config(text="Aplicar",bg="pale green",command=leer)
            combo_tarifas.grid(row=9,column=1,sticky="nwe",pady=0)
            pass
                          
            
        vent_cursada_modificacion= tk.Toplevel()            ## Nueva ventana cursada modificacion
        vent_cursada_modificacion.title("CURSADAS id %a"%self.id)
        vent_cursada_modificacion.state("zoomed")
        bot_materia_nombre=tk.Button(vent_cursada_modificacion,bg="light blue",text="Materia",command=lambda :seleccionar_materia(bot_materia_nombre)) 
        bot_materia_nombre.grid(row=0,column=0,sticky="nwe",pady=10) 
        materia_nombre=tk.Label(vent_cursada_modificacion,text=self.materia.nombre,font=("arial",20),fg="blue") 
        materia_nombre.grid(row=0,column=1,sticky="nwe",pady=0,columnspan=3) 
        bot_anio=tk.Button(vent_cursada_modificacion,bg="light blue",text="Año",command=lambda :seleccionar_anio(bot_anio)) 
        bot_anio.grid(row=2,column=0,sticky="nwe",pady=10) 
        anio=tk.Label(vent_cursada_modificacion,text=self.anio,font=("arial",20),fg="blue") 
        anio.grid(row=2,column=1,sticky="nwe")
        bot_cuatrimestre=tk.Button(vent_cursada_modificacion,bg="light blue",text="Cuatrimestre",command= lambda:seleccionar_cuatrimestre(bot_cuatrimestre)) 
        bot_cuatrimestre.grid(row=3,column=0,sticky="nwe",pady=15) 
        cuatrimestre=tk.Label(vent_cursada_modificacion,text=self.cuatrimestre,font=("arial",20),fg="blue") 
        cuatrimestre.grid(row=3,column=1,sticky="nwe")
        cartel_dia=tk.Button(vent_cursada_modificacion,bg="light blue",text="Día") 
        cartel_dia.grid(row=4,column=0,sticky="nwe",pady=15)        
        dia=tk.Label(vent_cursada_modificacion,text=self.dia,font=("arial",20),fg="blue") 
        dia.grid(row=4,column=1,sticky="nwe")
        bot_hora_inicio=tk.Button(vent_cursada_modificacion,bg="light blue",text="Hora inicio",command=lambda: seleccionar_horainicio(bot_hora_inicio)) 
        bot_hora_inicio.grid(row=5,column=0,sticky="nwe",pady=15) 
        hora_inicio=tk.Label(vent_cursada_modificacion,text=self.hora_inicio,font=("arial",20),fg="blue") 
        hora_inicio.grid(row=5,column=1,sticky="nwe")  
        bot_hora_fin=tk.Button(vent_cursada_modificacion,bg="light blue",text="Hora fin",command=lambda: seleccionar_horafin(bot_hora_fin)) 
        bot_hora_fin.grid(row=6,column=0,sticky="nwe",pady=15) 
        hora_fin=tk.Label(vent_cursada_modificacion,text=self.hora_fin,font=("arial",20),fg="blue") 
        hora_fin.grid(row=6,column=1,sticky="nwe")
        bot_fecha_inicio=tk.Button(vent_cursada_modificacion,bg="light blue",text="Fecha inicio",command= lambda: seleccionar_fecha_inicio(bot_fecha_inicio,dia)) 
        bot_fecha_inicio.grid(row=7,column=0,sticky="nwe",pady=15) 
        #fecha_inicio=tk.Entry(vent_cursada_modificacion,font=("arial",20))
        if self.fecha_inicio==None or self.fecha_inicio=="":
            self.fecha_inicio_mostrar=self.fecha_inicio
        else:
            self.fecha_inicio_mostrar=datetime.datetime.strftime(self.fecha_inicio, '%m/%d/%y')#( '%m/%d/%y')
        fecha_inicio=tk.Label(vent_cursada_modificacion,text=self.fecha_inicio_mostrar,font=("arial",20),fg="blue") 
        fecha_inicio.grid(row=7,column=1,sticky="nwe")
        bot_fecha_fin=tk.Button(vent_cursada_modificacion,bg="light blue",text="Fecha fin", command= lambda:seleccionar_fecha_fin(bot_fecha_fin)) 
        bot_fecha_fin.grid(row=8,column=0,sticky="nwe",pady=15)
        if self.fecha_fin==None or self.fecha_fin=="":
            self.fecha_fin_mostrar=self.fecha_fin
        else:
            self.fecha_fin_mostrar=datetime.datetime.strftime(self.fecha_fin, '%m/%d/%y')#( '%m/%d/%y')
        
        fecha_fin=tk.Label(vent_cursada_modificacion,text=self.fecha_fin_mostrar,font=("arial",20),fg="blue") 
        fecha_fin.grid(row=8,column=1,sticky="nwe")
        bot_tarifa=tk.Button(vent_cursada_modificacion,bg="light blue",text="Tarifa",command=lambda: seleccionar_tarifa(tarifa)) 
        bot_tarifa.grid(row=9,column=0,sticky="nwe",pady=15)          
        tarifa=tk.Label(vent_cursada_modificacion,text=self.tarifa.id,font=("arial",20),fg="blue") # Poner la tarifa correspondiente
        tarifa.grid(row=9,column=1,sticky="nwe")
        foto_prof=self.profesor.mostrar_foto(vent_cursada_modificacion,"PROFESOR")
        foto_prof.grid(row=3,column=3,sticky="n",rowspan=4) 
        bot_prof=tk.Button(vent_cursada_modificacion,bg="light blue",text="PROFESOR",command= lambda: seleccionar_docente(bot_prof,"profesor")) 
        bot_prof.grid(row=2,column=3,sticky="nwe")
        
        prof_nombre=tk.Label(vent_cursada_modificacion,text=self.profesor.nombre+" "+self.profesor.apellido,font=("arial",20),fg="blue")
        prof_nombre.grid(row=1,column=3,sticky="nw",columnspan=2)        
        datos_prof=self.profesor.mostrar_datos(vent_cursada_modificacion)
        datos_prof.grid(row=2,column=4,sticky="n",rowspan=6)
        foto_asistente=self.asistente.mostrar_foto(vent_cursada_modificacion,"Asistente")
        foto_asistente.grid(row=3,column=5,sticky="n",rowspan=4)
        datos_asistente=self.asistente.mostrar_datos(vent_cursada_modificacion)
        datos_asistente.grid(row=2,column=6,sticky="n",rowspan=6)
        bot_asistente=tk.Button(vent_cursada_modificacion,bg="light blue",text="ASISTENTE",command= lambda:seleccionar_docente(bot_asistente,"asistente")) 
        bot_asistente.grid(row=2,column=5,sticky="nwe")
        asistente_nombre=tk.Label(vent_cursada_modificacion,text=self.asistente.nombre+" "+self.asistente.apellido,font=("arial",20),fg="blue")
        asistente_nombre.grid(row=1,column=5,sticky="nw",columnspan=2)
        datos_escuela=self.escuela.mostrar_datos(vent_cursada_modificacion)
        datos_escuela.grid(row=2,column=7,sticky="n",rowspan=6)
        bot_escuela=tk.Button(vent_cursada_modificacion,bg="light blue",text="ESCUELA",command= lambda:seleccionar_escuela(bot_escuela)) 
        bot_escuela.grid(row=1,column=7,sticky="nwe")
        escuela_nombre=tk.Label(vent_cursada_modificacion,text=self.escuela.nombre,font=("arial",20),fg="blue")
        escuela_nombre.grid(row=0,column=4,sticky="ne",columnspan=4)
        bot_lista_alumnos=tk.Button(vent_cursada_modificacion,bg="light blue",text="Lista alumnos")
        bot_lista_alumnos.grid(row=10,column=3)
        cant_alumnos=tk.Label(vent_cursada_modificacion,bg="light blue",text="Cantidad de alumnos")#,comand=modificar_cantidad_alumnos)
        cant_alumnos.grid(row=10,column=4)
        rango_alumnos=[i for i in range(self.tarifa.minima_cant_alumnos,self.tarifa.maxima_cant_alumnos+1)]
        combo_cant_alumnos=ttk.Combobox(vent_cursada_modificacion, state="readonly",values=rango_alumnos,width=4)
        combo_cant_alumnos.set(self.cantidad_alumnos)
        marco_tarifa_valor_actual=tk.LabelFrame(vent_cursada_modificacion,text="Tarifa actual")
        marco_tarifa_valor_actual.config(width=35, height=6)
        marco_tarifa_valor_actual.grid(row=8,column=3,rowspan=1,columnspan=8,sticky="nwse")
    
        lista_mostrar_tarifa=["Cobro por alumno","Cobro por materiales ", "Gasto en materiales","Pago por acompañamiento","Pago por hora asistente"]
        lista_valores=[self.tarifa.tarifa_colegio,self.tarifa.tarifa_materiales,self.tarifa.gasto_materiales,self.tarifa.valor_hora_acompaniamiento,self.tarifa.valor_hora_asistente]
        for g in range (0,5,2):
            etiqueta=tk.Label(marco_tarifa_valor_actual,text=lista_mostrar_tarifa[g])
            etiqueta.grid(row=1,column=g,sticky="ne",padx=10)
            valores=tk.Label(marco_tarifa_valor_actual,text=lista_valores[g])
            valores.grid(row=1,column=g+1,sticky="nw",padx=0)
        
        marco_tarifa_total_alumnos=tk.LabelFrame(marco_tarifa_valor_actual,text="Computo para "+str(self.cantidad_alumnos)+" alumnos")
        marco_tarifa_total_alumnos.config(width=280, height=4) 
        marco_tarifa_total_alumnos.grid(row=3,column=0,columnspan=17,pady=10)   
        
        lista_mostrar_tarifa=["Cobro total por clase","Cobro total por materiales ", "Gasto total en materiales","Pago por acompañamiento","Pago por hora asistente","Pago al profesor","Beneficio Coloquia"]
        def cambiar_cant_alumnos(m,marco_tarifa_total_alumnos,lista_mostrar_tarifa):
            self.cantidad_alumnos=int(combo_cant_alumnos.get())
            pago_prof=pago_profesor(self.id_tarifa,self.cantidad_alumnos) 
            beneficio=self.tarifa.tarifa_colegio*self.cantidad_alumnos+self.tarifa.tarifa_materiales*self.cantidad_alumnos-self.tarifa.gasto_materiales*self.cantidad_alumnos-pago_prof
            
            acompaniamiento=0
            pago_asistente=0
            
            if self.tarifa.hora_anterior==1:
                acompaniamiento=self.tarifa.valor_hora_acompaniamiento
                pago_prof+=self.tarifa.valor_hora_acompaniamiento
            
            if self.tarifa.hora_posterior==1:
                acompaniamiento+=self.tarifa.valor_hora_acompaniamiento
                pago_prof+=self.tarifa.valor_hora_acompaniamiento 
            
            if self.tarifa.asistente==1:
                beneficio-=self.tarifa.valor_hora_asistente
                pago_asistente=self.tarifa.valor_hora_asistente
               
            lista_valores=[round(self.tarifa.tarifa_colegio*self.cantidad_alumnos+acompaniamiento,2),round(self.tarifa.tarifa_materiales*self.cantidad_alumnos,2),round(self.tarifa.gasto_materiales*self.cantidad_alumnos,2),round(acompaniamiento,2),round(pago_asistente,2),round(pago_prof,2),round(beneficio,2)]
            
            for g in range (0,7):#________________________________________________________________________
                etiqueta=tk.Label(marco_tarifa_total_alumnos,text=lista_mostrar_tarifa[g])
                etiqueta.grid(row=1,column=g,sticky="nwse",padx=10)
                valores=tk.Label(marco_tarifa_total_alumnos,text=lista_valores[g])
                valores.grid(row=2,column=g,sticky="nwse",padx=10)
            marco_tarifa_total_alumnos["text"]="Computo para "+str(self.cantidad_alumnos)+" alumnos"
            
        cambiar_cant_alumnos(marco_tarifa_total_alumnos,marco_tarifa_total_alumnos,lista_mostrar_tarifa)    
        combo_cant_alumnos.grid(row=10, column=4,sticky="w",padx=125,columnspan=3)
        combo_cant_alumnos.bind("<<ComboboxSelected>>", lambda a=marco_tarifa_total_alumnos, b=marco_tarifa_total_alumnos,c=lista_mostrar_tarifa:cambiar_cant_alumnos(a,b,c))
        bot_lista_grabar=tk.Button(vent_cursada_modificacion,bg="light blue",text="Grabar",command=grabar)
        bot_lista_grabar.grid(row=10,column=5)
        bot_cancelar=tk.Button(vent_cursada_modificacion,bg="light blue",text="Cancelar",command= reset)
        bot_cancelar.grid(row=10,column=6) 
        vent_cursada_modificacion.columnconfigure(0, weight=1)
        vent_cursada_modificacion.columnconfigure(1, weight=1) 
        vent_cursada_modificacion.columnconfigure(2, weight=2) 
        vent_cursada_modificacion.columnconfigure(3, weight=2) 
        vent_cursada_modificacion.columnconfigure(4, weight=2)
        vent_cursada_modificacion.columnconfigure(5, weight=2)
        vent_cursada_modificacion.columnconfigure(6, weight=2)    
        
    def mostrar(self):
        vent_cursada_mostrar= tk.Toplevel()            ## Nueva ventana cursada modificacion
        vent_cursada_mostrar.title("CURSADAS id %a"%self.id)
        vent_cursada_mostrar.state("zoomed")
        bot_materia_nombre=tk.Label(vent_cursada_mostrar,bg="light blue",text="Materia") 
        bot_materia_nombre.grid(row=0,column=0,sticky="nwe",pady=10) 
        materia_nombre=tk.Label(vent_cursada_mostrar,text=self.materia.nombre,font=("arial",20),fg="blue") 
        materia_nombre.grid(row=0,column=1,sticky="nwe",pady=0,columnspan=3) 
        bot_anio=tk.Label(vent_cursada_mostrar,bg="light blue",text="Año") 
        bot_anio.grid(row=2,column=0,sticky="nwe",pady=10) 
        anio=tk.Label(vent_cursada_mostrar,text=self.anio,font=("arial",20),fg="blue") 
        anio.grid(row=2,column=1,sticky="nwe")
        bot_cuatrimestre=tk.Label(vent_cursada_mostrar,bg="light blue",text="Cuatrimestre") 
        bot_cuatrimestre.grid(row=3,column=0,sticky="nwe",pady=15) 
        cuatrimestre=tk.Label(vent_cursada_mostrar,text=self.cuatrimestre,font=("arial",20),fg="blue") 
        cuatrimestre.grid(row=3,column=1,sticky="nwe")
        bot_dia=tk.Label(vent_cursada_mostrar,bg="light blue",text="Día") 
        bot_dia.grid(row=4,column=0,sticky="nwe",pady=15)        
        dia=tk.Label(vent_cursada_mostrar,text=self.dia,font=("arial",20),fg="blue") 
        dia.grid(row=4,column=1,sticky="nwe")
        bot_hora_inicio=tk.Label(vent_cursada_mostrar,bg="light blue",text="Hora inicio") 
        bot_hora_inicio.grid(row=5,column=0,sticky="nwe",pady=15) 
        hora_inicio=tk.Label(vent_cursada_mostrar,text=self.hora_inicio,font=("arial",20),fg="blue") 
        hora_inicio.grid(row=5,column=1,sticky="nwe")  
        bot_hora_fin=tk.Label(vent_cursada_mostrar,bg="light blue",text="Hora fin") 
        bot_hora_fin.grid(row=6,column=0,sticky="nwe",pady=15) 
        hora_fin=tk.Label(vent_cursada_mostrar,text=self.hora_fin,font=("arial",20),fg="blue") 
        hora_fin.grid(row=6,column=1,sticky="nwe")
        bot_fecha_inicio=tk.Label(vent_cursada_mostrar,bg="light blue",text="Fecha inicio") 
        bot_fecha_inicio.grid(row=7,column=0,sticky="nwe",pady=15) 
        fecha_inicio=tk.Label(vent_cursada_mostrar,font=("arial",20))
        if self.fecha_inicio==None or self.fecha_inicio=="":
            self.fecha_inicio_mostrar=self.fecha_inicio
        else:
            self.fecha_inicio_mostrar=datetime.datetime.strftime(self.fecha_inicio, '%m/%d/%y')#( '%m/%d/%y')
        fecha_inicio=tk.Label(vent_cursada_mostrar,text=self.fecha_inicio_mostrar,font=("arial",20),fg="blue") 
        fecha_inicio.grid(row=7,column=1,sticky="nwe")
        bot_fecha_fin=tk.Label(vent_cursada_mostrar,bg="light blue",text="Fecha fin") 
        bot_fecha_fin.grid(row=8,column=0,sticky="nwe",pady=15)
        if self.fecha_fin==None or self.fecha_fin=="":
            self.fecha_fin_mostrar=self.fecha_fin
        else:
            self.fecha_fin_mostrar=datetime.datetime.strftime(self.fecha_fin, '%m/%d/%y')#( '%m/%d/%y')
        
        fecha_fin=tk.Label(vent_cursada_mostrar,text=self.fecha_fin_mostrar,font=("arial",20),fg="blue") 
        fecha_fin.grid(row=8,column=1,sticky="nwe")
        bot_tarifa=tk.Label(vent_cursada_mostrar,bg="light blue",text="Tarifa") 
        bot_tarifa.grid(row=9,column=0,sticky="nwe",pady=15)          
        tarifa=tk.Label(vent_cursada_mostrar,text=self.id_tarifa,font=("arial",20),fg="blue") 
        tarifa.grid(row=9,column=1,sticky="nwe")
        foto_prof=self.profesor.mostrar_foto(vent_cursada_mostrar,"PROFESOR")
        foto_prof.grid(row=3,column=3,sticky="nw",rowspan=4) 
        bot_prof=tk.Label(vent_cursada_mostrar,bg="light blue",text="PROFESOR") 
        bot_prof.grid(row=2,column=3,sticky="nwe")
        prof_nombre=tk.Label(vent_cursada_mostrar,text=self.profesor.nombre+" "+self.profesor.apellido,font=("arial",20),fg="blue")
        prof_nombre.grid(row=1,column=3,sticky="nw",columnspan=2)        
        datos_prof=self.profesor.mostrar_datos(vent_cursada_mostrar)
        datos_prof.grid(row=2,column=4,sticky="n",rowspan=6)
        foto_asistente=self.asistente.mostrar_foto(vent_cursada_mostrar,"Asistente")
        foto_asistente.grid(row=3,column=5,sticky="n",rowspan=4)
        datos_asistente=self.asistente.mostrar_datos(vent_cursada_mostrar)
        datos_asistente.grid(row=2,column=6,sticky="n",rowspan=6)
        bot_asistente=tk.Label(vent_cursada_mostrar,bg="light blue",text="ASISTENTE") 
        bot_asistente.grid(row=2,column=5,sticky="nwe")
        asistente_nombre=tk.Label(vent_cursada_mostrar,text=self.asistente.nombre+" "+self.asistente.apellido,font=("arial",20),fg="blue")
        asistente_nombre.grid(row=1,column=5,sticky="nw",columnspan=2)
        datos_escuela=self.escuela.mostrar_datos(vent_cursada_mostrar)
        datos_escuela.grid(row=2,column=7,sticky="n",rowspan=6)
        bot_escuela=tk.Label(vent_cursada_mostrar,bg="light blue",text="ESCUELA") 
        bot_escuela.grid(row=1,column=7,sticky="nwe")
        escuela_nombre=tk.Label(vent_cursada_mostrar,text=self.escuela.nombre,font=("arial",20),fg="blue")
        escuela_nombre.grid(row=0,column=4,sticky="ne",columnspan=4)
        
        bot_lista_alumnos=tk.Button(vent_cursada_mostrar,bg="light blue",text="Lista alumnos")
        bot_lista_alumnos.grid(row=10,column=3)
        cant_alumnos=tk.Label(vent_cursada_mostrar,bg="light blue",text="Cantidad de alumnos")
        cant_alumnos.grid(row=10,column=4)
        rango_alumnos=[i for i in range(self.tarifa.minima_cant_alumnos,self.tarifa.maxima_cant_alumnos+1)]
        cant_alumnos=tk.Label(vent_cursada_mostrar, text= self.cantidad_alumnos)
        marco_tarifa_valor_actual=tk.LabelFrame(vent_cursada_mostrar,text="Tarifa actual")
        marco_tarifa_valor_actual.config(width=35, height=6)
        marco_tarifa_valor_actual.grid(row=8,column=3,rowspan=1,columnspan=8,sticky="nwse")
    
        lista_mostrar_tarifa=["Cobro por alumno","Cobro por materiales ", "Gasto en materiales","Pago por acompañamiento","Pago por hora asistente"]
        lista_valores=[self.tarifa.tarifa_colegio,self.tarifa.tarifa_materiales,self.tarifa.gasto_materiales,self.tarifa.valor_hora_acompaniamiento,self.tarifa.valor_hora_asistente]
        for g in range (0,5,2):
            etiqueta=tk.Label(marco_tarifa_valor_actual,text=lista_mostrar_tarifa[g])
            etiqueta.grid(row=1,column=g,sticky="ne",padx=10)
            valores=tk.Label(marco_tarifa_valor_actual,text=lista_valores[g])
            valores.grid(row=1,column=g+1,sticky="nw",padx=0)
        
        marco_tarifa_total_alumnos=tk.LabelFrame(marco_tarifa_valor_actual,text="Computo para "+str(self.cantidad_alumnos)+" alumnos")
        marco_tarifa_total_alumnos.config(width=280, height=4) 
        marco_tarifa_total_alumnos.grid(row=3,column=0,columnspan=17,pady=10)   
        
        lista_mostrar_tarifa=["Cobro total por clase","Cobro total por materiales ", "Gasto total en materiales","Pago por acompañamiento","Pago por hora asistente","Pago al profesor","Beneficio Coloquia"]
        def cambiar_cant_alumnos(m,marco_tarifa_total_alumnos,lista_mostrar_tarifa):
            pago_prof=pago_profesor(self.id_tarifa,self.cantidad_alumnos) 
            beneficio=self.tarifa.tarifa_colegio*self.cantidad_alumnos+self.tarifa.tarifa_materiales*self.cantidad_alumnos-self.tarifa.gasto_materiales*self.cantidad_alumnos-pago_prof
            
            acompaniamiento=0
            pago_asistente=0
            
            if self.tarifa.hora_anterior==1:
                acompaniamiento=self.tarifa.valor_hora_acompaniamiento
                pago_prof+=self.tarifa.valor_hora_acompaniamiento
            
            if self.tarifa.hora_posterior==1:
                acompaniamiento+=self.tarifa.valor_hora_acompaniamiento
                pago_prof+=self.tarifa.valor_hora_acompaniamiento 
            
            if self.tarifa.asistente==1:
                beneficio-=self.tarifa.valor_hora_asistente
                pago_asistente=self.tarifa.valor_hora_asistente
               
            lista_valores=[round(self.tarifa.tarifa_colegio*self.cantidad_alumnos+acompaniamiento,2),round(self.tarifa.tarifa_materiales*self.cantidad_alumnos,2),round(self.tarifa.gasto_materiales*self.cantidad_alumnos,2),round(acompaniamiento,2),round(pago_asistente,2),round(pago_prof,2),round(beneficio,2)]
            
            for g in range (0,7):#________________________________________________________________________
                etiqueta=tk.Label(marco_tarifa_total_alumnos,text=lista_mostrar_tarifa[g])
                etiqueta.grid(row=1,column=g,sticky="nwse",padx=10)
                valores=tk.Label(marco_tarifa_total_alumnos,text=lista_valores[g])
                valores.grid(row=2,column=g,sticky="nwse",padx=10)
            marco_tarifa_total_alumnos["text"]="Computo para "+str(self.cantidad_alumnos)+" alumnos"
            
        cambiar_cant_alumnos(marco_tarifa_total_alumnos,marco_tarifa_total_alumnos,lista_mostrar_tarifa)    
        cant_alumnos.grid(row=10, column=4,sticky="w",padx=180,columnspan=3)
        vent_cursada_mostrar.columnconfigure(0, weight=1)
        vent_cursada_mostrar.columnconfigure(1, weight=1) 
        vent_cursada_mostrar.columnconfigure(2, weight=2) 
        vent_cursada_mostrar.columnconfigure(3, weight=2) 
        vent_cursada_mostrar.columnconfigure(4, weight=2)
        vent_cursada_mostrar.columnconfigure(5, weight=2)
        vent_cursada_mostrar.columnconfigure(6, weight=2)    

########################################################   CLASS FACTURACION   #########################################################
class Facturacion():
    def __init__(self,entidad,entidad_asociada,id_entidad,nombre_entidad,fecha_inicio,fecha_fin,ventana,busqueda_id):
        self.entidad=entidad
        self.entidad_asociada=entidad_asociada
        self.id_identidad=id_entidad
        self.nombre_entidad=nombre_entidad
        self.fecha_inicio=fecha_inicio
        self.fecha_fin=fecha_fin
        self.ventana=ventana
        self.busqueda_id=busqueda_id
        pass
    def calcular(self):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        marco_liquidacion2=tk.LabelFrame(self.ventana,width=70,height=600)    #self.ventana=vent_liquidacion  
        marco_liquidacion2.grid_propagate(False)
        marco_liquidacion2.grid(row=2,column=0,sticky="nsew",columnspan=11)
        marco_liquidacion2.config(text="Liquidacion "+self.entidad+": "+self.nombre_entidad.upper())

        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas = tk.Canvas(marco_liquidacion2, borderwidth=0, background="#ffffff")
        canvas.config(width=1100,height=500)
        marco_liquidacion = tk.Frame(canvas, background="#ffffff")
        vsb = tk.Scrollbar(marco_liquidacion2, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.grid(row=2,column=0,sticky="ens")#(side="right", fill="y")
        canvas.grid_propagate(False)
        canvas.grid(row=2,column=0,sticky="nsew")#(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=marco_liquidacion, anchor="nw")

        marco_liquidacion.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        query=("select idCursada from cursadas where "+str(self.busqueda_id)+"=%a and fechaFin>%a and fechaInicio<%a and activo=1  "%(self.id_identidad,self.fecha_inicio.get(),self.fecha_fin.get()) )    ## Consulta sql
        cursor1.execute(query)
        cursadas=list(cursor1)
        query=("select * from feriados where fecha>=%a and fecha<=%a and   activo=1 order by fecha"%(self.fecha_inicio.get(),self.fecha_fin.get())  )    ## Consulta sql
        cursor1.execute(query)
        lista_feriados_periodo_liquidacion=list(cursor1)
        lista_feriados_periodo_liquidacion2=[l[3]for l in lista_feriados_periodo_liquidacion]
        conexion1.close() 
        id_cursadas_seleccionadas=[f[0] for f in cursadas]
        cursadas_seleccionadas=[Cursadas(i) for i in id_cursadas_seleccionadas]
        fin_liquidacion=datetime.datetime.strptime(self.fecha_fin.get(), '%Y-%m-%d').date()
        inicio_liquidacion=datetime.datetime.strptime(self.fecha_inicio.get(), '%Y-%m-%d').date()
        cursadas_fechas=[]
        for cursada_actual in cursadas_seleccionadas:
            aux_fecha_liquisdacion=datetime.datetime.strptime(self.fecha_inicio.get(), '%Y-%m-%d').date()#aux que voy modificando (dentro del periodo liquidacion)para ver si hay algo que pagar ese dia
            aux_fecha_cursada=cursada_actual.fecha_inicio #aux que vario de a 7 dias para misma cursada proxima semana
            while aux_fecha_liquisdacion<cursada_actual.fecha_fin and aux_fecha_liquisdacion<fin_liquidacion: 
                if aux_fecha_liquisdacion<aux_fecha_cursada: # fecha de liquidacion todavia no alcanzo inicio de cursada
                   aux_fecha_liquisdacion +=datetime.timedelta(days=1)                # incremento fecha liquidacion hasta alcanzarlo
                elif aux_fecha_liquisdacion>aux_fecha_cursada:# fecha liquidacion posterior al inicio cursada
                   aux_fecha_cursada +=datetime.timedelta(days=7)                      # aumento una semana aux fecha cursada
                else:                                     #Fecha liquidacion el mismo dia que la cursada entonces pago si no hay feriado
                    if self.entidad=="profesor":
                        if cursada_actual.profesor.id==int(self.id_identidad):
                            cursadas_fechas.append((cursada_actual,aux_fecha_liquisdacion,"--","Profesor"))
                            if cursada_actual.tarifa.hora_anterior==1:
                                cursadas_fechas.append((cursada_actual,aux_fecha_liquisdacion,"--","Hora anterior"))
                            if cursada_actual.tarifa.hora_anterior==1:
                                cursadas_fechas.append((cursada_actual,aux_fecha_liquisdacion,"--","Hora posterior"))
                        if cursada_actual.asistente.id==int(self.id_identidad):
                            cursadas_fechas.append((cursada_actual,aux_fecha_liquisdacion,"--","Asistente"))
                        aux_fecha_liquisdacion +=datetime.timedelta(days=7)
                        aux_fecha_cursada +=datetime.timedelta(days=7)
                    if self.entidad=="escuela":
                        cursadas_fechas.append((cursada_actual,aux_fecha_liquisdacion,"--","Profesor"))
                        if cursada_actual.tarifa.hora_anterior==1:
                            cursadas_fechas.append((cursada_actual,aux_fecha_liquisdacion,"--","Hora anterior"))
                        if cursada_actual.tarifa.hora_anterior==1:
                            cursadas_fechas.append((cursada_actual,aux_fecha_liquisdacion,"--","Hora posterior"))
                        aux_fecha_liquisdacion +=datetime.timedelta(days=7)
                        aux_fecha_cursada +=datetime.timedelta(days=7)
        lista_ordenada=[]
        
        while True:
            for j in cursadas_fechas:
                menor=cursadas_fechas[0]
                
                for i in cursadas_fechas:
                    if i[1]<menor[1]:
                        menor=i
                    elif i[1]==menor[1]:
                        if i[0].hora_fin<menor[0].hora_fin:
                            menor=i
            lista_ordenada.append(menor)
            cursadas_fechas.remove(menor)            
            if len(cursadas_fechas)==1:
                break
        titulo_materia= tk.Label(marco_liquidacion2,text="MATERIA") 
        titulo_materia.grid(row=1,column=0,sticky="w",padx=145)
        titulo_fecha= tk.Label(marco_liquidacion2,text="FECHA") 
        titulo_fecha.grid(row=1,column=0,sticky="w",padx=315) 
        titulo_hora_inicio= tk.Label(marco_liquidacion2,text="HORA") 
        titulo_hora_inicio.grid(row=1,column=0,sticky="w",padx=410,columnspan=8)  
        titulo_entidad_asociada= tk.Label(marco_liquidacion2,text="ESCUELA"if self.entidad=="profesor" else "PROFESOR") ## nombre entidad mostrar
        titulo_entidad_asociada.grid(row=1,column=0,sticky="w",padx=545,columnspan=8)
        titulo_cantidad_alumnos= tk.Label(marco_liquidacion2,text="ALUMNOS") 
        titulo_cantidad_alumnos.grid(row=1,column=0,sticky="w",padx=705,columnspan=8)
        titulo_funcion= tk.Label(marco_liquidacion2,text="FUNCION") 
        titulo_funcion.grid(row=1,column=0,sticky="w",padx=810,columnspan=8)
        titulo_monto= tk.Label(marco_liquidacion2,text="MONTO") 
        titulo_monto.grid(row=1,column=0,sticky="w",padx=910,columnspan=8)
        titulo_observaciones= tk.Label(marco_liquidacion2,text="OBSERVACIONES")
        titulo_observaciones.grid(row=1,column=0,sticky="w",padx=1012,columnspan=8)
        i=0 
        boton_n=[]
        registros=[]
        columnas=[]
        liquidacion_total_periodo=0   
        b=0
        for m in lista_ordenada:
            #k=0
            if self.entidad=="profesor":
                if m[3]=="Profesor":
                    pago_entidad=pago_profesor(m[0].tarifa.id,m[0].cantidad_alumnos) # Hay que definirlo para Escuela
                elif m[3]=="Hora anterior" or m[3]=="Hora posterior":
                    pago_entidad=m[0].tarifa.valor_hora_acompaniamiento
                elif  m[3]=="Asistente" :
                    pago_entidad=m[0].tarifa.valor_hora_asistente
            if self.entidad=="escuela":  
                if m[3]=="Profesor":
                    pago_entidad=m[0].tarifa.tarifa_colegio *m[0].cantidad_alumnos# Hay que definirlo para Escuela
                elif m[3]=="Hora anterior" or m[3]=="Hora posterior":
                    pago_entidad=m[0].tarifa.valor_hora_acompaniamiento      
            observaciones="--"
            for u in lista_feriados_periodo_liquidacion:
                if str(m[1])==  u[3].isoformat():
                    if u[2]==1:
                        pago_entidad=0
                        observaciones="Feriado nacional  "+ str(u[4])
                    elif u[1]==m[0].id_escuela:
                        pago_entidad=0
                        observaciones="Feriado local  "+ str(u[4]) 
                        
            lista_valores=(m[0].materia.nombre,m[1],m[0].hora_inicio,m[0].escuela.valores_demograficos[0] if self.entidad== "profesor" else (m[0].profesor.nombre+" "+m[0].profesor.apellido),m[0].cantidad_alumnos,m[3],round(pago_entidad,2),observaciones,m[0].id_materia)
            ancho=[36,16,14,36,13,20,11,30]
            for g in range(0,8):
                regis= tk.Entry(marco_liquidacion,justify="center",width=ancho[g])
                regis.insert(0, lista_valores[g])
                regis.config(state="disabled")
                regis.grid(row=i+2,column=g+1)
                columnas.append(regis)
                g+=1
            regis= tk.Entry(marco_liquidacion)
            regis.insert(0, lista_valores[8]) 
            columnas.append(regis)
            registros.append(columnas)
            columnas=[]
            liquidacion_total_periodo+=pago_entidad
            i+=1
            def actualizar(liq_final):
                liquidacion_total_periodo=0
                for r in registros:
                    liquidacion_total_periodo+=float(r[6].get())
                
                liq_final.config(text=round(liquidacion_total_periodo,2))
                liq_final.grid(row=3,column=0,sticky="w",padx=865,columnspan=8)     
                return liquidacion_total_periodo
            
            def modificar(registros,linea):
                registros[linea][6].config(state="normal")
                registros[linea][7].config(state="normal")
                boton_actualizar=tk.Button(marco_liquidacion,text="Actualizar",command= lambda :actualizar(liq_final))
                boton_actualizar.grid(row=linea+2,column=9)     
                
            boton_n.append(0)           
            boton_n[b]=tk.Button(marco_liquidacion,text="Modificar",command= lambda c= registros,linea=b,func=modificar: func(c,linea))
            boton_n[b].grid(row=i+1,column=0)    # posiciono boton modificar
            b+=1
            
        cartel_liq_final = tk.Label(marco_liquidacion2,text="TOTAL")
        cartel_liq_final.grid(row=3,column=0,sticky="w",padx=765,columnspan=8)
        liq_final = tk.Label(marco_liquidacion2)
        
        def grabar_liquidacion(registros,liquidacion_total_periodo):
            
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")
            ##Si estoy grabando una tabla nueva
            x=cursor1.execute("select  idLiquidacion from liquidaciones  order by IdLiquidacion desc limit 1" ) #busco el mayor IdLiquidacion
            fr=list(cursor1)
            nuevo_id=(fr[0][0])+1 if fr else 0
            query=("insert into liquidaciones values (%a,%a,%a,%a,%a,%a,1,%a)"%(nuevo_id,self.fecha_inicio.get(),self.fecha_fin.get(),self.entidad,self.id_identidad,round(actualizar(liq_final),2),self.nombre_entidad))
            cursor1.execute(query)
            conexion1.commit() 
            wb = openpyxl.Workbook()
            hoja = wb.active
            hoja.append(["Liquidacion ",self.nombre_entidad,"Periodo",inicio_liquidacion,fin_liquidacion,"id: %a"%nuevo_id]) 
            hoja.append([])
            hoja.append(["Id materia","Nombre materia","Fecha","Hora","Escuela","Cantidad alumnos","Funcion","Monto","Observaciones"])if self.entidad=="profesor" else hoja.append(["Id materia","Nombre materia","Fecha","Hora","Profesor","Cantidad alumnos","Funcion","Monto","Observaciones"])
            liquidacion_total_periodo=0       
            for i in registros:
                query=("insert into liquidacionesLineas values (null,%a,%a,%a,%a,%a,%a,%a,%a,%a,1)"%(nuevo_id,i[0].get(),i[1].get(),i[2].get(),i[3].get(),int(i[4].get()),i[5].get(),float(i[6].get()),i[7].get()))
                cursor1.execute(query)
                conexion1.commit()
                hoja.append([int(i[8].get()),i[0].get(),i[1].get(),i[2].get(),i[3].get(),int(i[4].get()),i[5].get(),float(i[6].get()),i[7].get()])
                liquidacion_total_periodo+=float(i[6].get())
            conexion1.close()    ## Cierro conexion
            file = filedialog.asksaveasfilename(filetypes=[("xlsx file", ".xlsx")],defaultextension=".xlsx")
            hoja.append([])
            hoja.append(["","","","","TOTAL PERIODO",round(liquidacion_total_periodo,2)])
            wb.save(file)
            wb.close()
        
        bot_grabar_bd=tk.Button(marco_liquidacion2,text="Grabar liquidacion", command=lambda:grabar_liquidacion(registros,liquidacion_total_periodo))
        bot_grabar_bd.grid(row=3,column=0,sticky="w",padx=465,columnspan=8)
        actualizar(liq_final)
        return(round(liquidacion_total_periodo,2))

#################################################    CLASS FACTURACION_ESCUELA    ##################################################   
class Facturacion_escuela(Facturacion):
    def __init__(self,id_entidad,nombre_entidad,fecha_inicio,fecha_fin,ventana,busqueda_id):
        self.entidad="escuela"
        self.entidad_asociada="profesor"
        self.busqueda_id=busqueda_id
        self.id_identidad=id_entidad
        self.nombre_entidad=nombre_entidad
        self.fecha_inicio=fecha_inicio #stringvar
        self.fecha_fin=fecha_fin
        self.ventana=ventana



#################################################    CLASS FACTURACION_PROFESOR    ##################################################    
class Facturacion_profesor(Facturacion):
    def __init__(self,id_entidad,nombre_entidad,fecha_inicio,fecha_fin,ventana,busqueda_id):
        self.entidad="profesor"
        self.entidad_asociada="escuela"
        self.busqueda_id=busqueda_id
        self.id_identidad=id_entidad
        self.nombre_entidad=nombre_entidad
        self.fecha_inicio=fecha_inicio #stringvar
        self.fecha_fin=fecha_fin
        self.ventana=ventana
       

########################################################################################################################################
#####################################################       VENTANA  PROFESORES     ####################################################
########################################################################################################################################

def modificar_prof(id):    
    profesor1=Profesor(id)   #### Creo el objeto profesor1 con id_profesor
    profesor1.modificar()
    
    
def mostrar_prof(id_profesor):
        profesor1=Profesor(id_profesor)
        profesor1.mostrar()         
     
def profesores_lista_gral():
    vent_profesores_lista_general= tk.Toplevel()            ## Nueva ventana profesores lista general
    vent_profesores_lista_general.title("PROFESORES LISTA GENERAL")
    vent_profesores_lista_general.state("zoomed")
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_profesores_lista_general,1,0,"NOMBRE","APELLIDO","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")             # Creo las etiquetas en el tope de la pagina
        
        
    cursor1.execute("select idProfesor, nombreProfesor, apellidoProfesor, estado, localidad, codigoPostal, calle,numero, piso, departamento, telefono, mail, activo from profesores inner join estados on profesores.idEstado = estados.idEstado inner join localidades on profesores.idLocalidad = localidades.idLocalidad" )    ## Consulta sql datos demograficos
                        
    crear_lista_seleccion(vent_profesores_lista_general,cursor1,mostrar_prof,1,2,3,4,5,6,7,8,9,10,11,12,13)   ## Muestro lista prof
                                                    # La seleccion de los botones lo levanto con la funcion mostrar_prof(idProfesor)
    conexion1.close()    ## Cierro conexion
    
def profesores_lista_encurso():
    vent_profesores_lista_en_curso= tk.Toplevel()            ## Nueva ventana profesores lista general
    vent_profesores_lista_en_curso.title("PROFESORES LISTA EN CURSO")
    vent_profesores_lista_en_curso.state("zoomed")
    ventana_fechas=tk.LabelFrame(vent_profesores_lista_en_curso)
    ventana_fechas.grid(row=0,column=0)
    fecha_inicio= tk.StringVar(master=vent_profesores_lista_en_curso, value="--")
    fecha_fin=tk.StringVar(master=vent_profesores_lista_en_curso, value="--") 
    seleccionar_fechas(fecha_inicio,fecha_fin,ventana_fechas)
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    def buscar(fecha_inicio,fecha_fin):
        funcion_etiquetas(vent_profesores_lista_en_curso,1,0,"NOMBRE","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL")             # Creo las etiquetas en el tope de la pagina
        inicio=fecha_inicio.get()  
        fin=fecha_fin.get()
        cursor1.execute("select profesores.idProfesor, nombreProfesor, estado, localidad, codigoPostal, calle,numero, piso, departamento, telefono, mail from profesores inner join estados on profesores.idEstado = estados.idEstado inner join localidades on profesores.idLocalidad = localidades.idLocalidad inner join cursadas on profesores.idProfesor= cursadas.idProfesor where fechaInicio<=%aand fechaFin >=%a"% (fin,inicio) )    ## Consulta sql datos demograficos
        ventana_fechas.destroy()  
        bot_buscar.destroy() 
        lista_sin_duplicados=[]
        
        cursor=list(cursor1)
        
        for nuevo_valor in cursor:
            repetido=0
            for valor in lista_sin_duplicados:
                if nuevo_valor[0] == valor[0]:
                    repetido=1
                    break
            if not repetido:
                lista_sin_duplicados.append(nuevo_valor)
                       
        crear_lista_seleccion(vent_profesores_lista_en_curso,lista_sin_duplicados,mostrar_esc,1,3,4,5,6,7,8,9,10,11,12)   ## Muestro lista escuela
                                                        # La seleccion de los botones lo levanto con la funcion mostrar_esc(idEscuela)
        conexion1.close()    ## Cierro conexion  
        
    bot_buscar=tk.Button(vent_profesores_lista_en_curso,text="Buscar",command=lambda :buscar(fecha_inicio,fecha_fin)) 
    bot_buscar.grid(row=4,column=1)
            
def profesores_modificacion():    
    vent_profesores_modificacion= tk.Toplevel()            ## Nueva ventana profesores lista general
    vent_profesores_modificacion.title("PROFESORES MODIFICACION")
    vent_profesores_modificacion.state("zoomed")
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_profesores_modificacion,1,0,"NOMBRE","APELLIDO","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")             # Creo las etiquetas en el tope de la pagina
        
        
    cursor1.execute("select idProfesor, nombreProfesor, apellidoProfesor, estado, localidad, codigoPostal, calle,numero,  ifnull(piso,'--'), departamento, ifnull( telefono,'--'), mail, activo from profesores inner join estados on profesores.idEstado = estados.idEstado inner join localidades on profesores.idLocalidad = localidades.idLocalidad" )    ## Consulta sql datos demograficos
    
                                                                            
    crear_lista_seleccion(vent_profesores_modificacion,cursor1,modificar_prof,1,2,3,4,5,6,7,8,9,10,11,12,13)   ## Muestro lista prof
                                                    # La seleccion de los botones lo levanto con la funcion mostrar_prof(idProfesor)
    conexion1.close()    ## Cierro conexion

def profesores_baja():      
    vent_profesores_baja= tk.Toplevel()            ## Nueva ventana 
    vent_profesores_baja.title("PROFESORES BAJA")
    vent_profesores_baja.state("zoomed")
    
    def baja_prof(id):
        profesor1=Profesor(id)           
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        query=("update profesores set activo = 0 where idProfesor=%a"%(profesor1.id))
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_profesores_baja.destroy()
        profesores_baja()

    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_profesores_baja,1,0,"NOMBRE","APELLIDO","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL")             # Creo las etiquetas en el tope de la pagina
        
        
    cursor1.execute("select idProfesor, nombreProfesor, apellidoProfesor, estado, localidad, codigoPostal, calle,numero,  ifnull(piso,'-3'), departamento, ifnull( telefono,'-3'), mail, activo from profesores inner join estados on profesores.idEstado = estados.idEstado inner join localidades on profesores.idLocalidad = localidades.idLocalidad  where activo =1" )    ## Consulta sql datos demograficos
                                                                                
    crear_lista_seleccion(vent_profesores_baja,cursor1,baja_prof,1,2,3,4,5,6,7,8,9,10,11,12)   ## Muestro lista prof
                                                    # La seleccion de los botones lo levanto con la funcion baja_prof(idProfesor)
    conexion1.close()    ## Cierro conexion
    
def profesores_alta():        
    vent_profesores_alta= tk.Toplevel()            ## Nueva ventana 
    vent_profesores_alta.title("PROFESORES ALTA")
    vent_profesores_alta.state("zoomed")
    
    def nuevo_prof():            
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        cursor1.execute("select idProfesor from profesores where nombreProfesor = '--' order by idProfesor desc limit 1")
        id_pr=list(cursor1)
        if id_pr==[]:
            cursor1.execute("insert into profesores(nombreProfesor)values ('--') ")         
            conexion1.commit()
        cursor1.execute("select idProfesor from profesores where nombreProfesor = '--' order by idProfesor desc limit 1")
        id_pr=list(cursor1)
        id_prof=id_pr[0][0]
        modificar_prof(id_prof)
        conexion1.close()    ## Cierro conexion
    
    def alta_existente():            
        vent_profesores_de_alta= tk.Toplevel()            ## Nueva ventana profesores lista general
        vent_profesores_de_alta.title("PROFESORES DADOS DE BAJA")
        vent_profesores_de_alta.state("zoomed")                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
           
        def profesor_revivir(id):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")            
            cursor1.execute("update profesores set activo = 1 where idProfesor=%r "%id)
            conexion1.commit()
            conexion1.close()    ## Cierro conexion
            vent_profesores_de_alta.destroy()
            alta_existente()
        
        funcion_etiquetas(vent_profesores_de_alta,1,0,"NOMBRE","APELLIDO","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL")             # Creo las etiquetas en el tope de la pagina            
            
        cursor1.execute("select idProfesor, nombreProfesor, apellidoProfesor, estado, localidad, codigoPostal, calle,numero, piso, departamento, telefono, mail, activo from profesores inner join estados on profesores.idEstado = estados.idEstado inner join localidades on profesores.idLocalidad = localidades.idLocalidad where activo = 0" )    ## Consulta sql datos demograficos para profesores dados de baja
                            
        crear_lista_seleccion(vent_profesores_de_alta,cursor1,profesor_revivir,1,2,3,4,5,6,7,8,9,10,11,12)   ## Muestro lista prof
                                                        # La seleccion de los botones lo levanto con la funcion mostrar_prof(idProfesor)
        conexion1.close()    ## Cierro conexion
           
    
    alto=3
    ancho=15
    vent_profesores_alta.columnconfigure(0, weight=1)           # Hago que se expandan las filas y columnas
    vent_profesores_alta.columnconfigure(1, weight=1)                 
    bot_nuevo=tk.Button(vent_profesores_alta,text="Nuevo profesor",command=nuevo_prof,height=alto,width=ancho)
    bot_existente=tk.Button(vent_profesores_alta,text="Profesor previamente dado de baja",command=alta_existente,height=alto,width=30)
    bot_nuevo.grid(row=0,column=0)  
    bot_existente.grid(row=0,column=1)       

def profesores():    
    marco_profesores=tk.Label(raiz)
    deseleccionar(lista_botones)
    marco_profesores.grid(row=0,column=1,rowspan=5,sticky="ns")
    marco_profesores.rowconfigure(0,weight=1)
    marco_profesores.rowconfigure(1,weight=1)
    marco_profesores.rowconfigure(2,weight=1)
    marco_profesores.rowconfigure(3,weight=1)
    marco_profesores.rowconfigure(4,weight=1)
    marco_profesores.rowconfigure(5,weight=1)
    cartel_profesores=tk.Label(raiz,text="PROFESORES",fg="dark slate blue",font=("arial",30))
    cartel_profesores.grid(row=0,column=0)
    bot_profesores_alta=tk.Button(marco_profesores,text="Alta",command=profesores_alta,height=alto,width=ancho)    
    bot_profesores_alta.grid(row=0,column=1)
    bot_profesores_baja=tk.Button(marco_profesores,text="Baja",command=profesores_baja,height=alto,width=ancho)    
    bot_profesores_baja.grid(row=1,column=1)
    bot_profesores_modificacion=tk.Button(marco_profesores,text="Modificación",command=profesores_modificacion,height=alto,width=ancho)    
    bot_profesores_modificacion.grid(row=2,column=1)
    bot_profesores_lista_gral=tk.Button(marco_profesores,text="Lista general",command=profesores_lista_gral,height=alto,width=ancho)    
    bot_profesores_lista_gral.grid(row=3,column=1)
    bot_profesores_lista_encurso=tk.Button(marco_profesores,text="Lista en curso",command=profesores_lista_encurso,height=alto,width=ancho)    
    bot_profesores_lista_encurso.grid(row=4,column=1)
    # bot_profesores_agenda=tk.Button(marco_profesores,text="Agenda",command=profesores_agenda,height=alto,width=ancho)    
    # bot_profesores_agenda.grid(row=5,column=1)
    bot_cancelar=tk.Button(raiz,text="Cancelar",command=lambda:cancelar(marco_profesores,bot_cancelar,cartel_profesores),height=alto,width=ancho)
    bot_cancelar.grid(row=1,column=0)

#######################################################################################################################################
##################################################       VENTANA  HORAS    ##############################################
#######################################################################################################################################  
       
def horas_lista_gral():
    vent_horas= tk.Toplevel()            ## Nueva ventana estados lista general
    vent_horas.title(" HORAS LISTA GENERAL")
    vent_horas.state("zoomed")   
        
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")        
    cursor1.execute("select * from horaInicio where activo=1" )    ## Consulta sql
    conexion1.close()    ## Cierro conexion 
    
    vent_horas.columnconfigure(0,weight=1)
    vent_horas.columnconfigure(1,weight=1)
    vent_horas.columnconfigure(2,weight=1)
    vent_horas.columnconfigure(3,weight=1)
    vent_horas.columnconfigure(4,weight=1)
    
    def grabar_hora_inicio_modificado(id,hora):                           
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
        query=("update horaInicio set horaInicio=%a where idHoraInicio=%a"%(hora,id))        
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_horas.destroy()
        horas_lista_gral()
    def eliminar_hora_inicio(id):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
        query=("update horaInicio set activo=0 where idHoraInicio=%a"%id)        
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_horas.destroy()
        horas_lista_gral()
    def modificar_hora_inicio(orden,id):
        ingreso_hora_inicio=tk.Entry (vent_horas)
        bot_inicio_n[orden]=tk.Button(vent_horas,text="Grabar",command=lambda : grabar_hora_inicio_modificado(id,ingreso_hora_inicio.get()),width=8)
        bot_inicio_n[orden].grid(row=orden+2,column=1,sticky="W",padx=15)
        bot_eliminar_inicio_n=tk.Button(vent_horas,text="Eliminar",command=lambda : eliminar_hora_inicio(id),width=8)
        bot_eliminar_inicio_n.grid(row=orden+2,column=1,sticky="W",padx=150)
        ingreso_hora_inicio.insert(0,inicio_n[orden].cget("text"))
        ingreso_hora_inicio.grid(row=orden+2,column=1,sticky="W",padx=90)
        
    
    etiqueta_inicio=tk.Label(vent_horas,text="HORA INICIO")
    etiqueta_inicio.grid(row=0,column=1,sticky="w",padx=90)                                                                      
    i=2 
    k=0                                                         
    inicio_n=[]
    bot_inicio_n=[]                                                          
    for bd in cursor1: 
        k+=1
        inicio_n.append(0)
        bot_inicio_n.append(0)      
        inicio_n[k-1] = tk.Label(vent_horas,text=bd[1])
        inicio_n[k-1].grid(row=i,column=1,sticky="w",padx=90)
        bot_inicio_n[k-1]=tk.Button(vent_horas,text="Modificar",command=lambda p=k-1, id=bd[0]: modificar_hora_inicio(p,id))
        bot_inicio_n[k-1].grid(row=i,column=1,sticky="W",padx=15)                
        i+=1
        
    def grabar_horas_inicio():
        nueva_hora_inicio=entrada_inicio.get()                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")        
        cursor1.execute("insert into HoraInicio(HoraInicio) values (%a)"%nueva_hora_inicio )    ## Consulta sql
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_horas.destroy() 
        horas_lista_gral()
    
    def cancelar_horas():
        vent_horas.destroy() 
        horas_lista_gral()
        
        
    etiqueta_entrada_inicio=tk.Label(vent_horas,text="Nueva hora inicio")
    etiqueta_entrada_inicio.grid(row=i+2,column=1,sticky="W",padx=0)
    entrada_inicio=tk.Entry(vent_horas)
    entrada_inicio.grid(row=i+2,column=1,sticky="W",padx=100)
    bot_grabar=tk.Button(vent_horas,text="Grabar",command=grabar_horas_inicio)
    bot_grabar.grid(row=i+4,column=1,sticky="W",padx=80)    
    bot_cancelar=tk.Button(vent_horas,text="Cancelar",command=cancelar_horas)
    bot_cancelar.grid(row=i+4,column=1,sticky="W",padx=145)
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")        
    cursor1.execute("select * from horaFin where activo=1" )    ## Consulta sql
    conexion1.close()    ## Cierro conexion 
    
    vent_horas.columnconfigure(0,weight=1)
    vent_horas.columnconfigure(1,weight=1)
    vent_horas.columnconfigure(2,weight=1)
    vent_horas.columnconfigure(3,weight=1)
    vent_horas.columnconfigure(4,weight=1)
    
    def grabar_hora_fin_modificado(id,hora):                           
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
        query=("update horaFin set horaFin=%a where idHoraFin=%a"%(hora,id))        
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_horas.destroy()
        horas_lista_gral()
    def eliminar_hora_fin(id):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
        query=("update horaFin set activo=0 where idHoraFin=%a"%id)        
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_horas.destroy()
        horas_lista_gral()
    def modificar_hora_fin(orden,id):
        ingreso_hora_fin=tk.Entry (vent_horas)
        bot_fin_n[orden]=tk.Button(vent_horas,text="Grabar",command=lambda : grabar_hora_fin_modificado(id,ingreso_hora_fin.get()),width=8)
        bot_fin_n[orden].grid(row=orden+2,column=3,sticky="W",padx=15)
        bot_eliminar_fin_n=tk.Button(vent_horas,text="Eliminar",command=lambda : eliminar_hora_fin(id),width=8)
        bot_eliminar_fin_n.grid(row=orden+2,column=3,sticky="W",padx=150)
        ingreso_hora_fin.insert(0,fin_n[orden].cget("text"))
        ingreso_hora_fin.grid(row=orden+2,column=3,sticky="W",padx=90)
        
    
    etiqueta_fin=tk.Label(vent_horas,text="HORA FIN")
    etiqueta_fin.grid(row=0,column=3,sticky="w",padx=90)                                                                      
    i=2 
    k=0                                                         
    fin_n=[]
    bot_fin_n=[]                                                          
    for bd in cursor1: 
        k+=1
        fin_n.append(0)
        bot_fin_n.append(0)      
        fin_n[k-1] = tk.Label(vent_horas,text=bd[1])
        fin_n[k-1].grid(row=i,column=3,sticky="w",padx=90)
        bot_fin_n[k-1]=tk.Button(vent_horas,text="Modificar",command=lambda p=k-1, id=bd[0]: modificar_hora_fin(p,id))
        bot_fin_n[k-1].grid(row=i,column=3,sticky="W",padx=15)                
        i+=1
        
    def grabar_horas_fin():
        nueva_hora_fin=entrada_fin.get()                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")        
        cursor1.execute("insert into HoraFin(HoraFin) values (%a)"%nueva_hora_fin )    ## Consulta sql
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_horas.destroy() 
        horas_lista_gral()
    
    def cancelar_horas():
        vent_horas.destroy() 
        horas_lista_gral()
        
        
    etiqueta_entrada_fin=tk.Label(vent_horas,text="Nueva hora fin")
    etiqueta_entrada_fin.grid(row=i+2,column=3,sticky="W",padx=0)
    entrada_fin=tk.Entry(vent_horas)
    entrada_fin.grid(row=i+2,column=3,sticky="W",padx=100)
    bot_grabar=tk.Button(vent_horas,text="Grabar",command=grabar_horas_fin)
    bot_grabar.grid(row=i+4,column=3,sticky="W",padx=80)    
    bot_cancelar=tk.Button(vent_horas,text="Cancelar",command=cancelar_horas)
    bot_cancelar.grid(row=i+4,column=3,sticky="W",padx=145) 
#######################################################################################################################################
##################################################       VENTANA  ESTADOS/LOCALIDADES    ##############################################
#######################################################################################################################################  
       
def estados_lista_gral():
    vent_estados= tk.Toplevel()            ## Nueva ventana estados lista general
    vent_estados.title(" ESTADOS LISTA GENERAL")
    vent_estados.state("zoomed")   
        
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")        
    cursor1.execute("select * from estados" )    ## Consulta sql
    conexion1.close()    ## Cierro conexion 
    
    vent_estados.columnconfigure(0,weight=1)
    vent_estados.columnconfigure(1,weight=1)
    vent_estados.columnconfigure(2,weight=1)
    vent_estados.columnconfigure(3,weight=1)
    vent_estados.columnconfigure(4,weight=1)
    
    def grabar_estado_modificado(id,nombre):                           
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
        query=("update estados set estado=%a where idEstado=%a"%(nombre,id))        
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_estados.destroy()
        estados_lista_gral()
    
    def modificar_estado(orden,id):
        ingreso_estado=tk.Entry (vent_estados)
        bot_estado_n[orden]=tk.Button(vent_estados,text="Grabar",command=lambda : grabar_estado_modificado(id,ingreso_estado.get()),width=8)
        bot_estado_n[orden].grid(row=orden+2,column=1,sticky="W",padx=15)
        ingreso_estado.insert(0,estado_n[orden].cget("text"))
        ingreso_estado.grid(row=orden+2,column=1,sticky="W",padx=90)
        
    
    etiqueta_estados=tk.Label(vent_estados,text="ESTADOS")
    etiqueta_estados.grid(row=0,column=1,sticky="w",padx=90)                                                                      
    i=2 
    k=0                                                         
    estado_n=[]
    bot_estado_n=[]                                                          
    for bd in cursor1: 
        k+=1
        estado_n.append(0)
        bot_estado_n.append(0)      
        estado_n[k-1] = tk.Label(vent_estados,text=bd[1])
        estado_n[k-1].grid(row=i,column=1,sticky="w",padx=90)
        bot_estado_n[k-1]=tk.Button(vent_estados,text="Modificar",command=lambda p=k-1, id=bd[0]: modificar_estado(p,id))
        bot_estado_n[k-1].grid(row=i,column=1,sticky="W",padx=15)                
        i+=1
        
    def grabar_estado():
        nuevo_estado=entrada_estado.get()                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")        
        cursor1.execute("insert into estados(estado) values (%a)"%nuevo_estado )    ## Consulta sql
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_estados.destroy() 
        estados_lista_gral()
    
    def cancelar_estado():
        vent_estados.destroy() 
        estados_lista_gral()
        
        
    etiqueta_entrada_estados=tk.Label(vent_estados,text="Nuevo estado")
    etiqueta_entrada_estados.grid(row=i+2,column=1,sticky="W",padx=0)
    entrada_estado=tk.Entry(vent_estados)
    entrada_estado.grid(row=i+2,column=1,sticky="W",padx=80)
    bot_grabar=tk.Button(vent_estados,text="Grabar",command=grabar_estado)
    bot_grabar.grid(row=i+4,column=1,sticky="W",padx=80)    
    bot_cancelar=tk.Button(vent_estados,text="Cancelar",command=cancelar_estado)
    bot_cancelar.grid(row=i+4,column=1,sticky="W",padx=145)
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")        
    cursor1.execute("select * from localidades" )    ## Consulta sql
    conexion1.close()    ## Cierro conexion 
  
    def grabar_localidad_modificado(id,nombre):                           
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
        query=("update localidades set localidad=%a where idLocalidad=%a"%(nombre,id)) 
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_estados.destroy()
        estados_lista_gral()
    
    def modificar_localidad(orden,id):
        ingreso_localidad=tk.Entry (vent_estados)
        bot_localidad_n[orden]=tk.Button(vent_estados,text="Grabar",command=lambda : grabar_localidad_modificado(id,ingreso_localidad.get()),width=8)
        bot_localidad_n[orden].grid(row=orden+2,column=3,sticky="W",padx=15)
        
        ingreso_localidad.insert(0,localidad_n[orden].cget("text"))
        ingreso_localidad.grid(row=orden+2,column=3,sticky="W",padx=90)

    etiqueta_localidades=tk.Label(vent_estados,text="LOCALIDADES")
    etiqueta_localidades.grid(row=0,column=3,sticky="w",padx=90)                                                                      
    i=2 
    k=0                                                         
    localidad_n=[]
    bot_localidad_n=[]                                                          
    for bd in cursor1: 
        k+=1
        localidad_n.append(0)
        bot_localidad_n.append(0)      
        localidad_n[k-1] = tk.Label(vent_estados,text=bd[1])
        localidad_n[k-1].grid(row=i,column=3,sticky="w",padx=90)
        bot_localidad_n[k-1]=tk.Button(vent_estados,text="Modificar",command=lambda p=k-1, id=bd[0]: modificar_localidad(p,id))
        bot_localidad_n[k-1].grid(row=i,column=3,sticky="W",padx=15)                
        i+=1
        
        
    def grabar_localidad():
        nueva_localidad=entrada_localidad.get()                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")        
        cursor1.execute("insert into localidades(localidad) values (%a)"%nueva_localidad )    ## Consulta sql
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_estados.destroy() 
        estados_lista_gral()
    
    def cancelar_localidad():
        vent_estados.destroy() 
        estados_lista_gral()
        
        
    etiqueta_entrada_localidad=tk.Label(vent_estados,text="Nueva localidad")
    etiqueta_entrada_localidad.grid(row=i+2,column=3,sticky="W",padx=0)
    entrada_localidad=tk.Entry(vent_estados)
    entrada_localidad.grid(row=i+2,column=3,sticky="W",padx=90)
    bot_grabar=tk.Button(vent_estados,text="Grabar",command=grabar_localidad)
    bot_grabar.grid(row=i+4,column=3,sticky="W",padx=80)    
    bot_cancelar=tk.Button(vent_estados,text="Cancelar",command=cancelar_localidad)
    bot_cancelar.grid(row=i+4,column=3,sticky="W",padx=145)
   
    
#########################################################################################################################################
##################################################        VENTANA  MATERIAS      ########################################################
#########################################################################################################################################

def mostrar_materia(id):
    materia1=Materia(id)
    materia1.mostrar_mat() 
    
def materias_lista_gral():
        vent_materias_lista_general= tk.Toplevel()            ## Nueva ventana materias lista general
        vent_materias_lista_general.title(" MATERIAS LISTA GENERAL")
        vent_materias_lista_general.state("zoomed") 
        
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")    
        
        funcion_etiquetas(vent_materias_lista_general,1,0,"Id","NOMBRE","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
            
        cursor1.execute("select idMateria,idMateria,nombreMateria,activo from materias" )    ## Consulta sql 
         
                            
        crear_lista_seleccion(vent_materias_lista_general,cursor1,mostrar_materia,1,2,3,4)   ## Muestro lista materia
                                                        
        conexion1.close()    ## Cierro conexion

def materias_lista_encurso():
    vent_materias_lista_en_curso= tk.Toplevel()            ## Nueva ventana profesores lista general
    vent_materias_lista_en_curso.title("MATERIAS LISTA EN CURSO")
    vent_materias_lista_en_curso.state("zoomed")
    ventana_fechas=tk.LabelFrame(vent_materias_lista_en_curso)
    ventana_fechas.grid(row=0,column=0)
    fecha_inicio= tk.StringVar(master=vent_materias_lista_en_curso, value="--")
    fecha_fin=tk.StringVar(master=vent_materias_lista_en_curso, value="--") 
    seleccionar_fechas(fecha_inicio,fecha_fin,ventana_fechas)
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    def buscar(fecha_inicio,fecha_fin):
        funcion_etiquetas(vent_materias_lista_en_curso,1,0,"Id","NOMBRE","ACTIVO")             # Creo las etiquetas en el tope de la pagina 
        inicio=fecha_inicio.get()  
        fin=fecha_fin.get()
        cursor1.execute("select materias.idMateria,materias.idMateria, nombreMateria, materias.activo from materias inner join cursadas on materias.idMAteria = cursadas.idMateria  where fechaInicio<=%aand fechaFin >=%a"% (fin,inicio) )    ## Consulta sql datos demograficos
        ventana_fechas.destroy()  
        bot_buscar.destroy() 
        lista_sin_duplicados=[]
        
        cursor=list(cursor1)
        for nuevo_valor in cursor:
            repetido=0
            for valor in lista_sin_duplicados:
                if nuevo_valor[0] == valor[0]:
                    repetido=1
                    break
            if not repetido:
                lista_sin_duplicados.append(nuevo_valor)
                       
        crear_lista_seleccion(vent_materias_lista_en_curso,lista_sin_duplicados,mostrar_materia,1,3,4,5)   ## Muestro lista escuela
                                                        # La seleccion de los botones lo levanto con la funcion mostrar_esc(idEscuela)
        conexion1.close()    ## Cierro conexion  
        
    bot_buscar=tk.Button(vent_materias_lista_en_curso,text="Buscar",command=lambda :buscar(fecha_inicio,fecha_fin)) 
    bot_buscar.grid(row=4,column=1)
        
def nueva_materia():            
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")
    query="select idMateria from  materias where nombreMateria ='--' order by idMateria desc limit 1"
    cursor1.execute(query) 
    val=list(cursor1)    
    if val==[]:        
        query="insert into materias set nombreMateria ='--'"                
        cursor1.execute(query)
        conexion1.commit()
    query="select idMateria from  materias where nombreMateria ='--' order by idMateria desc limit 1"
    cursor1.execute(query)             
    id_mt=list(cursor1)        
    id_mat=id_mt[0][0]
    materia1=Materia(id_mat)
    materia1.modificar_mat()             # Abro el elemento creado para modificaion             
    conexion1.close()    ## Cierro conexion        

def materias_baja():            
    vent_mat_de_baja= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_mat_de_baja.title("MATERIAS ACTIVAS")
    vent_mat_de_baja.state("zoomed")                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")            
    
    def mat_revivir(id):
        materia1=Materia(id)
        materia1.activo=0                
        materia1.grabar()
        vent_mat_de_baja.destroy()
        materias_baja()        
                        
    funcion_etiquetas(vent_mat_de_baja,1,0,"Id","NOMBRE")             # Creo las etiquetas en el tope de la pagina
        
    query="select idMateria,idMateria,nombreMateria from materias where activo =1"    
    cursor1.execute(query)    ## Consulta sql                     
    crear_lista_seleccion(vent_mat_de_baja,cursor1,mat_revivir,1,2,3)                                                
    conexion1.close()    ## Cierro conexion   


def materias_modificacion():
    vent_materias_modificacion= tk.Toplevel()           
    vent_materias_modificacion.title("MATERIAS")
    vent_materias_modificacion.state("zoomed")
                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")            
    
    def materia_modificar(id):
        materia1=Materia(id)                       
        materia1.modificar_mat()
        
                        
    funcion_etiquetas(vent_materias_modificacion,1,0,"Id","NOMBRE","ACTIVO")             # Creo las etiquetas en el tope de la pagina
        
    query="select idMateria,idMateria,nombreMateria,activo from materias "    
    cursor1.execute(query)    ## Consulta sql                     
    crear_lista_seleccion(vent_materias_modificacion,cursor1,materia_modificar,1,2,3,4)                                                
    conexion1.close()    ## Cierro conexion     
        
def materia_alta_existente():            
    vent_mat_de_alta= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_mat_de_alta.title("MATERIAS DADAS DE BAJA")
    vent_mat_de_alta.state("zoomed")                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values") 
    
    def mat_revivir(id):
        materia1=Materia(id)
        materia1.activo=1                
        materia1.grabar()
        vent_mat_de_alta.destroy()
        materia_alta_existente()        
            
    funcion_etiquetas(vent_mat_de_alta,1,0,"Id","NOMBRE")             # Creo las etiquetas en el tope de la pagina       
        
    cursor1.execute("select idMateria,idMateria,nombreMateria,activo from materias where activo=0")    ## Consulta sql 
                        
    crear_lista_seleccion(vent_mat_de_alta,cursor1,mat_revivir,1,2,3)  
                                                    
    conexion1.close()    ## Cierro conexion  

def materias_alta():        
    vent_materias_alta= tk.Toplevel()            ## Nueva ventana 
    vent_materias_alta.title("MATERIAS ALTA")
    vent_materias_alta.state("zoomed")       
    
    alto=3
    ancho=15
    vent_materias_alta.columnconfigure(0, weight=1)           # Hago que se expandan las filas y columnas
    vent_materias_alta.columnconfigure(1, weight=1)                 
    bot_nuevo=tk.Button(vent_materias_alta,text="Nueva materia",command=nueva_materia,height=alto,width=ancho)
    bot_existente=tk.Button(vent_materias_alta,text="Materia previamente dada de baja",command=materia_alta_existente,height=alto,width=30)
    bot_nuevo.grid(row=0,column=0)  
    bot_existente.grid(row=0,column=1)     


#
def materias():   
    marco_materias=tk.Label(raiz)
    deseleccionar(lista_botones)
    marco_materias.grid(row=0,column=1,rowspan=5,sticky="ns")
    marco_materias.rowconfigure(0,weight=1)
    marco_materias.rowconfigure(1,weight=1)
    marco_materias.rowconfigure(2,weight=1)
    marco_materias.rowconfigure(3,weight=1)
    marco_materias.rowconfigure(4,weight=1)
    marco_materias.rowconfigure(5,weight=1)
    cartel_materias=tk.Label(raiz,text="MATERIAS",fg="dark slate blue",font=("arial",30))
    cartel_materias.grid(row=0,column=0)
    bot_materias_alta=tk.Button(marco_materias,text="Alta",command=materias_alta,height=alto,width=ancho)    
    bot_materias_alta.grid(row=0,column=1)
    bot_materias_baja=tk.Button(marco_materias,text="Baja",command=materias_baja,height=alto,width=ancho)    
    bot_materias_baja.grid(row=1,column=1)
    bot_materias_modificacion=tk.Button(marco_materias,text="Modificación",command=materias_modificacion,height=alto,width=ancho)    
    bot_materias_modificacion.grid(row=2,column=1)
    bot_materias_lista_gral=tk.Button(marco_materias,text="Lista general",command=materias_lista_gral,height=alto,width=ancho)    
    bot_materias_lista_gral.grid(row=3,column=1)
    bot_materias_lista_encurso=tk.Button(marco_materias,text="Lista en curso",command=materias_lista_encurso,height=alto,width=ancho)    
    bot_materias_lista_encurso.grid(row=4,column=1)
    bot_cancelar=tk.Button(raiz,text="Cancelar",command=lambda:cancelar(marco_materias,bot_cancelar,cartel_materias),height=alto,width=ancho)
    bot_cancelar.grid(row=1,column=0)
 
 
#########################################################################################################################################
###############################################         VENTANA  MATERIALES           ###################################################
#########################################################################################################################################

def materiales_lista_gral():
        vent_materiales_lista_gral= tk.Toplevel()            ## Nueva ventana materias lista general
        vent_materiales_lista_gral.title(" MATERIALES LISTA GENERAL")
        vent_materiales_lista_gral.state("zoomed") 
        
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")    
        
        funcion_etiquetas(vent_materiales_lista_gral,1,0,"id","NOMBRE","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
            
        cursor1.execute("select idMAterial,idMAterial,nombreMaterial,activo from materiales" )    ## Consulta sql 
        
        def mostrar_material(id):
            material1=Material(id)            
            material1.mostrar_mat()
                
                
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")    
            
            # funcion_etiquetas(vent_materiales_lista_gral,1,0,"NOMBRE","DESCRIPCION","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
                
            cursor1.execute("select materias.idMateria,nombreMateria from materias inner join materiasMateriales on materias.idMateria=materiasMateriales.idMateria where materiasMateriales.idMaterial=%a"%id )    ## Consulta sql
            lista=list(cursor1)
            
            marco_materias=tk.LabelFrame(material1.vent_mat,text="Materias que utilizan este material")
            marco_materias.grid(row=0,column=3,sticky="w",padx=40)
            cartel_id=tk.Label(marco_materias,text="Id_material")
            cartel_id.grid(row=0,column=0,sticky="n",pady=15)
            cartel_nombre_materia=tk.Label(marco_materias,text="Nombre_material")
            cartel_nombre_materia.grid(row=0,column=1,sticky="nw",padx=15,pady=15)
            
            k=1 
            if len(lista):
                for i in lista:
                    id=tk.Label(marco_materias,text=i[0])
                    id.grid(row=k,column=0)
                    nombre=tk.Label(marco_materias,text=i[1])
                    nombre.grid(row=k,column=1,sticky="w",padx=15)
                    k+=1
            else:
                id=tk.Label(marco_materias,text="--")
                id.grid(row=1,column=0)
                nombre=tk.Label(marco_materias,text="--")
                nombre.grid(row=1,column=1,sticky="w",padx=15)
                    
                
            
            conexion1.close() 
                           
        crear_lista_seleccion(vent_materiales_lista_gral,cursor1,mostrar_material,1,2,3,4)   ## Muestro lista prof
                                                        # La seleccion de los botones lo levanto con la funcion mostrar_prof(idProfesor)
        conexion1.close()    ## Cierro conexion
        
               
def materiales_lista_encurso():
    
    vent_materiales_lista_encurso= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_materiales_lista_encurso.title(" MATERIALES LISTA EN CURSO")
    vent_materiales_lista_encurso.state("zoomed") 
    ventana_fechas=tk.LabelFrame(vent_materiales_lista_encurso)
    ventana_fechas.grid(row=0,column=0)
    
    fecha_inicio= tk.StringVar(master=vent_materiales_lista_encurso, value="--")
    fecha_fin=tk.StringVar(master=vent_materiales_lista_encurso, value="--") 
    seleccionar_fechas(fecha_inicio,fecha_fin,ventana_fechas) 
    
    def buscar(fecha_inicio,fecha_fin):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")    
        inicio=fecha_inicio.get()  
        fin=fecha_fin.get()    
        cursor1.execute("select materiales.idMaterial,materiales.idMaterial,nombreMaterial,materiasMateriales.idMAteria,nombreMateria ,cursadas.idEscuela,nombreEscuela from materiales inner join materiasMateriales on materiasMateriales.idMaterial=materiales.idMaterial  inner join cursadas on materiasMateriales.idMateria=cursadas.idMateria inner join materias on materiasMateriales.idMateria=materias.idMateria inner join escuelas on cursadas.idEscuela=escuelas.idEscuela where fechaInicio<=%aand fechaFin >=%a"% (fin,inicio) )    ## Consulta sql 
        funcion_etiquetas(vent_materiales_lista_encurso,1,0,"Id MATERIAL","NOMBRE MATERIAL","ID MATERIA","NOMBRE MATERIA","Id ESCUELA","NOMBRE ESCUELA")
        crear_lista_seleccion(vent_materiales_lista_encurso,cursor1,mostrar_material,0,1,2,3,4,5,6) 
        ventana_fechas.destroy()  
        bot_buscar.destroy() 
    
    bot_buscar=tk.Button(vent_materiales_lista_encurso,text="Buscar",command=lambda :buscar(fecha_inicio,fecha_fin)) 
    bot_buscar.grid(row=4,column=1)
    
    def mostrar_material(id):
        material1=Material(id)            
        material1.mostrar_mat()
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")    
        
        funcion_etiquetas(vent_materiales_lista_encurso,1,0,"Id","NOMBRE","DESCRIPCION","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
            
        cursor1.execute("select materias.idMateria,nombreMateria from materias inner join materiasMateriales on materias.idMateria=materiasMateriales.idMateria where materiasMateriales.idMaterial=%a"%id )    ## Consulta sql
        lista=list(cursor1)
        
        marco_materias=tk.LabelFrame(material1.vent_mat,text="Materias que utilizan este material")
        marco_materias.grid(row=0,column=3,sticky="w",padx=40)
        cartel_id=tk.Label(marco_materias,text="Id_material")
        cartel_id.grid(row=0,column=0,sticky="n",pady=15)
        cartel_nombre_materia=tk.Label(marco_materias,text="Nombre_material")
        cartel_nombre_materia.grid(row=0,column=1,sticky="nw",padx=15,pady=15)
        
        k=1 
        if len(lista):
            for i in lista:
                id=tk.Label(marco_materias,text=i[0])
                id.grid(row=k,column=0)
                nombre=tk.Label(marco_materias,text=i[1])
                nombre.grid(row=k,column=1,sticky="w",padx=15)
                k+=1
        else:
            id=tk.Label(marco_materias,text="--")
            id.grid(row=1,column=0)
            nombre=tk.Label(marco_materias,text="--")
            nombre.grid(row=1,column=1,sticky="w",padx=15)
                            
        conexion1.close() 

def nuevo_material():            
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")
    query="select idMaterial from  materiales where nombreMaterial ='--' order by idMaterial desc limit 1"
    cursor1.execute(query)              # saco el id del ultimo elemento que es el que acabo de crear
    id_mt=list(cursor1)    
    if id_mt==[]:    
        query="insert into materiales set nombreMaterial ='--'"                
        cursor1.execute(query)
        conexion1.commit()
    query="select idMaterial from  materiales where nombreMaterial ='--' order by idMaterial desc limit 1"
    cursor1.execute(query)              # saco el id del ultimo elemento que es el que acabo de crear
    id_mt=list(cursor1)        
    id_mat=id_mt[0][0]
    material1=Material(id_mat)
    material1.modificar_mat()             # Abro el elemento creado para modificaion             
    conexion1.close()    ## Cierro conexion        



def materiales_baja():            
    vent_materiales_de_baja= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_materiales_de_baja.title("MATERIALES ACTIVOS")
    vent_materiales_de_baja.state("zoomed")                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")            
    
    def materiales_revivir(id):
        material1=Material(id)
        material1.activo=0                
        material1.grabar()
        vent_materiales_de_baja.destroy()
        materiales_baja()        
                        
    funcion_etiquetas(vent_materiales_de_baja,1,0,"Id","NOMBRE")             # Creo las etiquetas en el tope de la pagina
        
    query="select idMaterial,idmaterial,nombreMaterial from materiales where activo =1"    
    cursor1.execute(query)    ## Consulta sql                     
    crear_lista_seleccion(vent_materiales_de_baja,cursor1,materiales_revivir,1,2,3)                                                
    conexion1.close()    ## Cierro conexion       
  
def materiales_modificacion():
    vent_materiales_modificacion= tk.Toplevel()           
    vent_materiales_modificacion.title("MODIFICAR MATERIALES")
    vent_materiales_modificacion.state("zoomed")
                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")            
    
    def material_modificar(id):
        material1=Material(id)                       
        material1.modificar_mat()
                        
    funcion_etiquetas(vent_materiales_modificacion,1,0,"Id","NOMBRE","ACTIVO")             # Creo las etiquetas en el tope de la pagina
        
    query="select idMAterial,idMaterial,nombreMaterial,activo from materiales "    
    cursor1.execute(query)    ## Consulta sql                     
    crear_lista_seleccion(vent_materiales_modificacion,cursor1, material_modificar,1,2,3,4)                               
    conexion1.close()    ## Cierro conexion
    
                         
def materiales_alta_existente():            
    vent_materiales_de_alta= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_materiales_de_alta.title("MATERIALES DADOS DE BAJA")
    vent_materiales_de_alta.state("zoomed")                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values") 
    
    def material_revivir(id):
        material1=Material(id)
        material1.activo=1                
        material1.grabar()
        vent_materiales_de_alta.destroy()
        materiales_alta_existente()        
            
    funcion_etiquetas(vent_materiales_de_alta,1,0,"iD","NOMBRE")             # Creo las etiquetas en el tope de la pagina       
        
    cursor1.execute("select idMaterial,idMaterial,nombreMaterial from materiales where activo=0")    ## Consulta sql 
                        
    crear_lista_seleccion(vent_materiales_de_alta,cursor1,material_revivir,1,2,3)  
                                                    
    conexion1.close()    ## Cierro conexion 
   
def materiales_alta():        
    vent_materiales_alta= tk.Toplevel()            ## Nueva ventana 
    vent_materiales_alta.title("MATERIALES ALTA")
    vent_materiales_alta.state("zoomed")       
    
    alto=3
    ancho=15
    vent_materiales_alta.columnconfigure(0, weight=1)           # Hago que se expandan las filas y columnas
    vent_materiales_alta.columnconfigure(1, weight=1)                 
    bot_nuevo=tk.Button(vent_materiales_alta,text="Nuevo material",command=nuevo_material,height=alto,width=ancho)
    bot_existente=tk.Button(vent_materiales_alta,text="Material previamente dado de baja",command=materiales_alta_existente,height=alto,width=30)
    bot_nuevo.grid(row=0,column=0)  
    bot_existente.grid(row=0,column=1)

def materiales():
    marco_materiales=tk.Label(raiz)
    deseleccionar(lista_botones)
    marco_materiales.grid(row=0,column=1,rowspan=5,sticky="ns")
    marco_materiales.rowconfigure(0,weight=1)
    marco_materiales.rowconfigure(1,weight=1)
    marco_materiales.rowconfigure(2,weight=1)
    marco_materiales.rowconfigure(3,weight=1)
    marco_materiales.rowconfigure(4,weight=1)
    marco_materiales.rowconfigure(5,weight=1)
    cartel_materiales=tk.Label(raiz,text="MATERIALES",fg="dark slate blue",font=("arial",30))
    cartel_materiales.grid(row=0,column=0)
    bot_materiales_alta=tk.Button(marco_materiales,text="Alta",command=materiales_alta,height=alto,width=ancho)    
    bot_materiales_alta.grid(row=0,column=1)
    bot_materiales_baja=tk.Button(marco_materiales,text="Baja",command=materiales_baja,height=alto,width=ancho)    
    bot_materiales_baja.grid(row=1,column=1)
    bot_materiales_modificacion=tk.Button(marco_materiales,text="Modificación",command=materiales_modificacion,height=alto,width=ancho)    
    bot_materiales_modificacion.grid(row=2,column=1)
    bot_materiales_lista_gral=tk.Button(marco_materiales,text="Lista general",command=materiales_lista_gral,height=alto,width=ancho)    
    bot_materiales_lista_gral.grid(row=3,column=1)
    bot_materiales_lista_encurso=tk.Button(marco_materiales,text="Lista en curso",command=materiales_lista_encurso,height=alto,width=ancho)    
    bot_materiales_lista_encurso.grid(row=4,column=1)
    bot_cancelar=tk.Button(raiz,text="Cancelar",command=lambda:cancelar(marco_materiales,bot_cancelar,cartel_materiales),height=alto,width=ancho)
    bot_cancelar.grid(row=1,column=0)
  
########################################################################################################################################
#####################################################        VENTANA  ESCUELAS      ####################################################
########################################################################################################################################

def modificar_esc(id):    
    escuela1=Escuela(id)   #### Creo el objeto profesor1 con id_profesor
    escuela1.modificar()
    
    
def mostrar_esc(id_escuela):
        escuela1=Escuela(id_escuela)
        escuela1.mostrar()         
       
def escuelas_lista_gral():
    vent_escuelas_lista_general= tk.Toplevel()            ## Nueva ventana profesores lista general
    vent_escuelas_lista_general.title("ESCUELAS LISTA GENERAL")
    vent_escuelas_lista_general.state("zoomed")
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_escuelas_lista_general,1,0,"NOMBRE","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")             # Creo las etiquetas en el tope de la pagina
        
        
    cursor1.execute("select idEscuela, nombreEscuela, estado, localidad, codigoPostal, calle,numero, piso, departamento, telefono, mail, activo from escuelas inner join estados on escuelas.idEstado = estados.idEstado inner join localidades on escuelas.idLocalidad = localidades.idLocalidad" )    ## Consulta sql datos demograficos
                        
    crear_lista_seleccion(vent_escuelas_lista_general,cursor1,mostrar_esc,1,3,4,5,6,7,8,9,10,11,12,13)   ## Muestro lista escuela
                                                    # La seleccion de los botones lo levanto con la funcion mostrar_esc(idEscuela)
    conexion1.close()    ## Cierro conexion
    

def escuelas_lista_encurso():
    vent_escuelas_lista_en_curso= tk.Toplevel()            ## Nueva ventana profesores lista general
    vent_escuelas_lista_en_curso.title("ESCUELAS LISTA EN CURSO")
    vent_escuelas_lista_en_curso.state("zoomed")
    ventana_fechas=tk.LabelFrame(vent_escuelas_lista_en_curso)
    ventana_fechas.grid(row=0,column=0)
    fecha_inicio= tk.StringVar(master=vent_escuelas_lista_en_curso, value="--")
    fecha_fin=tk.StringVar(master=vent_escuelas_lista_en_curso, value="--") 
    seleccionar_fechas(fecha_inicio,fecha_fin,ventana_fechas)
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    def buscar(fecha_inicio,fecha_fin):
        funcion_etiquetas(vent_escuelas_lista_en_curso,1,0,"NOMBRE","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL")             # Creo las etiquetas en el tope de la pagina
        inicio=fecha_inicio.get()  
        fin=fecha_fin.get()
        cursor1.execute("select escuelas.idEscuela, nombreEscuela, estado, localidad, codigoPostal, calle,numero, piso, departamento, telefono, mail from escuelas inner join estados on escuelas.idEstado = estados.idEstado inner join localidades on escuelas.idLocalidad = localidades.idLocalidad inner join cursadas on escuelas.idEscuela= cursadas.idEscuela where fechaInicio<=%aand fechaFin >=%a"% (fin,inicio) )    ## Consulta sql datos demograficos
        ventana_fechas.destroy()  
        bot_buscar.destroy() 
        lista_sin_duplicados=[]
        
        cursor=list(cursor1)
        
        for nuevo_valor in cursor:
            repetido=0
            for valor in lista_sin_duplicados:
                if nuevo_valor[0] == valor[0]:
                    repetido=1
                    break
            if not repetido:
                lista_sin_duplicados.append(nuevo_valor)
                       
        crear_lista_seleccion(vent_escuelas_lista_en_curso,lista_sin_duplicados,mostrar_esc,1,3,4,5,6,7,8,9,10,11,12)   ## Muestro lista escuela
                                                        # La seleccion de los botones lo levanto con la funcion mostrar_esc(idEscuela)
        conexion1.close()    ## Cierro conexion  
        
    bot_buscar=tk.Button(vent_escuelas_lista_en_curso,text="Buscar",command=lambda :buscar(fecha_inicio,fecha_fin)) 
    bot_buscar.grid(row=4,column=1)
   
def escuelas_modificacion():    
    vent_escuelas_modificacion= tk.Toplevel()            ## Nueva ventana escuelas lista general
    vent_escuelas_modificacion.title("ESCUELAS MODIFICACION")
    vent_escuelas_modificacion.state("zoomed")
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_escuelas_modificacion,1,0,"Id","NOMBRE","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")             # Creo las etiquetas en el tope de la pagina
        
        
    cursor1.execute("select idEscuela,idEscuela, nombreEscuela, estado, localidad, codigoPostal, calle,numero,  piso, departamento, telefono, mail, activo from escuelas inner join estados on escuelas.idEstado = estados.idEstado inner join localidades on escuelas.idLocalidad = localidades.idLocalidad" )    ## Consulta sql datos demograficos
    
                                                                            
    crear_lista_seleccion(vent_escuelas_modificacion,cursor1,modificar_esc,1,3,4,5,6,7,8,9,10,11,12,13,14)   ## Muestro lista escuelas
                                                    # La seleccion de los botones lo levanto con la funcion mostrar_esc(idEscuela)
    conexion1.close()    ## Cierro conexion

def escuelas_baja():      
    vent_escuelas_baja= tk.Toplevel()            ## Nueva ventana 
    vent_escuelas_baja.title("ESCUELAS BAJA")
    vent_escuelas_baja.state("zoomed")
    
    def baja_esc(id):
        escuela1=Escuela(id)           
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        query=("update escuelas set activo = 0 where idEscuela=%a"%(escuela1.id))
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_escuelas_baja.destroy()
        escuelas_baja()

    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_escuelas_baja,1,0,"NOMBRE","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")             # Creo las etiquetas en el tope de la pagina
    cursor1.execute("select idEscuela, nombreEscuela,  estado, localidad, codigoPostal, calle,numero,  piso ,departamento,  telefono, mail, activo from escuelas inner join estados on escuelas.idEstado = estados.idEstado inner join localidades on escuelas.idLocalidad = localidades.idLocalidad  where activo =1" )    ## Consulta sql datos demograficos
    crear_lista_seleccion(vent_escuelas_baja,cursor1,baja_esc,1,3,4,5,6,7,8,9,10,11,12,13)   ## Muestro lista esc
                                                    # La seleccion de los botones lo levanto con la funcion baja_esc(idEscuela)
    conexion1.close()    ## Cierro conexion
 
def escuelas_alta():        
    vent_escuelas_alta= tk.Toplevel()            ## Nueva ventana 
    vent_escuelas_alta.title("ESCUELAS ALTA")
    vent_escuelas_alta.state("zoomed")
    
    def nueva_esc():            
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        cursor1.execute("select idEscuela from escuelas where nombreEscuela = '--' order by idEscuela desc limit 1")
        id_pr=list(cursor1)
        if id_pr==[]:
            cursor1.execute("insert into escuelas(nombreEscuela)values ('--') ")         
            conexion1.commit()
        cursor1.execute("select idEscuela from escuelas where nombreEscuela = '--' order by idEscuela desc limit 1")
        id_pr=list(cursor1)
        id_esc=id_pr[0][0]
        modificar_esc(id_esc)
        conexion1.close()    ## Cierro conexion
    
    def alta_existente():            
        vent_escuelas_de_alta= tk.Toplevel()            ## Nueva ventana profesores lista general
        vent_escuelas_de_alta.title("ESCUELAS DADAS DE BAJA")
        vent_escuelas_de_alta.state("zoomed")                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
           
        def escuela_revivir(id):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")            
            cursor1.execute("update escuelas set activo = 1 where idEscuela=%r "%id)
            conexion1.commit()
            conexion1.close()    ## Cierro conexion
            vent_escuelas_de_alta.destroy()
            alta_existente()
        
        funcion_etiquetas(vent_escuelas_de_alta,1,0,"NOMBRE","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
            
        cursor1.execute("select idEscuela, nombreEscuela, estado, localidad, codigoPostal, calle,numero, piso, departamento, telefono, mail, activo from escuelas inner join estados on escuelas.idEstado = estados.idEstado inner join localidades on escuelas.idLocalidad = localidades.idLocalidad where activo = 0" )    ## Consulta sql datos demograficos para profesores dados de baja
                            
        crear_lista_seleccion(vent_escuelas_de_alta,cursor1,escuela_revivir,1,2,3,4,5,6,7,8,9,10,11,12)   ## Muestro lista escuela
                                                    # La seleccion de los botones lo levanto con la funcion escuela_revivir(idEscuela)
        conexion1.close()    ## Cierro conexion
           
    
    alto=3
    ancho=15
    vent_escuelas_alta.columnconfigure(0, weight=1)           # Hago que se expandan las filas y columnas
    vent_escuelas_alta.columnconfigure(1, weight=1)                 
    bot_nuevo=tk.Button(vent_escuelas_alta,text="Nueva escuela",command=nueva_esc,height=alto,width=ancho)
    bot_existente=tk.Button(vent_escuelas_alta,text="Escuela previamente dado de baja",command=alta_existente,height=alto,width=30)
    bot_nuevo.grid(row=0,column=0)  
    bot_existente.grid(row=0,column=1)       

#    
def escuelas():                                     # Crea botones en la nueva pantalla escuelas
    deseleccionar(lista_botones)
    marco_escuelas=tk.Label(raiz)
    marco_escuelas.grid(row=0,column=1,rowspan=5,sticky="ns")
    marco_escuelas.rowconfigure(0,weight=1)
    marco_escuelas.rowconfigure(1,weight=1)
    marco_escuelas.rowconfigure(2,weight=1)
    marco_escuelas.rowconfigure(3,weight=1)
    marco_escuelas.rowconfigure(4,weight=1)
    marco_escuelas.rowconfigure(5,weight=1)
    cartel_escuelas=tk.Label(raiz,text="ESCUELAS",fg="dark slate blue",font=("arial",30))
    cartel_escuelas.grid(row=0,column=0)
    bot_escuelas_alta=tk.Button(marco_escuelas,text="Alta",command=escuelas_alta,height=alto,width=ancho)    
    bot_escuelas_alta.grid(row=0,column=1)
    bot_escuelas_baja=tk.Button(marco_escuelas,text="Baja",command=escuelas_baja,height=alto,width=ancho)    
    bot_escuelas_baja.grid(row=1,column=1)
    bot_escuelas_modificacion=tk.Button(marco_escuelas,text="Modificación",command=escuelas_modificacion,height=alto,width=ancho)    
    bot_escuelas_modificacion.grid(row=2,column=1)
    bot_escuelas_lista_gral=tk.Button(marco_escuelas,text="Lista general",command=escuelas_lista_gral,height=alto,width=ancho)    
    bot_escuelas_lista_gral.grid(row=3,column=1)
    bot_escuelas_lista_encurso=tk.Button(marco_escuelas,text="Lista en curso",command=escuelas_lista_encurso,height=alto,width=ancho)    
    bot_escuelas_lista_encurso.grid(row=4,column=1)
    bot_cancelar=tk.Button(raiz,text="Cancelar",command=lambda:cancelar(marco_escuelas,bot_cancelar,cartel_escuelas),height=alto,width=ancho)
    bot_cancelar.grid(row=1,column=0)
    


########################################################################################################################################
#####################################################        VENTANA  CURSADAS      ####################################################
########################################################################################################################################
  
def cursadas_alta():
           
    vent_cursadas_alta= tk.Toplevel()            ## Nueva ventana 
    vent_cursadas_alta.title("CURSADAS ALTA")
    vent_cursadas_alta.state("zoomed")
    
    
    def cursada_nueva():          
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        cursor1.execute("select idCursada from cursadas where idMateria = 0 order by idCursada desc limit 1")
        id_pr=list(cursor1)
        if id_pr==[]:
            cursor1.execute("insert into cursadas(idMateria)values (0) ")         
            conexion1.commit()
            cursor1.execute("select idCursada from cursadas where idMateria = 0 order by idCursada desc limit 1")
            id_pr=list(cursor1)
        id_curs=int(id_pr[0][0])
        cursada1=Cursadas(id_curs)
        cursada1.modificar()
        conexion1.close()    ## Cierro conexion
        
    def alta_existente():            
        vent_cursadas_de_alta= tk.Toplevel()            ## Nueva ventana profesores lista general
        vent_cursadas_de_alta.title("CURSADAS DADAS DE BAJA")
        vent_cursadas_de_alta.state("zoomed")                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
           
        def cursada_revivir(id):
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")            
            cursor1.execute("update cursadas set activo = 1 where idCursada=%r "%id)
            conexion1.commit()
            conexion1.close()    ## Cierro conexion
            vent_cursadas_de_alta.destroy()
            alta_existente()
        
        funcion_etiquetas(vent_cursadas_de_alta,1,0,"Id","Nombre escuela","Nombre profesor","Año","Cuatrimestre","Día","Hora inicio","Hora fin","Id tarifa","Fecha inicio","Fecha fin","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
            
        cursor1.execute("select cursadas.idCursada,cursadas.idCursada, nombreEscuela, nombreProfesor, anios.anio, cursadas.cuatrimestre, dia,horaInicio, horaFin, cursadas.idTarifa,fechaInicio, fechaFin, cursadas.activo from cursadas inner join escuelas on escuelas.idEscuela = cursadas.idEscuela inner join profesores on profesores.idProfesor = cursadas.idProfesor inner join anios on anios.idAnio=cursadas.idAnio inner join dias on dias.idDia=cursadas.idDia inner join horaInicio on horaInicio.idHoraInicio=cursadas.idHoraInicio inner join horaFin on horaFin.idHoraFin=cursadas.idHoraFin where cursadas.activo = 0 ")   
        crear_lista_seleccion(vent_cursadas_de_alta,cursor1,cursada_revivir,1,2,3,4,5,6,7,8,9,10,11,12,13)  
        conexion1.close()    ## Cierro conexion
           
    
    alto=3
    ancho=15
    vent_cursadas_alta.columnconfigure(0, weight=1)           # Hago que se expandan las filas y columnas
    vent_cursadas_alta.columnconfigure(1, weight=1)                 
    bot_nuevo=tk.Button(vent_cursadas_alta,text="Nueva cursada",command=cursada_nueva,height=alto,width=ancho)
    bot_existente=tk.Button(vent_cursadas_alta,text="Cursada previamente dada de baja",command=alta_existente,height=alto,width=30)
    bot_nuevo.grid(row=0,column=0)  
    bot_existente.grid(row=0,column=1)       

def cursadas_baja():      
    vent_cursadas_baja= tk.Toplevel()            ## Nueva ventana 
    vent_cursadas_baja.title("CURSADAS BAJA")
    vent_cursadas_baja.state("zoomed")
    
    def baja_cursada(id):
        cursada1=Cursadas(id)           
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        query=("update cursadas set activo = 0 where idCursada=%a"%(cursada1.id))
        cursor1.execute(query)
        conexion1.commit()
        conexion1.close()    ## Cierro conexion
        vent_cursadas_baja.destroy()
        cursadas_baja()

    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_cursadas_baja,1,0,"Id","Nombre escuela","Nombre profesor","Año","Cuatrimestre","Día","Hora inicio","Hora fin","Id tarifa","Fecha inicio","Fecha fin","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
        
    cursor1.execute("select cursadas.idCursada,cursadas.idCursada, nombreEscuela, nombreProfesor, anios.anio, cursadas.cuatrimestre, dia,horaInicio, horaFin, cursadas.idTarifa,fechaInicio, fechaFin, cursadas.activo from cursadas inner join escuelas on escuelas.idEscuela = cursadas.idEscuela inner join profesores on profesores.idProfesor = cursadas.idProfesor inner join anios on anios.idAnio=cursadas.idAnio inner join dias on dias.idDia=cursadas.idDia inner join horaInicio on horaInicio.idHoraInicio=cursadas.idHoraInicio inner join horaFin on horaFin.idHoraFin=cursadas.idHoraFin where cursadas.activo = 1 ")   
    crear_lista_seleccion(vent_cursadas_baja,cursor1,baja_cursada,1,2,3,4,5,6,7,8,9,10,11,12,13)  
    conexion1.close()    ## Cierro conexion
    
def cursadas_modificacion():
    vent_cursadas_baja= tk.Toplevel()            ## Nueva ventana 
    vent_cursadas_baja.title("CURSADAS MODIFICACION")
    vent_cursadas_baja.state("zoomed")
    
    def modificar_cursada(id):
        print(id)
        cursada1=Cursadas(id)
        cursada1.modificar()
        pass
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_cursadas_baja,1,0,"Id","Nombre escuela","Nombre profesor","Año","Cuatrimestre","Día","Hora inicio","Hora fin","Id tarifa","Fecha inicio","Fecha fin","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
        
    cursor1.execute("select cursadas.idCursada,cursadas.idCursada, nombreEscuela, nombreProfesor, anios.anio, cursadas.cuatrimestre, dia,horaInicio, horaFin, cursadas.idTarifa,fechaInicio, fechaFin, cursadas.activo from cursadas inner join escuelas on escuelas.idEscuela = cursadas.idEscuela inner join profesores on profesores.idProfesor = cursadas.idProfesor inner join anios on anios.idAnio=cursadas.idAnio inner join dias on dias.idDia=cursadas.idDia inner join horaInicio on horaInicio.idHoraInicio=cursadas.idHoraInicio inner join horaFin on horaFin.idHoraFin=cursadas.idHoraFin where cursadas.activo = 1 ")   
    crear_lista_seleccion(vent_cursadas_baja,cursor1,modificar_cursada,1,2,3,4,5,6,7,8,9,10,11,12,13)  
    conexion1.close()    ## Cierro conexion
    
def cursadas_lista_gral():
    vent_cursadas_lista_gral= tk.Toplevel()            ## Nueva ventana 
    vent_cursadas_lista_gral.title("CURSADAS LISTA GENERAL")
    vent_cursadas_lista_gral.state("zoomed")
    
    def mostrar_cursada(id):
        cursada1=Cursadas(id)
        cursada1.mostrar()
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")    
    
    funcion_etiquetas(vent_cursadas_lista_gral,1,0,"Id","Nombre escuela","Nombre profesor","Año","Cuatrimestre","Día","Hora inicio","Hora fin","Id tarifa","Fecha inicio","Fecha fin","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
        
    cursor1.execute("select cursadas.idCursada,cursadas.idCursada, nombreEscuela, nombreProfesor, anios.anio, cursadas.cuatrimestre, dia,horaInicio, horaFin, cursadas.idTarifa,fechaInicio, fechaFin, cursadas.activo from cursadas inner join escuelas on escuelas.idEscuela = cursadas.idEscuela inner join profesores on profesores.idProfesor = cursadas.idProfesor inner join anios on anios.idAnio=cursadas.idAnio inner join dias on dias.idDia=cursadas.idDia inner join horaInicio on horaInicio.idHoraInicio=cursadas.idHoraInicio inner join horaFin on horaFin.idHoraFin=cursadas.idHoraFin")# where cursadas.activo = 1 ")   
    crear_lista_seleccion(vent_cursadas_lista_gral,cursor1,mostrar_cursada,1,2,3,4,5,6,7,8,9,10,11,12,13)  
    conexion1.close()    ## Cierro conexion

def cursadas_lista_encurso():  
    vent_cursadas_lista_encurso= tk.Toplevel()            ## Nueva ventana 
    vent_cursadas_lista_encurso.title("CURSADAS LISTA GENERAL")
    vent_cursadas_lista_encurso.state("zoomed")
    ventana_fechas=tk.LabelFrame(vent_cursadas_lista_encurso)
    ventana_fechas.grid(row=0,column=0)
    fecha_inicio= tk.StringVar(master=vent_cursadas_lista_encurso, value="--")
    fecha_fin=tk.StringVar(master=vent_cursadas_lista_encurso, value="--") 
    seleccionar_fechas(fecha_inicio,fecha_fin,ventana_fechas)
    
    def buscar(fecha_inicio,fecha_fin):
        def mostrar_cursada(id):
            cursada1=Cursadas(id)
            cursada1.mostrar()
        
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")    
        
        funcion_etiquetas(vent_cursadas_lista_encurso,1,0,"Id","Nombre escuela","Nombre profesor","Año","Cuatrimestre","Día","Hora inicio","Hora fin","Id tarifa","Fecha inicio","Fecha fin","ACTIVO")             # Creo las etiquetas en el tope de la pagina            
        inicio=fecha_inicio.get()  
        fin=fecha_fin.get()    
        cursor1.execute("select cursadas.idCursada,cursadas.idCursada, nombreEscuela, nombreProfesor, anios.anio, cursadas.cuatrimestre, dia,horaInicio, horaFin, cursadas.idTarifa,fechaInicio, fechaFin, cursadas.activo from cursadas inner join escuelas on escuelas.idEscuela = cursadas.idEscuela inner join profesores on profesores.idProfesor = cursadas.idProfesor inner join anios on anios.idAnio=cursadas.idAnio inner join dias on dias.idDia=cursadas.idDia inner join horaInicio on horaInicio.idHoraInicio=cursadas.idHoraInicio inner join horaFin on horaFin.idHoraFin=cursadas.idHoraFin where  fechaInicio<=%aand fechaFin >=%a "% (fin,inicio))   
        
        ventana_fechas.destroy()  
        bot_buscar.destroy() 
        crear_lista_seleccion(vent_cursadas_lista_encurso,cursor1,mostrar_cursada,1,2,3,4,5,6,7,8,9,10,11,12,13)  
        conexion1.close()    ## Cierro conexion
        
    bot_buscar=tk.Button(vent_cursadas_lista_encurso,text="Buscar",command=lambda :buscar(fecha_inicio,fecha_fin)) 
    bot_buscar.grid(row=4,column=1)

def cursadas():    
    marco_cursadas=tk.Label(raiz)
    deseleccionar(lista_botones)
    marco_cursadas.grid(row=0,column=1,rowspan=5,sticky="ns")
    marco_cursadas.rowconfigure(0,weight=1)
    marco_cursadas.rowconfigure(1,weight=1)
    marco_cursadas.rowconfigure(2,weight=1)
    marco_cursadas.rowconfigure(3,weight=1)
    marco_cursadas.rowconfigure(4,weight=1)
    marco_cursadas.rowconfigure(5,weight=1)
    cartel_cursadas=tk.Label(raiz,text="CURSADAS",fg="dark slate blue",font=("arial",30))
    cartel_cursadas.grid(row=0,column=0)
    bot_cursadas_alta=tk.Button(marco_cursadas,text="Alta",command=cursadas_alta,height=alto,width=ancho)    
    bot_cursadas_alta.grid(row=0,column=1)
    bot_cursadas_baja=tk.Button(marco_cursadas,text="Baja",command=cursadas_baja,height=alto,width=ancho)    
    bot_cursadas_baja.grid(row=1,column=1)
    bot_cursadas_modificacion=tk.Button(marco_cursadas,text="Modificación",command=cursadas_modificacion,height=alto,width=ancho)    
    bot_cursadas_modificacion.grid(row=2,column=1)
    bot_cursadas_lista_gral=tk.Button(marco_cursadas,text="Lista general",command=cursadas_lista_gral,height=alto,width=ancho)    
    bot_cursadas_lista_gral.grid(row=3,column=1)
    bot_cursadas_lista_encurso=tk.Button(marco_cursadas,text="Lista en curso",command=cursadas_lista_encurso,height=alto,width=ancho)    
    bot_cursadas_lista_encurso.grid(row=4,column=1)
    bot_cancelar=tk.Button(raiz,text="Cancelar",command=lambda:cancelar(marco_cursadas,bot_cancelar,cartel_cursadas),height=alto,width=ancho)
    bot_cancelar.grid(row=1,column=0)
   

########################################################################################################################################
#####################################################        VENTANA  TARIFAS       ####################################################
########################################################################################################################################
                    
def nueva_tarifa():            
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")
    query="select idTarifa from tarifas where nombreTarifa ='--' order by idTarifa desc limit 1"
    cursor1.execute(query)              
    id_tar=list(cursor1)   
    if id_tar ==[]:     
        query="insert into tarifas set nombreTarifa ='--'"                
        cursor1.execute(query)
        conexion1.commit()
    query="select idTarifa from tarifas where nombreTarifa ='--' order by idTarifa desc limit 1"
    cursor1.execute(query)              
    id_tar=list(cursor1)        
    id_tarifa=id_tar[0][0]
    tarifa1=Tarifa(id_tarifa)
    tarifa1.modificar()             # Abro el elemento creado para modificaion             
    conexion1.close()    ## Cierro conexion        

def tarifas_alta_existente():
    vent_tarifas_de_alta= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_tarifas_de_alta.title("TARIFAS DADAS DE BAJA")
    vent_tarifas_de_alta.state("zoomed")                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values") 
    
    def tarifa_revivir(id):
        # tarifa1=Tarifa(id)
        # tarifa1.activo=1                
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        cursor1.execute("update tarifas set activo=1 where idTarifa=%a"%id)    ## Consulta sql  
        conexion1.commit()
        vent_tarifas_de_alta.destroy()
        tarifas_alta_existente()        
            
    funcion_etiquetas(vent_tarifas_de_alta,1,0,"id","NOMBRE ")             # Creo las etiquetas en el tope de la pagina       
        
    cursor1.execute("select *from tarifas where activo=0")    ## Consulta sql 
                        
    crear_lista_seleccion(vent_tarifas_de_alta,cursor1,tarifa_revivir,1,2,3)  
                                                    
    conexion1.close()    ## Cierro conexion  

def tarifas_alta():        
    vent_tarifas_alta= tk.Toplevel()            ## Nueva ventana 
    vent_tarifas_alta.title("TARIFAS ALTA")
    vent_tarifas_alta.state("zoomed")     
    alto=3
    ancho=15
    vent_tarifas_alta.columnconfigure(0, weight=1)           # Hago que se expandan las filas y columnas
    vent_tarifas_alta.columnconfigure(1, weight=1)                 
    bot_nuevo=tk.Button(vent_tarifas_alta,text="Nueva tarifa",command=nueva_tarifa,height=alto,width=ancho)
    bot_existente=tk.Button(vent_tarifas_alta,text="Tarifas previamente dada de baja",command=tarifas_alta_existente,height=alto,width=30)
    bot_nuevo.grid(row=0,column=0)  
    bot_existente.grid(row=0,column=1)
    

def tarifas_baja():        
    vent_tarifas_baja= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_tarifas_baja.title("TARIFAS BAJA")
    vent_tarifas_baja.state("zoomed")                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values") 
    
    def tarifa_baja(id):           
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        cursor1.execute("update tarifas set activo=0 where idTarifa=%a"%id)    ## Consulta sql  
        conexion1.commit()
        vent_tarifas_baja.destroy()
        tarifas_baja()        
            
    funcion_etiquetas(vent_tarifas_baja,1,0,"id","NOMBRE ")             # Creo las etiquetas en el tope de la pagina       
        
    cursor1.execute("select *from tarifas where activo=1")    ## Consulta sql 
                        
    crear_lista_seleccion(vent_tarifas_baja,cursor1,tarifa_baja,1,2,3)  
                                                    
    conexion1.close()    ## Cierro conexion  

def tarifas_lista_gral():
    vent_tarifas_lista_gral= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_tarifas_lista_gral.title("TARIFAS BAJA")
    vent_tarifas_lista_gral.state("zoomed")                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values") 
    
    def mostrar_tarifa(id):      
        tarifa1=Tarifa(id)
        tarifa1.mostrar()  
            
    funcion_etiquetas(vent_tarifas_lista_gral,1,0,"id","NOMBRE ","Activo")             # Creo las etiquetas en el tope de la pagina    
    cursor1.execute("select idTarifa,idTarifa, nombreTarifa, activo from tarifas")    ## Consulta sql 
    crear_lista_seleccion(vent_tarifas_lista_gral,cursor1,mostrar_tarifa,2,3,4,5)  
    conexion1.close()    ## Cierro conexion 
    

def tarifas_lista_encurso():
    vent_tarifas_lista_encurso= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_tarifas_lista_encurso.title("TARIFAS LISTA EN CURSO")
    vent_tarifas_lista_encurso.state("zoomed")  
    
    ventana_fechas=tk.LabelFrame(vent_tarifas_lista_encurso)
    ventana_fechas.grid(row=0,column=0)
    fecha_inicio= tk.StringVar(master=vent_tarifas_lista_encurso, value="--")
    fecha_fin=tk.StringVar(master=vent_tarifas_lista_encurso, value="--") 
    seleccionar_fechas(fecha_inicio,fecha_fin,ventana_fechas)  
    def buscar(inicio,fin):            
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
        
        def mostrar_tarifa(id):      
            tarifa1=Tarifa(id)
            tarifa1.mostrar()  
        ventana_fechas.destroy()
        bot_buscar.destroy()        
        funcion_etiquetas(vent_tarifas_lista_encurso,1,0,"id","NOMBRE TARIFA","Activo","Id ESCUELA", "NOMBRE ESCUELA","Id PROFESOR","NOMBRE PROFESOR")             # Creo las etiquetas en el tope de la pagina 
        inicio=fecha_inicio.get()  
        fin=fecha_fin.get()     
        query= "select tarifas.idTarifa,tarifas.idTarifa, nombreTarifa, tarifas.activo, cursadas.idEscuela, nombreEscuela, cursadas.idProfesor, nombreProfesor  from tarifas inner join cursadas on cursadas.idTarifa=tarifas.idTarifa inner join escuelas on escuelas.idEscuela=cursadas.idEscuela inner join profesores on profesores.idProfesor=cursadas.idProfesor where fechaInicio<=%aand fechaFin >=%a"% (fin,inicio) 
        cursor1.execute(query )    ## Consulta sql 
        crear_lista_seleccion(vent_tarifas_lista_encurso,cursor1,mostrar_tarifa,2,3,4,5,6,7,8,9)  
        conexion1.close()    ## Cierro conexion 
    
    bot_buscar=tk.Button(vent_tarifas_lista_encurso,text="Buscar",command=lambda :buscar(fecha_inicio,fecha_fin)) 
    bot_buscar.grid(row=4,column=1) 

def tarifas_modificacion():
    vent_tarifas_lista_gral= tk.Toplevel()            ## Nueva ventana materias lista general
    vent_tarifas_lista_gral.title("TARIFAS MODIFICACION")
    vent_tarifas_lista_gral.state("zoomed")                
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values") 
    
    def modificar_tarifa(id):
        tarifa1=Tarifa(id)
        tarifa1.modificar()  
            
    funcion_etiquetas(vent_tarifas_lista_gral,1,0,"id","NOMBRE ","Activo")             # Creo las etiquetas en el tope de la pagina    
    cursor1.execute("select idTarifa,idTarifa, nombreTarifa, activo from tarifas")    ## Consulta sql 
    crear_lista_seleccion(vent_tarifas_lista_gral,cursor1,modificar_tarifa,2,3,4,5)  
    conexion1.close()    ## Cierro conexion     

    
def tarifas():
    marco_tarifas=tk.Label(raiz)
    deseleccionar(lista_botones)
    marco_tarifas.grid(row=0,column=1,rowspan=5,sticky="ns")
    marco_tarifas.rowconfigure(0,weight=1)
    marco_tarifas.rowconfigure(1,weight=1)
    marco_tarifas.rowconfigure(2,weight=1)
    marco_tarifas.rowconfigure(3,weight=1)
    marco_tarifas.rowconfigure(4,weight=1)
    marco_tarifas.rowconfigure(5,weight=1)
    cartel_tarifas=tk.Label(raiz,text="TARIFAS",fg="dark slate blue",font=("arial",30))
    cartel_tarifas.grid(row=0,column=0)
    bot_tarifas_alta=tk.Button(marco_tarifas,text="Alta",command=tarifas_alta,height=alto,width=ancho)    
    bot_tarifas_alta.grid(row=0,column=1)
    bot_tarifas_baja=tk.Button(marco_tarifas,text="Baja",command=tarifas_baja,height=alto,width=ancho)    
    bot_tarifas_baja.grid(row=1,column=1)
    bot_tarifas_modificacion=tk.Button(marco_tarifas,text="Modificación",command=tarifas_modificacion,height=alto,width=ancho)    
    bot_tarifas_modificacion.grid(row=2,column=1)
    bot_tarifas_lista_gral=tk.Button(marco_tarifas,text="Lista general",command=tarifas_lista_gral,height=alto,width=ancho)    
    bot_tarifas_lista_gral.grid(row=3,column=1)
    bot_tarifas_lista_encurso=tk.Button(marco_tarifas,text="Lista en curso",command=tarifas_lista_encurso,height=alto,width=ancho)    
    bot_tarifas_lista_encurso.grid(row=4,column=1)
    bot_cancelar=tk.Button(raiz,text="Cancelar",command=lambda:cancelar(marco_tarifas,bot_cancelar,cartel_tarifas),height=alto,width=ancho)
    bot_cancelar.grid(row=1,column=0)    

########################################################################################################################################
####################################################        VENTANA  CALENDARIO     ####################################################
########################################################################################################################################
               

def feriados_escuela(id_escuela):
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")
    query="select * from feriados where (idEscuela = %a and activo =1)or (idTipoFeriado = 1 and activo =1) order by fecha"%(id_escuela ) 
    cursor1.execute(query )    
    lista_feriados=list(cursor1)
    for i in lista_feriados:
        query="select tipoFeriado from tipoFeriado  where idTipoFeriado = %a"%i[2]        
        cursor1.execute(query )    ## Consulta sql 
        lup=list(cursor1)
    conexion1.close()
    return  lista_feriados   # Devuelvo lista con los feriados de la escuela seleccionada
        
        
def feriados_abm():      
    vent_feriados_abm= tk.Toplevel()            ## Nueva ventana 
    vent_feriados_abm.title("FERIADOS ")
    vent_feriados_abm.state("zoomed")
    vent_feriados_abm.columnconfigure(3, weight=1)
    vent_feriados_abm.rowconfigure(5, weight=1)
    
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")
    query="select tipoFeriado from tipoFeriado"       
    cursor1.execute(query )    ## Consulta sql 
    val=list(cursor1)
    tipo_feriado=[elemento[0] for elemento in val]  
    query="select nombreEscuela from escuelas where activo=1"       
    cursor1.execute(query )    ## Consulta sql 
    val=list(cursor1)
    nombre_escuelas=[elemento[0] for elemento in val]
    nombre_escuelas.append("Feriado nacional")
    conexion1.close()
    def resetear():
        vent_feriados_abm.destroy()
        feriados_abm()
        
    cartel_nombre_escuelas=tk.Label(vent_feriados_abm,text="Nombre escuela")
    cartel_nombre_escuelas.grid(row=0,column=0,sticky="e")  
    combo_nombre_escuelas=ttk.Combobox(vent_feriados_abm, state="readonly",values=nombre_escuelas) #combo_tipo_feriado.get()
    combo_nombre_escuelas.grid(row=0,column=1,sticky="w")
    cartel_tipo_feriado=tk.Label(vent_feriados_abm,text="Tipo feriado")
    cartel_tipo_feriado.grid(row=1,column=0,sticky="e")  
    combo_tipo_feriado=ttk.Combobox(vent_feriados_abm, state="readonly",values=tipo_feriado) #combo_tipo_feriado.get()
    combo_tipo_feriado.grid(row=1,column=1,sticky="w")
    cartel_fecha_seleccionada=tk.Label(vent_feriados_abm,text="Fecha seleccionada ")
    cartel_fecha_seleccionada.grid(row=3,column=0,pady=5,sticky="n")
    cartel_muestra_fecha_seleccionada=tk.Label(vent_feriados_abm,text="--")    
    cartel_muestra_fecha_seleccionada.grid(row=3,column=1,pady=5,sticky="n")
    boton_graba=tk.Button(vent_feriados_abm,text="",command=resetear)
    boton_graba.grid(row=4,column=0,padx=30,sticky="nw",columnspan=4)
    boton_cancelar=tk.Button(vent_feriados_abm,text="Cancelar",command=resetear)
    boton_cancelar.grid(row=4,column=0,padx=265,sticky="nw",columnspan=4)
    boton_baja=tk.Button(vent_feriados_abm,text="Eliminar",command=resetear)
    marco_observaciones=tk.LabelFrame(vent_feriados_abm,text="Observaciones")           ###  Marco observaciones  
    marco_observaciones.config(width=60, height=2)
    marco_observaciones.grid(row=2,column=0,columnspan=2)
    observaciones = tk.Text(marco_observaciones, wrap=tk.WORD,width=20, height=2,font=("Times New Roman", 15))
    observaciones.grid(row=0,column=0,rowspan=1,columnspan=2)
    marco_feriados=tk.LabelFrame(vent_feriados_abm,text= ("Feriados escuela " +str(combo_nombre_escuelas.get())))
    marco_feriados.config(width=368, height=400)
    marco_feriados.grid(row=5,column=0,columnspan=2,sticky="nwe",padx=5,pady=5)
    marco_feriados.grid_propagate(False)
        
    cal = Calendar(vent_feriados_abm, font="Arial 14", selectmode='day', locale='en_US', disabledforeground='red', cursor="hand1",tooltipdelay =1,selectbackground="olive drab")#, year=fecha.year, month=fecha.month, day=fecha.day)            
    cal.grid(row=0,column=3,rowspan=6,sticky="ewns")
    
    def cambiar_fecha():  
        fecha_feriado=cal.selection_get().strftime('%Y-%m-%d')
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        query=("select idFeriado, comentarios , idTipoFeriado from feriados inner join escuelas on escuelas.idEscuela=feriados.idEscuela where escuelas.nombreEscuela=%a and fecha=%a and feriados.activo=1"%  (combo_nombre_escuelas.get(),fecha_feriado))#))     
        cursor1.execute(query )    ## Consulta sql 
        consulta_feriado=cursor1.fetchall()
        query=("select idFeriado, comentarios , idTipoFeriado from feriados  where idTipoFeriado =1 and fecha=%a"%fecha_feriado ) 
        cursor1.execute(query )    ## Consulta sql 
        consulta_feriado_nacional=cursor1.fetchall()
        if not consulta_feriado:
            consulta_feriado=consulta_feriado_nacional   
        conexion1.close()
                    
        def modificar_feriado(id_feriado): 
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")
            query=("select idTipoFeriado from tipoferiado where tipoFeriado =%a"%  combo_tipo_feriado.get() )     
            cursor1.execute(query )    ## Consulta sql 
            cursor12=cursor1.fetchall()
            id_tipo_feriado_actual=cursor12[0][0]
            obs=observaciones.get("1.0", "end - 1 chars")
            query=("update feriados set comentarios =%a , idTipoFeriado =%a where idFeriado=%a"%(str(obs),id_tipo_feriado_actual,id_feriado))  
            cursor1.execute(query)   
            conexion1.commit()
            conexion1.close()
            cambiar_escuela()
                         
        def agregar_feriado():
            if combo_nombre_escuelas.get():
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")
                query=("select idEscuela from escuelas where nombreEscuela=%a"% combo_nombre_escuelas.get())
                cursor1.execute(query )     
                val=list(cursor1)
                if combo_nombre_escuelas.get()=="Feriado nacional":
                    fechasel=cal.selection_get().strftime('%Y-%m-%d')
                    obser=observaciones.get("1.0", "end - 1 chars")
                    query="insert into feriados(idEscuela,idTipoFeriado,fecha,comentarios) values(0,1,%a,%a) "%(fechasel,obser)
                    cursor1.execute(query) 
                    conexion1.commit()          
                    conexion1.close()
                else:
                    idescuela=val[0][0]
                    query=("select idTipoFeriado from tipoferiado where tipoFeriado =%a" %  combo_tipo_feriado.get() ) 
                    cursor1.execute(query )    ## Consulta sql 
                    cursor15=cursor1.fetchall()
                    if cursor15:
                        idtiopoferiado=cursor15[0][0]
                        fechasel=cal.selection_get().strftime('%Y-%m-%d')
                        obser=observaciones.get("1.0", "end - 1 chars")
                        query="insert into feriados(idEscuela,idTipoFeriado,fecha,comentarios) values(%a,%a,%a,%a) "%(idescuela, idtiopoferiado ,fechasel,obser)
                        cursor1.execute(query) 
                        conexion1.commit()          
                        conexion1.close()
                        cambiar_escuela()
                    else:
                        conexion1.close()
                        return
            else:
                return
            
        def eliminar_feriado(id_feriado):
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")
                cursor1.execute("update feriados set activo = 0 where idFeriado=%a"%(id_feriado))
                conexion1.commit()          
                conexion1.close()
                cambiar_escuela()
                
        if consulta_feriado:
            id_fer=consulta_feriado[0][0]
            obs_fer=consulta_feriado[0][1]
            id_tipo_feriado=consulta_feriado[0][2]
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")
            query=("select tipoFeriado from tipoferiado where idTipoFeriado =%a"% id_tipo_feriado  )     
            cursor1.execute(query )    ## Consulta sql 
            cursor12=cursor1.fetchall()
            conexion1.close()
            tipo_feriado_actual=cursor12[0][0]
            combo_tipo_feriado.set(tipo_feriado_actual)
            observaciones.delete(1.0, "end-1c")
            observaciones.insert("end-1c",  obs_fer)
            boton_graba.config(text="Grabar cambios", command=lambda:modificar_feriado(id_fer))
            boton_baja.config(command=lambda:eliminar_feriado(id_fer))
            boton_baja.grid(row=4,column=0,padx=167,sticky="nw",columnspan=4)
        else:
            observaciones.delete(1.0, "end-1c")
            combo_tipo_feriado.set("")
            boton_graba.config(text="Grabar nuevo", command=agregar_feriado)            
            boton_baja.grid_remove()
        
        cartel_muestra_fecha_seleccionada.config(text=cal.selection_get())
    def cambio_fecha(Event):
        cambiar_fecha()        
    cal.bind("<<CalendarSelected>>",cambio_fecha)
    
    def cambiar_escuela():
        cal.calevent_remove("all")
        nonlocal marco_feriados
        if marco_feriados:
            marco_feriados.destroy()
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        if combo_nombre_escuelas.get()=="Feriado nacional":
            marco_feriados=tk.LabelFrame(vent_feriados_abm,text= ("Feriados Nacionales "))
            marco_feriados.config(width=400, height=400)
            marco_feriados.grid(row=5,column=0,columnspan=2,sticky="nwe",padx=15,pady=5)
            id_escuela_seleccionada=0
        else:
            marco_feriados=tk.LabelFrame(vent_feriados_abm,text= ("Feriados escuela " +str(combo_nombre_escuelas.get())))
            marco_feriados.config(width=400, height=400)
            marco_feriados.grid(row=5,column=0,columnspan=2,sticky="nwe",padx=15,pady=5)
            query=("select idEscuela from escuelas where nombreEscuela=%a"% combo_nombre_escuelas.get())
            cursor1.execute(query )     
            val=list(cursor1)
            id_escuela_seleccionada= val[0][0]
        feriados=feriados_escuela(id_escuela_seleccionada) ##### Con esta lista hacer los calevents
        j=1
        titulo=tk.Label(marco_feriados,text="  Fecha        Tipo de feriado")
        titulo2=tk.Label(marco_feriados,text="Observaciones")
        titulo.grid(row=0,column=0,sticky="w",padx=13)
        titulo2.grid(row=0,column=1,sticky="w",padx=13)
        
        cal.tag_config("Feriado nacional", background="red")
        for i in feriados:
            query=("select tipoFeriado from tipoFeriado where idTipoFeriado=%a"% i[2])
            cursor1.execute(query )    ## Consulta sql 
            val=list(cursor1)
            tipo_feriado=val[0]
            if tipo_feriado[0]=="Feriado nacional":
                color_letras="red"
            else:
                color_letras="blue"
            cal.calevent_create(i[3], i[4], tipo_feriado)
            cal.tag_config("feriado nacional", background="red")
            valor_fecha=tk.Label(marco_feriados,text=(i[3].strftime('%Y-%m-%d')),anchor="w",justify="left",fg=color_letras)
            valor_fecha.grid(row=5+j,column=0,columnspan=2,sticky="nw",padx=5,pady=5)
            valor_tipo_feriado=tk.Label(marco_feriados,text= tipo_feriado[0],anchor="w",justify="left",fg=color_letras)
            valor_tipo_feriado.grid(row=5+j,column=0,columnspan=2,sticky="nw",padx=75,pady=5)
            if len(i[4])>0:   #Saco los espacios vacios al final del text
                while i[4][-1] == " " :
                        i[4]=i[4][:-1]
            coment=list(i[4])
            while len(coment)>18:
                    renglon=coment[:18]
                    coment=coment[18:]
                    valor_comentario=tk.Label(marco_feriados,text= renglon,anchor="w",justify="right",fg=color_letras)
                    valor_comentario.grid_propagate(False)
                    valor_comentario.grid(row=5+j,column=1,columnspan=3,sticky="nw",padx=1,pady=5)
                    j+=1
            valor_comentario=tk.Label(marco_feriados,text= coment,anchor="w",justify="left",fg=color_letras)
            valor_comentario.grid(row=5+j,column=1,columnspan=3,sticky="nw",padx=1,pady=5)
            titulo2.config(width=20)
            valor_comentario.grid_propagate(False)
            j+=1
        conexion1.close()
        cambiar_fecha()
    def cambio_escuela(Event):
        cambiar_escuela()
        
    combo_nombre_escuelas.bind("<<ComboboxSelected>>", cambio_escuela) 
    
    def cambio_tipo_feriado(Event):
        if combo_tipo_feriado.get()=="Feriado nacional":
            combo_nombre_escuelas.set("Feriado nacional")
    combo_tipo_feriado.bind("<<ComboboxSelected>>", cambio_tipo_feriado)    
    
    
    
########################################################################################################################################
####################################################       VENTANA  FACTURACION    #####################################################
########################################################################################################################################
                          



def liquidacion(entidad):  
    if entidad=="profesor":
        consulta_entidad= "select idProfesor,nombreProfesor,apellidoProfesor from profesores where activo= 1"
        nombre_entidad_mensaje="PROFESOR"
    if entidad=="escuela":
        consulta_entidad="select idEscuela,nombreEscuela from escuelas where activo=1"
        nombre_entidad_mensaje="ESCUELA"    
                
    vent_liquidacion= tk.Toplevel()            ## Nueva ventana 
    vent_liquidacion.title("")
    vent_liquidacion.state("zoomed")    
    
    fecha_inicio= tk.StringVar(master=vent_liquidacion, value="--")
    fecha_fin=tk.StringVar(master=vent_liquidacion, value="--") 
    seleccionar_fechas(fecha_inicio,fecha_fin,vent_liquidacion)   
    conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
    cursor1= conexion1.cursor()
    cursor1.execute("use test_values")
    #Definido mas arriba consulta_entidad= "select idProfesor,nombreProfesor,apellidoProfesor from profesores where activo= 1"        
    cursor1.execute(consulta_entidad )    ## Consulta sql
    entidades=list(cursor1)
    entidades_agregar=[str(i[0])+" "+i[1]+" "+i[2] for i in entidades]if entidad=="profesor" else [str(i[0])+" "+i[1]for i in entidades] 
    conexion1.close()  
    
    espacio=tk.Label(vent_liquidacion,text="                              ")
    espacio.grid(row=0, column=7,sticky="nw",padx=10,pady=15)
    cartel_entidad=tk.Label(vent_liquidacion,text=nombre_entidad_mensaje)    
    cartel_entidad.grid(row=0, column=8,sticky="nw",padx=15,pady=15)
    combo_entidad=ttk.Combobox(vent_liquidacion, state="readonly",values=entidades_agregar,width=50) 
    combo_entidad.grid(row=0, column=9,sticky="nw",padx=10,pady=15)
    
    def calcular_liquidacion():
        seleccion_entidad=combo_entidad.get()
        id_entidad=seleccion_entidad[:seleccion_entidad.find(" ",0)]
        nombre_entidad=seleccion_entidad[seleccion_entidad.find(" ",0):]
        if entidad=="profesor":
            liquidacion1=Facturacion_profesor(id_entidad,nombre_entidad,fecha_inicio,fecha_fin,vent_liquidacion,"idProfesor")
        elif entidad=="escuela":
            liquidacion1=Facturacion_escuela(id_entidad,nombre_entidad,fecha_inicio,fecha_fin,vent_liquidacion,"idEscuela")
        liquidacion1.calcular()
    
    bot_calcular_liq=tk.Button(vent_liquidacion,text="CALCULAR",command=lambda:calcular_liquidacion())#(entidad,fecha_inicio,fecha_fin))
    bot_calcular_liq.grid(row=0, column=10,sticky="nw",padx=10,pady=15)        
        
def recuperar_liquidacion(entidad,idEntidad_nombreSQL):
    vent_recupero_liquidacion= tk.Toplevel()            ## Nueva ventana 
    vent_recupero_liquidacion.title("REVISION LIQUIDACIONES GRABADAS ")
    vent_recupero_liquidacion.state("zoomed") 
    
    fecha_inicio= tk.StringVar(master=vent_recupero_liquidacion, value="--")
    fecha_fin=tk.StringVar(master=vent_recupero_liquidacion, value="--") 
    seleccionar_fechas(fecha_inicio,fecha_fin,vent_recupero_liquidacion) 
    
     
    def buscar_liquidaciones(fecha_inicio,fecha_fin,entidad,id_entidad):
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values")
        query=("select nombreProfesor,apellidoProfesor from profesores where idProfesor=%a",id_entidad) if entidad=="profesor" else ("select nombreEscuela from escuelas where idEscuela=%a",id_entidad)
        print("WW ",query)
        marco_busqueda=tk.LabelFrame(vent_recupero_liquidacion,width=170,height=600)     
        marco_busqueda.grid_propagate(False)
        
        marco_busqueda.grid(row=2,column=0,sticky="nsew",columnspan=11)
        marco_busqueda.config(text="Liquidaciones periodo seleccionado ")
        
        def onFrameConfigure(canvas):
            '''Reset the scroll region to encompass the inner frame'''
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas = tk.Canvas(marco_busqueda, borderwidth=0, background="#ffffff")
        canvas.config(width=1100,height=500)
        marco_mostrar = tk.Frame(canvas, background="#ffffff")#,height=100,width=200)
        vsb = tk.Scrollbar(marco_busqueda, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=vsb.set)

        vsb.grid(row=2,column=0,sticky="ens")#(side="right", fill="y")
        canvas.grid_propagate(False)
        canvas.grid(row=2,column=0,sticky="nsew")#(side="left", fill="both", expand=True)
        canvas.create_window((4,4), window=marco_mostrar, anchor="nw")

        marco_mostrar.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))
        query=("select idLiquidacion, FechaInicio, FechaFin, Total, Activo from liquidaciones where  fechaFin>%a and fechaInicio<%a and entidad=%a and idEntidad = %a "%(fecha_inicio.get(),fecha_fin.get(),entidad,id_entidad) )    ## Consulta sql
        cursor1.execute(query)
        liq=list(cursor1)

        cartel_id_cursada=tk.Label(marco_busqueda,text="id liquidacion")
        cartel_id_cursada.grid(row=0,column=0,sticky="w",padx=40)
        cartel_fecha_inicio=tk.Label(marco_busqueda,text="Fecha inicio")
        cartel_fecha_inicio.grid(row=0,column=0,padx=190,sticky="w")
        cartel_fecha_fin=tk.Label(marco_busqueda,text="Fecha fin")
        cartel_fecha_fin.grid(row=0,column=0,padx=340,sticky="w")
        cartel_valor=tk.Label(marco_busqueda,text="Monto liquidacion")
        cartel_valor.grid(row=0,column=0,padx=470,sticky="w")
        cartel_activo=tk.Label(marco_busqueda,text="Activo")
        cartel_activo.grid(row=0,column=0,padx=640,sticky="w")
        def mostrar_liquidacion(id_liquidacion):
            vent_mostrar_liquidacion= tk.Toplevel()            ## Nueva ventana 
            vent_mostrar_liquidacion.title("REVISION LIQUIDACION "+ str(id_liquidacion))
            vent_mostrar_liquidacion.state("zoomed") 
        
            conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
            cursor1= conexion1.cursor()
            cursor1.execute("use test_values")
            cursor1.execute("select * from liquidaciones where idLiquidacion = %a "%id_liquidacion )    ## Consulta sql 
            val=list(cursor1)
            fecha_inicio_liq=val[0][1]
            fecha_fin_liq=val[0][2]
            entidad=val[0][3]
            id_entidad=val[0][4]
            total_liquidacion=val[0][5]
            activo=val[0][6]
            nombre_entidad=val[0][7]
                
            cursor1.execute("select * from liquidacionesLineas where idLiquidacion = %a "%id_liquidacion )    ## Consulta sql 
            lista_liquidacionesLineas=list(cursor1)
            conexion1.close()
            marco_revision2=tk.LabelFrame(vent_mostrar_liquidacion,width=1500,height=600)     
            marco_revision2.grid_propagate(False)
            
            marco_revision2.grid(row=3,column=0,sticky="nsew",columnspan=11)
            marco_revision2.config(text="Liquidacion %a"%id_liquidacion)
            
            def onFrameConfigure(canvas2):
                '''Reset the scroll region to encompass the inner frame'''
                canvas2.configure(scrollregion=canvas2.bbox("all"))

            canvas2 = tk.Canvas(marco_revision2, borderwidth=0, background="#ffffff")
            canvas2.config(width=1100,height=500)
            marco_mostrar2 = tk.Frame(canvas2, background="#ffffff")#,height=100,width=200)
            vsb = tk.Scrollbar(marco_revision2, orient="vertical", command=canvas2.yview)
            canvas2.configure(yscrollcommand=vsb.set)
            vsb.grid(row=2,column=0,sticky="ens")#(side="right", fill="y")
            canvas2.grid_propagate(False)
            canvas2.grid(row=2,column=0,sticky="nsew")#(side="left", fill="both", expand=True)
            canvas2.create_window((4,4), window=marco_mostrar2, anchor="nw")

            marco_mostrar2.bind("<Configure>", lambda event, canvas2=canvas2: onFrameConfigure(canvas2))
            info_liquidacion=tk.Label(marco_revision2,text=("Fecha inicio liquidacion: "+fecha_inicio_liq.strftime('%Y-%m-%d')+"                 Fecha fin liquidacion: "+fecha_fin_liq.strftime('%Y-%m-%d')+"                 "+entidad+"  "+str(id_entidad)+" "+nombre_entidad+"                Activo: "+("Si" if activo==1 else "No")))
            info_liquidacion.grid(row=0,column=0)    
            titulo_materia= tk.Label(marco_revision2,text="MATERIA") 
            titulo_materia.grid(row=1,column=0,sticky="w",padx=105)
            titulo_fecha= tk.Label(marco_revision2,text="FECHA") 
            titulo_fecha.grid(row=1,column=0,sticky="w",padx=300) 
            titulo_hora_inicio= tk.Label(marco_revision2,text="HORA") 
            titulo_hora_inicio.grid(row=1,column=0,sticky="w",padx=413,columnspan=8)  
            titulo_entidad_asociada= tk.Label(marco_revision2,text="ESCUELA"if entidad=="profesor" else "PROFESOR") # nombre entidad mostrar
            titulo_entidad_asociada.grid(row=1,column=0,sticky="w",padx=580,columnspan=8)
            titulo_cantidad_alumnos= tk.Label(marco_revision2,text="ALUMNOS") 
            titulo_cantidad_alumnos.grid(row=1,column=0,sticky="w",padx=760,columnspan=8)
            titulo_funcion= tk.Label(marco_revision2,text="FUNCION") # FUNCION
            titulo_funcion.grid(row=1,column=0,sticky="w",padx=880,columnspan=8)
            titulo_monto= tk.Label(marco_revision2,text="MONTO") 
            titulo_monto.grid(row=1,column=0,sticky="w",padx=1000,columnspan=8)
            titulo_observaciones= tk.Label(marco_revision2,text="OBSERVACIONES")
            titulo_observaciones.grid(row=1,column=0,sticky="w",padx=1128,columnspan=8)
            total_liqui=tk.Label(marco_revision2,text="TOTAL VALOR LIQUIDACION: %a"%total_liquidacion)
            total_liqui.grid(row=3,column=0,sticky="nw",padx=650,pady=20,columnspan=8)
            fila=0
            ancho=[36,16,14,36,13,20,11,30]
            for linea in lista_liquidacionesLineas:
                for columna in range(0,8):
                    valor=tk.Label(marco_mostrar2,text=str(linea[columna+2]),width=ancho[columna])
                    valor.grid(row=fila,column=columna)
                fila+=1
            def habilitar(activar):
                conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ### Abro conexion
                cursor1= conexion1.cursor()
                cursor1.execute("use test_values")
                cursor1.execute("update  liquidaciones set activo =%a where idLiquidacion=%a"%(activar,id_liquidacion ))    ## Consulta sql
                conexion1.commit()
                conexion1.close()
                vent_recupero_liquidacion.destroy()
                mostrar_liquidacion(id_liquidacion)
                
            if activo==1:#
                activar=0
            else:
                activar=1
            boton_activar=tk.Button(marco_revision2,text="Deshabilitar"if activo==1 else "Habilitar",command=lambda:habilitar(activar))
            boton_activar.grid(row=3,column=0,sticky="nw",padx=350,pady=20,columnspan=8) 
                
                
        r=0
        for liquidacion in liq:
            for g in range(0,5):
                mostrar_valor=tk.Label(marco_mostrar,text=liquidacion[g],width=20)
                mostrar_valor.grid(row=r,column=g)
            boton_seleccion=tk.Button(marco_mostrar,text="Seleccionar",command=lambda c=liquidacion[0]:mostrar_liquidacion(c))
            boton_seleccion.grid(row=r,column=g+1)
            r+=1
    def seleccionar_nombre_entidad():
        def seleccionar_id_entidad(id_ent):
            nonlocal id
            id=id_ent  
            vent_entidad_seleccion.destroy()  
             
        vent_entidad_seleccion= tk.LabelFrame(vent_recupero_liquidacion,text="Seleccion "+entidad)           
        vent_entidad_seleccion.grid(row=3,column=0)
        
        conexion1 = mysql.connector.connect(host="localhost", user="root", passwd="")    ## Abro conexion
        cursor1= conexion1.cursor()
        cursor1.execute("use test_values") 
           
        if entidad=="profesor":
            funcion_etiquetas(vent_entidad_seleccion,1,0,"NOMBRE","APELLIDO","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")             # Creo las etiquetas en el tope de la pagina
            cursor1.execute("select idProfesor, nombreProfesor, apellidoProfesor, estado, localidad, codigoPostal, calle,numero,  ifnull(piso,'--'), departamento, ifnull( telefono,'--'), mail, activo from profesores inner join estados on profesores.idEstado = estados.idEstado inner join localidades on profesores.idLocalidad = localidades.idLocalidad" )    ## Consulta sql datos demograficos
            crear_lista_seleccion(vent_entidad_seleccion,cursor1,seleccionar_id_entidad,1,3,4,5,6,7,8,9,10,11,12,13) 
        else:
            funcion_etiquetas(vent_entidad_seleccion,1,0,"NOMBRE","ESTADO","LOCALIDAD","C P","CALLE","NUMERO","PISO","DEPTO","TELEFONO","EMAIL","ACTIVO")  
            cursor1.execute("select idEscuela, nombreEscuela, estado, localidad, codigoPostal, calle,numero, piso, departamento, telefono, mail, activo from escuelas inner join estados on escuelas.idEstado = estados.idEstado inner join localidades on escuelas.idLocalidad = localidades.idLocalidad" )    ## Consulta sql datos demograficos
            crear_lista_seleccion(vent_entidad_seleccion,cursor1,seleccionar_id_entidad,1,2,3,4,5,6,7,8,9,10,11,12)   ## Muestro lista prof
                                                        # La seleccion de los botones lo levanto con la funcion mostrar_prof(idProfesor)
        conexion1.close()    ## Cierro conexion
        
    
    id="*"
    texto= "Seleccionar " + entidad   
    bot_seleccionar_nombre_entidad=tk.Button(vent_recupero_liquidacion,text=texto,command=seleccionar_nombre_entidad)
    bot_seleccionar_nombre_entidad.grid(row=1, column=10,sticky="nw",padx=550,pady=15) 
    bot_buscar_liq=tk.Button(vent_recupero_liquidacion,text="BUSCAR",command=lambda :buscar_liquidaciones(fecha_inicio,fecha_fin,entidad,id))
    bot_buscar_liq.grid(row=0, column=10,sticky="nw",padx=550,pady=15)        

def liquidaciones():    
    marco_liquidaciones=tk.Label(raiz)
    deseleccionar(lista_botones)
    marco_liquidaciones.grid(row=0,column=1,rowspan=5,sticky="ns")
    marco_liquidaciones.rowconfigure(0,weight=1)
    marco_liquidaciones.rowconfigure(1,weight=1)
    marco_liquidaciones.rowconfigure(2,weight=1)
    marco_liquidaciones.rowconfigure(3,weight=1)
    marco_liquidaciones.rowconfigure(4,weight=1)
    marco_liquidaciones.rowconfigure(5,weight=1)
    cartel_liquidaciones=tk.Label(raiz,text="LIQUIDACIONES",fg="dark slate blue",font=("arial",30))
    cartel_liquidaciones.grid(row=0,column=0)
    
    bot_nueva_liquidacion_profesor=tk.Button(marco_liquidaciones,text="Nueva liquidacion por profesor",command=lambda:liquidacion("profesor"),height=alto,width=25)    
    bot_nueva_liquidacion_profesor.grid(row=0,column=1)
    bot_nueva_liquidacion_escuela=tk.Button(marco_liquidaciones,text="Nueva liquidacion por escuela",command=lambda:liquidacion("escuela"),height=alto,width=25)       
    bot_nueva_liquidacion_escuela.grid(row=1,column=1)
    bot_consulta_liquidaciones_profesor=tk.Button(marco_liquidaciones,text="Consulta liquidaciones por profesor",command=lambda:recuperar_liquidacion("profesor","idProfesor"),height=alto,width=30)    
    bot_consulta_liquidaciones_profesor.grid(row=2,column=1)
    bot_consulta_liquidaciones_escuela=tk.Button(marco_liquidaciones,text="Consulta liquidaciones por escuela",command=lambda:recuperar_liquidacion("escuela","idEscuela"),height=alto,width=30)       
    bot_consulta_liquidaciones_escuela.grid(row=3,column=1)
    
    bot_cancelar=tk.Button(raiz,text="Cancelar",command=lambda:cancelar(marco_liquidaciones,bot_cancelar,cartel_liquidaciones),height=alto,width=ancho)
    bot_cancelar.grid(row=1,column=0)

####################################################################################################################
#########################################   CONFIGURACION VENTANA PRINCIPAL             ###########################3
####################################################################################################################
def inicio():
    raiz.state("zoomed")   
    raiz.columnconfigure(0, weight=1)           # Hago que se expandan las filas y columnas
    raiz.columnconfigure(1, weight=1)
    raiz.columnconfigure(2, weight=1)   

    raiz.rowconfigure(0,weight=1) 
    raiz.rowconfigure(1,weight=1)  
    raiz.rowconfigure(2,weight=1)
    raiz.rowconfigure(3,weight=1) 
    raiz.rowconfigure(4,weight=1)                          
    
    bot_localidades.grid(row=0,column=0)
    bot_materiales.grid(row=0,column=1) 
    bot_tarifas.grid(row=0,column=2)  
    bot_escuelas.grid(row=1,column=0)  
    bot_profesores.grid(row=2,column=0)  
    bot_materias.grid(row=1,column=1)   
    bot_feriados.grid(row=2,column=1)  
    bot_cursadas.grid(row=3,column=0)    
    bot_liquidaciones.grid(row=4,column=0)  
    # bot_estadisticas.grid(row=3,column=3)  

alto=3
ancho=15                 
bot_escuelas=tk.Button(raiz,text="Escuelas",command=escuelas,height=alto,width=ancho)
bot_profesores=tk.Button(raiz,text="Profesores",command=profesores,height=alto,width=ancho)
bot_materias=tk.Button(raiz,text="Materias",command=materias,height=alto,width=ancho)
bot_materiales=tk.Button(raiz,text="Materiales",command=materiales,height=alto,width=ancho)
bot_tarifas=tk.Button(raiz,text="Tarifas",command=tarifas,height=alto,width=ancho)
bot_cursadas=tk.Button(raiz,text="Cursadas",command=cursadas,height=alto,width=ancho)
bot_localidades=tk.Button(raiz,text="Localidades",command=estados_lista_gral,height=alto,width=ancho)
# bot_estadisticas=tk.Button(raiz,text="Estadistcas",command=estadisticas,height=alto,width=ancho)
bot_liquidaciones=tk.Button(raiz,text="Liquidaciones",command=liquidaciones,height=alto,width=ancho)
bot_feriados=tk.Button(raiz,text="Feriados",command=feriados_abm,height=alto,width=ancho)




lista_botones=[bot_escuelas,bot_profesores,bot_materias,bot_materiales,bot_tarifas,bot_cursadas,bot_liquidaciones,bot_feriados,bot_localidades]
               
inicio()   
    ##########################################################################################################################   
     
# # # #mostrar_prof(5)                              #  PROFESORES
# # # #profesores_lista_encurso()
# # # #profesores_lista_gral()
# # # #profesores_modificacion()  
# # # #profesores_baja()
# # # #profesores_alta()

# # # materias_lista_gral()                      # MATERIAS
# # # materias_lista_encurso()
# # # #materias_alta()
# # # #materias_baja()
# # # #materias_modificacion()
# # # #nueva_materia()
# # # #materia_alta_existente()

# # # #nuevo_material()                               # MATERIALES
# # # #materiales_alta()
# # # #materiales_baja()
# # # #materiales_modificacion()
# # # #materiales_alta_existente()
# # # #materiales_alta()
# # # #materiales_lista_gral() 
# # # #materiales_lista_encurso()                      
# # # #materiales_baja()

# # # #materia1=Materia(1)
# # # #materia1.mostrar_mat()
# # # #materia1.baja_mat()
# # # #materia1.modificar_mat()
# # # #materia1.nueva_mat()


               
# # # #escuela1=Escuela(2)                               # ESCUELAS    
# # # #escuela1.modificar()                             
# # # #escuela1.mostrar()
# # # #mostrar_esc(3)
# # # #escuelas_lista_gral()
# # # #escuelas_lista_encurso()
# # # #escuelas_modificacion()
# # # #escuelas_baja()
# # # #escuelas_alta()


# # # cursada1 = Cursadas(1)                           #cursadas    
# # # cursada1.mostrar()
# # #cursada1.modificar()
# # #cursadas_alta()
# # #cursada_nueva()
# # #cursadas_baja()
# # #cursadas_modificacion()
# # #cursadas_lista_gral()
# # #cursadas_lista_encurso()

# # # tarifa1= Tarifa(1)                                                #Tarifas
# # # tarifa1.modificar()
# # # #nueva_tarifa()
# # # #tarifas_alta()
# # # #tarifas_baja()
# # # #tarifas_lista_gral()
# # # #tarifas_lista_encurso()


# # # #liquidacion("profesor")                                                    #LIQUIDACIONES
# # # #liquidacion("escuela")
# # # #recuperar_liquidacion()



# # # #horas_lista_gral()                                #HORAS   


# # # #estados_lista_gral()                          # LOCALIDADES/ESTADOS


# # # #feriados_escuela(8)                                 #feriados
# # # #feriados_abm()

#########################################################################################################################################



raiz.mainloop()

