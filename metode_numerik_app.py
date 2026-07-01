import streamlit as st
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
        fungsi_clean = fungsi_str.replace('^', '**')
        return eval(fungsi_clean, {"__builtins__": None}, konteks_aman)
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

# --- Antarmuka GUI Web Streamlit ---
st.set_page_config(page_title="Program Metode Numerik", layout="centered")

# Judul Aplikasi Web
st.title("Program Diferensial & Integral Numerik")
st.write("Disusun oleh Kelompok 5")
st.markdown("---")

# Section Input Fungsi f(x)
st.markdown("### 📝 Input Fungsi")
fungsi_input = st.text_input("Fungsi f(x):", "x**2 + 3*x")
st.caption("Tips: Gunakan `*` untuk perkalian dan `**` atau `^` untuk pangkat (contoh: x**2)")

st.markdown("---")

# Pilihan Mode Operasi
mode_var = st.radio(
    "Pilih Mode Operasi:",
    ["Diferensial (Beda Pusat)", "Integral (Trapesium)"]
)

st.markdown("---")

# Pemrosesan Parameter Berdasarkan Mode Pilihan (Dinamis & Tetap Rapi)
if mode_var == "Diferensial (Beda Pusat)":
    st.markdown("### 📐 Parameter Diferensial")
    col1, col2 = st.columns(2)
    with col1:
        x_val = st.number_input("Titik Evaluasi (x):", value=2.0, step=0.1)
    with col2:
        h_val = st.number_input("Ukuran Langkah (h):", value=0.1, step=0.01, format="%.4f")
        
    st.markdown(" ")
    btn_hitung = st.button("HITUNG SEKARANG", type="primary", use_container_width=True)
    
    st.markdown("### 📊 Hasil Perhitungan Numerik")
    if btn_hitung:
        func_str = fungsi_input.strip()
        if not func_str:
            st.error("Input fungsi f(x) tidak boleh kosong.")
        elif h_val <= 0:
            st.error("Nilai h harus lebih besar dari 0.")
        else:
            hasil = hitung_turunan(func_str, x_val, h_val)
            if hasil is not None:
                st.success(f"**Hasil Turunan (Beda Pusat):** {hasil:.6f}")
            else:
                st.error("Format penulisan fungsi salah atau tidak valid.")

else:
    st.markdown("### 📐 Parameter Integral")
    col1, col2, col3 = st.columns(3)
    with col1:
        a_val = st.number_input("Batas Bawah (a):", value=0.0, step=0.1)
    with col2:
        b_val = st.number_input("Batas Atas (b):", value=2.0, step=0.1)
    with col3:
        n_val = st.number_input("Jumlah Pias (n):", value=4, step=1)
        
    st.markdown(" ")
    btn_hitung = st.button("HITUNG SEKARANG", type="primary", use_container_width=True)
    
    st.markdown("### 📊 Hasil Perhitungan Numerik")
    if btn_hitung:
        func_str = fungsi_input.strip()
        if not func_str:
            st.error("Input fungsi f(x) tidak boleh kosong.")
        elif n_val <= 0:
            st.error("Jumlah pias (n) harus bilangan bulat > 0.")
        else:
            hasil = hitung_integral(func_str, a_val, b_val, n_val)
            if hasil is not None:
                st.success(f"**Hasil Integral (Trapesium):** {hasil:.6f}")
            else:
                st.error("Format penulisan fungsi salah atau tidak valid.")
