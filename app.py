from flask import Flask, render_template, request, send_file, redirect, url_for
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
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
    if not os.path.exists(NOMBRE_PLANTILLA):
        return "Error: No encuentro la plantilla.", 404

    try:
        # 1. RECIBIR DATOS DEL FORMULARIO
        nombre = request.form.get('nombre_cliente') or "Sin Nombre"
        ciudad = request.form.get('ciudad') or "Sin Ciudad"
        fecha = request.form.get('fecha_hoy') or "Sin Fecha"

        # 2. CREAR LA "HOJA TRANSPARENTE" (Overlay) EN MEMORIA
        packet = io.BytesIO()
        # Creamos un "lienzo" (canvas) para dibujar
        c = canvas.Canvas(packet, pagesize=A4)

        # --- DIBUJANDO EN LA PÁGINA 1 ---
        # c.drawString(X, Y, Texto) -> Recuerda: (0,0) es abajo-izquierda
        c.drawString(100, 700, f"Nombre: {nombre}")  # Arriba a la izquierda
        c.drawString(100, 680, f"Ciudad: {ciudad}")  # Un poco más abajo
        
        # Terminamos la página 1 y pasamos a la siguiente
        c.showPage() 

        # --- DIBUJANDO EN LA PÁGINA 2 ---
        c.drawString(300, 500, f"Fecha de firma: {fecha}") # En el medio aprox.
        c.drawString(300, 480, "Firmado digitalmente")
        
        # Guardamos el lienzo
        c.save()
        packet.seek(0)

        # 3. FUSIONAR EL ORIGINAL CON LO QUE DIBUJAMOS
        # Leemos el PDF que acabamos de crear en memoria
        new_pdf = PdfReader(packet)
        # Leemos la plantilla original
        existing_pdf = PdfReader(NOMBRE_PLANTILLA)
        output = PdfWriter()

        # Recorremos las páginas de la plantilla original
        # y le pegamos encima nuestra hoja transparente página por página
        for i in range(len(existing_pdf.pages)):
            page = existing_pdf.pages[i]
            
            # Si nuestra "hoja transparente" tiene contenido para esta página, lo pegamos
            if i < len(new_pdf.pages):
                page.merge_page(new_pdf.pages[i])
            
            output.add_page(page)

        # 4. GUARDAR Y ENVIAR
        output_stream = io.BytesIO()
        output.write(output_stream)
        output_stream.seek(0)

        return send_file(
            output_stream,
            as_attachment=True,
            download_name=f"Documento_{nombre}.pdf",
            mimetype='application/pdf'
        )

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)