# import menu as adminMenu
import os

file = os.path.exists("admin/userData.txt")

user = []
def load_user_data():
    if file:
        with open("admin/userData.txt", "r") as f:
            lines = f.readlines()
        
            for line in lines:
                bagian = line.strip().split("|")
                if len(bagian) == 4:
                    user.append({
                        'userId': bagian[0],
                        'username': bagian[1],
                        'email': bagian[2],
                        'password': bagian[3],
                        'role': bagian[4]
                    })
                else:
                    print("Format data user tidak valid:", line)
                    continue
    else:
        print("Tidak ditemukan file untuk menyimpan data")



def authentication(email, password):
    if(len(user) == 0):
        print("Belum ada user terdaftar. Silakan registrasi terlebih dahulu.")
        return False
    else:
        for i in user:
            if i['email'] == email :
                if i['password'] == password:
                    print("Login berhasil!")
                    if i['role'] == 'customer':
                        print("Selamat datang, Customer", i['username'])
                    elif i['role'] == 'penginapan':
                        print("Selamat datang, Pemilik Penginapan", i['username'])
                    elif i['role'] == 'kendaraan':
                        print("Selamat datang, Pemilik Rental Kendaraan", i['username'])
                    elif i['role'] == 'hiburan':    
                        print("Selamat datang, Pemilik Tiket Hiburan", i['username'])
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

def register_customer():
    user_id = str(len(user) + 1).zfill(1)
    username = input("Masukkan username baru: ")
    password = input("Masukkan password baru: ")
    email = input("Masukkan email baru: ")
    user.append({'userId': user_id, 'username': username, 'email': email, 'password': password, 'role': 'customer'})
    with open("admin/userData.txt", "a") as f:
        f.write(f"{user_id}|{username}|{email}|{password}|customer\n")
    print("Registrasi berhasil!")

def register():
    user_id = str(len(user) + 1).zfill(1)
    username = input("Masukkan username baru: ")
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
        user.append({'userId': user_id, 'username': username, 'email': email, 'password': password, 'role': role})
        with open("admin/userData.txt", "a") as f:
            f.write(f"{user_id}|{username}|{email}|{password}|{role}\n")
        print("Registrasi berhasil!")
    elif(role_choice == '2'):
        role = 'kendaraan'
        user.append({'userId': user_id, 'username': username, 'email': email, 'password': password, 'role': role})
        with open("admin/userData.txt", "a") as f:
            f.write(f"{user_id}|{username}|{email}|{password}|{role}\n")
        print("Registrasi berhasil!")
    elif(role_choice == '3'):
        role = 'hiburan'
        user.append({'userId': user_id, 'username': username, 'email': email, 'password': password, 'role': role})
        with open("admin/userData.txt", "a") as f:
            f.write(f"{user_id}|{username}|{email}|{password}|{role}\n")
        print("Registrasi berhasil!")
    elif(role_choice == '4'):
        role = 'customer'
        user.append({'userId': user_id, 'username': username, 'email': email, 'password': password, 'role': role})
        with open("admin/userData.txt", "a") as f:
            f.write(f"{user_id}|{username}|{email}|{password}|{role}\n")
        print("Registrasi berhasil!")

def listUser():
    with open("admin/userData.txt", "r") as f:
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

def start_authentication():
    load_user_data()
    while True:
        choice = input("Pilih opsi: 1. Login 2. Register 3. List User 4. Search User by Email 0. Exit\n")
        if choice == '1':
            login()
        elif choice == '2':
            username = input("Masukkan username baru: ")
            password = input("Masukkan password baru: ")
            register(username, password)
        elif choice == '3':
            listUser()
        elif choice == '4':
            email = input("Masukkan email yang ingin dicari: ")
            searchUserByEmail(email)
        elif choice == '0':
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")


if __name__ == "__main__":
    load_user_data()
    start_authentication()
