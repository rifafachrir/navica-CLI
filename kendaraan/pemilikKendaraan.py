import kendaraan.penyewaKendaraan as penyewaKendaraan
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

data_pemilik = []
kendaraan_data = []

FILE_KENDARAAN = "database/dataKendaraan.txt"
FILE_MITRA = "database/dataMitra.txt"

file_exists = os.path.exists(FILE_KENDARAAN) and os.path.exists(FILE_MITRA)


def load_data():
    global kendaraan_data, data_pemilik
    kendaraan_data.clear()
    data_pemilik.clear()

    if os.path.exists(FILE_KENDARAAN) and os.path.exists(FILE_MITRA):
        valid_mitra_ids = set()

        # Load Data Kendaraan
        with open(FILE_KENDARAAN, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) == 5:
                    valid_mitra_ids.add(bagian[1])
                    kendaraan_data.append({
                        "noKendaraan": bagian[0],
                        "mitraId": bagian[1],
                        "namaKendaraan": bagian[2],
                        "hargaSewaPerHari": bagian[3],
                        "status": bagian[4]
                    })
                else:
                    # print("Format data kendaraan tidak valid:", line) # Optional: uncomment for debug
                    continue

        # Load Data Mitra
        with open(FILE_MITRA, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                # Ambil semua mitra agar admin bisa lihat, nanti difilter jika perlu
                if len(bagian) >= 4:
                    data_pemilik.append({
                        "mitraId": bagian[0],
                        "userId": bagian[1],
                        "namaMitra": bagian[2],
                        "alamat": bagian[3],
                    })
                else:
                    # print("Format data mitra tidak valid:", line) # Optional: uncomment for debug
                    continue
    else:
        print("File database tidak ditemukan.")


def tambah_kendaraan():
    load_data()  # Reload data terbaru
    print("\n=== Tambah Data Kendaraan ===")

    noKendaraan = input("Masukkan no Polisi Kendaraan: ")

    # Tampilkan mitra untuk dipilih
    if not data_pemilik:
        print("Data mitra kosong.")
        return

    for i, mitra in enumerate(data_pemilik):
        print(f"{i + 1}. {mitra['namaMitra']} (ID: {mitra['mitraId']})")

    try:
        pilihan = int(
            input("Pilih mitra yang ingin menambahkan kendaraan: ")) - 1
        if 0 <= pilihan < len(data_pemilik):
            mitraId = data_pemilik[pilihan]['mitraId']
        else:
            print("Pilihan tidak valid.")
            return
    except ValueError:
        print("Input harus angka.")
        return

    nama_kendaraan = input("Nama Kendaraan: ")
    harga_sewa = input("Harga Sewa per Hari: ")

    kendaraan = {
        "noKendaraan": noKendaraan,
        "mitraId": mitraId,
        "namaKendaraan": nama_kendaraan,
        "hargaSewaPerHari": harga_sewa,
        "status": "tersedia"
    }

    kendaraan_data.append(kendaraan)

    with open(FILE_KENDARAAN, "a") as f:
        f.write(f"{noKendaraan}|{mitraId}|{nama_kendaraan}|{harga_sewa}|tersedia\n")

    print("Data kendaraan berhasil ditambahkan!\n")


def tambah_kendaraan_by_mitraId(mitraId):
    print("\n=== Tambah Data Kendaraan ===")
    noKendaraan = input("Masukkan no Polisi Kendaraan: ")
    nama_kendaraan = input("Nama Kendaraan: ")
    harga_sewa = input("Harga Sewa per Hari: ")

    kendaraan = {
        "noKendaraan": noKendaraan,
        "mitraId": mitraId,
        "namaKendaraan": nama_kendaraan,
        "hargaSewaPerHari": harga_sewa,
        "status": "tersedia"
    }

    kendaraan_data.append(kendaraan)

    with open(FILE_KENDARAAN, "a") as f:
        f.write(f"{noKendaraan}|{mitraId}|{nama_kendaraan}|{harga_sewa}|tersedia\n")

    print("Data kendaraan berhasil ditambahkan!\n")


def lihat_kendaraan():
    load_data()
    print("\n=== Daftar Data Kendaraan (Semua) ===")
    if len(kendaraan_data) == 0:
        print("Belum ada data kendaraan.\n")
        return

    for i, k in enumerate(kendaraan_data):
        print(f"{1+i}")
        print(f"noPolisi: {k['noKendaraan']}")

        # Cari nama mitra pemilik kendaraan ini
        nama_mitra = "Tidak Diketahui"
        for m in data_pemilik:
            if m['mitraId'] == k['mitraId']:
                nama_mitra = m['namaMitra']
                break

        print(f"Nama Mitra: {nama_mitra}")
        print(f"namaKendaraan: {k['namaKendaraan']}")
        print(f"hargaSewaPerHari: {k['hargaSewaPerHari']}")
        print(f"status: {k['status']}")
        print("-" * 30)


def lihat_kendaraan_by_mitraId(mitraId):
    load_data()
    print("\n=== Daftar Data Kendaraan Anda ===")

    kendaraan_saya = [k for k in kendaraan_data if k['mitraId'] == mitraId]

    if not kendaraan_saya:
        print("Belum ada data kendaraan.\n")
        return

    for i, k in enumerate(kendaraan_saya):
        print(f"{i+1}")
        print(f"noPolisi: {k['noKendaraan']}")
        print(f"namaKendaraan: {k['namaKendaraan']}")
        print(f"hargaSewaPerHari: {k['hargaSewaPerHari']}")
        print(f"status: {k['status']}")
        print("-" * 30)


def edit_kendaraan():
    load_data()
    lihat_kendaraan()
    if not kendaraan_data:
        return

    try:
        index = int(input("Pilih nomor data yang ingin diedit: ")) - 1
        if index < 0 or index >= len(kendaraan_data):
            print("Nomor tidak valid!")
            return
    except ValueError:
        print("Input harus angka.")
        return

    k = kendaraan_data[index]
    print(
        f"\n--- Ubah data: {k['namaKendaraan']} (Enter jika tidak ingin mengubah) ---")

    noKendaraan = input(f"No Polisi ({k['noKendaraan']}): ")

    # Tampilkan mitra untuk dipilih
    mitraId_baru = None
    print(f"Mitra saat ini ID: {k['mitraId']}")
    ubah_mitra = input("Ubah mitra? (y/n): ").lower()
    if ubah_mitra == 'y':
        for i, mitra in enumerate(data_pemilik):
            print(f"{i + 1}. {mitra['namaMitra']} (ID: {mitra['mitraId']})")
        try:
            pilihan = int(input("Pilih mitra baru: ")) - 1
            if 0 <= pilihan < len(data_pemilik):
                mitraId_baru = data_pemilik[pilihan]['mitraId']
            else:
                print("Pilihan tidak valid.")
        except ValueError:
            print("Input harus angka.")

    nama_kendaraan = input(f"Nama Kendaraan ({k['namaKendaraan']}): ")
    harga_sewa = input(f"Harga Sewa ({k['hargaSewaPerHari']}): ")

    # Update data di list memory
    if noKendaraan:
        k['noKendaraan'] = noKendaraan
    if mitraId_baru:
        k['mitraId'] = mitraId_baru
    if nama_kendaraan:
        k['namaKendaraan'] = nama_kendaraan
    if harga_sewa:
        k['hargaSewaPerHari'] = harga_sewa

    with open(FILE_KENDARAAN, "w") as f:
        for item in kendaraan_data:
            f.write(
                f"{item['noKendaraan']}|{item['mitraId']}|{item['namaKendaraan']}|{item['hargaSewaPerHari']}|{item['status']}\n")

    print("Data kendaraan berhasil diperbarui!\n")


def hapus_kendaraan():
    load_data()
    lihat_kendaraan()
    if not kendaraan_data:
        return

    try:
        index = int(input("Pilih nomor data yang ingin dihapus: ")) - 1
        if index < 0 or index >= len(kendaraan_data):
            print("Nomor tidak valid!")
            return
    except ValueError:
        print("Input harus angka.")
        return

    kendaraan_data.pop(index)

    with open(FILE_KENDARAAN, "w") as f:
        for k in kendaraan_data:
            f.write(
                f"{k['noKendaraan']}|{k['mitraId']}|{k['namaKendaraan']}|{k['hargaSewaPerHari']}|{k['status']}\n")
    print("Data kendaraan berhasil dihapus!\n")


def menuAdmin():
    load_data()
    while True:
        print("\n=== MENU ADMIN KENDARAAN ===")
        print("1. Tambah Kendaraan")
        print("2. Lihat Semua Kendaraan")
        print("3. Edit Kendaraan")
        print("4. Hapus Kendaraan")
        print("5. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1":
            tambah_kendaraan()
        elif pilih == "2":
            lihat_kendaraan()
        elif pilih == "3":
            edit_kendaraan()
        elif pilih == "4":
            hapus_kendaraan()
        elif pilih == "5":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!\n")


if __name__ == "__main__":
    menuAdmin()
else:
    load_data()
