# import kelolaCustomer as kelolaCustomer
from . import kelolaCustomer
import kendaraan.pemilikKendaraan as kendaraan
import kendaraan.menuAdmin as kendaraan
import penginapan.menuAdmin as penginapan
import komunitas.komunitas as komunitas
import admin.authentication as auth
import mitra.dataMitra as mitra
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def mainMenu():
    print("=== Selamat Datang di Navica (Alpha 1.0) ===")

    while True:
        # Tampilan Menu
        print("\n=== MENU UTAMA ===")
        print("1. menu authentication")
        print("2. menu Customer")  # <--- Ini nanti masuk ke RUD Customer
        print("3. Menu Mitra")
        print("4. Menu Penginapan")
        print("5. Menu Kendaraan")
        print("6. Menu Komunitas")
        print("0. Keluar")

        pilihan = input("Pilih menu (0-6): ")

        if pilihan == "1":
            auth.start_authentication()

        elif pilihan == "2":
            # MASUK KE FITUR RUD (Read Update Delete) CUSTOMER
            kelolaCustomer.menu_kelola_customer()

        elif pilihan == "3":
            mitra.main()

        elif pilihan == "4":
            penginapan.menu_penginapan_admin()

        elif pilihan == "5":
            kendaraan.menu_pemilik_kendaraan()

        elif pilihan == "6":
            komunitas.CommunityMenu()

        elif pilihan == "0":
            print("Program selesai.")
            print("Sampai Jumpa kembali!!!!")
            break

        else:
            print("Pilihan tidak dikenal.\n")


if __name__ == "__main__":
    mainMenu()
