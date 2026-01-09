import admin.kelolaCustomer as kelolaCustomer
import kendaraan.menuPemilikKendaraan as kendaraan
import penginapan.SewaPenginapan as sewa
import penginapan.DataKamarPenginapan as dataKamar
import penginapan.DataPenginapan as dataPenginapan
import komunitas.komunitas as komunitas
import admin.authentication as auth
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def mainMenu():
    print("=== Selamat Datang di Navica (Alpha 1.0) ===")

    while True:
        # Tampilan Menu
        print("\n=== MENU UTAMA ===")
        print("1. menu User")
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
            print("Menu mitra belum tersedia.")

        elif pilihan == "4":
            dataPenginapan.menu()

        elif pilihan == "5":
            kendaraan.menuAdmin()

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
