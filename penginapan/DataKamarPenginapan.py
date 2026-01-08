import os
from penginapan.DataPenginapan import load_penginapan

DATA_FILE = "database/dataKamar.txt"

def ensure_file():
    if not os.path.exists("penginapan"):
        os.makedirs("penginapan")
    if not os.path.exists(DATA_FILE):
        open(DATA_FILE, "w").close()


def load_kamar():
    """Load data kamar dari file ke kamar_list dan set next_id."""
    global kamar_list, penginapan_list, next_id

    kamar_list = []
    penginapan_list = []   
    if not os.path.exists(FILE_KAMAR):
        next_id = 1
        return

    with open(FILE_KAMAR, "r", encoding="utf-8") as f:
        for line in f:
            bagian = line.strip().split("|")
            kodeKamar = bagian[0]
            namaPenginapan = bagian[1]
            tipe = bagian[2]
            harga = int(bagian[3])
            kapasitas = int(bagian[4])
            status = bagian[5]

            kamar_list.append({
                "id": kodeKamar,
                "namaPenginapan": namaPenginapan,
                "tipe": tipe,
                "harga": harga,
                "kapasitas": kapasitas,
                "status": status
            })
    
    with open(FILE_PENGINAPAN, "r") as f:
        for line in f:
            bagian = line.strip().split("|")
            penginapanId = int(bagian[0])
            mitraId = int(bagian[1])
            namaPenginapan = bagian[2]
            alamat = bagian[3]
            noTelp = bagian[4]

            penginapan_list.append({
                "penginapanId": penginapanId,
                "mitraId": mitraId,
                "namaPenginapan": namaPenginapan,
                "alamat": alamat,
                "noTelp": noTelp
            })


    # atur next_id supaya lanjut dari id terakhir
    # if kamar_list:
    #     max_id = max(k["id"] for k in kamar_list)
    #     next_id = max_id + 1
    # else:
    #     next_id = 1



def save_kamar():
    """Simpan kamar_list ke file."""
    with open(FILE_KAMAR, "w", encoding="utf-8") as f:
        for k in kamar_list:
            f.write(
                f"{k['id']}|{k['namaPenginapan']}|{k['tipe']}|{k['harga']}|{k['kapasitas']}|{k['status']}\n"
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
            continue

load_kamar()
if __name__ == "__main__":
    menu()


