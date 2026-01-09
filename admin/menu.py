import penginapan.DataKamarPenginapan as dataKamar
import authentication as auth
import komunitas.komunitas as komunitas
import penginapan.SewaPenginapan as sewa
import mitra.dataMitra as mitra

def mainMenu():
    print("=== Selamat Datang di Navica (Alpha 1.0) ===")
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Login")
        print("2. Komunitas")
        print("3. Data Kamar Penginapan (Admin)")
        print("4. Sewa Penginapan (User)")
        print("5. Mitra (Admin)")
        print("6. Keluar")
        pilihan = input("Pilih menu (1-5): ")
        if pilihan == "1":
           auth.start_authentication()
        elif pilihan == "2":
            komunitas.CommunityMenu()
        elif pilihan == "3":
             dataKamar.menu()
        elif pilihan == "4":
            sewa.main()
        elif pilihan == "5":
            mitra.main()
        elif pilihan == "6":
            print("Program selesai.")
            print("Sampai Jumpa kembali!!!!")
            break
        else:
            print("Pilihan tidak dikenal.\n")


if __name__ == "__main__":
    mainMenu()
