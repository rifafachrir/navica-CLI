import kendaraan.penyewaKendaraan as penyewa
import kendaraan.pemilikKendaraan as pemilkKendaraan
import os
import sys

# Setup path agar bisa import modul lain
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modul yang dibutuhkan untuk menu


def menu_pemilik_kendaraan(userId):
    mitraId = None

    # Cek apakah file dataMitra ada
    if os.path.exists("database/dataMitra.txt"):
        with open("database/dataMitra.txt", 'r') as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                # Format: mitraId|userId|nama|alamat|...
                if len(bagian) >= 2 and bagian[1] == userId:
                    mitraId = bagian[0]
                    break

    if mitraId is None:
        print("\n[ERROR] Akun ini belum terdaftar di dataMitra.txt!")
        print(f"User ID Anda: {userId}")
        print("Pastikan User ID ini ada di file database/dataMitra.txt kolom ke-2.")
        return

    # Masuk ke menu jika mitraId sudah aman
    while True:
        print("\n=== Selamat Datang pemilik kendaraan ===")
        print(f"Mitra ID: {mitraId}")
        print("1. Lihat data peminjaman")
        print("2. Lihat data kendaraan yang ada")
        print("3. Tambah data kendaraan yang ingin dipinjam")
        print("4. Konfirmasi peminjaman")
        print("5. Ganti kendaraan")
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
