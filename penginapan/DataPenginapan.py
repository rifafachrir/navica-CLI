import os

DATA_FILE = "database/dataPenginapan.txt"
DATA_MITRA = "database/dataMitra.txt"


def ensure_file():
    if not os.path.exists("penginapan"):
        os.makedirs("penginapan")
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").close()
penginapan_list = []
mitra_list = []

def load_penginapan():
    ensure_file()
    
    with open(DATA_FILE, "r") as file:
        for line in file:
            data = line.strip().split("|")
            penginapan_list.append({
                "penginapan_id": data[0],
                "mitraId": data[1],
                "namaPenginapan": data[2],
                "alamat": data[3],
                "noTelp": data[4]
            })
    with open(DATA_MITRA, "r") as f:
        for line in f:
            data = line.strip().split("|")
            mitra_list.append({
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
    for i, m in enumerate(mitra_list):
        print(f"{1+i}. {m['id']} - {m['nama']}")
    pemilik = input("Masukkan Id pemilik: ")
    noTelp = input("Nomor Telepon: ")
    new_penginapan = {
        "penginapnaId": generate_id(penginapan_list),
        "mitraId": pemilik,
        "namaPenginapan": nama,
        "alamat": alamat,
        "noTelp": noTelp
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
        for m in mitra_list:
            if m["id"] == p["mitraId"]:
                print(f"Pemilik  : {m['nama']}")
        print(f"Nama     : {p['namaPenginapan']}")
        print(f"Alamat   : {p['alamat']}")
        print(f"no Telepon: {p['noTelp']}")
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
            for i, m in enumerate(mitra_list):
                print(f"{1+i}. {m['id']} - {m['nama']}")
                pemilik = input("Masukkan Id pemilik: ") or p['pemilik']
            noTelp = input(f"Nomor Telepon ({p['noTelp']}): ") or p["noTelp"]
            

            p["nama"] = nama
            p["alamat"] = alamat
            p["pemilik"] = pemilik
            p["noTelp"] = noTelp

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

if __name__ == "__main__":
    menu()