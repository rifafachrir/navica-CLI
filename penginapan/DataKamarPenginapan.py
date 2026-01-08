# BAGIAN FIRDAUS

import os

# path file database kamar
FILE_KAMAR = "database/DataKamarPenginapan.txt"
FILE_PENGINAPAN = "database/DataPenginapan.txt"

# Membuat fungsi tambah, lihat, ubah, dan hapus data Kamar penginapan / villa
kamar_list = []
penginapan_list = []

# Membuat fungsi tambah, lihat, ubah, dan hapus data Kamar penginapan / villa

next_id = 1  # next id yaitu untuk generate id kamar otomatis (jadi unik setiap kamar)

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

    





# Validasi sederhana: hanya huruf, dan input harus ada isi(tidak boleh kosong)
def hanya_huruf_dan_spasi(teks):
    teks = teks.strip()
    if teks == "":
        return False
    return teks.replace(" ", "").isalpha()

def tambah_kamar():
    print("\n=== TAMBAH KAMAR ===")
    print("Pilih Penginapan / Villa untuk kamar ini: ")
    for i, p in enumerate(penginapan_list):
        print(f"{i + 1}. (ID: {p['penginapanId']}) {p['namaPenginapan']} ")
    pilihan = int(input("Masukkan nomor penginapan: ")) - 1
    if 0 <= pilihan < len(penginapan_list):
        penginapanId = penginapan_list[pilihan]['penginapanId']
        namaPenginapan = penginapan_list[pilihan]['namaPenginapan']
    else:
        print("Pilihan tidak valid.")
        return
    kodeKamar = generate_id(penginapanId)
    tipe = input("Tipe kamar : ").strip()
    if not hanya_huruf_dan_spasi(tipe):
        print("Input ditolak: Tipe kamar hanya boleh huruf.\n")
        return
    harga = int(input("Harga per malam(isi dengan angka): "))
    kapasitas = int(input("Kapasitas orang(isi dengan angka): "))

    status = input("Status (tersedia/tidak): ").strip().lower()
    if status not in ["tersedia", "tidak"]:
        print("Input ditolak: Status harus 'tersedia' atau 'tidak'.\n")
        return

    kamar = {
        "id": kodeKamar,
        "namaPenginapan": namaPenginapan,
        "tipe": tipe,
        "harga": harga,
        "kapasitas": kapasitas,
        "status": status,
    }

    kamar_list.append(kamar)
    save_kamar()
    print("Kamar berhasil ditambahkan.\n")

def lihat_kamar():
    print("\n=== DAFTAR KAMAR ===")
    if len(kamar_list) == 0:
        print("Belum ada data kamar.\n")
    else:
        for k in kamar_list:
            print(f"ID        : {k['id']}")
            print(f"Nama Penginapan      : {k['namaPenginapan']}")

            print(f"Tipe      : {k['tipe']}")
            print(f"Harga     : {k['harga']}")
            print(f"Kapasitas : {k['kapasitas']}")
            print(f"Status    : {k['status']}")
            print("------------------------")
        print()

def lihat_kamar_pemilik(penginapanId):
    print("\n=== DAFTAR KAMAR ANDA ===")
    ditemukan = False
    for k in kamar_list:
        if k["id"].startswith(penginapanId):
            ditemukan = True
            print(f"ID        : {k['id']}")
            print(f"Nama Penginapan      : {k['namaPenginapan']}")
            print(f"Tipe      : {k['tipe']}")
            print(f"Harga     : {k['harga']}")
            print(f"Kapasitas : {k['kapasitas']}")
            print(f"Status    : {k['status']}")
            print("------------------------")
    if not ditemukan:
        print("Belum ada data kamar untuk penginapan Anda.\n")
    else:
        print()


def cari_kamar_by_id(kamar_id):
    for k in kamar_list:
        if k["id"] == kamar_id:
            return k
    return None

def ubah_kamar():
    print("\n=== UBAH KAMAR ===")
    print("Pilih Kode Kamar yang akan diubah: ")
    for i, k in enumerate(kamar_list):
        print(f"{i + 1}. (ID: {k['id']}) {k['namaPenginapan']} - {k['tipe']}")
    kamarId = int(input("Masukkan nomor kamar: ")) - 1
    kamar = cari_kamar_by_id(kamar_list[kamarId]['id'])
    if kamar is None:
        print("Data kamar tidak ditemukan.\n")
        return
    else:
        print("Isi Semua data baru (yang lama diganti):")
        tipe = input("Tipe kamar : ").strip()
        if not hanya_huruf_dan_spasi(tipe):
            print("Input ditolak: Tipe kamar hanya boleh huruf.\n")
            return
        harga = int(input("Harga per malam(isi dengan angka): "))
        kapasitas = int(input("Kapasitas orang(isi dengan angka): "))

        status = input("Status (tersedia/tidak) : ").strip().lower()
        if status not in ["tersedia", "tidak"]:
            print("Input ditolak: Status harus 'tersedia' atau 'tidak'.\n")
            return


        # kamar["nama"] = nama
        kamar["tipe"] = tipe
        kamar["harga"] = harga
        kamar["kapasitas"] = kapasitas
        kamar["status"] = status
        save_kamar()
        print("Data kamar berhasil diubah.\n")

def hapus_kamar():
    print("\n=== HAPUS KAMAR ===")
    kodeKamar = input("Masukkan Kode Kamar yang akan dihapus: ").strip()

    kamar = cari_kamar_by_id(kodeKamar)

    if kamar is None:
        print("Kamar tidak ditemukan.\n")
    else:
        kamar_list.remove(kamar)
        save_kamar()
        print("Data kamar berhasil dihapus.\n")

def menu():
    # setiap masuk menu, load dulu dari file supaya data terbaru
    load_kamar()
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
            continue

load_kamar()
if __name__ == "__main__":
    menu()


