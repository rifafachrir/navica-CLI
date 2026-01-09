import os
import datetime



FILE_KAMAR = "database/DataKamarPenginapan.txt"
FILE_CUSTOMER = "database/dataCustomer.txt"
FILE_PEMBAYARAN = "database/dataPembayaran.txt"
FILE_SEWA = "database/SewaPenginapan.txt"
FILE_PENGINAPAN ="database/dataPenginapan.txt"


# Konfigurasi file database


# List Global untuk menampung data
kamar_list = []
penginapan_list = []
pembayaran_data = []
data_sewa = []
customer = []

# conflict 1
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
                        "id": (bagian[0]),
                        "penginapan_id": (bagian[1]),
                        "nama": bagian[2],
                        "tipe": bagian[3],
                        "harga": int(bagian[4]),
                        "kapasitas": int(bagian[5]),
                        "status": bagian[6]
                    }
                    kamar_list.append(kamar)

    # 2. Load Data Penginapan

    with open(FILE_PENGINAPAN, "r") as f:
        lines = f.readlines()
        for line in lines:
            bagian = line.strip().split("|")
            penginapan_list.append({
                "penginapanId": bagian[0],
                "mitraId": bagian[1],
                "namaPenginapan": bagian[2],
                "alamat": bagian[3],
                "noTelp": bagian[4]
            })
    
    # 3. Load Data Sewa
    with open(FILE_SEWA, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            bagian = line.strip().split("|")
            if len(bagian) == 10:
                data_sewa.append({
                    "id": bagian[0],
                    "penyewa": bagian[1],
                    "jenis": bagian[2],
                    "penginapanId": bagian[3],
                    "kode_kamar": bagian[4],
                    "tanggal_mulai": bagian[5],
                    "lama_menginap": bagian[6],
                    "harga_permalam": bagian[7],
                    "total": bagian[8],
                    "status": bagian[9],
                })



    with open(FILE_CUSTOMER, "r")as f:
        lines = f.readlines()
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) == 5:
                customer.append({
                    "id": bagian[0],
                    "nama": bagian[1],
                    "alamat": bagian[2],
                    "noTelp": bagian[3],
                    "email": bagian[4],
                })


    with open(FILE_PEMBAYARAN, "r") as f:
        lines = f.readlines()
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) == 6:
                pembayaran_data.append({
                    "id": bagian[0],
                    "sewaId": bagian[1],
                    "metode": bagian[2],
                    "total": bagian[3],
                    "tanggal": bagian[4],
                    "status": bagian[5]
                })

    return data_sewa



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


def cek_ketersediaan_kamar(noKamar, tanggalMulai, tanggalSelesai):
    tanggalMulaiBaru = datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")
    tanggalSelesaiBaru = datetime.datetime.strptime(tanggalSelesai, "%Y-%m-%d")

    for kamar in kamar_list:
        if kamar["id"] == noKamar:
            kamarYangAda = kamar["id"]
            tanggalMulaiYangAda = datetime.datetime.strptime(kamar["tanggalMulai"], "%Y-%m-%d")
            tanggalSelesaiYangAda = datetime.datetime.strptime(kamar["tanggalSelesai"], "%Y-%m-%d")
    
    for s in data_sewa:
        if s["kode_kamar"] == noKamar:
            statusYangAda = s["status"]
            

    if tanggalMulaiBaru <= tanggalSelesaiYangAda and tanggalMulaiYangAda <= tanggalSelesaiBaru:
        if kamarYangAda == noKamar and statusYangAda == "booking":
            return False
    return True



# def save_data(data):
#     with open(FILE_SEWA, "w", encoding="utf-8") as file:
#         for d in data:
#             file.write(
#                 f"{d['id']}|{d['penyewa']}|{d['jenis']}|{d['penginapanId']}|"
#                 f"{d['nomor_kamar']}|{d['lama_menginap']}|{d['harga_permalam']}|"
#                 f"{d['total']}|{d['status']}\n"
#             )
def save_data_sewa():
    
    with open(FILE_SEWA, "w") as f:
        for d in data_sewa:
            line = f"{d['id']}|{d['penyewa']}|{d['jenis']}|{d['nama_properti']}|{d['kode_kamar']}|{d['tanggal_mulai']}|{d['lama_menginap']}|{d['harga_permalam']}|{d['total']}|{d['status']}\n"
            f.write(line)


def generate_id_sewa():
    nomor = len(data_sewa) + 1
    return "NAV" + str(nomor).zfill(3)

# ===== FUNGSI PEMBAYARAN =====


# def simpan_ke_pembayaran_db(sewaId, total, metode):
#     # Cek jumlah data untuk membuat ID baru
#     jumlah_data = 0
#     if os.path.exists(FILE_PEMBAYARAN):
#         with open(FILE_PEMBAYARAN, "r") as f:
#             lines = f.readlines()
#             jumlah_data = len(lines)

#     # Generate ID Pembayaran
#     id_bayar = "PAY" + str(jumlah_data + 1).zfill(3)
#     tgl_sekarang = str(datetime.date.today())
#     status = "Lunas"

#     # Format data sesuai ERD
#     data_string = f"{id_bayar}|{sewaId}|{metode}|{total}|{tgl_sekarang}|{status}\n"

#     # Simpan ke file
#     with open(FILE_PEMBAYARAN, "a") as f:
#         f.write(data_string)


# def bayar_pesanan_user(customerId):
#     print("\n=== PEMBAYARAN PENGINAPAN ===")

#     # Cari tagihan user yang belum dibayar
#     tagihan_saya = []

#     for item in data_sewa:
#         if item['penyewa'] == customerId:
#             if item['status'] == "Booking":
#                 tagihan_saya.append(item)

#     if len(tagihan_saya) == 0:
#         print("Tidak ada tagihan yang harus dibayar.")
#         return

#     # Tampilkan daftar tagihan
#     print("Daftar Tagihan Anda:")
#     nomor = 1
#     for t in tagihan_saya:
#         print(f"{nomor}. Hotel: {t['nama_properti']} | Total: Rp {t['total']}")
#         nomor = nomor + 1

#     # Proses pembayaran
#     pilihan_str = input("Pilih nomor tagihan: ")
#     if not pilihan_str.isdigit():
#         print("Input harus angka.")
#         return

#     pilihan = int(pilihan_str) - 1

#     if pilihan >= 0 and pilihan < len(tagihan_saya):
#         data_dipilih = tagihan_saya[pilihan]

#         print(f"\nTotal Tagihan: Rp {data_dipilih['total']}")
#         print("Metode Pembayaran:")
#         print("1. Transfer Bank")
#         print("2. E-Wallet")

#         metode_input = input("Pilih (1/2): ")
#         metode = "Cash"
#         if metode_input == "1":
#             metode = "Transfer Bank"
#         elif metode_input == "2":
#             metode = "E-Wallet"

#         yakin = input("Bayar sekarang? (y/n): ")
#         if yakin == "y" or yakin == "Y":
#             # Update status jadi Lunas
#             data_dipilih['status'] = "Lunas"

#             # Simpan update ke file sewa
#             save_data_sewa()

#             # Catat riwayat pembayaran
#             simpan_ke_pembayaran_db(
#                 data_dipilih['id'], data_dipilih['total'], metode)
#             print("Pembayaran Berhasil! Status pesanan sudah Lunas.")
#         else:
#             print("Batal bayar.")
#     else:
#         print("Nomor pilihan salah.")

def create_pembayaran(sewaId, total):
    jumlah = 0
    with open(FILE_PEMBAYARAN, "r") as f:
        jumlah = len(f.readlines())
    idBayar = "PAY-P" + str(jumlah + 1).zfill(3)
    status = "belum bayar"

    with open(FILE_PEMBAYARAN, "a") as f:
        f.write(f"{idBayar}|{sewaId}|-|{total}|-|{status}\n")
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



def bayar_pesanan_user(idBayar):
    print("\n=== PEMBAYARAN PENGINAPAN ===")
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
                    break


            else: 
                print("Kode pembayaran ini sudah Lunas.")



def create_data(data):
    print("\n=== PEMESANAN PENGINAPAN ===")
    id_sewa = generate_id_sewa(data)

    # penyewa = input("Nama Penyewa : ")
    for i, cust in enumerate(customer):
        print(f"{i+1}. {cust['nama']}")
    select = int(input("Pilih Penyewa : ")) - 1
    penyewa = customer[select]["nama"]
    
    

    tanggal_menginap = input("Tanggal Menginap (YYYY-MM-DD) : ")

    # load kamar dari database
    # kamar_list = load_data()
    # load kamar dari database
    # kamar_list = load_data()
    if not kamar_list:
        print("Belum ada data kamar. Silakan hubungi admin.\n")
        return

    # tampilkan kamar yang tersedia saja
    print("\n=== DAFTAR KAMAR TERSEDIA ===")
    # tersedia = [k for k in kamar_list if k["status"] == "tersedia"]
    tersedia = []
    for k in kamar_list:
        if k["status"] == "tersedia" and k["tanggal_mulai"] != tanggal_menginap:
            tersedia.append(k)
    if len(tersedia) == 0:
        print(f"Tidak ada kamar yang tersedia untuk tanggal {tanggal_menginap}.\n")
        return

    for i, k in enumerate(tersedia):
        print(f"                {i+1}")
        print(f"kode Kamar  : {k['id']}")
        print(f"Nama        : {k['nama']}")
        print(f"Tipe        : {k['tipe']}")
        print(f"Harga       : {k['harga']}")
        print(f"Kapasitas   : {k['kapasitas']}")
        print(f"Status      : {k['status']}")

        print("------------------------")

    # pilih kamar
    try:
        pilih_id = int(input("Masukkan urutan kamar yang ingin dipesan: ")) - 1

    except ValueError:
        print("ID kamar harus angka.\n")
        return

    kamar_dipilih = None
    for k in kamar_list:
        if k["id"] == pilih_id:
            kamar_dipilih = k
            break

    if kamar_dipilih is None:
        print("Kamar dengan urutan tersebut tidak ditemukan.\n")
        return
    
    lama_menginap = input("Lama Menginap (hari) : ")
    while not lama_menginap.isdigit():
        lama_menginap = input("Input harus angka : ")

    lama_menginap = int(lama_menginap)
    startDate = datetime.datetime.strptime(tanggal_menginap, "%Y-%m-%d")
    endDate = startDate + datetime.timedelta(days=lama_menginap)

    if cek_ketersediaan_kamar(kamar_dipilih["id"], startDate, endDate) :
        print("Kamar Tersedia!!\n")
    else:
        print("Kamar Tidak Tersedia!!\n")
        return

    # ambil data dari kamar
    penginapanId = kamar_dipilih["penginapanId"]
    jenis = kamar_dipilih["tipe"]          # bisa kamu mapping ke 'Hotel'/'Vila' kalau mau
    kode_kamar = str(kamar_dipilih["id"])  # sementara pakai ID kamar sebagai nomor kamar


    
    harga_permalam = str(kamar_dipilih["harga"])
    total = int(lama_menginap) * int(harga_permalam)

    bayarId = create_pembayaran(id_sewa, total)

    data.append({
        "id": id_sewa,
        "penyewa": penyewa,
        "jenis": jenis,
        "penginapanId": penginapanId,
        "kode_kamar": kode_kamar,
        "tanggal_mulai": tanggal_menginap,
        "lama_menginap": lama_menginap,
        "harga_permalam": harga_permalam,
        "total": str(total),
        "status": "Booking",
    })

    save_data_sewa()

    # update status kamar jadi tidak
    update_status_kamar(kamar_dipilih["id"], "booking")


    print("\nPemesanan berhasil dibuat!\n")
    print("Silahkan lakukan pembayaran untuk melakukan pemesanan penginapan.")
    bayar_pesanan_user(bayarId)
    print("kode pembayaran anda adalah: ", bayarId)




def bookingCutomer(customerId):
    print("\n=== PEMESANAN PENGINAPAN ===")
    id_sewa = generate_id_sewa(data_sewa)

    for c in customer:
        if c["id"] == customerId:
            penyewa = c["id"]        

    tanggal_menginap = input("Tanggal Menginap (YYYY-MM-DD) : ")

    for i, nginap in enumerate(penginapan_list):
        print(f"{i + 1}. (ID: {nginap['penginapanId']}) {nginap['namaPenginapan']} ")
    pilihan = int(input("Masukkan nomor penginapan: ")) - 1
    if 0 <= pilihan < len(penginapan_list):
        penginapanId = penginapan_list[pilihan]['penginapanId']
    else:
        print("Pilihan tidak valid.")
        penginapan_list = "tidak ada"

    list_kamar = load_kamar_by_penginapan(penginapanId)

    if not list_kamar:
        print("Belum ada data kamar. Silakan hubungi admin.\n")
        return

    # tampilkan kamar yang tersedia saja
    print("\n=== DAFTAR KAMAR TERSEDIA ===")
    # tersedia = [k for k in list_kamar if k["status"] == "tersedia"]
    tersedia = []
    for k in list_kamar:
        if k["status"] == "tersedia" and k["tanggal_mulai"] != tanggal_menginap:
            tersedia.append(k)
    if len(tersedia) == 0:
        print(f"Tidak ada kamar yang tersedia untuk tanggal {tanggal_menginap}.\n")
        return

    for i, k in enumerate(tersedia):
        print(f"                {i+1}")
        print(f"kode Kamar  : {k['id']}")
        print(f"Nama        : {k['nama']}")
        print(f"Tipe        : {k['tipe']}")
        print(f"Harga       : {k['harga']}")
        print(f"Kapasitas   : {k['kapasitas']}")
        print(f"Status      : {k['status']}")

        print("------------------------")

    # pilih kamar
    try:
        pilih_id = int(input("Masukkan urutan kamar yang ingin dipesan: ")) - 1

    except ValueError:
        print("ID kamar harus angka.\n")
        return

    kamar_dipilih = None
    for k in list_kamar:
        if k["id"] == pilih_id:
            kamar_dipilih = k
            break

    if kamar_dipilih is None:
        print("Kamar dengan urutan tersebut tidak ditemukan.\n")
        return

    lama_menginap = input("Lama Menginap (hari) : ")
    while not lama_menginap.isdigit():
        lama_menginap = input("Input harus angka : ")

    lama_menginap = int(lama_menginap)
    startDate = datetime.datetime.strptime(tanggal_menginap, "%Y-%m-%d")
    endDate = startDate + datetime.timedelta(days=lama_menginap)

    if cek_ketersediaan_kamar(kamar_dipilih["id"], startDate, endDate) :
        print("Kamar Tersedia!!\n")
    else:
        print("Kamar Tidak Tersedia!!\n")
        return

    # ambil data dari kamar
    penginapanId = kamar_dipilih["penginapanId"]
    jenis = kamar_dipilih["tipe"]           # bisa kamu mapping ke 'Hotel'/'Vila' kalau mau
    kode_kamar = str(kamar_dipilih["id"])  # sementara pakai ID kamar sebagai nomor kamar


    harga_permalam = str(kamar_dipilih["harga"])
    total = int(lama_menginap) * int(harga_permalam)

    bayarId = create_pembayaran(id_sewa, total)

    data_sewa.append({
        "id": id_sewa,
        "penyewa": penyewa,
        "jenis": jenis,
        "penginapanId": penginapanId,
        "kode_kamar": kode_kamar,
        "tanggal_mulai": tanggal_menginap,
        "lama_menginap": lama_menginap,
        "harga_permalam": harga_permalam,
        "total": str(total),
        "status": "Booking",
    })

    save_data_sewa()

    update_status_kamar(kamar_dipilih["id"], "booking")


    print("\nPemesanan berhasil dibuat!\n")
    print("Silahkan lakukan pembayaran untuk melakukan pemesanan penginapan.")
    bayar_pesanan_user(bayarId)
    print("kode pembayaran anda adalah: ", bayarId)

def booking_with_mitraId(mitraId):
    print("\n=== PEMESANAN PENGINAPAN ===")
    id_sewa = generate_id_sewa(data_sewa)

    # penyewa = input("Nama Penyewa : ")
    for i, cust in enumerate(customer):
        print(f"{i+1}. {cust['nama']}")
    select = int(input("Pilih Penyewa : ")) - 1
    penyewa = customer[select]["nama"]
    
    for p in penginapan_list:
        if p['mitraId'] == mitraId:
            penginapanId = p['penginapanId']

    tanggal_menginap = input("Tanggal Menginap (YYYY-MM-DD) : ")

    # load kamar dari database
    kamar_list = load_kamar_by_penginapan(penginapanId)

    if not kamar_list:
        print("Belum ada data kamar. Silakan hubungi admin.\n")
        return

    # tampilkan kamar yang tersedia saja
    print("\n=== DAFTAR KAMAR TERSEDIA ===")
    # tersedia = [k for k in kamar_list if k["status"] == "tersedia"]
    tersedia = []
    for k in kamar_list:
        if k["status"] == "tersedia" and k["tanggal_mulai"] != tanggal_menginap:
            tersedia.append(k)
    if len(tersedia) == 0:
        print(f"Tidak ada kamar yang tersedia untuk tanggal {tanggal_menginap}.\n")
        return

    for i, k in enumerate(tersedia):
        print(f"                {i+1}")
        print(f"kode Kamar  : {k['id']}")
        print(f"Nama        : {k['nama']}")
        print(f"Tipe        : {k['tipe']}")
        print(f"Harga       : {k['harga']}")
        print(f"Kapasitas   : {k['kapasitas']}")
        print(f"Status      : {k['status']}")

        print("------------------------")

    # pilih kamar
    try:
        pilih_id = int(input("Masukkan urutan kamar yang ingin dipesan: ")) - 1

    except ValueError:
        print("ID kamar harus angka.\n")
        return

    kamar_dipilih = None
    for k in kamar_list:
        if k["id"] == pilih_id:
            kamar_dipilih = k
            break

    if kamar_dipilih is None:
        print("Kamar dengan urutan tersebut tidak ditemukan.\n")
        return

    lama_menginap = input("Lama Menginap (hari) : ")
    while not lama_menginap.isdigit():
        lama_menginap = input("Input harus angka : ")

    lama_menginap = int(lama_menginap)
    startDate = datetime.datetime.strptime(tanggal_menginap, "%Y-%m-%d")
    endDate = startDate + datetime.timedelta(days=lama_menginap)

    if cek_ketersediaan_kamar(kamar_dipilih["id"], startDate, endDate) :
        print("Kamar Tersedia!!\n")
    else:
        print("Kamar Tidak Tersedia!!\n")
        return

    # ambil data dari kamar
    jenis = kamar_dipilih["tipe"]           # bisa kamu mapping ke 'Hotel'/'Vila' kalau mau
    kode_kamar = str(kamar_dipilih["id"])  # sementara pakai ID kamar sebagai nomor kamar

    harga_permalam = str(kamar_dipilih["harga"])
    total = int(lama_menginap) * int(harga_permalam)

    bayarId = create_pembayaran(id_sewa, total)

    data_sewa.append({
        "id": id_sewa,
        "penyewa": penyewa,
        "jenis": jenis,
        "penginapanId": penginapanId,
        "kode_kamar": kode_kamar,
        "tanggal_mulai": tanggal_menginap,
        "lama_menginap": lama_menginap,
        "harga_permalam": harga_permalam,
        "total": str(total),
        "status": "Booking",
    })

    save_data_sewa()

    # update status kamar jadi tidak
    update_status_kamar(kamar_dipilih["id"], "booking")


    print("\nPemesanan berhasil dibuat!\n")
    print("Silahkan lakukan pembayaran untuk melakukan pemesanan penginapan.")
    bayar_pesanan_user(bayarId)
    print("kode pembayaran anda adalah: ", bayarId)



def read_data(data):
    print("\n=== DAFTAR PEMESANAN ===")
    if not data:
        print("Belum ada data.\n")
        return

    for d in data:
        customerId = d['penyewa']
        penginapanId = d['penginapanId']
        print(f"ID Sewa        : {d['id']}")
        for c in customer:
            if c['id'] == customerId:
                print(f"Nama Penyewa   : {c['nama']}")
        print(f"Jenis          : {d['jenis']}")
        for p in penginapan_list:
            if p['id'] == penginapanId:
                print(f"Nama Properti  : {p['namaPenginapan']}")
        print(f"kodeKamar      : {d['kode_kamar']}")
        print(f"Tanggal Mulai  : {d['tanggal_mulai']}")
        # print(f"Nomor Kamar    : {d['nomor_kamar']}")
        print(f"Lama Menginap  : {d['lama_menginap']} hari")
        print(f"Harga/Malam    : Rp {d['harga_permalam']}")
        print(f"Total Harga    : Rp {d['total']}")
        print(f"Status         : {d['status']}")
        for b in pembayaran_data:
            if b['sewaId'] == d["id"]:
                print("kode pembayaran : ", b["idBayar"])
                print("Status Pembayaran : ", b["status"])
        print("-" * 30)
       

       
def read_data_by_mitraId(mitraId):
    print("\n=== TAMBAH KAMAR ===")

    for k in penginapan_list:
        if k["mitraId"] == mitraId:
            penginapanId = k["penginapanId"]
    
    for d in data_sewa:
        if d['penginapanId'] == penginapanId:
            print(f"ID Sewa        : {d['id']}")
            for c in customer:
                print(f"Nama Penyewa   : {c['nama']}")
            print(f"Jenis          : {d['jenis']}")
            for p in penginapan_list:
                if p['id'] == penginapanId:
                    print(f"Nama Properti  : {p['namaPenginapan']}")
            print(f"kodeKamar      : {d['kode_kamar']}")
            print(f"Tanggal Mulai  : {d['tanggal_mulai']}")
            # print(f"Nomor Kamar    : {d['nomor_kamar']}")
            print(f"Lama Menginap  : {d['lama_menginap']} hari")
            print(f"Harga/Malam    : Rp {d['harga_permalam']}")
            print(f"Total Harga    : Rp {d['total']}")
            print(f"Status         : {d['status']}")
            for b in pembayaran_data:
                if b['sewaId'] == d["id"]:
                    print("Status Pembayaran : ", b["status"])
        print("-" * 30)

def read_data_for_customer(customerId):
    print("\n === DAFTAR PEMESANAN PENGINAPAN ANDA ===")

    priority = {"booking", "check-in", "check-out"}



    data_sewa.sort(key=lambda x: x["status"] in priority)

    for d in data_sewa:
        if d['penyewa'] == customerId:
            customerId = d['penyewa']
            penginapanId = d['penginapanId']
            print(f"ID Sewa        : {d['id']}")
            for c in customer:
                if c['id'] == customerId:
                    print(f"Nama Penyewa   : {c['nama']}")
            print(f"Jenis          : {d['jenis']}")
            for p in penginapan_list:
                if p['id'] == penginapanId:
                    print(f"Nama Properti  : {p['namaPenginapan']}")
            print(f"kodeKamar      : {d['kode_kamar']}")
            print(f"Tanggal Mulai  : {d['tanggal_mulai']}")
            # print(f"Nomor Kamar    : {d['nomor_kamar']}")
            print(f"Lama Menginap  : {d['lama_menginap']} hari")
            print(f"Harga/Malam    : Rp {d['harga_permalam']}")
            print(f"Total Harga    : Rp {d['total']}")
            print(f"Status         : {d['status']}")
            for b in pembayaran_data:
                if b['sewaId'] == d["id"]:
                    print("Status Pembayaran : ", b["status"])
            print("-" * 30)
def read_data_by_id(idSewa):
    for d in data_sewa:
        if d['id'] == idSewa:
            customerId = d['penyewa']
            penginapanId = d['penginapanId']
            print(f"ID Sewa        : {d['id']}")
            for c in customer:
                if c['id'] == customerId:
                    print(f"Nama Penyewa   : {c['nama']}")
            print(f"Jenis          : {d['jenis']}")
            for p in penginapan_list:
                if p['id'] == penginapanId:
                    print(f"Nama Properti  : {p['namaPenginapan']}")
            print(f"kodeKamar      : {d['kode_kamar']}")
            print(f"Tanggal Mulai  : {d['tanggal_mulai']}")
            # print(f"Nomor Kamar    : {d['nomor_kamar']}")
            print(f"Lama Menginap  : {d['lama_menginap']} hari")
            print(f"Harga/Malam    : Rp {d['harga_permalam']}")
            print(f"Total Harga    : Rp {d['total']}")
            print(f"Status         : {d['status']}")
            for b in pembayaran_data:
                if b['sewaId'] == d["id"]:
                    print("Status Pembayaran : ", b["status"])

def update_status():
    print("\n=== UPDATE STATUS ===")
    # for i, s in enumerate(data_sewa):

    while True:
        idSewa = input("Masukkan no id customer: ")
        for d in data_sewa:
            read_data_by_id(idSewa)
        question = input("apakah data customer sudah benar? (y/n): ").lower()
        if question == "y":
            break
        elif question == "n":
            print("silahkan masukkan kembali no id customer")
        else:
            print("opsi tidak valid silahkan ulangi dari masukkan id customer")
        


    for d in data_sewa:
        if d["id"] == idSewa:
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

            save_data_sewa()

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

def check_in(mitraId):
    print("\n=== CHECK-IN ===")

    for p in penginapan_list:
        if p['mitraId'] == mitraId:
            penginapanId = p['penginapanId']
    
    idSewa = input("Masukkan ID sewa: ")
    
    for s in data_sewa:
        if s['id'] == idSewa and s['penginapanId'] == penginapanId:
            s['status'] = "Check-in"
    
    save_data_sewa()

def check_out(mitraId):
    print("\n=== CHECK-IN ===")

    for p in penginapan_list:
        if p['mitraId'] == mitraId:
            penginapanId = p['penginapanId']
    
    idSewa = input("Masukkan ID sewa: ")
    
    for s in data_sewa:
        if s['id'] == idSewa and s['penginapanId'] == penginapanId:
            s['status'] = "Check-out"
    
    save_data_sewa()



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
            save_data_sewa()
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
        print(f"Nama Properti  : {d['penginapanId']}")
        print(f"Nomor Kamar    : {d['nomor_kamar']}")
        print(f"Lama Menginap  : {d['lama_menginap']} hari")
        print(f"Harga/Malam    : Rp {d['harga_permalam']}")
        print(f"Total Harga    : Rp {d['total']}")
        print(f"Status         : {d['status']}")
        print("-" * 30)

    if not found:
        print("Tidak ada data yang cocok.\n")


# def sort_data(data):
#     print("\n=== URUTKAN DATA ===")
#     print("1. Nama Penyewa (A-Z)")
#     print("2. Total Harga (Termurah)")
#     pilihan = input("Pilih metode: ")
#     while pilihan not in ["1", "2"]:
#         pilihan = input("Pilih 1 atau 2: ")

#     if pilihan == "1":
#         data.sort(key=lambda x: x["penyewa"].lower())
                

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


def pindah_ruangan():
    print("\n=== PINDAH RUANGAN (GANTI KAMAR) ===")

    id_sewa = input("Masukkan ID Sewa: ").strip()

    sewa = None
    for s in data_sewa:
        if s["id"] == id_sewa:
            sewa = s
            break

    if sewa is None:
        print("ID sewa tidak ditemukan.")
        return
    
    # validasi status
    if sewa["status"] not in ["Booking", "Check-in"]:
        print("Pindah ruangan hanya bisa saat Booking atau Check-in.")
        return

    penginapanId = sewa["penginapanId"]
    kamar_lama = int(sewa["kode_kamar"])

    print("\nKamar Saat Ini:", kamar_lama)

    # cari kamar tersedia di penginapan yang sama
    kamar_tersedia = [] 
    for k in kamar_list: 
        if ( 
            k["penginapan_id"] == penginapanId and 
            k["status"] == "tersedia" 
        ): 
            kamar_tersedia.append(k)
            
    if not kamar_tersedia:
        print("Tidak ada kamar lain yang tersedia.")
        return
    
    # kamar tersedia
    print("\n=== DAFTAR KAMAR TERSEDIA ===")
    for i, k in enumerate(kamar_tersedia):
        print(f"{i+1}. ID: {k['id']} | {k['tipe']} | Rp {k['harga']}")

    pilih = input("Pilih nomor kamar baru: ").strip()
    if not pilih.isdigit():
        print("Input harus angka.")
        return

    pilih = int(pilih) - 1
    if pilih < 0 or pilih >= len(kamar_tersedia):
        print("Pilihan tidak valid.")
        return

    kamar_baru = kamar_tersedia[pilih]

    # update kamar lama → tersedia
    update_status_kamar(kamar_lama, "tersedia")

    # update kamar baru → booking / check-in
    update_status_kamar(kamar_baru["id"], "tidak")

    # update data sewa
    sewa["kode_kamar"] = str(kamar_baru["id"])
    sewa["jenis"] = kamar_baru["tipe"]
    sewa["harga_permalam"] = str(kamar_baru["harga"])
    sewa["total"] = str(int(sewa["lama_menginap"]) * int(kamar_baru["harga"]))

    save_data_sewa()

    print("\nPindah ruangan berhasil!")
    print("Kamar baru:", kamar_baru["id"])


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
            read_data_for_customer(customerId)
        elif pilihan == "3":
            bayar_pesanan_user(idBayar=None)
        elif pilihan == "0":
            break
        else:
            print("Pilihan salah.")



def main():
# Materi: Perulangan While
    
    data = data_sewa
    # data = load_data()
    while True:
        print("\n====== NAVICA — PEMESANAN PENGINAPAN ======")
        print("1. Tambah Pemesanan")
        print("2. Lihat Pemesanan")
        print("3. Update Status")
        print("4. Hapus Pemesanan")
        print("5. Cari Pemesanan")
        # print("6. Urutkan Pemesanan")
        print("7. Pindah Ruangan")
        print("8. Keluar")
        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            create_data(data)
        elif pilihan == "2":
            read_data(data)
        elif pilihan == "3":
            update_status(data)
        elif pilihan == "4":
            delete_data(data)
        elif pilihan == "5":
            search_data(data)
            data = data_sewa
        # elif pilihan == "6":
        #     sort_data(data)
        elif pilihan == "7":
                pindah_ruangan(data)
        elif pilihan == "8":
            print("Terima kasih telah menggunakan Navica.")
            break
        else:
            print("Pilihan tidak valid.\n")
    # Menampilkan semua data sewa (Admin)
    for d in data_sewa:
        print(d)

load_data()
if __name__ == "__main__":
    main()
