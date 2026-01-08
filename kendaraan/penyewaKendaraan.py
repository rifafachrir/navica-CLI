import os
import datetime

# Konfigurasi file database
FILE_PENYEWA = "database/sewaKendaraan.txt"
FILE_KENDARAAN = "database/dataKendaraan.txt"
FILE_CUSTOMER = "database/dataCustomer.txt"
FILE_PEMBAYARAN = "database/dataPembayaran.txt"

# List Global
penyewa_list = []
kendaraan_data = []


def load_data():
    # Bersihkan list sebelum memuat data baru
    global penyewa_list, kendaraan_data
    penyewa_list.clear()
    kendaraan_data.clear()

    # 1. Load Data Sewa
    if os.path.exists(FILE_PENYEWA):
        with open(FILE_PENYEWA, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) >= 8:
                    data = {
                        "sewaId": bagian[0],
                        "customerId": bagian[1],
                        "kendaraan": bagian[2],
                        "tgl_booking": bagian[3],
                        "total": bagian[4],
                        "mulai": bagian[5],
                        "selesai": bagian[6],
                        "status": bagian[7]
                    }
                    penyewa_list.append(data)

    # 2. Load Data Mobil
    if os.path.exists(FILE_KENDARAAN):
        with open(FILE_KENDARAAN, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) >= 4:
                    mobil = {
                        "nama": bagian[2],
                        "harga": bagian[3],
                        "status": bagian[4]
                    }
                    kendaraan_data.append(mobil)


def simpan_file_sewa():
    with open(FILE_PENYEWA, "w") as f:
        for p in penyewa_list:
            line = f"{p['sewaId']}|{p['customerId']}|{p['kendaraan']}|{p['tgl_booking']}|{p['total']}|{p['mulai']}|{p['selesai']}|{p['status']}\n"
            f.write(line)

# ===== FUNGSI PEMBAYARAN =====


def simpan_ke_pembayaran_db(sewa_id, total, metode):
    # Cek jumlah data untuk generate ID
    jumlah = 0
    if os.path.exists(FILE_PEMBAYARAN):
        with open(FILE_PEMBAYARAN, "r") as f:
            jumlah = len(f.readlines())

    # Generate ID Pembayaran
    id_bayar = "PAY-K" + str(jumlah + 1).zfill(3)
    tanggal = str(datetime.date.today())
    status = "Lunas"

    # Simpan data ke file
    with open(FILE_PEMBAYARAN, "a") as f:
        f.write(f"{id_bayar}|{sewa_id}|{metode}|{total}|{tanggal}|{status}\n")


def bayar_sewa_user(customerId):
    print("\n=== PEMBAYARAN RENTAL KENDARAAN ===")

    # Cari tagihan user yang belum dibayar
    tagihan = []
    for item in penyewa_list:
        if item['customerId'] == customerId:
            if item['status'] == "booking":
                tagihan.append(item)

    if len(tagihan) == 0:
        print("Tidak ada tagihan kendaraan.")
        return

    # Tampilkan daftar tagihan
    nomor = 1
    for t in tagihan:
        print(
            f"{nomor}. Mobil: {t['kendaraan']} (Mulai: {t['mulai']}) - Rp {t['total']}")
        nomor = nomor + 1

    pilih = input("Pilih nomor tagihan: ")
    if not pilih.isdigit():
        print("Input harus angka.")
        return

    idx = int(pilih) - 1

    if idx >= 0 and idx < len(tagihan):
        data = tagihan[idx]
        print(f"\nTotal Bayar: Rp {data['total']}")
        print("Metode Pembayaran:")
        print("1. Transfer Bank")
        print("2. E-Wallet")

        metode_in = input("Pilih: ")
        metode = "Cash"
        if metode_in == "1":
            metode = "Transfer Bank"
        elif metode_in == "2":
            metode = "E-Wallet"

        yakin = input("Bayar sekarang? (y/n): ")
        if yakin == "y" or yakin == "Y":
            # Update status jadi Lunas
            data['status'] = "Lunas"
            simpan_file_sewa()

            # Catat riwayat pembayaran
            simpan_ke_pembayaran_db(data['sewaId'], data['total'], metode)
            print("Pembayaran Berhasil!")
        else:
            print("Pembayaran dibatalkan.")
    else:
        print("Pilihan nomor salah.")

# ===== FITUR UTAMA (Booking & Menu) =====


def tambah_penyewa_user(customerId):
    print("\n=== BOOKING KENDARAAN ===")

    if len(kendaraan_data) == 0:
        print("Data kendaraan kosong.")
        return

    nomor = 1
    for m in kendaraan_data:
        print(f"{nomor}. {m['nama']} - Rp {m['harga']}/hari")
        nomor = nomor + 1

    pilih = int(input("Pilih kendaraan: ")) - 1
    if pilih < 0 or pilih >= len(kendaraan_data):
        print("Pilihan salah.")
        return

    mobil_pilih = kendaraan_data[pilih]

    mulai = input("Tanggal Mulai (YYYY-MM-DD): ")
    selesai = input("Tanggal Selesai (YYYY-MM-DD): ")

    # Hitung durasi sewa
    durasi_str = input("Berapa hari sewa: ")
    if not durasi_str.isdigit():
        print("Input harus angka.")
        return
    durasi = int(durasi_str)

    total = int(mobil_pilih['harga']) * durasi
    sewa_id = "RENT" + str(len(penyewa_list) + 1).zfill(3)
    tgl_now = str(datetime.date.today())

    # Simpan data booking baru
    data_baru = {
        "sewaId": sewa_id,
        "customerId": customerId,
        "kendaraan": mobil_pilih['nama'],
        "tgl_booking": tgl_now,
        "total": str(total),
        "mulai": mulai,
        "selesai": selesai,
        "status": "booking"
    }

    penyewa_list.append(data_baru)
    simpan_file_sewa()
    print(
        f"\nBooking Berhasil! Total: Rp {total}. Silakan lakukan pembayaran.")


def lihat_riwayat(customerId):
    print("\n=== RIWAYAT KENDARAAN ===")
    ada = False
    for p in penyewa_list:
        if p['customerId'] == customerId:
            print(
                f"Mobil: {p['kendaraan']} | Status: {p['status']} | Total: {p['total']}")
            ada = True

    if not ada:
        print("Belum ada riwayat.")


def menu_customer(userId):
    load_data()  # Selalu load data saat masuk menu
    while True:
        print("\n=== MENU RENTAL KENDARAAN ===")
        print("1. Booking Kendaraan")
        print("2. Lihat Riwayat")
        print("3. Bayar Sewa")
        print("0. Kembali")

        pilihan = input("Pilih: ")
        if pilihan == "1":
            tambah_penyewa_user(userId)
        elif pilihan == "2":
            lihat_riwayat(userId)
        elif pilihan == "3":
            bayar_sewa_user(userId)
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")

# Menu Admin (Untuk melihat semua data)


def menu_penyewa_kendaraan():
    load_data()
    print("=== DATA SEMUA PENYEWA (ADMIN) ===")
    for p in penyewa_list:
        print(
            f"ID: {p['sewaId']} | User: {p['customerId']} | Status: {p['status']}")


if __name__ == "__main__":
    load_data()
    menu_penyewa_kendaraan()
