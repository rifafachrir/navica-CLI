import os
import re

# Path ke file database
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "dataMitra.txt")

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def input_id():
    while True:
        id_mitra = input("ID Mitra (tanpa spasi): ").strip()
        if id_mitra and not ' ' in id_mitra:
            return id_mitra
        print("❌ ID Mitra tidak boleh kosong atau mengandung spasi!")

def input_text(prompt):
    while True:
        text = input(prompt).strip()
        if text:
            return text
        print(f"❌ {prompt.split(':')[0]} tidak boleh kosong!")

def input_telepon():
    while True:
        telepon = input("Telepon (angka saja): ")
        if telepon.isdigit() and len(telepon) >= 10:
            return telepon
        print("❌ Telepon hanya boleh ANGKA dan minimal 10 digit!")

def input_email():
    while True:
        email = input("Email: ").strip()
        # Regex sederhana untuk validasi email
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return email
        print("❌ Format email tidak valid! (contoh: nama@domain.com)")

def input_jenis_mitra():
    while True:
        jenis = input("Jenis Mitra ('transportasi', 'hiburan', 'rental', 'penginapan): ").strip().lower()
        if jenis in ['transportasi', 'hiburan', 'rental', 'penginapan']:
            return jenis.capitalize()
        print("❌ Jenis Mitra hanya boleh 'Transportasi', 'Hiburan', 'Rental', atau 'Penginapan'!")

def is_header(line):
    return line.strip() == "ID|Nama|Jenis|Alamat|Telepon|Email|Status"

def tambah_mitra():
    print("\n=== TAMBAH MITRA BARU ===")
    
    id_mitra = input_id()
    nama = input_text("Nama Mitra: ")
    jenis = input_jenis_mitra()
    alamat = input_text("Alamat: ")
    telepon = input_telepon()
    email = input_email()
    status = "Aktif"  # Auto-fill status

    with open(DB_PATH, "a") as file:
        data = f"{id_mitra}|{nama}|{jenis}|{alamat}|{telepon}|{email}|{status}\n"
        file.write(data)

    print(f"✅ Mitra berhasil ditambahkan dengan status: {status}")
    input("\nTekan Enter untuk melanjutkan...")

def lihat_mitra():
    try:
        with open(DB_PATH, "r") as file:
            lines = file.readlines()
            
        if not lines:
            print("📋 Data mitra masih kosong")
        else:
            print("\n=== DAFTAR MITRA ===")
            ada_data = False
            for line in lines:
                line = line.strip()
                
                # Skip header dan baris kosong
                if not line or is_header(line):
                    continue
                    
                if '|' in line:
                    data = line.split("|")
                    if len(data) == 7:
                        ada_data = True
                        # Emoji untuk status
                        status_emoji = "✅" if data[6] == "Aktif" else "❌"
                        print(f"""
ID       : {data[0]}
Nama     : {data[1]}
Jenis    : {data[2]}
Alamat   : {data[3]}
Telepon  : {data[4]}
Email    : {data[5]}
Status   : {status_emoji} {data[6]}
-------------------------""")
            
            if not ada_data:
                print("📋 Tidak ada data mitra yang valid")
                
    except FileNotFoundError:
        print("📋 Data mitra belum ada")
    
    input("\nTekan Enter untuk melanjutkan...")

def update_mitra():
    print("\n=== UPDATE DATA MITRA ===")
    id_cari = input("Masukkan ID Mitra yang ingin diupdate: ").strip()

    try:
        with open(DB_PATH, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("❌ File data tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    found = False
    mitra_lama = None

    # Cari data mitra
    for line in lines:
        line_stripped = line.strip()
        if line_stripped and '|' in line_stripped and not is_header(line_stripped):
            data = line_stripped.split("|")
            if len(data) == 7 and data[0] == id_cari:
                found = True
                mitra_lama = data
                break

    if not found:
        print(f"❌ Mitra dengan ID '{id_cari}' tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    # Tampilkan data lama
    print(f"""
Data Mitra Saat Ini:
Nama     : {mitra_lama[1]}
Jenis    : {mitra_lama[2]}
Alamat   : {mitra_lama[3]}
Telepon  : {mitra_lama[4]}
Email    : {mitra_lama[5]}
Status   : {mitra_lama[6]}
""")

    print("\n=== Masukkan Data Baru (tekan Enter untuk tidak mengubah) ===")
    
    # Input data baru (optional)
    nama = input(f"Nama Mitra [{mitra_lama[1]}]: ").strip() or mitra_lama[1]
    
    jenis_input = input(f"Jenis Mitra [{mitra_lama[2]}] (Transportasi/Hiburan): ").strip().lower()
    if jenis_input in ['transportasi', 'hiburan']:
        jenis = jenis_input.capitalize()
    else:
        jenis = mitra_lama[2]
    
    alamat = input(f"Alamat [{mitra_lama[3]}]: ").strip() or mitra_lama[3]
    
    telepon_input = input(f"Telepon [{mitra_lama[4]}]: ").strip()
    if telepon_input and telepon_input.isdigit() and len(telepon_input) >= 10:
        telepon = telepon_input
    else:
        telepon = mitra_lama[4]
    
    email_input = input(f"Email [{mitra_lama[5]}]: ").strip()
    if email_input and re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email_input):
        email = email_input
    else:
        email = mitra_lama[5]
    
    status = mitra_lama[6]  # Status tetap

    # Update file
    with open(DB_PATH, "w") as file:
        for line in lines:
            line_stripped = line.strip()

            if is_header(line_stripped):
                file.write(line)
                continue

            if line_stripped and '|' in line_stripped:
                data = line_stripped.split("|")
                if len(data) == 7 and data[0] == id_cari:
                    line = f"{id_cari}|{nama}|{jenis}|{alamat}|{telepon}|{email}|{status}\n"

            file.write(line)

    print("✅ Data mitra berhasil diupdate!")
    input("\nTekan Enter untuk melanjutkan...")

def nonaktifkan_mitra():
    print("\n=== NONAKTIFKAN MITRA ===")
    id_cari = input("Masukkan ID Mitra yang ingin dinonaktifkan: ").strip()

    try:
        with open(DB_PATH, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("❌ File data tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    found = False
    mitra_info = None

    # Cari mitra dan tampilkan informasinya
    for line in lines:
        line_stripped = line.strip()
        if line_stripped and '|' in line_stripped and not is_header(line_stripped):
            data = line_stripped.split("|")
            if len(data) == 7 and data[0] == id_cari:
                found = True
                mitra_info = data
                break

    if not found:
        print(f"❌ Mitra dengan ID '{id_cari}' tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    # Tampilkan info mitra
    print(f"""
╔══════════════════════════════════╗
║     INFORMASI MITRA              ║
╚══════════════════════════════════╝
ID       : {mitra_info[0]}
Nama     : {mitra_info[1]}
Jenis    : {mitra_info[2]}
Alamat   : {mitra_info[3]}
Telepon  : {mitra_info[4]}
Email    : {mitra_info[5]}
Status   : {mitra_info[6]}
""")

    # Cek status mitra
    if mitra_info[6] == "Nonaktif":
        print("⚠️  Mitra ini sudah nonaktif sebelumnya!")
        input("\nTekan Enter untuk melanjutkan...")
        return

    # Konfirmasi
    print("Apakah Anda yakin ingin menonaktifkan mitra ini?")
    konfirmasi = input("Ketik 'ya' untuk konfirmasi: ").strip().lower()

    if konfirmasi != 'ya':
        print("⚠️  Penonaktifan dibatalkan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    # Update status mitra menjadi "Nonaktif"
    with open(DB_PATH, "w") as file:
        for line in lines:
            line_stripped = line.strip()

            if is_header(line_stripped):
                file.write(line)
                continue

            if line_stripped and '|' in line_stripped:
                data = line_stripped.split("|")
                if len(data) == 7 and data[0] == id_cari:
                    data[6] = "Nonaktif"
                    line = "|".join(data) + "\n"

            file.write(line)

    print("✅ Mitra berhasil dinonaktifkan!")
    input("\nTekan Enter untuk melanjutkan...")

def hapus_mitra():
    print("\n=== HAPUS MITRA ===")
    id_cari = input("Masukkan ID Mitra yang ingin dihapus: ").strip()

    try:
        with open(DB_PATH, "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        print("❌ File data tidak ditemukan")
        input("\nTekan Enter untuk melanjutkan...")
        return

    found = False
    with open("../database/dataMitra.txt", "w") as file:
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
        print("✅ Mitra berhasil dihapus!")
    else:
        print(f"❌ Mitra dengan ID '{id_cari}' tidak ditemukan")
    
    input("\nTekan Enter untuk melanjutkan...")

def bersihkan_data():
    print("\n=== BERSIHKAN DATA RUSAK ===")
    try:
        with open("../database/dataMitra.txt", "r") as file:
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
                    # Validasi status
                    if data[6] in ["Aktif", "Nonaktif"]:
                        data_valid.append(line)
                    else:
                        data_rusak += 1
                else:
                    data_rusak += 1
        
        # Tulis ulang tanpa header
        with open("../database/dataMitra.txt", "w") as file:
            file.writelines(data_valid)
        
        print(f"✅ Pembersihan selesai!")
        if has_header:
            print(f"   Header dihapus: 1")
        print(f"   Data valid: {len(data_valid)}")
        print(f"   Data rusak dihapus: {data_rusak}")
        
    except FileNotFoundError:
        print("❌ File data tidak ditemukan")
    
    input("\nTekan Enter untuk melanjutkan...")

def main():
    """Fungsi utama untuk menjalankan aplikasi manajemen mitra"""
    while True:
        clear_screen()
        print("""
╔══════════════════════════════════╗
║  APLIKASI MANAJEMEN MITRA        ║
╚══════════════════════════════════╝

1. 📝 Tambah Mitra
2. 📋 Lihat Mitra
3. ✏️  Update Mitra
4. 🔒 Nonaktifkan Mitra
5. 🗑️  Hapus Mitra
6. 🧹 Bersihkan Data Rusak
7. 🚪 Keluar
""")

        pilih = input("Pilih menu (1-7): ").strip()

        if pilih == "1":
            tambah_mitra()
        elif pilih == "2":
            lihat_mitra()
        elif pilih == "3":
            update_mitra()
        elif pilih == "4":
            nonaktifkan_mitra()
        elif pilih == "5":
            hapus_mitra()
        elif pilih == "6":
            bersihkan_data()
        elif pilih == "7":
            print("\n✨ Terima kasih telah menggunakan aplikasi!")
            break
        else:
            print("❌ Pilihan tidak valid! Pilih angka 1-7")
            input("\nTekan Enter untuk melanjutkan...")

# Program Utama - hanya jalan jika file ini dijalankan langsung
if __name__ == "__main__":
    main()