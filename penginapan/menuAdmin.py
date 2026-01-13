import os
import sys

import penginapan.SewaPenginapan as sewa
import penginapan.DataPenginapan as penginapan

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def menu_penginapan_admin():

    while True:
        print("\n=== Menu Penginapan Admin ===")
        print("1. Lihat menu Penginapan")
        print("2. Lihat menu booking penginapan")
        print("0. Keluar")

        # Input di DALAM loop
        pilihan = input("Pilih opsi (0-7): ")

        if pilihan == "1":
            penginapan.menu()
        elif pilihan == "2":
            sewa.main()           
        elif pilihan == "0":
            print("Keluar dari menu pemilik penginapan.")
            break
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")
