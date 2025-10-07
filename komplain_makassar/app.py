from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "supersecretkey"  # untuk flash messages

# Konfigurasi MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'zul'
app.config['MYSQL_PASSWORD'] = 'gowa2105'
app.config['MYSQL_DB'] = 'komplain_db'

mysql = MySQL(app)

# Membuat tabel jika belum ada
with app.app_context():
    with mysql.connection.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS komplain (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nama VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                kategori VARCHAR(50) NOT NULL,
                pesan TEXT NOT NULL
            )
        """)
        mysql.connection.commit()


@app.route('/')
def index():
    with mysql.connection.cursor() as cur:
        cur.execute("SELECT * FROM komplain")
        data = cur.fetchall()
    return render_template("index.html", data=data)


@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == "POST":
        nama = request.form['nama']
        email = request.form['email']
        kategori = request.form['kategori']
        pesan = request.form['pesan']

        with mysql.connection.cursor() as cur:
            cur.execute(
                "INSERT INTO komplain (nama, email, kategori, pesan) VALUES (%s, %s, %s, %s)",
                (nama, email, kategori, pesan)
            )
            mysql.connection.commit()

        flash("Komplain berhasil ditambahkan!", "success")
        return redirect(url_for('index'))

    return render_template("form.html")


@app.route('/hapus/<int:komplain_id>')
def hapus(komplain_id):
    """Hapus komplain berdasarkan ID"""
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM komplain WHERE id = %s", (komplain_id,))
        mysql.connection.commit()

    flash("Komplain berhasil dihapus!", "danger")
    return redirect(url_for('index'))


@app.route('/batalkan')
def batalkan():
    """Hapus semua komplain"""
    with mysql.connection.cursor() as cur:
        cur.execute("DELETE FROM komplain")
        mysql.connection.commit()

    flash("Semua komplain berhasil dibatalkan!", "danger")
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
