# tracker/rekap_kelas.py
import csv
import os
from .mahasiswa import Mahasiswa
from .penilaian import Penilaian

class RekapKelas:
    """Kelas manajer untuk mengelola data Mahasiswa dan Penilaian."""
    
    def __init__(self):
        """Inisialisasi penyimpanan data: {nim: {'mhs': obj_mhs, 'nilai': obj_nilai}}."""
        self._records = {} 

    # --- FUNGSI UTAMA MANAJEMEN DATA ---

    def tambah_mahasiswa(self, nim, nama, hadir_persen=0.0, silent=False):
        """Menambahkan objek Mahasiswa baru ke rekap."""
        if nim in self._records:
            return False 

        try:
            mhs = Mahasiswa(nim, nama, hadir_persen)
            self._records[nim] = {'mhs': mhs, 'nilai': Penilaian()}
            if not silent:
                print(f"Mahasiswa {nama} ({nim}) berhasil ditambahkan.")
            return True 
        except ValueError as e:
            if not silent:
                print(f"Gagal menambah mahasiswa: {e}")
            return False

    def set_hadir(self, nim, hadir_persen):
        """Mengatur persentase kehadiran mahasiswa tertentu."""
        if nim not in self._records:
            print(f"Error: NIM {nim} tidak ditemukan.")
            return False
        
        try:
            self._records[nim]['mhs'].hadir_persen = hadir_persen
            print(f"Kehadiran NIM {nim} diubah menjadi {hadir_persen}%.")
            return True
        except ValueError as e:
            print(f"Gagal mengatur kehadiran: {e}")
            return False

    def set_penilaian(self, nim, quiz, tugas, uts, uas, silent=False):
        """Mengatur semua nilai (quiz, tugas, uts, uas) mahasiswa tertentu."""
        if nim not in self._records:
            if not silent:
                print(f"Error: NIM {nim} tidak ditemukan.")
            return False
        
        try:
            nilai_obj = self._records[nim]['nilai']
            nilai_obj.quiz = quiz
            nilai_obj.tugas = tugas
            nilai_obj.uts = uts
            nilai_obj.uas = uas
            if not silent:
                print(f"Nilai NIM {nim} berhasil diperbarui.")
            return True
        except ValueError as e:
            if not silent:
                print(f"Gagal mengatur nilai: {e}")
            return False

    def rekap(self):
        """Menghasilkan list of dict berisi rekap data lengkap setiap mahasiswa."""
        rekap_list = []
        for nim, data in self._records.items():
            mhs_obj = data['mhs']
            nilai_obj = data['nilai']
            
            record = {
                'nim': mhs_obj.nim,
                'nama': mhs_obj.nama,
                'hadir_persen': mhs_obj.hadir_persen,
                'nilai_akhir': nilai_obj.nilai_akhir(),
                'predikat': nilai_obj.predikat()
            }
            rekap_list.append(record)
        return rekap_list
    
    # --- FUNGSI PERSISTENCE CSV (SILENT LOAD) ---

    def muat_data_csv(self, data_dir='data'):
        """Memuat data mahasiswa dari CSV secara silent saat dipanggil dari menu."""
        print("\n--- Memuat data dari CSV ---")
        
        # Reset data di memori sebelum memuat ulang
        self._records = {} 
        
        # 1. Muat Data Kehadiran (Profil Mahasiswa)
        attendance_path = os.path.join(data_dir, "attendance.csv")
        data_loaded_count = 0
        if os.path.exists(attendance_path):
            try:
                with open(attendance_path, mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        # Panggil dalam mode silent=True
                        if self.tambah_mahasiswa(nim=row['nim'], nama=row['nama'], hadir_persen=row['hadir_persen'], silent=True):
                             data_loaded_count += 1
                print(f"[SUKSES] {data_loaded_count} profil dimuat dari {attendance_path}.")
            except Exception as e:
                print(f"[ERROR] Gagal memproses {attendance_path}: {e}")
        else:
            print(f"[INFO] File {attendance_path} tidak ditemukan. Memulai dengan data kosong.")

        # 2. Muat Data Nilai (Update Nilai)
        grades_path = os.path.join(data_dir, "grades.csv")
        grades_updated_count = 0
        if os.path.exists(grades_path):
            try:
                with open(grades_path, mode='r') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        nim = row['nim']
                        if nim in self._records:
                            # Panggil dalam mode silent=True
                            if self.set_penilaian(nim=nim, quiz=row['quiz'], tugas=row['tugas'], uts=row['uts'], uas=row['uas'], silent=True):
                                grades_updated_count += 1
                    print(f"[SUKSES] {grades_updated_count} penilaian diupdate dari {grades_path}.")
            except Exception as e:
                print(f"[ERROR] Gagal memproses {grades_path}: {e}")
        else:
            print(f"[INFO] File {grades_path} tidak ditemukan.")
            
    def simpan_data_csv(self, data_dir='data'):
        """Menyimpan data mahasiswa dari memori ke attendance.csv dan grades.csv."""
        rekap_data = self.rekap()
        if not rekap_data:
            return

        os.makedirs(data_dir, exist_ok=True)
        
        # 1. Simpan Data Kehadiran
        attendance_path = os.path.join(data_dir, "attendance.csv")
        try:
            fieldnames_att = ['nim', 'nama', 'hadir_persen']
            with open(attendance_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames_att)
                writer.writeheader()
                for rec in rekap_data:
                    writer.writerow({'nim': rec['nim'], 'nama': rec['nama'], 'hadir_persen': rec['hadir_persen']})
        except Exception as e:
            print(f"[ERROR] Gagal menyimpan ke {attendance_path}: {e}")
            
        # 2. Simpan Data Nilai
        grades_path = os.path.join(data_dir, "grades.csv")
        try:
            fieldnames_grade = ['nim', 'quiz', 'tugas', 'uts', 'uas']
            with open(grades_path, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames_grade)
                writer.writeheader()
                for nim, data in self._records.items():
                    nilai_obj = data['nilai']
                    writer.writerow({
                        'nim': nim, 'quiz': nilai_obj.quiz, 'tugas': nilai_obj.tugas, 
                        'uts': nilai_obj.uts, 'uas': nilai_obj.uas
                    })
        except Exception as e:
            print(f"[ERROR] Gagal menyimpan ke {grades_path}: {e}")