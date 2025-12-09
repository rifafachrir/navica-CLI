import DataKamarPenginapan as dataKamar
import komunitas as komunitas
import authentication as auth

def mainMenu():
    print("=== Selamat Datang di Navica (Alpha 1.0) ===")
    
    while True:
        print("\n=== MENU UTAMA ===")
        print("1. Data Kamar Penginapan")
        print("2. Komunitas")
        print("3. Login")
        print("4. Keluar")
        pilihan = input("Pilih menu (1-4): ")

        if pilihan == "1":
            dataKamar.menu()
        elif pilihan == "2":
            komunitas.CommunityMenu()
        elif pilihan == "3":
            auth.start_authentication()
        elif pilihan == "4":
            print("Program selesai.")
            print("Sampai Jumpa kembali!!!!")
            break
        else:
            print("Pilihan tidak dikenal.\n")


mainMenu()