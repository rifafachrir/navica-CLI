data_pemilik = []

def input_huruf(teks):
    while True:
        data = input(teks)
        if data.isalpha():
            return data
        else:
            print("Input harus huruf saja!")

def input_angka(teks):
    while True:
        data = input(teks)
        if data.isdigit():
            return data
        else:
            print("Input harus angka saja!")

def input_alnum(teks):
    while True:
        data = input(teks)
        if data.replace(" ", "").isalnum():
            return data
        else:
            print("Input tidak boleh simbol!")

def cek_no_polisi(no_polisi):
    for p in data_pemilik:
        if p["no_kendaraan"] == no_polisi:
            return True
    return False

def tambah_pemilik():
    print("\n=== Tambah Data Pemilik Kendaraan ===")
    nama = input_huruf("Nama Pemilik: ")
    alamat = input("Alamat: ")
    no_hp = input_angka("No. HP: ")

    while True:
        no_kendaraan = input_alnum("Nomor Polisi Kendaraan : ")
        if cek_no_polisi(no_kendaraan):
            print("Nomor polisi sudah terdaftar!")
        else:
            break
    
    merek = input_huruf("Nama/Merek Kendaraan: ")
    jenis = input_huruf("Jenis/Tipe Kendaraan: ")

    pemilik = {
        "nama": nama,
        "alamat": alamat,
        "no_hp": no_hp,
        "no_kendaraan": no_kendaraan,
        "merek": merek,
        "jenis": jenis
    }

    data_pemilik.append(pemilik)
    print("Data pemilik berhasil ditambahkan!\n")

def lihat_pemilik():
    print("\n=== Daftar Data Pemilik Kendaraan ===")
    if len(data_pemilik) == 0:
        print("Belum ada data pemilik.\n")
        return

    for i, p in enumerate(data_pemilik):
        print(f"{i+1}. {p['nama']} | {p['alamat']} | {p['no_hp']} | "
              f"Polisi: {p['no_kendaraan']} | Merek: {p['merek']} | Jenis: {p['jenis']}")
    print()
 
def edit_pemilik():
    lihat_pemilik()
    if len(data_pemilik) == 0:
        return

    index = int(input("Pilih nomor data yang ingin diedit: ")) - 1
    if index < 0 or index >= len(data_pemilik):
        print("Nomor tidak valid!")
        return

    print("\n--- Masukkan data baru (kosongkan jika tidak ingin mengubah) ---")
    nama = input("Nama baru: ")
    alamat = input("Alamat baru: ")
    no_hp = input("No. HP baru: ")
    no_kendaraan = input("Nomor Polisi baru: ")
    merek = input("Nama/Merek Kendaraan baru: ")
    jenis = input("Jenis/Tipe Kendaraan baru: ")

    if nama: data_pemilik[index]["nama"] = nama
    if alamat: data_pemilik[index]["alamat"] = alamat
    if no_hp: data_pemilik[index]["no_hp"] = no_hp
    if no_kendaraan: data_pemilik[index]["no_kendaraan"] = no_kendaraan
    if merek: data_pemilik[index]["merek"] = merek
    if jenis: data_pemilik[index]["jenis"] = jenis

    print("Data pemilik berhasil diperbarui!\n")

def hapus_pemilik():
    lihat_pemilik()
    if len(data_pemilik) == 0:
        return

    index = int(input("Pilih nomor data yang ingin dihapus: ")) - 1
    if index < 0 or index >= len(data_pemilik):
        print("Nomor tidak valid!")
        return

    data_pemilik.pop(index)
    print("Data pemilik berhasil dihapus!\n")

def menu():
    while True:
        print("=== MENU PEMILIK KENDARAAN ===")
        print("1. Tambah Pemilik")
        print("2. Lihat Pemilik")
        print("3. Edit Pemilik")
        print("4. Hapus Pemilik")
        print("5. Keluar")

        pilih = input("Pilih menu: ")

        if pilih == "1": tambah_pemilik()
        elif pilih == "2": lihat_pemilik()
        elif pilih == "3": edit_pemilik()
        elif pilih == "4": hapus_pemilik()
        elif pilih == "5":
            print("Terima kasih!")
            break
        else:
            print("Pilihan tidak valid!\n")

menu()