import authentication as auth
import komunitas.komunitas as komunitas
import penginapan.DataPenginapan as dataPenginapan
import penginapan.DataKamarPenginapan as dataKamar
import penginapan.SewaPenginapan as sewa
import kendaraan.menuPemilikKendaraan as kendaraan


def mainMenu():
    print("=== Selamat Datang di Navica (Alpha 1.0) ===")

    while True:
        print("\n=== MENU UTAMA ===")
        print("1. menu User")
        print("2. menu Customer")
        print("3. Menu Mitra")
        print("4. Menu Penginapan")
        print("5. Menu Kendaraan")
        print("6. Menu Komunitas")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-6): ")
        if pilihan == "1":
            auth.start_authentication()

        elif pilihan == "2":
            auth.m
        elif pilihan == "3":
             print("menu mitra")
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
