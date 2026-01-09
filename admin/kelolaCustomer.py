import os
import sys

# Setup path agar database terbaca
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

FILE_CUSTOMER = "database/dataCustomer.txt"
FILE_USER = "database/userData.txt"

customer_list = []


def load_data():
    global customer_list
    customer_list.clear()

    # 1. BACA EMAIL (Disimpan di dictionary)
    kamus_email = {}

    if os.path.exists(FILE_USER):
        with open(FILE_USER, "r") as f:
            for line in f:
                bagian = line.strip().split("|")
                # Format User: userId|email|password|role
                if len(bagian) >= 2:
                    u_id = bagian[0]
                    u_email = bagian[1]
                    kamus_email[u_id] = u_email

    # 2. BACA DATA CUSTOMER DAN GABUNGKAN
    if os.path.exists(FILE_CUSTOMER):
        with open(FILE_CUSTOMER, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                # Format: idCustomer|idUser|nama|alamat|noTelepon
                if len(bagian) == 5:
                    id_user_cust = bagian[1]

                    # Cari email
                    email_nya = "-"
                    if id_user_cust in kamus_email:
                        email_nya = kamus_email[id_user_cust]

                    customer_list.append({
                        "idCustomer": bagian[0],
                        "idUser": bagian[1],
                        "nama": bagian[2],
                        "alamat": bagian[3],
                        "noTelepon": bagian[4],
                        "email": email_nya  # Email masuk ke list
                    })


def save_data():
    # Simpan hanya data customer
    with open(FILE_CUSTOMER, "w") as f:
        for c in customer_list:
            f.write(
                f"{c['idCustomer']}|{c['idUser']}|{c['nama']}|{c['alamat']}|{c['noTelepon']}\n")


def lihat_customer():
    print("\n=== DATA CUSTOMER (ADMIN) ===")
    if not customer_list:
        print("Belum ada data customer.")
        return

    # Tabel
    print(f"{'No':<4} {'ID':<6} {'Nama':<20} {'Email':<25} {'No Telp':<13} {'Alamat'}")
    print("-" * 90)

    for i, c in enumerate(customer_list):
        print(
            f"{i+1:<4} {c['idCustomer']:<6} {c['nama']:<20} {c['email']:<25} {c['noTelepon']:<13} {c['alamat']}")
    print("-" * 90)


def ubah_customer():
    print("\n=== UBAH DATA CUSTOMER ===")
    lihat_customer()
    if not customer_list:
        return

    try:
        idx = int(input("Pilih nomor (0 batal): ")) - 1
        if idx == -1:
            return
        if 0 <= idx < len(customer_list):
            cust = customer_list[idx]
            print(f"\nUbah data: {cust['nama']} (Enter jika tidak ingin ubah)")
            print("Info: Email tidak bisa diubah di sini (harus lewat menu User).")

            nama = input(f"Nama ({cust['nama']}): ")
            alamat = input(f"Alamat ({cust['alamat']}): ")
            telp = input(f"No Telp ({cust['noTelepon']}): ")

            if nama.strip():
                cust['nama'] = nama
            if alamat.strip():
                cust['alamat'] = alamat
            if telp.strip():
                cust['noTelepon'] = telp

            save_data()
            print("Data berhasil diupdate!")
        else:
            print("Nomor tidak valid.")
    except ValueError:
        print("Input harus angka.")


def hapus_customer():
    print("\n=== HAPUS DATA CUSTOMER ===")
    lihat_customer()
    if not customer_list:
        return

    try:
        idx = int(input("Pilih nomor hapus (0 batal): ")) - 1
        if idx == -1:
            return
        if 0 <= idx < len(customer_list):
            yakin = input(
                f"Hapus {customer_list[idx]['nama']}? (y/n): ").lower()
            if yakin == 'y':
                customer_list.pop(idx)
                save_data()
                print("Data berhasil dihapus.")
        else:
            print("Nomor tidak valid.")
    except ValueError:
        print("Input harus angka.")


def menu_kelola_customer():
    load_data()
    while True:
        print("\n=== KELOLA DATA CUSTOMER ===")
        print("1. Lihat Customer")
        print("2. Ubah Data Customer")
        print("3. Hapus Customer")
        print("0. Kembali")

        pilihan = input("Pilih menu: ")
        if pilihan == "1":
            lihat_customer()
        elif pilihan == "2":
            ubah_customer()
        elif pilihan == "3":
            hapus_customer()
        elif pilihan == "0":
            break
        else:
            print("Pilihan salah.")


if __name__ == "__main__":
    menu_kelola_customer()
