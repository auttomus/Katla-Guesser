# Katla Guesser

Katla Guesser adalah program Python untuk membantu memecahkan permainan menebak kata "Katla". Program ini menggunakan sebuah wordlist untuk menyaring kandidat jawaban berdasarkan umpan balik tebakan (seperti status huruf: abu-abu, kuning, hijau). Proyek ini juga menyertakan modul eksperimen untuk menghitung frekuensi kemunculan huruf dalam wordlist.

Katla Guesser is a Python program designed to assist in solving the word-guessing game "Katla". The program uses a wordlist to filter candidate words based on guess feedback (such as letter statuses: gray, yellow, and green). This project also includes an experiment module to count the frequency of letters in the wordlist.

---

## Daftar Isi / Table of Contents

- [Fitur Utama / Key Features](#fitur-utama--key-features)
- [Struktur Proyek / Project Structure](#struktur-proyek--project-structure)
- [Instalasi / Installation](#instalasi--installation)
- [Cara Menggunakan / How to Use](#cara-menggunakan--how-to-use)

---

## Fitur Utama / Key Features

- **Penyaringan Kandidat Kata**  
  Menyaring kandidat kata dari wordlist berdasarkan umpan balik tebakan dengan aturan:
  - Huruf yang tidak muncul (abu-abu) tidak boleh ada.
  - Frekuensi huruf harus memenuhi nilai minimal dan maksimal sesuai tebakan.
  - Posisi huruf harus sesuai dengan feedback (hijau untuk posisi yang benar, kuning untuk posisi yang salah).

- **Eksperimen Wordlist**  
  Modul `experiment.py` menghitung dan menampilkan frekuensi kemunculan setiap huruf dalam wordlist.

- **Automasi Permainan**  
  Modul `main.py` membuka situs Katla secara acak dan menjalankan permainan dengan input tebakan dari pengguna.

---

## Struktur Proyek / Project Structure

- **experiment.py**  
  Program sederhana untuk menghitung frekuensi huruf dari wordlist.

- **guesser.py**  
  Berisi kelas `KatlaGame` yang mengelola logika penyaringan kandidat kata berdasarkan umpan balik tebakan.

- **main.py**  
  Titik masuk program yang membuka situs web Katla secara acak dan memulai permainan.

---

## Instalasi / Installation

### Prasyarat / Requirements:
- Python 3.7 atau lebih tinggi / Python 3.7 or higher
- Modul Python:
  - PyAutoGUI
  - webbrowser (standar)
  - random (standar)
  - collections, typing (standar)

### Instalasi Dependensi / Installing Dependencies:
Jalankan perintah berikut untuk menginstal dependensi (jika belum terinstal):
```bash
pip install pyautogui
```

## Cara Menggunakan / How To Use

### Bahasa Indonesa

#### 1. Eksperimen Wordlist (opsional)
Jalankan experiment.py untuk melihat frekuensi kemunculan tiap huruf dalam wordlist:

```bash
python experiment.py
```

#### 2. Memulai Permainan Katla
Jalankan main.py

```bash
python main.py
```

Program akan:

- Membuka situs Katla dengan URL acak.
- Memulai sesi permainan menggunakan kelas KatlaGame.
Input Tebakan:

- Masukkan kata tebakan (5 huruf).
- Masukkan status masing-masing huruf tanpa spasi:
- 0: Huruf tidak ada (abu-abu)
- 1: Huruf ada tetapi posisinya salah (kuning)
- 2: Huruf ada dan posisinya benar (hijau)
Jika status yang dimasukkan adalah 22222, program akan langsung memeriksa apakah kata tersebut merupakan solusi yang benar.

### English

#### 1. Wordlist Experiment (optional)
Run experiment.py to display the frequency of each letter in the wordlist:

```bash
python experiment.py
```

#### 2. Starting the Katla Game
Run main.py

```bash
python main.py
```

The program will:

- Membuka situs Katla dengan URL acak.
- Memulai sesi permainan menggunakan kelas KatlaGame.

Guess Input:

- Enter a 5-letter word as your guess.
- Enter the status for each letter (without spaces):
- 0: Letter is not in the word (gray)
- 1: Letter is in the word but in the wrong position (yellow)
- 2: Letter is in the correct position (green)
If the status entered is 22222, the program will immediately check if the guess is the correct solution.

