import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from penginapan.DataPenginapan import load_penginapan


FILE_KAMAR = "database/DataKamarPenginapan.txt"
FILE_PENGINAPAN = "database/DataPenginapan.txt"

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
            penginapanId = bagian[1]
            tipe = bagian[2]
            harga = int(bagian[3])
            kapasitas = int(bagian[4])
            status = bagian[5]

            kamar_list.append({
                "id": kodeKamar,
                "penginapanId": penginapanId,
                "tipe": tipe,
                "harga": harga,
                "kapasitas": kapasitas,
                "status": status
            })
    
    with open(FILE_PENGINAPAN, "r") as f:
        for line in f:
            bagian = line.strip().split("|")
            penginapanId = bagian[0]
            mitraId = bagian[1]
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
                f"{k['id']}|{k['penginapanId']}|{k['tipe']}|{k['harga']}|{k['kapasitas']}|{k['status']}\n"
            )


def generate_id(penginapanId):
    inisials = []
    cocok = 0
    for p in penginapan_list:
        if p["penginapanId"] == penginapanId:
            nama = p["namaPenginapan"].lower().split(" ")
            inisial = "".join([n[0] for n in nama])  
            inisials.append(inisial)
    for i in inisials: 
        if i == inisial:
            cocok += 1
    return inisial + "-" + str(cocok).zfill(2)


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
    print("\n=== TAMBAH KAMAR ===")
    print("Pilih Penginapan / Villa untuk kamar ini: ")
    for i, p in enumerate(penginapan_list):
        print(f"{i + 1}. (ID: {p['penginapanId']}) {p['namaPenginapan']} ")
    pilihan = int(input("Masukkan nomor penginapan: ")) - 1
    if 0 <= pilihan < len(penginapan_list):
        penginapanId = penginapan_list[pilihan]['penginapanId']
    else:
        print("Pilihan tidak valid.")
        return
    kodeKamar = generate_id(penginapanId)
    tipe = input("Tipe kamar : ").strip()
    harga = int(input("Harga per malam(isi dengan angka): "))
    kapasitas = int(input("Kapasitas orang(isi dengan angka): "))

    status = input("Status (tersedia/tidak): ").strip().lower()
    if status not in ["tersedia", "tidak"]:
        print("Input ditolak: Status harus 'tersedia' atau 'tidak'.\n")
        return

    kamar = {
        "id": kodeKamar,
        "penginapanId": penginapanId,
        "tipe": tipe,
        "harga": harga,
        "kapasitas": kapasitas,
        "status": status,
    }

    kamar_list.append(kamar)
    save_kamar()
    print("Kamar berhasil ditambahkan.\n")

def tambah_kamar_with_mitraId(mitraId):
    print("\n=== TAMBAH KAMAR ===")
    print("Pilih Penginapan / Villa untuk kamar ini: ")
    for p in penginapan_list:
        if p["mitraId"] == mitraId:
            penginapanId = p['penginapanId']
    kodeKamar = generate_id(penginapanId)
    tipe = input("Tipe kamar : ").strip()
    harga = int(input("Harga per malam(isi dengan angka): "))
    kapasitas = int(input("Kapasitas orang(isi dengan angka): "))

    status = input("Status (tersedia/tidak): ").strip().lower()
    if status not in ["tersedia", "tidak"]:
        print("Input ditolak: Status harus 'tersedia' atau 'tidak'.\n")
        return

    kamar = {
        "id": kodeKamar,
        "penginapanId": penginapanId,
        "tipe": tipe,
        "harga": harga,
        "kapasitas": kapasitas,
        "status": status,
    }

    kamar_list.append(kamar)
    save_kamar()
    print("Kamar berhasil ditambahkan.\n")


def liat_kamar_with_mitraId(mitraId):
    print("\n=== TAMBAH KAMAR ===")

    for k in kamar_list:
        if k["mitraId"] == mitraId:
            print(f"ID Kamar      : {k['id']}")
            print(f"Tipe          : {k['tipe']}")
            print(f"Harga         : {k['harga']}")
            print(f"Status        : {k['status']}")
            print(f"kapasitas     : {k['kapasitas']}")
            for p in penginapan_list:
                if p["mitraId"] == mitraId:
                    print(f"Penginapan    : {p['namaPenginapan']}")
            print("-" * 30)
        


def tampilkan_kamar():

    print("\n=== DATA KAMAR ===")
    if not kamar_list:
        print("Belum ada data kamar.")
        return

    for k in kamar_list:
        print(f"ID Kamar      : {k['id']}")
        print(f"Tipe          : {k['tipe']}")
        print(f"Harga         : {k['harga']}")
        print(f"Status        : {k['status']}")
        print(f"kapasitas     : {k['kapasitas']}")
        for p in penginapan_list:
            if p["penginapnanId"] == k["penginapanId"]:
                print(f"Penginapan    : {p['namaPenginapan']}")        
    print("-" * 30)

def cari_kamar_by_id_and_penginapanId(penginapnanId,kamar_id):
    for k in kamar_list:
        if k["id"] == kamar_id and k["penginapanId"] == penginapnanId:
            return k
    return None

def ubah_kamar():
    print("\n=== UBAH KAMAR ===")
    print("List Penginapan: ")
    for i, p in enumerate(penginapan_list):
        print(f"{i + 1}. (ID: {p['penginapanId']}) {p['namaPenginapan']}")
    penginapanId = int(input("Masukkan berdasarkan no urutan penginapan:"))

    print("Pilih Kode Kamar yang akan diubah: ")
    for i, k in enumerate(kamar_list):
        if k["penginapanId"] == penginapanId:
            print(f"{i + 1}. (ID: {k['id']}) {k['namaPenginapan']} - {k['tipe']}")
    kamarId = int(input("Masukkan nomor kamar: ")) - 1
    kamar = cari_kamar_by_id_and_penginapanId(penginapanId, kamar_list[kamarId]['id'])
    if kamar is None:
        print("Data kamar tidak ditemukan.\n")
        return
    else:
        print("Isi Semua data baru (yang lama diganti):")
        tipe = input("Tipe kamar : ").strip()
        harga = int(input("Harga per malam(isi dengan angka): "))
        kapasitas = int(input("Kapasitas orang(isi dengan angka): "))

        status = input("Status (tersedia/tidak) : ").strip().lower()
        if status not in ["tersedia", "tidak"]:
            print("Input ditolak: Status harus 'tersedia' atau 'tidak'.\n")
            return


        kamar["penginapanId"] = penginapanId
        kamar["tipe"] = tipe
        kamar["harga"] = harga
        kamar["kapasitas"] = kapasitas
        kamar["status"] = status
        save_kamar()
        print("Data kamar berhasil diubah.\n")

def ubah_kamar_by_mitraId(mitraId):
    print("\n=== UBAH KAMAR ===")
    print("List Penginapan: ")
    for p in penginapan_list:
        if p['mitraId'] == mitraId:
            penginapanId = p["penginapanId"] 
    print("Pilih Kode Kamar yang akan diubah: ")
    for i, k in enumerate(kamar_list):
        if k['penginapanId'] == penginapanId:
            print(f"{i + 1}. (ID: {k['id']}) {k['namaPenginapan']} - {k['tipe']}")
    kamarId = int(input("Masukkan nomor kamar: ")) - 1
    kamar = cari_kamar_by_id_and_penginapanId(penginapanId, kamar_list[kamarId]['id'])
    if kamar is None:
        print("Data kamar tidak ditemukan.\n")
        return
    else:
        print("Isi Semua data baru (yang lama diganti):")
        tipe = input("Tipe kamar : ").strip()
        harga = int(input("Harga per malam(isi dengan angka): "))
        kapasitas = int(input("Kapasitas orang(isi dengan angka): "))

        status = input("Status (tersedia/tidak) : ").strip().lower()
        if status not in ["tersedia", "tidak"]:
            print("Input ditolak: Status harus 'tersedia' atau 'tidak'.\n")
            return


        kamar["penginapanId"] = penginapanId
        kamar["tipe"] = tipe
        kamar["harga"] = harga
        kamar["kapasitas"] = kapasitas
        kamar["status"] = status
        save_kamar()
        print("Data kamar berhasil diubah.\n")


def hapus_kamar():
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
            ubah_kamar()
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


