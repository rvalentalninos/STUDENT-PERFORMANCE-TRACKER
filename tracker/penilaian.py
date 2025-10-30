class Penilaian:
    """Kelas untuk menyimpan dan menghitung nilai akhir mahasiswa."""

    # Bobot: Quiz: 15%, Tugas: 25%, UTS: 25%, UAS: 35%
    BOBOT = {'quiz': 0.15, 'tugas': 0.25, 'uts': 0.25, 'uas': 0.35}

    def __init__(self, quiz=0, tugas=0, uts=0, uas=0):
        """Inisialisasi nilai-nilai, menggunakan setter untuk validasi."""
        self.quiz = quiz
        self.tugas = tugas
        self.uts = uts
        self.uas = uas

    def _validate_nilai(self, nilai):
        """Method bantu untuk validasi nilai 0-100."""
        nilai = int(nilai)
        if not (0 <= nilai <= 100):
            raise ValueError("Nilai harus antara 0 dan 100.")
        return nilai

    # --- Property & Setter untuk Quiz ---
    @property
    def quiz(self):
        return self._quiz

    @quiz.setter
    def quiz(self, nilai):
        self._quiz = self._validate_nilai(nilai)

    # --- Property & Setter untuk Tugas ---
    @property
    def tugas(self):
        return self._tugas

    @tugas.setter
    def tugas(self, nilai):
        self._tugas = self._validate_nilai(nilai)

    # --- Property & Setter untuk UTS ---
    @property
    def uts(self):
        return self._uts

    @uts.setter
    def uts(self, nilai):
        self._uts = self._validate_nilai(nilai)

    # --- Property & Setter untuk UAS ---
    @property
    def uas(self):
        return self._uas

    @uas.setter
    def uas(self, nilai):
        self._uas = self._validate_nilai(nilai)

    def nilai_akhir(self):
        """Menghitung nilai akhir dengan bobot yang ditentukan (15, 25, 25, 35)."""
        na = (self.quiz * self.BOBOT['quiz'] +
              self.tugas * self.BOBOT['tugas'] +
              self.uts * self.BOBOT['uts'] +
              self.uas * self.BOBOT['uas'])
        return round(na, 2)

    def predikat(self):
        """Menentukan predikat (huruf A-E) berdasarkan nilai akhir."""
        na = self.nilai_akhir()
        if na >= 85:
            return 'A'
        elif na >= 75:
            return 'B'
        elif na >= 65:
            return 'C'
        elif na >= 55:
            return 'D'
        else:
            return 'E'