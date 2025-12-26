# BAGIAN FIRDAUS

import os

# path file database kamar
FILE_KAMAR = "database/DataKamarPenginapan.txt"

# Membuat fungsi tambah, lihat, ubah, dan hapus data Kamar penginapan / villa
kamar_list = []

next_id = 1  # next id yaitu untuk generate id kamar otomatis (jadi unik setiap kamar)

def load_kamar():
    """Load data kamar dari file ke kamar_list dan set next_id."""
    global kamar_list, next_id

    kamar_list = []
    if not os.path.exists(FILE_KAMAR):
        next_id = 1
        return

    with open(FILE_KAMAR, "r", encoding="utf-8") as f:
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) != 6:
                continue
            kamar_id = int(bagian[0])
            nama = bagian[1]
            tipe = bagian[2]
            harga = int(bagian[3])
            kapasitas = int(bagian[4])
            status = bagian[5]

            kamar_list.append({
                "id": kamar_id,
                "nama": nama,
                "tipe": tipe,
                "harga": harga,
                "kapasitas": kapasitas,
                "status": status,
            })

    # atur next_id supaya lanjut dari id terakhir
    if kamar_list:
        max_id = max(k["id"] for k in kamar_list)
        next_id = max_id + 1
    else:
        next_id = 1


def save_kamar():
    """Simpan kamar_list ke file."""
    with open(FILE_KAMAR, "w", encoding="utf-8") as f:
        for k in kamar_list:
            f.write(
                f"{k['id']}|{k['nama']}|{k['tipe']}|{k['harga']}|{k['kapasitas']}|{k['status']}\n"
            )


def generate_id():
    global next_id
    kamar_id = next_id
    next_id = next_id + 1
    return kamar_id

# Validasi sederhana: hanya huruf, dan input harus ada isi(tidak boleh kosong)
def hanya_huruf_dan_spasi(teks):
    teks = teks.strip()
    if teks == "":
        return False
    return teks.replace(" ", "").isalpha()

def tambah_kamar():
    print("\n=== TAMBAH KAMAR ===")
    nama = input("Nama penginapan / villa : ").strip()
    if not hanya_huruf_dan_spasi(nama):
        print("Input ditolak: Nama hanya boleh huruf.\n")
        return

    tipe = input("Tipe kamar : ").strip()
    if not hanya_huruf_dan_spasi(tipe):
        print("Input ditolak: Tipe kamar hanya boleh huruf.\n")
        return

    try:
        harga = int(input("Harga per malam(isi dengan angka): "))
        kapasitas = int(input("Kapasitas orang(isi dengan angka): "))
    except ValueError:
        print("Input ditolak: Harga dan kapasitas harus angka.\n")
        return

    status = input("Status (tersedia/tidak): ").strip().lower()
    if status not in ["tersedia", "tidak"]:
        print("Input ditolak: Status harus 'tersedia' atau 'tidak'.\n")
        return

    kamar = {
        "id": generate_id(),
        "nama": nama,
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
            print(f"Nama      : {k['nama']}")
            print(f"Tipe      : {k['tipe']}")
            print(f"Harga     : {k['harga']}")
            print(f"Kapasitas : {k['kapasitas']}")
            print(f"Status    : {k['status']}")
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
        nama = input("Nama penginapan / villa : ").strip()
        if not hanya_huruf_dan_spasi(nama):
            print("Input ditolak: Nama hanya boleh huruf.\n")
            return

        tipe = input("Tipe kamar : ").strip()
        if not hanya_huruf_dan_spasi(tipe):
            print("Input ditolak: Tipe kamar hanya boleh huruf.\n")
            return

        try:
            harga = int(input("Harga per malam : "))
            kapasitas = int(input("Kapasitas orang : "))
        except ValueError:
            print("Input ditolak: Harga dan kapasitas harus angka.\n")
            return

        status = input("Status (tersedia/tidak) : ").strip().lower()
        if status not in ["tersedia", "tidak"]:
            print("Input ditolak: Status harus 'tersedia' atau 'tidak'.\n")
            return

        kamar["nama"] = nama
        kamar["tipe"] = tipe
        kamar["harga"] = harga
        kamar["kapasitas"] = kapasitas
        kamar["status"] = status

        save_kamar()
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
            print("Masukkan pilihan yang benar.\n")

if __name__ == "__main__":
    menu()
