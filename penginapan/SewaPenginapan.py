import os
import datetime

# Konfigurasi file database
FILE_SEWA = "database/sewaPenginapan.txt"
FILE_PEMBAYARAN = "database/dataPembayaran.txt"
FILE_KAMAR = "database/DataKamarPenginapan.txt"
FILE_PENGINAPAN = "database/DataPenginapan.txt"
FILE_CUSTOMER = "database/dataCustomer.txt"

# List Global untuk menampung data
kamar_list = []
penginapan_list = []
data_sewa = []
customer = []


def load_data():
    # Bersihkan list sebelum memuat data baru
    global kamar_list, penginapan_list, data_sewa, customer
    kamar_list.clear()
    penginapan_list.clear()
    data_sewa.clear()
    customer.clear()

    # 1. Load Data Kamar
    if os.path.exists(FILE_KAMAR):
        with open(FILE_KAMAR, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) == 7:
                    kamar = {
                        "id": int(bagian[0]),
                        "penginapan_id": int(bagian[1]),
                        "nama": bagian[2],
                        "tipe": bagian[3],
                        "harga": int(bagian[4]),
                        "kapasitas": int(bagian[5]),
                        "status": bagian[6]
                    }
                    kamar_list.append(kamar)

    # 2. Load Data Penginapan
    if os.path.exists(FILE_PENGINAPAN):
        with open(FILE_PENGINAPAN, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) == 5:
                    tempat = {
                        "penginapanId": int(bagian[0]),
                        "mitraId": int(bagian[1]),
                        "namaPenginapan": bagian[2]
                    }
                    penginapan_list.append(tempat)

    # 3. Load Data Sewa
    if os.path.exists(FILE_SEWA):
        with open(FILE_SEWA, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) >= 9:
                    status_sewa = "Booking"
                    if len(bagian) > 9:
                        status_sewa = bagian[9]

                    sewa = {
                        "id": bagian[0],
                        "penyewa": bagian[1],
                        "jenis": bagian[2],
                        "nama_properti": bagian[3],
                        "kode_kamar": bagian[4],
                        "tanggal_mulai": bagian[5],
                        "lama_menginap": bagian[6],
                        "harga_permalam": bagian[7],
                        "total": bagian[8],
                        "status": status_sewa
                    }
                    data_sewa.append(sewa)

    # 4. Load Data Customer
    if os.path.exists(FILE_CUSTOMER):
        with open(FILE_CUSTOMER, "r", encoding="utf-8") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) == 5:
                    cust = {
                        "idCustomer": bagian[0],
                        "idUser": bagian[1],
                        "nama": bagian[2]
                    }
                    customer.append(cust)


def load_kamar_by_penginapan(penginapan_id):
    hasil = []
    for k in kamar_list:
        if k["penginapan_id"] == penginapan_id:
            hasil.append(k)
    return hasil


def update_status_kamar(kamar_id, status_baru):
    # Ubah status di list
    for k in kamar_list:
        if k["id"] == kamar_id:
            k["status"] = status_baru
            break

    # Simpan perubahan ke file
    with open(FILE_KAMAR, "w") as f:
        for k in kamar_list:
            line = f"{k['id']}|{k['penginapan_id']}|{k['nama']}|{k['tipe']}|{k['harga']}|{k['kapasitas']}|{k['status']}\n"
            f.write(line)


def save_data_sewa():
    with open(FILE_SEWA, "w") as f:
        for d in data_sewa:
            line = f"{d['id']}|{d['penyewa']}|{d['jenis']}|{d['nama_properti']}|{d['kode_kamar']}|{d['tanggal_mulai']}|{d['lama_menginap']}|{d['harga_permalam']}|{d['total']}|{d['status']}\n"
            f.write(line)


def generate_id_sewa():
    nomor = len(data_sewa) + 1
    return "NAV" + str(nomor).zfill(3)

# ===== FUNGSI PEMBAYARAN =====


def simpan_ke_pembayaran_db(sewa_id, total, metode):
    # Cek jumlah data untuk membuat ID baru
    jumlah_data = 0
    if os.path.exists(FILE_PEMBAYARAN):
        with open(FILE_PEMBAYARAN, "r") as f:
            lines = f.readlines()
            jumlah_data = len(lines)

    # Generate ID Pembayaran
    id_bayar = "PAY" + str(jumlah_data + 1).zfill(3)
    tgl_sekarang = str(datetime.date.today())
    status = "Lunas"

    # Format data sesuai ERD
    data_string = f"{id_bayar}|{sewa_id}|{metode}|{total}|{tgl_sekarang}|{status}\n"

    # Simpan ke file
    with open(FILE_PEMBAYARAN, "a") as f:
        f.write(data_string)


def bayar_pesanan_user(customerId):
    print("\n=== PEMBAYARAN PENGINAPAN ===")

    # Cari tagihan user yang belum dibayar
    tagihan_saya = []

    for item in data_sewa:
        if item['penyewa'] == customerId:
            if item['status'] == "Booking":
                tagihan_saya.append(item)

    if len(tagihan_saya) == 0:
        print("Tidak ada tagihan yang harus dibayar.")
        return

    # Tampilkan daftar tagihan
    print("Daftar Tagihan Anda:")
    nomor = 1
    for t in tagihan_saya:
        print(f"{nomor}. Hotel: {t['nama_properti']} | Total: Rp {t['total']}")
        nomor = nomor + 1

    # Proses pembayaran
    pilihan_str = input("Pilih nomor tagihan: ")
    if not pilihan_str.isdigit():
        print("Input harus angka.")
        return

    pilihan = int(pilihan_str) - 1

    if pilihan >= 0 and pilihan < len(tagihan_saya):
        data_dipilih = tagihan_saya[pilihan]

        print(f"\nTotal Tagihan: Rp {data_dipilih['total']}")
        print("Metode Pembayaran:")
        print("1. Transfer Bank")
        print("2. E-Wallet")

        metode_input = input("Pilih (1/2): ")
        metode = "Cash"
        if metode_input == "1":
            metode = "Transfer Bank"
        elif metode_input == "2":
            metode = "E-Wallet"

        yakin = input("Bayar sekarang? (y/n): ")
        if yakin == "y" or yakin == "Y":
            # Update status jadi Lunas
            data_dipilih['status'] = "Lunas"

            # Simpan update ke file sewa
            save_data_sewa()

            # Catat riwayat pembayaran
            simpan_ke_pembayaran_db(
                data_dipilih['id'], data_dipilih['total'], metode)

            print("Pembayaran Berhasil! Status pesanan sudah Lunas.")
        else:
            print("Batal bayar.")
    else:
        print("Nomor pilihan salah.")

# ===== FITUR UTAMA (Booking & Menu) =====


def bookingCustomer(customerId):
    print("\n=== BOOKING PENGINAPAN ===")

    if len(penginapan_list) == 0:
        print("Data penginapan kosong.")
        return

    nomor = 1
    for p in penginapan_list:
        print(f"{nomor}. {p['namaPenginapan']}")
        nomor = nomor + 1

    pilih_p = int(input("Pilih nomor penginapan: ")) - 1
    if pilih_p < 0 or pilih_p >= len(penginapan_list):
        print("Pilihan salah.")
        return

    id_penginapan = penginapan_list[pilih_p]['penginapanId']

    # Cari kamar yang tersedia
    kamar_tersedia = []
    for k in kamar_list:
        if k['penginapan_id'] == id_penginapan:
            if k['status'] == "tersedia":
                kamar_tersedia.append(k)

    if len(kamar_tersedia) == 0:
        print("Kamar penuh atau tidak ada.")
        return

    print("\n--- Pilih Kamar ---")
    nomor = 1
    for k in kamar_tersedia:
        print(f"{nomor}. {k['nama']} ({k['tipe']}) - Rp {k['harga']}")
        nomor = nomor + 1

    pilih_k = int(input("Pilih nomor kamar: ")) - 1
    if pilih_k < 0 or pilih_k >= len(kamar_tersedia):
        return

    kamar_fix = kamar_tersedia[pilih_k]

    tgl = input("Tanggal Menginap (YYYY-MM-DD): ")
    lama = input("Lama Menginap (hari): ")

    total_harga = int(lama) * int(kamar_fix['harga'])
    id_baru = generate_id_sewa()

    # Simpan data booking baru
    data_baru = {
        "id": id_baru,
        "penyewa": customerId,
        "jenis": kamar_fix['tipe'],
        "nama_properti": kamar_fix['nama'],
        "kode_kamar": str(kamar_fix['id']),
        "tanggal_mulai": tgl,
        "lama_menginap": lama,
        "harga_permalam": str(kamar_fix['harga']),
        "total": str(total_harga),
        "status": "Booking"
    }

    data_sewa.append(data_baru)
    save_data_sewa()

    # Update status kamar
    update_status_kamar(kamar_fix['id'], "booking")

    print("\n>>> Booking Berhasil! Silakan masuk menu Pembayaran.")


def read_data_user(customerId):
    print("\n=== RIWAYAT PESANAN ===")
    ada = False
    for d in data_sewa:
        if d['penyewa'] == customerId:
            print(
                f"ID: {d['id']} | Hotel: {d['nama_properti']} | Total: {d['total']} | Status: {d['status']}")
            ada = True

    if not ada:
        print("Belum ada riwayat.")


def userMenu(customerId):
    load_data()
    while True:
        print("\n=== MENU USER PENGINAPAN ===")
        print("1. Booking Kamar")
        print("2. Lihat Riwayat")
        print("3. Bayar Pesanan")
        print("0. Kembali")

        pilihan = input("Pilih: ")
        if pilihan == "1":
            bookingCustomer(customerId)
        elif pilihan == "2":
            read_data_user(customerId)
        elif pilihan == "3":
            bayar_pesanan_user(customerId)
        elif pilihan == "0":
            break
        else:
            print("Pilihan salah.")


def main():
    load_data()
    # Menampilkan semua data sewa (Admin)
    for d in data_sewa:
        print(d)


if __name__ == "__main__":
    load_data()
    main()
