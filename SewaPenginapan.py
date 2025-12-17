import os

# file database sewa
file_name = "database/sewa_navica.txt"

# file database kamar (harus sama dengan di DataKamarPenginapan.py)
file_kamar = "database/DataKamarPenginapan.txt"


# ===== UTILITAS KAMAR (baca & update status) =====
def load_kamar_from_file():
    """Load daftar kamar dari file kamar (hanya untuk modul sewa)."""
    kamar_list = []
    if not os.path.exists(file_kamar):
        return kamar_list

    with open(file_kamar, "r", encoding="utf-8") as f:
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) != 6:
                continue
            try:
                kamar_id = int(bagian[0])
                nama = bagian[1]
                tipe = bagian[2]
                harga = int(bagian[3])
                kapasitas = int(bagian[4])
                status = bagian[5]
            except ValueError:
                continue

            kamar_list.append({
                "id": kamar_id,
                "nama": nama,
                "tipe": tipe,
                "harga": harga,
                "kapasitas": kapasitas,
                "status": status,
            })
    return kamar_list


def update_status_kamar(kamar_id, status_baru):
    """Update status kamar (tersedia/tidak) di file DataKamarPenginapan."""
    kamar_list = load_kamar_from_file()
    changed = False
    for k in kamar_list:
        if k["id"] == kamar_id:
            k["status"] = status_baru
            changed = True
            break

    if not changed:
        return  # kamar tidak ditemukan

    with open(file_kamar, "w", encoding="utf-8") as f:
        for k in kamar_list:
            f.write(
                f"{k['id']}|{k['nama']}|{k['tipe']}|{k['harga']}|{k['kapasitas']}|{k['status']}\n"
            )


# ===== DATA SEWA (LOAD & SAVE) =====
def load_data():
    if not os.path.exists(file_name):
        return []
    data = []
    with open(file_name, "r", encoding="utf-8") as file:
        for line in file:
            bagian = line.strip().split("|")
            if len(bagian) == 9:
                data.append({
                    "id": bagian[0],
                    "penyewa": bagian[1],
                    "jenis": bagian[2],
                    "nama_properti": bagian[3],
                    "nomor_kamar": bagian[4],
                    "lama_menginap": bagian[5],
                    "harga_permalam": bagian[6],
                    "total": bagian[7],
                    "status": bagian[8],
                })
    return data


def save_data(data):
    with open(file_name, "w", encoding="utf-8") as file:
        for d in data:
            file.write(
                f"{d['id']}|{d['penyewa']}|{d['jenis']}|{d['nama_properti']}|"
                f"{d['nomor_kamar']}|{d['lama_menginap']}|{d['harga_permalam']}|"
                f"{d['total']}|{d['status']}\n"
            )


def generate_id(data):
    nomor = len(data) + 1
    return "NAV" + str(nomor).zfill(2)


# ========================
# CRUD SEWA
# ========================
def create_data(data):
    print("\n=== PEMESANAN PENGINAPAN ===")
    id_sewa = generate_id(data)
    print("ID Sewa Otomatis :", id_sewa)

    penyewa = input("Nama Penyewa : ")

    # load kamar dari database
    kamar_list = load_kamar_from_file()
    if not kamar_list:
        print("Belum ada data kamar. Silakan hubungi admin.\n")
        return

    # tampilkan kamar yang tersedia saja
    print("\n=== DAFTAR KAMAR TERSEDIA ===")
    tersedia = [k for k in kamar_list if k["status"] == "tersedia"]
    if not tersedia:
        print("Tidak ada kamar yang tersedia saat ini.\n")
        return

    for k in tersedia:
        print(f"ID        : {k['id']}")
        print(f"Nama      : {k['nama']}")
        print(f"Tipe      : {k['tipe']}")
        print(f"Harga     : {k['harga']}")
        print(f"Kapasitas : {k['kapasitas']}")
        print(f"Status    : {k['status']}")
        print("------------------------")

    # pilih kamar
    try:
        pilih_id = int(input("Masukkan ID kamar yang ingin dipesan: "))
    except ValueError:
        print("ID kamar harus angka.\n")
        return

    kamar_dipilih = None
    for k in kamar_list:
        if k["id"] == pilih_id:
            kamar_dipilih = k
            break

    if kamar_dipilih is None:
        print("Kamar dengan ID tersebut tidak ditemukan.\n")
        return

    if kamar_dipilih["status"] != "tersedia":
        print("Kamar yang dipilih tidak tersedia.\n")
        return

    # ambil data dari kamar
    nama_properti = kamar_dipilih["nama"]
    jenis = kamar_dipilih["tipe"]           # bisa kamu mapping ke 'Hotel'/'Vila' kalau mau
    nomor_kamar = str(kamar_dipilih["id"])  # sementara pakai ID kamar sebagai nomor kamar

    lama_menginap = input("Lama Menginap (hari) : ")
    while not lama_menginap.isdigit():
        lama_menginap = input("Input harus angka : ")

    harga_permalam = str(kamar_dipilih["harga"])
    total = int(lama_menginap) * int(harga_permalam)

    data.append({
        "id": id_sewa,
        "penyewa": penyewa,
        "jenis": jenis,
        "nama_properti": nama_properti,
        "nomor_kamar": nomor_kamar,
        "lama_menginap": lama_menginap,
        "harga_permalam": harga_permalam,
        "total": str(total),
        "status": "Booking",
    })

    save_data(data)

    # update status kamar jadi tidak
    update_status_kamar(kamar_dipilih["id"], "tidak")

    print("\nPemesanan berhasil dibuat!\n")


def read_data(data):
    print("\n=== DAFTAR PEMESANAN ===")
    if not data:
        print("Belum ada data.\n")
        return

    for d in data:
        print(f"ID Sewa        : {d['id']}")
        print(f"Nama Penyewa   : {d['penyewa']}")
        print(f"Jenis          : {d['jenis']}")
        print(f"Nama Properti  : {d['nama_properti']}")
        print(f"Nomor Kamar    : {d['nomor_kamar']}")
        print(f"Lama Menginap  : {d['lama_menginap']} hari")
        print(f"Harga/Malam    : Rp {d['harga_permalam']}")
        print(f"Total Harga    : Rp {d['total']}")
        print(f"Status         : {d['status']}")
        print("-" * 30)


def update_data(data):
    print("\n=== UPDATE STATUS ===")
    target = input("Masukkan ID sewa: ")

    for d in data:
        if d["id"] == target:
            print("\nStatus saat ini:", d["status"])
            print("1. Booking")
            print("2. Check-in")
            print("3. Check-out")
            pilih = input("Pilih status: ")
            while pilih not in ["1", "2", "3"]:
                pilih = input("Masukkan pilihan 1-3: ")

            status_lama = d["status"]

            if pilih == "1":
                d["status"] = "Booking"
            elif pilih == "2":
                d["status"] = "Check-in"
            else:
                d["status"] = "Check-out"

            save_data(data)

            # jika dari Booking/Check-in menjadi Check-out -> buka kamar lagi
            if status_lama != "Check-out" and d["status"] == "Check-out":
                try:
                    id_kamar = int(d["nomor_kamar"])
                    update_status_kamar(id_kamar, "tersedia")
                except ValueError:
                    pass  # jika nomor_kamar bukan angka, abaikan

            print("Status berhasil diupdate!\n")
            return

    print("ID tidak ditemukan.\n")


def delete_data(data):
    print("\n=== HAPUS DATA ===")
    target = input("Masukkan ID sewa: ")

    for d in data:
        if d["id"] == target:
            # jika sewa masih Booking / Check-in, balikan kamar ke tersedia
            if d["status"] in ["Booking", "Check-in"]:
                try:
                    id_kamar = int(d["nomor_kamar"])
                    update_status_kamar(id_kamar, "tersedia")
                except ValueError:
                    pass

            data.remove(d)
            save_data(data)
            print("Data berhasil dihapus!\n")
            return

    print("ID tidak ditemukan.\n")


def search_data(data):
    print("\n=== PENCARIAN ===")
    print("1. Berdasarkan ID")
    print("2. Berdasarkan Nama Penyewa")
    pilihan = input("Pilih metode: ")
    while pilihan not in ["1", "2"]:
        pilihan = input("Pilih 1 atau 2: ")

    keyword = input("Masukkan kata kunci: ").lower()
    found = False

    for d in data:
        if pilihan == "1" and d["id"].lower() == keyword:
            found = True
        elif pilihan == "2" and keyword in d["penyewa"].lower():
            found = True
        else:
            continue

        print("\nData ditemukan:")
        print(f"ID Sewa        : {d['id']}")
        print(f"Nama Penyewa   : {d['penyewa']}")
        print(f"Jenis          : {d['jenis']}")
        print(f"Nama Properti  : {d['nama_properti']}")
        print(f"Nomor Kamar    : {d['nomor_kamar']}")
        print(f"Lama Menginap  : {d['lama_menginap']} hari")
        print(f"Harga/Malam    : Rp {d['harga_permalam']}")
        print(f"Total Harga    : Rp {d['total']}")
        print(f"Status         : {d['status']}")
        print("-" * 30)

    if not found:
        print("Tidak ada data yang cocok.\n")


def sort_data(data):
    print("\n=== URUTKAN DATA ===")
    print("1. Nama Penyewa (A-Z)")
    print("2. Total Harga (Termurah)")
    pilihan = input("Pilih metode: ")
    while pilihan not in ["1", "2"]:
        pilihan = input("Pilih 1 atau 2: ")

    if pilihan == "1":
        data.sort(key=lambda x: x["penyewa"].lower())
    else:
        data.sort(key=lambda x: int(x["total"]))

    save_data(data)
    read_data(data)


def main():
    data = load_data()
    while True:
        print("\n====== NAVICA — PEMESANAN PENGINAPAN ======")
        print("1. Tambah Pemesanan")
        print("2. Lihat Pemesanan")
        print("3. Update Status")
        print("4. Hapus Pemesanan")
        print("5. Cari Pemesanan")
        print("6. Urutkan Pemesanan")
        print("7. Keluar")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            create_data(data)
        elif pilihan == "2":
            read_data(data)
        elif pilihan == "3":
            update_data(data)
        elif pilihan == "4":
            delete_data(data)
        elif pilihan == "5":
            search_data(data)
        elif pilihan == "6":
            sort_data(data)
        elif pilihan == "7":
            print("Terima kasih telah menggunakan Navica.")
            break
        else:
            print("Pilihan tidak valid.\n")


if __name__ == "__main__":
    main()
