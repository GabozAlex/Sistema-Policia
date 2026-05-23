from tkinter import *
from tkinter import ttk, messagebox, simpledialog
from logic import (Funcionario, Familiar, cargar_funcionarios, guardar_funcionarios,
                   verificar_login, eliminar_funcionario, restaurar_funcionario,
                   crear_usuario, eliminar_usuario, obtener_usuarios,
                   obtener_auditoria, registrar_auditoria, ROLES)

class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienestar y Proteccion Social - Sistema Policia")
        self.root.minsize(950, 680)
        self.root.geometry("950x680")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.bg = "#f0f2f5"
        self.bg_card = "#ffffff"
        self.primary = "#1a73e8"
        self.primary_hover = "#1557b0"
        self.danger = "#dc3545"
        self.success = "#28a745"
        self.warning = "#ffc107"
        self.text = "#202124"
        self.text_sec = "#5f6368"
        self.border = "#dadce0"

        self.style.configure(".", font=("Segoe UI", 10), background=self.bg)
        self.style.configure("Card.TFrame", background=self.bg_card, relief="solid", borderwidth=1)
        self.style.configure("CardTitle.TLabel", font=("Segoe UI", 12, "bold"), background=self.bg_card, foreground=self.text)
        self.style.configure("Title.TLabel", font=("Segoe UI", 16, "bold"), foreground=self.text)
        self.style.configure("Subtitle.TLabel", font=("Segoe UI", 11), foreground=self.text_sec)
        self.style.configure("Field.TLabel", font=("Segoe UI", 10), background=self.bg_card, foreground=self.text)
        self.style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), background=self.primary, foreground="white", borderwidth=0)
        self.style.map("Accent.TButton", background=[("active", self.primary_hover)])
        self.style.configure("Danger.TButton", font=("Segoe UI", 10), background=self.danger, foreground="white", borderwidth=0)
        self.style.map("Danger.TButton", background=[("active", "#c82333")])
        self.style.configure("Success.TButton", font=("Segoe UI", 10, "bold"), background=self.success, foreground="white", borderwidth=0)
        self.style.map("Success.TButton", background=[("active", "#218838")])
        self.style.configure("Warning.TButton", font=("Segoe UI", 10), background=self.warning, foreground=self.text, borderwidth=0)
        self.style.map("Warning.TButton", background=[("active", "#e0a800")])
        self.style.configure("TEntry", fieldbackground=self.bg_card, foreground=self.text, borderwidth=1, relief="solid")
        self.style.configure("TNotebook", background=self.bg, borderwidth=0)
        self.style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[15, 6], background=self.border, foreground=self.text_sec)
        self.style.map("TNotebook.Tab", background=[("selected", self.bg_card)], foreground=[("selected", self.primary)])
        self.style.configure("Treeview", font=("Segoe UI", 10), rowheight=32, fieldbackground=self.bg_card, foreground=self.text)
        self.style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background=self.border, foreground=self.text)
        self.style.map("Treeview", background=[("selected", "#e8f0fe")], foreground=[("selected", self.text)])
        self.style.configure("TSpinbox", fieldbackground=self.bg_card)
        self.style.configure("TRadiobutton", font=("Segoe UI", 10), background=self.bg_card, foreground=self.text)
        self.style.configure("TCheckbutton", font=("Segoe UI", 10), background=self.bg_card, foreground=self.text)

        self.panel_principal = Frame(root, bg=self.bg)
        self.panel_principal.pack(fill=BOTH, expand=True)

        self.funcionarios = []
        self.mostrar_inactivos = False
        self.usuario_actual = None
        self.usuario_rol = None
        self.editando_cedula = None
        self.familiares_panels = []

        self.inicio_sesion()

    def limpiar_panel_principal(self):
        for widget in self.panel_principal.winfo_children():
            widget.destroy()

    def inicio_sesion(self):
        self.limpiar_panel_principal()

        topbar = Frame(self.panel_principal, bg=self.primary, height=6)
        topbar.pack(fill=X)
        topbar.pack_propagate(False)

        container = Frame(self.panel_principal, bg=self.bg)
        container.pack(fill=BOTH, expand=True)

        card = Frame(container, bg=self.bg_card)
        card.place(relx=0.5, rely=0.45, anchor=CENTER)

        Label(card, text="\U0001f6e1", font=("Segoe UI", 36),
              bg=self.bg_card, fg=self.primary).pack(pady=(35, 5))
        Label(card, text="Bienestar y Proteccion Social", font=("Segoe UI", 18, "bold"),
              bg=self.bg_card, fg=self.primary).pack(pady=(0, 5))
        Label(card, text="Sistema de Gestion Policial", font=("Segoe UI", 11),
              bg=self.bg_card, fg=self.text_sec).pack(pady=(0, 30))

        frame = Frame(card, bg=self.bg_card)
        frame.pack(padx=50, pady=(0, 35))

        Label(frame, text="Usuario", font=("Segoe UI", 10),
              bg=self.bg_card, fg=self.text, anchor=W).grid(row=0, column=0, sticky=W, pady=(0, 3))
        self.input_usuario = Entry(frame, font=("Segoe UI", 12), relief="solid", borderwidth=1,
                                   highlightbackground=self.border, highlightthickness=1, highlightcolor=self.primary)
        self.input_usuario.grid(row=1, column=0, pady=(0, 12), ipady=5, ipadx=6)
        self.input_usuario.focus()

        Label(frame, text="Contrasena", font=("Segoe UI", 10),
              bg=self.bg_card, fg=self.text, anchor=W).grid(row=2, column=0, sticky=W, pady=(0, 3))
        self.input_contrasena = Entry(frame, font=("Segoe UI", 12), show="*", relief="solid", borderwidth=1,
                                      highlightbackground=self.border, highlightthickness=1, highlightcolor=self.primary)
        self.input_contrasena.grid(row=3, column=0, pady=(0, 18), ipady=5, ipadx=6)
        self.input_contrasena.bind("<Return>", lambda e: self.verificar_login())

        self.label_error = Label(frame, text="", font=("Segoe UI", 9), bg=self.bg_card, fg=self.danger)
        self.label_error.grid(row=4, column=0, pady=(0, 8))

        Button(frame, text="Iniciar Sesion", font=("Segoe UI", 12, "bold"), bg=self.primary, fg="white",
               activebackground=self.primary_hover, activeforeground="white", relief="flat", borderwidth=0,
               cursor="hand2", command=self.verificar_login).grid(row=5, column=0, sticky=EW, ipady=7)

        modo = "MODO PRUEBA" if __import__('os').environ.get("DB_MODE") == "test" else ""
        texto_footer = f"\u00a9 {__import__('datetime').datetime.now().year} Sistema Policial v1.0. Todos los derechos reservados."
        if modo:
            texto_footer = f"{modo} - {texto_footer}"
        Label(container, text=texto_footer,
              font=("Segoe UI", 8), bg=self.bg, fg=self.text_sec).pack(side=BOTTOM, pady=15)

        Button(container, text="Salir", font=("Segoe UI", 10), bg=self.danger, fg="white",
               activebackground="#c82333", activeforeground="white", relief="flat", borderwidth=0,
               command=self.root.quit, cursor="hand2").pack(side=BOTTOM, pady=(0, 10))

    def verificar_login(self):
        u = self.input_usuario.get()
        p = self.input_contrasena.get()
        user = verificar_login(u, p)
        if user:
            self.usuario_actual = user["username"]
            self.usuario_rol = user["rol"]
            self.mostrar_pagina_principal()
        else:
            self.label_error.config(text="Usuario o contrasena incorrectos")

    def _puede(self, permiso):
        return ROLES.get(self.usuario_rol, {}).get(permiso, False)

    def mostrar_panel_acciones(self):
        panel = Frame(self.pagina_principal, bg=self.primary, width=220, highlightthickness=0)
        panel.pack(side=LEFT, fill=Y)
        panel.pack_propagate(False)

        # Header with icon
        header = Frame(panel, bg=self.primary)
        header.pack(fill=X, pady=(20, 0))
        Label(header, text="\U0001f6e1", font=("Segoe UI", 18),
              bg=self.primary, fg="white").pack()
        Label(header, text="Bienestar Social", font=("Segoe UI", 13, "bold"),
              bg=self.primary, fg="white").pack(pady=(2, 10))

        # User info card
        user_card = Frame(panel, bg=self.primary_hover, highlightthickness=0)
        user_card.pack(fill=X, padx=12, pady=(0, 12), ipady=6)
        Label(user_card, text=f"{self.usuario_actual}", font=("Segoe UI", 12, "bold"),
              bg=self.primary_hover, fg="white").pack(pady=(6, 1))
        Label(user_card, text=f"Rol: {self.usuario_rol}", font=("Segoe UI", 9),
              bg=self.primary_hover, fg="#d2e3fc").pack(pady=(0, 6))

        # Separator
        Frame(panel, bg="#ffffff", height=1).pack(fill=X, padx=15, pady=(0, 8))

        btn_style = {"font": ("Segoe UI", 10), "bg": self.primary, "fg": "white",
                     "activebackground": self.primary_hover, "activeforeground": "white",
                     "relief": "flat", "borderwidth": 0, "cursor": "hand2", "anchor": W}

        btn_hover = {"bg": self.primary_hover}

        def make_btn(text, cmd, icon=""):
            b = Button(panel, text=f"  {icon} {text}".rstrip() if icon else f"  {text}",
                       **btn_style, command=cmd)
            b.pack(fill=X, padx=10, pady=2, ipady=7)
            b.bind("<Enter>", lambda e: b.configure(**btn_hover))
            b.bind("<Leave>", lambda e: b.configure(bg=self.primary))
            return b

        make_btn("Inicio", self.mostrar_pagina_principal, "\U0001f3e0")
        Frame(panel, bg="#ffffff", height=1).pack(fill=X, padx=15, pady=6)
        make_btn("Ayuda", self.mostrar_ayuda, "\u2753")
        if self._puede("crear"):
            make_btn("Nuevo Funcionario", self.mostrar_registrar_usuario, "\u2795")
        if self.usuario_rol == "admin":
            Frame(panel, bg="#ffffff", height=1).pack(fill=X, padx=15, pady=6)
            make_btn("Gestionar Usuarios", self.gestionar_usuarios, "\u2699")
        if self.usuario_rol in ("admin", "subadmin"):
            if self.usuario_rol == "subadmin":
                Frame(panel, bg="#ffffff", height=1).pack(fill=X, padx=15, pady=6)
            make_btn("Ver Auditoria", self.ver_auditoria, "\U0001f4cb")

        # Logout at bottom
        Frame(panel, bg="#ffffff", height=1).pack(fill=X, padx=15, pady=6)
        logout_btn = Button(panel, text="  \u23f3 Cerrar Sesion",
                            font=("Segoe UI", 10), fg="white",
                            bg="#dc3545", activebackground="#c82333",
                            activeforeground="white", relief="flat",
                            borderwidth=0, cursor="hand2", anchor=W,
                            command=self.cerrar_sesion)
        logout_btn.pack(side=BOTTOM, fill=X, padx=10, pady=15, ipady=7)

    def mostrar_ayuda(self):
        self.limpiar_panel_principal()
        self.pagina_principal = Frame(self.panel_principal, bg=self.bg)
        self.pagina_principal.pack(fill=BOTH, expand=True)

        self.mostrar_panel_acciones()

        content = Frame(self.pagina_principal, bg=self.bg)
        content.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        canvas = Canvas(content, bg=self.bg_card, highlightthickness=0)
        scroll = ttk.Scrollbar(content, orient=VERTICAL, command=canvas.yview)
        scroll_frame = Frame(canvas, bg=self.bg_card)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor=NW)
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)

        xpad = 25

        def titulo(texto, size=16, pady=(20, 5)):
            Label(scroll_frame, text=texto, font=("Segoe UI", size, "bold"),
                  bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=xpad, pady=pady)
            Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=xpad)

        def subtitulo(texto):
            Label(scroll_frame, text=texto, font=("Segoe UI", 12, "bold"),
                  bg=self.bg_card, fg=self.text).pack(anchor=W, padx=xpad, pady=(12, 3))

        def parrafo(texto):
            Label(scroll_frame, text=texto, font=("Segoe UI", 10), wraplength=600, justify=LEFT,
                  bg=self.bg_card, fg=self.text).pack(anchor=W, padx=xpad, pady=(0, 6))

        titulo("Manual del Sistema")

        subtitulo("Secciones del Programa")
        parrafo("Inicio: Pantalla principal que lista todos los funcionarios registrados. "
                "Permite buscar, filtrar inactivos, y acceder a las acciones de cada registro (Ver, Editar, Desactivar, Restaurar).")
        parrafo("Nuevo Funcionario: Formulario de varios pasos (pestanas) para registrar un nuevo funcionario. "
                "Incluye datos personales, laborales, plan de vivienda, estado de la vivienda y grupo familiar.")
        parrafo("Ver Datos: Muestra la ficha completa de un funcionario con toda su informacion en detalle. "
                "Desde ahi se puede imprimir, exportar a PDF, guardar TXT, editar o desactivar.")
        parrafo("Gestionar Usuarios (Admin): Panel para administrar las cuentas de usuario del sistema. "
                "Permite agregar y eliminar usuarios.")
        parrafo("Ver Auditoria (Admin/SubAdmin): Registro cronologico de todas las acciones realizadas en el sistema "
                "(creaciones, modificaciones, eliminaciones) con fecha, usuario y detalle.")

        subtitulo("Roles de Usuario")
        parrafo("Cada usuario tiene un rol que determina lo que puede hacer dentro del sistema:")

        roles_info = [
            ("Visor (viewer)", "Solo puede ver la informacion. No puede crear, modificar ni eliminar registros."),
            ("Editor (editor)", "Puede ver y crear nuevos funcionarios. No puede modificar ni eliminar."),
            ("Modificador (modifier)", "Puede ver, crear y modificar funcionarios. No puede eliminar."),
            ("SubAdmin (subadmin)", "Puede ver, crear, modificar, eliminar (desactivar) y restaurar funcionarios. "
             "Tambien puede ver el registro de auditoria. No gestiona usuarios."),
        ]
        for rol, desc in roles_info:
            Label(scroll_frame, text=f"  \u2022 {rol}", font=("Segoe UI", 10, "bold"),
                  bg=self.bg_card, fg=self.text).pack(anchor=W, padx=xpad, pady=(6, 1))
            parrafo(f"    {desc}")

        subtitulo("Usuarios del Sistema")
        parrafo("A continuacion se listan los usuarios preconfigurados. "
                "Contacte al administrador si necesita una cuenta con diferentes permisos.")

        user_info = [
            ("visor / visor123", "Rol: Visor — Solo lectura"),
            ("editor / editor123", "Rol: Editor — Ver y crear"),
            ("modificador / mod123", "Rol: Modificador — Ver, crear y modificar"),
            ("subadmin / sub123", "Rol: SubAdmin — Acceso completo sin gestion de usuarios"),
        ]
        for cred, desc in user_info:
            Label(scroll_frame, text=f"  \u2022 {cred}", font=("Segoe UI", 10, "bold"),
                  bg=self.bg_card, fg=self.text).pack(anchor=W, padx=xpad, pady=(4, 1))
            parrafo(f"    {desc}")

        subtitulo("Funcionalidades Adicionales")
        parrafo("Imprimir / Exportar: Desde la ficha de un funcionario puede imprimir directamente, "
                "exportar a PDF o guardar un archivo de texto con los datos.")
        parrafo("Filtro de Inactivos: Marque 'Ver inactivos' en la pantalla principal para mostrar "
                "los funcionarios desactivados y poder restaurarlos.")
        parrafo("Modo Prueba: Ejecute el programa con la variable DB_MODE=test para usar una base "
                "de datos separada de prueba sin afectar los datos reales.")

        subtitulo("Seguridad")
        parrafo("Todas las acciones quedan registradas en el modulo de Auditoria. "
                "Las eliminaciones son logicas (desactivacion), los datos nunca se pierden.")

        Label(scroll_frame, text="", bg=self.bg_card).pack(pady=20)

    def mostrar_pagina_principal(self):
        self.limpiar_panel_principal()
        self.pagina_principal = Frame(self.panel_principal, bg=self.bg)
        self.pagina_principal.pack(fill=BOTH, expand=True)

        self.mostrar_panel_acciones()

        content = Frame(self.pagina_principal, bg=self.bg)
        content.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        Label(content, text="Funcionarios Registrados", font=("Segoe UI", 18, "bold"),
              bg=self.bg, fg=self.text).pack(anchor=W, pady=(0, 5))
        Label(content, text="Gestione los funcionarios del sistema", font=("Segoe UI", 10),
              bg=self.bg, fg=self.text_sec).pack(anchor=W, pady=(0, 15))

        bar = Frame(content, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        bar.pack(fill=X, pady=(0, 15))

        if self._puede("crear"):
            Button(bar, text="+ Nuevo Funcionario", font=("Segoe UI", 10, "bold"), bg=self.success, fg="white",
                   activebackground="#218838", activeforeground="white", relief="flat", borderwidth=0,
                   cursor="hand2", command=self.mostrar_registrar_usuario).pack(side=LEFT, padx=10, pady=8, ipady=5)

        Label(bar, text="Buscar:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).pack(side=LEFT, padx=(20, 5))
        self.input_busqueda = Entry(bar, font=("Segoe UI", 10), relief="solid", borderwidth=1,
                                    highlightbackground=self.border, highlightthickness=1)
        self.input_busqueda.pack(side=LEFT, ipady=3, ipadx=3)
        self.input_busqueda.bind("<Return>", lambda e: self.buscar_funcionario())

        Button(bar, text="Buscar", font=("Segoe UI", 10), bg=self.primary, fg="white",
               activebackground=self.primary_hover, activeforeground="white", relief="flat", borderwidth=0,
               cursor="hand2", command=self.buscar_funcionario).pack(side=LEFT, padx=5, pady=8, ipady=4)

        self.mostrar_inactivos_var = IntVar()
        Checkbutton(bar, text="Ver inactivos", font=("Segoe UI", 9), variable=self.mostrar_inactivos_var,
                    bg=self.bg_card, fg=self.text, activebackground=self.bg_card,
                    activeforeground=self.primary, selectcolor=self.bg_card,
                    command=self.toggle_inactivos).pack(side=RIGHT, padx=10)

        # Action bar
        action_bar = Frame(content, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        action_bar.pack(fill=X, pady=(0, 10))

        Button(action_bar, text="Ver Datos", font=("Segoe UI", 10), bg=self.primary, fg="white",
               activebackground=self.primary_hover, activeforeground="white", relief="flat", borderwidth=0,
               cursor="hand2", command=self.ver_funcionario).pack(side=LEFT, padx=5, pady=5, ipady=5)
        if self._puede("modificar"):
            Button(action_bar, text="Editar", font=("Segoe UI", 10), bg=self.warning, fg=self.text,
                   activebackground="#e0a800", relief="flat", borderwidth=0, cursor="hand2",
                   command=self.editar_funcionario).pack(side=LEFT, padx=5, pady=5, ipady=5)
        if self._puede("eliminar"):
            Button(action_bar, text="Desactivar", font=("Segoe UI", 10), bg=self.danger, fg="white",
                   activebackground="#c82333", activeforeground="white", relief="flat", borderwidth=0,
                   cursor="hand2", command=self.desactivar_funcionario).pack(side=LEFT, padx=5, pady=5, ipady=5)
        if self.usuario_rol in ("admin", "subadmin"):
            Button(action_bar, text="Restaurar", font=("Segoe UI", 10), bg=self.success, fg="white",
                   activebackground="#218838", relief="flat", borderwidth=0,
                   cursor="hand2", command=self.restaurar_funcionario).pack(side=LEFT, padx=5, pady=5, ipady=5)

        # Treeview
        tree_frame = Frame(content, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        tree_frame.pack(fill=BOTH, expand=True)

        columns = ("Cedula", "Nombre", "Apellido", "Edad", "Telefono")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", selectmode="browse")
        for col in columns:
            self.tree.heading(col, text=col)
        self.tree.column("Cedula", width=120, anchor=CENTER)
        self.tree.column("Nombre", width=180)
        self.tree.column("Apellido", width=180)
        self.tree.column("Edad", width=70, anchor=CENTER)
        self.tree.column("Telefono", width=130, anchor=CENTER)

        scroll_y = ttk.Scrollbar(tree_frame, orient=VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll_y.set)
        self.tree.pack(side=LEFT, fill=BOTH, expand=True, padx=5, pady=5)
        scroll_y.pack(side=RIGHT, fill=Y, pady=5)

        self.tree.tag_configure("even", background="#f8f9fa")
        self.tree.tag_configure("inactivo", background="#ffe0e0", foreground="#999")
        self.tree.bind("<Double-1>", lambda e: self.ver_funcionario())
        self.tree.bind("<Delete>", lambda e: self.desactivar_funcionario())

        self.funcionarios = cargar_funcionarios()
        self.cargar_en_tabla()

    def cargar_en_tabla(self, filtro=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if filtro:
            lista = [f for f in self.funcionarios
                     if (self.mostrar_inactivos or (hasattr(f, 'activo') and f.activo == 1) or not hasattr(f, 'activo'))
                     and (filtro.lower() in (f.nombre or "").lower()
                          or filtro.lower() in (f.apellido or "").lower()
                          or filtro.lower() in (f.cedula or "").lower())]
        else:
            lista = [f for f in self.funcionarios
                     if (self.mostrar_inactivos or (hasattr(f, 'activo') and f.activo == 1) or not hasattr(f, 'activo'))]
        for i, f in enumerate(lista):
            tag = "inactivo" if (hasattr(f, 'activo') and f.activo == 0) else ("even" if i % 2 == 0 else "odd")
            nombre = f.nombre or ""; apellido = f.apellido or ""; cedula = f.cedula or ""
            edad = f.edad or ""; telefono = f.telefono or ""
            self.tree.insert("", END, iid=cedula, values=(cedula, nombre, apellido, edad, telefono), tags=(tag,))

    def toggle_inactivos(self):
        self.mostrar_inactivos = self.mostrar_inactivos_var.get()
        self.cargar_en_tabla()

    def buscar_funcionario(self):
        self.funcionarios = cargar_funcionarios()
        texto = self.input_busqueda.get().strip()
        self.cargar_en_tabla(filtro=texto if texto else None)

    def ver_funcionario(self, cedula=None):
        if cedula is None:
            sel = self.tree.selection()
            if not sel: return
            cedula = sel[0]

        self._clear_imprimir_frame()

        for f in self.funcionarios:
            if f.cedula == cedula:
                func = f; break
        else:
            return

        self.limpiar_panel_principal()
        self.pagina_principal = Frame(self.panel_principal, bg=self.bg)
        self.pagina_principal.pack(fill=BOTH, expand=True)

        self.mostrar_panel_acciones()

        self._imprimir_content = Frame(self.pagina_principal, bg=self.bg)
        self._imprimir_content.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        content = Frame(self._imprimir_content, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        content.pack(fill=BOTH, expand=True)

        canvas = Canvas(content, bg=self.bg_card, highlightthickness=0)
        scroll = ttk.Scrollbar(content, orient=VERTICAL, command=canvas.yview)
        scroll_frame = Frame(canvas, bg=self.bg_card)

        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor=NW)
        canvas.configure(yscrollcommand=scroll.set)

        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)

        Label(scroll_frame, text="Datos Personales", font=("Segoe UI", 16, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(20, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 10))

        fields = [
            ("Cedula", func.cedula),
            ("Nombre", func.nombre),
            ("Apellido", func.apellido),
            ("Fecha de Nacimiento", func.fecha_nacimiento or ""),
            ("Edad", func.edad or ""),
            ("Estado Civil", func.estado_civil or ""),
            ("Telefono", func.telefono or ""),
            ("Peso", func.peso or ""),
            ("Altura", func.altura or ""),
        ]
        self._crear_field_grid(scroll_frame, fields)

        if func.residencia:
            Label(scroll_frame, text="Direccion", font=("Segoe UI", 12, "bold"),
                  bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
            Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))
            self._crear_field_grid(scroll_frame, [("Direccion", func.residencia or "")])

        Label(scroll_frame, text="Datos Laborales", font=("Segoe UI", 12, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))

        laboral_fields = [
            ("Jerarquia", func.jerarquia or ""),
            ("Lugar de Servicio", func.lugar_presta_servicio or ""),
            ("Tiempo de Servicio", func.tiempo_servicio or ""),
            ("Salario Mensual", func.salario_mensual or ""),
            ("Fecha de Gestion", func.fecha_gestion or ""),
        ]
        self._crear_field_grid(scroll_frame, laboral_fields)

        Label(scroll_frame, text="Plan Vivienda", font=("Segoe UI", 12, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))

        plan_fields = [
            ("Terreno Propio", func.terreno_propio or ""),
            ("Ubicacion del Terreno", func.ubicacion_terreno or ""),
            ("Condicion de Vivienda", func.condicion_vivienda or ""),
            ("Necesidad Habitacional", func.necesidad_vivienda or ""),
            ("Organismo Publico", func.organismo_publico or ""),
            ("Organismo Privado", func.organismo_privado or ""),
            ("Gestion Organismo Oficial", func.gestion_organismo_oficial or ""),
            ("Fecha de Gestion", func.fecha_gestion or ""),
        ]
        self._crear_field_grid(scroll_frame, plan_fields)

        Label(scroll_frame, text="Estado de la Vivienda", font=("Segoe UI", 12, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))

        estado_fields = [
            ("Tenencia de Tierra", func.tenencia_tierra or ""),
            ("Tiempo de Ocupacion", func.tiempo_ocupacion or ""),
            ("Ambiente de Vivienda", func.ambiente_vivienda or ""),
            ("Servicios Disponibles", func.servicio_vivienda_disponible or ""),
            ("Materiales de Vivienda", func.materiales_vivienda or ""),
            ("Servicios de la Comunidad", func.servicio_comunidad or ""),
        ]
        self._crear_field_grid(scroll_frame, estado_fields)

        if func.grupo_familiar:
            Label(scroll_frame, text="Grupo Familiar", font=("Segoe UI", 12, "bold"),
                  bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
            Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))
            for i, fam in enumerate(func.grupo_familiar):
                Label(scroll_frame, text=f"Familiar {i+1}", font=("Segoe UI", 10, "bold"),
                      bg=self.bg_card, fg=self.text).pack(anchor=W, padx=25, pady=(6, 0))
                self._crear_field_grid(scroll_frame, [
                    ("Nombre Completo", f"{fam.nombre or ''} {fam.apellido or ''}"),
                    ("Parentesco", fam.parentesco or ""),
                    ("Edad", fam.edad or ""),
                    ("Genero", fam.genero or ""),
                    ("Estado Civil", fam.estado_civil or ""),
                    ("Nivel Educacion", fam.nivel_educacion or ""),
                    ("Profesion/Oficio", fam.profesion_oficio or ""),
                    ("Lugar de Trabajo", fam.lugar_trabajo or ""),
                    ("Ingreso Mensual", fam.ingreso_mensual or ""),
                    ("Observacion", fam.observacion or ""),
                ])

        Label(scroll_frame, text="", bg=self.bg_card).pack(pady=10)

        btn_frame = Frame(content, bg=self.bg_card)
        btn_frame.pack(fill=X, padx=20, pady=(0, 15))
        btn_left = Frame(btn_frame, bg=self.bg_card)
        btn_left.pack(side=LEFT)
        btn_right = Frame(btn_frame, bg=self.bg_card)
        btn_right.pack(side=RIGHT)

        Button(btn_left, text="Imprimir Ficha", font=("Segoe UI", 10), bg=self.primary, fg="white",
               activebackground=self.primary_hover, relief="flat", borderwidth=0,
               cursor="hand2", command=lambda: self.imprimir_ficha(func)).pack(side=LEFT, padx=5, ipady=5)
        if self._puede("modificar"):
            Button(btn_left, text="Editar", font=("Segoe UI", 10), bg=self.warning, fg=self.text,
                   activebackground="#e0a800", relief="flat", borderwidth=0, cursor="hand2",
                   command=lambda: self.editar_funcionario(cedula)).pack(side=LEFT, padx=5, ipady=5)
        if self._puede("eliminar"):
            Button(btn_left, text="Desactivar", font=("Segoe UI", 10), bg=self.danger, fg="white",
                   activebackground="#c82333", relief="flat", borderwidth=0, cursor="hand2",
                   command=lambda: self.desactivar_funcionario(cedula, content.get_toplevel() if content.winfo_toplevel() != self.root else None)).pack(side=LEFT, padx=5, ipady=5)
        if self.usuario_rol in ("admin", "subadmin"):
            Button(btn_left, text="Restaurar", font=("Segoe UI", 10), bg=self.success, fg="white",
                   activebackground="#218838", relief="flat", borderwidth=0, cursor="hand2",
                   command=lambda: self.restaurar_funcionario(cedula, content.get_toplevel() if content.winfo_toplevel() != self.root else None)).pack(side=LEFT, padx=5, ipady=5)
        Button(btn_right, text="Volver", font=("Segoe UI", 10), bg="#6c757d", fg="white",
               activebackground="#5a6268", relief="flat", borderwidth=0,
               cursor="hand2", command=self.mostrar_pagina_principal).pack(side=RIGHT, padx=5, ipady=5)

    def _clear_imprimir_frame(self):
        if hasattr(self, '_imprimir_content') and self._imprimir_content:
            try:
                self._imprimir_content.destroy()
            except: pass
        self._imprimir_content = None

    def _crear_field_grid(self, parent, fields):
        frame = Frame(parent, bg=self.bg_card)
        frame.pack(fill=X, padx=10)
        for i, (label, value) in enumerate(fields):
            lbl = Label(frame, text=f"{label}:", font=("Segoe UI", 10, "bold"),
                        bg=self.bg_card, fg=self.text_sec, width=28, anchor=W)
            lbl.grid(row=i, column=0, sticky=W, padx=(25, 5), pady=2)
            val = Label(frame, text=value if value else "-", font=("Segoe UI", 10),
                        bg=self.bg_card, fg=self.text, anchor=W)
            val.grid(row=i, column=1, sticky=W, pady=2)
            val.bind("<MouseWheel>", lambda e: self._parent_canvas(event=e))

    def _parent_canvas(self, event):
        widget = event.widget
        while widget:
            if isinstance(widget, Canvas):
                widget.yview_scroll(int(-1 * (event.delta / 120)), "units")
                return
            widget = widget.master

    def imprimir_ficha(self, func):
        def exportar_pdf():
            from fpdf import FPDF
            import platform, os, subprocess
            pdf = FPDF()
            pdf.add_page()
            pdf.set_auto_page_break(auto=True, margin=15)
            try:
                font_path = None
                sys_name = platform.system()
                if sys_name == "Windows":
                    font_path = "C:\\Windows\\Fonts\\arial.ttf"
                elif sys_name == "Linux":
                    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
                if font_path and os.path.exists(font_path):
                    pdf.add_font("CustomFont", "", font_path, uni=True)
                    pdf.set_font("CustomFont", "", 12)
                else:
                    pdf.set_font("Courier", "", 10)
            except:
                pdf.set_font("Courier", "", 10)

            pdf.cell(0, 10, f"Ficha de Funcionario - {func.nombre} {func.apellido}", ln=True, align="C")
            pdf.ln(5)
            try:
                pdf.set_font("CustomFont", "", 10)
            except:
                pdf.set_font("Courier", "", 10)

            def write_section(title, data):
                try:
                    pdf.set_font("CustomFont", "", 11)
                except:
                    pdf.set_font("Courier", "", 11)
                pdf.cell(0, 8, title, ln=True)
                try:
                    pdf.set_font("CustomFont", "", 10)
                except:
                    pdf.set_font("Courier", "", 10)
                for k, v in data:
                    pdf.cell(0, 7, f"{k}: {v if v else '-'}", ln=True)
                pdf.ln(3)

            write_section("Datos Personales", [
                ("Cedula", func.cedula), ("Nombre", func.nombre),
                ("Apellido", func.apellido), ("Fecha Nacimiento", func.fecha_nacimiento),
                ("Edad", func.edad), ("Estado Civil", func.estado_civil),
                ("Telefono", func.telefono), ("Peso", func.peso or ""),
                ("Altura", func.altura or ""), ("Direccion", func.residencia or ""),
            ])
            write_section("Datos Laborales", [
                ("Jerarquia", func.jerarquia or ""),
                ("Lugar Servicio", func.lugar_presta_servicio or ""),
                ("Tiempo Servicio", func.tiempo_servicio or ""),
                ("Salario Mensual", func.salario_mensual or ""),
            ])
            write_section("Plan Vivienda", [
                ("Terreno Propio", func.terreno_propio or ""),
                ("Ubicacion Terreno", func.ubicacion_terreno or ""),
                ("Condicion Vivienda", func.condicion_vivienda or ""),
                ("Necesidad Vivienda", func.necesidad_vivienda or ""),
                ("Organismo Publico", func.organismo_publico or ""),
                ("Organismo Privado", func.organismo_privado or ""),
                ("Gestion Organismo", func.gestion_organismo_oficial or ""),
                ("Fecha Gestion", func.fecha_gestion or ""),
            ])
            write_section("Estado Vivienda", [
                ("Tenencia Tierra", func.tenencia_tierra or ""),
                ("Tiempo Ocupacion", func.tiempo_ocupacion or ""),
                ("Ambiente", func.ambiente_vivienda or ""),
                ("Servicios", func.servicio_vivienda_disponible or ""),
                ("Materiales", func.materiales_vivienda or ""),
                ("Serv. Comunidad", func.servicio_comunidad or ""),
            ])
            if func.grupo_familiar:
                for i, fam in enumerate(func.grupo_familiar):
                    write_section(f"Familiar {i+1}", [
                        ("Nombre", f"{fam.nombre or ''} {fam.apellido or ''}"),
                        ("Parentesco", fam.parentesco or ""),
                        ("Edad", fam.edad or ""),
                        ("Genero", fam.genero or ""),
                        ("Estado Civil", fam.estado_civil or ""),
                        ("Nivel Educacion", fam.nivel_educacion or ""),
                        ("Profesion", fam.profesion_oficio or ""),
                        ("Lugar Trabajo", fam.lugar_trabajo or ""),
                        ("Ingreso Mensual", fam.ingreso_mensual or ""),
                        ("Observacion", fam.observacion or ""),
                    ])
            try:
                pdf.output("tmp_ficha.pdf")
                subprocess.Popen(["xdg-open", "tmp_ficha.pdf"] if platform.system() == "Linux" else ["start", "tmp_ficha.pdf"], shell=(platform.system() == "Windows"))
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo generar el PDF:\n{e}")

        def guardar_txt():
            lines = [f"FICHA DE FUNCIONARIO", "="*40]
            lines.append(f"\nDATOS PERSONALES")
            lines.append(f"Cedula: {func.cedula}")
            lines.append(f"Nombre: {func.nombre} {func.apellido}")
            lines.append(f"Fecha Nacimiento: {func.fecha_nacimiento}")
            lines.append(f"Edad: {func.edad}")
            lines.append(f"Estado Civil: {func.estado_civil}")
            lines.append(f"Telefono: {func.telefono}")
            lines.append(f"Peso: {func.peso or '-'}")
            lines.append(f"Altura: {func.altura or '-'}")
            lines.append(f"Direccion: {func.residencia or '-'}")
            lines.append(f"\nDATOS LABORALES")
            lines.append(f"Jerarquia: {func.jerarquia or '-'}")
            lines.append(f"Lugar Servicio: {func.lugar_presta_servicio or '-'}")
            lines.append(f"Tiempo Servicio: {func.tiempo_servicio or '-'}")
            lines.append(f"Salario Mensual: {func.salario_mensual or '-'}")
            lines.append(f"\nPLAN VIVIENDA")
            lines.append(f"Terreno Propio: {func.terreno_propio or '-'}")
            lines.append(f"Ubicacion Terreno: {func.ubicacion_terreno or '-'}")
            lines.append(f"Condicion: {func.condicion_vivienda or '-'}")
            lines.append(f"Necesidad Vivienda: {func.necesidad_vivienda or '-'}")
            lines.append(f"Organismo Publico: {func.organismo_publico or '-'}")
            lines.append(f"Organismo Privado: {func.organismo_privado or '-'}")
            lines.append(f"Gestion Organismo: {func.gestion_organismo_oficial or '-'}")
            lines.append(f"Fecha Gestion: {func.fecha_gestion or '-'}")
            lines.append(f"\nESTADO VIVIENDA")
            lines.append(f"Tenencia Tierra: {func.tenencia_tierra or '-'}")
            lines.append(f"Tiempo Ocupacion: {func.tiempo_ocupacion or '-'}")
            lines.append(f"Ambiente: {func.ambiente_vivienda or '-'}")
            lines.append(f"Servicios: {func.servicio_vivienda_disponible or '-'}")
            lines.append(f"Materiales: {func.materiales_vivienda or '-'}")
            lines.append(f"Serv. Comunidad: {func.servicio_comunidad or '-'}")
            if func.grupo_familiar:
                lines.append(f"\nGRUPO FAMILIAR")
                for i, fam in enumerate(func.grupo_familiar):
                    lines.append(f"\nFamiliar {i+1}")
                    lines.append(f"  Nombre: {fam.nombre or ''} {fam.apellido or ''}")
                    lines.append(f"  Parentesco: {fam.parentesco or '-'}")
                    lines.append(f"  Edad: {fam.edad or '-'}")
                    lines.append(f"  Genero: {fam.genero or '-'}")
                    lines.append(f"  Estado Civil: {fam.estado_civil or '-'}")
                    lines.append(f"  Nivel Educacion: {fam.nivel_educacion or '-'}")
                    lines.append(f"  Profesion: {fam.profesion_oficio or '-'}")
                    lines.append(f"  Lugar Trabajo: {fam.lugar_trabajo or '-'}")
                    lines.append(f"  Ingreso Mensual: {fam.ingreso_mensual or '-'}")
            try:
                with open("ficha_funcionario.txt", "w", encoding="utf-8") as f:
                    f.write("\n".join(lines))
                messagebox.showinfo("Exportado", "Ficha guardada como ficha_funcionario.txt")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo:\n{e}")

        def imprimir():
            import platform, subprocess, tempfile, os
            lines = []
            lines.append(f"FICHA DE FUNCIONARIO")
            lines.append("="*40)
            lines.append(f"Cedula: {func.cedula} | Nombre: {func.nombre} {func.apellido}")
            lines.append(f"Fecha Nac: {func.fecha_nacimiento} | Edad: {func.edad}")
            lines.append(f"Estado Civil: {func.estado_civil} | Peso: {func.peso or '-'} | Altura: {func.altura or '-'} | Dir: {func.residencia or '-'}")
            lines.append(f"Tel: {func.telefono}")
            lines.append(f"")
            lines.append(f"LABORALES: Jer:{func.jerarquia or '-'} Lugar:{func.lugar_presta_servicio or '-'}")
            lines.append(f"Tiempo:{func.tiempo_servicio or '-'} Salario:{func.salario_mensual or '-'} FecGestion:{func.fecha_gestion or '-'}")
            lines.append(f"")
            lines.append(f"VIVIENDA: Terreno:{func.terreno_propio or '-'} Ubi:{func.ubicacion_terreno or '-'}")
            lines.append(f"Condicion:{func.condicion_vivienda or '-'} Nec:{func.necesidad_vivienda or '-'}")
            lines.append(f"OrgPub:{func.organismo_publico or '-'} OrgPriv:{func.organismo_privado or '-'}")
            lines.append(f"Gestion:{func.gestion_organismo_oficial or '-'} FecGestion:{func.fecha_gestion or '-'}")
            lines.append(f"Tenencia:{func.tenencia_tierra or '-'} TiempoOcup:{func.tiempo_ocupacion or '-'}")
            lines.append(f"Servicios:{func.servicio_vivienda_disponible or '-'}")
            lines.append(f"Materiales:{func.materiales_vivienda or '-'}")
            lines.append(f"Serv.Com:{func.servicio_comunidad or '-'}")
            if func.grupo_familiar:
                for i, fam in enumerate(func.grupo_familiar):
                    lines.append(f"Fam{i+1}: {fam.nombre or ''} {fam.apellido or ''} ({fam.parentesco or '-'}) Edad:{fam.edad or '-'} Gen:{fam.genero or '-'} EstCiv:{fam.estado_civil or '-'} NivelEd:{fam.nivel_educacion or '-'} Prof:{fam.profesion_oficio or '-'} L Trab:{fam.lugar_trabajo or '-'} Ing:{fam.ingreso_mensual or '-'}")
            content = "\n".join(lines)
            try:
                tmp = tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False, encoding="utf-8")
                tmp.write(content)
                tmp.close()
                if platform.system() == "Windows":
                    subprocess.Popen(["notepad", "/p", tmp.name])
                else:
                    subprocess.Popen(["lpr", tmp.name])
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo imprimir:\n{e}")

        menu = Menu(self.root, tearoff=0, font=("Segoe UI", 10), bg=self.bg_card, fg=self.text, activebackground=self.primary, activeforeground="white")
        menu.add_command(label="Imprimir (Sistema)", command=imprimir)
        menu.add_command(label="Exportar PDF", command=exportar_pdf)
        menu.add_command(label="Guardar TXT", command=guardar_txt)
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def desactivar_funcionario(self, cedula=None, frame_actual=None):
        if cedula is None:
            sel = self.tree.selection()
            if not sel: return
            cedula = sel[0]
        if messagebox.askyesno("Confirmar", "Desea desactivar este funcionario? (quedara oculto pero sus datos se conservan)", parent=self.root):
            eliminar_funcionario(cedula, usuario=self.usuario_actual)
            if frame_actual: frame_actual.destroy()
            self.cargar_en_tabla()

    def restaurar_funcionario(self, cedula=None, frame_actual=None):
        if cedula is None:
            sel = self.tree.selection()
            if not sel: return
            cedula = sel[0]
        if messagebox.askyesno("Confirmar", "Desea restaurar este funcionario?", parent=self.root):
            restaurar_funcionario(cedula, usuario=self.usuario_actual)
            if frame_actual: frame_actual.destroy()
            self.cargar_en_tabla()

    def mostrar_registrar_usuario(self, funcionario=None):
        self.editando_cedula = funcionario.cedula if funcionario else None
        self.limpiar_panel_principal()
        self.pagina_principal = Frame(self.panel_principal, bg=self.bg)
        self.pagina_principal.pack(fill=BOTH, expand=True)

        self.mostrar_panel_acciones()

        content = Frame(self.pagina_principal, bg=self.bg)
        content.pack(side=LEFT, fill=BOTH, expand=True, padx=20, pady=20)

        if funcionario:
            titulo = f"Editar Funcionario: {funcionario.nombre} {funcionario.apellido}"
            subtitulo = "Modifique los datos del funcionario"
        else:
            titulo = "Registrar Funcionario"
            subtitulo = "Complete todos los datos del funcionario"

        Label(content, text=titulo, font=("Segoe UI", 18, "bold"),
              bg=self.bg, fg=self.text).pack(anchor=W, pady=(0, 5))
        Label(content, text=subtitulo, font=("Segoe UI", 10),
              bg=self.bg, fg=self.text_sec).pack(anchor=W, pady=(0, 15))

        notebook = ttk.Notebook(content)
        notebook.pack(fill=BOTH, expand=True)

        self.tab_personales = Frame(notebook, bg=self.bg_card)
        self.tab_laborales = Frame(notebook, bg=self.bg_card)
        self.tab_vivienda_plan = Frame(notebook, bg=self.bg_card)
        self.tab_vivienda_estado = Frame(notebook, bg=self.bg_card)
        self.tab_familiares = Frame(notebook, bg=self.bg_card)

        notebook.add(self.tab_personales, text="Datos Personales")
        notebook.add(self.tab_laborales, text="Datos Laborales")
        notebook.add(self.tab_vivienda_plan, text="Plan Vivienda")
        notebook.add(self.tab_vivienda_estado, text="Estado Vivienda")
        notebook.add(self.tab_familiares, text="Grupo Familiar")

        self._crear_tab_personales()
        self._crear_tab_laborales()
        self._crear_tab_plan_vivienda()
        self._crear_tab_estado_vivienda()
        self._crear_tab_familiares()

        footer = Frame(content, bg=self.bg)
        footer.pack(fill=X, pady=(12, 0))

        Button(footer, text="Limpiar Campos", font=("Segoe UI", 10), bg=self.warning, fg=self.text,
               relief="flat", borderwidth=0, cursor="hand2", command=self.limpiar_campos).pack(side=LEFT, padx=5, ipady=5)
        Button(footer, text="Guardar Funcionario", font=("Segoe UI", 10, "bold"), bg=self.success, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=self.guardar_funcionario).pack(side=RIGHT, padx=5, ipady=5)

    def _calcular_edad(self, event=None):
        try:
            val = self.input_fecha_nacimiento.get()
            if not val or "/" not in val:
                return
            d, m, a = val.split("/")
            from datetime import date
            hoy = date.today()
            nac = date(int(a), int(m), int(d))
            edad = hoy.year - nac.year - ((hoy.month, hoy.day) < (nac.month, nac.day))
            self.input_edad.config(state=NORMAL)
            self.input_edad.delete(0, END)
            self.input_edad.insert(0, str(edad))
            self.input_edad.config(state="readonly")
        except:
            pass

    def _crear_date_picker(self, parent, on_change=None):
        frame = Frame(parent, bg=self.bg_card)

        meses = [f"{i:02d}" for i in range(1, 13)]
        dias = [f"{i:02d}" for i in range(1, 32)]
        anios = [str(i) for i in range(1950, 2031)]

        dia_cb = ttk.Combobox(frame, values=dias, width=4, font=("Segoe UI", 11), state="readonly")
        dia_cb.pack(side=LEFT, padx=(0, 2))
        Label(frame, text="/", font=("Segoe UI", 12, "bold"), bg=self.bg_card, fg=self.text_sec).pack(side=LEFT)
        mes_cb = ttk.Combobox(frame, values=meses, width=4, font=("Segoe UI", 11), state="readonly")
        mes_cb.pack(side=LEFT, padx=2)
        Label(frame, text="/", font=("Segoe UI", 12, "bold"), bg=self.bg_card, fg=self.text_sec).pack(side=LEFT)
        anio_cb = ttk.Combobox(frame, values=anios, width=6, font=("Segoe UI", 11), state="readonly")
        anio_cb.pack(side=LEFT, padx=2)

        if on_change:
            for cb in (dia_cb, mes_cb, anio_cb):
                cb.bind("<<ComboboxSelected>>", on_change)

        def get_val():
            d = dia_cb.get()
            m = mes_cb.get()
            a = anio_cb.get()
            if d and m and a:
                return f"{d}/{m}/{a}"
            return ""

        def set_val(val):
            if not val or "/" not in val:
                return
            parts = val.split("/")
            if len(parts) == 3:
                d, m, a = parts
                if d in dias: dia_cb.set(d)
                if m in meses: mes_cb.set(m)
                if a in anios: anio_cb.set(a)

        frame.get = get_val
        frame.delete = lambda *a: None
        frame.insert = lambda idx, val: set_val(val)
        frame.config = lambda **kw: None

        return frame

    def _crear_tab_personales(self):
        p = self.tab_personales
        for i in range(6): p.grid_rowconfigure(i, pad=8)
        for i in range(6): p.grid_columnconfigure(i, weight=1, pad=15)

        Label(p, text="Datos Personales", font=("Segoe UI", 13, "bold"),
              bg=self.bg_card, fg=self.primary).grid(row=0, column=0, columnspan=6, sticky=W, pady=(15, 10))

        def campo_fila(fila, textos, colspan=1):
            widgets = []
            for j, (label, col) in enumerate(zip(textos, range(0, 6, 2))):
                c = col if colspan == 1 else j * 2
                Label(p, text=label, font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).grid(row=fila, column=c, sticky=W, pady=(6, 2))
                e = Entry(p, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                          highlightbackground=self.border, highlightthickness=1)
                e.grid(row=fila + 1, column=c, columnspan=colspan, sticky=EW, padx=(0, 10), ipady=3)
                widgets.append(e)
            return widgets

        self.input_cedula, self.input_nombre, self.input_apellido = campo_fila(1, ["Cedula:", "Nombre:", "Apellido:"], colspan=2)

        Label(p, text="Fecha Nacimiento:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).grid(row=3, column=0, sticky=W, pady=(6, 2))
        self.input_fecha_nacimiento = self._crear_date_picker(p, on_change=self._calcular_edad)
        self.input_fecha_nacimiento.grid(row=4, column=0, columnspan=2, sticky=EW, padx=(0, 10))

        Label(p, text="Edad:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).grid(row=3, column=2, sticky=W, pady=(6, 2))
        self.input_edad = Entry(p, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                                highlightbackground=self.border, highlightthickness=1,
                                state="readonly", readonlybackground=self.bg_card)
        self.input_edad.grid(row=4, column=2, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)

        Label(p, text="Telefono:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).grid(row=3, column=4, sticky=W, pady=(6, 2))
        self.input_telefono = Entry(p, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                                    highlightbackground=self.border, highlightthickness=1)
        self.input_telefono.grid(row=4, column=4, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)
        self.input_peso, self.input_altura, self.input_estado_civil = campo_fila(5, ["Peso (kg):", "Altura (m):", "Estado Civil:"], colspan=2)
        self.input_residencia, = campo_fila(7, ["Direccion:"], colspan=6)

    def _crear_tab_laborales(self):
        p = self.tab_laborales
        for i in range(4): p.grid_rowconfigure(i, pad=8)
        for i in range(4): p.grid_columnconfigure(i, weight=1, pad=15)

        Label(p, text="Datos Laborales", font=("Segoe UI", 13, "bold"),
              bg=self.bg_card, fg=self.primary).grid(row=0, column=0, columnspan=4, sticky=W, pady=(15, 10))

        Label(p, text="Jerarquia:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).grid(row=1, column=0, sticky=W, pady=(6, 2))
        self.input_jerarquia = Entry(p, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                                     highlightbackground=self.border, highlightthickness=1)
        self.input_jerarquia.grid(row=2, column=0, sticky=EW, padx=(0, 15), ipady=3)

        Label(p, text="Tiempo Servicio:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).grid(row=1, column=1, sticky=W, pady=(6, 2))
        self.input_tiempo_servicio = Entry(p, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                                           highlightbackground=self.border, highlightthickness=1)
        self.input_tiempo_servicio.grid(row=2, column=1, sticky=EW, padx=(0, 15), ipady=3)

        Label(p, text="Lugar Servicio:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).grid(row=1, column=2, sticky=W, pady=(6, 2))
        self.input_lugar_servicio = Entry(p, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                                          highlightbackground=self.border, highlightthickness=1)
        self.input_lugar_servicio.grid(row=2, column=2, sticky=EW, padx=(0, 15), ipady=3)

        Label(p, text="Ingreso Mensual:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text).grid(row=1, column=3, sticky=W, pady=(6, 2))
        self.input_ingreso_mensual = Entry(p, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                                           highlightbackground=self.border, highlightthickness=1)
        self.input_ingreso_mensual.grid(row=2, column=3, sticky=EW, padx=(0, 15), ipady=3)

    def _crear_tab_plan_vivienda(self):
        p = self.tab_vivienda_plan

        self.posee_terreno = StringVar(value="NO")
        self.posee_vivienda = StringVar(value="NO")
        self.necesidad_habiacion = StringVar(value="Vivienda")
        self.gestion_organismo = StringVar(value="NO")
        self.organismo_publico = StringVar(value="Otra")
        self.organismo_privado = StringVar(value="Otra")

        canvas = Canvas(p, bg=self.bg_card, highlightthickness=0)
        scroll = ttk.Scrollbar(p, orient=VERTICAL, command=canvas.yview)
        scroll_frame = Frame(canvas, bg=self.bg_card)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win_id = canvas.create_window((0, 0), window=scroll_frame, anchor=NW)
        def _resize_canvas(event):
            canvas.itemconfig(win_id, width=event.width)
        canvas.bind("<Configure>", _resize_canvas)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        def _on_mousewheel_pv(event):
            if event.num == 4: canvas.yview_scroll(-3, "units")
            elif event.num == 5: canvas.yview_scroll(3, "units")
            else: canvas.yview_scroll(-1 * (event.delta // 120), "units")
        for w in (canvas, scroll_frame):
            w.bind("<Button-4>", _on_mousewheel_pv)
            w.bind("<Button-5>", _on_mousewheel_pv)
            w.bind("<MouseWheel>", _on_mousewheel_pv)

        self._plan_entries = {}
        def entry_row(parent, label):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=3)
            Label(r, text=label, font=("Segoe UI", 10), bg=self.bg_card, fg=self.text, width=20, anchor=W).pack(side=LEFT)
            e = Entry(r, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                      highlightbackground=self.border, highlightthickness=1)
            e.pack(side=LEFT, ipady=3, fill=X, expand=True)
            return e

        def seccion(parent, titulo):
            f = LabelFrame(parent, text=titulo, font=("Segoe UI", 10, "bold"),
                           bg=self.bg_card, fg=self.text, relief="groove", borderwidth=1, padx=10, pady=8)
            f.pack(fill=X, padx=15, pady=6)
            return f

        def radio_group(parent, label, var, options):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=3)
            Label(r, text=label, font=("Segoe UI", 10), bg=self.bg_card, fg=self.text, width=20, anchor=W).pack(side=LEFT)
            for val in options:
                Radiobutton(r, text=val, variable=var, value=val, font=("Segoe UI", 9),
                            bg=self.bg_card, fg=self.text, activebackground=self.bg_card,
                            activeforeground=self.primary, selectcolor=self.bg_card).pack(side=LEFT, padx=3)

        sf = scroll_frame

        f = seccion(sf, "Terreno")
        radio_group(f, "Terreno Propio:", self.posee_terreno, ["SI", "NO"])
        self._plan_entries["ubicacion_terreno"] = entry_row(f, "Ubicacion:")

        f = seccion(sf, "Vivienda")
        radio_group(f, "Posee Vivienda:", self.posee_vivienda, ["SI", "NO"])
        self._plan_entries["condicion_vivienda"] = entry_row(f, "Condicion:")

        f = seccion(sf, "Necesidad Habitacional")
        radio_group(f, "Necesidad:", self.necesidad_habiacion, ["Vivienda", "Construccion", "Sustitucion", "Mejoramiento"])

        f = seccion(sf, "Gestion Organismo Oficial")
        radio_group(f, "Gestion:", self.gestion_organismo, ["SI", "NO"])
        radio_group(f, "Organismo Publico:", self.organismo_publico, ["Gobernacion", "INAVI", "Malariologia", "Otra"])
        radio_group(f, "Organismo Privado:", self.organismo_privado, ["Entidad Bancaria", "Empresa Promotora", "Otra"])

        f = seccion(sf, "Fecha")
        r = Frame(f, bg=self.bg_card)
        r.pack(fill=X, pady=3)
        Label(r, text="Fecha Gestion:", font=("Segoe UI", 10), bg=self.bg_card, fg=self.text, width=20, anchor=W).pack(side=LEFT)
        self._plan_entries["fecha_gestion"] = self._crear_date_picker(r)
        self._plan_entries["fecha_gestion"].pack(side=LEFT, ipady=3, fill=X, expand=True)

        self.input_ubicacion_terreno = self._plan_entries["ubicacion_terreno"]
        self.input_condicion_vivienda = self._plan_entries["condicion_vivienda"]
        self.input_fecha_gestion = self._plan_entries["fecha_gestion"]

    def _crear_tab_estado_vivienda(self):
        p = self.tab_vivienda_estado
        self.tenencia_tierra = StringVar(value="Otra")

        canvas = Canvas(p, bg=self.bg_card, highlightthickness=0)
        scroll = ttk.Scrollbar(p, orient=VERTICAL, command=canvas.yview)
        scroll_frame = Frame(canvas, bg=self.bg_card)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win_id = canvas.create_window((0, 0), window=scroll_frame, anchor=NW)
        def _resize_canvas(event):
            canvas.itemconfig(win_id, width=event.width)
        canvas.bind("<Configure>", _resize_canvas)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        def _on_mousewheel_ev(event):
            if event.num == 4: canvas.yview_scroll(-3, "units")
            elif event.num == 5: canvas.yview_scroll(3, "units")
            else: canvas.yview_scroll(-1 * (event.delta // 120), "units")
        for w in (canvas, scroll_frame):
            w.bind("<Button-4>", _on_mousewheel_ev)
            w.bind("<Button-5>", _on_mousewheel_ev)
            w.bind("<MouseWheel>", _on_mousewheel_ev)

        self._estado_entries = {}

        def entry_row(parent, label):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=2)
            Label(r, text=label, font=("Segoe UI", 10), bg=self.bg_card, fg=self.text, width=22, anchor=W).pack(side=LEFT)
            e = Entry(r, font=("Segoe UI", 11), relief="solid", borderwidth=1,
                      highlightbackground=self.border, highlightthickness=1)
            e.pack(side=LEFT, ipady=3, fill=X, expand=True)
            return e

        def seccion(titulo):
            f = LabelFrame(sf, text=titulo, font=("Segoe UI", 10, "bold"),
                           bg=self.bg_card, fg=self.text, relief="groove", borderwidth=1, padx=10, pady=8)
            f.pack(fill=X, padx=15, pady=6)
            return f

        def radio_group(parent, label, var, options):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=2)
            Label(r, text=label, font=("Segoe UI", 10), bg=self.bg_card, fg=self.text, width=22, anchor=W).pack(side=LEFT)
            for val in options:
                Radiobutton(r, text=val, variable=var, value=val, font=("Segoe UI", 9),
                            bg=self.bg_card, fg=self.text, activebackground=self.bg_card,
                            activeforeground=self.primary, selectcolor=self.bg_card).pack(side=LEFT, padx=2)

        sf = scroll_frame
        Label(sf, text="Estado de la Vivienda", font=("Segoe UI", 13, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, pady=(15, 15), padx=15)

        f = seccion("Tenencia de Tierra")
        radio_group(f, "Tipo:", self.tenencia_tierra, ["Propia", "Proceso Pago", "Cedida", "Invadida", "Otra"])
        self._estado_entries["tenencia_tierra_otra"] = entry_row(f, "Especifique:")

        f = seccion("Ocupacion")
        self._estado_entries["tiempo_ocupacion"] = entry_row(f, "Tiempo Ocupacion:")

        f = seccion("Ambientes")
        self._estado_entries["num_sala"] = entry_row(f, "Sala:")
        self._estado_entries["num_sala_comedor"] = entry_row(f, "Sala-Comedor:")
        self._estado_entries["num_cocina"] = entry_row(f, "Cocina:")
        self._estado_entries["num_cocina_comedor"] = entry_row(f, "Cocina-Comedor:")
        self._estado_entries["num_bano"] = entry_row(f, "Bano:")
        self._estado_entries["num_dormitorio"] = entry_row(f, "Dormitorios:")
        self._estado_entries["otros"] = entry_row(f, "Otros:")
        self._estado_entries["especificacion"] = entry_row(f, "Especifique:")

        self._serv_vars = {}
        f = seccion("Servicios de la Vivienda")
        def serv_check(label, key):
            r = Frame(f, bg=self.bg_card)
            r.pack(fill=X, pady=2)
            var = StringVar(value="NO")
            self._serv_vars[key] = var
            Label(r, text=label, font=("Segoe UI", 10), bg=self.bg_card, fg=self.text, width=22, anchor=W).pack(side=LEFT)
            for val in ("SI", "NO"):
                Radiobutton(r, text=val, variable=var, value=val, font=("Segoe UI", 9),
                            bg=self.bg_card, fg=self.text, activebackground=self.bg_card,
                            activeforeground=self.primary, selectcolor=self.bg_card).pack(side=LEFT, padx=2)

        serv_check("Agua Potable:", "serv_agua")
        serv_check("Red Cloaca:", "serv_cloaca")
        serv_check("Alumbrado:", "serv_alumbrado")
        serv_check("Aseo Publico:", "serv_aseo")
        serv_check("Telefono:", "serv_telefono")
        serv_check("Ninguno:", "serv_ninguno")
        serv_check("Otros:", "serv_otro")
        self._estado_entries["serv_especifico"] = entry_row(f, "Especifique:")

        self._mat_pared_vars = {}
        self._mat_techo_vars = {}
        self._mat_piso_vars = {}
        self._mat_serv_com_vars = {}

        def check_row(label, options, store):
            r = Frame(sf, bg=self.bg_card)
            r.pack(fill=X, pady=3, padx=15)
            Label(r, text=label, font=("Segoe UI", 10, "bold"), bg=self.bg_card, fg=self.text, width=22, anchor=W).pack(side=LEFT)
            for val in options:
                var = IntVar()
                Checkbutton(r, text=val, variable=var, font=("Segoe UI", 9), bg=self.bg_card, fg=self.text,
                            activebackground=self.bg_card, activeforeground=self.primary,
                            selectcolor=self.bg_card).pack(side=LEFT, padx=4)
                store[val] = var

        check_row("Pared:", ["Bloque", "Madera", "Zinc", "Bahareque", "Carton"], self._mat_pared_vars)
        check_row("Techo:", ["Platabanda", "Asbesto", "Madera", "Zinc", "Otro"], self._mat_techo_vars)
        check_row("Piso:", ["Cemento", "Ceramica", "Madera", "Vinil", "Tierra", "Otro"], self._mat_piso_vars)
        check_row("Serv. Comunidad:", ["Agua potable", "Red cloacal", "Alumbrado", "Aseo Urbano", "Telefono", "Transporte", "Ninguno"], self._mat_serv_com_vars)

        self.input_tenencia_tierra_otra = self._estado_entries["tenencia_tierra_otra"]
        self.input_tiempo_ocupacion = self._estado_entries["tiempo_ocupacion"]
        self.input_num_sala = self._estado_entries["num_sala"]
        self.input_num_sala_comedor = self._estado_entries["num_sala_comedor"]
        self.input_num_cocina = self._estado_entries["num_cocina"]
        self.input_num_cocina_comedor = self._estado_entries["num_cocina_comedor"]
        self.input_num_bano = self._estado_entries["num_bano"]
        self.input_num_dormitorio = self._estado_entries["num_dormitorio"]
        self.input_otros = self._estado_entries["otros"]
        self.input_especificacion = self._estado_entries["especificacion"]

    def _crear_tab_familiares(self):
        p = self.tab_familiares
        self.familiares_panels = []

        Label(p, text="Grupo Familiar", font=("Segoe UI", 13, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, pady=(15, 5), padx=15)
        Label(p, text="Agregue los familiares del funcionario", font=("Segoe UI", 10),
              bg=self.bg_card, fg=self.text_sec).pack(anchor=W, padx=15, pady=(0, 10))

        # Scrollable container for family member cards
        canvas_container = Frame(p, bg=self.bg_card)
        canvas_container.pack(fill=BOTH, expand=True, padx=15)

        canvas = Canvas(canvas_container, bg=self.bg_card, highlightthickness=0)
        scroll = ttk.Scrollbar(canvas_container, orient=VERTICAL, command=canvas.yview)
        self.familiares_container = Frame(canvas, bg=self.bg_card)
        self.familiares_container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win_id = canvas.create_window((0, 0), window=self.familiares_container, anchor=NW)
        def _resize_fam(event):
            canvas.itemconfig(win_id, width=event.width)
        canvas.bind("<Configure>", _resize_fam)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        def _on_mousewheel_fam(event):
            if event.num == 4: canvas.yview_scroll(-3, "units")
            elif event.num == 5: canvas.yview_scroll(3, "units")
            else: canvas.yview_scroll(-1 * (event.delta // 120), "units")
        for w in (canvas, self.familiares_container):
            w.bind("<Button-4>", _on_mousewheel_fam)
            w.bind("<Button-5>", _on_mousewheel_fam)
            w.bind("<MouseWheel>", _on_mousewheel_fam)

        # Empty state
        self.empty_label = Label(self.familiares_container, text="No hay familiares agregados. Presione 'Agregar Familiar'.",
                                  font=("Segoe UI", 10), bg=self.bg_card, fg=self.text_sec)
        self.empty_label.pack(pady=30)

        footer_fam = Frame(p, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        footer_fam.pack(fill=X, padx=15, pady=(10, 15))

        Button(footer_fam, text="+ Agregar Familiar", font=("Segoe UI", 10, "bold"), bg=self.primary, fg="white",
               activebackground=self.primary_hover, activeforeground="white", relief="flat", borderwidth=0,
               cursor="hand2", command=self.crear_nuevo_panel_familiar).pack(side=LEFT, padx=10, pady=8, ipady=5)

    def crear_nuevo_panel_familiar(self):
        self.empty_label.pack_forget()
        idx = len(self.familiares_panels)

        card = Frame(self.familiares_container, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        card.pack(fill=X, pady=5)

        header = Frame(card, bg=self.primary)
        header.pack(fill=X)
        Label(header, text=f"Familiar #{idx + 1}", font=("Segoe UI", 10, "bold"),
              bg=self.primary, fg="white", padx=10).pack(side=LEFT, pady=4)
        Button(header, text="X", font=("Segoe UI", 9, "bold"), bg=self.danger, fg="white",
               activebackground="#c82333", relief="flat", borderwidth=0, cursor="hand2",
               command=lambda i=idx: self.borrar_panel_familiar(i)).pack(side=RIGHT, padx=5, pady=2)

        body = Frame(card, bg=self.bg_card)
        body.pack(fill=X, padx=10, pady=8)

        inputs = {}

        def make_campo(fila, label, col, colspan=1):
            Label(body, text=label, font=("Segoe UI", 9), bg=self.bg_card, fg=self.text).grid(row=fila, column=col, sticky=W, padx=(0, 2))
            e = Entry(body, font=("Segoe UI", 10), relief="solid", borderwidth=1,
                      highlightbackground=self.border, highlightthickness=1)
            e.grid(row=fila + 1, column=col, columnspan=colspan, sticky=EW, padx=(0, 8), ipady=2)
            return e

        inputs["nombre"] = make_campo(0, "Nombre:", 0)
        inputs["apellido"] = make_campo(0, "Apellido:", 2)
        inputs["parentesco"] = make_campo(0, "Parentesco:", 4)
        inputs["edad"] = make_campo(2, "Edad:", 0)
        inputs["genero"] = make_campo(2, "Genero:", 2)
        inputs["estado_civil"] = make_campo(2, "Estado Civil:", 4)
        inputs["nivel_educacion"] = make_campo(4, "Nivel Educacion:", 0)
        inputs["profesion"] = make_campo(4, "Profesion:", 2)
        inputs["lugar_trabajo"] = make_campo(4, "Lugar Trabajo:", 4)
        inputs["ingreso_mensual"] = make_campo(6, "Ingreso Mensual:", 0)
        inputs["observacion"] = make_campo(6, "Observacion:", 2, colspan=3)

        for i in range(8):
            body.grid_rowconfigure(i, pad=2)
        for i in range(6):
            body.grid_columnconfigure(i, weight=1)

        self.familiares_panels.append((card, inputs))

    def borrar_panel_familiar(self, idx):
        if 0 <= idx < len(self.familiares_panels):
            panel, _ = self.familiares_panels[idx]
            panel.destroy()
            self.familiares_panels.pop(idx)
            if not self.familiares_panels:
                self.empty_label = Label(self.familiares_container, text="No hay familiares agregados. Presione 'Agregar Familiar'.",
                                          font=("Segoe UI", 10), bg=self.bg_card, fg=self.text_sec)
                self.empty_label.pack(pady=30)

    def guardar_funcionario(self):
        cedula = self.input_cedula.get().strip()
        if not cedula:
            messagebox.showwarning("Error", "La cedula es obligatoria", parent=self.root)
            return

        if not self.editando_cedula:
            existentes = cargar_funcionarios(incluir_inactivos=True)
            for ex in existentes:
                if ex.cedula == cedula:
                    messagebox.showwarning("Error", f"La cedula {cedula} ya existe en el sistema", parent=self.root)
                    return

        f = Funcionario(
            cedula, self.input_nombre.get().strip(), self.input_apellido.get().strip(),
            self.input_fecha_nacimiento.get().strip(), self.input_edad.get().strip(),
            self.input_telefono.get().strip(), self.input_peso.get().strip(),
            self.input_altura.get().strip(), self.input_estado_civil.get().strip(),
            self.input_residencia.get().strip()
        )

        f.datos_laborales(
            self.input_jerarquia.get().strip(), self.input_lugar_servicio.get().strip(),
            self.input_tiempo_servicio.get().strip(), self.input_ingreso_mensual.get().strip()
        )

        f.plan_vivienda(
            self.posee_terreno.get(), self.input_ubicacion_terreno.get().strip(),
            self.input_condicion_vivienda.get().strip(), self.necesidad_habiacion.get(),
            self.organismo_publico.get(), self.organismo_privado.get(),
            self.gestion_organismo.get(), self.input_fecha_gestion.get().strip()
        )

        ambiente = (f"Sala:{self.input_num_sala.get()}, Sala-Comedor:{self.input_num_sala_comedor.get()}, "
                    f"Cocina:{self.input_num_cocina.get()}, Cocina-Comedor:{self.input_num_cocina_comedor.get()}, "
                    f"Bano:{self.input_num_bano.get()}, Dormitorios:{self.input_num_dormitorio.get()}, "
                    f"Otros:{self.input_otros.get()}, Especifique:{self.input_especificacion.get()}")

        servicios = (f"Agua:{self._serv_vars['serv_agua'].get()}, Cloaca:{self._serv_vars['serv_cloaca'].get()}, "
                     f"Alumbrado:{self._serv_vars['serv_alumbrado'].get()}, Aseo:{self._serv_vars['serv_aseo'].get()}, "
                     f"Telefono:{self._serv_vars['serv_telefono'].get()}, Ninguno:{self._serv_vars['serv_ninguno'].get()}, "
                     f"Otros:{self._serv_vars['serv_otro'].get()}, Especifique:{self._estado_entries['serv_especifico'].get()}")

        def _checked(store):
            return ", ".join(k for k, v in store.items() if v.get())

        materiales = f"Pared: {_checked(self._mat_pared_vars)} | Techo: {_checked(self._mat_techo_vars)} | Piso: {_checked(self._mat_piso_vars)}"
        serv_comunidad = _checked(self._mat_serv_com_vars)

        f.estado_vivienda(self.tenencia_tierra.get(), ambiente, self.input_tiempo_ocupacion.get().strip(),
                          servicios, materiales, serv_comunidad)

        for panel, inputs in self.familiares_panels:
            fam = Familiar(
                inputs["nombre"].get().strip(), inputs["apellido"].get().strip(),
                inputs["parentesco"].get().strip(), inputs["edad"].get().strip(),
                inputs["genero"].get().strip(), inputs["estado_civil"].get().strip(),
                inputs["nivel_educacion"].get().strip(), inputs["profesion"].get().strip(),
                inputs["lugar_trabajo"].get().strip(), inputs["ingreso_mensual"].get().strip(),
                inputs["observacion"].get().strip()
            )
            f.agregar_familiar(fam)

        funcs = cargar_funcionarios(incluir_inactivos=True)
        try:
            if self.editando_cedula:
                for i, func in enumerate(funcs):
                    if func.cedula == self.editando_cedula:
                        funcs[i] = f
                        break
                accion = "MODIFICAR"
            else:
                funcs.append(f)
                accion = "CREAR"
            guardar_funcionarios(funcs)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el funcionario:\n{e}", parent=self.root)
            return

        try:
            registrar_auditoria(self.usuario_actual, accion,
                                f"Funcionario {f.nombre} {f.apellido} - Cedula {f.cedula}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar la auditoria:\n{e}", parent=self.root)
        self.editando_cedula = None
        messagebox.showinfo("Exito", "Funcionario guardado correctamente", parent=self.root)
        self.mostrar_pagina_principal()

    def limpiar_campos(self):
        self.mostrar_registrar_usuario()

    def editar_funcionario(self, cedula=None):
        if cedula is None:
            sel = self.tree.selection()
            if not sel: return
            cedula = sel[0]
        for f in self.funcionarios:
            if f.cedula == cedula:
                self._cargar_datos_en_formulario(f)
                return

    def _cargar_datos_en_formulario(self, f):
        self.mostrar_registrar_usuario(funcionario=f)

        self.input_cedula.config(state=NORMAL)
        self.input_cedula.delete(0, END)
        self.input_cedula.insert(0, f.cedula)
        self.input_cedula.config(state="readonly")

        self.input_nombre.delete(0, END); self.input_nombre.insert(0, f.nombre)
        self.input_apellido.delete(0, END); self.input_apellido.insert(0, f.apellido)
        self.input_fecha_nacimiento.delete(0, END); self.input_fecha_nacimiento.insert(0, f.fecha_nacimiento)
        self._calcular_edad()
        self.input_telefono.delete(0, END); self.input_telefono.insert(0, f.telefono)
        self.input_peso.delete(0, END); self.input_peso.insert(0, f.peso)
        self.input_altura.delete(0, END); self.input_altura.insert(0, f.altura)
        self.input_estado_civil.delete(0, END); self.input_estado_civil.insert(0, f.estado_civil)
        self.input_residencia.delete(0, END); self.input_residencia.insert(0, f.residencia)

        self.input_jerarquia.delete(0, END)
        self.input_jerarquia.insert(0, getattr(f, "jerarquia", ""))
        self.input_tiempo_servicio.delete(0, END)
        self.input_tiempo_servicio.insert(0, getattr(f, "tiempo_servicio", ""))
        self.input_lugar_servicio.delete(0, END)
        self.input_lugar_servicio.insert(0, getattr(f, "lugar_presta_servicio", ""))
        self.input_ingreso_mensual.delete(0, END)
        self.input_ingreso_mensual.insert(0, getattr(f, "salario_mensual", ""))

        if hasattr(f, "terreno_propio"):
            self.posee_terreno.set(f.terreno_propio if f.terreno_propio else "NO")
            self.necesidad_habiacion.set(f.necesidad_vivienda if f.necesidad_vivienda else "Vivienda")
            self.gestion_organismo.set(f.gestion_organismo_oficial if f.gestion_organismo_oficial else "NO")
            self.organismo_publico.set(f.organismo_publico if f.organismo_publico else "Otra")
            self.organismo_privado.set(f.organismo_privado if f.organismo_privado else "Otra")
            self._plan_entries["ubicacion_terreno"].delete(0, END)
            self._plan_entries["ubicacion_terreno"].insert(0, f.ubicacion_terreno)
            self._plan_entries["condicion_vivienda"].delete(0, END)
            self._plan_entries["condicion_vivienda"].insert(0, f.condicion_vivienda)
            self._plan_entries["fecha_gestion"].delete(0, END)
            self._plan_entries["fecha_gestion"].insert(0, f.fecha_gestion)

        if hasattr(f, "tenencia_tierra"):
            self.tenencia_tierra.set(f.tenencia_tierra if f.tenencia_tierra else "Otra")
            self._estado_entries["tiempo_ocupacion"].delete(0, END)
            self._estado_entries["tiempo_ocupacion"].insert(0, f.tiempo_ocupacion)
            if hasattr(f, "servicio_vivienda_disponible") and f.servicio_vivienda_disponible:
                for part in f.servicio_vivienda_disponible.split(", "):
                    if ":" not in part: continue
                    key, val = part.split(":", 1)
                    key_map = {"Agua":"serv_agua","Cloaca":"serv_cloaca","Alumbrado":"serv_alumbrado",
                               "Aseo":"serv_aseo","Telefono":"serv_telefono","Ninguno":"serv_ninguno","Otros":"serv_otro"}
                    k = key_map.get(key)
                    if k in self._serv_vars:
                        self._serv_vars[k].set(val.strip())
                    elif k == "serv_especifico" or key == "Especifique":
                        self._estado_entries["serv_especifico"].delete(0, END)
                        self._estado_entries["serv_especifico"].insert(0, val.strip())

        def _set_checkboxes(store, raw):
            if not raw: return
            for chunk in raw.split(" | "):
                if ":" not in chunk: continue
                _, vals = chunk.split(":", 1)
                for v in vals.split(", "):
                    v = v.strip()
                    if v in store:
                        store[v].set(1)

        if hasattr(f, "materiales_vivienda"):
            _set_checkboxes(self._mat_pared_vars, f.materiales_vivienda)
            _set_checkboxes(self._mat_techo_vars, f.materiales_vivienda)
            _set_checkboxes(self._mat_piso_vars, f.materiales_vivienda)
        if hasattr(f, "servicio_comunidad"):
            _set_checkboxes(self._mat_serv_com_vars, f"Comunidad: {f.servicio_comunidad}")

        for fam in f.grupo_familiar:
            self.crear_nuevo_panel_familiar()
            panel, inputs = self.familiares_panels[-1]
            inputs["nombre"].delete(0, END); inputs["nombre"].insert(0, fam.nombre)
            inputs["apellido"].delete(0, END); inputs["apellido"].insert(0, fam.apellido)
            inputs["parentesco"].delete(0, END); inputs["parentesco"].insert(0, fam.parentesco)
            inputs["edad"].delete(0, END); inputs["edad"].insert(0, fam.edad)
            inputs["genero"].delete(0, END); inputs["genero"].insert(0, fam.genero)
            inputs["estado_civil"].delete(0, END); inputs["estado_civil"].insert(0, fam.estado_civil)
            inputs["nivel_educacion"].delete(0, END); inputs["nivel_educacion"].insert(0, fam.nivel_educacion)
            inputs["profesion"].delete(0, END); inputs["profesion"].insert(0, fam.profesion_oficio)
            inputs["lugar_trabajo"].delete(0, END); inputs["lugar_trabajo"].insert(0, fam.lugar_trabajo)
            inputs["ingreso_mensual"].delete(0, END); inputs["ingreso_mensual"].insert(0, fam.ingreso_mensual)
            inputs["observacion"].delete(0, END); inputs["observacion"].insert(0, fam.observacion)

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.usuario_rol = None
        self.funcionarios = []
        self.familiares_panels = []
        self.inicio_sesion()

    def gestionar_usuarios(self):
        win = Toplevel(self.root)
        win.title("Gestionar Usuarios")
        win.geometry("500x400")
        win.configure(bg=self.bg_card)
        win.transient(self.root)
        win.grab_set()

        Label(win, text="Usuarios del Sistema", font=("Segoe UI", 14, "bold"),
              bg=self.bg_card, fg=self.primary).pack(pady=(15, 10))

        frame = Frame(win, bg=self.bg_card)
        frame.pack(fill=BOTH, expand=True, padx=15)

        columns = ("Usuario", "Rol")
        tree = ttk.Treeview(frame, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
        tree.column("Usuario", width=200)
        tree.column("Rol", width=150)
        tree.pack(fill=BOTH, expand=True)

        def cargar_usuarios():
            for item in tree.get_children():
                tree.delete(item)
            for u in obtener_usuarios():
                tree.insert("", "end", iid=u["username"], values=(u["username"], u["rol"]))

        cargar_usuarios()

        btn_frame = Frame(win, bg=self.bg_card)
        btn_frame.pack(fill=X, padx=15, pady=10)

        def agregar_usuario():
            username = simpledialog.askstring("Nuevo Usuario", "Nombre de usuario:", parent=win)
            if not username: return
            password = simpledialog.askstring("Nuevo Usuario", "Contrasena:", parent=win, show="*")
            if not password: return
            rol = simpledialog.askstring("Nuevo Usuario", "Rol (viewer/editor/modifier/subadmin/admin):", parent=win)
            if rol not in ("viewer", "editor", "modifier", "subadmin", "admin"):
                messagebox.showerror("Error", "Rol invalido", parent=win)
                return
            try:
                crear_usuario(username, password, rol)
                cargar_usuarios()
                registrar_auditoria(self.usuario_actual, "CREAR_USUARIO", f"Usuario {username} con rol {rol}")
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)

        def eliminar_usr():
            sel = tree.selection()
            if not sel: return
            user = sel[0]
            if user == "admin":
                messagebox.showwarning("Error", "No se puede eliminar el usuario admin", parent=win)
                return
            if messagebox.askyesno("Confirmar", f"Eliminar usuario '{user}'?", parent=win):
                eliminar_usuario(user)
                cargar_usuarios()
                registrar_auditoria(self.usuario_actual, "ELIMINAR_USUARIO", f"Usuario {user}")

        Button(btn_frame, text="Agregar", font=("Segoe UI", 10), bg=self.success, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=agregar_usuario).pack(side=LEFT, padx=5, ipady=4)
        Button(btn_frame, text="Eliminar", font=("Segoe UI", 10), bg=self.danger, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=eliminar_usr).pack(side=LEFT, padx=5, ipady=4)
        Button(btn_frame, text="Cerrar", font=("Segoe UI", 10), bg=self.text_sec, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=win.destroy).pack(side=RIGHT, padx=5, ipady=4)

    def ver_auditoria(self):
        win = Toplevel(self.root)
        win.title("Registro de Auditoria")
        win.geometry("700x500")
        win.configure(bg=self.bg_card)
        win.transient(self.root)
        win.grab_set()

        Label(win, text="Auditoria del Sistema", font=("Segoe UI", 14, "bold"),
              bg=self.bg_card, fg=self.primary).pack(pady=(15, 10))

        frame = Frame(win, bg=self.bg_card)
        frame.pack(fill=BOTH, expand=True, padx=15, pady=(0, 10))

        columns = ("Fecha", "Usuario", "Accion", "Detalle")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        for col in columns:
            tree.heading(col, text=col)
        tree.column("Fecha", width=160)
        tree.column("Usuario", width=100)
        tree.column("Accion", width=100)
        tree.column("Detalle", width=300)
        tree.pack(fill=BOTH, expand=True)

        for reg in obtener_auditoria(200):
            tree.insert("", "end", values=(reg["fecha"], reg["usuario"], reg["accion"], reg["detalle"]))

        Button(win, text="Cerrar", font=("Segoe UI", 10), bg=self.text_sec, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=win.destroy).pack(pady=(0, 15), ipady=4)


if __name__ == "__main__":
    root = Tk()
    app = UI(root)
    root.mainloop()
