import os
import re
from datetime import datetime

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

def input_jenis():
    while True:
        jenis = input("Jenis (Transportasi/Hiburan): ").strip().lower()
        if jenis in ['transportasi', 'hiburan']:
            return jenis.capitalize()
        print("❌ Jenis hanya boleh 'Transportasi' atau 'Hiburan'!")

def input_id():
    while True:
        id_tiket = input("ID Tiket (tanpa spasi): ").strip()
        if id_tiket and not ' ' in id_tiket:
            return id_tiket
        print("❌ ID Tiket tidak boleh kosong atau mengandung spasi!")

def input_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print(f"❌ {prompt.split(':')[0]} tidak boleh kosong!")

def is_header(line):
    return line.strip() == "ID|Jenis|Nama|Asal|Tujuan|Tanggal|Harga|Status"

def tambah_tiket():
    print("\n=== TAMBAH TIKET BARU ===")
    
    id_tiket = input_id()
    jenis = input_jenis()
    nama = input_text("Nama: ")
    asal = input_text("Asal: ")

    if jenis == "Hiburan":
        tujuan = "-"
    else:
        tujuan = input_text("Tujuan: ")

    tanggal = input_tanggal()
    harga = input_harga()
    status = "Belum Terpakai"  # Auto-fill status

    with open("dataTiket.txt", "a") as file:
        data = f"{id_tiket}|{jenis}|{nama}|{asal}|{tujuan}|{tanggal}|{harga}|{status}\n"
        file.write(data)

    print(f"✅ Tiket berhasil ditambahkan dengan status: {status}")
    input("\nTekan Enter untuk melanjutkan...")

def lihat_tiket():
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
                    if len(data) == 8:  # Update: sekarang 8 kolom (dengan Status)
                        try:
                            harga_int = int(data[6])
                            ada_data = True
                            # Emoji untuk status
                            status_emoji = "✅" if data[7] == "Sudah Terpakai" else "🎫"
                            print(f"""
ID       : {data[0]}
Jenis    : {data[1]}
Nama     : {data[2]}
Asal     : {data[3]}
Tujuan   : {data[4]}
Tanggal  : {data[5]}
Harga    : Rp {harga_int:,}
Status   : {status_emoji} {data[7]}
-------------------------""")
                        except ValueError:
                            print(f"⚠️  Data rusak ditemukan, baris dilewati: {line[:50]}...")
                            continue
            
            if not ada_data:
                print("📋 Tidak ada data tiket yang valid")
                
    except FileNotFoundError:
        print("📋 Data tiket belum ada")
    
    input("\nTekan Enter untuk melanjutkan...")

def update_tiket():
    print("\n=== UPDATE SCHEDULE (TANGGAL SAJA) ===")
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

def verifikasi_tiket():
    print("\n=== VERIFIKASI TIKET ===")
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

def bersihkan_data():
    print("\n=== BERSIHKAN DATA RUSAK ===")
    try:
        with open("dataTiket.txt", "r") as file:
            lines = file.readlines()
        
        data_valid = []
        data_rusak = 0
        has_header = False
        
        for line in lines:
            line_stripped = line.strip()
            
            # Simpan header jika ada
            if is_header(line_stripped):
                has_header = True
                continue
                
            if line_stripped and '|' in line_stripped:
                data = line_stripped.split("|")
                if len(data) == 8:  # Update: sekarang harus 8 kolom
                    try:
                        int(data[6])  # Validasi harga
                        # Validasi status
                        if data[7] in ["Belum Terpakai", "Sudah Terpakai"]:
                            data_valid.append(line)
                        else:
                            data_rusak += 1
                    except ValueError:
                        data_rusak += 1
                else:
                    data_rusak += 1
        
        # Tulis ulang tanpa header
        with open("dataTiket.txt", "w") as file:
            file.writelines(data_valid)
        
        print(f"✅ Pembersihan selesai!")
        if has_header:
            print(f"   Header dihapus: 1")
        print(f"   Data valid: {len(data_valid)}")
        print(f"   Data rusak dihapus: {data_rusak}")
        
    except FileNotFoundError:
        print("❌ File data tidak ditemukan")
    
    input("\nTekan Enter untuk melanjutkan...")

# Program Utama
while True:
    clear_screen()
    print("""
╔══════════════════════════════════╗
║  APLIKASI PEMESANAN TIKET        ║
╚══════════════════════════════════╝

1. 📝 Tambah Tiket
2. 📋 Lihat Tiket
3. ✏️  Update Tiket
4. ✅ Verifikasi Tiket
5. 🗑️  Hapus Tiket
6. 🧹 Bersihkan Data Rusak
7. 🚪 Keluar
""")

    pilih = input("Pilih menu (1-7): ").strip()

    if pilih == "1":
        tambah_tiket()
    elif pilih == "2":
        lihat_tiket()
    elif pilih == "3":
        update_tiket()
    elif pilih == "4":
        verifikasi_tiket()
    elif pilih == "5":
        hapus_tiket()
    elif pilih == "6":
        bersihkan_data()
    elif pilih == "7":
        print("\n✨ Terima kasih telah menggunakan aplikasi!")
        break
    else:
        print("❌ Pilihan tidak valid! Pilih angka 1-7")
        input("\nTekan Enter untuk melanjutkan...")