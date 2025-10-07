from flask import Flask, render_template, request, redirect, url_for, flash
from db_config import get_db, query_db

app = Flask(__name__)
app.secret_key = "secret_key_anda"

@app.route('/')
def index():
    data = query_db("SELECT * FROM komplain")
    return render_template('index.html', data=data, hide_nav_buttons=False)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        nama = request.form['nama']
        email = request.form['email']
        kategori = request.form['kategori']
        pesan = request.form['pesan']

        db = get_db()
        db.execute(
            "INSERT INTO komplain (nama, email, kategori, pesan) VALUES (?, ?, ?, ?)",
            (nama, email, kategori, pesan)
        )
        db.commit()
        flash("Komplain berhasil ditambahkan", "success")
        return redirect(url_for('index'))
    
    # hide tombol navbar di halaman tambah
    return render_template('form.html', hide_nav_buttons=True)

@app.route('/hapus/<int:komplain_id>')
def hapus(komplain_id):
    db = get_db()
    db.execute("DELETE FROM komplain WHERE id = ?", (komplain_id,))
    db.commit()
    flash("Komplain berhasil dihapus", "danger")
    return redirect(url_for('index'))

@app.route('/batalkan')
def batalkan():
    db = get_db()
    db.execute("DELETE FROM komplain")
    db.commit()
    flash("Semua komplain telah dibatalkan", "danger")
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
