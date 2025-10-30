# app.py

from tracker import RekapKelas, build_markdown_report, save_text # Asumsi impor dari __init__.py

def tampilkan_menu():
    """Menampilkan menu CLI."""
    print("\n" + "="*40)
    print("=== Student Performance Tracker ===")
    print("1) Muat data CSV")
    print("2) Tambah mahasiswa")
    print("3) Ubah presensi") # Keterangan Autosave ditambahkan
    print("4) Ubah nilai")
    print("5) Lihat rekapan")
    print("6) Save to (out/report.md)")
    print("7) Keluar")
    print("="*40)

def ambil_input_float(prompt, min_val=0, max_val=100):
    """Fungsi bantu untuk mengambil input angka (float) dan memvalidasinya."""
    while True:
        try:
            nilai = input(prompt).strip()
            if nilai.lower() == 'batal':
                return None
            f_nilai = float(nilai)
            if not (min_val <= f_nilai <= max_val):
                raise ValueError(f"Nilai harus antara {min_val} dan {max_val}.")
            return f_nilai
        except ValueError as e:
            print(f"Input tidak valid: {e}. Coba lagi atau ketik 'batal'.")

def main():
    """Fungsi utama untuk menjalankan aplikasi."""
    manager = RekapKelas()

    # Program memulai dengan memori kosong secara default.

    while True:
        tampilkan_menu()
        pilihan = input("Masukkan pilihan (1-7): ").strip()

        if pilihan == '1':
            # Muat Data dari CSV
            manager.muat_data_csv()
            
        elif pilihan == '2':
            # Tambah Mahasiswa (DENGAN AUTOSAVE)
            print("\n--- Tambah Mahasiswa ---")
            nim = input("Masukkan NIM: ").strip()
            nama = input("Masukkan Nama: ").strip()
            hadir = ambil_input_float("Persentase Kehadiran (0-100): ")
            
            if hadir is not None:
                if manager.tambah_mahasiswa(nim, nama, hadir):
                    # --- FITUR AUTOSAVE TAMBAH MAHASISWA ---
                    manager.simpan_data_csv()
                    print("[INFO] Data baru telah disimpan otomatis ke CSV.")
                    # --------------------------------------

        elif pilihan == '3':
            # Ubah Presensi (DENGAN AUTOSAVE)
            print("\n--- Ubah Presensi ---")
            nim = input("Masukkan NIM mahasiswa yang akan diubah: ").strip()
            hadir = ambil_input_float("Persentase Kehadiran Baru (0-100): ")
            
            if hadir is not None:
                # Panggil set_hadir dan cek apakah berhasil
                if manager.set_hadir(nim, hadir):
                    # --- FITUR AUTOSAVE DITAMBAHKAN DI SINI ---
                    manager.simpan_data_csv()
                    print("[INFO] Data presensi telah disimpan otomatis ke CSV.")
                    # ------------------------------------------

        elif pilihan == '4':
            # Ubah Nilai (DENGAN AUTOSAVE)
            print("\n--- Ubah Nilai ---")
            nim = input("Masukkan NIM mahasiswa yang akan diubah nilainya: ").strip()
            
            if nim not in manager._records:
                print(f"Error: NIM {nim} tidak ditemukan.")
                continue

            print("Masukkan nilai-nilai (0-100), atau ketik 'batal' untuk membatalkan proses:")
            
            quiz = ambil_input_float("Nilai Quiz (15%): ")
            if quiz is None: continue
            
            tugas = ambil_input_float("Nilai Tugas (25%): ")
            if tugas is None: continue
            
            uts = ambil_input_float("Nilai UTS (25%): ")
            if uts is None: continue
            
            uas = ambil_input_float("Nilai UAS (35%): ")
            if uas is None: continue

            # Panggil set_penilaian dan cek apakah berhasil
            if manager.set_penilaian(nim, quiz, tugas, uts, uas):
                # --- FITUR AUTOSAVE DITAMBAHKAN DI SINI ---
                manager.simpan_data_csv()
                print("[INFO] Data nilai telah disimpan otomatis ke CSV.")
                # ----------------------------------------
            
        elif pilihan == '5':
            # Lihat Rekap di Terminal
            rekap_data = manager.rekap()
            if not rekap_data:
                print("[INFO] Tidak ada data mahasiswa untuk ditampilkan.")
                continue
                
            print("\n--- REKAP NILAI (Terminal View) ---")
            print(f"{'NIM':<12}{'Nama':<15}{'Hadir (%)':<10}{'NA':<8}{'Predikat':<10}")
            print("="*55)
            for rec in rekap_data:
                print(f"{rec['nim']:<12}{rec['nama']:<15}{rec['hadir_persen']:<10.1f}{rec['nilai_akhir']:<8.2f}{rec['predikat']:<10}")

        elif pilihan == '6':
            # Simpan Laporan Markdown
            rekap_data = manager.rekap()
            markdown_content = build_markdown_report(rekap_data)
            save_text('out/report.md', markdown_content)
            print("[INFO] Laporan Markdown disimpan ke out/report.md.")
            
        elif pilihan == '7':
            # Keluar
            print("Terima kasih, program dihentikan.")
            break
        
        else:
            print("Pilihan tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    main()