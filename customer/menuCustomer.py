import kendaraan.penyewaKendaraan as penyewa
import penginapan.SewaPenginapan as sewaPenginapan
import admin.komunitas.komunitas as komunitas
import os

def menu_user(userId):
    with open("database/dataCustomer.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            bagian = line.strip().split("|")
            if bagian[1] == userId:
                print(f"SELAMAT DATANG, {bagian[2]} !!!")
                customerId = bagian[0]

    while True:
        print("=== Selamat Datang ===")
        print("1. Booking Hotel")
        print("2. Rental Kendaraan")
        print("3. Komunitas")
        print("0. Keluar")
        menu = input("Pilih menu (0-3): ")
        if menu == "1":
            sewaPenginapan.userMenu(customerId)
        elif menu == "2":
            penyewa.menu_customer(customerId)
        elif menu == "3":
            komunitas.CommunityMenu()
        elif menu == "0":
            print("Keluar dari menu user.")
            break
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")

if "__main__" == __name__:
    menu_user()

