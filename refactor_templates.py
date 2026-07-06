import os
import re

def refactor_template(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.content = f.read()

    # Replacements
    content = content.replace('for ficha in fichas', 'for b in beneficiarios')
    content = content.replace('ficha.id_ficha', 'b.id_beneficiario_jefe')
    
    # Replace ficha.jefe.field -> b.field
    content = re.sub(r'ficha\.jefe\.([a-zA-Z0-9_]+)', r'b.\1', content)
    
    # Replace ficha.satellite -> b.satellite
    content = content.replace('ficha.predio', 'b.predio')
    content = content.replace('ficha.conyuge', 'b.conyuge')
    content = content.replace('ficha.cargas', 'b.cargas')
    content = content.replace('ficha.adicionales', 'b.adicionales')
    content = content.replace('ficha.constatacion', 'b.constatacion')
    content = content.replace('ficha.informe', 'b.informe')
    
    # Replace missing references to just ficha
    content = content.replace('ficha.fecha_registro', 'b.fecha_registro')
    content = content.replace('ficha.correo_contacto', 'b.correo_contacto')
    content = content.replace('ficha.telefono_contacto', 'b.telefono_contacto')
    
    # Entidad tecnica references
    # b.proyecto.entidades_tecnicas[0].razon_social
    content = content.replace('ficha.entidad_tecnica.razon_social', 'b.proyecto.entidades_tecnicas[0].razon_social if b.proyecto and b.proyecto.entidades_tecnicas else "N/A"')
    content = content.replace('ficha.entidad_tecnica', 'b.proyecto')

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

for tpl in ['templates/fichas.html', 'templates/usuario_matriz.html']:
    if os.path.exists(tpl):
        refactor_template(tpl)
        print(f"Refactored {tpl}")
    else:
        print(f"Not found: {tpl}")
