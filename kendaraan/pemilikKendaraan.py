import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kendaraan.penyewaKendaraan as penyewaKendaraan

data_pemilik = [] #data mitra
kendaraan_data = []

FILE_KENDARAAN = "database/dataKendaraan.txt"
FILE_MITRA = "database/dataMitra.txt"
file = os.path.exists(FILE_KENDARAAN) and os.path.exists(FILE_MITRA)

def input_angka(prompt):
    val = input(prompt).strip()
    if val == "" or not val.isdigit():
        return None
    return int(val)

def input_teks(prompt):
    val = input(prompt).strip()
    if val == "":
        return None
    return val

def load_data():
    
    if file:
        valid_mitra_ids = set()
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
                    print("Format data kendaraan tidak valid:", line)
                    continue
                
        with open(FILE_MITRA, "r") as f:
            lines = f.readlines()
            mitra_ditemukan = False
            
            for line in lines:
                bagian = line.strip().split("|")
                if bagian[0] in valid_mitra_ids:
                    data_pemilik.append({
                        "mitraId": bagian[0],
                        "userId": bagian[1],
                        "namaMitra": bagian[2],
                        "alamat": bagian[3],
                    })
                mitra_ditemukan = True

            if not mitra_ditemukan:
                print("Tidak ada mitra yang memiliki kendaraan.")
        

def tambah_kendaraan():
    print("\n=== Tambah Data Kendaraan ===")
    print("Masukkan ID Mitra Pemilik Kendaraan: ")
    
    if not data_pemilik:
        print("Data mitra kosong.")
        return

    noKendaraan = input_teks("Masukkan no Polisi Kendaraan: ")
    if noKendaraan is None:
        print("Input dibatalkan.")
        return

    for i, mitra in enumerate(data_pemilik):
        print(f"{i + 1}. {mitra['namaMitra']} (ID: {mitra['mitraId']})")
    
    pilihan = int(input("Pilih mitra yang ingin menambahkan kendaraan: ")) - 1
    if pilihan is None or pilihan < 1 or pilihan > len(data_pemilik):
        print("Pilihan tidak valid.")
        return

    mitraId = data_pemilik[pilihan - 1]['mitraId']

    nama_kendaraan = input_teks("Nama Kendaraan: ")
    harga_sewa = input_teks("Harga Sewa per Hari: ")

    if nama_kendaraan is None or harga_sewa is None:
        print("Data tidak lengkap.")
        return

    kendaraan_data.append({
        "noKendaraan": noKendaraan,
        "mitraId": mitraId,
        "namaKendaraan": nama_kendaraan,
        "hargaSewaPerHari": harga_sewa,
        "status": "tersedia"
    })
    
    with open(FILE_KENDARAAN, "a") as f:
        f.write(f"{noKendaraan}|{mitraId}|{nama_kendaraan}|{harga_sewa}|tersedia\n")
    print("Data kendaraan berhasil ditambahkan!\n")

def tambah_kendaraan_by_mitraId(mitraId):
    print("\n=== Tambah Data Kendaraan ===")
    print("Masukkan ID Mitra Pemilik Kendaraan: ")
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
    print("\n=== Daftar Data Kendaraan ===")
    if len(kendaraan_data) == 0:
        print("Belum ada data kendaraan.\n")
        return

    for i, k in enumerate(kendaraan_data):
        print(f"{1+i}")
        print(f"noPolisi: {k['noKendaraan']}")
        for m in data_pemilik:
            if m['mitraId'] == k['mitraId']:
                print(f"Nama Mitra: {m['namaMitra']}")
        print(f"namaKendaraan: {k['namaKendaraan']}")
        print(f"hargaSewaPerHari: {k['hargaSewaPerHari']}")
        print(f"status: {k['status']}")

    print("-" * 30)

def lihat_kendaraan_by_mitraId(mitraId):
    print("\n=== Daftar Data Kendaraan ===")
    if len(kendaraan_data) == 0:
        print("Belum ada data kendaraan.\n")
        return

    for i, k in enumerate(kendaraan_data):
        if k['mitraId'] != mitraId:
            print(f"{1+i}")
            print(f"noPolisi: {k['noKendaraan']}")
            for m in data_pemilik:
                if m['mitraId'] == k['mitraId']:
                    print(f"Nama Mitra: {m['namaMitra']}")
            print(f"namaKendaraan: {k['namaKendaraan']}")
            print(f"hargaSewaPerHari: {k['hargaSewaPerHari']}")
            print(f"status: {k['status']}")

    print("-" * 30)

def edit_kendaraan():
    lihat_kendaraan()
    if not kendaraan_data:
        return

    index = input_angka("Pilih nomor data yang ingin diedit: ")
    if index is None or index < 1 or index > len(kendaraan_data):
        print("Nomor tidak valid!")
        return

    print("\n--- Masukkan data baru (ENTER jika tidak ingin mengubah) ---")
    noKendaraan = input_teks("No Polisi baru: ")

    print("Pilih mitra baru (ENTER untuk lewati):")
    for i, mitra in enumerate(data_pemilik):
        print(f"{i + 1}. {mitra['namaMitra']}")

    pilihan = input_angka("Nomor mitra: ")
    mitraId = None
    if pilihan and 1 <= pilihan <= len(data_pemilik):
        mitraId = data_pemilik[pilihan - 1]['mitraId']

    nama_kendaraan = input_teks("Nama Kendaraan baru: ")
    harga_sewa = input_teks("Harga Sewa per Hari baru: ")

    if noKendaraan: kendaraan_data[index]['noKendaraan'] = noKendaraan
    if mitraId: kendaraan_data[index]['mitraId'] = mitraId
    if nama_kendaraan: kendaraan_data[index]['namaKendaraan'] = nama_kendaraan
    if harga_sewa: kendaraan_data[index]['hargaSewaPerHari'] = harga_sewa

    with open(FILE_KENDARAAN, "w") as f:
        for k in kendaraan_data:
            f.write(f"{k['noKendaraan']}|{k['mitraId']}|{k['namaKendaraan']}|{k['hargaSewaPerHari']}|{k['status']}\n")
            
    print("Data kendaraan berhasil diperbarui!\n")

def hapus_kendaraan():
    lihat_kendaraan()
    if not kendaraan_data:
        return

    index = input_angka("Pilih nomor data yang ingin dihapus: ")
    if index is None or index < 1 or index > len(kendaraan_data):
        print("Nomor tidak valid!")
        return

    kendaraan_data.pop(index - 1)
    with open(FILE_KENDARAAN, "w") as f:
        for k in kendaraan_data:
            f.write(f"{k['noKendaraan']}|{k['mitraId']}|{k['namaKendaraan']}|{k['hargaSewaPerHari']}|{k['status']}\n")
    print("Data kendaraan berhasil dihapus!\n")

def menuAdmin():
    while True:
        print("=== MENU PEMILIK KENDARAAN ===")
        print("1. Tambah Kendaraan")
        print("2. Lihat Pemilik")
        print("3. Edit Pemilik")
        print("4. Hapus Pemilik")
        print("5. Keluar")

        pilih = input("Pilih menu: ").strip()
        if pilih == "":
            print("Input tidak boleh kosong.\n")
            continue

        if pilih == "1": tambah_kendaraan()
        elif pilih == "2": lihat_kendaraan()
        elif pilih == "3": edit_kendaraan()
        elif pilih == "4": hapus_kendaraan()
        elif pilih == "5":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!\n")
load_data()

if __name__ == "__main__":
    menuAdmin()