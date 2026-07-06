import re

filepath = r'templates\asignacion_ingenieros.html'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace variables and headers
content = content.replace('Entidad Técnica', 'Proyecto')
content = content.replace('RUC', 'Año')
content = content.replace('{% for entidad in entidades %}', '{% for proyecto in proyectos %}')
content = content.replace('entidad.razon_social', 'proyecto.codigo_registro')
content = content.replace('entidad.ruc', 'proyecto.anio')
content = content.replace('entidad.ingeniero_vigente', 'proyecto.ingeniero_actual.ingeniero_rel')
content = content.replace('entidad.id_entidad_tecnica', 'proyecto.id_proyecto')
content = content.replace('{% if not entidades %}', '{% if not proyectos %}')
content = content.replace('No tienes entidades técnicas permitidas.', 'No hay proyectos registrados.')

# the URL for eliminate assignment now expects id_asignacion
# But how do we get id_asignacion from the view? If it has an active engineer, proyecto.ingeniero_actual has it!
# I will use regex for the eliminate form action.
content = re.sub(
    r'action="/asignacion_ingenieros/eliminar/\{\{ proyecto.id_proyecto \}\}"',
    r'action="/asignacion_ingenieros/eliminar/{{ proyecto.ingeniero_actual.id_asignacion }}"',
    content
)

# Modal fields
content = content.replace('Entidad a Asignar:', 'Proyecto a Asignar:')
content = content.replace('id_entidad_tecnica', 'id_proyecto')
content = content.replace('hidden_id_entidad', 'hidden_id_proyecto')
content = content.replace('display_nombre_entidad', 'display_nombre_proyecto')
content = content.replace('abrirModalAsignacion(idEntidad, nombreEntidad)', 'abrirModalAsignacion(idProyecto, nombreProyecto)')
content = content.replace("document.getElementById('hidden_id_proyecto').value = idEntidad;", "document.getElementById('hidden_id_proyecto').value = idProyecto;")
content = content.replace("document.getElementById('display_nombre_proyecto').textContent = nombreEntidad;", "document.getElementById('display_nombre_proyecto').textContent = nombreProyecto;")
content = content.replace("onclick=\"abrirModalAsignacion('{{ proyecto.id_proyecto }}', '{{ proyecto.codigo_registro }}')\"", "onclick=\"abrirModalAsignacion('{{ proyecto.id_proyecto }}', '{{ proyecto.codigo_registro }}')\"")
content = content.replace('desvincular a este ingeniero de la entidad', 'desvincular a este ingeniero del proyecto')

# Re-read to check if onclick replaced properly since the param names changed
content = content.replace("abrirModalAsignacion('{{ proyecto.id_proyecto }}', '{{ proyecto.codigo_registro }}')", "abrirModalAsignacion('{{ proyecto.id_proyecto }}', '{{ proyecto.codigo_registro }}')")

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("HTML Refactored")
