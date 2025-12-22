# Start Menu
import authentication as auth
import menu as main_menu

def tampilkan_menu():
    while True:
        print("=== Selamat Datang di Navica ===")
        print("1. Login")
        print("2. Register")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-2): ")

        if pilihan == "1":
            auth.login()
            main_menu.mainMenu()
        elif pilihan == "2":
            username = input("Masukkan username baru: ")
            password = input("Masukkan password baru: ")
            auth.register(username, password)
        elif pilihan == "0":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak dikenal. Silakan coba lagi.")

tampilkan_menu()