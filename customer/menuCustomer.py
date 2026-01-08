import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kendaraan.penyewaKendaraan as penyewa
import penginapan.SewaPenginapan as sewaPenginapan
import komunitas.komunitas as komunitas


def menu_user(userId):
    customerId = None
    
    if not os.path.exists("database/dataCustomer.txt"):
        print("Data customer belum tersedia.")
        return

    with open("database/dataCustomer.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            bagian = line.strip().split("|")
            if bagian[1] == userId:
                print(f"SELAMAT DATANG, {bagian[2]} !!!")
                customerId = bagian[0]
                break

    if not os.path.exists("database/dataCustomer.txt"):
        print("Data customer belum tersedia.")
        return

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

if __name__ == "__main__":
    menu_user("1")