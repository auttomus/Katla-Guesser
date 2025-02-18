from collections import Counter
from typing import Set, List, Dict, Tuple, Optional

def load_wordlist(filename: str) -> Set[str]:
    """
    Memuat wordlist dari file.
    Hanya mengambil kata yang terdiri dari 5 huruf dan mengonversinya ke huruf besar.
    """
    with open(filename, encoding="utf8") as file:
        return {line.strip().upper() for line in file if len(line.strip()) == 5}

def is_candidate_valid(candidate: str, must_not: Set[str], min_counts: Dict[str, int],
                         max_counts: Dict[str, int], must_in: Dict[int, str],
                         must_not_in: Dict[int, Set[str]]) -> bool:
    """
    Memvalidasi apakah kandidat memenuhi kriteria:
      1. Tidak mengandung huruf yang dilarang (must_not).
      2. Mengandung tiap huruf dengan frekuensi minimal sesuai min_counts.
      3. Tidak melebihi frekuensi maksimal sesuai max_counts.
      4. Memenuhi syarat posisi hijau (must_in) – huruf harus ada di posisi yang tepat.
      5. Memenuhi syarat posisi kuning (must_not_in) – huruf tidak boleh ada di posisi tertentu.
    """
    candidate = candidate.upper()
    
    # 1. Cek huruf yang tidak boleh ada
    if must_not & set(candidate):
        return False

    candidate_counts = Counter(candidate)
    
    # 2. Cek frekuensi huruf minimal
    for letter, required in min_counts.items():
        if candidate_counts.get(letter, 0) < required:
            return False

    # 3. Cek frekuensi huruf maksimal
    for letter, max_val in max_counts.items():
        if candidate_counts.get(letter, 0) > max_val:
            return False

    # 4. Cek posisi hijau (harus tepat)
    for pos, letter in must_in.items():
        if candidate[pos] != letter:
            return False

    # 5. Cek posisi kuning (tidak boleh ada di posisi tertentu)
    for pos, letters in must_not_in.items():
        if candidate[pos] in letters:
            return False

    return True

def filter_words(wordlist: Set[str], must_not: Set[str], min_counts: Dict[str, int],
                 max_counts: Dict[str, int], must_in: Dict[int, str],
                 must_not_in: Dict[int, Set[str]]) -> Set[str]:
    """
    Menyaring wordlist berdasarkan kriteria yang diberikan.
    """
    return {
        word for word in wordlist
        if is_candidate_valid(word, must_not, min_counts, max_counts, must_in, must_not_in)
    }

class KatlaGame:
    """
    Kelas KatlaGame mengelola permainan menebak kata.
    Informasi dari setiap tebakan (kriteria eliminasi) diingat untuk kesempatan berikutnya.
    """
    def __init__(self, wordlist_file: str):
        self.full_wordlist = load_wordlist(wordlist_file)
        self.candidates = self.full_wordlist.copy()
        self.must_not: Set[str] = set()           # Huruf yang tidak boleh ada
        self.min_counts: Dict[str, int] = {}        # Minimal frekuensi tiap huruf (dari status kuning/hijau)
        self.max_counts: Dict[str, int] = {}        # Maksimal frekuensi tiap huruf (dibatasi oleh feedback tebakan)
        self.must_in: Dict[int, str] = {}           # Huruf yang harus ada di posisi tertentu (hijau)
        self.must_not_in: Dict[int, Set[str]] = {}    # Huruf yang tidak boleh ada di posisi tertentu (kuning)

    def _calculate_positive_frequency(self, guess_word: str, statuses: List[int]) -> Dict[str, int]:
        """
        Menghitung frekuensi huruf dengan status positif (1 dan 2) dari tebakan.
        """
        positive_freq: Dict[str, int] = {}
        for letter, status in zip(guess_word, statuses):
            if status in (1, 2):
                positive_freq[letter] = positive_freq.get(letter, 0) + 1
        return positive_freq

    def update_criteria(self, guess_word: str, statuses: List[int]) -> None:
        """
        Memperbarui kriteria eliminasi berdasarkan tebakan.
        
        Proses:
          1. Ubah guess_word ke uppercase.
          2. Hitung frekuensi positif (status 1 dan 2) dan total frekuensi huruf dalam tebakan.
          3. Update min_counts untuk tiap huruf dengan nilai maksimum antara nilai yang sudah ada dan
             frekuensi positif tebakan ini.
          4. Update max_counts: Jika terdapat huruf dengan status 0 (tidak muncul secara positif) dalam tebakan,
             maka batas maksimalnya adalah jumlah kemunculan positif.
          5. Update must_in dan must_not_in berdasarkan posisi dan status huruf.
          6. Untuk status 0, jika huruf belum pernah muncul secara positif, tambahkan ke must_not.
        """
        guess_word = guess_word.upper()
        positive_freq = self._calculate_positive_frequency(guess_word, statuses)

        total_freq: Dict[str, int] = {}
        for letter in guess_word:
            total_freq[letter] = total_freq.get(letter, 0) + 1

        # Update minimal counts: ambil nilai maksimum antara yang sudah ada dan frekuensi positif tebakan ini.
        for letter, freq in positive_freq.items():
            self.min_counts[letter] = max(self.min_counts.get(letter, 0), freq)

        # Update maximal counts:
        for letter, total in total_freq.items():
            if letter in positive_freq and total > positive_freq[letter]:
                self.max_counts[letter] = positive_freq[letter]
            else:
                self.max_counts[letter] = total

        # Update posisi berdasarkan status tiap huruf
        for pos, (letter, status) in enumerate(zip(guess_word, statuses)):
            if status == 2:
                self.must_in[pos] = letter
            elif status == 1:
                self.must_not_in.setdefault(pos, set()).add(letter)
            elif status == 0 and letter not in self.min_counts:
                self.must_not.add(letter)

    def filter_candidates(self) -> None:
        """
        Menyaring kandidat berdasarkan kriteria terkini.
        """
        self.candidates = filter_words(self.candidates, self.must_not,
                                       self.min_counts, self.max_counts,
                                       self.must_in, self.must_not_in)

    def print_state(self) -> None:
        """
        Mencetak kriteria eliminasi dan jumlah kandidat tersisa.
        """
        print("\nKriteria Saat Ini:")
        print("  Must Not:", self.must_not)
        print("  Minimal Counts:", self.min_counts)
        print("  Maximal Counts:", self.max_counts)
        print("  Must In (posisi tepat):", self.must_in)
        print("  Must Not In (posisi terlarang):", self.must_not_in)
        print("  Kandidat Tersisa:", len(self.candidates))

    def _get_user_guess(self) -> Tuple[Optional[str], Optional[List[int]]]:
        """
        Membaca input tebakan dari pengguna.
        Mengembalikan tuple (guess_word, statuses) atau (None, None) jika input tidak valid.
        """
        guess_word = input("Masukkan kata tebakan Anda (5 huruf): ").strip().upper()
        if len(guess_word) != 5:
            print("Panjang kata harus 5 huruf. Silakan coba lagi.")
            return None, None

        statuses_str = input("Masukkan status untuk tiap huruf (0=abu, 1=kuning, 2=hijau) tanpa spasi: ").strip()
        if len(statuses_str) != 5 or not statuses_str.isdigit():
            print("Input status tidak valid. Pastikan memasukkan 5 digit (0,1,2).")
            return None, None

        statuses = [int(ch) for ch in statuses_str]
        return guess_word, statuses

    def play(self, attempts: int = 6) -> None:
        """
        Loop utama permainan. Pemain diberikan kesempatan untuk memasukkan tebakan
        hingga maksimal attempt tercapai atau solusi ditemukan.
        """
        for attempt in range(1, attempts + 1):
            print(f"\n=== Attempt {attempt}/{attempts} ===")
            self.print_state()

            guess_word, statuses = self._get_user_guess()
            if guess_word is None or statuses is None:
                continue

            # Jika status adalah 22222, periksa langsung apakah kata tersebut valid.
            if statuses == [2, 2, 2, 2, 2]:
                if guess_word in self.full_wordlist:
                    self.candidates = {guess_word}
                    print("\nSolusi ditemukan!")
                    print("Kata yang benar adalah:", guess_word)
                    break
                else:
                    print("Tebakan dengan status 22222 tidak ada dalam wordlist. Silakan periksa kembali.")
                    continue

            self.update_criteria(guess_word, statuses)
            self.filter_candidates()

            print("\nKandidat yang tersisa:")
            print(", ".join(sorted(self.candidates)) if self.candidates else "Tidak ada kandidat tersisa.")

            if len(self.candidates) == 1:
                print("\nSolusi ditemukan!")
                print("Kata yang benar adalah:", next(iter(self.candidates)))
                break

def main() -> None:
    game = KatlaGame("wordlist.txt")
    print("=== Selamat Datang di Katla Guesser ===")
    print(f"Wordlist dimuat dengan {len(game.full_wordlist)} kata.\n")
    game.play()

if __name__ == "__main__":
    main()
