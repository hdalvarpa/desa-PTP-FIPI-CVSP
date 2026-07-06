import os
import re

models = ['predio.py', 'conyuge.py', 'carga.py', 'adicional.py', 'constatacion.py', 'informe_tecnico.py']

for m in models:
    path = os.path.join('models', m)
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace id_ficha with id_beneficiario_jefe and ForeignKey to beneficiario_jefe
        content = re.sub(
            r"id_ficha\s*=\s*db\.Column\(db\.Integer,\s*db\.ForeignKey\('fichas_inscripcion\.id_ficha',?\s*ondelete='CASCADE'\),\s*nullable=False(?:,\s*unique=True)?\)",
            "id_beneficiario_jefe = db.Column(db.Integer, db.ForeignKey('beneficiario_jefe.id_beneficiario_jefe', ondelete='CASCADE'), nullable=False)",
            content
        )
        
        # Sometimes it might not have ondelete='CASCADE' or nullable=False in the exact same order, let's just do a simpler replace:
        content = re.sub(
            r"id_ficha\s*=\s*db\.Column\(db\.Integer,\s*db\.ForeignKey\('fichas_inscripcion\.id_ficha'.*?\).*?\)",
            "id_beneficiario_jefe = db.Column(db.Integer, db.ForeignKey('beneficiario_jefe.id_beneficiario_jefe', ondelete='CASCADE'), nullable=False)",
            content
        )
        
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Refactored {m}")
    else:
        print(f"Not found {m}")
