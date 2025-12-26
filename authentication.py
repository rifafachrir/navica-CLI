import menu as adminMenu

user = [
    {'username': 'admin', 'password': 'admin123', 'isLogin': False, 'role': 'admin'},
]


def authentication (username, password):
    if(len(user) == 0):
        print("Belum ada user terdaftar. Silakan registrasi terlebih dahulu.")
        return False
    else:
        for i in user:
            if i['username'] == username :
                if i['password'] == password:
                    print("Login berhasil!")
                    i['isLogin'] = True
                    return True
                else:
                    print("Password salah!")
                    return False
            else:
                print("Username tidak ditemukan!")
                return False



def login():
    looping = True
    while looping:
        username = input("Masukkan username: ")
        password = input("Masukkan password: ")
        if authentication(username, password):
            looping = False
            if( user['role'] == "admin"):
                adminMenu.mainMenu()
            elif( user['role'] == "user"):
                print("Goes to User Menu")
            elif( user['role'] == "pemilik_kendaraan"):
                print("Goes to menu Pemilik kendaraan")
            elif( user['role'] == "pemilik_penginapan"):
                print("Goes to menu pemilik Penginapan")
            

def register(username, password):
    user.append({'username': username, 'password': password, 'isLogin': False, 'role': 'user'})
    print("Registrasi berhasil!")

def admin_register():
    username = input("Masukkan username admin baru: ")
    password = input("Masukkan password admin baru: ")
    print("Pilih")
    print("1. Admin")
    print("2. User")
    print("3.Pemilik Kendaraan")
    print("4.Pemilik Penginapan")
    role = input("Masukkan role: ")
    if role == '1':
        user.append({'username': username, 'password': password, 'isLogin': False, 'role': 'admin'})
        print("Registrasi berhasil!")
    elif role == '2':
        user.append({'username': username, 'password': password, 'isLogin': False, 'role': 'user'})
        print("Registrasi berhasil!")
    elif role == '3':
        user.append({'username': username, 'password': password, 'isLogin': False, 'role': 'pemilik_kendaraan'})
        print("Registrasi berhasil!")
    elif role == '4':
        user.append({'username': username, 'password': password, 'isLogin': False, 'role': 'pemilik_penginapan'})
        print("Registrasi berhasil!")
    else:
        print("Role tidak valid! Default ke admin.")

def list():
    for i in user:
        print(i)

def logout():
    if user == []:
        print("Kembali ke menu utama.")
    for i in user:
        if i['isLogin'] == True:
            i['isLogin'] = False
            print("Logout Berhasil")
            print("Kembali ke menu Utama.")
        else:
            print("Kembali ke menu utama.")


def authentication_menu():
    while True:
        choice = input("Pilih opsi: 1. Login 2. Register 3. List  0. Logout\n")
        if choice == '1':
            login()
        elif choice == '2':
            username = input("Masukkan username baru: ")
            password = input("Masukkan password baru: ")
            register(username, password)
        elif choice == '3':
            list()
        elif choice == '0':
           logout()
           break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

if __name__ == "__main__":
    authentication_menu()
