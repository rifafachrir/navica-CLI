import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kendaraan.penyewaKendaraan as penyewaKendaraan

data_pemilik = [] #data mitra
kendaraan_data = []

FILE_KENDARAAN = "database/dataKendaraan.txt"
FILE_MITRA = "database/dataMitra.txt"
file = os.path.exists(FILE_KENDARAAN) and os.path.exists(FILE_MITRA)

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
                        "namaMitra": bagian[1],
                        "namaKendaraan": bagian[2],
                        "hargaSewaPerHari": bagian[3],
                        "status": bagian[4]
                    })
                else:
                    print("Format data kendaraan tidak valid:", line)
                    continue
                
        with open(FILE_MITRA, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                if bagian[0] in valid_mitra_ids:
                    data_pemilik.append({
                        "mitraId": bagian[0],
                        "userId": bagian[1],
                        "namaMitra": bagian[2],
                        "alamat": bagian[3],
                    })
                else:
                    print("Tidak ada mitra untuk pemilik kendaraan")
                    continue
        

def tambah_kendaraan():
    print("\n=== Tambah Data Kendaraan ===")
    print("Masukkan ID Mitra Pemilik Kendaraan: ")
    noKendaraan = input("Masukkan no Polisi Kendaraan: ")
    for i, mitra in enumerate(data_pemilik):
        print(f"{i + 1}. {mitra['nama']} (ID: {mitra['mitraId']})")
    pilihan = int(input("Pilih mitra yang ingin menambahkan kendaraan: ")) - 1
    if 0 <= pilihan < len(data_pemilik):
        namaMitra = data_pemilik[pilihan]['namaMitra']
    else:
        print("Pilihan tidak valid.")
        return
    nama_kendaraan = input("Nama Kendaraan: ")
    harga_sewa = input("Harga Sewa per Hari: ")

    kendaraan = {
        "noKendaraan": noKendaraan,
        "namaMitra": namaMitra,
        "namaKendaraan": nama_kendaraan,
        "hargaSewaPerHari": harga_sewa,
        "status": "tersedia"
    }

    kendaraan_data.append(kendaraan)
    with open(FILE_KENDARAAN, "a") as f:
        f.write(f"{noKendaraan}|{namaMitra}|{nama_kendaraan}|{harga_sewa}|tersedia\n")
    print("Data kendaraan berhasil ditambahkan!\n")



def lihat_kendaraan():
    print("\n=== Daftar Data Kendaraan ===")
    if len(kendaraan_data) == 0:
        print("Belum ada data kendaraan.\n")
        return

    for i, k in enumerate(kendaraan_data):
        print(f"{1 + i}, kendaraanId: {k['kendaraanId']}, mitraId: {k['mitraId']}, Nama Kendaraan: {k['namaKendaraan']}, Harga Sewa per Hari: {k['hargaSewaPerHari']}, Status: {k['status']} \n")

    print("-" * 30)

def lihat_data_peminjam():
    penyewaKendaraan.lihat_penyewa()


def edit_kendaraan():
    lihat_kendaraan()
    if len(data_pemilik) == 0:
        return

    index = int(input("Pilih nomor data yang ingin diedit: ")) - 1
    if index < 0 or index >= len(kendaraan_data):
        print("Nomor tidak valid!")
        return

    print("\n--- Masukkan data baru (kosongkan jika tidak ingin mengubah) ---")
    noKendaraan = input("Masukkan no Polisi Kendaraan baru: ")
    for i, mitra in enumerate(data_pemilik):
        print(f"{i + 1}. {mitra['nama']} (ID: {mitra['mitraId']})")
    pilihan = int(input("Masukkan nomor mitra baru: ")) - 1
    if 0 <= pilihan < len(data_pemilik):
        namaMitra = data_pemilik[pilihan]['namaMitra']
    else:
        print("Pilihan tidak valid.")
        return
    nama_kendaraan = input("Nama Kendaraan baru: ")
    harga_sewa = input("Harga Sewa per Hari baru: ")

    if noKendaraan: kendaraan_data[index]['noKendaraan'] = noKendaraan
    if namaMitra: kendaraan_data[index]['namaMitra'] = namaMitra
    if nama_kendaraan: kendaraan_data[index]['namaKendaraan'] = nama_kendaraan
    if harga_sewa: kendaraan_data[index]['hargaSewaPerHari'] = harga_sewa

    with open(FILE_KENDARAAN, "w") as f:
        for k in kendaraan_data:
            f.write(f"{k['noKendaraan']}|{k['namaMitra']}|{k['namaKendaraan']}|{k['hargaSewaPerHari']}|{k['status']}\n")
    print("Data kendaraan berhasil diperbarui!\n")

def hapus_kendaraan():
    lihat_kendaraan()
    if len(kendaraan_data) == 0:
        return

    index = int(input("Pilih nomor data yang ingin dihapus: ")) - 1
    if index < 0 or index >= len(kendaraan_data):
        print("Nomor tidak valid!")
        return

    kendaraan_data.pop(index)
    with open(FILE_KENDARAAN, "w") as f:
        for k in kendaraan_data:
            f.write(f"{k['noKendaraan']}|{k['namaMitra']}|{k['namaKendaraan']}|{k['hargaSewaPerHari']}|{k['status']}\n")
    print("Data kendaraan berhasil dihapus!\n")

def menuAdmin():
    while True:
        print("=== MENU PEMILIK KENDARAAN ===")
        print("1. Tambah Kendaraan")
        print("2. Lihat Pemilik")
        print("3. Edit Pemilik")
        print("4. Hapus Pemilik")
        print("5. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1": tambah_kendaraan()
        elif pilih == "2": lihat_kendaraan()
        elif pilih == "3": edit_kendaraan()
        elif pilih == "4": hapus_kendaraan()
        elif pilih == "5":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!\n")

if __name__ == "__main__":
    load_data()
    menuAdmin()