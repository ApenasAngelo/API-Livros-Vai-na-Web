from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__, template_folder="../templates")


# Criar a tabela LIVROS caso não exista
def init_db():
    with sqlite3.connect("livros.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS LIVROS (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT NOT NULL,
                categoria TEXT NOT NULL,
                autor TEXT NOT NULL,
                imagem_url TEXT NOT NULL
            )
        """
        )
        conn.commit()


init_db()


# Página inicial
@app.route("/")
def home():
    return render_template("index.html")


# Rota para cadastrar um livro
@app.route("/doar", methods=["POST"])
def doar_livro():
    data = request.get_json()
    if not all(key in data for key in ("titulo", "categoria", "autor", "imagem_url")):
        return jsonify({"erro": "Todos os campos são obrigatórios."}), 400

    with sqlite3.connect("livros.db") as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            INSERT INTO LIVROS (titulo, categoria, autor, imagem_url) 
            VALUES (?, ?, ?, ?)""",
            (data["titulo"], data["categoria"], data["autor"], data["imagem_url"]),
        )
        conn.commit()

    return jsonify({"mensagem": "Livro cadastrado com sucesso!"}), 201


# Rota para listar todos os livros
@app.route("/livros", methods=["GET"])
def listar_livros():
    with sqlite3.connect("livros.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM LIVROS")
        livros = [
            {
                "id": row[0],
                "titulo": row[1],
                "categoria": row[2],
                "autor": row[3],
                "imagem_url": row[4],
            }
            for row in cursor.fetchall()
        ]

    return jsonify(livros)


# Rota para deletar um livro
@app.route("/livros/<int:livro_id>", methods=["DELETE"])
def deletar_livro(livro_id):
    with sqlite3.connect("livros.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM LIVROS WHERE id = ?", (livro_id,))
        conn.commit()

    if cursor.rowcount == 0:
        return jsonify({"erro": "Livro não encontrado"}), 400

    return jsonify({"mensagem": "Livro excluído com sucesso"}), 200


if __name__ == "__main__":
    app.run(debug=True)
