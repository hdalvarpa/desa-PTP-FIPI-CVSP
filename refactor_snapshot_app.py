import re

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 1. Admin Update (around line 1483)
# We need to extract the engineer from b.proyecto
admin_update_find = """        if not b.constatacion:
            b.constatacion = Constatacion(id_beneficiario_jefe=b.id_beneficiario_jefe)
            db.session.add(b.constatacion)
        b.constatacion.tiene_agua = (request.form.get('tiene_agua') == 'on')
        b.constatacion.tiene_saneamiento = (request.form.get('tiene_saneamiento') == 'on')

        def to_float(val):
            try: return float(val) if val else None
            except: return None

        if not b.informe:
            b.informe = InformeTecnico(id_beneficiario_jefe=b.id_beneficiario_jefe)
            db.session.add(b.informe)"""

admin_update_replace = """        # Resolver id_ingeniero actual para sellarlo
        id_ing_actual = b.proyecto.ingeniero_actual.id_ingeniero if b.proyecto and b.proyecto.ingeniero_actual else None

        if not b.constatacion:
            b.constatacion = Constatacion(id_beneficiario_jefe=b.id_beneficiario_jefe, id_ingeniero=id_ing_actual)
            db.session.add(b.constatacion)
        # Actualizamos el sello en cada edición para reflejar al ingeniero responsable de la última modificación
        b.constatacion.id_ingeniero = id_ing_actual
        b.constatacion.tiene_agua = (request.form.get('tiene_agua') == 'on')
        b.constatacion.tiene_saneamiento = (request.form.get('tiene_saneamiento') == 'on')

        def to_float(val):
            try: return float(val) if val else None
            except: return None

        if not b.informe:
            b.informe = InformeTecnico(id_beneficiario_jefe=b.id_beneficiario_jefe, id_ingeniero=id_ing_actual)
            db.session.add(b.informe)
        b.informe.id_ingeniero = id_ing_actual"""

content = content.replace(admin_update_find, admin_update_replace)


# 2. Portal Update (around line 1836)
portal_update_find = """        if not b.constatacion:
            b.constatacion = Constatacion(id_beneficiario_jefe=b.id_beneficiario_jefe)
            db.session.add(b.constatacion)
        b.constatacion.tiene_agua = (request.form.get('tiene_agua') == 'on')
        b.constatacion.tiene_saneamiento = (request.form.get('tiene_saneamiento') == 'on')

        def to_float(val):
            try: return float(val) if val else None
            except: return None

        if not b.informe:
            b.informe = InformeTecnico(id_beneficiario_jefe=b.id_beneficiario_jefe)
            db.session.add(b.informe)"""

portal_update_replace = """        # Resolver id_ingeniero actual para sellarlo
        id_ing_actual = b.proyecto.ingeniero_actual.id_ingeniero if b.proyecto and b.proyecto.ingeniero_actual else None

        if not b.constatacion:
            b.constatacion = Constatacion(id_beneficiario_jefe=b.id_beneficiario_jefe, id_ingeniero=id_ing_actual)
            db.session.add(b.constatacion)
        b.constatacion.id_ingeniero = id_ing_actual
        b.constatacion.tiene_agua = (request.form.get('tiene_agua') == 'on')
        b.constatacion.tiene_saneamiento = (request.form.get('tiene_saneamiento') == 'on')

        def to_float(val):
            try: return float(val) if val else None
            except: return None

        if not b.informe:
            b.informe = InformeTecnico(id_beneficiario_jefe=b.id_beneficiario_jefe, id_ingeniero=id_ing_actual)
            db.session.add(b.informe)
        b.informe.id_ingeniero = id_ing_actual"""

content = content.replace(portal_update_find, portal_update_replace)


# 3. Admin Create (around line 1603)
admin_create_find = """        # 6. Crear Constatacion e Informe Tecnico
        nueva_constatacion = Constatacion(
            id_beneficiario_jefe=nuevo_b.id_beneficiario_jefe,
            tiene_agua=(request.form.get('tiene_agua') == 'on'),
            tiene_saneamiento=(request.form.get('tiene_saneamiento') == 'on')
        )
        db.session.add(nueva_constatacion)

        def to_float(val):
            try: return float(val) if val else None
            except: return None

        nuevo_informe = InformeTecnico(
            id_beneficiario_jefe=nuevo_b.id_beneficiario_jefe,
            medida_frente=to_float(request.form.get('medida_frente')),"""

admin_create_replace = """        # Resolver id_ingeniero actual
        proyecto = Proyecto.query.get(id_proyecto)
        id_ing_actual = proyecto.ingeniero_actual.id_ingeniero if proyecto and proyecto.ingeniero_actual else None

        # 6. Crear Constatacion e Informe Tecnico
        nueva_constatacion = Constatacion(
            id_beneficiario_jefe=nuevo_b.id_beneficiario_jefe,
            id_ingeniero=id_ing_actual,
            tiene_agua=(request.form.get('tiene_agua') == 'on'),
            tiene_saneamiento=(request.form.get('tiene_saneamiento') == 'on')
        )
        db.session.add(nueva_constatacion)

        def to_float(val):
            try: return float(val) if val else None
            except: return None

        nuevo_informe = InformeTecnico(
            id_beneficiario_jefe=nuevo_b.id_beneficiario_jefe,
            id_ingeniero=id_ing_actual,
            medida_frente=to_float(request.form.get('medida_frente')),"""

content = content.replace(admin_create_find, admin_create_replace)


# 4. Portal Create (around line 1957)
portal_create_find = """        nueva_constatacion = Constatacion(
            id_beneficiario_jefe=nuevo_b.id_beneficiario_jefe,
            tiene_agua=(request.form.get('tiene_agua') == 'on'),
            tiene_saneamiento=(request.form.get('tiene_saneamiento') == 'on')
        )
        db.session.add(nueva_constatacion)
        
        def to_float(val):
            try: return float(val) if val else None
            except: return None
            
        nuevo_informe = InformeTecnico(
            id_beneficiario_jefe=nuevo_b.id_beneficiario_jefe,
            medida_frente=to_float(request.form.get('medida_frente')),"""

portal_create_replace = """        # Resolver id_ingeniero actual
        proyecto = Proyecto.query.get(id_proyecto)
        id_ing_actual = proyecto.ingeniero_actual.id_ingeniero if proyecto and proyecto.ingeniero_actual else None

        nueva_constatacion = Constatacion(
            id_beneficiario_jefe=nuevo_b.id_beneficiario_jefe,
            id_ingeniero=id_ing_actual,
            tiene_agua=(request.form.get('tiene_agua') == 'on'),
            tiene_saneamiento=(request.form.get('tiene_saneamiento') == 'on')
        )
        db.session.add(nueva_constatacion)
        
        def to_float(val):
            try: return float(val) if val else None
            except: return None
            
        nuevo_informe = InformeTecnico(
            id_beneficiario_jefe=nuevo_b.id_beneficiario_jefe,
            id_ingeniero=id_ing_actual,
            medida_frente=to_float(request.form.get('medida_frente')),"""

content = content.replace(portal_create_find, portal_create_replace)


# 5. Document Generation (generar_actas_web)
# This one I already modified earlier, let's update it.
doc_gen_1_find = """        # Obtener proyecto e ingeniero
        proyecto = b.proyecto
        ingeniero_asignacion = proyecto.ingeniero_actual if proyecto else None
        ingeniero = ingeniero_asignacion.ingeniero_rel if ingeniero_asignacion else None"""

doc_gen_1_replace = """        # Extraer el ingeniero SELLADO en el documento
        constatacion = Constatacion.query.filter_by(id_beneficiario_jefe=id_beneficiario).first()
        ingeniero = constatacion.ingeniero if constatacion else None"""

content = content.replace(doc_gen_1_find, doc_gen_1_replace)

# 6. Document Generation (get_contexto_documentos)
doc_gen_2_find = """    entidad = b.proyecto.entidades_tecnicas[0] if b.proyecto and b.proyecto.entidades_tecnicas else None
    proyecto = b.proyecto
    ingeniero_asignacion = proyecto.ingeniero_actual if proyecto else None
    ingeniero = ingeniero_asignacion.ingeniero_rel if ingeniero_asignacion else None
    informe = b.informe"""

doc_gen_2_replace = """    entidad = b.proyecto.entidades_tecnicas[0] if b.proyecto and b.proyecto.entidades_tecnicas else None
    informe = b.informe
    ingeniero = informe.ingeniero if informe else None"""

content = content.replace(doc_gen_2_find, doc_gen_2_replace)


with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Backend routes updated!")
