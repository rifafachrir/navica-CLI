import os
from penginapan.DataPenginapan import load_penginapan

DATA_FILE = "database/dataKamar.txt"

def ensure_file():
    if not os.path.exists("penginapan"):
        os.makedirs("penginapan")
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").close()


def load_kamar():
    ensure_file()
    kamar_list = []
    with open(DATA_FILE, "r") as file:
        for line in file:
            data = line.strip().split("|")
            if len(data) == 5:
                kamar_list.append({
                    "id": data[0],
                    "tipe": data[1],
                    "harga": data[2],
                    "status": data[3],
                    "id_penginapan": data[4]
                })
    return kamar_list


def save_kamar(kamar_list):
    with open(DATA_FILE, "w") as file:
        for k in kamar_list:
            file.write(
                f"{k['id']}|{k['tipe']}|{k['harga']}|{k['status']}|{k['id_penginapan']}\n"
            )


def generate_id(kamar_list):
    if not kamar_list:
        return "K001"
    last_id = int(kamar_list[-1]["id"][1:])
    return f"K{last_id + 1:03d}"


def pilih_penginapan():
    penginapan_list = load_penginapan()

    if not penginapan_list:
        print("Belum ada data penginapan. Tambahkan penginapan terlebih dahulu.")
        return None

    print("\n=== PILIH PENGINAPAN ===")
    for p in penginapan_list:
        print(f"{p['id']} - {p['nama']}")

    id_penginapan = input("Masukkan ID Penginapan: ")

    for p in penginapan_list:
        if p["id"] == id_penginapan:
            return id_penginapan

    print("ID penginapan tidak valid.")
    return None


def get_nama_penginapan(id_penginapan):
    for p in load_penginapan():
        if p["id"] == id_penginapan:
            return p["nama"]
    return "Tidak Diketahui"


def tambah_kamar():
    kamar_list = load_kamar()

    id_penginapan = pilih_penginapan()
    if not id_penginapan:
        return

    print("\n=== TAMBAH KAMAR ===")
    tipe = input("Tipe Kamar: ")
    harga = input("Harga per malam: ")

    kamar_baru = {
        "id": generate_id(kamar_list),
        "tipe": tipe,
        "harga": harga,
        "status": "Tersedia",
        "id_penginapan": id_penginapan
    }

    kamar_list.append(kamar_baru)
    save_kamar(kamar_list)

    print("Kamar berhasil ditambahkan.\n")


def tampilkan_kamar():
    kamar_list = load_kamar()

    print("\n=== DATA KAMAR ===")
    if not kamar_list:
        print("Belum ada data kamar.")
        return

    for k in kamar_list:
        print(f"ID Kamar      : {k['id']}")
        print(f"Tipe          : {k['tipe']}")
        print(f"Harga         : {k['harga']}")
        print(f"Status        : {k['status']}")
        print(f"Penginapan    : {get_nama_penginapan(k['id_penginapan'])}")
        print("-" * 30)


def edit_kamar():
    kamar_list = load_kamar()
    tampilkan_kamar()

    id_edit = input("Masukkan ID Kamar yang ingin diedit: ")

    for k in kamar_list:
        if k["id"] == id_edit:
            print("Kosongkan jika tidak ingin mengubah.")
            tipe = input(f"Tipe ({k['tipe']}): ") or k["tipe"]
            harga = input(f"Harga ({k['harga']}): ") or k["harga"]
            status = input(f"Status ({k['status']}): ") or k["status"]

            k["tipe"] = tipe
            k["harga"] = harga
            k["status"] = status

            save_kamar(kamar_list)
            print("Data kamar berhasil diperbarui.\n")
            return

    print("ID kamar tidak ditemukan.\n")


def hapus_kamar():
    kamar_list = load_kamar()
    tampilkan_kamar()

    id_hapus = input("Masukkan ID Kamar yang ingin dihapus: ")

    for k in kamar_list:
        if k["id"] == id_hapus:
            kamar_list.remove(k)
            save_kamar(kamar_list)
            print("Kamar berhasil dihapus.\n")
            return

    print("ID kamar tidak ditemukan.\n")


def menu():
    while True:
        print("\n=== MENU DATA KAMAR ===")
        print("1. Tambah Kamar")
        print("2. Lihat Kamar")
        print("3. Edit Kamar")
        print("4. Hapus Kamar")
        print("5. Kembali")

        pilihan = input("Pilih menu (1-5): ")

        if pilihan == "1":
            tambah_kamar()
        elif pilihan == "2":
            tampilkan_kamar()
        elif pilihan == "3":
            edit_kamar()
        elif pilihan == "4":
            hapus_kamar()
        elif pilihan == "5":
            break
        else:
            print("Pilihan tidak valid.")
