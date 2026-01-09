import os
import sys

import penginapan.DataKamarPenginapan as kamar
import penginapan.SewaPenginapan as sewa

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def menu_pemilik_penginapan(userId):
    mitraId = None
    # Cek Mitra ID
    if os.path.exists("database/dataMitra.txt"):
        with open("database/dataMitra.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) > 1 and bagian[1] == userId:
                    mitraId = bagian[0]
                    break

    if mitraId is None:
        print("Error: User ini tidak terdaftar sebagai Mitra Penginapan.")
        return

    while True:
        print("\n=== Menu Pemilik Penginapan ===")
        print("1. Lihat Daftar menginap")
        print("2. Tambah daftar penginap Baru")
        print("3. Check-in")
        print("4. Check-out")
        print("5. Pindah kamar")
        print("6. Tambah data Kamar")
        print("7. Lihat data Kamar")
        print("8. Ubah data Kamar")
        print("0. Keluar")

        # Input di DALAM loop
        pilihan = input("Pilih opsi: ")

        if pilihan == "1":
            sewa.read_data_by_mitraId(mitraId)
        elif pilihan == "2":
            sewa.booking_with_mitraId(mitraId)
        elif pilihan == "3":
            sewa.check_in(mitraId)
        elif pilihan == "4":
            sewa.check_out(mitraId)
        elif pilihan == "5":
            sewa.pindah_ruangan()
        elif pilihan == "6":
            kamar.tambah_kamar_with_mitraId(mitraId)
        elif pilihan == "7":
            kamar.liat_kamar_with_mitraId(mitraId)
        elif pilihan == "8":
            kamar.ubah_kamar_by_mitraId(mitraId)
        elif pilihan == "0":
            print("Keluar dari menu pemilik penginapan.")
            break
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")
