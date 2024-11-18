import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, ttk

# Fungsi untuk membuat database dan tabel
def create_database():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS nilai_siswa (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama_siswa TEXT,
            biologi INTEGER,
            fisika INTEGER,
            inggris INTEGER,
            prediksi_fakultas TEXT
        )
    """)
    conn.commit()
    conn.close()

# Fungsi untuk menyimpan data baru ke database
def save_to_database(nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO nilai_siswa (nama_siswa, biologi, fisika, inggris, prediksi_fakultas)
        VALUES (?, ?, ?, ?, ?)
    """, (nama, biologi, fisika, inggris, prediksi))
    conn.commit()
    conn.close()

# Fungsi untuk memperbarui data di database
def update_database(record_id, nama, biologi, fisika, inggris, prediksi):
    conn = sqlite3.connect("nilai_siswa.db")
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE nilai_siswa
        SET nama_siswa = ?, biologi = ?, fisika = ?, inggris = ?, prediksi_fakultas = ?
        WHERE id = ?
    """, (nama, biologi, fisika, inggris, prediksi, record_id))
    conn.commit()
    conn.close()

# Fungsi untuk mengambil semua data dari database
def fetch_data():
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM nilai_siswa")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Fungsi untuk menghapus data dari database
def delete_database(record_id):
    conn = sqlite3.connect('nilai_siswa.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM nilai_siswa WHERE id = ?', (record_id,))
    conn.commit()
    conn.close()

# Fungsi untuk menghitung prediksi fakultas
def calculate_prediction(biologi, fisika, inggris):
    if biologi > fisika and biologi > inggris:
        return "Kedokteran"
    elif fisika > biologi and fisika > inggris:
        return "Teknik"
    elif inggris > biologi and inggris > fisika:
        return "Bahasa"
    else:
        return "Tidak Diketahui"

# Fungsi untuk menangani tombol submit
def submit():
    try:
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise Exception("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        save_to_database(nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", f"Data berhasil disimpan!\nPrediksi Fakultas: {prediksi}")
        clear_inputs()
        populate_table()
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk menangani tombol update
def update():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk di-update!")

        record_id = int(selected_record_id.get())
        nama = nama_var.get()
        biologi = int(biologi_var.get())
        fisika = int(fisika_var.get())
        inggris = int(inggris_var.get())

        if not nama:
            raise ValueError("Nama siswa tidak boleh kosong.")

        prediksi = calculate_prediction(biologi, fisika, inggris)
        update_database(record_id, nama, biologi, fisika, inggris, prediksi)

        messagebox.showinfo("Sukses", "Data berhasil di-update!")
        clear_inputs()
        populate_table()
    except ValueError:
        messagebox.showerror("Error", "Nilai harus berupa angka.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk menangani tombol delete
def delete():
    try:
        if not selected_record_id.get():
            raise Exception("Pilih data dari tabel untuk dihapus!")

        record_id = int(selected_record_id.get())

        # Konfirmasi penghapusan
        confirm = messagebox.askyesno("Konfirmasi", "Apakah Anda yakin ingin menghapus data ini?")
        if confirm:
            delete_database(record_id)
            messagebox.showinfo("Sukses", "Data berhasil dihapus!")
            clear_inputs()
            populate_table()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# Fungsi untuk mengosongkan input
def clear_inputs():
    nama_var.set("")
    biologi_var.set("")
    fisika_var.set("")
    inggris_var.set("")
    selected_record_id.set("")

# Fungsi untuk mengisi tabel dengan data dari database
def populate_table():
    for row in table.get_children():
        table.delete(row)
    for row in fetch_data():
        table.insert('', 'end', values=row)

# Fungsi untuk menangani pemilihan data dari tabel
def on_table_select(event):
    try:
        selected_item = table.selection()[0]
        values = table.item(selected_item, "values")
        selected_record_id.set(values[0])
        nama_var.set(values[1])
        biologi_var.set(values[2])
        fisika_var.set(values[3])
        inggris_var.set(values[4])
    except IndexError:
        pass

# Inisialisasi database
create_database()

# Membuat GUI dengan tkinter
root = Tk()
root.title("Prediksi Fakultas Siswa")

# Variabel tkinter
nama_var = StringVar()
biologi_var = StringVar()
fisika_var = StringVar()
inggris_var = StringVar()
selected_record_id = StringVar()

# Elemen GUI
Label(root, text="Nama Siswa:").grid(row=0, column=0, padx=10, pady=5)
Entry(root, textvariable=nama_var).grid(row=0, column=1, padx=10, pady=5)

Label(root, text="Nilai Biologi:").grid(row=1, column=0, padx=10, pady=5)
Entry(root, textvariable=biologi_var).grid(row=1, column=1, padx=10, pady=5)

Label(root, text="Nilai Fisika:").grid(row=2, column=0, padx=10, pady=5)
Entry(root, textvariable=fisika_var).grid(row=2, column=1, padx=10, pady=5)

Label(root, text="Nilai Inggris:").grid(row=3, column=0, padx=10, pady=5)
Entry(root, textvariable=inggris_var).grid(row=3, column=1, padx=10, pady=5)

Button(root, text="Add", command=submit).grid(row=4, column=0, padx=10, pady=10)
Button(root, text="Update", command=update).grid(row=4, column=1, padx=10, pady=10)
Button(root, text="Delete", command=delete).grid(row=4, column=2, padx=10, pady=10)

# Tabel untuk menampilkan data
columns = ("id", "nama_siswa", "biologi", "fisika", "inggris", "prediksi_fakultas")
table = ttk.Treeview(root, columns=columns, show="headings")

# Menambahkan heading ke tabel
for col in columns:
    table.heading(col, text=col.capitalize())
    table.column(col, width=100)

table.grid(row=5, column=0, columnspan=3, padx=10, pady=10)
table.bind("<<TreeviewSelect>>", on_table_select)

populate_table()
root.mainloop()
