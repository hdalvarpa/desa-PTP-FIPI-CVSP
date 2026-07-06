import os
import re

filepath = 'app.py'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# I need to find the block for asignacion_ingenieros and replace it entirely.
old_block = """@app.route('/asignacion_ingenieros')
def listar_asignaciones():
    # Solo mostramos las asignaciones de las entidades permitidas
    entidades_permitidas = get_entidades_permitidas()
    ingenieros = Ingeniero.query.all()
    return render_template('asignacion_ingenieros.html', entidades=entidades_permitidas, ingenieros=ingenieros)

@app.route('/asignacion_ingenieros/crear', methods=['POST'])
def crear_asignacion():
    id_entidad = request.form.get('id_entidad_tecnica')
    id_ingeniero = request.form.get('id_ingeniero')
    
    try:
        entidad = EntidadTecnica.query.get_or_404(id_entidad)
        entidad.id_ingeniero_vigente = id_ingeniero
        db.session.commit()
        flash('Ingeniero asignado exitosamente a la Entidad Técnica.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al asignar ingeniero: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones'))

@app.route('/asignacion_ingenieros/eliminar/<int:id>', methods=['POST'])
def eliminar_asignacion(id):
    entidad = EntidadTecnica.query.get_or_404(id)
    try:
        entidad.id_ingeniero_vigente = None
        db.session.commit()
        flash('Ingeniero desvinculado de la Entidad Técnica.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desvincular ingeniero: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones'))"""

new_block = """from models.ingeniero_proyecto import IngenieroProyecto
from datetime import date

@app.route('/asignacion_ingenieros')
def listar_asignaciones():
    proyectos = Proyecto.query.all()
    ingenieros = Ingeniero.query.all()
    return render_template('asignacion_ingenieros.html', proyectos=proyectos, ingenieros=ingenieros)

@app.route('/asignacion_ingenieros/crear', methods=['POST'])
def crear_asignacion():
    id_proyecto = request.form.get('id_proyecto')
    id_ingeniero = request.form.get('id_ingeniero')
    
    try:
        proyecto = Proyecto.query.get_or_404(id_proyecto)
        # Validación estricta: buscar si ya existe un ingeniero activo
        if proyecto.ingeniero_actual:
            flash('El proyecto ya tiene un ingeniero activo', 'danger')
            return redirect(url_for('listar_asignaciones'))

        nueva_asignacion = IngenieroProyecto(
            id_ingeniero=id_ingeniero,
            id_proyecto=id_proyecto,
            fecha_inicio=date.today(),
            estado_activo=True
        )
        db.session.add(nueva_asignacion)
        db.session.commit()
        flash('Ingeniero asignado exitosamente al Proyecto.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al asignar ingeniero: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones'))

@app.route('/asignacion_ingenieros/eliminar/<int:id_asignacion>', methods=['POST'])
def eliminar_asignacion(id_asignacion):
    asignacion = IngenieroProyecto.query.get_or_404(id_asignacion)
    try:
        asignacion.estado_activo = False
        asignacion.fecha_fin = date.today()
        db.session.commit()
        flash('Ingeniero desvinculado del Proyecto (Historial cerrado).', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desvincular ingeniero: {str(e)}', 'danger')
        
    return redirect(url_for('listar_asignaciones'))"""

if old_block in content:
    content = content.replace(old_block, new_block)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print("app.py refactored successfully (asignacion routes)")
else:
    print("Could not find exact block in app.py")
