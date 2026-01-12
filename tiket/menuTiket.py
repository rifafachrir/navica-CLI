import os
import sys
import tiket.dataTiket as pembelian


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
3. ✏️ Update Tiket
4. ✅ Verifikasi Tiket
5. 📝 buat Tiket
6. 📖 lihat Tiket
7. 📝 ubah tiket
8. 🗑️  hapus tiket
0. 🚪 Keluar
""")

        pilih = input("Pilih menu (1-7): ").strip()

        if pilih == "1":
            pembelian.pesan_tiket(mitraId)
        elif pilih == "2":
            pembelian.lihat_tiket_by_mitraId(mitraId)
        elif pilih == "3":
            pembelian.update_tiket(mitraId)
        elif pilih == "4":
            pembelian.verifikasi_tiket(mitraId)
        elif pilih == "0":
            print("\nTerima kasih telah menggunakan aplikasi!")
            break
        else:
            print("❌ Pilihan tidak valid! Pilih angka 1-7")
            input("\nTekan Enter untuk melanjutkan...")


if __name__ == "__main__":
    menu_tiket()