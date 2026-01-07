

def menu_pemilik_penginapan():
    print("=== Menu Pemilik Penginapan ===")
    print("1. Lihat Daftar menginap")
    print("2. Tambah daftar penginap Baru")
    print("3. Liat data Kamar")
    print("0. Keluar")

    pilihan = input("Pilih opsi (0-2): ")

    while True:
        if pilihan == "1":
            print("=== Daftar Penginap ===")
        elif pilihan == "2":
            print("=== Tambah Penginap Baru ===")
        elif pilihan == "0":
            print("Keluar dari menu pemilik penginapan.")
            break
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")