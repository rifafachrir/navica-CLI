import os
import datetime

# Konfigurasi file database
FILE_PENYEWA = "database/sewaKendaraan.txt"
FILE_KENDARAAN = "database/dataKendaraan.txt"
FILE_CUSTOMER = "database/dataCustomer.txt"
FILE_PEMBAYARAN = "database/dataPembayaran.txt"

# List Global
penyewa_list = []
customer_data = []
kendaraan_data = []
pembayaran_data = []

def input_tanggal(prompt):
    while True:
        tgl = input(prompt).strip()

        if tgl == "":
            print("Tanggal tidak boleh kosong!")
            continue

        # cek format dasar YYYY-MM-DD
        bagian = tgl.split("-")
        if len(bagian) != 3:
            print("Format tanggal salah! Gunakan YYYY-MM-DD")
            continue

        if not (bagian[0].isdigit() and bagian[1].isdigit() and bagian[2].isdigit()):
            print("Tanggal harus angka! (YYYY-MM-DD)")
            continue

        tahun, bulan, hari = int(bagian[0]), int(bagian[1]), int(bagian[2])

        if not (1 <= bulan <= 12):
            print("Bulan harus 1-12!")
            continue

        if not (1 <= hari <= 31):
            print("Hari harus 1-31!")
            continue

        # VALID → return
        return tgl

def load_data():
    # Bersihkan list sebelum memuat data baru
    global penyewa_list, kendaraan_data
    penyewa_list.clear()
    kendaraan_data.clear()
    customer_data.clear()
    pembayaran_data.clear()

    # 1. Load Data Sewa
    if os.path.exists(FILE_PENYEWA):
        with open(FILE_PENYEWA, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                tgl_mulai = datetime.datetime.strptime(bagian[5], "%Y-%m-%d")
                tgl_selesai = datetime.datetime.strptime(bagian[6], "%Y-%m-%d")

                lama_sewa = (tgl_selesai - tgl_mulai).days

                if len(bagian) >= 8:
                    data = {
                    "sewaId": bagian[0],
                    "customerId": bagian[1],
                    "kendaraanYangDisewa": bagian[2],
                    "tanggal_booking": bagian[3],
                    "total_harga": int(bagian[4]),
                    "tanggalMulai": bagian[5],
                    "TanggalSelesai": bagian[6],
                    "lama_sewa": lama_sewa,
                    "statusSewa": bagian[7],
                    }
                    penyewa_list.append(data)

    # 2. Load Data Mobil
    if os.path.exists(FILE_CUSTOMER):
        with open(FILE_CUSTOMER, "r") as f:
            for line in f:
                bagian = line.strip().split("|")
                if len(bagian) == 5:
                    customer_data.append({
                        "customerId": bagian[0],
                        'idUser': bagian[1],
                        "nama": bagian[2],
                        "email": bagian[3],
                        "noTelp": bagian[4]
                    })
                else:
                    print("Format data customer tidak valid:", line)
                    continue
        
    if os.path.exists(FILE_KENDARAAN):
        with open("database/dataKendaraan.txt", "r") as f:
            for line in f:
                bagian = line.strip().split("|")
                if len(bagian) == 5:
                    kendaraan_data.append({
                        "noKendaraan": bagian[0],
                        "mitraId": bagian[1],
                        "namaKendaraan": bagian[2],
                        "hargaSewaPerHari": bagian[3],
                        "status": bagian[4]
                    })
                # if len(bagian) >= 4:
                #     mobil = {
                #         "nama": bagian[2],
                #         "harga": bagian[3],
                        # "status": bagian[4]
                    # }
                    # kendaraan_data.append(mobil)
        with open(FILE_PEMBAYARAN, 'r') as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) == 6:
                    pembayaran_data.append({
                        "idBayar": bagian[0],
                        "sewaId": bagian[1],
                        "metode": bagian[2],
                        "total": bagian[3],
                        "tanggal": bagian[4],
                        "status": bagian[5]
                    })
                else:
                    print("Format data pembayaran tidak valid:", line)
                    continue


def simpan_file_sewa():
    with open(FILE_PENYEWA, "w") as f:
        for p in penyewa_list:
            line = f"{p['sewaId']}|{p['customerId']}|{p['kendaraanYangDisewa']}|{p['tanggal_booking']}|{p['total_harga']}|{p['tanggalMulai']}|{p['TanggalSelesai']}|{p['statusSewa']}|\n"
            f.write(line)
def pick_customer():
    print("=== Pilih Customer ===")
    for i, customer in enumerate(customer_data):
        print(f"{i + 1}. {customer['nama']} (ID: {customer['customerId']})")
    pilihan = input("Masukkan nomor customer: ").strip()
    if pilihan == "":
        return None
    if not pilihan.isdigit():
        print("Input harus angka!")
        return None

    pilihan = int(pilihan) - 1
    if 0 <= pilihan < len(customer_data):
        return customer_data[pilihan]['customerId']
    else:
        print("Pilihan tidak valid.")
        return None

    if 0 <= pilihan < len(customer_data):
        return customer_data[pilihan]['customerId']
    else:
        print("Pilihan tidak valid.")
        return None

def pick_kendaraan():
    print("=== Pilih Kendaraan ===")
    for i, kendaraan in enumerate(kendaraan_data):
        print(f"{i + 1}. {kendaraan['namaKendaraan']} , Rp. {kendaraan['hargaSewaPerHari']}/hari")
    pilihan = input("Masukkan nomor kendaraan: ").strip()
    if pilihan == "":
        return None, None
    if not pilihan.isdigit():
        print("Input harus angka!")
        return None, None

    pilihan = int(pilihan) - 1

    if 0 <= pilihan < len(kendaraan_data):
        return kendaraan_data[pilihan]['noKendaraan'], kendaraan_data[pilihan]['hargaSewaPerHari']
    else:
        print("Pilihan tidak valid.")
        return None
    
def cek_ketersediaan_kendaraan(kendaraan, tanggalMulai, TanggalSelesai):
    tanggalMulaiBaru = datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")
    TanggalSelesaiBaru = datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d")
    
    for penyewa in penyewa_list:
        if penyewa['kendaraanYangDisewa'] == kendaraan and penyewa["statusSewa"] != "selesai":
            tanggalMulaiYangAda = datetime.datetime.strptime(penyewa['tanggalMulai'], "%Y-%m-%d")
            tanggalSelesaiYangAda = datetime.datetime.strptime(penyewa['TanggalSelesai'], "%Y-%m-%d")
                
    if tanggalMulaiBaru <= tanggalSelesaiYangAda and tanggalMulaiYangAda <= TanggalSelesaiBaru:
            return False
    return True

# ===== FUNGSI PEMBAYARAN =====

def filter_pembayaran_by_bayarId(bayarId):
    single_pembayaran_data = []
    with open(FILE_PEMBAYARAN, 'r') as f:
        lines = f.readlines()
        for line in lines:
            bagian = line.strip().split("|")
            if bagian[0] == bayarId:
                single_pembayaran_data.append({
                    "idBayar": bagian[0],
                    "sewaId": bagian[1],
                    "metode": bagian[2],
                    "total": bagian[3],
                    "tanggal": bagian[4],
                    "status": bagian[5]
                })

def create_pembayaran(sewa_id, total):
    print("\n=== PEMBAYARAN RENTAL KENDARAAN ===")
    jumlah = 0
    with open(FILE_PEMBAYARAN, "r") as f:
        jumlah = len(f.readlines())
    idBayar = "PAY-K" + str(jumlah + 1).zfill(3)
    status = "belum bayar"

    with open(FILE_PEMBAYARAN, "a") as f:
        f.write(f"{idBayar}|{sewa_id}|-|{total}|-|{status}\n")
    return idBayar


def simpan_ke_pembayaran_db(id_bayar, metode, status):
    tgl_sekarang = str(datetime.date.today().strftime("%Y-%m-%d"))
    
    for p in pembayaran_data:
        if p["idBayar"] == id_bayar:
            p["metode"] = metode
            p["tanggal"] = tgl_sekarang
            p["status"] = status
            break
    # Simpan data
    with open(FILE_PEMBAYARAN, "w") as f:
        for p in pembayaran_data:
            f.write(f"{p['idBayar']}|{p['sewaId']}|{p['metode']}|{p['total']}|{p['tanggal']}|{p['status']}\n")



def bayar_sewa_user(idBayar):
    print("\n=== PEMBAYARAN RENTAL KENDARAAN ===")

    # Cari tagihan user yang belum dibayar
    # tagihan = []
    # for item in penyewa_list:
    #     if item['customerId'] == customerId:
    #         if item['status'] == "booking":
    #             tagihan.append(item)

    # if len(tagihan) == 0:
    #     print("Tidak ada tagihan kendaraan.")
    #     return

    # # Tampilkan daftar tagihan
    # nomor = 1
    # for t in tagihan:
    #     print(
    #         f"{nomor}. Mobil: {t['kendaraan']} (Mulai: {t['mulai']}) - Rp {t['total']}")
    #     nomor = nomor + 1

    # pilih = input("Pilih nomor tagihan: ")
    # if not pilih.isdigit():
    #     print("Input harus angka.")
    #     return

    # idx = int(pilih) - 1

    # if idx >= 0 and idx < len(tagihan):
    #     data = tagihan[idx]
    #     print(f"\nTotal Bayar: Rp {data['total']}")
    #     print("Metode Pembayaran:")
    #     print("1. Transfer Bank")
    #     print("2. E-Wallet")

    #     metode_in = input("Pilih: ")
    #     metode = "Cash"
    #     if metode_in == "1":
    #         metode = "Transfer Bank"
    #     elif metode_in == "2":
    #         metode = "E-Wallet"

    #     yakin = input("Bayar sekarang? (y/n): ")
    #     if yakin == "y" or yakin == "Y":
    #         # Update status jadi Lunas
    #         data['status'] = "Lunas"
    #         simpan_file_sewa()

    #         # Catat riwayat pembayaran
    #         simpan_ke_pembayaran_db(data['sewaId'], data['total'], metode)
    #         print("Pembayaran Berhasil!")
    #     else:
    #         print("Pembayaran dibatalkan.")
    # else:
    #     print("Pilihan nomor salah.")
    if idBayar == None:
        bayarId = input("Masukkan kode pembayaran Anda: ")
    else: 
        bayarId = idBayar

    for p in pembayaran_data:
        if p["idBayar"] == bayarId:
            if p["status"] == "belum bayar":
                print(f"\nTotal Bayar: Rp {p['total']}")
                print("Metode Pembayaran:")
                print("1. Transfer Bank")
                print("2. E-Wallet")

                metode_in = input("Pilih: ")
                metode = "Cash"
                if metode_in == "1":
                    metode = "Transfer Bank"
                elif metode_in == "2":
                    metode = "E-Wallet"


                yakin = input("Bayar sekarang? (y/n): ").lower()
                if yakin == "y":
                    simpan_ke_pembayaran_db(bayarId, metode, "Lunas")
                    print("Pembayaran Berhasil!")

                else:
                    print("Pembayaran dibatalkan.")


            else: 
                print("Kode pembayaran ini sudah Lunas.")



    

# ===== FITUR UTAMA (Booking & Menu) =====


# def tambah_penyewa_user(customerId):
#     print("\n=== BOOKING KENDARAAN ===")

#     if len(kendaraan_data) == 0:
#         print("Data kendaraan kosong.")
#         return

#     nomor = 1
#     for m in kendaraan_data:
#         print(f"{nomor}. {m['namaKendaraan']} - Rp {m['hargaSewaPerHari']}/hari")
#         nomor = nomor + 1

#     pilih = int(input("Pilih kendaraan: ")) - 1
#     if pilih < 0 or pilih >= len(kendaraan_data):
#         print("Pilihan salah.")
#         return

#     mobil_pilih = kendaraan_data[pilih]

#     mulai = input("Tanggal Mulai (YYYY-MM-DD): ")
#     selesai = input("Tanggal Selesai (YYYY-MM-DD): ")

#     # Hitung durasi sewa
#     durasi_str = input("Berapa hari sewa: ")
#     if not durasi_str.isdigit():
#         print("Input harus angka.")
#         return
#     durasi = int(durasi_str)

#     total = int(mobil_pilih['harga']) * durasi
#     sewa_id = "RENT" + str(len(penyewa_list) + 1).zfill(3)
#     tgl_now = str(datetime.date.today())

#     # Simpan data booking baru
#     data_baru = {
#         "sewaId": sewa_id,
#         "customerId": customerId,
#         "kendaraan": mobil_pilih['nama'],
#         "tgl_booking": tgl_now,
#         "total": str(total),
#         "mulai": mulai,
#         "selesai": selesai,
#         "status": "booking"
#     }

#     penyewa_list.append(data_baru)
#     simpan_file_sewa()
#     print(
#         f"\nBooking Berhasil! Total: Rp {total}. Silakan lakukan pembayaran.")
    
# TODO: perlihatkan data penyewa berdasarkan tanggal
def tambah_penyewa():
    print("\n=== Tambah Data Penyewa ===")
    sewaId = "p" + str(len(penyewa_list) + 1).zfill(3)
    customerId = pick_customer()
    kendaraan, harga_per_hari = pick_kendaraan()
    tanggal_booking = datetime.date.today().strftime("%Y-%m-%d")
    tanggalMulai = input_tanggal("Tanggal Mulai Sewa (YYYY-MM-DD): ")
    TanggalSelesai = input_tanggal("Tanggal Selesai Sewa (YYYY-MM-DD): ")
    if cek_ketersediaan_kendaraan(kendaraan, tanggalMulai, TanggalSelesai):
        print(" Kendaraan tersedia!")
    else:
        print(f"kendaraan: {kendaraan} . Tidak tersedia pada tanggal tersebut")
        return
    lama_sewa = (datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d") - datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")).days
    total_harga = int(harga_per_hari) * lama_sewa

    bayarId = create_pembayaran(sewaId, total_harga)

    data = {
        "sewaId": sewaId,
        "customerId": customerId,
        "kendaraanYangDisewa": kendaraan,
        "tanggal_booking": tanggal_booking,
        "total_harga": total_harga,
        "tanggalMulai": tanggalMulai,
        "TanggalSelesai": TanggalSelesai,
        "lama_sewa": lama_sewa,
        "statusSewa": "booking",
    }

    penyewa_list.append(data)
    simpan_file_sewa()
    print(">> Data berhasil ditambahkan!\n")
    print("Silahkan lakukan pembayaran untuk melakukan penyewaan kendaraan.")
    bayar_sewa_user(bayarId)
    print("kode pembayaran anda adalah: ", bayarId)

def tambah_penyewa_customer(customerId):
    print("\n=== Tambah Data Penyewa ===")
    sewaId = "p" + str(len(penyewa_list) + 1).zfill(3)
    kendaraan, harga_per_hari = pick_kendaraan()
    tanggal_booking = datetime.date.today().strftime("%Y-%m-%d")
    tanggalMulai = input_tanggal("Tanggal Mulai Sewa (YYYY-MM-DD): ")
    TanggalSelesai = input_tanggal("Tanggal Selesai Sewa (YYYY-MM-DD): ")
    if cek_ketersediaan_kendaraan(kendaraan, tanggalMulai, TanggalSelesai):
        print(" Kendaraan tersedia!")
    else:
        print(f"kendaraan: {kendaraan} . Tidak tersedia pada tanggal tersebut")
        return
    lama_sewa = (datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d") - datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")).days
    total_harga = int(harga_per_hari) * lama_sewa

    bayarId = create_pembayaran(sewaId, total_harga)

    data = {
        "sewaId": sewaId,
        "customerId": customerId,
        "kendaraanYangDisewa": kendaraan,
        "tanggal_booking": tanggal_booking,
        "total_harga": total_harga,
        "tanggalMulai": tanggalMulai,
        "TanggalSelesai": TanggalSelesai,
        "lama_sewa": lama_sewa,
        "statusSewa": "booking",
    }

    penyewa_list.append(data)
    simpan_file_sewa()
    print(">> Data berhasil ditambahkan!\n")
    print("Silahkan lakukan pembayaran untuk melakukan penyewaan kendaraan.")
    bayar_sewa_user(bayarId)
    print("kode pembayaran anda adalah: ", bayarId)

def lihat_penyewa():
    print("\n=== Daftar Penyewa ===")
    if not penyewa_list:
        print("Belum ada data penyewa.\n")
        return

    for i, p in enumerate(penyewa_list):
        print(f"{1+i}")
        print(f"id sewa : {p['sewaId']}")
        for c in customer_data:
            if c['customerId'] == p['customerId']:                print(f"Nama Penyewa: {c['nama']}")
        for k in kendaraan_data:
            if k['noKendaraan'] == p['kendaraanYangDisewa']:
                print(f"Nama Kendaraan: {k['namaKendaraan']}")
        print(f"Tanggal Booking: {p['tanggal_booking']}")
        print(f"Total Harga: {p['total_harga']}")
        print(f"Tanggal Mulai: {p['tanggalMulai']}")
        print(f"Tanggal Selesai: {p['TanggalSelesai']}")
        print(f"Lama Sewa: {p['lama_sewa']} hari")
        print(f"Status Sewa: {p['statusSewa']}")
        for b in pembayaran_data:
            if b['sewaId'] == p['sewaId']:
                print(f"Metode Pembayaran: {b['status']}")


    print("-" * 30)

def lihat_riwayat(customerId):
    print("\n=== RIWAYAT KENDARAAN ===")
 
    for i, p in enumerate(penyewa_list):
        if p['customerId'] != customerId:
            print(f"{1+i}")
            print(f"id sewa : {p['sewaId']}")
            for c in customer_data:
                if c['customerId'] == p['customerId']:                    print(f"Nama Penyewa: {c['nama']}")
            for k in kendaraan_data:
                if k['noKendaraan'] == p['kendaraanYangDisewa']:
                    print(f"Nama Kendaraan: {k['namaKendaraan']}")
            print(f"Tanggal Booking: {p['tanggal_booking']}")
            print(f"Total Harga: {p['total_harga']}")
            print(f"Tanggal Mulai: {p['tanggalMulai']}")
            print(f"Tanggal Selesai: {p['TanggalSelesai']}")
            print(f"Lama Sewa: {p['lama_sewa']} hari")
            print(f"Status Sewa: {p['statusSewa']}")
            for b in pembayaran_data:
                if b['sewaId'] == p['sewaId']:
                    print(f"Metode Pembayaran: {b['status']}")

    print("-" * 30)

def lihat_penyewa_by_customer_id(customerId):
    print("\n === Daftar Riwayat peminjaman ===")
    if not penyewa_list:
        print("Belum ada riwayat menyewa kendaraan. \n")
        return
        
    for i, p in enumerate(penyewa_list):
        if p['customerId'] == customerId:
            print(f"{1+i}")
            print(f"id sewa : {p['sewaId']}")
            for c in customer_data:
                if c['customerId'] == p['customerId']:                    print(f"Nama Penyewa: {c['nama']}")
            for k in kendaraan_data:
                if k['noKendaraan'] == p['kendaraanYangDisewa']:
                    print(f"Nama Kendaraan: {k['namaKendaraan']}")
            print(f"Tanggal Booking: {p['tanggal_booking']}")
            print(f"Total Harga: {p['total_harga']}")
            print(f"Tanggal Mulai: {p['tanggalMulai']}")
            print(f"Tanggal Selesai: {p['TanggalSelesai']}")
            print(f"Lama Sewa: {p['lama_sewa']} hari")
            print(f"Status Sewa: {p['statusSewa']}")
            for b in pembayaran_data:
                if b['sewaId'] == p['sewaId']:
                    print(f"Metode Pembayaran: {b['status']}")
            print("-" * 30)
    
def lihat_penyewa_by_mitraId(mitraId):
    print("\n === Daftar Riwayat peminjaman ===")
    if not penyewa_list:
        print("Belum ada riwayat menyewa kendaraan. \n")
        return
        
    for i, p in enumerate(penyewa_list):
        if p['mitraId'] == mitraId:
            print(f"{1+i}")
            print(f"id sewa : {p['sewaId']}")
            for c in customer_data:
                if c['customerId'] == p['customerId']:                    print(f"Nama Penyewa: {c['nama']}")
            for k in kendaraan_data:
                if k['noKendaraan'] == p['kendaraanYangDisewa']:
                    print(f"Nama Kendaraan: {k['namaKendaraan']}")
            print(f"Tanggal Booking: {p['tanggal_booking']}")
            print(f"Total Harga: {p['total_harga']}")
            print(f"Tanggal Mulai: {p['tanggalMulai']}")
            print(f"Tanggal Selesai: {p['TanggalSelesai']}")
            for b in pembayaran_data:
                if b['sewaId'] == p['sewaId']:
                    print(f"Metode Pembayaran: {b['status']}")
    print("-" * 30)
# def lihat_penyewa_by_status_and_date(status, tanggalMulai):

    
def ubah_data_penyewa():
    
    print("\n=== Ubah Data Penyewa ===")
    lihat_penyewa()

    if not penyewa_list:
        return

    nomor = input("Masukkan nomor penyewa: ").strip()
    if not nomor.isdigit():
        print("Input harus angka!")
        return

    nomor = int(nomor)
    print("Biarkan kosong jika tidak ingin mengubah.")

    customerId = pick_customer()
    kendaraan, harga_per_hari = pick_kendaraan()
    tanggal_booking = datetime.date.today().strftime("%Y-%m-%d")
    tanggalMulai = input_tanggal("Tanggal Mulai Sewa (YYYY-MM-DD): ")
    TanggalSelesai = input_tanggal("Tanggal Selesai Sewa (YYYY-MM-DD): ")
    lama_sewa = (datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d") - datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")).days
    total_harga = int(harga_per_hari) * lama_sewa

    index = nomor - 1
    penyewa_list[index]['kendaraanYangDisewa'] = kendaraan
    penyewa_list[index]['tanggal_booking'] = tanggal_booking
    penyewa_list[index]['tanggalMulai'] = tanggalMulai
    penyewa_list[index]['TanggalSelesai'] = TanggalSelesai
    penyewa_list[index]['lama_sewa'] = lama_sewa
    penyewa_list[index]['total_harga'] = total_harga

    with open(FILE_PENYEWA, "w") as f:
        for p in penyewa_list:
            f.write(f"{p['sewaId']}|{p['customerId']}|{p['kendaraanYangDisewa']}|{p['tanggal_booking']}|{p['total_harga']}|{p['tanggalMulai']}|{p['TanggalSelesai']}|{p['statusSewa']}\n")

    print(">> Data berhasil diubah!\n")

def ubah_peminjaman(mitraId):
    print("\n=== Ubah Data Penyewa ===")
    lihat_penyewa_by_mitraId(mitraId)

    if not penyewa_list:
        return

    sewaId = input("Masukkan id penyewa yang ingin diubah: ")

    kendaraan, harga_per_hari = pick_kendaraan()
    tanggalMulai = input_tanggal("Tanggal Mulai Sewa (YYYY-MM-DD): ")
    TanggalSelesai = input_tanggal("Tanggal Selesai Sewa (YYYY-MM-DD): ")
    lama_sewa = (datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d") - datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")).days
    total_harga = int(harga_per_hari) * lama_sewa
    for p in penyewa_list:
        if p['sewaId'] == sewaId:
            p['kendaraanYangDisewa'] = kendaraan
            p['tanggalMulai'] = tanggalMulai
            p['TanggalSelesai'] = TanggalSelesai
            p['lama_sewa'] = lama_sewa
            p['total_harga'] = total_harga
            break
    with open(FILE_PENYEWA, "w") as f:
        for p in penyewa_list:
            f.write(f"{p['sewaId']}|{p['customerId']}|{p['kendaraanYangDisewa']}|{p['tanggal_booking']}|{p['total_harga']}|{p['tanggalMulai']}|{p['TanggalSelesai']}|{p['statusSewa']}\n")
    print(">> Data berhasil diubah!\n")

def konfirmasi_peminjaman(mitraId):
    print("\n==== konfirmasi peminjaman ====")
    lihat_penyewa_by_mitraId(mitraId)
    print("=" * 30)    
    sewaId = input("pilih Id sewanya: ")
    for p in penyewa_list:
        if p['sewaId'] == sewaId:
            p['statusSewa'] = "sedang digunakan"
            break
    with open(FILE_PENYEWA, "w") as f:
        for p in penyewa_list:
            f.write(f"{p['sewaId']}|{p['customerId']}|{p['kendaraanYangDisewa']}|{p['tanggal_booking']}|{p['total_harga']}|{p['tanggalMulai']}|{p['TanggalSelesai']}|{p['statusSewa']}\n")
    print(">> Data berhasil diubah!\n")

def konfirmasi_pengembalian(mitraId):
    print("\n==== konfirmasi peminjaman ====")
    lihat_penyewa_by_mitraId(mitraId)
    print("=" * 30)    
    sewaId = input("pilih Id sewanya: ")
    for p in penyewa_list:
        if p['sewaId'] == sewaId:
            p['statusSewa'] = "selesai"
            break
    with open(FILE_PENYEWA, "w") as f:
        for p in penyewa_list:
            f.write(f"{p['sewaId']}|{p['customerId']}|{p['kendaraanYangDisewa']}|{p['tanggal_booking']}|{p['total_harga']}|{p['tanggalMulai']}|{p['TanggalSelesai']}|{p['statusSewa']}\n")
    print(">> Data berhasil diubah!\n")

def hapus_penyewa():
    print("\n=== Hapus Data Penyewa ===")
    lihat_penyewa()

    if not penyewa_list:
        return

    nomor = input("Masukkan nomor penyewa yang akan dihapus: ").strip()
    if not nomor.isdigit():
        print("Input harus angka!")
        return

    nomor = int(nomor)
    if nomor < 1 or nomor > len(penyewa_list):
        print("Nomor tidak valid!\n")
        return

    penyewa_list.pop(nomor - 1)
    with open(FILE_PENYEWA, "w") as f:
        for p in penyewa_list:
            f.write(f"{p['sewaId']}|{p['customerId']}|{p['kendaraanYangDisewa']}|{p['tanggal_booking']}|{p['total_harga']}|{p['tanggalMulai']}|{p['TanggalSelesai']}|{p['statusSewa']}\n")
    print(">> Data berhasil dihapus!\n")

def menu_customer(customerId):
    load_data()  # Selalu load data saat masuk menu
    while True:
        print("\n=== MENU RENTAL KENDARAAN ===")
        print("1. Booking Kendaraan")
        print("2. Lihat Riwayat")
        print("3. Bayar Sewa")
        print("0. Kembali")

        pilihan = input("Pilih: ")
        if pilihan == "1":
            tambah_penyewa_customer(customerId)
        elif pilihan == "2":
            lihat_riwayat(customerId)
        elif pilihan == "3":
            bayar_sewa_user(idBayar=None)
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid.")




def menu_penyewa_kendaraan():
    # Menu utama
    while True:
        print("=== MENU PENYEWA KENDARAAN ===")
        print("1. Tambah Data")
        print("2. Lihat Data")
        print("3. Ubah Data")
        print("4. Hapus Data")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ").strip()

        if pilihan == "":
            print("Input tidak boleh kosong!")
            continue

        if pilihan == "1":
            tambah_penyewa()
        elif pilihan == "2":
            lihat_penyewa()
        elif pilihan == "3":
            ubah_data_penyewa()
        elif pilihan == "4":
            hapus_penyewa()
        elif pilihan == "5":
            print("Terima kasih! Program selesai.")
            break
        else:
            print("Pilihan tidak valid, coba lagi!\n")


# def menu_penyewa_kendaraan():
#     load_data()
#     print("=== DATA SEMUA PENYEWA (ADMIN) ===")
#     for p in penyewa_list:
#         print(
#             f"ID: {p['sewaId']} | User: {p['customerId']} | Status: {p['status']}")
# >>>>>>> e92512ebebbf2355e7ecd50a988067e32e5f4093

load_data()

if __name__ == "__main__":
    menu_penyewa_kendaraan()
