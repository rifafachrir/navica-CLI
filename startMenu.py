# Start Menu
import admin.authentication as auth
import admin.menu as main_menu

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
            auth.register()
        elif pilihan == "0":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak dikenal. Silakan coba lagi.")

tampilkan_menu()