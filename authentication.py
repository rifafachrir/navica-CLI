import os  # Materi: Module & Operasi File

file_name = "sewa_navica.txt"

# Materi: List & Dictionary
# List menampung banyak data, tiap data berbentuk dictionary


def load_data():
    if not os.path.exists(file_name):
        return []

    data = []
    with open(file_name, "r") as file:
        for line in file:
            bagian = line.strip().split("|")  # Materi: String & List
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
                    "status": bagian[8]
                })
    return data


# Materi: Operasi File (Write)
def save_data(data):
    with open(file_name, "w") as file:
        for d in data:
            file.write(
                f"{d['id']}|{d['penyewa']}|{d['jenis']}|{d['nama_properti']}|{d['nomor_kamar']}|{d['lama_menginap']}|{d['harga_permalam']}|{d['total']}|{d['status']}\n"
            )


# Materi: Operasi String, Perhitungan
def generate_id(data):
    nomor = len(data) + 1
    return "NAV" + str(nomor).zfill(2)


# ========================
# CRUD (Materi: Fungsi)
# ========================

def create_data(data):
    print("\n=== PEMESANAN PENGINAPAN ===")

    id_sewa = generate_id(data)
    print("ID Sewa Otomatis :", id_sewa)

    penyewa = input("Nama Penyewa            : ")

    print("\nJenis Penginapan:")
    print("1. Hotel")
    print("2. Vila")

    jenis_choice = input("Pilih jenis (1/2): ")
    while jenis_choice not in ["1", "2"]:  # Materi: Percabangan
        jenis_choice = input("Input salah. Pilih 1 atau 2: ")

    if jenis_choice == "1":
        jenis = "Hotel"
        nama_properti = input("Nama Hotel             : ")
        nomor_kamar = input("Nomor Kamar            : ")

        # Materi: Validasi dengan kondisi
        while not nomor_kamar.isdigit():
            nomor_kamar = input("Nomor kamar harus angka: ")

    else:
        jenis = "Vila"
        nama_properti = input("Nama Vila              : ")
        nomor_kamar = "-"

    lama_menginap = input("Lama Menginap (hari)   : ")
    while not lama_menginap.isdigit():
        lama_menginap = input("Input harus angka       : ")

    harga_permalam = input("Harga per malam        : ")
    while not harga_permalam.isdigit():
        harga_permalam = input("Input harus angka       : ")

    total = int(lama_menginap) * int(harga_permalam)

    # Materi: Dictionary
    data.append({
        "id": id_sewa,
        "penyewa": penyewa,
        "jenis": jenis,
        "nama_properti": nama_properti,
        "nomor_kamar": nomor_kamar,
        "lama_menginap": lama_menginap,
        "harga_permalam": harga_permalam,
        "total": str(total),
        "status": "Booking"
    })

    save_data(data)
    print("\nPemesanan berhasil dibuat!\n")


def read_data(data):
    print("\n=== DAFTAR PEMESANAN ===")

    if not data:
        print("Belum ada data.\n")
        return

    # Materi: Perulangan For
    for d in data:
        print(f"ID Sewa         : {d['id']}")
        print(f"Penyewa         : {d['penyewa']}")
        print(f"Jenis           : {d['jenis']}")
        print(f"Nama Properti   : {d['nama_properti']}")
        print(f"Nomor Kamar     : {d['nomor_kamar']}")
        print(f"Lama Menginap   : {d['lama_menginap']} hari")
        print(f"Harga/Malam     : Rp {d['harga_permalam']}")
        print(f"Total Harga     : Rp {d['total']}")
        print(f"Status          : {d['status']}")
        print("-" * 30)


def update_data(data):
    print("\n=== UPDATE STATUS ===")
    target = input("Masukkan ID sewa: ")

    # Materi: Searching (Linear Search)
    for d in data:
        if d["id"] == target:
            print("\nStatus saat ini:", d["status"])
            print("1. Booking")
            print("2. Check-in")
            print("3. Check-out")

            pilih = input("Pilih status: ")
            while pilih not in ["1", "2", "3"]:
                pilih = input("Masukkan pilihan 1-3: ")

            if pilih == "1":
                d["status"] = "Booking"
            elif pilih == "2":
                d["status"] = "Check-in"
            else:
                d["status"] = "Check-out"

            save_data(data)
            print("Status berhasil diupdate!\n")
            return

    print("ID tidak ditemukan.\n")


def delete_data(data):
    print("\n=== HAPUS DATA ===")
    target = input("Masukkan ID sewa: ")

    # Materi: List Operation (remove)
    for d in data:
        if d["id"] == target:
            data.remove(d)
            save_data(data)
            print("Data berhasil dihapus!\n")
            return

    print("ID tidak ditemukan.\n")


# Materi: Searching + String Matching
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
        print(f"ID Sewa         : {d['id']}")
        print(f"Penyewa         : {d['penyewa']}")
        print(f"Jenis           : {d['jenis']}")
        print(f"Nama Properti   : {d['nama_properti']}")
        print(f"Nomor Kamar     : {d['nomor_kamar']}")
        print(f"Lama Menginap   : {d['lama_menginap']} hari")
        print(f"Harga/Malam     : Rp {d['harga_permalam']}")
        print(f"Total Harga     : Rp {d['total']}")
        print(f"Status          : {d['status']}")
        print("-" * 30)

    if not found:
        print("Tidak ada data yang cocok.\n")


# Materi: Sorting List
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


# Materi: Perulangan While
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


main()