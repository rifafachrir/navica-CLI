

def menu_pemilik_kendaraan():
    while True: 
        print("=== Selamat Datang pemilik kendaraan ===")
        print("1. lihat data peminjaman")
        print("2. Lihat data kendaraan yang ada")
        print("3. Tambah data kendaraan yang ingin dipinjam")
        print("4. Pengajuan kendaraan")
        menu = input("Pilih menu (1-4)")

        if menu == "1":
            print("=== Lihat data peminjaman")
        elif menu == "2":
            print("=== Lihat data kendaraan yang ada ")
        elif menu == "3":
            print("=== Tambah data kendaraan yang ingin dipinjam ===")
        elif menu == "4":
            print("=== data pengajuan kendaraan ===")
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")

if "__main__" == __name__:
    menu_pemilik_kendaraan()
