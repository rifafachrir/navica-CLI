import os
import sys
import DataKamarPenginapan as kamar
import SewaPenginapan as sewa

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def menu_pemilik_penginapan(userId):
    with open("database/dataMitra.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            bagian = line.strip().split("|")
            if bagian[1] == userId:
                mitraId = bagian[0]
    print("=== Menu Pemilik Penginapan ===")
    print("1. Lihat Daftar menginap")
    print("2. Tambah daftar penginap Baru")
    print("3. check-in")
    print("4. check-out")
    print("5. pindah kamar")
    print("6. Tambah data Kamar")
    print("7. Liat data Kamar")
    print("8. Ubah data Kamar ")

    print("0. Keluar")

    pilihan = input("Pilih opsi (0-4): ")

    while True:
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
        elif pilihan == "9":
            kamar.ubah_kamar_by_mitraId(mitraId)
        elif pilihan == "0":
            print("Keluar dari menu pemilik penginapan.")
            break
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")