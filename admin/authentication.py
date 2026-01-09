# import menu as adminMenu
import kendaraan.menuPemilikKendaraan as kendaraanMenu
import penginapan.menuPemilikPenginapan as penginapanMenu
import customer.menuCustomer as customerMenu
import os
import sys
import re
import getpass

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

file = os.path.exists("database/userData.txt")
FILE_CUSTOMER = "database/dataCustomer.txt"

user = []
customer = []
selected_user_id = ""


def loadData():
    user.clear()
    customer.clear()

    # ===== LOAD USER =====
    if os.path.exists("database/userData.txt"):
        with open("database/userData.txt", "r") as f:
            for line in f:
                bagian = line.strip().split("|")
                if len(bagian) == 4:
                    user.append({
                        'userId': bagian[0],
                        'email': bagian[1],
                        'password': bagian[2],
                        'role': bagian[3]
                    })
                else:
                    print("Format data user tidak valid:", line.strip())

    else:
        print("Tidak ditemukan file untuk menyimpan data")

    # ===== LOAD CUSTOMER =====
    if os.path.exists(FILE_CUSTOMER):
        with open(FILE_CUSTOMER, "r") as f:
            for line in f:
                bagian = line.strip().split("|")
                if len(bagian) == 5:
                    customer.append({
                        "idCustomer": bagian[0],
                        "idUser": bagian[1],
                        "nama": bagian[2],
                        "alamat": bagian[3],
                        "noTelepon": bagian[4]
                    })
                else:
                    print("Format data vudyomrt tidak valid: ", line.strip())


def authentication(email, password):
    global selected_user_id
    if len(user) == 0:
        print("Belum ada user terdaftar. Silakan registrasi terlebih dahulu.")
        return False
    else:
        for i in user:
            if i['email'] == email:
                if i['password'] == password:
                    print("Login berhasil!")
                    selected_user_id = i['userId']
                    if i['role'] == 'customer':
                        # print("Selamat datang, Customer", i['username'])
                        customerMenu.menu_user(selected_user_id)
                    elif i['role'] == 'penginapan':
                        # print("Selamat datang, Pemilik Penginapan", i['username'])
                        penginapanMenu.menu_pemilik_penginapan(
                            selected_user_id)
                    elif i['role'] == 'kendaraan':
                        # print("Selamat datang, Pemilik Rental Kendaraan", i['username'])
                        kendaraanMenu.menu_pemilik_kendaraan(selected_user_id)
                    elif i['role'] == 'hiburan':
                        print("Selamat datang, Pemilik Tiket Hiburan")
                    return True

                else:
                    print("Password salah!")
                    return False
        print("email tidak ditemukan!")
        return False


def login():
    if len(user) == 0:
        print("Belum ada user. Silakan register dulu.")
        return

    while True:
        email = input("Masukkan email: ")
        password = input_password()

        if authentication(email, password):
            break
        else:
            print("Email atau password salah.")


def register():
    user_id = str(len(user) + 1).zfill(1)
    email = input("Masukkan email baru: ")
    password = input_password()
    confirm = input_password()

    if password != confirm:
        print("Password tidak sama!")
        return

    user.append({'userId': user_id, 'email': email,
                'password': password, 'role': 'customer'})
    with open("database/userData.txt", "a") as f:
        f.write(f"{user_id}|{email}|{password}|customer\n")
    print("Registrasi berhasil!")

    # Registrasi Customer
    print("=== ISI BIODATA ANDA ====")
    idCustomer = str(len(customer) + 1).zfill(1)
    nama = input("Masukkan nama anda: ")
    alamat = input("Masukkan alamat anda: ")
    noTelepon = input("Masukkan nomor telepon anda: ")
    customer.append({"idCustomer": idCustomer, "idUser": user_id,
                    "nama": nama, "alamat": alamat, "noTelepon": noTelepon})
    with open(FILE_CUSTOMER, "a") as f:
        f.write(f"{idCustomer}|{user_id}|{nama}|{alamat}|{noTelepon}\n")
    print("ISI BIODATA SELESAI!")


def all_register():
    user_id = str(len(user) + 1)

    email = input("Masukkan email baru: ").strip()
    if email == "":
        print("Email tidak boleh kosong!")
        return
    if is_email_exists(email):
        print("Email sudah terdaftar. Silakan gunakan email lain.")
        return
    if not is_email_valid(email):
        print("Format email tidak valid! Contoh: nama@email.com")
        return

    password = input("Masukkan password baru: ").strip()
    if password == "":
        print("Password tidak boleh kosong!")
        return

    print("\nPilih Role:")
    print("1. Pemilik Penginapan")
    print("2. Pemilik Rental Kendaraan")
    print("3. Pemilik Tiket Hiburan")
    print("4. Customer")

    role_choice = input("Masukkan pilihan (1-4): ").strip()

    if role_choice == '1':
        role = 'penginapan'
    elif role_choice == '2':
        role = 'kendaraan'
    elif role_choice == '3':
        role = 'hiburan'
    elif role_choice == '4':
        role = 'customer'
    else:
        print("Pilihan role tidak valid!")
        return

    user.append({
        'userId': user_id,
        'email': email,
        'password': password,
        'role': role
    })

    with open("database/userData.txt", "a") as f:
        f.write(f"{user_id}|{email}|{password}|{role}\n")

    print("Registrasi berhasil!")


def listUser():
    with open("database/userData.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            print(line.strip())


def searchUserByEmail(email):
    for i in user:
        if i['email'] == email:
            print("User ditemukan:")
            print(i)
            return i
    print("User dengan email tersebut tidak ditemukan.")
    return None


def is_email_exists(email):
    for u in user:
        if u['email'] == email:
            return True
    return False


def is_email_valid(email):
    pola = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pola, email)


def input_password():
    while True:
        print("Tampilkan password?")
        print("1. Tidak (disembunyikan)")
        print("2. Ya (ditampilkan)")
        pilihan = input("Pilih (1/2): ")

        if pilihan == "1":
            password = getpass.getpass("Masukkan password: ")
            return password
        elif pilihan == "2":
            password = input("Masukkan password: ")
            return password
        else:
            print("Pilihan tidak valid.\n")

    while not password:
        print("Password tidak boleh kosong!")
        password = input_password()


def forget_password():
    email = input("Masukkan email Anda: ")
    found = False

    for i in user:
        if i['email'] == email:
            password_baru = input("Masukkan password baru: ")
            i['password'] = password_baru
            found = True
            break

    if not found:
        print("Email tidak ditemukan!")
        return

    # Update file userData.txt
    with open("database/userData.txt", "w") as f:
        for i in user:
            f.write(f"{i['userId']}|{i['email']}|{i['password']}|{i['role']}\n")

    print("Password berhasil diubah! Silakan login kembali.")


def start_authentication():
    while True:
        choice = input(
            "\nPilih opsi:\n"
            "1. Login\n"
            "2. Register\n"
            "3. List User\n"
            "4. Search User by Email\n"
            "5. Forget Password\n"
            "0. Exit\n"
            "Pilih: "
        )
        if choice == '1':
            login()
        elif choice == '2':
            all_register()
            loadData()
        elif choice == '3':
            listUser()
        elif choice == '4':
            email = input("Masukkan email yang ingin dicari: ")
            searchUserByEmail(email)
        elif choice == '5':
            forget_password()
            loadData()
        elif choice == '0':
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")


loadData()
if __name__ == "__main__":
    start_authentication()
