class Funcionario():
	def __init__(self,cedula,nombre,apellido,fecha_nacimiento,edad,telefono,peso,altura,estado_civil,residencia):
		self.cedula=cedula
		self.nombre=nombre
		self.apellido=apellido
		self.fecha_nacimiento=fecha_nacimiento
		self.edad=edad
		self.telefono=telefono
		self.peso=peso
		self.altura=altura
		self.estado_civil=estado_civil
		self.residencia=residencia

		self.grupo_familiar=[]

	def agregar_familiar(self,familiar):
		self.grupo_familiar.append(familiar)

	def datos_laborales(self, jerarquia,lugar_presta_servicvio,tiempo_servicio,salario_mensual):
		self.jerarquia=jerarquia
		self.lugar_presta_servicvio=lugar_presta_servicvio
		self.tiempo_servicio=tiempo_servicio
		self.salario_mensual=salario_mensual

	def plan_vivienda(self,terreno_propio,ubicacion_terreno,condicion_vivienda,necesidad_vivienda,organismo_publico,organismo_privado,gestion_organismo_oficial,fecha_gestion):
		self.terreno_propio=terreno_propio
		self.ubicacion_terreno=ubicacion_terreno
		self.condicion_vivienda=condicion_vivienda
		self.necesidad_vivienda=necesidad_vivienda
		self.gestion_organismo_oficial=gestion_organismo_oficial
		self.organismo_publico=organismo_publico
		self.organismo_privado=organismo_privado
		self.fecha_gestion=fecha_gestion

	def estado_vivienda(self,tenencia_tierra,ambiente_vivienda,tiempo_ocupacion,servicio_vivienda_disponible,materiales_vivienda,servicio_comunidad):
		self.tenencia_tierra=tenencia_tierra
		self.ambiente_vivienda=ambiente_vivienda
		self.tiempo_ocupacion=tiempo_ocupacion
		self.servicio_vivienda_disponible=servicio_vivienda_disponible
		self.materiales_vivienda=materiales_vivienda
		self.servicio_comunidad=servicio_comunidad

class Familiar():
	def __init__(self,nombre,apellido,parentesco,edad,genero,estado_civil,nivel_educacion,profesion_oficio,lugar_trabajo,ingreso_mensual,observacion):
		self.nombre=nombre
		self.apellido=apellido
		self.parentesco=parentesco
		self.edad=edad
		self.genero=genero
		self.estado_civil=estado_civil
		self.nivel_educacion=nivel_educacion
		self.profesion_oficio=profesion_oficio
		self.lugar_trabajo=lugar_trabajo
		self.ingreso_mensual=ingreso_mensual
		self.observacion=observacion
