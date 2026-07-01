import tkinter as tk
from tkinter import messagebox
import math

# --- Validasi & Evaluasi Fungsi Tanpa Library Luar ---
def evaluasi_fungsi(fungsi_str, x_val):
    try:
        konteks_aman = {
            'x': x_val,
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'exp': math.exp,
            'log': math.log,
            'sqrt': math.sqrt,
            'pi': math.pi
        }
        fungsi_bersih = fungsi_str.replace('^', '**')
        return eval(fungsi_bersih, {"__builtins__": None}, konteks_aman)
    except Exception:
        return None

# --- Logika Metode Numerik ---
def hitung_turunan(func_str, x_val, h):
    f_plus = evaluasi_fungsi(func_str, x_val + h)
    f_minus = evaluasi_fungsi(func_str, x_val - h)
    if f_plus is None or f_minus is None:
        return None
    return (f_plus - f_minus) / (2 * h)

def hitung_integral(func_str, a, b, n):
    fa = evaluasi_fungsi(func_str, a)
    fb = evaluasi_fungsi(func_str, b)
    if fa is None or fb is None:
        return None
        
    h = (b - a) / n
    total_pias_tengah = 0
    for i in range(1, n):
        x_i = a + i * h
        y_i = evaluasi_fungsi(func_str, x_i)
        if y_i is None:
            return None
        total_pias_tengah += y_i
        
    return (h / 2) * (fa + 2 * total_pias_tengah + fb)

# --- Antarmuka GUI Tkinter (Layout Tetap) ---
def proses_hitung():
    func_str = entry_fungsi.get().strip()
    if not func_str:
        messagebox.showerror("Error", "Input fungsi f(x) tidak boleh kosong.")
        return
        
    if mode_var.get() == "Diferensial":
        try:
            x_val = float(entry_x.get())
            h = float(entry_h.get())
            if h <= 0:
                messagebox.showerror("Error", "Nilai h harus lebih besar dari 0.")
                return
            hasil = hitung_turunan(func_str, x_val, h)
            if hasil is not None:
                lbl_hasil.config(text=f"Hasil Turunan (Beda Pusat):\n{hasil:.6f}", fg="#1b5e20")
            else:
                messagebox.showerror("Error", "Format penulisan fungsi salah atau tidak valid.")
        except ValueError:
            messagebox.showerror("Error", "Masukkan nilai X dan h berupa angka desimal.")
            
    elif mode_var.get() == "Integral":
        try:
            a = float(entry_a.get())
            b = float(entry_b.get())
            n = int(entry_n.get())
            if n <= 0:
                messagebox.showerror("Error", "Jumlah pias (n) harus bilangan bulat > 0.")
                return
            hasil = hitung_integral(func_str, a, b, n)
            if hasil is not None:
                lbl_hasil.config(text=f"Hasil Integral (Trapesium):\n{hasil:.6f}", fg="#1b5e20")
            else:
                messagebox.showerror("Error", "Format penulisan fungsi salah atau tidak valid.")
        except ValueError:
            messagebox.showerror("Error", "Pastikan batas A dan B adalah angka, dan N adalah bilangan bulat.")

def toggle_mode():
    if mode_var.get() == "Diferensial":
        frame_diff.pack(fill="x")
        frame_int.pack_forget()
    else:
        frame_int.pack(fill="x")
        frame_diff.pack_forget()

# Setup Window Utama
root = tk.Tk()
root.title("Tugas Metode Numerik")
root.geometry("460x480")
root.resizable(False, False)

# Judul Aplikasi
tk.Label(root, text="Program Diferensial & Integral Numerik", font=("Arial", 13, "bold"), fg="#0d47a1").pack(pady=10)

# Frame Input Fungsi f(x)
frame_umum = tk.LabelFrame(root, text=" Input Fungsi ", padx=10, pady=8, font=("Arial", 9, "bold"))
frame_umum.pack(fill="x", padx=15, pady=5)
tk.Label(frame_umum, text="Fungsi f(x):").grid(row=0, column=0, sticky="w")
entry_fungsi = tk.Entry(frame_umum, width=32, font=("Consolas", 10))
entry_fungsi.insert(0, "x**2 + 3*x")
entry_fungsi.grid(row=0, column=1, padx=10)
tk.Label(frame_umum, text="Tips: Gunakan * untuk perkalian dan ** atau ^ untuk pangkat", font=("Arial", 8, "italic"), fg="gray").grid(row=1, column=0, columnspan=2, sticky="w", pady=4)

# Pilihan Mode Operasi
frame_mode = tk.Frame(root)
frame_mode.pack(fill="x", padx=15, pady=8)
mode_var = tk.StringVar(value="Diferensial")
tk.Radiobutton(frame_mode, text="Diferensial (Beda Pusat)", variable=mode_var, value="Diferensial", command=toggle_mode, font=("Arial", 9)).pack(side="left", padx=15)
tk.Radiobutton(frame_mode, text="Integral (Trapesium)", variable=mode_var, value="Integral", command=toggle_mode, font=("Arial", 9)).pack(side="left", padx=15)

# ==========================================
# 💡 KUNCI PERBAIKAN: FRAME KONTAINER TETAP
# ==========================================
frame_kontainer_parameter = tk.Frame(root)
frame_kontainer_parameter.pack(fill="x", padx=15, pady=5)

# Parameter Mode Diferensial (dimasukkan ke dalam wadah utama)
frame_diff = tk.LabelFrame(frame_kontainer_parameter, text=" Parameter Diferensial ", padx=10, pady=10, font=("Arial", 9, "bold"))
tk.Label(frame_diff, text="Titik Evaluasi (x):").grid(row=0, column=0, sticky="w")
entry_x = tk.Entry(frame_diff, width=8)
entry_x.insert(0, "2")
entry_x.grid(row=0, column=1, padx=5)
tk.Label(frame_diff, text="Ukuran Langkah (h):").grid(row=0, column=2, sticky="w", padx=10)
entry_h = tk.Entry(frame_diff, width=8)
entry_h.insert(0, "0.1")
entry_h.grid(row=0, column=3, padx=5)

# Parameter Mode Integral (dimasukkan ke dalam wadah utama)
frame_int = tk.LabelFrame(frame_kontainer_parameter, text=" Parameter Integral ", padx=10, pady=10, font=("Arial", 9, "bold"))
tk.Label(frame_int, text="Batas Bawah (a):").grid(row=0, column=0, sticky="w")
entry_a = tk.Entry(frame_int, width=6)
entry_a.insert(0, "0")
entry_a.grid(row=0, column=1, padx=2)
tk.Label(frame_int, text="Batas Atas (b):").grid(row=0, column=2, sticky="w", padx=5)
entry_b = tk.Entry(frame_int, width=6)
entry_b.insert(0, "2")
entry_b.grid(row=0, column=3, padx=2)
tk.Label(frame_int, text="Jumlah Pias (n):").grid(row=0, column=4, sticky="w", padx=5)
entry_n = tk.Entry(frame_int, width=6)
entry_n.insert(0, "4")
entry_n.grid(row=0, column=5, padx=2)

# Set Tampilan Awal Parameter (Diferensial)
frame_diff.pack(fill="x")
# ==========================================

# Tombol Hitung (Posisinya sekarang terkunci di bawah wadah kontainer)
btn_hitung = tk.Button(root, text="HITUNG SEKARANG", font=("Arial", 11, "bold"), bg="#0d47a1", fg="white", cursor="hand2", command=proses_hitung)
btn_hitung.pack(fill="x", padx=15, pady=15)

# Output Hasil
frame_hasil = tk.LabelFrame(root, text=" Hasil Perhitungan Numerik ", padx=10, pady=10, font=("Arial", 9, "bold"))
frame_hasil.pack(fill="x", padx=15, pady=5)
lbl_hasil = tk.Label(frame_hasil, text="Hasil akan muncul di sini", font=("Consolas", 12, "bold"), fg="#333333")
lbl_hasil.pack()

root.mainloop()
