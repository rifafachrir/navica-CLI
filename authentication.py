user = []


def authentication (username, password):
    if(len(user) == 0):
        print("Belum ada user terdaftar. Silakan registrasi terlebih dahulu.")
        return False
    else:
        for i in user:
            if i['username'] == username :
                if i['password'] == password:
                    print("Login berhasil!")
                    i['status'] = True
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
            return True

def register(username, password):
    user.append({'username': username, 'password': password, 'status': False})
    print("Registrasi berhasil!")

def list():
    for i in user:
        print(i)

def logout():
    print("Logout berhasil!")
    for i in user:
        if i['status'] == True:
            i['status'] = False
    return False


def start_authentication():
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
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

start_authentication()