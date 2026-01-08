import os

DATA_FILE = "penginapan/penginapan.txt"


def ensure_file():
    if not os.path.exists("penginapan"):
        os.makedirs("penginapan")
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").close()


def load_penginapan():
    ensure_file()
    penginapan_list = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            data = line.strip().split("|")
            if len(data) == 4:
                penginapan_list.append({
                    "id": data[0],
                    "nama": data[1],
                    "alamat": data[2],
                    "pemilik": data[3]
                })
    return penginapan_list


def save_penginapan(penginapan_list):
    with open(DATA_FILE, "w") as file:
        for p in penginapan_list:
            file.write(f"{p['id']}|{p['nama']}|{p['alamat']}|{p['pemilik']}\n")


def generate_id(penginapan_list):
    if not penginapan_list:
        return "P001"
    last_id = int(penginapan_list[-1]["id"][1:])
    return f"P{last_id + 1:03d}"


def tambah_penginapan():
    penginapan_list = load_penginapan()

    print("\n=== TAMBAH PENGINAPAN ===")
    nama = input("Nama Penginapan: ")
    alamat = input("Alamat Penginapan: ")
    pemilik = input("Nama Pemilik: ")

    new_penginapan = {
        "id": generate_id(penginapan_list),
        "nama": nama,
        "alamat": alamat,
        "pemilik": pemilik
    }

    penginapan_list.append(new_penginapan)
    save_penginapan(penginapan_list)

    print("Penginapan berhasil ditambahkan.\n")


def tampilkan_penginapan():
    penginapan_list = load_penginapan()

    print("\n=== DATA PENGINAPAN ===")
    if not penginapan_list:
        print("Belum ada data penginapan.")
        return

    for p in penginapan_list:
        print(f"ID       : {p['id']}")
        print(f"Nama     : {p['nama']}")
        print(f"Alamat   : {p['alamat']}")
        print(f"Pemilik  : {p['pemilik']}")
        print("-" * 30)


def edit_penginapan():
    penginapan_list = load_penginapan()
    tampilkan_penginapan()

    id_edit = input("Masukkan ID Penginapan yang ingin diedit: ")

    for p in penginapan_list:
        if p["id"] == id_edit:
            print("Kosongkan jika tidak ingin mengubah.")
            nama = input(f"Nama ({p['nama']}): ") or p["nama"]
            alamat = input(f"Alamat ({p['alamat']}): ") or p["alamat"]
            pemilik = input(f"Pemilik ({p['pemilik']}): ") or p["pemilik"]

            p["nama"] = nama
            p["alamat"] = alamat
            p["pemilik"] = pemilik

            save_penginapan(penginapan_list)
            print("Data penginapan berhasil diperbarui.\n")
            return

    print("ID penginapan tidak ditemukan.\n")


def hapus_penginapan():
    penginapan_list = load_penginapan()
    tampilkan_penginapan()

    id_hapus = input("Masukkan ID Penginapan yang ingin dihapus: ")

    for p in penginapan_list:
        if p["id"] == id_hapus:
            penginapan_list.remove(p)
            save_penginapan(penginapan_list)
            print("Penginapan berhasil dihapus.\n")
            return

    print("ID penginapan tidak ditemukan.\n")


def menu():
    while True:
        print("\n=== MENU DATA PENGINAPAN ===")
        print("1. Tambah Penginapan")
        print("2. Lihat Penginapan")
        print("3. Edit Penginapan")
        print("4. Hapus Penginapan")
        print("5. Kembali")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            tambah_penginapan()
        elif pilihan == "2":
            tampilkan_penginapan()
        elif pilihan == "3":
            edit_penginapan()
        elif pilihan == "4":
            hapus_penginapan()
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid.")
