

def menu_user():
    while True:
        print("=== Selamat Datang ===")
        print("1. Booking Hotel")
        print("2. Rental Kendaraan")
        print("3. Komunitas")
        print("0. Keluar")
        menu = input("Pilih menu (0-3): ")
        if menu == "1":
            print("=== Booking Hotel ===")
        elif menu == "2":
            print("=== Rental Kendaraan ===")
        elif menu == "3":
            print("=== Komunitas ===")
        elif menu == "0":
            print("Keluar dari menu user.")
            break
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")

if "__main__" == __name__:
    menu_user()

