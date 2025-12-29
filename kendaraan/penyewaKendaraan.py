penyewa_list = []  # Menyimpan semua data penyewa


def tambah_penyewa():
    print("\n=== Tambah Data Penyewa ===")
    nama = input("Nama Penyewa       : ")
    kendaraan = input("Jenis Kendaraan    : ")
    lama_sewa = input("Lama Sewa (hari)   : ")

    data = {
        "nama": nama,
        "kendaraan": kendaraan,
        "lama_sewa": lama_sewa
    }

    penyewa_list.append(data)
    print(">> Data berhasil ditambahkan!\n")


def lihat_penyewa():
    print("\n=== Daftar Penyewa ===")
    if not penyewa_list:
        print("Belum ada data penyewa.\n")
        return

    for i, p in enumerate(penyewa_list):
        print(f"{i+1}. Nama: {p['nama']}, Kendaraan: {p['kendaraan']}, Lama sewa: {p['lama_sewa']} hari")
    print()


def ubah_penyewa():
    print("\n=== Ubah Data Penyewa ===")
    lihat_penyewa()

    if not penyewa_list:
        return

    nomor = int(input("Masukkan nomor penyewa yang ingin diubah: "))
    if nomor < 1 or nomor > len(penyewa_list):
        print("Nomor tidak valid!\n")
        return

    index = nomor - 1
    print("Biarkan kosong jika tidak ingin mengubah.")

    nama_baru = input("Nama Penyewa Baru       : ")
    kendaraan_baru = input("Jenis Kendaraan Baru    : ")
    lama_baru = input("Lama Sewa Baru (hari)   : ")

    if nama_baru:
        penyewa_list[index]["nama"] = nama_baru
    if kendaraan_baru:
        penyewa_list[index]["kendaraan"] = kendaraan_baru
    if lama_baru:
        penyewa_list[index]["lama_sewa"] = lama_baru

    print(">> Data berhasil diubah!\n")


def hapus_penyewa():
    print("\n=== Hapus Data Penyewa ===")
    lihat_penyewa()

    if not penyewa_list:
        return

    nomor = int(input("Masukkan nomor penyewa yang akan dihapus: "))
    if nomor < 1 or nomor > len(penyewa_list):
        print("Nomor tidak valid!\n")
        return

    penyewa_list.pop(nomor - 1)
    print(">> Data berhasil dihapus!\n")


def menu_penyewa_kendaraan():
    # Menu utama
    while True:
        print("=== MENU PENYEWA KENDARAAN ===")
        print("1. Tambah Data")
        print("2. Lihat Data")
        print("3. Ubah Data")
        print("4. Hapus Data")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            tambah_penyewa()
        elif pilihan == "2":
            lihat_penyewa()
        elif pilihan == "3":
            ubah_penyewa()
        elif pilihan == "4":
            hapus_penyewa()
        elif pilihan == "5":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("Pilihan tidak valid, coba lagi!\n")

if __name__ == "__main__":
    menu_penyewa_kendaraan()