import os
import sys
import tiket.dataTiket as pembelian
import tiket.tiket as tiket


sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def menu_tiket(userId):
    with open("database/dataMitra.txt", "r") as f:
        for line in f:
            bagian = line.strip().split("|")
            if bagian[1] == userId:
                mitraId = bagian[0]

    while True:
    
        print("""
╔══════════════════════════════════╗
║  APLIKASI PEMESANAN TIKET        ║
╚══════════════════════════════════╝

1. 🧾 pesan Tiket
2. 🧾 Lihat Pemesanan Tiket
3. ✅ Verifikasi Tiket
4. 📝 buat Tiket
5. 📖 lihat Tiket
6. 📝 ubah tiket
7. 🗑️  hapus tiket
0. 🚪 Keluar
""")

        pilih = input("Pilih menu (0-7): ").strip()

        if pilih == "1":
            pembelian.pesan_tiket(mitraId)
        elif pilih == "2":
            pembelian.lihat_tiket_by_mitraId(mitraId)
        elif pilih == "3":
            pembelian.verifikasi_tiket(mitraId)
        elif pilih == "4":
            tiket.create_tiket_with_mitra(mitraId)
        elif pilih == "5":
            tiket.list_tiket(mitraId)
        elif pilih == "6":
            tiket.update_tiket(mitraId)
        elif pilih == "7":
            tiket.delete_tiket(mitraId)
        elif pilih == "0":
            print("\nTerima kasih telah menggunakan aplikasi!")
            break
        else:
            print("❌ Pilihan tidak valid! Pilih angka 1-7")
            input("\nTekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    menu_tiket()