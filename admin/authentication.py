# import menu as adminMenu
import os
import customer.menuCustomer as customerMenu
import penginapan.menuPemilikPenginapan as penginapanMenu
import kendaraan.menuPemilikKendaraan as kendaraanMenu

file = os.path.exists("database/userData.txt")
FILE_CUSTOMER = "database/dataCustomer.txt"

user = []
customer = []
selected_user_id = ""
def loadData():
    user.clear()
    customer.clear()
    if file:
        with open("database/userData.txt", "r") as f:
            lines = f.readlines()
        
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) == 4:
                    user.append({
                        'userId': bagian[0],
                        'email': bagian[1],
                        'password': bagian[2],
                        'role': bagian[3]
                    })
                else:
                    print("Format data user tidak valid:", line)
                    continue
    else:
        print("Tidak ditemukan file untuk menyimpan data")
    
    if os.path.exists(FILE_CUSTOMER):
        with open(FILE_CUSTOMER, "r") as f:
            lines = f.readlines()
        for line in lines:
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
                print("Format data user tidak valid: ", line)
                continue



def authentication(email, password):
    global selected_user_id
    if len(user) == 0:
        print("Belum ada user terdaftar. Silakan registrasi terlebih dahulu.")
        return False
    else:
        for i in user:
            if i['email'] == email :
                if i['password'] == password:
                    print("Login berhasil!")
                    selected_user_id = i['userId']
                    if i['role'] == 'customer':
                        # print("Selamat datang, Customer", i['username'])
                        customerMenu.menu_user(selected_user_id)
                    elif i['role'] == 'penginapan':
                        # print("Selamat datang, Pemilik Penginapan", i['username'])
                        penginapanMenu.menu_pemilik_penginapan(selected_user_id)
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
    looping = True
    while looping:
        email = input("Masukkan email: ")
        password = input("Masukkan password: ")
        if authentication(email, password):
            looping = False

def register():
    user_id = str(len(user) + 1).zfill(1)
    password = input("Masukkan password baru: ")
    email = input("Masukkan email baru: ")
    user.append({'userId': user_id, 'email': email, 'password': password, 'role': 'customer'})
    with open("database/userData.txt", "a") as f:
        f.write(f"{user_id}|{email}|{password}|customer\n")
    print("Registrasi berhasil!")

    # Registrasi Customer
    print("=== ISI BIODATA ANDA ====")
    idCustomer = str(len(customer) + 1).zfill(1)
    nama = input("Masukkan nama anda: ")
    alamat = input("Masukkan alamat anda: ")
    noTelepon = input("Masukkan nomor telepon anda: ")
    customer.append({"idCustomer": idCustomer, "idUser": user_id, "nama": nama, "alamat": alamat, "noTelepon": noTelepon})
    with open(FILE_CUSTOMER, "a") as f:
        f.write(f"{idCustomer}|{user_id}|{nama}|{alamat}|{noTelepon}\n")
    print("ISI BIODATA SELESAI!")


def all_register():
    user_id = str(len(user) + 1).zfill(1)
    password = input("Masukkan password baru: ")
    email = input("Masukkan email baru: ")
    print("Pilih Role:")
    print("1.Pemilik Penginapan")
    print("2. Pemilik rental kendaraan")
    print("3. Pemilik tiket hiburan")
    print("4. Customer")
    role_choice = input("Masukkan pilihan (1-4): ")

    if(role_choice == '1'):
        role = 'penginapan'
        user.append({'userId': user_id, 'email': email, 'password': password, 'role': role})
        with open("database/userData.txt", "a") as f:
            f.write(f"{user_id}|{email}|{password}|{role}\n")
        print("Registrasi berhasil!")
    elif(role_choice == '2'):
        role = 'kendaraan'
        user.append({'userId': user_id, 'email': email, 'password': password, 'role': role})
        with open("database/userData.txt", "a") as f:
            f.write(f"{user_id}|{email}|{password}|{role}\n")
        print("Registrasi berhasil!")
    elif(role_choice == '3'):
        role = 'hiburan'
        user.append({'userId': user_id, 'email': email, 'password': password, 'role': role})
        with open("database/userData.txt", "a") as f:
            f.write(f"{user_id}|{email}|{password}|{role}\n")
        print("Registrasi berhasil!")
    elif(role_choice == '4'):
        role = 'customer'
        user.append({'userId': user_id, 'email': email, 'password': password, 'role': role})
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

def lupa_password():
    email = input("Masukkan email Anda: ")
    ditemukan = False

    for i in user:
        if i['email'] == email:
            password_baru = input("Masukkan password baru: ")
            i['password'] = password_baru
            ditemukan = True
            break

    if not ditemukan:
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
    "Pilih opsi:\n"
    "1. Login\n"
    "2. Register\n"
    "3. List User\n"
    "4. Search User by Email\n"
    "5. Lupa Password\n"
    "0. Exit\n"
)
        if choice == '1':
            login()
        elif choice == '2':
            all_register()
        elif choice == '3':
            listUser()
        elif choice == '4':
            email = input("Masukkan email yang ingin dicari: ")
            searchUserByEmail(email)
        elif choice == '5':
            lupa_password()
        elif choice == '0':
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    loadData()
    start_authentication()
