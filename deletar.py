import sqlite3

conn = sqlite3.connect("clientes.db")
cursor = conn.cursor()

id_usuario = input("Digite o ID do usuário a deletar: ")

cursor.execute("SELECT COUNT(*) FROM usuarios WHERE id = ?", (id_usuario,))
existe = cursor.fetchone()[0]

if existe == 0:
    print("Usuário não encontrado")
else:
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (id_usuario,))
    conn.commit()
    print("Usuário deletado com sucesso")

conn.close()