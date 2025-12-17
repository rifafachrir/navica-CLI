import DataKamarPenginapan as dataKamar
import komunitas as komunitas
import authentication as auth
import SewaPenginapan as sewa


def mainMenu():
    print("=== Selamat Datang di Navica (Alpha 1.0) ===")
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Data Kamar Penginapan (Admin)")
        print("2. Komunitas")
        print("3. Login")
        print("4. Sewa Penginapan (User)")
        print("5. Keluar")
        pilihan = input("Pilih menu (1-5): ")
        if pilihan == "1":
            dataKamar.menu()
        elif pilihan == "2":
            komunitas.CommunityMenu()
        elif pilihan == "3":
            auth.start_authentication()
        elif pilihan == "4":
            sewa.main()
        elif pilihan == "5":
            print("Program selesai.")
            print("Sampai Jumpa kembali!!!!")
            break
        else:
            print("Pilihan tidak dikenal.\n")


if __name__ == "__main__":
    mainMenu()
