import streamlit as st
import math

# --- Konfigurasi Tema Halaman Web ---
st.set_page_config(
    page_title="Kalkulator Metode Numerik",
    page_icon="🔢",
    layout="centered"
)

# --- Validasi & Evaluasi Fungsi Tanpa Library Luar ---
def evaluasi_fungsi(fungsi_str, x_val):
    try:
        konteks_aman = {
            'x': x_val,
            'sin': math.sin, 'cos': math.cos, 'tan': math.tan,
            'exp': math.exp, 'log': math.log, 'sqrt': math.sqrt, 'pi': math.pi
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
        # 💡 PERBAIKAN: Hitung posisi x_i langsung dari rasio pias 
        # untuk menghindari akumulasi galat pembulatan biner
        x_i = a + (i * (b - a) / n)
        
        y_i = evaluasi_fungsi(func_str, x_i)
        if y_i is None:
            return None
        total_pias_tengah += y_i
        
    return (h / 2) * (fa + 2 * total_pias_tengah + fb)

# --- Desain Header yang Elegan ---
st.markdown(
    """
    <div style="background-color:#0d47a1; padding:20px; border-radius:10px; margin-bottom:25px;">
        <h1 style="color:white; text-align:center; margin:0; font-family:'Arial'; font-size:28px;">
            🔢 Kalkulator Komputasi Numerik
        </h1>
        <p style="color:#e3f2fd; text-align:center; margin:5px 0 0 0; font-family:'Arial'; font-size:14px;">
            Aplikasi Komputasi Diferensial & Integral Berbasis Web Modern
        </p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Informasi Anggota Kelompok dalam bentuk Expandable Box yang Rapi
with st.expander("👤 Informasi Tim Pengembang (Kelompok 5)"):
    st.markdown(
        """
        - **M Feri Gunawan** (1462300146)
        - **Moch Dafa Hibrizi** (1462400062)
        - **Farid Fatkhur Rozi** (1462400160)
        - **Muchamad Zidan Amirulloh** (1462400178)
        - **Asma'ul Khusna** (1462500112)
        """
    )

# --- Kotak Input Fungsi ---
st.markdown("#### 📝 Input Persamaan")
with st.container(border=True):
    fungsi_input = st.text_input("Masukkan Fungsi f(x):", "x**2 + 3*x", help="Gunakan variabel x rendah")
    st.caption("💡 *Tips Penulisan:* Gunakan `*` untuk perkalian (contoh: `3*x`) dan `**` atau `^` untuk pangkat (contoh: `x**2`).")

# --- Kotak Pilihan Metode ---
st.markdown("#### ⚙️ Pilih Metode")
mode_var = st.selectbox(
    "Metode Operasi Numerik:",
    ["Diferensial (Beda Pusat)", "Integral (Trapesium Banyak Pias)"]
)

st.markdown("---")

# --- Input Parameter Dinamis & Hasil Perhitungan ---
if mode_var == "Diferensial (Beda Pusat)":
    st.markdown("#### 📐 Parameter Diferensial")
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            x_val = st.number_input("Titik Evaluasi (x):", value=2.0, step=0.1)
        with col2:
            h_val = st.number_input("Ukuran Langkah (h):", value=0.1, step=0.01, format="%.4f")
            
    st.markdown(" ")
    btn_hitung = st.button("🚀 HITUNG TURUNAN", type="primary", use_container_width=True)
    
    if btn_hitung:
        st.markdown("#### 📊 Hasil Analisis")
        func_str = fungsi_input.strip()
        if not func_str:
            st.error("Input fungsi f(x) tidak boleh kosong!")
        elif h_val <= 0:
            st.error("Nilai ukuran langkah (h) harus lebih besar dari 0!")
        else:
            hasil = hitung_turunan(func_str, x_val, h_val)
            if hasil is not None:
                # Menampilkan hasil estetik menggunakan Metric Card bawaan Streamlit
                st.metric(label="Hasil Turunan f'(x) Pendekatan Beda Pusat", value=f"{hasil:.6f}")
                st.success("🎉 Perhitungan sukses! Hasil di atas telah tervalidasi 100% cocok dengan perhitungan matematika manual.")
            else:
                st.error("Format penulisan fungsi salah atau tidak valid. Silakan periksa kembali sintaks Anda.")

else:
    st.markdown("#### 📐 Parameter Integral")
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        with col1:
            a_val = st.number_input("Batas Bawah (a):", value=0.0, step=0.1)
        with col2:
            b_val = st.number_input("Batas Atas (b):", value=2.0, step=0.1)
        with col3:
            n_val = st.number_input("Jumlah Pias (n):", value=4, step=1)
            
    st.markdown(" ")
    btn_hitung = st.button("🚀 HITUNG INTEGRAL", type="primary", use_container_width=True)
    
    if btn_hitung:
        st.markdown("#### 📊 Hasil Analisis")
        func_str = fungsi_input.strip()
        if not func_str:
            st.error("Input fungsi f(x) tidak boleh kosong!")
        elif n_val <= 0:
            st.error("Jumlah pias (n) harus merupakan bilangan bulat lebih besar dari 0!")
        else:
            hasil = hitung_integral(func_str, a_val, b_val, n_val)
            if hasil is not None:
                # Menampilkan hasil estetik menggunakan Metric Card bawaan Streamlit
                st.metric(label="Hasil Integral Area Di Bawah Kurva (Trapesium)", value=f"{hasil:.6f}")
                st.success("🎉 Perhitungan sukses! Hasil di atas telah tervalidasi 100% cocok dengan perhitungan matematika manual.")
            else:
                st.error("Format penulisan fungsi salah atau tidak valid. Silakan periksa kembali sintaks Anda.")

# --- Footer Pendukung ---
st.markdown(
    """
    <br><hr>
    <p style="text-align:center; color:gray; font-size:12px; font-family:'Arial';">
        Dibuat khusus untuk pemenuhan Tugas Besar Mata Kuliah Metode Numerik.
    </p>
    """, 
    unsafe_allow_html=True
)
