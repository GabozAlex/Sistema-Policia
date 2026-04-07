from tkinter import *
from logic import Funcionario, Familiar

class UI:
    def __init__(self, root):
        #ventana principal
        self.root = root
        self.root.title("Bienestar y Proteccion Social")
        self.min_x=800
        self.min_y=600
        self.max_x=1920
        self.max_y=1080
        self.root.minsize(self.min_x,self.min_y)
        self.root.maxsize(self.max_x,self.max_y)
        self.root.geometry("800x600")
        self.root.resizable(True,True)
        #panel principal
        self.panel_principal=Frame(root,width=800,height=600, bg="gray")
        self.panel_principal.pack(fill=BOTH, expand=True)
        self.inicio_sesion()

    def limpiar_panel_principal(self):
        for widget in self.panel_principal.winfo_children():
            widget.destroy()

    def inicio_sesion(self):
        self.limpiar_panel_principal()
        self.panel_inicio_sesion=Frame(self.panel_principal, bg="yellow",)
        self.panel_inicio_sesion.pack(fill="none", expand=True)

        self.label_usuario=Label(self.panel_inicio_sesion, text="usuario")
        self.label_usuario.pack()
        self.input_usuario=Entry(self.panel_inicio_sesion)
        self.input_usuario.pack()

        self.label_contrasena=Label(self.panel_inicio_sesion, text="contrasena")
        self.label_contrasena.pack()
        self.input_contrasena=Entry(self.panel_inicio_sesion, show="*")
        self.input_contrasena.pack()

        self.button_iniciar_sesion=Button(self.panel_inicio_sesion, text="Iniciar Sesion", command=self.mostrar_pagina_principal)
        self.button_iniciar_sesion.pack()

    def mostrar_panel_acciones(self):
        self.panel_acciones=Frame(self.pagina_principal, height=600, bg="white")
        self.panel_acciones.pack(side=LEFT, fill=Y, expand=False)

        self.titulo_acciones=Label(self.panel_acciones, text="usuario").pack()
        self.boton_regresar_menu_principal=Button(self.panel_acciones, text="Regresar", command=self.mostrar_pagina_principal)
        self.boton_regresar_menu_principal.pack(side=BOTTOM, fill=Y, expand=False)

    def mostrar_pagina_principal(self):
        self.limpiar_panel_principal()
        self.pagina_principal=Frame(self.panel_principal, bg="blue")
        self.pagina_principal.pack(fill=BOTH, expand=True)

        self.mostrar_panel_acciones()

        self.panel_busqueda=Frame(self.pagina_principal,width=800,height=200, bg="red")
        self.panel_busqueda.pack(side=TOP, fill=X, expand=False)
        self.panel_busqueda.rowconfigure(0, weight=1)
        self.panel_busqueda.columnconfigure(1, weight=1)
        self.panel_busqueda.columnconfigure(2, weight=1)
        self.panel_busqueda.columnconfigure(3, weight=1)
        self.panel_busqueda.columnconfigure(4, weight=1)

        self.titulo=Label(self.panel_busqueda, text="Funcionario")
        self.titulo.grid(row=1, column=1,padx=50, pady=10)
        self.titulo.config(width=20)

        self.botton_crear_funcionario=Button(self.panel_busqueda, text="Nuevo Funcionario", bg="green", command=self.mostrar_registrar_usuario)
        self.botton_crear_funcionario.grid(row=1, column=2,padx=50, pady=10)
        self.botton_crear_funcionario.config()

        self.input_busqueda=Entry(self.panel_busqueda, text="Busqueda...")
        self.input_busqueda.grid(row=1, column=3, padx=50, pady=10)
        self.input_busqueda.config(width=20)

        self.botton_buscar=Button(self.panel_busqueda, text="Buscar")
        self.botton_buscar.grid(row=1, column=4, padx=50, pady=10)
        self.botton_buscar.config(width=20)

        self.panel_tabla=Frame(self.pagina_principal, bg="gray")
        self.panel_tabla.pack(side=TOP, fill=BOTH ,expand=True)
        self.panel_tabla.rowconfigure(3, weight=1)
        self.panel_tabla.columnconfigure(1, weight=1)
        self.panel_tabla.columnconfigure(2, weight=1)
        self.panel_tabla.columnconfigure(3, weight=1)
        self.panel_tabla.columnconfigure(4, weight=1)

        self.ID_label=Label(self.panel_tabla, text="ID")
        self.ID_label.grid(padx=50, pady=5, row=1, column=1)

        self.Nombre_label=Label(self.panel_tabla, text="Nombre")
        self.Nombre_label.grid(padx=50, pady=5, row=1, column=2)

        self.Apellido_label=Label(self.panel_tabla, text="Apellido")
        self.Apellido_label.grid(padx=50, pady=5, row=1, column=3)

        self.Acciones_label=Label(self.panel_tabla, text="Acciones")
        self.Acciones_label.grid(padx=50, pady=5, row=1, column=4)

    def preguntas_datos_personales(self):#-------------------------------------------------------------------------------
        self.panel_categorias_preguntas=Frame(self.panel_cuestionarios, bg="gray")
        self.panel_categorias_preguntas.pack(fill="x",expand=False)

        self.titulo_datos_personales=Label(self.panel_categorias_preguntas, text="Datos Personales", width=20)
        self.titulo_datos_personales.grid(row=0, column=0, columnspan=2, pady=10)

        self.label_cedula=Label(self.panel_categorias_preguntas, text="Cedula:", width=20)
        self.label_cedula.grid(row=1,column=0, sticky=E, pady=10)
        self.input_cedula=Entry(self.panel_categorias_preguntas)
        self.input_cedula.grid(row=1,column=1, sticky=W, pady=10)

        self.label_nombre=Label(self.panel_categorias_preguntas, text="Nombre:", width=20)
        self.label_nombre.grid(row=1,column=2, sticky=E, pady=10)
        self.input_nombre=Entry(self.panel_categorias_preguntas)
        self.input_nombre.grid(row=1,column=3, sticky=W, pady=10)

        self.label_apellido=Label(self.panel_categorias_preguntas, text="Apellido:", width=20)
        self.label_apellido.grid(row=1,column=4 , sticky=E, pady=10)
        self.input_apellido=Entry(self.panel_categorias_preguntas)
        self.input_apellido.grid(row=1,column=5, sticky=W, pady=10)

        self.label_fecha_nacimiento=Label(self.panel_categorias_preguntas, text="Fecha de Nacimiento:", width=20)
        self.label_fecha_nacimiento.grid(row=2,column=0, sticky=E, pady=10)
        self.input_fecha_nacimiento=Entry(self.panel_categorias_preguntas)
        self.input_fecha_nacimiento.grid(row=2,column=1, sticky=W, pady=10)

        self.label_telefono_contacto=Label(self.panel_categorias_preguntas, text="Telefono:", width=20)
        self.label_telefono_contacto.grid(row=2,column=2, sticky=E, pady=10)
        self.input_telefono_contacto=Entry(self.panel_categorias_preguntas)
        self.input_telefono_contacto.grid(row=2,column=3, sticky=W, pady=10)

        self.label_peso=Label(self.panel_categorias_preguntas, text="Peso:", width=20)
        self.label_peso.grid(row=2,column=4, sticky=E, pady=10)
        self.input_peso=Entry(self.panel_categorias_preguntas)
        self.input_peso.grid(row=2,column=5, sticky=W, pady=10)

        self.label_altura=Label(self.panel_categorias_preguntas, text="Altura:", width=20)
        self.label_altura.grid(row=3,column=0, sticky=E, pady=10)
        self.input_altura=Entry(self.panel_categorias_preguntas)
        self.input_altura.grid(row=3,column=1, sticky=W, pady=10)

        self.label_estado_civil=Label(self.panel_categorias_preguntas, text="Estado Civil:", width=20)
        self.label_estado_civil.grid(row=3,column=2, sticky=E, pady=10)
        self.input_estado_civil=Entry(self.panel_categorias_preguntas)
        self.input_estado_civil.grid(row=3,column=3, sticky=W, pady=10)

        self.label_direccion_habitacion=Label(self.panel_categorias_preguntas, text="Direccion de Habitacion:", width=20)
        self.label_direccion_habitacion.grid(row=3,column=4, sticky=E, pady=10)
        self.input_direccion_habitacion=Entry(self.panel_categorias_preguntas)
        self.input_direccion_habitacion.grid(row=3,column=5, sticky=W, pady=10)

        self.label_municipio_residencia=Label(self.panel_categorias_preguntas, text="Municipio de Residencia:", width=20)
        self.label_municipio_residencia.grid(row=4,column=0, sticky=E, pady=10)
        self.input_municipio_residencia=Entry(self.panel_categorias_preguntas)
        self.input_municipio_residencia.grid(row=4,column=1, sticky=W, pady=10)

        row=0
        column=0
        for row in range(4):
            self.panel_categorias_preguntas.rowconfigure(row)
            for column in range(5):
                self.panel_categorias_preguntas.columnconfigure(column)

    def preguntas_datos_laborales(self):#--------------------------------------------------------------------------------
        self.panel_categorias_preguntas=Frame(self.panel_cuestionarios, bg="gray")
        self.panel_categorias_preguntas.pack(fill="x", expand=False)

        self.titulo_datos_personales=Label(self.panel_categorias_preguntas, text="Datos Laborales:", width=20)
        self.titulo_datos_personales.grid(row=0, column=0, columnspan=2, pady=10)

        self.label_jerarquia=Label(self.panel_categorias_preguntas, text="Jerarquia:", width=20)
        self.label_jerarquia.grid(row=1,column=0, sticky=E, pady=10)
        self.input_jerarquia=Entry(self.panel_categorias_preguntas)
        self.input_jerarquia.grid(row=1,column=1, sticky=W, pady=10)

        self.label_tiempo_servicio=Label(self.panel_categorias_preguntas, text="Tiempo de Servicio:", width=20)
        self.label_tiempo_servicio.grid(row=1,column=2, sticky=E, pady=10)
        self.input_tiempo_servicio=Entry(self.panel_categorias_preguntas)
        self.input_tiempo_servicio.grid(row=1,column=3, sticky=W, pady=10)

        self.label_lugar_servicio=Label(self.panel_categorias_preguntas, text="Lugar de Servico:", width=20)
        self.label_lugar_servicio.grid(row=1,column=4, sticky=E, pady=10)
        self.input_lugar_servicio=Entry(self.panel_categorias_preguntas)
        self.input_lugar_servicio.grid(row=1,column=5, sticky=W, pady=10)

        self.label_ingreso_mensual=Label(self.panel_categorias_preguntas, text="Ingreso Mensual:", width=20)
        self.label_ingreso_mensual.grid(row=2,column=0, sticky=E, pady=10)
        self.input_ingreso_mensual=Entry(self.panel_categorias_preguntas)
        self.input_ingreso_mensual.grid(row=2,column=1, sticky=W, pady=10)

        row=0
        column=0
        for row in range(4):
            self.panel_categorias_preguntas.rowconfigure(row)
            for column in range(5):
                self.panel_categorias_preguntas.columnconfigure(column)

    def borrar_panel_familiar(self):
        self.panel_categorias_preguntas.pack_forget()

    def crear_nuevo_panel_familiar(self):
        #self.ID_panel+=self.ID_panel
        self.preguntas_datos_familiares()

    def preguntas_datos_familiares(self):#-------------------------------------------------------------------------------
        self.panel_categorias_preguntas=Frame(self.panel_cuestionarios, bg="gray")
        self.panel_categorias_preguntas.pack(fill="x", expand=False)

        self.titulo_datos_personales=Label(self.panel_categorias_preguntas, text="Datos Familiares", width=20)
        self.titulo_datos_personales.grid(row=0, column=0, columnspan=2, pady=10)

        self.label_nombre=Label(self.panel_categorias_preguntas, text="Nombre:", width=20)
        self.label_nombre.grid(row=1,column=0, sticky=E, pady=10)
        self.input_nombre=Entry(self.panel_categorias_preguntas)
        self.input_nombre.grid(row=1,column=1, sticky=W, pady=10)

        self.label_apellido=Label(self.panel_categorias_preguntas, text="Apellido:", width=20)
        self.label_apellido.grid(row=1,column=2 , sticky=E, pady=10)
        self.input_apellido=Entry(self.panel_categorias_preguntas)
        self.input_apellido.grid(row=1,column=3, sticky=W, pady=10)

        self.label_parentesco=Label(self.panel_categorias_preguntas, text="Parentesco:", width=20)
        self.label_parentesco.grid(row=1,column=4, sticky=E, pady=10)
        self.input_parentesco=Entry(self.panel_categorias_preguntas)
        self.input_parentesco.grid(row=1,column=5, sticky=W, pady=10)

        self.label_edad=Label(self.panel_categorias_preguntas, text="Edad:", width=20)
        self.label_edad.grid(row=2,column=0, sticky=E, pady=10)
        self.input_edad=Entry(self.panel_categorias_preguntas)
        self.input_edad.grid(row=2,column=1, sticky=W, pady=10)

        self.label_estado_civil=Label(self.panel_categorias_preguntas, text="Estado civil:", width=20)
        self.label_estado_civil.grid(row=2,column=2, sticky=E, pady=10)
        self.input_estado_civil=Entry(self.panel_categorias_preguntas)
        self.input_estado_civil.grid(row=2,column=3, sticky=W, pady=10)

        self.label_nivel_educacion=Label(self.panel_categorias_preguntas, text="Nivel Educacion:", width=20)
        self.label_nivel_educacion.grid(row=2,column=4, sticky=E, pady=10)
        self.input_nivel_educacion=Entry(self.panel_categorias_preguntas)
        self.input_nivel_educacion.grid(row=2,column=5, sticky=W, pady=10)

        self.label_profesion=Label(self.panel_categorias_preguntas, text="Profesion:", width=20)
        self.label_profesion.grid(row=3,column=0, sticky=E, pady=10)
        self.input_profesion=Entry(self.panel_categorias_preguntas)
        self.input_profesion.grid(row=3,column=1, sticky=W, pady=10)

        self.label_lugar_trabajo=Label(self.panel_categorias_preguntas, text="Lugar de Trabajo:", width=20)
        self.label_lugar_trabajo.grid(row=3,column=2, sticky=E, pady=10)
        self.input_lugar_trabajo=Entry(self.panel_categorias_preguntas)
        self.input_lugar_trabajo.grid(row=3,column=3, sticky=W, pady=10)

        self.label_ingreso_mensual=Label(self.panel_categorias_preguntas, text="Ingreso mensual:", width=20)
        self.label_ingreso_mensual.grid(row=3,column=4, sticky=E, pady=10)
        self.input_ingreso_mensual=Entry(self.panel_categorias_preguntas)
        self.input_ingreso_mensual.grid(row=3,column=5, sticky=W, pady=10)

        self.label_viven_juntos=Label(self.panel_categorias_preguntas, text="Viven Juntos:", width=20)
        self.label_viven_juntos.grid(row=4,column=0, sticky=E, pady=10)
        self.input_viven_juntos=Entry(self.panel_categorias_preguntas)
        self.input_viven_juntos.grid(row=4,column=1, sticky=W, pady=10)

        self.label_observacion=Label(self.panel_categorias_preguntas, text="Observacion:", width=20)
        self.label_observacion.grid(row=4,column=2, sticky=E, pady=10)
        self.input_observacion=Entry(self.panel_categorias_preguntas)
        self.input_observacion.grid(row=4,column=3, sticky=W, pady=10)

        self.boton_borrar_familiar=Button(self.panel_categorias_preguntas, text="Borrar Familiar", bg="red",command=self.borrar_panel_familiar, width=20)
        self.boton_borrar_familiar.grid(row=4,column=5, sticky=E, pady=10)

        row=0
        column=0
        for row in range(4):
            self.panel_categorias_preguntas.rowconfigure(row)
            for column in range(5):
                self.panel_categorias_preguntas.columnconfigure(column)
        
    def preguntas_plan_vivienda(self):#-------------------------------------------------------------------------------
        self.posee_terreno=StringVar()
        self.posee_terreno.set("NO")

        self.posee_vivienda=StringVar()
        self.posee_vivienda.set("NO")

        self.necesidad_habiacion=StringVar()
        self.necesidad_habiacion.set("Vivienda")

        self.gestion_organismo=StringVar()
        self.gestion_organismo.set("NO")

        self.organismo_publico=StringVar()
        self.organismo_publico.set("OTRA")

        self.organismo_privado=StringVar()
        self.organismo_privado.set("OTRA")

        self.panel_categorias_preguntas=Frame(self.panel_cuestionarios, bg="gray")
        self.panel_categorias_preguntas.pack(fill="x", expand=False)

        self.titulo_datos_personales=Label(self.panel_categorias_preguntas, text="Datos Plan de Vivienda:", width=20)
        self.titulo_datos_personales.grid(row=0, column=0, columnspan=2, sticky=W, pady=10)

        self.label_terreno_propio=Label(self.panel_categorias_preguntas, text="Terreno Propio:", width=20)
        self.label_terreno_propio.grid(row=1,column=0, sticky=W, pady=10)

        self.radio_posee_terreno_1=Radiobutton(self.panel_categorias_preguntas, text="SI", variable=self.posee_terreno, value="SI", width=10)
        self.radio_posee_terreno_1.grid(row=1,column=1, sticky=W, pady=10)
        self.radio_posee_terreno_2=Radiobutton(self.panel_categorias_preguntas, text="NO", variable=self.posee_terreno, value="NO", width=10)
        self.radio_posee_terreno_2.grid(row=1,column=2, sticky=W, pady=10)
        self.label_ubicacion_terreno=Label(self.panel_categorias_preguntas, text="Ubicacion Terreno:", width=20)
        self.label_ubicacion_terreno.grid(row=1, column=3, sticky=W, pady=10)
        self.input_ubicacion_terreno=Entry(self.panel_categorias_preguntas, width=20)
        self.input_ubicacion_terreno.grid(row=1, column=4, sticky=W, pady=10)

        self.label_posee_vivienda=Label(self.panel_categorias_preguntas, text="Posee Vivienda:", width=20)
        self.label_posee_vivienda.grid(row=2,column=0, sticky=W, pady=10)

        self.radio_posee_vivienda_1=Radiobutton(self.panel_categorias_preguntas, text="SI", variable=self.posee_vivienda, value="SI", width=10)
        self.radio_posee_vivienda_1.grid(row=2,column=1, sticky=W, pady=10)
        self.radio_posee_vivienda_2=Radiobutton(self.panel_categorias_preguntas, text="NO", variable=self.posee_vivienda, value="NO", width=10)
        self.radio_posee_vivienda_2.grid(row=2,column=2, sticky=W, pady=10)
        self.label_condicion_vivienda=Label(self.panel_categorias_preguntas, text="Condicion Vivienda:", width=20)
        self.label_condicion_vivienda.grid(row=2,column=3, sticky=W, pady=10)
        self.input_condicion_vivienda=Entry(self.panel_categorias_preguntas, width=20)
        self.input_condicion_vivienda.grid(row=2, column=4, sticky=W,pady=10)

        self.label_necesidad_vivienda=Label(self.panel_categorias_preguntas, text="Necesidad Habitacional de:", width=20)
        self.label_necesidad_vivienda.grid(row=3,column=0, sticky=W, pady=10)
        self.radio_necesidad_vivienda_1=Radiobutton(self.panel_categorias_preguntas, text="Vivienda", variable=self.posee_vivienda, value="Vivienda", width=15)
        self.radio_necesidad_vivienda_1.grid(row=3,column=1, pady=10)
        self.radio_necesidad_vivienda_2=Radiobutton(self.panel_categorias_preguntas, text="Contruccion", variable=self.posee_vivienda, value="Contruccion", width=15)
        self.radio_necesidad_vivienda_2.grid(row=3,column=2, pady=10)
        self.radio_necesidad_vivienda_3=Radiobutton(self.panel_categorias_preguntas, text="Sustitucion", variable=self.posee_vivienda, value="Sustitucion", width=15)
        self.radio_necesidad_vivienda_3.grid(row=3,column=3, pady=10)
        self.radio_necesidad_vivienda_4=Radiobutton(self.panel_categorias_preguntas, text="Mejoramiento", variable=self.posee_vivienda, value="Mejoramiento", width=15)
        self.radio_necesidad_vivienda_4.grid(row=3,column=4, pady=10)

        self.label_gestion_organismo_oficial=Label(self.panel_categorias_preguntas, text="Gestion Organismo Ofical:", width=20)
        self.label_gestion_organismo_oficial.grid(row=4,column=0, sticky=W, pady=10)
        self.radio_gestion_organismo_1=Radiobutton(self.panel_categorias_preguntas, text="SI", variable=self.gestion_organismo, value="SI", width=10)
        self.radio_gestion_organismo_1.grid(row=4,column=1, sticky=W, pady=10)
        self.radio_gestion_organismo_2=Radiobutton(self.panel_categorias_preguntas, text="NO", variable=self.gestion_organismo, value="NO", width=10)
        self.radio_gestion_organismo_2.grid(row=4,column=2, sticky=W, pady=10)

        self.label_organismo_publico=Label(self.panel_categorias_preguntas, text="Nombre Organismo:", width=20)
        self.label_organismo_publico.grid(row=5, column=0, sticky=W, pady=10)
        self.radio_organismo_publico_1=Radiobutton(self.panel_categorias_preguntas, text="Gobernacion", variable=self.organismo_publico, value="Gobernacion", width=15)
        self.radio_organismo_publico_1.grid(row=6, column=0, pady=10)
        self.radio_organismo_publico_2=Radiobutton(self.panel_categorias_preguntas, text="INAVI", variable=self.organismo_publico, value="INAVI", width=15)
        self.radio_organismo_publico_2.grid(row=6, column=1, pady=10)
        self.radio_organismo_publico_3=Radiobutton(self.panel_categorias_preguntas, text="Malariologia", variable=self.organismo_publico, value="Malariologia", width=15)
        self.radio_organismo_publico_3.grid(row=6, column=2, pady=10)
        self.radio_organismo_publico_4=Radiobutton(self.panel_categorias_preguntas, text="Otra", variable=self.organismo_publico, value="Otra", width=15)
        self.radio_organismo_publico_4.grid(row=6, column=3, pady=10)

        self.label_organismo_privado=Label(self.panel_categorias_preguntas, text="Nombre Organismo:", width=20)
        self.label_organismo_privado.grid(row=7, column=0, sticky=W, pady=10)
        self.radio_organismo_privado_1=Radiobutton(self.panel_categorias_preguntas, text="Entidad Bancaria", variable=self.organismo_privado, value="Entidad Bancaria", width=20)
        self.radio_organismo_privado_1.grid(row=8, column=0, pady=10)
        self.entry_organismo_privado_1=Entry(self.panel_categorias_preguntas)
        self.entry_organismo_privado_1.grid(row=8, column=1, sticky=W, pady=10)
        self.radio_organismo_privado_2=Radiobutton(self.panel_categorias_preguntas, text="Empresa Promotora", variable=self.organismo_privado, value="Empresa Promotora", width=20)
        self.radio_organismo_privado_2.grid(row=8, column=2, sticky=W, pady=10)
        self.entry_organismo_privado_2=Entry(self.panel_categorias_preguntas)
        self.entry_organismo_privado_2.grid(row=8, column=3, sticky=W, pady=10)
        self.radio_organismo_privado_3=Radiobutton(self.panel_categorias_preguntas, text="Otra", variable=self.organismo_privado, value="Otra", width=20)
        self.radio_organismo_privado_3.grid(row=8, column=4, sticky=W, pady=10)
        self.entry_organismo_privado_3=Entry(self.panel_categorias_preguntas)
        self.entry_organismo_privado_3.grid(row=8, column=5, sticky=W, pady=10)

        self.label_fecha_gestion=Label(self.panel_categorias_preguntas, text="Fecha de la Gestion:", width=20)
        self.label_fecha_gestion.grid(row=9, column=0, sticky=W, pady=10)
        self.input_fecha_gestion=Entry(self.panel_categorias_preguntas, width=20)
        self.input_fecha_gestion.grid(row=9, column=1, sticky=W, pady=10)

        row=0
        column=0
        for row in range(4):
            self.panel_categorias_preguntas.rowconfigure(row)
            for column in range(6):
                self.panel_categorias_preguntas.columnconfigure(column)

    def preguntas_estado_viviendas(self):#-------------------------------------------------------------------------------
        self.tenencia_tierra=StringVar()
        self.tenencia_tierra.set("Otra")

        self.panel_categorias_preguntas=Frame(self.panel_cuestionarios, bg="gray")
        self.panel_categorias_preguntas.pack(fill="x", expand=False)

        self.titulo_datos_personales=Label(self.panel_categorias_preguntas, text="Estado de la Vivienda", width="20")
        self.titulo_datos_personales.grid(row=0, column=0, columnspan=2, pady=10)

        self.label_tenencia_tierra=Label(self.panel_categorias_preguntas, text="Tenencia de Tierra:", width="20")
        self.label_tenencia_tierra.grid(row=1,column=0, sticky=E, pady=10)
        self.radio_tenencia_tierra_1=Radiobutton(self.panel_categorias_preguntas, text="Propia", value="Propia", variable=self.tenencia_tierra, width="15")
        self.radio_tenencia_tierra_1.grid(row=1,column=1, pady=10)
        self.radio_tenencia_tierra_2=Radiobutton(self.panel_categorias_preguntas, text="Proceso de Pago", value="Proceso de Pago", variable=self.tenencia_tierra, width="15")
        self.radio_tenencia_tierra_2.grid(row=1,column=2, pady=10)
        self.radio_tenencia_tierra_3=Radiobutton(self.panel_categorias_preguntas, text="Cedida", value="Cedida", variable=self.tenencia_tierra, width="15")
        self.radio_tenencia_tierra_3.grid(row=1,column=3, pady=10)
        self.radio_tenencia_tierra_4=Radiobutton(self.panel_categorias_preguntas, text="Invadida", value="Invadida", variable=self.tenencia_tierra, width="15")
        self.radio_tenencia_tierra_4.grid(row=1,column=4, pady=10)
        self.radio_tenencia_tierra_5=Radiobutton(self.panel_categorias_preguntas, text="Otra", value="Otra", variable=self.tenencia_tierra, width="15")
        self.radio_tenencia_tierra_5.grid(row=1,column=5, pady=10)
        self.input_tenencia_tierra=Entry(self.panel_categorias_preguntas, width="20")
        self.input_tenencia_tierra.grid(row=1,column=6, sticky=W, pady=10)

        self.label_tiempo_ocupacion=Label(self.panel_categorias_preguntas, text="Tiempo de Ocupacion:", width="20")
        self.label_tiempo_ocupacion.grid(row=2,column=0 , sticky=E, pady=10)
        self.input_tiempo_ocupacion=Entry(self.panel_categorias_preguntas)
        self.input_tiempo_ocupacion.grid(row=2,column=1, sticky=W, pady=10)

        self.label_ambiente_vivienda=Label(self.panel_categorias_preguntas, text="Ambiente de la Vivienda:" , width="20")
        self.label_ambiente_vivienda.grid(row=3,column=0 , sticky=E, pady=10)

        self.label_num_sala=Label(self.panel_categorias_preguntas, text="Sala:", width="20")
        self.label_num_sala.grid(row=4,column=0, sticky=E, pady=10)
        self.input_num_sala=Entry(self.panel_categorias_preguntas, width="20")
        self.input_num_sala.grid(row=4,column=1, sticky=W, pady=10)

        self.label_num_bano_comedor=Label(self.panel_categorias_preguntas, text="Sala-Comedor:", width="20")
        self.label_num_bano_comedor.grid(row=4,column=2, sticky=E, pady=10)
        self.input_num_bano_comedor=Entry(self.panel_categorias_preguntas, width="20")
        self.input_num_bano_comedor.grid(row=4,column=3, sticky=W, pady=10)

        self.label_num_cocina=Label(self.panel_categorias_preguntas, text="Cocina:", width="20")
        self.label_num_cocina.grid(row=4,column=4, sticky=E, pady=10)
        self.input_num_cocina=Entry(self.panel_categorias_preguntas, width="20")
        self.input_num_cocina.grid(row=4,column=5, sticky=W, pady=10)

        self.label_num_cocina_comedor=Label(self.panel_categorias_preguntas, text="Cocina-Comedor:", width="20")
        self.label_num_cocina_comedor.grid(row=5,column=0, sticky=E, pady=10)
        self.input_num_cocina_comedor=Entry(self.panel_categorias_preguntas, width="20")
        self.input_num_cocina_comedor.grid(row=5,column=1, sticky=W, pady=10)

        self.label_num_bano=Label(self.panel_categorias_preguntas, text="Baño:", width="20")
        self.label_num_bano.grid(row=5,column=2, sticky=E, pady=10)
        self.input_num_bano=Entry(self.panel_categorias_preguntas, width="20")
        self.input_num_bano.grid(row=5,column=3, sticky=W, pady=10)

        self.label_num_dormitorio=Label(self.panel_categorias_preguntas, text="Dormitorios:", width="20")
        self.label_num_dormitorio.grid(row=5,column=4, sticky=E, pady=10)
        self.input_num_dormitorio=Entry(self.panel_categorias_preguntas, width="20")
        self.input_num_dormitorio.grid(row=5,column=5, sticky=W, pady=10)

        self.label_otros=Label(self.panel_categorias_preguntas, text="Otros:", width="20")
        self.label_otros.grid(row=6,column=0, sticky=E, pady=10)
        self.input_otros=Entry(self.panel_categorias_preguntas, width="20")
        self.input_otros.grid(row=6,column=1, sticky=W, pady=10)

        self.label_especificacion=Label(self.panel_categorias_preguntas, text="Especifique:", width="20")
        self.label_especificacion.grid(row=6,column=2, sticky=E, pady=10)
        self.input_especificacion=Entry(self.panel_categorias_preguntas, width="20")
        self.input_especificacion.grid(row=6,column=3, sticky=W, pady=10)

        self.label_tiempo_ocupacion=Label(self.panel_categorias_preguntas, text="Servicio en la Vivienda:", width="20")
        self.label_tiempo_ocupacion.grid(row=7,column=0 , sticky=E, pady=10)

        self.label_serv_agua=Label(self.panel_categorias_preguntas, text="Agua Potable:", width="20")
        self.label_serv_agua.grid(row=8,column=0, sticky=E, pady=10)
        self.input_serv_agua=Entry(self.panel_categorias_preguntas)
        self.input_serv_agua.grid(row=8,column=1, sticky=W, pady=10)

        self.label_serv_cloaca=Label(self.panel_categorias_preguntas, text="Red Cloaca:", width="20")
        self.label_serv_cloaca.grid(row=8,column=2, sticky=E, pady=10)
        self.input_serv_cloaca=Entry(self.panel_categorias_preguntas)
        self.input_serv_cloaca.grid(row=8,column=3, sticky=W, pady=10)

        self.label_serv_alumbrado=Label(self.panel_categorias_preguntas, text="Alumbrado Publico", width="20")
        self.label_serv_alumbrado.grid(row=8,column=4, sticky=E, pady=10)
        self.input_serv_alumbrado=Entry(self.panel_categorias_preguntas)
        self.input_serv_alumbrado.grid(row=8,column=5, sticky=W, pady=10)

        self.label_serv_telefono=Label(self.panel_categorias_preguntas, text="Aseo Publico:", width="20")
        self.label_serv_telefono.grid(row=9,column=0, sticky=E, pady=10)
        self.input_serv_telefono=Entry(self.panel_categorias_preguntas)
        self.input_serv_telefono.grid(row=9,column=1, sticky=W, pady=10)

        self.label_serv_aseo=Label(self.panel_categorias_preguntas, text="Telefono:", width="20")
        self.label_serv_aseo.grid(row=9,column=2, sticky=E, pady=10)
        self.input_serv_aseo=Entry(self.panel_categorias_preguntas)
        self.input_serv_aseo.grid(row=9,column=3, sticky=W, pady=10)

        self.label_serv_ninguno=Label(self.panel_categorias_preguntas, text="Ninguno:", width="20")
        self.label_serv_ninguno.grid(row=9,column=4, sticky=E, pady=10)
        self.input_serv_ninguno=Entry(self.panel_categorias_preguntas)
        self.input_serv_ninguno.grid(row=9,column=5, sticky=W, pady=10)

        self.label_serv_otro=Label(self.panel_categorias_preguntas, text="Otros ", width="20")
        self.label_serv_otro.grid(row=10,column=0, sticky=E, pady=10)
        self.input_serv_otro=Entry(self.panel_categorias_preguntas)
        self.input_serv_otro.grid(row=10,column=1, sticky=W, pady=10)

        self.label_serv_especifico=Label(self.panel_categorias_preguntas, text="Especifique:", width="20")
        self.label_serv_especifico.grid(row=10,column=2, sticky=E, pady=10)
        self.input_serv_especifico=Entry(self.panel_categorias_preguntas)
        self.input_serv_especifico.grid(row=10,column=3, sticky=W, pady=10)

        self.label_mate_contruccion=Label(self.panel_categorias_preguntas, text="Materiales de la Vivienda:", width="20")
        self.label_mate_contruccion.grid(row=11,column=0 , sticky=E, pady=10)

        self.label_mat_pared=Label(self.panel_categorias_preguntas, text="Material de Pared:", width="20")
        self.label_mat_pared.grid(row=12,column=0, sticky=E, pady=10)
        self.check_mat_pared_1=Checkbutton(self.panel_categorias_preguntas, text="Bloque", width="15")
        self.check_mat_pared_1.grid(row=13, column=0, pady=10)
        self.check_mat_pared_2=Checkbutton(self.panel_categorias_preguntas, text="Madera", width="15")
        self.check_mat_pared_2.grid(row=13, column=1, pady=10)
        self.check_mat_pared_3=Checkbutton(self.panel_categorias_preguntas, text="Zinc", width="15")
        self.check_mat_pared_3.grid(row=13, column=2, pady=10)
        self.check_mat_pared_4=Checkbutton(self.panel_categorias_preguntas, text="Bahareque", width="15")
        self.check_mat_pared_4.grid(row=13, column=3, pady=10)
        self.check_mat_pared_5=Checkbutton(self.panel_categorias_preguntas, text="Carton", width="15")
        self.check_mat_pared_5.grid(row=13, column=4, pady=10)

        self.label_mat_techo=Label(self.panel_categorias_preguntas, text="Material de Techo:", width="20")
        self.label_mat_techo.grid(row=14,column=0, sticky=E, pady=10)
        self.check_mat_techo_1=Checkbutton(self.panel_categorias_preguntas, text="Platabanda", width="15")
        self.check_mat_techo_1.grid(row=15, column=0, pady=10)
        self.check_mat_techo_2=Checkbutton(self.panel_categorias_preguntas, text="Asbesto", width="15")
        self.check_mat_techo_2.grid(row=15, column=1, pady=10)
        self.check_mat_techo_3=Checkbutton(self.panel_categorias_preguntas, text="Madera", width="15")
        self.check_mat_techo_3.grid(row=15, column=2, pady=10)
        self.check_mat_techo_4=Checkbutton(self.panel_categorias_preguntas, text="Zinc", width="15")
        self.check_mat_techo_4.grid(row=15, column=3, pady=10)
        self.check_mat_techo_5=Checkbutton(self.panel_categorias_preguntas, text="Otro", width="15")
        self.check_mat_techo_5.grid(row=15, column=4, pady=10)

        self.label_mat_piso=Label(self.panel_categorias_preguntas, text="Material de Piso:", width="20")
        self.label_mat_piso.grid(row=16,column=0, sticky=E, pady=10)
        self.check_mat_piso_1=Checkbutton(self.panel_categorias_preguntas, text="Cemento", width="15")
        self.check_mat_piso_1.grid(row=17, column=0, pady=10)
        self.check_mat_piso_2=Checkbutton(self.panel_categorias_preguntas, text="Ceramica", width="15")
        self.check_mat_piso_2.grid(row=17, column=1, pady=10)
        self.check_mat_piso_3=Checkbutton(self.panel_categorias_preguntas, text="Madera", width="15")
        self.check_mat_piso_3.grid(row=17, column=2, pady=10)
        self.check_mat_piso_4=Checkbutton(self.panel_categorias_preguntas, text="Vinil", width="15")
        self.check_mat_piso_4.grid(row=17, column=3, pady=10)
        self.check_mat_piso_5=Checkbutton(self.panel_categorias_preguntas, text="Tierra", width="15")
        self.check_mat_piso_5.grid(row=17, column=4, pady=10)
        self.check_mat_piso_5=Checkbutton(self.panel_categorias_preguntas, text="Otro", width="15")
        self.check_mat_piso_5.grid(row=17, column=5, pady=10)

        self.label_servicio_comunidad=Label(self.panel_categorias_preguntas, text="Servicio en la comunidad:", width="20")
        self.label_servicio_comunidad.grid(row=18,column=0 , sticky=E, pady=10)
        self.check_servicio_comunidad_1=Checkbutton(self.panel_categorias_preguntas, text="Agua potable", width="15")
        self.check_servicio_comunidad_1.grid(row=19, column=0, pady=10)
        self.check_servicio_comunidad_2=Checkbutton(self.panel_categorias_preguntas, text="Red cloacal", width="15")
        self.check_servicio_comunidad_2.grid(row=19, column=1, pady=10)
        self.check_servicio_comunidad_3=Checkbutton(self.panel_categorias_preguntas, text="Alumbrado Publico", width="15")
        self.check_servicio_comunidad_3.grid(row=19, column=2, pady=10)
        self.check_servicio_comunidad_4=Checkbutton(self.panel_categorias_preguntas, text="Aseo Urbano", width="15")
        self.check_servicio_comunidad_4.grid(row=19, column=3, pady=10)
        self.check_servicio_comunidad_5=Checkbutton(self.panel_categorias_preguntas, text="Telefono", width="15")
        self.check_servicio_comunidad_5.grid(row=19, column=4, pady=10)
        self.check_servicio_comunidad_5=Checkbutton(self.panel_categorias_preguntas, text="Transporte Publico", width="15")
        self.check_servicio_comunidad_5.grid(row=19, column=5, pady=10)
        self.check_servicio_comunidad_6=Checkbutton(self.panel_categorias_preguntas, text="Ninguno", width="15")
        self.check_servicio_comunidad_6.grid(row=19, column=6, pady=10)

        row=0
        column=0
        for row in range(20):
            self.panel_categorias_preguntas.rowconfigure(row)
            for column in range(7):
                self.panel_categorias_preguntas.columnconfigure(column)

    def footer_pagina_principal(self):
        self.panel_footer=Frame(self.panel_cuestionarios, bg="white")
        self.panel_footer.pack(side="bottom", fill="x", expand=False)

        self.boton_new_familar=Button(self.panel_footer, text="Agregar Familiar", bg="blue", command=self.crear_nuevo_panel_familiar)
        self.boton_new_familar.grid(row=0, column=0)
        self.boton_reset=Button(self.panel_footer, text="Limpiar Campos", bg="yellow")
        self.boton_reset.grid(row=0, column=1)
        self.boton_guardar=Button(self.panel_footer, text="Guardar" , bg="green")
        self.boton_guardar.grid(row=0, column=2)

        row=0
        column=0
        for row in range(1):
            self.panel_footer.rowconfigure(row, weight=1)
            for column in range(3):
                self.panel_footer.columnconfigure(column, weight=1)

    def mostrar_registrar_usuario(self):
        self.limpiar_panel_principal()

        self.pagina_principal = Frame(self.panel_principal, bg="yellow")
        self.pagina_principal.pack(fill=BOTH, expand=True)

        self.mostrar_panel_acciones()

        self.titulo=Label(self.pagina_principal, text="Registrar datos de un Funcionario")
        self.titulo.pack(side=TOP, fill=X, expand=False)

        self.panel_principal_cuestionarios=Frame(self.pagina_principal)
        self.panel_principal_cuestionarios.pack(fill="both", expand=True)

        self.panel_canvas=Canvas(self.panel_principal_cuestionarios)
        self.panel_canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar_y=Scrollbar(self.panel_principal_cuestionarios, command=self.panel_canvas.yview)
        self.scrollbar_y.pack(side="right", fill="y")

        self.panel_canvas.configure(yscrollcommand=self.scrollbar_y.set)
        """
        self.scrollbar_x=Scrollbar(self.panel_principal_cuestionarios, command=self.panel_canvas.xview)
        self.scrollbar_x.pack(side="bottom", fill="x")

        self.panel_canvas.configure(xscrollcommand=self.scrollbar_x.set)
        """
        self.panel_cuestionarios=Frame(self.panel_canvas, bg="blue")
        self.canvas_window = self.panel_canvas.create_window(
                (0, 0),              # coordenadas x, y
                window=self.panel_cuestionarios,  # el frame que va dentro
                anchor="nw"           # anclaje en la esquina noroeste
            )

        def actualizar_scrollregion(event):
            self.panel_canvas.configure(scrollregion=self.panel_canvas.bbox("all"))

        self.panel_cuestionarios.bind("<Configure>", actualizar_scrollregion)

        self.footer_pagina_principal()

        self.preguntas_datos_personales()
        self.preguntas_datos_laborales()
        self.preguntas_plan_vivienda()
        self.preguntas_estado_viviendas()
        self.preguntas_datos_familiares()

#Programa Principal
if __name__ == "__main__":
    root = Tk()
    app = UI(root)
    root.mainloop()