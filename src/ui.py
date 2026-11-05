import calendar
from datetime import date

from tkinter import *
from tkinter import ttk, messagebox, simpledialog
import tkinter.font as tkfont
from logic import (Funcionario, Familiar, cargar_funcionarios, guardar_funcionarios,
                   verificar_login, eliminar_funcionario, restaurar_funcionario,
                   crear_usuario, eliminar_usuario, obtener_usuarios,
                   obtener_auditoria, registrar_auditoria, ROLES,
                   cargar_egresos, guardar_egresos, RUBROS_EGRESO, calcular_balance,
                   cargar_catalogo, valores_catalogo, detalle_de_lugar, lugar_por_detalle,
                   cargar_operadoras, agregar_catalogo, eliminar_catalogo,
                   agregar_operadora, eliminar_operadora,
                   normalizar_cedula, dividir_telefono, solo_digitos)


def _detectar_fuente():
    """Elige la mejor tipografia disponible segun el sistema."""
    try:
        disponibles = set(tkfont.families())
    except Exception:
        disponibles = set()
    for nombre in ("Segoe UI", "Inter", "Noto Sans", "DejaVu Sans", "Liberation Sans"):
        if nombre in disponibles:
            return nombre
    return "TkDefaultFont"


FONT = "Segoe UI"

class UI:
    def __init__(self, root):
        self.root = root
        self.root.title("Bienestar y Proteccion Social - Sistema Policia")
        self.root.minsize(950, 680)
        self.root.geometry("950x680")

        global FONT
        FONT = _detectar_fuente()

        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Paleta institucional: azul marino + dorado
        self.bg = "#eef1f6"
        self.bg_card = "#ffffff"
        self.primary = "#0f2a4a"
        self.primary_hover = "#1b3d66"
        self.accent = "#c9a227"
        self.accent_hover = "#b08d1e"
        self.danger = "#b3283c"
        self.danger_hover = "#8f1f30"
        self.success = "#1e7d4f"
        self.success_hover = "#166039"
        self.warning = "#c9a227"
        self.warning_hover = "#b08d1e"
        self.text = "#18222f"
        self.text_sec = "#5b6b82"
        self.border = "#d8dee9"
        self.sidebar_bg = "#0c1d33"
        self.sidebar_active = "#17314f"
        self.sidebar_text = "#dbe6f5"
        self.sep = "#2a4a70"
        self.muted = "#6c7a90"
        self.muted_hover = "#56637a"
        self.row_even = "#f7f9fc"
        self.row_odd = "#ffffff"
        self.readonly_bg = "#f4f6fa"
        self.selected_bg = "#dbe6f5"

        self.style.configure(".", font=(FONT, 10), background=self.bg)
        self.style.configure("Card.TFrame", background=self.bg_card, relief="solid", borderwidth=1)
        self.style.configure("CardTitle.TLabel", font=(FONT, 12, "bold"), background=self.bg_card, foreground=self.text)
        self.style.configure("Title.TLabel", font=(FONT, 16, "bold"), foreground=self.text)
        self.style.configure("Subtitle.TLabel", font=(FONT, 11), foreground=self.text_sec)
        self.style.configure("Field.TLabel", font=(FONT, 10), background=self.bg_card, foreground=self.text)
        self.style.configure("Accent.TButton", font=(FONT, 10, "bold"), background=self.accent, foreground=self.primary, borderwidth=0)
        self.style.map("Accent.TButton", background=[("active", self.accent_hover)])
        self.style.configure("Danger.TButton", font=(FONT, 10), background=self.danger, foreground="white", borderwidth=0)
        self.style.map("Danger.TButton", background=[("active", self.danger_hover)])
        self.style.configure("Success.TButton", font=(FONT, 10, "bold"), background=self.success, foreground="white", borderwidth=0)
        self.style.map("Success.TButton", background=[("active", self.success_hover)])
        self.style.configure("Warning.TButton", font=(FONT, 10), background=self.warning, foreground=self.primary, borderwidth=0)
        self.style.map("Warning.TButton", background=[("active", self.warning_hover)])
        self.style.configure("TEntry", fieldbackground=self.bg_card, foreground=self.text, borderwidth=1, relief="solid", bordercolor=self.border, lightcolor=self.border, darkcolor=self.border)
        self.style.map("TEntry", bordercolor=[("focus", self.accent)])
        self.style.configure("TCombobox", fieldbackground=self.readonly_bg,
                             background=self.readonly_bg, foreground=self.text,
                             arrowcolor=self.primary, bordercolor=self.border,
                             lightcolor=self.border, darkcolor=self.border, padding=4)
        self.style.map("TCombobox",
                       fieldbackground=[("readonly", self.readonly_bg), ("disabled", self.bg), ("focus", self.readonly_bg)],
                       foreground=[("readonly", self.text), ("disabled", self.muted)],
                       selectbackground=[("readonly", self.readonly_bg)],
                       selectforeground=[("readonly", self.text)],
                       background=[("active", self.readonly_bg), ("readonly", self.readonly_bg)],
                       arrowcolor=[("active", self.accent), ("disabled", self.muted)],
                       bordercolor=[("focus", self.accent)])
        self.root.option_add("*TCombobox*Listbox.background", self.bg_card)
        self.root.option_add("*TCombobox*Listbox.foreground", self.text)
        self.root.option_add("*TCombobox*Listbox.selectBackground", self.selected_bg)
        self.root.option_add("*TCombobox*Listbox.selectForeground", self.primary)
        self.style.configure("TNotebook", background=self.bg, borderwidth=0)
        self.style.configure("TNotebook.Tab", font=(FONT, 10, "bold"), padding=[11, 7], background=self.border, foreground=self.text_sec)
        self.style.map("TNotebook.Tab", background=[("selected", self.bg_card)], foreground=[("selected", self.primary)])
        self.style.configure("Treeview", font=(FONT, 10), rowheight=34, fieldbackground=self.bg_card, foreground=self.text, borderwidth=0)
        self.style.configure("Treeview.Heading", font=(FONT, 10, "bold"), background=self.primary, foreground="white", relief="flat", borderwidth=0)
        self.style.map("Treeview.Heading", background=[("active", self.primary_hover)])
        self.style.map("Treeview", background=[("selected", self.selected_bg)], foreground=[("selected", self.primary)])
        self.style.configure("TSpinbox", fieldbackground=self.bg_card)
        self.style.configure("TRadiobutton", font=(FONT, 10), background=self.bg_card, foreground=self.text)
        self.style.configure("TCheckbutton", font=(FONT, 10), background=self.bg_card, foreground=self.text)
        self.style.configure("Vertical.TScrollbar", background=self.border, troughcolor=self.bg, borderwidth=0, arrowsize=14)

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

        topbar = Frame(self.panel_principal, bg=self.accent, height=6)
        topbar.pack(fill=X)
        topbar.pack_propagate(False)

        container = Frame(self.panel_principal, bg=self.sidebar_bg)
        container.pack(fill=BOTH, expand=True)

        card = Frame(container, bg=self.bg_card, highlightbackground=self.accent, highlightthickness=1)
        card.place(relx=0.5, rely=0.45, anchor=CENTER)

        Frame(card, bg=self.accent, height=5).pack(fill=X)

        Label(card, text="\U0001f6e1", font=(FONT, 36),
              bg=self.bg_card, fg=self.accent).pack(pady=(30, 5))
        Label(card, text="Bienestar y Proteccion Social", font=(FONT, 18, "bold"),
              bg=self.bg_card, fg=self.primary).pack(pady=(0, 5))
        Label(card, text="Sistema de Gestion Policial", font=(FONT, 11),
              bg=self.bg_card, fg=self.text_sec).pack(pady=(0, 28))

        frame = Frame(card, bg=self.bg_card)
        frame.pack(padx=50, pady=(0, 35))

        Label(frame, text="Usuario", font=(FONT, 10),
              bg=self.bg_card, fg=self.text, anchor=W).grid(row=0, column=0, sticky=W, pady=(0, 3))
        self.input_usuario = Entry(frame, font=(FONT, 12), relief="solid", borderwidth=1,
                                   highlightbackground=self.border, highlightthickness=1, highlightcolor=self.accent)
        self.input_usuario.grid(row=1, column=0, pady=(0, 12), ipady=5, ipadx=6)
        self.input_usuario.focus()

        Label(frame, text="Contrasena", font=(FONT, 10),
              bg=self.bg_card, fg=self.text, anchor=W).grid(row=2, column=0, sticky=W, pady=(0, 3))
        self.input_contrasena = Entry(frame, font=(FONT, 12), show="*", relief="solid", borderwidth=1,
                                      highlightbackground=self.border, highlightthickness=1, highlightcolor=self.accent)
        self.input_contrasena.grid(row=3, column=0, pady=(0, 18), ipady=5, ipadx=6)
        self.input_contrasena.bind("<Return>", lambda e: self.verificar_login())

        self.label_error = Label(frame, text="", font=(FONT, 9), bg=self.bg_card, fg=self.danger)
        self.label_error.grid(row=4, column=0, pady=(0, 8))

        Button(frame, text="Iniciar Sesion", font=(FONT, 12, "bold"), bg=self.accent, fg=self.primary,
               activebackground=self.accent_hover, activeforeground=self.primary, relief="flat", borderwidth=0,
               cursor="hand2", command=self.verificar_login).grid(row=5, column=0, sticky=EW, ipady=7)

        modo = "MODO PRUEBA" if __import__('os').environ.get("DB_MODE") == "test" else ""
        texto_footer = f"\u00a9 {__import__('datetime').datetime.now().year} Sistema Policial v1.0. Todos los derechos reservados."
        if modo:
            texto_footer = f"{modo} - {texto_footer}"
        Label(container, text=texto_footer,
              font=(FONT, 8), bg=self.sidebar_bg, fg="#9db2cc").pack(side=BOTTOM, pady=15)

        Button(container, text="Salir", font=(FONT, 10), bg=self.danger, fg="white",
               activebackground=self.danger_hover, activeforeground="white", relief="flat", borderwidth=0,
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
        panel = Frame(self.pagina_principal, bg=self.sidebar_bg, width=220, highlightthickness=0)
        panel.pack(side=LEFT, fill=Y)
        panel.pack_propagate(False)

        # Header with icon
        header = Frame(panel, bg=self.sidebar_bg)
        header.pack(fill=X, pady=(22, 0))
        Label(header, text="\U0001f6e1", font=(FONT, 20),
              bg=self.sidebar_bg, fg=self.accent).pack()
        Label(header, text="Bienestar Social", font=(FONT, 13, "bold"),
              bg=self.sidebar_bg, fg="white").pack(pady=(2, 12))

        # User info card
        user_card = Frame(panel, bg=self.sidebar_active, highlightbackground=self.accent, highlightthickness=1)
        user_card.pack(fill=X, padx=12, pady=(0, 14), ipady=6)
        Label(user_card, text=f"{self.usuario_actual}", font=(FONT, 12, "bold"),
              bg=self.sidebar_active, fg="white").pack(pady=(6, 1))
        Label(user_card, text=f"Rol: {self.usuario_rol}", font=(FONT, 9),
              bg=self.sidebar_active, fg="#c7d6ea").pack(pady=(0, 6))

        # Separator
        Frame(panel, bg=self.sep, height=1).pack(fill=X, padx=15, pady=(0, 8))

        btn_style = {"font": (FONT, 10), "bg": self.sidebar_bg, "fg": self.sidebar_text,
                     "activebackground": self.sidebar_active, "activeforeground": self.accent,
                     "relief": "flat", "borderwidth": 0, "highlightthickness": 0,
                     "cursor": "hand2", "anchor": W}

        def make_btn(text, cmd, icon=""):
            b = Button(panel, text=f"  {icon}  {text}" if icon else f"  {text}",
                       **btn_style, command=cmd)
            b.pack(fill=X, padx=10, pady=2, ipady=8)
            b.bind("<Enter>", lambda e: b.configure(bg=self.sidebar_active, fg=self.accent))
            b.bind("<Leave>", lambda e: b.configure(bg=self.sidebar_bg, fg=self.sidebar_text))
            return b

        make_btn("Inicio", self.mostrar_pagina_principal, "\U0001f3e0")
        Frame(panel, bg=self.sep, height=1).pack(fill=X, padx=15, pady=8)
        make_btn("Ayuda", self.mostrar_ayuda, "\u2753")
        if self._puede("crear"):
            make_btn("Nuevo Funcionario", self.mostrar_registrar_usuario, "\u2795")
        if self.usuario_rol == "admin":
            Frame(panel, bg=self.sep, height=1).pack(fill=X, padx=15, pady=8)
            make_btn("Gestionar Usuarios", self.gestionar_usuarios, "\u2699")
        if self.usuario_rol in ("admin", "subadmin"):
            if self.usuario_rol == "subadmin":
                Frame(panel, bg=self.sep, height=1).pack(fill=X, padx=15, pady=8)
            make_btn("Ver Auditoria", self.ver_auditoria, "\U0001f4cb")
            make_btn("Catálogos", self.abrir_catalogos, "\U0001f4c1")

        # Logout at bottom
        Frame(panel, bg=self.sep, height=1).pack(fill=X, padx=15, pady=8)
        logout_btn = Button(panel, text="  \u23f3  Cerrar Sesion",
                            font=(FONT, 10), fg="white",
                            bg=self.danger, activebackground=self.danger_hover,
                            activeforeground="white", relief="flat",
                            borderwidth=0, highlightthickness=0, cursor="hand2", anchor=W,
                            command=self.cerrar_sesion)
        logout_btn.pack(side=BOTTOM, fill=X, padx=10, pady=15, ipady=8)

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
            Label(scroll_frame, text=texto, font=(FONT, size, "bold"),
                  bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=xpad, pady=pady)
            Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=xpad)

        def subtitulo(texto):
            Label(scroll_frame, text=texto, font=(FONT, 12, "bold"),
                  bg=self.bg_card, fg=self.text).pack(anchor=W, padx=xpad, pady=(12, 3))

        def parrafo(texto):
            Label(scroll_frame, text=texto, font=(FONT, 10), wraplength=600, justify=LEFT,
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
            Label(scroll_frame, text=f"  \u2022 {rol}", font=(FONT, 10, "bold"),
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
            Label(scroll_frame, text=f"  \u2022 {cred}", font=(FONT, 10, "bold"),
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

        Label(content, text="Funcionarios Registrados", font=(FONT, 18, "bold"),
              bg=self.bg, fg=self.primary).pack(anchor=W, pady=(0, 2))
        Frame(content, bg=self.accent, height=3, width=46).pack(anchor=W, pady=(0, 6))
        Label(content, text="Gestione los funcionarios del sistema", font=(FONT, 10),
              bg=self.bg, fg=self.text_sec).pack(anchor=W, pady=(0, 15))

        bar = Frame(content, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        bar.pack(fill=X, pady=(0, 15))

        if self._puede("crear"):
            Button(bar, text="+ Nuevo Funcionario", font=(FONT, 10, "bold"), bg=self.accent, fg=self.primary,
                   activebackground=self.accent_hover, activeforeground=self.primary, relief="flat", borderwidth=0,
                   cursor="hand2", command=self.mostrar_registrar_usuario).pack(side=LEFT, padx=10, pady=8, ipady=5)

        Label(bar, text="Buscar:", font=(FONT, 10), bg=self.bg_card, fg=self.text).pack(side=LEFT, padx=(20, 5))
        self.input_busqueda = Entry(bar, font=(FONT, 10), relief="solid", borderwidth=1,
                                    highlightbackground=self.border, highlightthickness=1, highlightcolor=self.accent)
        self.input_busqueda.pack(side=LEFT, ipady=3, ipadx=3)
        self.input_busqueda.bind("<Return>", lambda e: self.buscar_funcionario())

        Button(bar, text="Buscar", font=(FONT, 10), bg=self.primary, fg="white",
               activebackground=self.primary_hover, activeforeground="white", relief="flat", borderwidth=0,
               cursor="hand2", command=self.buscar_funcionario).pack(side=LEFT, padx=5, pady=8, ipady=4)

        self.mostrar_inactivos_var = IntVar()
        Checkbutton(bar, text="Ver inactivos", font=(FONT, 9), variable=self.mostrar_inactivos_var,
                    bg=self.bg_card, fg=self.text, activebackground=self.bg_card,
                    activeforeground=self.primary, selectcolor=self.bg_card,
                    command=self.toggle_inactivos).pack(side=RIGHT, padx=10)

        # Action bar
        action_bar = Frame(content, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        action_bar.pack(fill=X, pady=(0, 10))

        Button(action_bar, text="Ver Datos", font=(FONT, 10), bg=self.primary, fg="white",
               activebackground=self.primary_hover, activeforeground="white", relief="flat", borderwidth=0,
               cursor="hand2", command=self.ver_funcionario).pack(side=LEFT, padx=5, pady=5, ipady=5)
        if self._puede("modificar"):
            Button(action_bar, text="Editar", font=(FONT, 10), bg=self.warning, fg=self.primary,
                   activebackground=self.warning_hover, activeforeground=self.primary, relief="flat", borderwidth=0, cursor="hand2",
                   command=self.editar_funcionario).pack(side=LEFT, padx=5, pady=5, ipady=5)
        if self._puede("eliminar"):
            Button(action_bar, text="Desactivar", font=(FONT, 10), bg=self.danger, fg="white",
                   activebackground=self.danger_hover, activeforeground="white", relief="flat", borderwidth=0,
                   cursor="hand2", command=self.desactivar_funcionario).pack(side=LEFT, padx=5, pady=5, ipady=5)
        if self.usuario_rol in ("admin", "subadmin"):
            Button(action_bar, text="Restaurar", font=(FONT, 10), bg=self.success, fg="white",
                   activebackground=self.success_hover, relief="flat", borderwidth=0,
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

        self.tree.tag_configure("even", background=self.row_even)
        self.tree.tag_configure("odd", background=self.row_odd)
        self.tree.tag_configure("inactivo", background="#fbe4e6", foreground="#9aa6b8")
        self.tree.bind("<Double-1>", lambda e: self.ver_funcionario())
        if self._puede("eliminar"):
            self.tree.bind("<Delete>", lambda e: self.desactivar_funcionario())

        self.funcionarios = cargar_funcionarios()
        self.cargar_en_tabla()

    def cargar_en_tabla(self, filtro=None):
        for row in self.tree.get_children():
            self.tree.delete(row)
        if filtro:
            lista = [f for f in self.funcionarios
                     if (self.mostrar_inactivos or getattr(f, "activo", 1) == 1)
                     and (filtro.lower() in (f.nombre or "").lower()
                          or filtro.lower() in (f.apellido or "").lower()
                          or filtro.lower() in (f.cedula or "").lower())]
        else:
            lista = [f for f in self.funcionarios
                     if self.mostrar_inactivos or getattr(f, "activo", 1) == 1]
        for i, f in enumerate(lista):
            tag = "inactivo" if getattr(f, "activo", 1) == 0 else ("even" if i % 2 == 0 else "odd")
            nombre = f.nombre or ""; apellido = f.apellido or ""; cedula = f.cedula or ""
            edad = f.edad or ""; telefono = self._telefono_completo(f)
            self.tree.insert("", END, iid=cedula,
                             values=(normalizar_cedula(cedula), nombre, apellido, edad, telefono),
                             tags=(tag,))

    def toggle_inactivos(self):
        self.mostrar_inactivos = self.mostrar_inactivos_var.get()
        self.cargar_en_tabla()

    def buscar_funcionario(self):
        self.funcionarios = cargar_funcionarios()
        texto = self.input_busqueda.get().strip()
        self.cargar_en_tabla(filtro=texto if texto else None)

    def _telefono_completo(self, func):
        op = (getattr(func, "operadora", "") or "").strip()
        prefijo, abonado = dividir_telefono(getattr(func, "telefono", "") or "")
        if not prefijo and len(op) == 3 and op.isdigit():
            prefijo = op
        if prefijo and abonado:
            return f"{prefijo}-{abonado}"
        return abonado or (getattr(func, "telefono", "") or "")

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

        Label(scroll_frame, text="Datos Personales", font=(FONT, 16, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(20, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 10))

        fields = [
            ("Cedula", func.cedula),
            ("Nombre", func.nombre),
            ("Apellido", func.apellido),
            ("Fecha de Nacimiento", func.fecha_nacimiento or ""),
            ("Edad", func.edad or ""),
            ("Genero", getattr(func, "genero", "") or ""),
            ("Estado Civil", func.estado_civil or ""),
            ("Telefono", self._telefono_completo(func)),
            ("Peso", func.peso or ""),
            ("Altura", func.altura or ""),
        ]
        self._crear_field_grid(scroll_frame, fields)

        if func.residencia_municipio or func.residencia_pueblo or func.residencia:
            Label(scroll_frame, text="Direccion", font=(FONT, 12, "bold"),
                  bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
            Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))
            self._crear_field_grid(scroll_frame, [
                ("Municipio", getattr(func, "residencia_municipio", "") or ""),
                ("Pueblo/Sector", getattr(func, "residencia_pueblo", "") or ""),
                ("Direccion", func.residencia or ""),
            ])

        Label(scroll_frame, text="Datos Laborales", font=(FONT, 12, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))

        laboral_fields = [
            ("Jerarquia", getattr(func, "jerarquia", "") or ""),
            ("Lugar de Servicio", getattr(func, "lugar_presta_servicio", "") or ""),
            ("Tiempo de Servicio", getattr(func, "tiempo_servicio", "") or ""),
            ("Salario Mensual (Bs.)", getattr(func, "salario_mensual", "") or ""),
            ("Fecha de Gestion", getattr(func, "fecha_gestion", "") or ""),
        ]
        self._crear_field_grid(scroll_frame, laboral_fields)

        Label(scroll_frame, text="Plan Vivienda", font=(FONT, 12, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))

        plan_fields = [
            ("Terreno Propio", getattr(func, "terreno_propio", "") or ""),
            ("Ubicacion del Terreno", getattr(func, "ubicacion_terreno", "") or ""),
            ("Condicion de Vivienda", getattr(func, "condicion_vivienda", "") or ""),
            ("Necesidad Habitacional", getattr(func, "necesidad_vivienda", "") or ""),
            ("Posee Vivienda", getattr(func, "posee_vivienda", "") or ""),
            ("Organismo Publico", getattr(func, "organismo_publico", "") or ""),
            ("Especifique Organismo Publico", getattr(func, "organismo_publico_otro", "") or ""),
            ("Organismo Privado", getattr(func, "organismo_privado", "") or ""),
            ("Especifique Organismo Privado", getattr(func, "organismo_privado_otro", "") or ""),
            ("Gestion Organismo Oficial", getattr(func, "gestion_organismo_oficial", "") or ""),
            ("Fecha de Gestion", getattr(func, "fecha_gestion", "") or ""),
        ]
        self._crear_field_grid(scroll_frame, plan_fields)

        Label(scroll_frame, text="Estado de la Vivienda", font=(FONT, 12, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))

        estado_fields = [
            ("Tenencia de Tierra", getattr(func, "tenencia_tierra", "") or ""),
            ("Especifique Tenencia", getattr(func, "tenencia_tierra_otra", "") or ""),
            ("Tiempo de Ocupacion", getattr(func, "tiempo_ocupacion", "") or ""),
            ("Ambiente de Vivienda", getattr(func, "ambiente_vivienda", "") or ""),
            ("Servicios Disponibles", getattr(func, "servicio_vivienda_disponible", "") or ""),
            ("Materiales de Vivienda", getattr(func, "materiales_vivienda", "") or ""),
            ("Servicios de la Comunidad", getattr(func, "servicio_comunidad", "") or ""),
        ]
        self._crear_field_grid(scroll_frame, estado_fields)

        Label(scroll_frame, text="Balance Socio-Económico Familiar", font=(FONT, 12, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
        Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))

        bal_fields = [
            ("Ingreso del Trabajador", getattr(func, "ingreso_trabajador", "0") or "0"),
            ("Ingreso Familiar (adicional)", getattr(func, "ingreso_familiar_adicional", "0") or "0"),
            ("Total Ingreso Familiar", getattr(func, "total_ingreso_familiar", "0") or "0"),
            ("Egreso del Grupo Familiar", getattr(func, "egreso_grupo_familiar", "0") or "0"),
            ("Disponibilidad Económica", getattr(func, "disponibilidad_economica", "0") or "0"),
        ]
        self._crear_field_grid(scroll_frame, bal_fields)

        egresos = getattr(func, "egresos_mensuales", None)
        if egresos is None:
            egresos = cargar_egresos(func.cedula)
        if egresos:
            Label(scroll_frame, text="Distribución del Ingreso Real Familiar", font=(FONT, 10, "bold"),
                  bg=self.bg_card, fg=self.text).pack(anchor=W, padx=25, pady=(8, 4))
            for e in egresos:
                monto = e.get("monto", "0")
                obs = e.get("observacion", "")
                txt = f"{e.get('rubro', '')}: {monto}" + (f"  ({obs})" if obs else "")
                Label(scroll_frame, text=txt, font=(FONT, 9),
                      bg=self.bg_card, fg=self.text, anchor=W).pack(anchor=W, padx=35, pady=1)

        if func.grupo_familiar:
            Label(scroll_frame, text="Grupo Familiar", font=(FONT, 12, "bold"),
                  bg=self.bg_card, fg=self.primary).pack(anchor=W, padx=20, pady=(12, 5))
            Frame(scroll_frame, bg=self.border, height=1).pack(fill=X, padx=20, pady=(0, 8))
            for i, fam in enumerate(func.grupo_familiar):
                Label(scroll_frame, text=f"Familiar {i+1}", font=(FONT, 10, "bold"),
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
                        ("Ingreso Mensual (Bs.)", fam.ingreso_mensual or ""),
                    ("Observacion", fam.observacion or ""),
                ])

        Label(scroll_frame, text="", bg=self.bg_card).pack(pady=10)

        btn_frame = Frame(content, bg=self.bg_card)
        btn_frame.pack(fill=X, padx=20, pady=(0, 15))
        btn_left = Frame(btn_frame, bg=self.bg_card)
        btn_left.pack(side=LEFT)
        btn_right = Frame(btn_frame, bg=self.bg_card)
        btn_right.pack(side=RIGHT)

        Button(btn_left, text="Imprimir Ficha", font=(FONT, 10), bg=self.primary, fg="white",
               activebackground=self.primary_hover, relief="flat", borderwidth=0,
               cursor="hand2", command=lambda: self.imprimir_ficha(func)).pack(side=LEFT, padx=5, ipady=5)
        if self._puede("modificar"):
            Button(btn_left, text="Editar", font=(FONT, 10), bg=self.warning, fg=self.primary,
                   activebackground=self.warning_hover, activeforeground=self.primary, relief="flat", borderwidth=0, cursor="hand2",
                   command=lambda: self.editar_funcionario(cedula)).pack(side=LEFT, padx=5, ipady=5)
        if self._puede("eliminar"):
            Button(btn_left, text="Desactivar", font=(FONT, 10), bg=self.danger, fg="white",
                   activebackground=self.danger_hover, relief="flat", borderwidth=0, cursor="hand2",
                   command=lambda: self.desactivar_funcionario(cedula, self._imprimir_content)).pack(side=LEFT, padx=5, ipady=5)
        if self.usuario_rol in ("admin", "subadmin"):
            Button(btn_left, text="Restaurar", font=(FONT, 10), bg=self.success, fg="white",
                   activebackground=self.success_hover, relief="flat", borderwidth=0, cursor="hand2",
                   command=lambda: self.restaurar_funcionario(cedula, self._imprimir_content)).pack(side=LEFT, padx=5, ipady=5)
        Button(btn_right, text="Volver", font=(FONT, 10), bg=self.muted, fg="white",
               activebackground=self.muted_hover, relief="flat", borderwidth=0,
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
            lbl = Label(frame, text=f"{label}:", font=(FONT, 10, "bold"),
                        bg=self.bg_card, fg=self.text_sec, width=28, anchor=W)
            lbl.grid(row=i, column=0, sticky=W, padx=(25, 5), pady=2)
            val = Label(frame, text=value if value else "-", font=(FONT, 10),
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
                ("Edad", func.edad), ("Genero", getattr(func, "genero", "") or ""),
                ("Estado Civil", func.estado_civil),
                ("Telefono", self._telefono_completo(func)), ("Peso", func.peso or ""),
                ("Altura", func.altura or ""),
                ("Municipio", getattr(func, "residencia_municipio", "") or ""),
                ("Pueblo/Sector", getattr(func, "residencia_pueblo", "") or ""),
                ("Direccion", func.residencia or ""),
            ])
            write_section("Datos Laborales", [
                ("Jerarquia", func.jerarquia or ""),
                ("Lugar Servicio", func.lugar_presta_servicio or ""),
                ("Tiempo Servicio", func.tiempo_servicio or ""),
                ("Salario Mensual (Bs.)", func.salario_mensual or ""),
            ])
            write_section("Plan Vivienda", [
                ("Terreno Propio", func.terreno_propio or ""),
                ("Ubicacion Terreno", func.ubicacion_terreno or ""),
                ("Condicion Vivienda", func.condicion_vivienda or ""),
                ("Necesidad Vivienda", func.necesidad_vivienda or ""),
                ("Organismo Publico", func.organismo_publico or ""),
                ("Especifique Organismo Publico", getattr(func, "organismo_publico_otro", "") or ""),
                ("Organismo Privado", func.organismo_privado or ""),
                ("Especifique Organismo Privado", getattr(func, "organismo_privado_otro", "") or ""),
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
                    ("Ingreso Mensual (Bs.)", fam.ingreso_mensual or ""),
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
            lines.append(f"Genero: {getattr(func, 'genero', '') or '-'}")
            lines.append(f"Estado Civil: {func.estado_civil}")
            lines.append(f"Telefono: {self._telefono_completo(func) or '-'}")
            lines.append(f"Peso: {func.peso or '-'}")
            lines.append(f"Altura: {func.altura or '-'}")
            lines.append(f"Municipio: {getattr(func, 'residencia_municipio', '') or '-'}")
            lines.append(f"Pueblo/Sector: {getattr(func, 'residencia_pueblo', '') or '-'}")
            lines.append(f"Direccion: {func.residencia or '-'}")
            lines.append(f"\nDATOS LABORALES")
            lines.append(f"Jerarquia: {func.jerarquia or '-'}")
            lines.append(f"Lugar Servicio: {func.lugar_presta_servicio or '-'}")
            lines.append(f"Tiempo Servicio: {func.tiempo_servicio or '-'}")
            lines.append(f"Salario Mensual (Bs.): {func.salario_mensual or '-'}")
            lines.append(f"\nPLAN VIVIENDA")
            lines.append(f"Terreno Propio: {func.terreno_propio or '-'}")
            lines.append(f"Ubicacion Terreno: {func.ubicacion_terreno or '-'}")
            lines.append(f"Condicion: {func.condicion_vivienda or '-'}")
            lines.append(f"Necesidad Vivienda: {func.necesidad_vivienda or '-'}")
            lines.append(f"Organismo Publico: {func.organismo_publico or '-'}")
            lines.append(f"Especifique Organismo Publico: {getattr(func, 'organismo_publico_otro', '') or '-'}")
            lines.append(f"Organismo Privado: {func.organismo_privado or '-'}")
            lines.append(f"Especifique Organismo Privado: {getattr(func, 'organismo_privado_otro', '') or '-'}")
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
                    lines.append(f"  Ingreso Mensual (Bs.): {fam.ingreso_mensual or '-'}")
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
            lines.append(f"Tiempo:{func.tiempo_servicio or '-'} Salario(Bs.):{func.salario_mensual or '-'} FecGestion:{func.fecha_gestion or '-'}")
            lines.append(f"")
            lines.append(f"VIVIENDA: Terreno:{func.terreno_propio or '-'} Ubi:{func.ubicacion_terreno or '-'}")
            lines.append(f"Condicion:{func.condicion_vivienda or '-'} Nec:{func.necesidad_vivienda or '-'}")
            lines.append(f"OrgPub:{func.organismo_publico or '-'} Esp:{getattr(func, 'organismo_publico_otro', '') or '-'}")
            lines.append(f"OrgPriv:{func.organismo_privado or '-'} Esp:{getattr(func, 'organismo_privado_otro', '') or '-'}")
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

        menu = Menu(self.root, tearoff=0, font=(FONT, 10), bg=self.bg_card, fg=self.text, activebackground=self.primary, activeforeground="white")
        menu.add_command(label="Imprimir (Sistema)", command=imprimir)
        menu.add_command(label="Exportar PDF", command=exportar_pdf)
        menu.add_command(label="Guardar TXT", command=guardar_txt)
        try:
            menu.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally:
            menu.grab_release()

    def desactivar_funcionario(self, cedula=None, frame_actual=None):
        if not self._puede("eliminar"):
            messagebox.showwarning("Permisos", "Su rol no tiene permiso para desactivar registros", parent=self.root)
            return
        if cedula is None:
            sel = self.tree.selection()
            if not sel: return
            cedula = sel[0]
        if messagebox.askyesno("Confirmar", "Desea desactivar este funcionario? (quedara oculto pero sus datos se conservan)", parent=self.root):
            eliminar_funcionario(cedula, usuario=self.usuario_actual)
            if frame_actual: frame_actual.destroy()
            self.cargar_en_tabla()

    def restaurar_funcionario(self, cedula=None, frame_actual=None):
        if not self._puede("eliminar"):
            messagebox.showwarning("Permisos", "Su rol no tiene permiso para restaurar registros", parent=self.root)
            return
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

        Label(content, text=titulo, font=(FONT, 18, "bold"),
              bg=self.bg, fg=self.text).pack(anchor=W, pady=(0, 5))
        Label(content, text=subtitulo, font=(FONT, 10),
              bg=self.bg, fg=self.text_sec).pack(anchor=W, pady=(0, 15))

        notebook = ttk.Notebook(content)
        notebook.pack(fill=BOTH, expand=True)

        self.tab_personales = Frame(notebook, bg=self.bg_card)
        self.tab_laborales = Frame(notebook, bg=self.bg_card)
        self.tab_vivienda_plan = Frame(notebook, bg=self.bg_card)
        self.tab_vivienda_estado = Frame(notebook, bg=self.bg_card)
        self.tab_familiares = Frame(notebook, bg=self.bg_card)
        self.tab_balance = Frame(notebook, bg=self.bg_card)

        notebook.add(self.tab_personales, text="Personales")
        notebook.add(self.tab_laborales, text="Laborales")
        notebook.add(self.tab_vivienda_plan, text="Plan Vivienda")
        notebook.add(self.tab_vivienda_estado, text="Estado Vivienda")
        notebook.add(self.tab_familiares, text="Familiares")
        notebook.add(self.tab_balance, text="Balance")

        self._crear_tab_personales()
        self._crear_tab_laborales()
        self._crear_tab_plan_vivienda()
        self._crear_tab_estado_vivienda()
        self._crear_tab_familiares()
        self._crear_tab_balance()

        footer = Frame(content, bg=self.bg)
        footer.pack(fill=X, pady=(12, 0))

        Button(footer, text="Limpiar Campos", font=(FONT, 10), bg=self.warning, fg=self.text,
               relief="flat", borderwidth=0, cursor="hand2", command=self.limpiar_campos).pack(side=LEFT, padx=5, ipady=5)
        Button(footer, text="Guardar Funcionario", font=(FONT, 10, "bold"), bg=self.success, fg="white",
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
        var = StringVar(master=frame)
        habilitado = {"valor": True}

        entry = Entry(frame, textvariable=var, font=(FONT, 11), relief="solid", borderwidth=1,
                      highlightbackground=self.border, highlightthickness=1,
                      state="readonly", readonlybackground=self.bg_card,
                      disabledbackground=self.readonly_bg, disabledforeground=self.text_sec)
        entry.pack(side=LEFT, fill=X, expand=True, ipady=3)

        boton = Button(frame, text="...", font=(FONT, 10, "bold"), bg=self.accent, fg=self.primary,
                       activebackground=self.accent_hover, relief="flat", borderwidth=0,
                       cursor="hand2")
        boton.pack(side=LEFT, padx=(4, 0), ipady=3, ipadx=6)

        meses = ["", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
                 "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]

        def get_val():
            return var.get()

        def set_val(val, disparar=False):
            s = str(val or "").strip()
            if not s or "/" not in s:
                var.set("")
                return
            parts = s.split("/")
            if len(parts) != 3:
                return
            try:
                d, m, a = int(parts[0]), int(parts[1]), int(parts[2])
                fecha = date(a, m, d)
            except Exception:
                return
            if fecha > date.today():
                return
            var.set(f"{d:02d}/{m:02d}/{a:04d}")
            if disparar and on_change:
                on_change()

        def abrir():
            if not habilitado["valor"]:
                return
            hoy = date.today()
            base = var.get()
            sel = hoy
            if "/" in base:
                try:
                    dd, mm, aa = [int(x) for x in base.split("/")]
                    sel = date(aa, mm, dd)
                except Exception:
                    sel = hoy
            estado = {"anio": sel.year, "mes": sel.month}

            top = Toplevel(self.root)
            top.title("Seleccionar fecha")
            top.transient(self.root)
            top.resizable(False, False)
            top.configure(bg=self.bg_card)
            top.grab_set()

            cab = Frame(top, bg=self.bg_card)
            cab.pack(fill=X, padx=10, pady=(10, 4))
            Button(cab, text="<", font=(FONT, 10, "bold"), bg=self.bg_card, fg=self.text,
                   relief="flat", borderwidth=0, cursor="hand2",
                   command=lambda: mover(-1)).pack(side=LEFT, padx=2)
            lbl = Label(cab, text="", font=(FONT, 11, "bold"), bg=self.bg_card, fg=self.text)
            lbl.pack(side=LEFT, expand=True)
            Button(cab, text=">", font=(FONT, 10, "bold"), bg=self.bg_card, fg=self.text,
                   relief="flat", borderwidth=0, cursor="hand2",
                   command=lambda: mover(1)).pack(side=RIGHT, padx=2)

            yrow = Frame(top, bg=self.bg_card)
            yrow.pack(fill=X, padx=10, pady=(0, 6))
            Label(yrow, text="Año:", font=(FONT, 10), bg=self.bg_card, fg=self.text).pack(side=LEFT)
            spin = Spinbox(yrow, from_=1900, to=hoy.year, width=6, font=(FONT, 10),
                           relief="solid", borderwidth=1)
            spin.pack(side=LEFT, padx=(4, 0))

            grid = Frame(top, bg=self.bg_card)
            grid.pack(padx=10, pady=(0, 6))

            def elegir(dia):
                set_val(f"{dia:02d}/{estado['mes']:02d}/{estado['anio']}", disparar=True)
                top.destroy()

            def render():
                lbl.config(text=f"{meses[estado['mes']]} {estado['anio']}")
                spin.delete(0, END)
                spin.insert(0, str(estado["anio"]))
                for w in grid.winfo_children():
                    w.destroy()
                for i, nombre in enumerate(["Lu", "Ma", "Mi", "Ju", "Vi", "Sá", "Do"]):
                    Label(grid, text=nombre, font=(FONT, 9, "bold"), bg=self.bg_card,
                          fg=self.text_sec, width=3).grid(row=0, column=i, padx=1, pady=1)
                cal = calendar.Calendar(firstweekday=0)
                for r, semana in enumerate(cal.monthdayscalendar(estado["anio"], estado["mes"]), start=1):
                    for c, dia in enumerate(semana):
                        if dia == 0:
                            Label(grid, text="", bg=self.bg_card, width=3).grid(row=r, column=c)
                            continue
                        fecha = date(estado["anio"], estado["mes"], dia)
                        futuro = fecha > hoy
                        Button(grid, text=str(dia), font=(FONT, 9), width=3,
                               relief="flat", borderwidth=0, cursor="hand2",
                               bg=self.bg_card, fg=self.text_sec if futuro else self.text,
                               state="disabled" if futuro else "normal",
                               command=lambda d=dia: elegir(d)).grid(row=r, column=c, padx=1, pady=1)

            def mover(delta):
                m = estado["mes"] + delta
                a = estado["anio"]
                if m < 1:
                    m, a = 12, a - 1
                elif m > 12:
                    m, a = 1, a + 1
                if a < 1900:
                    a, m = 1900, 1
                if (a, m) > (hoy.year, hoy.month):
                    return
                estado["mes"], estado["anio"] = m, a
                render()

            def set_anio(val):
                try:
                    a = int(val)
                except Exception:
                    a = estado["anio"]
                a = max(1900, min(a, hoy.year))
                if a == hoy.year and estado["mes"] > hoy.month:
                    estado["mes"] = hoy.month
                estado["anio"] = a
                render()

            spin.config(command=lambda: set_anio(spin.get()))
            spin.bind("<Return>", lambda e: set_anio(spin.get()))
            spin.bind("<FocusOut>", lambda e: set_anio(spin.get()))

            pie = Frame(top, bg=self.bg_card)
            pie.pack(fill=X, padx=10, pady=(0, 10))
            def ir_hoy():
                estado["anio"], estado["mes"] = hoy.year, hoy.month
                render()
            Button(pie, text="Hoy", font=(FONT, 10), bg=self.bg_card, fg=self.text,
                   relief="solid", borderwidth=1, cursor="hand2", command=ir_hoy).pack(side=LEFT, ipady=2, ipadx=8)
            Button(pie, text="Cerrar", font=(FONT, 10), bg=self.bg_card, fg=self.text,
                   relief="solid", borderwidth=1, cursor="hand2", command=top.destroy).pack(side=RIGHT, ipady=2, ipadx=8)

            render()

        boton.config(command=abrir)

        def set_enabled(valor):
            habilitado["valor"] = bool(valor)
            entry.configure(state="readonly" if valor else "disabled")
            boton.configure(state="normal" if valor else "disabled")

        frame.get = get_val
        frame.set = set_val
        frame.delete = lambda *a: var.set("")
        frame.insert = lambda idx, val: set_val(val)
        frame.config = lambda **kw: None
        frame.abrir = abrir
        frame.set_enabled = set_enabled
        frame.entry = entry
        frame.boton = boton

        return frame

    def _validar_cedula(self, propuesto):
        return all(c.isdigit() or c == "." for c in propuesto) and len(solo_digitos(propuesto)) <= 8

    def _validar_nombre(self, propuesto):
        return all(c.isalpha() or c.isspace() or c in "'-." for c in propuesto)

    def _validar_telefono(self, propuesto):
        return all(c.isdigit() or c == "-" for c in propuesto) and len(solo_digitos(propuesto)) <= 7

    def _formatear_telefono(self, valor):
        d = solo_digitos(valor)[:7]
        return f"{d[:3]}-{d[3:]}" if len(d) > 3 else d

    def _formatear_telefono_event(self, event=None):
        valor = self.input_telefono.get()
        fmt = self._formatear_telefono(valor)
        if valor != fmt:
            self.input_telefono.delete(0, END)
            self.input_telefono.insert(0, fmt)

    def _validar_decimal(self, propuesto, max_ent, max_dec):
        if propuesto == "":
            return True
        p = propuesto.replace(",", ".")
        if p.count(".") > 1 or any(c not in "0123456789." for c in p):
            return False
        entero, _, decimales = p.partition(".")
        if not entero:
            return False
        return len(entero) <= max_ent and len(decimales) <= max_dec

    def _validar_peso(self, propuesto):
        return self._validar_decimal(propuesto, 3, 1)

    def _validar_altura(self, propuesto):
        return self._validar_decimal(propuesto, 1, 2)

    def _normalizar_decimal(self, entry):
        valor = entry.get().strip().replace(",", ".")
        if valor != entry.get():
            entry.delete(0, END)
            entry.insert(0, valor)
        return valor

    def _validar_ingreso(self, propuesto):
        return self._validar_decimal(propuesto, 10, 2)

    def _normalizar_monto(self, valor):
        v = (valor or "").strip().replace(",", ".")
        return v[:-1] if v.endswith(".") else v

    def _normalizar_monto_entry(self, entry):
        valor = self._normalizar_monto(entry.get())
        if valor != entry.get():
            entry.delete(0, END)
            entry.insert(0, valor)
        return valor

    def _normalizar_tiempo_servicio(self, valor):
        v = (valor or "").strip()
        if not v:
            return ""
        if v.isdigit():
            n = int(v)
            if 1 <= n <= 35:
                return f"{n} año" if n == 1 else f"{n} años"
            return ""
        return v

    def _crear_tab_personales(self):
        p = self.tab_personales

        canvas = Canvas(p, bg=self.bg_card, highlightthickness=0)
        scroll = ttk.Scrollbar(p, orient=VERTICAL, command=canvas.yview)
        sf = Frame(canvas, bg=self.bg_card)
        sf.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win_id = canvas.create_window((0, 0), window=sf, anchor=NW)
        def _resize_canvas(event):
            canvas.itemconfig(win_id, width=event.width)
        canvas.bind("<Configure>", _resize_canvas)
        canvas.configure(yscrollcommand=scroll.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=True)
        scroll.pack(side=RIGHT, fill=Y)
        def _on_mousewheel(event):
            if event.num == 4: canvas.yview_scroll(-3, "units")
            elif event.num == 5: canvas.yview_scroll(3, "units")
            else: canvas.yview_scroll(-1 * (event.delta // 120), "units")
        for w in (canvas, sf):
            w.bind("<Button-4>", _on_mousewheel)
            w.bind("<Button-5>", _on_mousewheel)
            w.bind("<MouseWheel>", _on_mousewheel)

        p = sf
        for i in range(14): p.grid_rowconfigure(i, pad=8)
        for i in range(6): p.grid_columnconfigure(i, weight=1, pad=15)

        Label(p, text="Datos Personales", font=(FONT, 13, "bold"),
              bg=self.bg_card, fg=self.primary).grid(row=0, column=0, columnspan=6, sticky=W, pady=(15, 10))

        def campo_fila(fila, textos, colspan=1):
            widgets = []
            for j, (label, col) in enumerate(zip(textos, range(0, 6, 2))):
                c = col if colspan == 1 else j * 2
                Label(p, text=label, font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=fila, column=c, sticky=W, pady=(6, 2))
                e = Entry(p, font=(FONT, 11), relief="solid", borderwidth=1,
                          highlightbackground=self.border, highlightthickness=1)
                e.grid(row=fila + 1, column=c, columnspan=colspan, sticky=EW, padx=(0, 10), ipady=3)
                widgets.append(e)
            return widgets

        # Cedula: prefijo "V-" fijo + hasta 8 digitos
        Label(p, text="Cedula:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=1, column=0, sticky=W, pady=(6, 2))
        ced_frame = Frame(p, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        ced_frame.grid(row=2, column=0, columnspan=2, sticky=EW, padx=(0, 10))
        Label(ced_frame, text="V-", font=(FONT, 11, "bold"), bg=self.bg_card, fg=self.text).pack(side=LEFT, padx=(6, 2))
        self.input_cedula = Entry(
            ced_frame, font=(FONT, 11), relief="flat", borderwidth=0, highlightthickness=0,
            validate="key", validatecommand=(self.root.register(self._validar_cedula), "%P"))
        self.input_cedula.pack(side=LEFT, fill=X, expand=True, ipady=3)

        Label(p, text="Nombre:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=1, column=2, sticky=W, pady=(6, 2))
        self.input_nombre = Entry(p, font=(FONT, 11), relief="solid", borderwidth=1,
                                  highlightbackground=self.border, highlightthickness=1,
                                  validate="key", validatecommand=(self.root.register(self._validar_nombre), "%P"))
        self.input_nombre.grid(row=2, column=2, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)

        Label(p, text="Apellido:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=1, column=4, sticky=W, pady=(6, 2))
        self.input_apellido = Entry(p, font=(FONT, 11), relief="solid", borderwidth=1,
                                    highlightbackground=self.border, highlightthickness=1,
                                    validate="key", validatecommand=(self.root.register(self._validar_nombre), "%P"))
        self.input_apellido.grid(row=2, column=4, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)

        Label(p, text="Fecha Nacimiento:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=3, column=0, sticky=W, pady=(6, 2))
        self.input_fecha_nacimiento = self._crear_date_picker(p, on_change=self._calcular_edad)
        self.input_fecha_nacimiento.grid(row=4, column=0, columnspan=2, sticky=EW, padx=(0, 10))

        Label(p, text="Edad:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=3, column=2, sticky=W, pady=(6, 2))
        self.input_edad = Entry(p, font=(FONT, 11), relief="solid", borderwidth=1,
                                highlightbackground=self.border, highlightthickness=1,
                                state="readonly", readonlybackground=self.readonly_bg,
                                fg=self.text_sec, takefocus=0, cursor="arrow")
        self.input_edad.grid(row=4, column=2, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)

        # Operadora (prefijo) y luego Telefono (7 digitos)
        Label(p, text="Operadora:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=3, column=4, sticky=W, pady=(6, 2))
        prefijos = [op["prefijo"] for op in cargar_operadoras()]
        orden = ["412", "422", "414", "424", "416", "426"]
        prefijos = [x for x in orden if x in prefijos] + [x for x in prefijos if x not in orden]
        self.input_operadora = ttk.Combobox(p, values=prefijos, font=(FONT, 11), state="readonly", width=6)
        self.input_operadora.grid(row=4, column=4, sticky=EW, padx=(0, 10), ipady=3)

        Label(p, text="Telefono:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=3, column=5, sticky=W, pady=(6, 2))
        self.input_telefono = Entry(
            p, font=(FONT, 11), relief="solid", borderwidth=1,
            highlightbackground=self.border, highlightthickness=1,
            validate="key", validatecommand=(self.root.register(self._validar_telefono), "%P"))
        self.input_telefono.grid(row=4, column=5, sticky=EW, padx=(0, 10), ipady=3)
        self.input_telefono.bind("<FocusOut>", self._formatear_telefono_event)
        self.input_telefono.bind("<Return>", self._formatear_telefono_event)

        self.input_peso, self.input_altura = campo_fila(5, ["Peso (kg):", "Altura (m):"], colspan=2)
        self.input_peso.config(validate="key", validatecommand=(self.root.register(self._validar_peso), "%P"))
        self.input_altura.config(validate="key", validatecommand=(self.root.register(self._validar_altura), "%P"))
        self.input_peso.bind("<FocusOut>", lambda e: self._normalizar_decimal(self.input_peso))
        self.input_altura.bind("<FocusOut>", lambda e: self._normalizar_decimal(self.input_altura))
        Label(p, text="Estado Civil:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=5, column=4, sticky=W, pady=(6, 2))
        self.input_estado_civil = ttk.Combobox(p, values=valores_catalogo("estado_civil"), font=(FONT, 11), state="readonly")
        self.input_estado_civil.grid(row=6, column=4, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)

        Label(p, text="Genero:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=7, column=0, sticky=W, pady=(6, 2))
        self.input_genero = ttk.Combobox(p, values=["Masculino", "Femenino"], font=(FONT, 11), state="readonly")
        self.input_genero.grid(row=8, column=0, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)

        Label(p, text="Direccion", font=(FONT, 12, "bold"), bg=self.bg_card, fg=self.primary).grid(
            row=9, column=0, columnspan=6, sticky=W, pady=(14, 4))

        Label(p, text="Municipio:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=10, column=0, sticky=W, pady=(6, 2))
        self.input_residencia_municipio = ttk.Combobox(
            p, values=valores_catalogo("municipio"), font=(FONT, 11), state="readonly")
        self.input_residencia_municipio.grid(row=11, column=0, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)
        self.input_residencia_municipio.bind("<<ComboboxSelected>>", self._filtrar_pueblos_residencia)

        Label(p, text="Pueblo/Sector:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=10, column=2, sticky=W, pady=(6, 2))
        self.input_residencia_pueblo = ttk.Combobox(p, values=[], font=(FONT, 11), state="readonly")
        self.input_residencia_pueblo.grid(row=11, column=2, columnspan=2, sticky=EW, padx=(0, 10), ipady=3)

        Label(p, text="Direccion:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=12, column=0, sticky=W, pady=(6, 2))
        self.input_residencia = Entry(p, font=(FONT, 11), relief="solid", borderwidth=1,
                                      highlightbackground=self.border, highlightthickness=1)
        self.input_residencia.grid(row=13, column=0, columnspan=6, sticky=EW, padx=(0, 10), ipady=3)

    def _crear_tab_laborales(self):
        p = self.tab_laborales
        for i in range(4): p.grid_rowconfigure(i, pad=8)
        for i in range(4): p.grid_columnconfigure(i, weight=1, pad=15)

        Label(p, text="Datos Laborales", font=(FONT, 13, "bold"),
              bg=self.bg_card, fg=self.primary).grid(row=0, column=0, columnspan=4, sticky=W, pady=(15, 10))

        Label(p, text="Jerarquia:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=1, column=0, sticky=W, pady=(6, 2))
        self.input_jerarquia = ttk.Combobox(p, values=valores_catalogo("jerarquia"), font=(FONT, 11), state="readonly")
        self.input_jerarquia.grid(row=2, column=0, sticky=EW, padx=(0, 15), ipady=3)

        Label(p, text="Tiempo Servicio:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=1, column=1, sticky=W, pady=(6, 2))
        opciones_tiempo = [f"{n} año" if n == 1 else f"{n} años" for n in range(1, 36)]
        self.input_tiempo_servicio = ttk.Combobox(p, values=opciones_tiempo, font=(FONT, 11), state="readonly")
        self.input_tiempo_servicio.grid(row=2, column=1, sticky=EW, padx=(0, 15), ipady=3)

        Label(p, text="Lugar Servicio:", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=1, column=2, sticky=W, pady=(6, 2))
        self.input_lugar_servicio = ttk.Combobox(p, values=valores_catalogo("lugar_servicio"), font=(FONT, 11), state="readonly")
        self.input_lugar_servicio.grid(row=2, column=2, sticky=EW, padx=(0, 15), ipady=3)

        Label(p, text="Ingreso Mensual (Bs.):", font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(row=1, column=3, sticky=W, pady=(6, 2))
        self.input_ingreso_mensual = Entry(p, font=(FONT, 11), relief="solid", borderwidth=1,
                                           highlightbackground=self.border, highlightthickness=1,
                                           validate="key", validatecommand=(self.root.register(self._validar_ingreso), "%P"))
        self.input_ingreso_mensual.grid(row=2, column=3, sticky=EW, padx=(0, 15), ipady=3)
        self.input_ingreso_mensual.bind("<FocusOut>", lambda e: self._normalizar_monto_entry(self.input_ingreso_mensual))

    def _crear_tab_plan_vivienda(self):
        p = self.tab_vivienda_plan

        self.posee_terreno = StringVar(value="NO")
        self.posee_vivienda = StringVar(value="NO")
        self.necesidad_habiacion = StringVar(value="Vivienda")
        self.gestion_organismo = StringVar(value="NO")
        self.organismo_publico = StringVar(value="")
        self.organismo_privado = StringVar(value="")
        self._opciones_organismo_publico = ["Gobernacion", "INAVI", "Malariologia", "Otra"]
        self._opciones_organismo_privado = ["Entidad Bancaria", "Empresa Promotora", "Otra"]

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
        def combobox_row(parent, label, valores, es_readonly=True):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=3)
            Label(r, text=label, font=(FONT, 10), bg=self.bg_card, fg=self.text, width=20, anchor=W).pack(side=LEFT)
            cb = ttk.Combobox(r, values=valores, font=(FONT, 11), state="readonly" if es_readonly else NORMAL)
            cb.pack(side=LEFT, ipady=3, fill=X, expand=True)
            return cb

        def entry_row(parent, label):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=3)
            Label(r, text=label, font=(FONT, 10), bg=self.bg_card, fg=self.text, width=20, anchor=W).pack(side=LEFT)
            e = Entry(r, font=(FONT, 11), relief="solid", borderwidth=1,
                      highlightbackground=self.border, highlightthickness=1)
            e.pack(side=LEFT, ipady=3, fill=X, expand=True)
            return r, e

        def seccion(parent, titulo):
            f = LabelFrame(parent, text=titulo, font=(FONT, 10, "bold"),
                           bg=self.bg_card, fg=self.text, relief="groove", borderwidth=1, padx=10, pady=8)
            f.pack(fill=X, padx=15, pady=6)
            return f

        def radio_group(parent, label, var, options):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=3)
            Label(r, text=label, font=(FONT, 10), bg=self.bg_card, fg=self.text, width=20, anchor=W).pack(side=LEFT)
            botones = []
            for val in options:
                rb = Radiobutton(r, text=val, variable=var, value=val, font=(FONT, 9),
                                 bg=self.bg_card, fg=self.text, activebackground=self.bg_card,
                                 activeforeground=self.primary, selectcolor=self.bg_card)
                rb.pack(side=LEFT, padx=3)
                botones.append(rb)
            return botones

        sf = scroll_frame

        f = seccion(sf, "Terreno")
        radio_group(f, "Terreno Propio:", self.posee_terreno, ["SI", "NO"])
        
        municipios = valores_catalogo("municipio")
        self.input_municipio = combobox_row(f, "Municipio:", municipios)
        self.input_pueblo = combobox_row(f, "Pueblo/Sector:", [])
        self.input_municipio.bind("<<ComboboxSelected>>", self._filtrar_pueblos)

        f = seccion(sf, "Vivienda")
        radio_group(f, "Posee Vivienda:", self.posee_vivienda, ["SI", "NO"])
        self.input_condicion_vivienda = combobox_row(f, "Condicion:", valores_catalogo("condicion_vivienda"))

        f = seccion(sf, "Necesidad Habitacional")
        radio_group(f, "Necesidad:", self.necesidad_habiacion, ["Vivienda", "Construccion", "Sustitucion", "Mejoramiento"])

        f = seccion(sf, "Gestion Organismo Oficial")
        radio_group(f, "Gestion:", self.gestion_organismo, ["SI", "NO"])
        self._radios_organismo_publico = radio_group(
            f, "Organismo Publico:", self.organismo_publico,
            self._opciones_organismo_publico)
        self._fila_organismo_publico_otro, self.input_organismo_publico_otro = entry_row(f, "Especifique:")
        self._fila_organismo_publico_otro.pack_forget()
        self._radios_organismo_privado = radio_group(
            f, "Organismo Privado:", self.organismo_privado,
            self._opciones_organismo_privado)
        self._fila_organismo_privado_otro, self.input_organismo_privado_otro = entry_row(f, "Especifique:")
        self._fila_organismo_privado_otro.pack_forget()

        f = seccion(sf, "Fecha")
        r = Frame(f, bg=self.bg_card)
        r.pack(fill=X, pady=3)
        Label(r, text="Fecha Gestion:", font=(FONT, 10), bg=self.bg_card, fg=self.text, width=20, anchor=W).pack(side=LEFT)
        self._plan_entries["fecha_gestion"] = self._crear_date_picker(r)
        self._plan_entries["fecha_gestion"].pack(side=LEFT, ipady=3, fill=X, expand=True)

        self.input_fecha_gestion = self._plan_entries["fecha_gestion"]

        for var in (self.posee_terreno, self.posee_vivienda, self.gestion_organismo):
            var.trace_add("write", self._actualizar_dependencias_plan_vivienda)
        self.organismo_publico.trace_add("write", self._actualizar_especificaciones_organismos)
        self.organismo_privado.trace_add("write", self._actualizar_especificaciones_organismos)
        self._actualizar_dependencias_plan_vivienda()

    def _actualizar_dependencias_plan_vivienda(self, *_):
        terreno = (self.posee_terreno.get() or "").strip().upper() == "SI"
        vivienda = (self.posee_vivienda.get() or "").strip().upper() == "SI"
        gestion = (self.gestion_organismo.get() or "").strip().upper() == "SI"

        self.input_municipio.configure(state="readonly" if terreno else "disabled")
        self.input_pueblo.configure(state="readonly" if terreno else "disabled")
        self.input_condicion_vivienda.configure(state="readonly" if vivienda else "disabled")

        if not terreno:
            self.input_municipio.set("")
            self._filtrar_pueblos()
        if not vivienda:
            self.input_condicion_vivienda.set("")

        radios = (getattr(self, "_radios_organismo_publico", []) +
                  getattr(self, "_radios_organismo_privado", []))
        for rb in radios:
            rb.configure(state="normal" if gestion else "disabled")
        if not gestion:
            self.organismo_publico.set("")
            self.organismo_privado.set("")
            self._limpiar_entry(self.input_organismo_publico_otro)
            self._limpiar_entry(self.input_organismo_privado_otro)
            self.input_fecha_gestion.delete(0, END)
        self.input_fecha_gestion.set_enabled(gestion)
        self._actualizar_especificaciones_organismos()

    def _limpiar_entry(self, entrada):
        self._set_entry_text(entrada, "")

    def _set_entry_text(self, entrada, valor):
        estado = str(entrada.cget("state"))
        entrada.configure(state="normal")
        entrada.delete(0, END)
        entrada.insert(0, valor or "")
        entrada.configure(state=estado)

    def _actualizar_especificaciones_organismos(self, *_):
        gestion = (self.gestion_organismo.get() or "").strip().upper() == "SI"
        publico = (self.organismo_publico.get() or "").strip() == "Otra"
        privado = (self.organismo_privado.get() or "").strip() == "Otra"

        def _toggle(fila, entrada, visible, after=None):
            if visible and gestion:
                entrada.configure(state="normal")
                if not fila.winfo_ismapped():
                    if after is not None:
                        fila.pack(fill=X, pady=3, after=after)
                    else:
                        fila.pack(fill=X, pady=3)
            else:
                fila.pack_forget()
                entrada.configure(state="disabled")

        after_publico = self._radios_organismo_publico[0].master if self._radios_organismo_publico else None
        _toggle(self._fila_organismo_publico_otro, self.input_organismo_publico_otro, publico, after_publico)
        _toggle(self._fila_organismo_privado_otro, self.input_organismo_privado_otro, privado)

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
            Label(r, text=label, font=(FONT, 10), bg=self.bg_card, fg=self.text, width=22, anchor=W).pack(side=LEFT)
            e = Entry(r, font=(FONT, 11), relief="solid", borderwidth=1,
                      highlightbackground=self.border, highlightthickness=1)
            e.pack(side=LEFT, ipady=3, fill=X, expand=True)
            return e

        def seccion(titulo):
            f = LabelFrame(sf, text=titulo, font=(FONT, 10, "bold"),
                           bg=self.bg_card, fg=self.text, relief="groove", borderwidth=1, padx=10, pady=8)
            f.pack(fill=X, padx=15, pady=6)
            return f

        def radio_group(parent, label, var, options):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=2)
            Label(r, text=label, font=(FONT, 10), bg=self.bg_card, fg=self.text, width=22, anchor=W).pack(side=LEFT)
            for val in options:
                Radiobutton(r, text=val, variable=var, value=val, font=(FONT, 9),
                            bg=self.bg_card, fg=self.text, activebackground=self.bg_card,
                            activeforeground=self.primary, selectcolor=self.bg_card).pack(side=LEFT, padx=2)

        sf = scroll_frame
        Label(sf, text="Estado de la Vivienda", font=(FONT, 13, "bold"),
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
            Label(r, text=label, font=(FONT, 10), bg=self.bg_card, fg=self.text, width=22, anchor=W).pack(side=LEFT)
            for val in ("SI", "NO"):
                Radiobutton(r, text=val, variable=var, value=val, font=(FONT, 9),
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
            Label(r, text=label, font=(FONT, 10, "bold"), bg=self.bg_card, fg=self.text, width=22, anchor=W).pack(side=LEFT)
            for val in options:
                var = IntVar()
                Checkbutton(r, text=val, variable=var, font=(FONT, 9), bg=self.bg_card, fg=self.text,
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

    def _crear_tab_balance(self):
        p = self.tab_balance

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

        def _on_mousewheel_bal(event):
            if event.num == 4: canvas.yview_scroll(-3, "units")
            elif event.num == 5: canvas.yview_scroll(3, "units")
            else: canvas.yview_scroll(-1 * (event.delta // 120), "units")
        for w in (canvas, scroll_frame):
            w.bind("<Button-4>", _on_mousewheel_bal)
            w.bind("<Button-5>", _on_mousewheel_bal)
            w.bind("<MouseWheel>", _on_mousewheel_bal)

        sf = scroll_frame
        Label(sf, text="Balance Socio-Económico Familiar", font=(FONT, 13, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, pady=(15, 10), padx=15)

        def seccion(titulo):
            f = LabelFrame(sf, text=titulo, font=(FONT, 10, "bold"),
                           bg=self.bg_card, fg=self.text, relief="groove", borderwidth=1, padx=10, pady=8)
            f.pack(fill=X, padx=15, pady=6)
            return f

        def entry_row(parent, label):
            r = Frame(parent, bg=self.bg_card)
            r.pack(fill=X, pady=3)
            Label(r, text=label, font=(FONT, 10), bg=self.bg_card, fg=self.text, width=24, anchor=W).pack(side=LEFT)
            e = Entry(r, font=(FONT, 11), relief="solid", borderwidth=1,
                      highlightbackground=self.border, highlightthickness=1)
            e.pack(side=LEFT, ipady=3, fill=X, expand=True)
            return e

        f = seccion("Ingresos")
        self._bal_entries = {}
        self._bal_entries["ingreso_trabajador"] = entry_row(f, "Ingreso del trabajador:")
        self._bal_entries["ingreso_familiar_adicional"] = entry_row(f, "Ingreso familiar (adicional):")
        self._bal_entries["total_ingreso_familiar"] = entry_row(f, "Total ingreso familiar:")
        self._bal_entries["egreso_grupo_familiar"] = entry_row(f, "Egreso del grupo familiar:")
        self._bal_entries["disponibilidad_economica"] = entry_row(f, "Disponibilidad económica:")

        for key, val in self._bal_entries.items():
            val.insert(0, "0")
        self._bal_entries["total_ingreso_familiar"].config(state="readonly", readonlybackground=self.readonly_bg)
        self._bal_entries["disponibilidad_economica"].config(state="readonly", readonlybackground=self.readonly_bg)

        Button(f, text="Recalcular totales", font=(FONT, 9), bg=self.primary, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=self._recalcular_balance).pack(
            anchor=E, padx=5, pady=(6, 0), ipady=3)

        f = seccion("Distribución del Ingreso Real Familiar (Egresos Mensuales)")
        cols = ("Rubro", "Monto", "Observación")
        tree = ttk.Treeview(f, columns=cols, show="headings", height=15)
        tree.heading("Rubro", text="Rubro")
        tree.heading("Monto", text="Monto")
        tree.heading("Observación", text="Observación")
        tree.column("Rubro", width=220, anchor=W)
        tree.column("Monto", width=100, anchor=E)
        tree.column("Observación", width=280, anchor=W)
        tree.pack(fill=X, padx=5, pady=5)
        self._bal_tree = tree

        for rubro in RUBROS_EGRESO:
            tree.insert("", "end", iid=rubro, values=(rubro, "0", ""))

        def _editar_egreso(event=None):
            sel = tree.selection()
            if not sel:
                return
            rubro = sel[0]
            monto_actual, obs_actual = tree.item(rubro, "values")[1], tree.item(rubro, "values")[2]
            win = Toplevel(p)
            win.title(f"Egreso — {rubro}")
            win.configure(bg=self.bg_card)
            win.transient(self.root)
            win.grab_set()
            win.geometry("400x180")
            Label(win, text=rubro, font=(FONT, 12, "bold"),
                  bg=self.bg_card, fg=self.primary).pack(pady=(15, 10))
            r1 = Frame(win, bg=self.bg_card); r1.pack(fill=X, padx=15)
            Label(r1, text="Monto:", font=(FONT, 10), bg=self.bg_card, fg=self.text, width=12, anchor=W).pack(side=LEFT)
            e_monto = Entry(r1, font=(FONT, 11), relief="solid", borderwidth=1)
            e_monto.pack(side=LEFT, fill=X, expand=True, ipady=3)
            e_monto.insert(0, monto_actual)
            r2 = Frame(win, bg=self.bg_card); r2.pack(fill=X, padx=15, pady=(8, 0))
            Label(r2, text="Observación:", font=(FONT, 10), bg=self.bg_card, fg=self.text, width=12, anchor=W).pack(side=LEFT)
            e_obs = Entry(r2, font=(FONT, 11), relief="solid", borderwidth=1)
            e_obs.pack(side=LEFT, fill=X, expand=True, ipady=3)
            e_obs.insert(0, obs_actual)

            def _guardar():
                tree.item(rubro, values=(rubro, e_monto.get().strip() or "0", e_obs.get().strip()))
                self._recalcular_balance()
                win.destroy()
            Button(win, text="Guardar", font=(FONT, 10, "bold"), bg=self.success, fg="white",
                   relief="flat", borderwidth=0, cursor="hand2", command=_guardar).pack(pady=12, ipady=4)

        tree.bind("<Double-1>", _editar_egreso)
        Label(sf, text="Doble clic sobre un rubro para editar monto/observación",
              font=(FONT, 9), bg=self.bg_card, fg=self.text_sec).pack(anchor=W, padx=20, pady=(0, 15))

        self.input_ingreso_trabajador = self._bal_entries["ingreso_trabajador"]
        self.input_ingreso_familiar_adicional = self._bal_entries["ingreso_familiar_adicional"]
        self.input_total_ingreso_familiar = self._bal_entries["total_ingreso_familiar"]
        self.input_egreso_grupo_familiar = self._bal_entries["egreso_grupo_familiar"]
        self.input_disponibilidad_economica = self._bal_entries["disponibilidad_economica"]

    def _recalcular_balance(self):
        total_ingreso, egreso_total, disponibilidad = calcular_balance(
            self._bal_entries["ingreso_trabajador"].get(),
            self._bal_entries["ingreso_familiar_adicional"].get(),
            [self._bal_tree.item(iid, "values")[1] for iid in self._bal_tree.get_children()],
        )
        for key, val in (
            ("total_ingreso_familiar", total_ingreso),
            ("egreso_grupo_familiar", egreso_total),
            ("disponibilidad_economica", disponibilidad),
        ):
            entry = self._bal_entries[key]
            if key == "egreso_grupo_familiar":
                entry.config(state=NORMAL)
                entry.delete(0, END)
                entry.insert(0, str(int(val) if val == int(val) else val))
            else:
                entry.config(state=NORMAL)
                entry.delete(0, END)
                entry.insert(0, str(int(val) if val == int(val) else val))
                entry.config(state="readonly", readonlybackground=self.readonly_bg)
        # egreso del grupo familiar es editable a mano, pero lo recalculamos por defecto
        self._bal_entries["egreso_grupo_familiar"].config(state=NORMAL)

    def _crear_tab_familiares(self):
        p = self.tab_familiares
        self.familiares_panels = []

        Label(p, text="Grupo Familiar", font=(FONT, 13, "bold"),
              bg=self.bg_card, fg=self.primary).pack(anchor=W, pady=(15, 5), padx=15)
        Label(p, text="Agregue los familiares del funcionario", font=(FONT, 10),
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
                                  font=(FONT, 10), bg=self.bg_card, fg=self.text_sec)
        self.empty_label.pack(pady=30)

        footer_fam = Frame(p, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        footer_fam.pack(fill=X, padx=15, pady=(10, 15))

        Button(footer_fam, text="+ Agregar Familiar", font=(FONT, 10, "bold"), bg=self.primary, fg="white",
               activebackground=self.primary_hover, activeforeground="white", relief="flat", borderwidth=0,
               cursor="hand2", command=self.crear_nuevo_panel_familiar).pack(side=LEFT, padx=10, pady=8, ipady=5)

    def _set_combo_familiar(self, combo, valor):
        valor = (valor or "").strip()
        if valor:
            actuales = list(combo.cget("values"))
            if valor not in actuales:
                combo.configure(values=actuales + [valor])
        combo.set(valor)

    def crear_nuevo_panel_familiar(self):
        self.empty_label.pack_forget()
        idx = len(self.familiares_panels)

        card = Frame(self.familiares_container, bg=self.bg_card, highlightbackground=self.border, highlightthickness=1)
        card.pack(fill=X, pady=5)

        header = Frame(card, bg=self.primary)
        header.pack(fill=X)
        Label(header, text=f"Familiar #{idx + 1}", font=(FONT, 10, "bold"),
              bg=self.primary, fg="white", padx=10).pack(side=LEFT, pady=4)
        Button(header, text="X", font=(FONT, 9, "bold"), bg=self.danger, fg="white",
               activebackground=self.danger_hover, relief="flat", borderwidth=0, cursor="hand2",
               command=lambda i=idx: self.borrar_panel_familiar(i)).pack(side=RIGHT, padx=5, pady=2)

        body = Frame(card, bg=self.bg_card)
        body.pack(fill=X, padx=10, pady=8)

        inputs = {}

        def make_campo(fila, label, col, colspan=1):
            Label(body, text=label, font=(FONT, 9), bg=self.bg_card, fg=self.text).grid(row=fila, column=col, sticky=W, padx=(0, 2))
            e = Entry(body, font=(FONT, 10), relief="solid", borderwidth=1,
                      highlightbackground=self.border, highlightthickness=1)
            e.grid(row=fila + 1, column=col, columnspan=colspan, sticky=EW, padx=(0, 8), ipady=2)
            return e

        def make_combobox(fila, label, col, valores, colspan=1):
            Label(body, text=label, font=(FONT, 9), bg=self.bg_card, fg=self.text).grid(row=fila, column=col, sticky=W, padx=(0, 2))
            cb = ttk.Combobox(body, values=valores, font=(FONT, 10), state="readonly")
            cb.grid(row=fila + 1, column=col, columnspan=colspan, sticky=EW, padx=(0, 8), ipady=2)
            return cb

        inputs["nombre"] = make_campo(0, "Nombre:", 0)
        inputs["nombre"].config(validate="key", validatecommand=(self.root.register(self._validar_nombre), "%P"))
        inputs["apellido"] = make_campo(0, "Apellido:", 2)
        inputs["apellido"].config(validate="key", validatecommand=(self.root.register(self._validar_nombre), "%P"))
        inputs["parentesco"] = make_combobox(0, "Parentesco:", 4, valores_catalogo("parentesco"))
        inputs["edad"] = make_campo(2, "Edad:", 0)
        inputs["genero"] = make_combobox(2, "Genero:", 2, ["Masculino", "Femenino"])
        inputs["estado_civil"] = make_combobox(2, "Estado Civil:", 4, valores_catalogo("estado_civil"))
        inputs["nivel_educacion"] = make_combobox(4, "Nivel Educacion:", 0, valores_catalogo("nivel_educacion"))
        inputs["profesion"] = make_combobox(4, "Profesion:", 2, valores_catalogo("profesion"))
        inputs["lugar_trabajo"] = make_campo(4, "Lugar Trabajo:", 4)
        inputs["ingreso_mensual"] = make_campo(6, "Ingreso Mensual (Bs.):", 0)
        inputs["ingreso_mensual"].config(validate="key", validatecommand=(self.root.register(self._validar_ingreso), "%P"))
        inputs["ingreso_mensual"].bind("<FocusOut>", lambda e, w=inputs["ingreso_mensual"]: self._normalizar_monto_entry(w))
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
                                          font=(FONT, 10), bg=self.bg_card, fg=self.text_sec)
                self.empty_label.pack(pady=30)

    def _filtrar_pueblos(self, event=None):
        mun = self.input_municipio.get().strip()
        pueblos = [p["valor"] for p in cargar_catalogo("pueblo") if p["detalle"] == mun]
        self.input_pueblo.configure(values=pueblos)
        self.input_pueblo.set("")

    def _filtrar_pueblos_residencia(self, event=None):
        mun = self.input_residencia_municipio.get().strip()
        pueblos = [p["valor"] for p in cargar_catalogo("pueblo") if p["detalle"] == mun]
        self.input_residencia_pueblo.configure(values=pueblos)
        self.input_residencia_pueblo.set("")

    def guardar_funcionario(self):
        cedula = normalizar_cedula(self.input_cedula.get())
        if not cedula:
            messagebox.showwarning("Error", "La cedula es obligatoria", parent=self.root)
            return

        telefono = solo_digitos(self.input_telefono.get())
        if telefono and len(telefono) != 7:
            messagebox.showwarning("Error", "El telefono debe tener exactamente 7 digitos", parent=self.root)
            return

        if not self.editando_cedula:
            existentes = cargar_funcionarios(incluir_inactivos=True)
            for ex in existentes:
                if normalizar_cedula(ex.cedula) == cedula:
                    messagebox.showwarning("Error", f"La cedula {cedula} ya existe en el sistema", parent=self.root)
                    return

        peso = self.input_peso.get().strip().replace(",", ".")
        altura = self.input_altura.get().strip().replace(",", ".")

        f = Funcionario(
            cedula, self.input_nombre.get().strip(), self.input_apellido.get().strip(),
            self.input_fecha_nacimiento.get().strip(), self.input_edad.get().strip(),
            telefono, peso, altura, self.input_estado_civil.get().strip(),
            self.input_residencia.get().strip()
        )
        f.operadora = self.input_operadora.get().strip()
        f.genero = self.input_genero.get().strip()
        f.residencia_municipio = self.input_residencia_municipio.get().strip()
        f.residencia_pueblo = self.input_residencia_pueblo.get().strip()
        f.municipio = self.input_municipio.get().strip()
        f.pueblo = self.input_pueblo.get().strip()
        f.condicion_vivienda = self.input_condicion_vivienda.get().strip()

        f.datos_laborales(
            self.input_jerarquia.get().strip(), detalle_de_lugar(self.input_lugar_servicio.get().strip()),
            self.input_tiempo_servicio.get().strip(), self._normalizar_monto(self.input_ingreso_mensual.get())
        )
        f.plan_vivienda(
            self.posee_terreno.get(), "",
            self.input_condicion_vivienda.get().strip(),
            self.input_municipio.get().strip(), self.input_pueblo.get().strip(),
            self.necesidad_habiacion.get(),
            self.organismo_publico.get(), self.organismo_privado.get(),
            self.gestion_organismo.get(), self.input_fecha_gestion.get().strip(),
            self.input_organismo_publico_otro.get().strip() if self.organismo_publico.get() == "Otra" else "",
            self.input_organismo_privado_otro.get().strip() if self.organismo_privado.get() == "Otra" else ""
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
        f.posee_vivienda = self.posee_vivienda.get()
        f.tenencia_tierra_otra = self.input_tenencia_tierra_otra.get().strip()

        # Balance socio-económico (recalcula totales antes de guardar)
        self._recalcular_balance()
        egresos = []
        for iid in self._bal_tree.get_children():
            _, monto, obs = self._bal_tree.item(iid, "values")
            egresos.append({"rubro": iid, "monto": str(monto or "0"), "observacion": str(obs or "")})
        f.balance_socioeconomico(
            self._bal_entries["ingreso_trabajador"].get().strip() or "0",
            self._bal_entries["ingreso_familiar_adicional"].get().strip() or "0",
            self._bal_entries["total_ingreso_familiar"].get().strip() or "0",
            self._bal_entries["egreso_grupo_familiar"].get().strip() or "0",
            self._bal_entries["disponibilidad_economica"].get().strip() or "0",
            egresos,
        )

        for panel, inputs in self.familiares_panels:
            fam = Familiar(
                inputs["nombre"].get().strip(), inputs["apellido"].get().strip(),
                inputs["parentesco"].get().strip(), inputs["edad"].get().strip(),
                inputs["genero"].get().strip(), inputs["estado_civil"].get().strip(),
                inputs["nivel_educacion"].get().strip(), inputs["profesion"].get().strip(),
                inputs["lugar_trabajo"].get().strip(), self._normalizar_monto(inputs["ingreso_mensual"].get()),
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
        self.input_cedula.insert(0, solo_digitos(f.cedula)[:8])
        self.input_cedula.config(state="readonly")

        self.input_nombre.delete(0, END); self.input_nombre.insert(0, f.nombre)
        self.input_apellido.delete(0, END); self.input_apellido.insert(0, f.apellido)
        self.input_fecha_nacimiento.delete(0, END); self.input_fecha_nacimiento.insert(0, f.fecha_nacimiento)
        self._calcular_edad()

        prefijo, abonado = dividir_telefono(f.telefono)
        op_guardada = (getattr(f, "operadora", "") or "").strip()
        if not (len(op_guardada) == 3 and op_guardada.isdigit()):
            op_guardada = prefijo
        self.input_operadora.set(op_guardada)
        self.input_telefono.delete(0, END)
        self.input_telefono.insert(0, self._formatear_telefono(abonado))

        self.input_peso.delete(0, END); self.input_peso.insert(0, f.peso)
        self.input_altura.delete(0, END); self.input_altura.insert(0, f.altura)
        self.input_estado_civil.set(f.estado_civil)
        self.input_genero.set(getattr(f, "genero", "") or "")
        self.input_municipio.set(f.municipio or "")
        self._filtrar_pueblos()
        self.input_pueblo.set(f.pueblo or "")
        self.input_condicion_vivienda.set(f.condicion_vivienda or "")
        self.input_residencia.delete(0, END); self.input_residencia.insert(0, f.residencia)
        self.input_residencia_municipio.set(getattr(f, "residencia_municipio", "") or "")
        self._filtrar_pueblos_residencia()
        self.input_residencia_pueblo.set(getattr(f, "residencia_pueblo", "") or "")

        self.input_jerarquia.set(getattr(f, "jerarquia", ""))
        self.input_tiempo_servicio.set(self._normalizar_tiempo_servicio(getattr(f, "tiempo_servicio", "")))
        self.input_lugar_servicio.set(lugar_por_detalle(getattr(f, "lugar_presta_servicio", "")))
        self.input_ingreso_mensual.delete(0, END)
        self.input_ingreso_mensual.insert(0, self._normalizar_monto(getattr(f, "salario_mensual", "")))

        self.posee_terreno.set(getattr(f, "terreno_propio", "") or "NO")
        self.posee_vivienda.set(getattr(f, "posee_vivienda", "") or "NO")
        self.necesidad_habiacion.set(getattr(f, "necesidad_vivienda", "") or "Vivienda")
        self.gestion_organismo.set(getattr(f, "gestion_organismo_oficial", "") or "NO")
        self.organismo_publico.set(getattr(f, "organismo_publico", "") or "")
        self.organismo_privado.set(getattr(f, "organismo_privado", "") or "")
        self._set_entry_text(self.input_organismo_publico_otro, getattr(f, "organismo_publico_otro", "") or "")
        self._set_entry_text(self.input_organismo_privado_otro, getattr(f, "organismo_privado_otro", "") or "")
        self.input_municipio.set(f.municipio or "")
        self._filtrar_pueblos()
        self.input_pueblo.set(f.pueblo or "")
        self.input_condicion_vivienda.set(f.condicion_vivienda or "")
        self.input_fecha_gestion.delete(0, END); self.input_fecha_gestion.insert(0, f.fecha_gestion or "")
        self._actualizar_dependencias_plan_vivienda()

        self.tenencia_tierra.set(getattr(f, "tenencia_tierra", "") or "Otra")
        self.input_tenencia_tierra_otra.delete(0, END)
        self.input_tenencia_tierra_otra.insert(0, getattr(f, "tenencia_tierra_otra", "") or "")
        self._estado_entries["tiempo_ocupacion"].delete(0, END)
        self._estado_entries["tiempo_ocupacion"].insert(0, getattr(f, "tiempo_ocupacion", "") or "")

        # Restaurar ambientes desde el string "Sala:2, Sala-Comedor:1, ..."
        amb_map = {
            "Sala": "input_num_sala", "Sala-Comedor": "input_num_sala_comedor",
            "Cocina": "input_num_cocina", "Cocina-Comedor": "input_num_cocina_comedor",
            "Bano": "input_num_bano", "Dormitorios": "input_num_dormitorio",
            "Otros": "input_otros", "Especifique": "input_especificacion",
        }
        raw_amb = getattr(f, "ambiente_vivienda", "") or ""
        for part in raw_amb.split(", "):
            if ":" not in part:
                continue
            key, val = part.split(":", 1)
            attr = amb_map.get(key.strip())
            if attr:
                w = getattr(self, attr)
                w.delete(0, END)
                w.insert(0, val.strip())

        if getattr(f, "servicio_vivienda_disponible", ""):
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

        def _set_checkboxes_by_section(store, raw, section):
            if not raw:
                return
            for chunk in raw.split(" | "):
                if ":" not in chunk:
                    continue
                name, vals = chunk.split(":", 1)
                if name.strip() != section:
                    continue
                for v in vals.split(", "):
                    v = v.strip()
                    if v in store:
                        store[v].set(1)

        raw_mat = getattr(f, "materiales_vivienda", "") or ""
        _set_checkboxes_by_section(self._mat_pared_vars, raw_mat, "Pared")
        _set_checkboxes_by_section(self._mat_techo_vars, raw_mat, "Techo")
        _set_checkboxes_by_section(self._mat_piso_vars, raw_mat, "Piso")
        raw_com = getattr(f, "servicio_comunidad", "") or ""
        if raw_com:
            for v in raw_com.split(", "):
                v = v.strip()
                if v in self._mat_serv_com_vars:
                    self._mat_serv_com_vars[v].set(1)

        # Balance socio-económico
        for key in ("ingreso_trabajador", "ingreso_familiar_adicional",
                    "total_ingreso_familiar", "egreso_grupo_familiar", "disponibilidad_economica"):
            entry = self._bal_entries[key]
            entry.config(state=NORMAL)
            entry.delete(0, END)
            entry.insert(0, getattr(f, key, "0") or "0")
            if key in ("total_ingreso_familiar", "disponibilidad_economica"):
                entry.config(state="readonly", readonlybackground=self.readonly_bg)

        for iid in self._bal_tree.get_children():
            self._bal_tree.item(iid, values=(iid, "0", ""))
        for e in (getattr(f, "egresos_mensuales", None) or cargar_egresos(f.cedula)):
            rubro = e.get("rubro", "")
            if rubro in self._bal_tree.get_children() or rubro in RUBROS_EGRESO:
                if self._bal_tree.exists(rubro):
                    self._bal_tree.item(rubro, values=(rubro, e.get("monto", "0"), e.get("observacion", "")))

        for fam in f.grupo_familiar:
            self.crear_nuevo_panel_familiar()
            panel, inputs = self.familiares_panels[-1]
            inputs["nombre"].delete(0, END); inputs["nombre"].insert(0, fam.nombre)
            inputs["apellido"].delete(0, END); inputs["apellido"].insert(0, fam.apellido)
            self._set_combo_familiar(inputs["parentesco"], fam.parentesco)
            inputs["edad"].delete(0, END); inputs["edad"].insert(0, fam.edad)
            self._set_combo_familiar(inputs["genero"], fam.genero)
            self._set_combo_familiar(inputs["estado_civil"], fam.estado_civil)
            self._set_combo_familiar(inputs["nivel_educacion"], fam.nivel_educacion)
            self._set_combo_familiar(inputs["profesion"], fam.profesion_oficio)
            inputs["lugar_trabajo"].delete(0, END); inputs["lugar_trabajo"].insert(0, fam.lugar_trabajo)
            inputs["ingreso_mensual"].delete(0, END); inputs["ingreso_mensual"].insert(0, self._normalizar_monto(fam.ingreso_mensual))
            inputs["observacion"].delete(0, END); inputs["observacion"].insert(0, fam.observacion)

    def cerrar_sesion(self):
        self.usuario_actual = None
        self.usuario_rol = None
        self.funcionarios = []
        self.familiares_panels = []
        self.inicio_sesion()

    def _contar_uso_catalogo(self, tipo, valor, detalle=""):
        usados = 0
        for f in cargar_funcionarios(incluir_inactivos=True):
            if tipo == "estado_civil":
                if (f.estado_civil or "").strip().lower() == valor.lower():
                    usados += 1
            elif tipo == "jerarquia":
                if (getattr(f, "jerarquia", "") or "").strip().lower() == valor.lower():
                    usados += 1
            elif tipo == "lugar_servicio":
                actual = (getattr(f, "lugar_presta_servicio", "") or "").strip().lower()
                if actual and actual in (detalle.lower(), valor.lower()):
                    usados += 1
            elif tipo == "condicion_vivienda":
                if (getattr(f, "condicion_vivienda", "") or "").strip().lower() == valor.lower():
                    usados += 1
            elif tipo == "municipio":
                if ((getattr(f, "municipio", "") or "").strip().lower() == valor.lower()
                        or (getattr(f, "residencia_municipio", "") or "").strip().lower() == valor.lower()):
                    usados += 1
            elif tipo == "pueblo":
                if ((getattr(f, "pueblo", "") or "").strip().lower() == valor.lower()
                        or (getattr(f, "residencia_pueblo", "") or "").strip().lower() == valor.lower()):
                    usados += 1
            for fam in (getattr(f, "grupo_familiar", None) or []):
                if tipo == "parentesco":
                    if (fam.parentesco or "").strip().lower() == valor.lower():
                        usados += 1
                elif tipo == "nivel_educacion":
                    if (fam.nivel_educacion or "").strip().lower() == valor.lower():
                        usados += 1
                elif tipo == "profesion":
                    if (fam.profesion_oficio or "").strip().lower() == valor.lower():
                        usados += 1
        return usados

    def _contar_uso_operadora(self, prefijo):
        usados = 0
        for f in cargar_funcionarios(incluir_inactivos=True):
            op = (getattr(f, "operadora", "") or "").strip()
            pre, _ = dividir_telefono(getattr(f, "telefono", "") or "")
            op_valido = len(op) == 3 and op.isdigit()
            if op == prefijo or (not op_valido and pre == prefijo):
                usados += 1
        return usados

    def abrir_catalogos(self):
        win = Toplevel(self.root)
        win.title("Gestión de Catálogos")
        win.geometry("820x500")
        win.minsize(700, 440)
        win.configure(bg=self.bg_card)
        win.transient(self.root)
        win.grab_set()

        pie = Frame(win, bg=self.bg_card)
        pie.pack(side=BOTTOM, fill=X, pady=(0, 10))
        Button(pie, text="Cerrar", font=(FONT, 10), bg=self.text_sec, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=win.destroy).pack(ipady=4)

        nb = ttk.Notebook(win)
        nb.pack(fill=BOTH, expand=True, padx=10, pady=(10, 4))

        def pedir_datos(titulo, campos):
            dlg = Toplevel(win)
            dlg.title(f"Agregar a {titulo}")
            dlg.configure(bg=self.bg_card)
            dlg.transient(win)
            dlg.resizable(False, False)
            dlg.grab_set()

            entradas = {}
            for i, (clave, etiqueta) in enumerate(campos):
                Label(dlg, text=etiqueta, font=(FONT, 10), bg=self.bg_card, fg=self.text).grid(
                    row=i, column=0, sticky=W, padx=(12, 6), pady=(12 if i == 0 else 6, 2))
                entry = Entry(dlg, font=(FONT, 11), relief="solid", borderwidth=1,
                              highlightbackground=self.border, highlightthickness=1, width=32)
                entry.grid(row=i, column=1, sticky=EW, padx=(6, 12),
                           pady=(12 if i == 0 else 6, 2), ipady=3)
                entradas[clave] = entry
            dlg.grid_columnconfigure(1, weight=1)

            resultado = {"ok": False}

            def guardar():
                valores = {k: e.get().strip() for k, e in entradas.items()}
                if "valor" in valores and not valores["valor"]:
                    messagebox.showwarning("Error", "El valor es obligatorio.", parent=dlg)
                    return
                if "detalle" in valores and not valores["detalle"]:
                    messagebox.showwarning("Error", "La dirección es obligatoria.", parent=dlg)
                    return
                if "prefijo" in valores:
                    if not valores["prefijo"]:
                        messagebox.showwarning("Error", "El prefijo es obligatorio.", parent=dlg)
                        return
                    if len(valores["prefijo"]) != 3 or not valores["prefijo"].isdigit():
                        messagebox.showwarning("Error", "El prefijo debe tener exactamente 3 dígitos.", parent=dlg)
                        return
                    if not valores.get("operadora"):
                        messagebox.showwarning("Error", "El nombre de la operadora es obligatorio.", parent=dlg)
                        return
                resultado.update(valores)
                resultado["ok"] = True
                dlg.destroy()

            def cancelar():
                dlg.destroy()

            dlg.bind("<Return>", lambda e: guardar())
            dlg.bind("<Escape>", lambda e: cancelar())

            barra = Frame(dlg, bg=self.bg_card)
            barra.grid(row=len(campos), column=0, columnspan=2, sticky=EW, padx=12, pady=(8, 12))
            Button(barra, text="Guardar", font=(FONT, 10), bg=self.success, fg="white",
                   relief="flat", borderwidth=0, cursor="hand2", command=guardar).pack(
                       side=LEFT, padx=(0, 6), ipady=4)
            Button(barra, text="Cancelar", font=(FONT, 10), bg=self.text_sec, fg="white",
                   relief="flat", borderwidth=0, cursor="hand2", command=cancelar).pack(side=LEFT, ipady=4)

            entradas[list(entradas)[0]].focus_set()
            dlg.wait_window()
            try:
                win.grab_set()
            except Exception:
                pass
            return resultado if resultado["ok"] else None

        def crear_tab_catalogo(tipo, titulo):
            tab = Frame(nb, bg=self.bg_card)
            nb.add(tab, text=titulo)
            con_detalle = (tipo == "lugar_servicio")

            cols = ("valor", "detalle") if con_detalle else ("valor",)
            tree = ttk.Treeview(tab, columns=cols, show="headings", height=12)
            tree.heading("valor", text="Sede" if con_detalle else "Valor")
            if con_detalle:
                tree.heading("detalle", text="Dirección")
                tree.column("valor", width=190)
                tree.column("detalle", width=430)
            else:
                tree.column("valor", width=620)
            tree.pack(fill=BOTH, expand=True, padx=10, pady=(10, 4))

            def refrescar():
                for item in tree.get_children():
                    tree.delete(item)
                for reg in cargar_catalogo(tipo):
                    if con_detalle:
                        tree.insert("", "end", iid=reg["valor"],
                                    values=(reg["valor"], reg["detalle"] or ""))
                    else:
                        tree.insert("", "end", iid=reg["valor"], values=(reg["valor"],))

            def agregar():
                campos = ([("valor", "Valor:"), ("detalle", "Dirección:")] if con_detalle
                          else [("valor", "Valor:")])
                datos = pedir_datos(titulo, campos)
                if not datos:
                    return
                valor = datos["valor"]
                detalle = datos.get("detalle", "")
                existentes = cargar_catalogo(tipo)
                if any((r["valor"] or "").strip().lower() == valor.lower() for r in existentes):
                    messagebox.showwarning("Error", f"'{valor}' ya existe en {titulo}.", parent=win)
                    return
                if con_detalle and any((r["detalle"] or "").strip().lower() == detalle.lower()
                                       for r in existentes):
                    messagebox.showwarning("Error", "La dirección ya está registrada.", parent=win)
                    return
                try:
                    agregar_catalogo(tipo, valor, detalle)
                except Exception as e:
                    messagebox.showerror("Error", str(e), parent=win)
                    return
                registrar_auditoria(self.usuario_actual, "AGREGAR_CATALOGO", f"{tipo}: {valor}")
                refrescar()
                messagebox.showinfo("Listo", f"'{valor}' agregado.", parent=win)

            def eliminar():
                sel = tree.selection()
                if not sel:
                    messagebox.showwarning("Error", "Seleccione un valor para eliminar.", parent=win)
                    return
                valor = sel[0]
                detalle = ""
                for reg in cargar_catalogo(tipo):
                    if reg["valor"] == valor:
                        detalle = reg["detalle"] or ""
                        break
                usados = self._contar_uso_catalogo(tipo, valor, detalle)
                if usados:
                    messagebox.showwarning(
                        "No se puede eliminar",
                        f"'{valor}' está asignado a {usados} funcionario(s).\n"
                        "Cambie esos registros antes de eliminarlo.",
                        parent=win)
                    return
                if not messagebox.askyesno("Confirmar", f"¿Eliminar '{valor}'?", parent=win):
                    return
                eliminar_catalogo(tipo, valor)
                registrar_auditoria(self.usuario_actual, "ELIMINAR_CATALOGO", f"{tipo}: {valor}")
                refrescar()

            barra = Frame(tab, bg=self.bg_card)
            barra.pack(fill=X, padx=10, pady=(0, 10))
            Button(barra, text="Agregar", font=(FONT, 10), bg=self.success, fg="white",
                   relief="flat", borderwidth=0, cursor="hand2", command=agregar).pack(
                       side=LEFT, padx=(0, 6), ipady=4)
            Button(barra, text="Eliminar", font=(FONT, 10), bg=self.danger, fg="white",
                   relief="flat", borderwidth=0, cursor="hand2", command=eliminar).pack(side=LEFT, ipady=4)

            refrescar()

        crear_tab_catalogo("estado_civil", "Estado Civil")
        crear_tab_catalogo("jerarquia", "Jerarquía")
        crear_tab_catalogo("lugar_servicio", "Lugar de Servicio")
        crear_tab_catalogo("parentesco", "Parentesco")
        crear_tab_catalogo("nivel_educacion", "Nivel de Educación")
        crear_tab_catalogo("profesion", "Profesión")
        crear_tab_catalogo("condicion_vivienda", "Condición Vivienda")
        crear_tab_catalogo("municipio", "Municipios")
        crear_tab_catalogo("pueblo", "Pueblos/Sectores")

        tab_op = Frame(nb, bg=self.bg_card)
        nb.add(tab_op, text="Operadoras")
        tree_op = ttk.Treeview(tab_op, columns=("prefijo", "operadora"),
                               show="headings", height=12)
        tree_op.heading("prefijo", text="Prefijo")
        tree_op.heading("operadora", text="Operadora")
        tree_op.column("prefijo", width=120)
        tree_op.column("operadora", width=480)
        tree_op.pack(fill=BOTH, expand=True, padx=10, pady=(10, 4))

        def refrescar_op():
            for item in tree_op.get_children():
                tree_op.delete(item)
            for op in sorted(cargar_operadoras(), key=lambda x: x["prefijo"]):
                tree_op.insert("", "end", iid=op["prefijo"],
                               values=(op["prefijo"], op["operadora"]))

        def agregar_op():
            datos = pedir_datos("Operadoras", [("prefijo", "Prefijo:"), ("operadora", "Operadora:")])
            if not datos:
                return
            prefijo = datos["prefijo"]
            operadora = datos["operadora"]
            if any(op["prefijo"] == prefijo for op in cargar_operadoras()):
                messagebox.showwarning("Error", f"El prefijo {prefijo} ya existe.", parent=win)
                return
            try:
                agregar_operadora(prefijo, operadora)
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=win)
                return
            registrar_auditoria(self.usuario_actual, "AGREGAR_OPERADORA", f"{prefijo} - {operadora}")
            refrescar_op()
            messagebox.showinfo("Listo", f"Operadora {operadora} agregada.", parent=win)

        def eliminar_op():
            sel = tree_op.selection()
            if not sel:
                messagebox.showwarning("Error", "Seleccione una operadora para eliminar.", parent=win)
                return
            prefijo = sel[0]
            usados = self._contar_uso_operadora(prefijo)
            if usados:
                messagebox.showwarning(
                    "No se puede eliminar",
                    f"El prefijo {prefijo} está asignado a {usados} funcionario(s).\n"
                    "Cambie esos registros antes de eliminarlo.",
                    parent=win)
                return
            if not messagebox.askyesno("Confirmar", f"¿Eliminar el prefijo {prefijo}?", parent=win):
                return
            eliminar_operadora(prefijo)
            registrar_auditoria(self.usuario_actual, "ELIMINAR_OPERADORA", prefijo)
            refrescar_op()

        barra_op = Frame(tab_op, bg=self.bg_card)
        barra_op.pack(fill=X, padx=10, pady=(0, 10))
        Button(barra_op, text="Agregar", font=(FONT, 10), bg=self.success, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=agregar_op).pack(
                   side=LEFT, padx=(0, 6), ipady=4)
        Button(barra_op, text="Eliminar", font=(FONT, 10), bg=self.danger, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=eliminar_op).pack(side=LEFT, ipady=4)

        refrescar_op()

    def gestionar_usuarios(self):
        win = Toplevel(self.root)
        win.title("Gestión de Usuarios")
        win.geometry("500x400")
        win.configure(bg=self.bg_card)
        win.transient(self.root)
        win.grab_set()

        Label(win, text="Usuarios del Sistema", font=(FONT, 14, "bold"),
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

        Button(btn_frame, text="Agregar", font=(FONT, 10), bg=self.success, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=lambda: None).pack(side=LEFT, padx=5, ipady=4)
        Button(btn_frame, text="Eliminar", font=(FONT, 10), bg=self.danger, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=lambda: None).pack(side=LEFT, padx=5, ipady=4)
        Button(btn_frame, text="Cerrar", font=(FONT, 10), bg=self.text_sec, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=win.destroy).pack(side=RIGHT, padx=5, ipady=4)

    def ver_auditoria(self):
        win = Toplevel(self.root)
        win.title("Registro de Auditoria")
        win.geometry("700x500")
        win.configure(bg=self.bg_card)
        win.transient(self.root)
        win.grab_set()

        Label(win, text="Auditoria del Sistema", font=(FONT, 14, "bold"),
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

        Button(win, text="Cerrar", font=(FONT, 10), bg=self.text_sec, fg="white",
               relief="flat", borderwidth=0, cursor="hand2", command=win.destroy).pack(pady=(0, 15), ipady=4)


if __name__ == "__main__":
    root = Tk()
    app = UI(root)
    root.mainloop()
