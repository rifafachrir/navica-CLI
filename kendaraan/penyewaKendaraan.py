import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import datetime

penyewa_list = []  # Menyimpan semua data penyewa
customer_data = []
kendaraan_data = []


FILE_PENYEWA = "database/sewaKendaraan.txt"
file = os.path.exists(FILE_PENYEWA)

def load_data():
    today = datetime.date.today()
    if file:
        with open(FILE_PENYEWA, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                penyewa_list.append({
                    "sewaId": bagian[0],
                    "customerId": bagian[1],
                    "kendaraanYangDisewa": bagian[2],
                    "tanggal_booking": bagian[3],
                    "total_harga": bagian[4],
                    "tanggalMulai": bagian[5],
                    "TanggalSelesai": bagian[6],
                    "lama_sewa": int(bagian[6]) - int(bagian[5]),
                    "statusSewa": bagian[7]
                })
                if datetime.datetime.strptime(bagian[5], "%Y-%m-%d").date() <= today and bagian[7] == "booking":
                    bagian[7] = "sedang disewa"



        
        with open("database/dataCustomer.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
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
        
        with open("database/dataKendaraan.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) == 5:
                    kendaraan_data.append({
                        "noKendaraan": bagian[0],
                        "mitraId": bagian[1],
                        "namaKendaraan": bagian[2],
                        "hargaSewaPerHari": bagian[3],
                        "status": bagian[4]
                    })
    else:
        print("Tidak ditemukan file untuk menyimpan data")

def pick_customer():
    print("=== Pilih Customer ===")
    for i, customer in enumerate(customer_data):
        print(f"{i + 1}. {customer['nama']} (ID: {customer['customerId']})")
    pilihan = int(input("Masukkan nomor customer: ")) - 1
    if 0 <= pilihan < len(customer_data):
        return customer_data[pilihan]['id']
    else:
        print("Pilihan tidak valid.")
        return None

def pick_kendaraan():
    print("=== Pilih Kendaraan ===")
    for i, kendaraan in enumerate(kendaraan_data):
        print(f"{i + 1}. {kendaraan['namaKendaraan']} (ID: {kendaraan['noKendaraan']}) - Harga per hari: {kendaraan['hargaSewaPerHari']}")
    pilihan = int(input("Masukkan nomor kendaraan: ")) - 1
    if 0 <= pilihan < len(kendaraan_data):
        return kendaraan_data[pilihan]['noKendaraan'], kendaraan_data[pilihan]['hargaSewaPerHari']
    else:
        print("Pilihan tidak valid.")
        return None
    
def cek_ketersediaan_kendaraan(kendaraan, tanggalMulai, TanggalSelesai):
    tanggalMulaiBaru = datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")
    TanggalSelesaiBaru = datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d")
    
    for penyewa in penyewa_list:
        if penyewa['kendaraanYangDisewa'] == kendaraan:
            kendaraanYangAda = penyewa['kendaraanYangDisewa']
            tanggalMulaiYangAda = datetime.datetime.strptime(penyewa['tanggalMulai'], "%Y-%m-%d")
            tanggalSelesaiYangAda = datetime.datetime.strptime(penyewa['TanggalSelesai'], "%Y-%m-%d")
            statusYangAda = penyewa['statusSewa']
    
    if tanggalMulaiBaru <= tanggalSelesaiYangAda and tanggalMulaiYangAda <= TanggalSelesaiBaru:
        if kendaraanYangAda == kendaraan and statusYangAda == "booking":
            return False
    return True
    
# TODO: perlihatkan data penyewa berdasarkan tanggal
def tambah_penyewa():
    print("\n=== Tambah Data Penyewa ===")
    sewaId = str(len(penyewa_list) + 1).zfill(2)
    customerId = pick_customer()
    kendaraan, harga_per_hari = pick_kendaraan()
    tanggal_booking = datetime.date.today().strftime("%Y-%m-%d")
    tanggalMulai = input("Tanggal Mulai Sewa (YYYY-MM-DD): ")
    TanggalSelesai = input("Tanggal Selesai Sewa (YYYY-MM-DD): ")
    if cek_ketersediaan_kendaraan(kendaraan, tanggalMulai, TanggalSelesai):
        print(" Kendaraan tersedia!")
    else:
        print(f"kendaraan: {kendaraan} . Tidak tersedia pada tanggal tersebut")
        return
    lama_sewa = (datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d") - datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")).days
    total_harga = int(harga_per_hari) * lama_sewa


    data = {
        "sewaId": sewaId,
        "customerId": customerId,
        "kendaraanYangDisewa": kendaraan,
        "tanggal_booking": tanggal_booking,
        "total_harga": total_harga,
        "tanggalMulai": tanggalMulai,
        "TanggalSelesai": TanggalSelesai,
        "lama_sewa": lama_sewa,
        "statusSewa": "booking"
    }

    penyewa_list.append(data)
    with open(FILE_PENYEWA, "a") as f:
        f.write(f"{sewaId}|{customerId}|{kendaraan}|{tanggal_booking}|{total_harga}|{tanggalMulai}|{TanggalSelesai}|booking\n")
    print(">> Data berhasil ditambahkan!\n")

def tambah_penyewa_customer(customerId):
    print("\n=== Tambah Data Penyewa ===")
    sewaId = str(len(penyewa_list) + 1).zfill(2)
    # customerId = pick_customer()
    kendaraan, harga_per_hari = pick_kendaraan()
    tanggal_booking = datetime.date.today().strftime("%Y-%m-%d")
    tanggalMulai = input("Tanggal Mulai Sewa (YYYY-MM-DD): ")
    TanggalSelesai = input("Tanggal Selesai Sewa (YYYY-MM-DD): ")
    if cek_ketersediaan_kendaraan(kendaraan, tanggalMulai, TanggalSelesai):
        print(" Kendaraan tersedia!")
    else:
        print(f"kendaraan: {kendaraan} . Tidak tersedia pada tanggal tersebut")
        return
    lama_sewa = (datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d") - datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")).days
    total_harga = int(harga_per_hari) * lama_sewa

    data = {
        "sewaId": sewaId,
        "customerId": customerId,
        "kendaraanYangDisewa": kendaraan,
        "tanggal_booking": tanggal_booking,
        "total_harga": total_harga,
        "tanggalMulai": tanggalMulai,
        "TanggalSelesai": TanggalSelesai,
        "lama_sewa": lama_sewa,
        "statusSewa": "booking"
    }

    penyewa_list.append(data)
    with open(FILE_PENYEWA, "a") as f:
        f.write(f"{sewaId}|{customerId}|{kendaraan}|{tanggal_booking}|{total_harga}|{tanggalMulai}|{TanggalSelesai}|booking\n")
    print(">> Data berhasil ditambahkan!\n")

def lihat_penyewa():
    print("\n=== Daftar Penyewa ===")
    if not penyewa_list:
        print("Belum ada data penyewa.\n")
        return

    for i, p in enumerate(penyewa_list):
        print(f"{1+i}")
        print(f"id sewa : {p['sewaId']}")
        for c in customer_data:
            if c['id'] == p['customerId']:
                print(f"Nama Penyewa: {c['nama']}")
        for k in kendaraan_data:
            if k['id'] == p['kendaraanYangDisewa']:
                print(f"Nama Kendaraan: {k['namaKendaraan']}")
        print(f"Tanggal Booking: {p['tanggal_booking']}")
        print(f"Total Harga: {p['total_harga']}")
        print(f"Tanggal Mulai: {p['tanggalMulai']}")
        print(f"Tanggal Selesai: {p['TanggalSelesai']}")
        print(f"Lama Sewa: {p['lama_sewa']} hari")
        print(f"Status Sewa: {p['statusSewa']}")

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
                if c['id'] == p['customerId']:
                    print(f"Nama Penyewa: {c['nama']}")
            for k in kendaraan_data:
                if k['id'] == p['kendaraanYangDisewa']:
                    print(f"Nama Kendaraan: {k['namaKendaraan']}")
            print(f"Tanggal Booking: {p['tanggal_booking']}")
            print(f"Total Harga: {p['total_harga']}")
            print(f"Tanggal Mulai: {p['tanggalMulai']}")
            print(f"Tanggal Selesai: {p['TanggalSelesai']}")
            print(f"Lama Sewa: {p['lama_sewa']} hari")
            print(f"Status Sewa: {p['statusSewa']}")
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
                if c['id'] == p['customerId']:
                    print(f"Nama Penyewa: {c['nama']}")
            for k in kendaraan_data:
                if k['id'] == p['kendaraanYangDisewa']:
                    print(f"Nama Kendaraan: {k['namaKendaraan']}")
            print(f"Tanggal Booking: {p['tanggal_booking']}")
            print(f"Total Harga: {p['total_harga']}")
            print(f"Tanggal Mulai: {p['tanggalMulai']}")
            print(f"Tanggal Selesai: {p['TanggalSelesai']}")

# def lihat_penyewa_by_status_and_date(status, tanggalMulai):

    
def ubah_data_penyewa():
    
    print("\n=== Ubah Data Penyewa ===")
    lihat_penyewa()

    if not penyewa_list:
        return

    nomor = input("Masukkan id penyewa yang ingin diubah: ")
    if nomor < 1 or nomor > len(penyewa_list):
        print("Nomor tidak valid!\n")
        return

    index = nomor - 1
    print("Biarkan kosong jika tidak ingin mengubah.")

    customerId = pick_customer()
    kendaraan, harga_per_hari = pick_kendaraan()
    tanggal_booking = datetime.date.today().strftime("%Y-%m-%d")
    tanggalMulai = input("Tanggal Mulai Sewa (YYYY-MM-DD): ")
    TanggalSelesai = input("Tanggal Selesai Sewa (YYYY-MM-DD): ")
    lama_sewa = (datetime.datetime.strptime(TanggalSelesai, "%Y-%m-%d") - datetime.datetime.strptime(tanggalMulai, "%Y-%m-%d")).days
    total_harga = int(harga_per_hari) * lama_sewa

    penyewa_list[index]['customerId'] = customerId
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
    tanggalMulai = input("Tanggal Mulai Sewa (YYYY-MM-DD): ")
    TanggalSelesai = input("Tanggal Selesai Sewa (YYYY-MM-DD): ")
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
    print("=")*30
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
    print("=")*30
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

    nomor = int(input("Masukkan nomor penyewa yang akan dihapus: "))
    if nomor < 1 or nomor > len(penyewa_list):
        print("Nomor tidak valid!\n")
        return

    penyewa_list.pop(nomor - 1)
    with open(FILE_PENYEWA, "w") as f:
        for p in penyewa_list:
            f.write(f"{p['sewaId']}|{p['customerId']}|{p['kendaraanYangDisewa']}|{p['tanggal_booking']}|{p['total_harga']}|{p['tanggalMulai']}|{p['TanggalSelesai']}|{p['statusSewa']}\n")
    print(">> Data berhasil dihapus!\n")


def menu_penyewa_kendaraan():
    # Menu utama
    while True:
        print("=== MENU PENYEWA KENDARAAN ===")
        print("1. Tambah Data")
        print("2. Lihat Data")
        print("3. Ubah Data")
        print("4. Hapus Data")
        print("5. Keluar")

        pilihan = input("Pilih menu (1-5): ")

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

def menu_customer(customerId):
    print(customer_data)
    # Menu utama
    while True:
        print("=== MENU MENYEWA KENDARAAN ===")
        print("1. Tambah Data")
        print("2. Lihat Riwayat")
        print("0. Keluar")

        pilihan = input("Pilih menu (0-2): ")

        if pilihan == "1":
            tambah_penyewa_customer(customerId)
        elif pilihan == "2":
            lihat_penyewa_by_customer_id(customerId)
        elif pilihan == "0":
            break
        else:
            print("Pilihan tidak valid, coba lagi!\n")

load_data()

if __name__ == "__main__":
    menu_penyewa_kendaraan()