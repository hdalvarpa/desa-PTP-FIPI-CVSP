from flask import Flask, render_template, request, send_file, redirect, url_for
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from datetime import datetime
import io
import os

app = Flask(__name__)

# --- CONFIGURACIÓN ---
NOMBRE_PLANTILLA = "FORMULARIO DE INSCRIPCION 2025 II.pdf"  # El nombre de tu archivo PDF real
USUARIO_ADMIN = "admin"
CLAVE_ADMIN = "1234"

@app.route('/') 
def mostrar_login():
    return render_template('login.html')

@app.route('/validar', methods=['POST'])
def login():
    if request.method == 'POST':
        usuario = request.form.get('usuario')
        password = request.form.get('password')
        
        # Validación simple
        if usuario == USUARIO_ADMIN and password == CLAVE_ADMIN:
            # ¡Aquí está el cambio! Ahora redirige al Dashboard, no al formulario directo
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Usuario o contraseña incorrectos')
    
    return render_template('login.html')

# 2. RUTA DASHBOARD (La bienvenida)
@app.route('/dashboard')
def dashboard():
    # Renderiza la página de bienvenida que hereda de base.html
    return render_template('dashboard.html')

# 3. RUTA FORMULARIO (La herramienta)
@app.route('/formulario')
def formulario():
    # Renderiza el formulario que hereda de base.html
    return render_template('formulario.html')

# 4. RUTA GENERAR PDF (La lógica pesada)
@app.route('/generar', methods=['POST'])
def generar_pdf():

# --- AGREGA ESTO AQUÍ ---
    #print("\n" + "="*30)
    #print("--- DATOS RECIBIDOS DEL FORMULARIO ---")
    #print(request.form)  # <--- ESTO ES EL CHISMOSO
    #print("="*30 + "\n")
    # ------------------------


    if not os.path.exists(NOMBRE_PLANTILLA):
        return "Error: No encuentro la plantilla (asegúrate que el nombre coincida).", 404

    try:
        #packet = io.BytesIO()
        # 1. CREAMOS EL LIENZO (CANVAS)
        packet = io.BytesIO()
        c = canvas.Canvas(packet, pagesize=A4)

        fonttype_default = "Helvetica"
        sizefont_default = 10

        c.setFont(fonttype_default, sizefont_default)
        # ==========================================
        #  PÁGINA 1: Secciones 1, 2, 3 y 4
        # ==========================================
        
        # --- 1. INFORMACIÓN DEL PREDIO ---
        # (Coordenadas inventadas, TÚ las ajustas luego)
        c.drawString(18, 482, request.form.get('direccion') or "")
        
        c.drawString(18, 454, request.form.get('departamento') or "")
        c.drawString(215, 454, request.form.get('provincia') or "")
        c.drawString(419, 454, request.form.get('distrito') or "")

        # Manzana, Lote, etc.
        c.drawString(18, 427, request.form.get('manzana') or "")
        c.drawString(115, 427, request.form.get('lote') or "")
        c.drawString(215, 427, request.form.get('sublote') or "")
        c.drawString(317, 427, request.form.get('centro_poblado') or "")
        c.drawString(419, 427, request.form.get('referencia') or "")

        # --- 2. JEFE DE FAMILIA ---
        c.drawString(18, 364, request.form.get('nombres_jefe') or "")
        c.drawString(155, 364, request.form.get('ap_paterno_jefe') or "")
        c.drawString(290, 364, request.form.get('ap_materno_jefe') or "")
        # --- RADIO BUTTONS: SITUACIÓN LABORAL JEFE ---
        sit_jefe = request.form.get('sit_laboral')
        if sit_jefe == 'Dependiente':
            c.drawString(429.8, 365, "X")
        elif sit_jefe == 'Independiente':
            c.drawString(508, 365, "X")

        c.drawString(18, 336, request.form.get('dni_jefe') or "")        
        # FECHA FORMATEADA
        fecha_nac_jefe = format_fecha(request.form.get('nacimiento_jefe'))
        c.drawString(155, 336, fecha_nac_jefe)
        c.drawString(290, 336, request.form.get('estado_civil_jefe') or "") # Select devuelve texto
        # --- RADIO BUTTONS: CONDICIÓN JEFE ---
        cond_jefe = request.form.get('condicion_eco')
        if cond_jefe == 'Formal':
            c.drawString(429.8, 337, "X")
        elif cond_jefe == 'Informal':
            c.drawString(508, 337, "X")

        c.drawString(18, 310, request.form.get('grado_instruccion') or "")
        c.drawString(155, 310, request.form.get('ocupacion') or "")
        # --- RADIO BUTTONS: DISCAPACIDAD JEFE (Aquí está la lógica de la X) ---
        disc_jefe = request.form.get('discapacidad') # Valores: 'Permanente' o 'Severa'
        if disc_jefe == 'Permanente':
            c.drawString(300.6, 309, "X")
        elif disc_jefe == 'Severa':
            c.drawString(368.6, 309, "X") 
        c.drawString(419, 310, request.form.get('ingreso_mensual') or "")

        # --- 3. CÓNYUGE (Misma lógica) ---
        c.drawString(18, 243, request.form.get('nombres_conyuge') or "")
        c.drawString(155, 243, request.form.get('ap_paterno_conyuge') or "")
        c.drawString(290, 243, request.form.get('ap_materno_conyuge') or "")
        # --- RADIO BUTTONS: SITUACIÓN LABORAL CÓNYUGE ---
        sit_conyuge = request.form.get('sit_laboral_conyuge')
        if sit_conyuge == 'Dependiente':
            c.drawString(429.8, 244, "X")
        elif sit_conyuge == 'Independiente':
            c.drawString(508, 244, "X")

        c.drawString(18, 215, request.form.get('dni_conyuge') or "")
        # Usamos la función format_fecha para que salga DD/MM/YYYY
        fecha_nac_conyuge = format_fecha(request.form.get('nacimiento_conyuge'))
        c.drawString(155, 215, fecha_nac_conyuge)
        c.drawString(290, 215, request.form.get('estado_civil_conyuge') or "")
        # ... Agrega los demás campos de texto del cónyuge aquí con sus coordenadas ...
        # Radios Cónyuge
        # --- RADIO BUTTONS: CONDICIÓN ECONÓMICA CÓNYUGE ---
        cond_conyuge = request.form.get('condicion_conyuge')
        if cond_conyuge == 'Formal':
            c.drawString(429.8, 216, "X")
        elif cond_conyuge == 'Informal':
            c.drawString(508, 216, "X")
        
        # Fila 3: Instrucción y Ocupación
        c.drawString(18, 187, request.form.get('grado_instruccion_conyuge') or "")
        c.drawString(155, 187, request.form.get('ocupacion_conyuge') or "")
        disc_conyuge = request.form.get('discapacidad_conyuge')
        if disc_conyuge == 'Permanente':
            c.drawString(300.6, 188, "X")
        elif disc_conyuge == 'Severa':
            c.drawString(368.6, 188, "X")
        # Ingreso Mensual
        c.drawString(419, 187, request.form.get('ingreso_mensual_conyuge') or "")

        # --- 4. CARGA FAMILIAR (Tabla de 3 filas) ---

        # Fila 1
        c.drawString(38, 117, request.form.get('nombres_carga_1') or "")
        c.drawString(230, 117, request.form.get('dni_carga_1') or "")
        c.drawString(288, 117, format_fecha(request.form.get('nacimiento_carga_1')))

        c.setFont("Helvetica", 7.5)
        c.drawString(365, 117, request.form.get('vinculo_carga_1') or "")

        c.setFont("Helvetica", 6.9)

        inst_1 = request.form.get('instruccion_carga_1') or ""
        inst_1 = inst_1.strip().upper()
        if inst_1 in ["SIN INSTRUCCION", "SIN INSTRUCCIÓN"]:
            c.drawString(405, 122, "SIN")         
            c.drawString(405, 114, "INSTRUCCIÓN") 
        else:
            c.drawString(405, 117, inst_1)
        
        c.setFont(fonttype_default, sizefont_default)

        disc_carga_1 = request.form.get('discapacidad_carga_1')
        if disc_carga_1 == 'Permanente':
            c.drawString(469.8, 121, "X")
        elif disc_carga_1 == 'Severa':
            c.drawString(538, 121, "X")
        
        # Fila 2
        c.drawString(38, 88, request.form.get('nombres_carga_2') or "")
        c.drawString(230, 88, request.form.get('dni_carga_2') or "")
        c.drawString(288, 88, format_fecha(request.form.get('nacimiento_carga_2')))

        c.setFont("Helvetica", 7.5)
        c.drawString(365, 88, request.form.get('vinculo_carga_2') or "")

        c.setFont("Helvetica", 6.9)

        inst_2 = request.form.get('instruccion_carga_2') or ""
        inst_2 = inst_2.strip().upper()
        if inst_2 in ["SIN INSTRUCCION", "SIN INSTRUCCIÓN"]:
            c.drawString(405, 92, "SIN")         
            c.drawString(405, 84, "INSTRUCCIÓN") 
        else:
            c.drawString(405, 88, inst_2)
        
        c.setFont(fonttype_default, sizefont_default)

            
        disc_carga_2 = request.form.get('discapacidad_carga_2')
        if disc_carga_2 == 'Permanente':
            c.drawString(469.8, 95.5, "X")
        elif disc_carga_2 == 'Severa':
            c.drawString(538, 95.5, "X")

        # Fila 3
        c.drawString(38, 61, request.form.get('nombres_carga_3') or "")
        c.drawString(230, 61, request.form.get('dni_carga_3') or "")
        c.drawString(288, 61, format_fecha(request.form.get('nacimiento_carga_3')))

        c.setFont("Helvetica", 7.5)
        c.drawString(365, 61, request.form.get('vinculo_carga_3') or "")

        c.setFont("Helvetica", 6.9)

        inst_3 = request.form.get('instruccion_carga_3') or ""
        inst_3 = inst_3.strip().upper()
        if inst_3 in ["SIN INSTRUCCION", "SIN INSTRUCCIÓN"]:
            c.drawString(405, 69, "SIN")         
            c.drawString(405, 61, "INSTRUCCIÓN") 
        else:
            c.drawString(405, 61, inst_3)

        c.setFont(fonttype_default, sizefont_default)

        disc_carga_3 = request.form.get('discapacidad_carga_3')
        if disc_carga_3 == 'Permanente':
            c.drawString(469.8, 66.5, "X")
        elif disc_carga_3 == 'Severa':
            c.drawString(538, 66.5, "X")

        # ==========================================
        #  CAMBIO DE PÁGINA (Aquí ocurre la magia)
        # ==========================================
        c.showPage() 

        c.setFont(fonttype_default, sizefont_default)
        # A partir de aquí, las coordenadas (0,0) son de la PÁGINA 2
        
        # ==========================================
        #  PÁGINA 2: Secciones 5 y 6
        # ==========================================

        # --- 5. INFORMACIÓN ADICIONAL ---
        # Recuerda: Y empieza desde abajo. 700 es arriba de la hoja 2.
        c.drawString(38, 784, request.form.get('nombres_adic_1') or "")
        c.drawString(175, 784, request.form.get('ap_paterno_adic_1') or "")
        c.drawString(275, 784, request.form.get('ap_materno_adic_1') or "")
        c.drawString(377, 784, request.form.get('dni_adic_1') or "")
        c.drawString(477, 784, request.form.get('vinculo_adic_1') or "")
        # --- 6. CONTACTO ---
        c.drawString(18, 694, request.form.get('correo_contacto') or "")
        c.drawString(305, 694, request.form.get('telefono_contacto') or "")

        # FINALIZAR
        c.save()
        packet.seek(0)

        # 2. FUSIÓN (Merge)
        new_pdf = PdfReader(packet)
        existing_pdf = PdfReader(NOMBRE_PLANTILLA)
        output = PdfWriter()

        # Recorremos las páginas del original
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            
            # Si nuestra "capa de datos" tiene esa página, la pegamos
            if i < len(new_pdf.pages):
                page.merge_page(new_pdf.pages[i])
            
            output.add_page(page)

        # 3. ENVIAR AL NAVEGADOR
        output_stream = io.BytesIO()
        output.write(output_stream)
        output_stream.seek(0)

        return send_file(
            output_stream,
            as_attachment=True,
            download_name=f"Ficha_{request.form.get('dni_jefe')}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        return f"<h1>Ocurrió un error:</h1><p>{str(e)}</p>"


def format_fecha(fecha_str):
    """Convierte YYYY-MM-DD a DD/MM/YYYY"""
    if not fecha_str:
        return ""
    try:
        fecha_obj = datetime.strptime(fecha_str, '%Y-%m-%d')
        return fecha_obj.strftime('%d/%m/%Y')
    except:
        return fecha_str # Si falla, devuelve el texto original

if __name__ == '__main__':
    app.run(debug=True)