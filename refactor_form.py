import os
import re

filepath = 'templates/formulario_fichas.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace ficha -> beneficiario
content = content.replace('ficha.', 'beneficiario.')
content = content.replace(' ficha ', ' beneficiario ')
content = content.replace(' if ficha ', ' if beneficiario ')
content = content.replace('ficha=', 'beneficiario=')
content = content.replace('ficha)', 'beneficiario)')
content = content.replace('(ficha ', '(beneficiario ')

# Replace jefe variables
content = content.replace('beneficiario.jefe.', 'beneficiario.')

# Replace id_ficha -> id_beneficiario_jefe in urls and variables
content = content.replace('beneficiario.id_ficha', 'beneficiario.id_beneficiario_jefe')
content = content.replace('id_ficha', 'id_beneficiario') # for url /matriz/actualizar/{{ ficha.id_ficha }} -> beneficiario.id_beneficiario_jefe wait, done above

# Proyectos mapping
content = content.replace('entidades|length', 'proyectos|length')
content = content.replace('{% for e in entidades %}', '{% for p in proyectos %}')
content = content.replace('e.id_entidad_tecnica', 'p.id_proyecto')
content = content.replace('id_entidad_tecnica', 'id_proyecto')
content = content.replace('entidades[0]', 'proyectos[0]')
content = content.replace('e.razon_social', 'p.codigo_proyecto')
content = content.replace('e.ruc', 'p.anio')
content = content.replace('Entidad Técnica', 'Proyecto')
content = content.replace('Entidad', 'Proyecto')


with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Done")
