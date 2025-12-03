# BAGIAN FIRDAUS
# Membuat fungsi tambah, lihat, ubah, dan hapus data Kamar penginapan / villa

kamar_list = []
next_id = 1  # next id yaitu untuk generate id kamar otomatis (jadi unik setiap kamar)


def generate_id():
    global next_id
    kamar_id = next_id
    next_id = next_id + 1  # setiap kamar yang dibuat akan menghasilkan next id + 1
    return kamar_id


def tambah_kamar():
    print("\n=== TAMBAH KAMAR ===")
    nama = input("Nama penginapan / villa : ")
    tipe = input("Tipe kamar             : ")
    harga = input("Harga per malam        : ")
    kapasitas = input("Kapasitas orang        : ")
    status = input("Status (tersedia/tidak): ")

    kamar = {
        "id": generate_id(),
        "nama": nama,
        "tipe": tipe,
        "harga": harga,
        "kapasitas": kapasitas,
        "status": status,
    }

    kamar_list.append(kamar)
    print("Kamar berhasil ditambahkan.\n")


def lihat_kamar():
    print("\n=== DAFTAR KAMAR ===")
    if len(kamar_list) == 0:
        print("Belum ada data kamar.\n")
    else:
        for k in kamar_list:
            print(f"ID: {k['id']}")
            print(f"Nama     : {k['nama']}")
            print(f"Tipe     : {k['tipe']}")
            print(f"Harga    : {k['harga']}")
            print(f"Kapasitas: {k['kapasitas']}")
            print(f"Status   : {k['status']}")
            print("------------------------")
        print()


def cari_kamar_by_id(kamar_id):
    for k in kamar_list:
        if k["id"] == kamar_id:
            return k
    return None


def ubah_kamar():
    print("\n=== UBAH KAMAR ===")
    try:
        kamar_id = int(input("Masukkan ID kamar: "))
    except ValueError:
        print("ID harus angka.\n")
        return

    kamar = cari_kamar_by_id(kamar_id)

    if kamar is None:
        print("Kamar tidak ditemukan.\n")
    else:
        print("Isi data baru (yang lama diganti):")
        nama = input("Nama penginapan / villa  : ")
        tipe = input("Tipe kamar               : ")
        harga = input("Harga per malam         : ")
        kapasitas = input("Kapasitas orang     : ")
        status = input("Status (tersedia/tidak): ")

        kamar["nama"] = nama
        kamar["tipe"] = tipe
        kamar["harga"] = harga
        kamar["kapasitas"] = kapasitas
        kamar["status"] = status

        print("Data kamar berhasil diubah.\n")


def hapus_kamar():
    print("\n=== HAPUS KAMAR ===")
    try:
        kamar_id = int(input("Masukkan ID kamar: "))
    except ValueError:
        print("ID harus angka.\n")
        return

    kamar = cari_kamar_by_id(kamar_id)

    if kamar is None:
        print("Kamar tidak ditemukan.\n")
    else:
        kamar_list.remove(kamar)
        print("Data kamar berhasil dihapus.\n")


def menu():
    while True:
        print("=== MENU KAMAR ===")
        print("1. Tambah kamar")
        print("2. Lihat kamar")
        print("3. Ubah kamar")
        print("4. Hapus kamar")
        print("5. Keluar")
        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            tambah_kamar()
        elif pilihan == "2":
            lihat_kamar()
        elif pilihan == "3":
            ubah_kamar()
        elif pilihan == "4":
            hapus_kamar()
        elif pilihan == "5":
            print("Program selesai.")
            break
        else:
            print("Pilihan tidak dikenal.\n")

menu()
