import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import kendaraan.pemilikKendaraan as pemilkKendaraan
import kendaraan.penyewaKendaraan as penyewa

def menu_pemilik_kendaraan(userId):
    mitraId = None
    
    with open ("database/dataMitra.txt", 'r') as f:
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) >= 2 and bagian[1] == userId:
                mitraId = bagian[0]
                break
            
    if mitraId is None:
        print("Data mitra tidak ditemukan untuk user ini.")
        return

    while True: 
        print("=== Selamat Datang pemilik kendaraan ===")
        print("1. lihat data peminjaman")
        print("2. Lihat data kendaraan yang ada")
        print("3. Tambah data kendaraan yang ingin dipinjam")
        print("4. konfirmasi peminjaman")
        print("5. ganti kendaraan")
        print("6. Konfirmasi Pengembalian")
        print("0. Keluar")
        menu = input("Pilih menu (1-6): ").strip()
        if menu == "":
            print("Menu tidak boleh kosong.")
            continue

        if menu == "1":
            penyewa.lihat_penyewa_by_mitraId(mitraId)
        elif menu == "2":
            pemilkKendaraan.lihat_kendaraan_by_mitraId(mitraId)
        elif menu == "3":
            pemilkKendaraan.tambah_kendaraan_by_mitraId(mitraId)
        elif menu == "4":
            penyewa.konfirmasi_peminjaman(mitraId)
        elif menu == "5":
            penyewa.ubah_peminjaman(mitraId)
        elif menu == "6":
            penyewa.konfirmasi_pengembalian(mitraId)
        elif menu == "0":
            break
        else:
            print("Pilihan tidak dikenal silahkan coba lagi.")

if __name__ == "__main__":
    menu_pemilik_kendaraan("U001")
