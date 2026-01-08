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
        jenis = input("Jenis (Hotel/Pesawat): ").strip().lower()
        if jenis in ['hotel', 'pesawat']:
            return jenis.capitalize()
        print("❌ Jenis hanya boleh 'Hotel' atau 'Pesawat'!")

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
    return line.strip() == "ID|Jenis|Nama|Asal|Tujuan|Tanggal|Harga"

def tambah_tiket():
    print("\n=== TAMBAH TIKET BARU ===")
    
    id_tiket = input_id()
    jenis = input_jenis()
    nama = input_text("Nama Hotel/Maskapai: ")
    asal = input_text("Kota Asal: ")
    
    if jenis == "Hotel":
        tujuan = "-"
    else:
        tujuan = input_text("Kota Tujuan: ")
    
    tanggal = input_tanggal()
    harga = input_harga()

    with open("dataTiket.txt", "a") as file:
        data = f"{id_tiket}|{jenis}|{nama}|{asal}|{tujuan}|{tanggal}|{harga}\n"
        file.write(data)

    print("✅ Tiket berhasil ditambahkan!")
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
                    if len(data) == 7:
                        try:
                            harga_int = int(data[6])
                            ada_data = True
                            print(f"""
ID       : {data[0]}
Jenis    : {data[1]}
Nama     : {data[2]}
Asal     : {data[3]}
Tujuan   : {data[4]}
Tanggal  : {data[5]}
Harga    : Rp {harga_int:,}
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
    print("\n=== UPDATE TIKET ===")
    id_cari = input("Masukkan ID Tiket yang ingin diubah: ").strip()

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
                    print("\n📝 Masukkan data baru:")
                    jenis = input_jenis()
                    nama = input_text("Nama: ")
                    asal = input_text("Asal: ")
                    
                    if jenis == "Hotel":
                        tujuan = "-"
                    else:
                        tujuan = input_text("Tujuan: ")
                    
                    tanggal = input_tanggal()
                    harga = input_harga()

                    line = f"{id_cari}|{jenis}|{nama}|{asal}|{tujuan}|{tanggal}|{harga}\n"
                    print("✅ Tiket berhasil diupdate!")
                
                file.write(line)
    
    if not found:
        print(f"❌ Tiket dengan ID '{id_cari}' tidak ditemukan")
    
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
                if len(data) == 7:
                    try:
                        int(data[6])
                        data_valid.append(line)
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
4. 🗑️  Hapus Tiket
5. 🧹 Bersihkan Data Rusak
6. 🚪 Keluar
""")

    pilih = input("Pilih menu (1-6): ").strip()

    if pilih == "1":
        tambah_tiket()
    elif pilih == "2":
        lihat_tiket()
    elif pilih == "3":
        update_tiket()
    elif pilih == "4":
        hapus_tiket()
    elif pilih == "5":
        bersihkan_data()
    elif pilih == "6":
        print("\n✨ Terima kasih telah menggunakan aplikasi!")
        break
    else:
        print("❌ Pilihan tidak valid! Pilih angka 1-6")
        input("\nTekan Enter untuk melanjutkan...")