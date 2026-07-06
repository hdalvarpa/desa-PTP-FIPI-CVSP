from app import app
client = app.test_client()
with client.session_transaction() as sess:
    sess['admin'] = 'admin'
    sess['usuario_id'] = 1

response = client.get('/asignacion_ingenieros')
print(f"Status Code for /asignacion_ingenieros: {response.status_code}")
