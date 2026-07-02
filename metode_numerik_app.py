import math
import streamlit as st

# --- Konfigurasi Halaman Web ---
st.set_page_config(
    page_title="Kalkulator Metode Numerik",
    page_icon="📐",
    layout="centered"
)

# --- Validasi & Evaluasi Fungsi ---
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

# --- Header Aplikasi ---
st.title("📐 Program Diferensial & Integral Numerik")
st.write("Aplikasi pembuktian rumus metode numerik dengan penjabaran langkah substitusi nilai secara runut.")
st.markdown("---")

# --- Input Fungsi Utama ---
st.header("1. Input Fungsi Matematika")
func_str = st.text_input("Masukkan Fungsi f(x):", value="x**2 + 3*x")
st.caption("💡 **Tips Penulisan:** Gunakan `*` untuk perkalian (contoh: `3*x`), `**` atau `^` untuk pangkat (contoh: `x**2` atau `x^2`), dan fungsi matematika murni seperti `exp(x)`, `sin(x)`, `cos(x)`, `sqrt(x)`.")

# --- Pilihan Mode Operasi ---
st.header("2. Pilih Metode")
mode = st.radio(
    "Metode Komputasi:",
    ("Diferensial (Beda Pusat)", "Integral (Trapesium Banyak Pias)"),
    horizontal=True
)

st.markdown("---")
st.header("3. Parameter & Kalkulasi")

# --- Prosedur jika memilih Diferensial ---
if mode == "Diferensial (Beda Pusat)":
    col1, col2 = st.columns(2)
    with col1:
        x_val = st.number_input("Titik Evaluasi (x):", value=2.0, step=0.1, format="%.4f")
    with col2:
        h = st.number_input("Ukuran Langkah (h):", value=0.1, step=0.01, format="%.4f", min_value=0.000001)

    if st.button("HITUNG TURUNAN NOW", type="primary"):
        if not func_str.strip():
            st.error("Input fungsi f(x) tidak boleh kosong!")
        else:
            f_plus = evaluasi_fungsi(func_str, x_val + h)
            f_minus = evaluasi_fungsi(func_str, x_val - h)
            
            if f_plus is not None and f_minus is not None:
                hasil = (f_plus - f_minus) / (2 * h)
                
                # Menampilkan Hasil Utama dalam Metric Card
                st.success("Perhitungan Berhasil!")
                st.metric(label="Hasil Akhir Turunan f'(x)", value=f"{hasil:.6f}")
                
                # Menampilkan Penjabaran Langkah Singkat
                st.subheader("📝 Ringkasan Langkah Substitusi:")
                ringkasan_teks = (
                    f"[1] Evaluasi Titik Sekitar:\n"
                    f"    • f(x + h) = f({x_val} + {h}) = f({x_val + h:.4f}) = {f_plus:.6f}\n"
                    f"    • f(x - h) = f({x_val} - {h}) = f({x_val - h:.4f}) = {f_minus:.6f}\n\n"
                    f"[2] Substitusi ke Rumus Beda Pusat:\n"
                    f"    f'(x) ≈ [f(x + h) - f(x - h)] / (2 * h)\n"
                    f"    f'({x_val}) ≈ [{f_plus:.6f} - {f_minus:.6f}] / (2 * {h})\n"
                    f"    f'({x_val}) ≈ {f_plus - f_minus:.6f} / {2 * h:.4f}\n"
                    f" ───────────────────────────────────────────────\n"
                    f" Hasil Akhir Turunan = {hasil:.6f}"
                )
                st.code(ringkasan_teks, language="text")
            else:
                st.error("Format penulisan fungsi salah atau tidak valid. Silakan periksa kembali tanda kurung atau operator perkalian Anda.")

# --- Prosedur jika memilih Integral ---
elif mode == "Integral (Trapesium Banyak Pias)":
    col1, col2, col3 = st.columns(3)
    with col1:
        a = st.number_input("Batas Bawah (a):", value=0.0, step=0.1, format="%.4f")
    with col2:
        b = st.number_input("Batas Atas (b):", value=2.0, step=0.1, format="%.4f")
    with col3:
        n = st.number_input("Jumlah Pias (n):", value=4, step=1, min_value=1)

    if st.button("HITUNG INTEGRAL NOW", type="primary"):
        if not func_str.strip():
            st.error("Input fungsi f(x) tidak boleh kosong!")
        else:
            fa = evaluasi_fungsi(func_str, a)
            fb = evaluasi_fungsi(func_str, b)
            
            if fa is not None and fb is not None:
                h_langkah = (b - a) / n
                total_pias_tengah = 0
                
                for i in range(1, n):
                    # Rumus koordinat langsung rasio pias (Bebas Galat Pembulatan Biner)
                    x_i = a + (i * (b - a) / n)
                    y_i = evaluasi_fungsi(func_str, x_i)
                    if y_i is None:
                        st.error("Format fungsi mendadak tidak valid di titik tengah pias.")
                        st.stop()
                    total_pias_tengah += y_i
                    
                hasil = (h_langkah / 2) * (fa + 2 * total_pias_tengah + fb)
                
                # Menampilkan Hasil Utama dalam Metric Card
                st.success("Perhitungan Berhasil!")
                st.metric(label="Hasil Akhir Integral ∫ f(x) dx", value=f"{hasil:.6f}")
                
                # Menampilkan Penjabaran Langkah Singkat
                st.subheader("📝 Ringkasan Langkah Substitusi:")
                ringkasan_teks = (
                    f"[1] Parameter Interval Pias:\n"
                    f"    • Lebar Langkah (h) = (b - a) / n = ({b} - {a}) / {n} = {h_langkah:.4f}\n\n"
                    f"[2] Evaluasi Titik Batas & Pias Tengah:\n"
                    f"    • f(a) = f({a}) = {fa:.6f}\n"
                    f"    • f(b) = f({b}) = {fb:.6f}\n"
                    f"    • ∑ pias tengah (∑y_i) = {total_pias_tengah:.6f}  (dikali 2 = {2 * total_pias_tengah:.6f})\n\n"
                    f"[3] Substitusi ke Rumus Trapesium Komposisi:\n"
                    f"    ∫ f(x) dx ≈ (h / 2) * [f(a) + 2*(∑y_i) + f(b)]\n"
                    f"    ∫ f(x) dx ≈ ({h_langkah:.4f} / 2) * [{fa:.6f} + {2 * total_pias_tengah:.6f} + {fb:.6f}]\n"
                    f"    ∫ f(x) dx ≈ {h_langkah / 2:.4f} * [{fa + (2 * total_pias_tengah) + fb:.6f}]\n"
                    f" ───────────────────────────────────────────────\n"
                    f" Hasil Akhir Integral = {hasil:.6f}"
                )
                st.code(ringkasan_teks, language="text")
            else:
                st.error("Format penulisan fungsi salah atau tidak valid. Silakan periksa kembali.")
