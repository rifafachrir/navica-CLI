import kendaraan.penyewaKendaraan as penyewa
import kendaraan.pemilikKendaraan as pemilkKendaraan
import os
import sys

# Setup path agar bisa import modul lain
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modul yang dibutuhkan untuk menu


def menu_pemilik_kendaraan():

    # Masuk ke menu jika mitraId sudah aman
    while True:
        print(f"\n=== Selamat Datang admin di menu Kendaraan ===")
        print("1. Lihat data peminjaman")
        print("2. Lihat data Kendaraan")
        print("0. Keluar")
        menu = input("Pilih menu (0-2): ").strip()
        if menu == "":
            print("Menu tidak boleh kosong.")
            continue

        if menu == "1":
            penyewa.menu_penyewa_kendaraan()
        elif menu == "2":
            pemilkKendaraan.menuAdmin()
        elif menu == "0":
            break
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")
