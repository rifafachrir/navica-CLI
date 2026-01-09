import os
import re
from datetime import datetime

FILE_CUSTOMER = 'database/dataCustomer.txt'
FILE_DATA_TIKET = 'database/dataTiket.txt'
FILE_TIKET = "database/tiket.txt"
FILE_PEMBAYARAN = "database/dataPembayaran.txt"


customers = []
file_datas_tiket = []
data_pembayaran = []
tiket = []

def load_data():
    with open(FILE_CUSTOMER, 'r') as f:
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) == 5:
                customers.append({
                    "idCustomer": bagian[0],
                    "idUser": bagian[1],
                    "nama": bagian[2],
                    "alamat": bagian[3],
                    "noTelepon": bagian[4]
                })
            else:
                print("Format data customer tidak valid:", line.strip())
    
    with open(FILE_DATA_TIKET):
        with open(FILE_DATA_TIKET, 'r') as f:
            for line in f:
                bagian = line.strip().split("|")
                if len(bagian) == 4:
                    file_datas_tiket.append({
                        "pembelianId": bagian[0],
                        "idCustomer": bagian[1],
                        "tiketId": bagian[2],
                        'tanggal': bagian[3],
                        "status": bagian[4]
                    })
                else:
                    print("Format data tiket tidak valid:", line.strip())

    with open(FILE_TIKET, 'r') as f:
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) == 7:
                tiket.append({
                    "idTiket": bagian[0],
                    "mitraId": bagian[1],
                    'namaTiket': bagian[2],
                    "harga": bagian[3],
                    "jenis": bagian[4],
                    "asal": bagian[5],
                    "tujuan": bagian[6]
                })
            else:
                print("Format data tiket tidak valid:", line.strip())
    with open(FILE_PEMBAYARAN, "r") as f:
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) == 6:
                data_pembayaran.append({
                    "idBayar": bagian[0],
                    "sewaId": bagian[1],
                    "metode": bagian[2],
                    "total": bagian[3],
                    "tanggal": bagian[4],
                    "status": bagian[5]
                })





def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_tanggal():
    while True:
        tanggal = input("Tanggal (YYYY-MM-DD): ")
        if re.fullmatch(r"\d{4}-\d{2}-\d{2}", tanggal):
            try:
                datetime.strptime(tanggal, "%Y-%m-%d")
                return tanggal
            except ValueError:
                print("❌ Tanggal tidak valid! (contoh: 2024-12-31)")
        else:
            print("❌ Format tanggal salah! Gunakan format YYYY-MM-DD (contoh: 2024-12-31)")

def input_harga():
    while True:
        harga = input("Harga (angka saja): Rp ")
        if harga.isdigit() and int(harga) > 0:
            return harga
        print("❌ Harga hanya boleh ANGKA dan harus lebih dari 0!")



def input_id(mitraId):
    if not tiket:
        print("❌ Data tiket masih kosong!")
        return
    else:
        for i, t in enumerate(tiket):
            if t['mitraId'] == mitraId:
                print(f"{i+1} - {t['idTiket']} - {t['jenis']} - {t['asal']} - {t['tujuan']} - {t['harga']}")

        while True:
            id_tiket = input("ID Tiket: ").strip()
            if any(t['idTiket'] == id_tiket for t in tiket):
                return id_tiket
            print("❌ ID Tiket tidak valid!")


def generateId():
    jumlah = len(file_datas_tiket) + 1
    return  "NAV-T"+str(jumlah).zfill(3)
    
def input_customer():
    for i, c in enumerate(customers):
        print(f"{i+1} - {c['idCustomer']} - {c['nama']} - {c['alamat']} - {c['noTelepon']}")

    selected = int(input("Pilih customer: ")) - 1
    return customers[selected]

def input_tiket():
    if not tiket:
        print("❌ Data tiket masih kosong!")
        return False
    else:
        for i, t in enumerate(tiket):
            print(f"{i+1} - {t['idTiket']} - {t['jenis']} - {t['asal']} - {t['tujuan']} - {t['harga']}")

        selected = int(input("Pilih tiket: ")) - 1
        return tiket[selected]
    

def input_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print(f"❌ {prompt.split(':')[0]} tidak boleh kosong!")

def is_header(line):
    return line.strip() == "ID|Jenis|Nama|Asal|Tujuan|Tanggal|Harga|Status"

def create_pembayaran(pembelianId, total):
    jumlah = 0
    with open(FILE_PEMBAYARAN, 'r') as f:
        jumlah = len(f.readlines())
    idBayar = "PAY-T" + str(jumlah + 1).zfill(3)
    status = "belum bayar"

    with open(FILE_PEMBAYARAN, "a") as f:
        f.write(f"{idBayar}|{pembelianId}|-|{total}|-|{status}\n")
    return idBayar

def simpan_ke_pembayaran_db(id_bayar, metode, status):
    tgl_sekarang = str(datetime.date.today().strftime("%Y-%m-%d"))
    
    for p in data_pembayaran:
        if p["idBayar"] == id_bayar:
            p["metode"] = metode
            p["tanggal"] = tgl_sekarang
            p["status"] = status
            break
    # Simpan data
    with open(FILE_PEMBAYARAN, "w") as f:
        for p in data_pembayaran:
            f.write(f"{p['idBayar']}|{p['sewaId']}|{p['metode']}|{p['total']}|{p['tanggal']}|{p['status']}\n")

    
def bayar_pesanan_user(idBayar):
    print("\n=== PEMBAYARAN TIKET===")
    if idBayar == None:
        bayarId = input("Masukkan kode pembayaran Anda: ")
    else:
        bayarId = idBayar

    for p in data_pembayaran:
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
                print("Pembayaran sudah lunas.")
                break
        

def pesan_tiket(mitraId):
    print("\n=== TAMBAH TIKET BARU ===")
    pembelianId = generateId()


    # nama = input_text("Nama: ")
    customerId = input_customer()
    tiket = input_id(mitraId)
    tanggal = input_tanggal()

    for t in tiket:
        if t["idTiket"] == tiket:
            harga = t["harga"]
            break

    bayarId = create_pembayaran(pembelianId, harga)
    status = "daftar"  # Auto-fill status

    with open("dataTiket.txt", "a") as file:
        data = f"{pembelianId}|{customerId}|{tiket}|{tanggal}|{status}\n"
        file.write(data)

    print(f"✅ Tiket berhasil ditambahkan dengan status: {status}")
    bayar_pesanan_user(bayarId)
    print("kode pembayaran anda adalah: ", bayarId)
    input("\nTekan Enter untuk melanjutkan...")
    

def pesan_tiket_by_customer(customerId):
    print("\n=== TAMBAH TIKET BARU ===")
    pembelianId = generateId()


    # nama = input_text("Nama: ")
    tiket = input_tiket()
    if tiket == False:
        print("tidak ada tiket yang tersedia")
        return      
    tanggal = input_tanggal()

    for t in tiket:
        if t["idTiket"] == tiket:
            harga = t["harga"]
            break

    bayarId = create_pembayaran(pembelianId, harga)

    
    status = "daftar"  # Auto-fill status

    with open("dataTiket.txt", "a") as file:
        data = f"{pembelianId}|{customerId}|{tiket}|{tanggal}|{status}\n"
        file.write(data)

    print(f"✅ Tiket berhasil ditambahkan dengan status: {status}")
    bayar_pesanan_user(bayarId)
    print("kode pembayaran anda adalah: ", bayarId)
    input("\nTekan Enter untuk melanjutkan...")

def lihat_tiket():
    try:
        with open("dataTiket.txt", "r") as file:
            lines = file.readlines()
            
        if not lines:
            print("📋 Data tiket masih kosong")
        else:
            print("\n=== DAFTAR PEMESANAN TIKET ===")
            ada_data = False
            for line in lines:
                line = line.strip()
                
                # Skip header dan baris kosong
                if not line or is_header(line):
                    continue
                    
                if '|' in line:
                    data = line.split("|")
                    if len(data) == 5:  # Update: sekarang 8 kolom (dengan Status)
                        try:
                            ada_data = True
                            # Emoji untuk status
                            status_emoji = "✅" if data[7] == "Sudah Terpakai" else "🎫"
                            print(f"Id: {data[0]}")
                            for c in customers:
                                if c['idCustomer'] == data[1]:
                                    print(f"nama: {c['nama']}")
                            for t in tiket:
                                if t['idTiket'] == data[2]:
                                    print(f"nama Tiket: {t['namaTiket']}")
                                    print(f"harga: {t['harga']}")
                                    print(f"jenis Tiket : {t['jenis']}")
                            print(f"tanggal: {data[3]}")
                            print(f"status: {status_emoji} {data[4]}")
                            for b in data_pembayaran:
                                if b['idBayar'] == data[5]:
                                    print(f"kode pembayaran: {b['idBayar']}")
                                    print(f"status pembayaran: {b['status']}")
                        except ValueError:
                            print(f"⚠️  Data rusak ditemukan, baris dilewati: {line[:50]}...")
                            continue
            
            if not ada_data:
                print("📋 Tidak ada data tiket yang valid")
                
    except FileNotFoundError:
        print("📋 Data tiket belum ada")
    
    input("\nTekan Enter untuk melanjutkan...")

def lihat_tiket_by_mitraId(mitraId):
    for t in tiket:
        if t['mitraId'] == mitraId:
            tiketId = t['idTiket']
    try:
        with open("dataTiket.txt", "r") as file:
            lines = file.readlines()
            
        if not lines:
            print("📋 Data tiket masih kosong")
        else:
            print("\n=== DAFTAR TIKET ===")
            ada_data = False
            for line in lines:
                line = line.strip()
                
                
                # Skip header dan baris kosong
                if not line or is_header(line):
                    continue
                    
                if '|' in line:
                    data = line.split("|")
                    if data[2] == tiketId:
                        if len(data) == 5:  # Update: sekarang 8 kolom (dengan Status)
                            try:
                                ada_data = True
                                # Emoji untuk status
                                status_emoji = "✅" if data[7] == "Sudah Terpakai" else "🎫"
                                print(f"Id: {data[0]}")
                                for c in customers:
                                    if c['idCustomer'] == data[1]:
                                        print(f"nama: {c['nama']}")
                                for t in tiket:
                                    if t['idTiket'] == data[2]:
                                        print(f"nama Tiket: {t['namaTiket']}")
                                        print(f"harga: {t['harga']}")
                                        print(f"jenis Tiket : {t['jenis']}")
                                print(f"tanggal: {data[3]}")
                                print(f"status: {status_emoji} {data[7]}")
                                for b in data_pembayaran:
                                    if b['idBayar'] == data[5]:
                                        print(f"kode pembayaran: {b['idBayar']}")
                                        print(f"status pembayaran: {b['status']}")
                            except ValueError:
                                print(f"⚠️  Data rusak ditemukan, baris dilewati: {line[:50]}...")
                                continue
            
            if not ada_data:
                print("📋 Tidak ada data tiket yang valid")
                
    except FileNotFoundError:
        print("📋 Data tiket belum ada")
    
    input("\nTekan Enter untuk melanjutkan...")

def lihat_tiket_by_customerId(customerId):
    try:
        with open("dataTiket.txt", "r") as file:
            lines = file.readlines()
            
        if not lines:
            print("📋 Data tiket masih kosong")
        else:
            print("\n=== DAFTAR TIKET ===")
            ada_data = False
            for line in lines:
                line = line.strip()
                
                
                # Skip header dan baris kosong
                if not line or is_header(line):
                    continue
                    
                if '|' in line:
                    data = line.split("|")
                    if data[1] == customerId:
                        if len(data) == 5:  # Update: sekarang 8 kolom (dengan Status)
                            try:
                                ada_data = True
                                # Emoji untuk status
                                status_emoji = "✅" if data[7] == "Sudah Terpakai" else "🎫"
                                print(f"Id: {data[0]}")
                                for c in customers:
                                    if c['idCustomer'] == data[1]:
                                        print(f"nama: {c['nama']}")
                                for t in tiket:
                                    if t['idTiket'] == data[2]:
                                        print(f"nama Tiket: {t['namaTiket']}")
                                        print(f"harga: {t['harga']}")
                                        print(f"jenis Tiket : {t['jenis']}")
                                print(f"tanggal: {data[3]}")
                                print(f"status: {status_emoji} {data[7]}")
                            except ValueError:
                                print(f"⚠️  Data rusak ditemukan, baris dilewati: {line[:50]}...")
                                continue
            
            if not ada_data:
                print("📋 Tidak ada data tiket yang valid")
                
    except FileNotFoundError:
        print("📋 Data tiket belum ada")
    
    input("\nTekan Enter untuk melanjutkan...")

def update_tiket(mitraId):
    print("\n=== UPDATE SCHEDULE (TANGGAL SAJA) ===")
    lihat_tiket_by_mitraId(mitraId)
    id_cari = input("Masukkan ID Tiket yang ingin diupdate tanggalnya: ").strip()

    try:
        with open("dataTiket.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("❌ File data tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    found = False
    tanggal_baru = input_tanggal()

    with open("dataTiket.txt", "w") as file:
        for line in lines:
            line_stripped = line.strip()

            if is_header(line_stripped):
                file.write(line)
                continue

            if line_stripped and '|' in line_stripped:
                data = line_stripped.split("|")
                if len(data) == 8 and data[0] == id_cari:
                    found = True
                    data[5] = tanggal_baru
                    line = "|".join(data) + "\n"
                    print("✅ Schedule berhasil diupdate!")

            file.write(line)

    if not found:
        print(f"❌ Tiket dengan ID '{id_cari}' tidak ditemukan")

    input("\nTekan Enter untuk melanjutkan...")

def verifikasi_tiket(mitraId):
    print("\n=== VERIFIKASI TIKET ===")
    lihat_tiket_by_mitraId(mitraId)
    id_cari = input("Masukkan ID Tiket yang ingin diverifikasi: ").strip()

    try:
        with open("dataTiket.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("❌ File data tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    found = False
    tiket_info = None

    # Cari tiket dan tampilkan informasinya
    for line in lines:
        line_stripped = line.strip()
        if line_stripped and '|' in line_stripped and not is_header(line_stripped):
            data = line_stripped.split("|")
            if len(data) == 8 and data[0] == id_cari:
                found = True
                tiket_info = data
                break

    if not found:
        print(f"❌ Tiket dengan ID '{id_cari}' tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    # Tampilkan info tiket
    print(f"""
╔══════════════════════════════════╗
║     INFORMASI TIKET              ║
╚══════════════════════════════════╝
ID       : {tiket_info[0]}
Jenis    : {tiket_info[1]}
Nama     : {tiket_info[2]}
Asal     : {tiket_info[3]}
Tujuan   : {tiket_info[4]}
Tanggal  : {tiket_info[5]}
Harga    : Rp {int(tiket_info[6]):,}
Status   : {tiket_info[7]}
""")

    # Cek status tiket
    if tiket_info[7] == "Sudah Terpakai":
        print("❌ Tiket ini sudah terpakai sebelumnya!")
        input("\nTekan Enter untuk melanjutkan...")
        return

    # Konfirmasi verifikasi
    print("Apakah Anda yakin ingin memverifikasi tiket ini?")
    konfirmasi = input("Ketik 'ya' untuk konfirmasi: ").strip().lower()

    if konfirmasi != 'ya':
        print("⚠️  Verifikasi dibatalkan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    # Update status tiket menjadi "Sudah Terpakai"
    with open("dataTiket.txt", "w") as file:
        for line in lines:
            line_stripped = line.strip()

            if is_header(line_stripped):
                file.write(line)
                continue

            if line_stripped and '|' in line_stripped:
                data = line_stripped.split("|")
                if len(data) == 8 and data[0] == id_cari:
                    data[7] = "Sudah Terpakai"
                    line = "|".join(data) + "\n"

            file.write(line)

    print("✅ Tiket berhasil diverifikasi! Status diubah menjadi 'Sudah Terpakai'")
    input("\nTekan Enter untuk melanjutkan...")

def hapus_tiket():
    print("\n=== HAPUS TIKET ===")
    id_cari = input("Masukkan ID Tiket yang ingin dihapus: ").strip()

    try:
        with open("dataTiket.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("❌ File data tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    found = False
    with open("dataTiket.txt", "w") as file:
        for line in lines:
            line_stripped = line.strip()
            
            # Tulis ulang header jika ada
            if is_header(line_stripped):
                file.write(line)
                continue
                
            if line_stripped and '|' in line_stripped:
                data = line_stripped.split("|")
                if len(data) >= 1 and data[0] == id_cari:
                    found = True
                else:
                    file.write(line)

    if found:
        print("✅ Tiket berhasil dihapus!")
    else:
        print(f"❌ Tiket dengan ID '{id_cari}' tidak ditemukan")
    
    input("\nTekan Enter untuk melanjutkan...")

# def bersihkan_data():
#     print("\n=== BERSIHKAN DATA RUSAK ===")
#     try:
#         with open("dataTiket.txt", "r") as file:
#             lines = file.readlines()
        
#         data_valid = []
#         data_rusak = 0
#         has_header = False
        
#         for line in lines:
#             line_stripped = line.strip()
            
#             # Simpan header jika ada
#             if is_header(line_stripped):
#                 has_header = True
#                 continue
                
#             if line_stripped and '|' in line_stripped:
#                 data = line_stripped.split("|")
#                 if len(data) == 8:  # Update: sekarang harus 8 kolom
#                     try:
#                         int(data[6])  # Validasi harga
#                         # Validasi status
#                         if data[7] in ["Belum Terpakai", "Sudah Terpakai"]:
#                             data_valid.append(line)
#                         else:
#                             data_rusak += 1
#                     except ValueError:
#                         data_rusak += 1
#                 else:
#                     data_rusak += 1
        
#         # Tulis ulang tanpa header
#         with open("dataTiket.txt", "w") as file:
#             file.writelines(data_valid)
        
#         print(f"✅ Pembersihan selesai!")
#         if has_header:
#             print(f"   Header dihapus: 1")
#         print(f"   Data valid: {len(data_valid)}")
#         print(f"   Data rusak dihapus: {data_rusak}")
        
#     except FileNotFoundError:
#         print("❌ File data tidak ditemukan")
    
#     input("\nTekan Enter untuk melanjutkan...")

# # Program Utama
# while True:
#     clear_screen()
#     print("""
# ╔══════════════════════════════════╗
# ║  APLIKASI PEMESANAN TIKET        ║
# ╚══════════════════════════════════╝

# 1. 📝 Tambah Tiket
# 2. 📋 Lihat Tiket
# 3. ✏️  Update Tiket
# 4. ✅ Verifikasi Tiket
# 5. 🗑️  Hapus Tiket
# 6. 🧹 Bersihkan Data Rusak
# 7. 🚪 Keluar
# """)

#     pilih = input("Pilih menu (1-7): ").strip()

#     if pilih == "1":
#         pesan_tiket()
#     elif pilih == "2":
#         lihat_tiket()
#     elif pilih == "3":
#         update_tiket()
#     elif pilih == "4":
#         verifikasi_tiket()
#     elif pilih == "5":
#         hapus_tiket()
#     elif pilih == "6":
#         bersihkan_data()
#     elif pilih == "7":
#         print("\nTerima kasih telah menggunakan aplikasi!")
#         break
#     else:
#         print("❌ Pilihan tidak valid! Pilih angka 1-7")
#         input("\nTekan Enter untuk melanjutkan...")

load_data()

def menu_customer(customerId):
    while True:
        print("\n=== NAVICA - PEMESANAN TIKET ===")
        print("1. pesan Tiket")
        print("2. lihat Tiket")
        print("3. Pembayaran Tiket")
        print("0. Keluar")
        pilihan = input("Pilih menu (0-2): ")
        if pilihan == "1":
            pesan_tiket_by_customer(customerId)
        elif pilihan == "2":
            lihat_tiket_by_customerId(customerId)
        elif pilihan == '3':
            bayar_pesanan_user(idBayar=None)
        elif pilihan == "0":
            print("Keluar dari menu pemesanan tiket.")
            break
        else:
            print("Pilihan tidak valid.")