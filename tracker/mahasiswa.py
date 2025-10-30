class Mahasiswa:
    """Kelas untuk menyimpan data profil dan kehadiran mahasiswa."""

    def __init__(self, nim, nama, hadir_persen=0.0):
        """Inisialisasi Mahasiswa."""
        self.nim = nim
        self.nama = nama
        # Menggunakan atribut tersembunyi (_) untuk enkapsulasi
        self._hadir_persen = self._validate_persen(hadir_persen)

    def _validate_persen(self, nilai):
        """Memastikan nilai persentase antara 0-100."""
        nilai = float(nilai)
        if not (0 <= nilai <= 100):
            raise ValueError("Persentase harus antara 0 dan 100.")
        return nilai

    @property
    def hadir_persen(self):
        """Properti untuk mendapatkan persentase kehadiran."""
        return self._hadir_persen

    @hadir_persen.setter
    def hadir_persen(self, nilai):
        """Setter untuk mengatur dan memvalidasi persentase kehadiran (0-100)."""
        self._hadir_persen = self._validate_persen(nilai)

    def info(self):
        """Menampilkan profil singkat mahasiswa."""
        return f"NIM: {self.nim} | Nama: {self.nama} | Kehadiran: {self.hadir_persen:.1f}%"