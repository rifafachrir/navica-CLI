# Start Menu
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import admin.authentication as auth
# import admin.menu as main_menu

def tampilkan_menu():
    while True:
        print("=== Selamat Datang di Navica ===")
        print("1. Login")
        print("2. Register")
        print("3. Forget Password")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-3): ")

        if pilihan == "1":
            auth.login()
            # main_menu.mainMenu()
        elif pilihan == "2":
            auth.register()
        elif pilihan == "3":
            auth.forget_password()
        elif pilihan == "0":
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak dikenal. Silakan coba lagi.")


tampilkan_menu()