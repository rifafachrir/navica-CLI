import os

FILE_TIKET = "database/tiket.txt"
FILE_MITRA = "database/dataMitra.txt"

data_tiket = []
mitra_data = []

def load_data():
    data_tiket.clear()
    mitra_data.clear()
    with open(FILE_TIKET, 'r') as f:
        for line in f:
            bagian = line.strip().split("|")
            data_tiket.append({
                "idTiket": bagian[0],
                "mitraId": bagian[1],
                'namaTiket': bagian[2],
                "harga": bagian[3],
                "jenis": bagian[4],
                "asal": bagian[5],
                "tujuan": bagian[6]
            })

    with open(FILE_MITRA, 'r') as f:
        lines = f.readlines()
        for line in lines:
            bagian = line.strip().split("|")
            mitra_data.append({
                "mitraId": bagian[0],
                "userId": bagian[1],
                "namaMitra": bagian[2],
                "alamat": bagian[3],
                "noTelepon": bagian[4]
            })


def generateId():
    jumlah = len(data_tiket) + 1
    return  "T"+str(jumlah).zfill(3)

def input_jenis():
    while True:
        jenis = input("Jenis (Transportasi/Hiburan): ").strip().lower()
        if jenis in ['transportasi', 'hiburan']:
            return jenis.capitalize()
        print("❌ Jenis hanya boleh 'Transportasi' atau 'Hiburan'!")

def create_tiket_with_mitra(mitraId):
    load_data()
    id_tiket = generateId()
    nama_tiket = input("Nama Tiket: ").strip()
    harga = input("Harga: ").strip()
    jenis = input_jenis()
    asal = input("Asal: ").strip()
    tujuan = input("Tujuan: ").strip()

    data_tiket.append({
        "idTiket": id_tiket,
        "mitraId": mitraId,
        "namaTiket": nama_tiket,
        "harga": harga,
        "jenis": jenis,
        "asal": asal,
        "tujuan": tujuan
    })

    with open(FILE_TIKET, 'a') as f:
        f.write(f"{id_tiket}|{mitraId}|{nama_tiket}|{harga}|{jenis}|{asal}|{tujuan}\n")
def list_tiket(mitraId):
    load_data()
    print("\n=== DAFTAR TIKET ===")
    if not data_tiket:
        print("Tidak ada tiket yang tersedia.")

    for t in data_tiket:
        if t["mitraId"] == mitraId:
            print(f"Id  : {t['idTiket']}")
            for m in mitra_data:
                if m['mitraId'] == mitraId:
                    print(f"Nama Mitra: {m['namaMitra']}")
            print(f"Nama Tiket: {t['namaTiket']}")
            print(f"Harga: {t['harga']}")
            print(f"Jenis: {t['jenis']}")
            if t['jenis'] == 'Transportasi':
                print(f"Asal: {t['asal']}")
                print(f"Tujuan: {t['tujuan']}")
            else:
                print(f"Daerah Hiburan: {t['asal']}")
            print("-" * 30)
    input("Tekan Enter untuk melanjutkan")

def update_tiket(mitraId):
    load_data()
    print("\n === UPDATE DATA TIKET ===")

    list_tiket(mitraId)

    tiketId = input("Masukan Tiket Id: ")
    print("\n Kosongkan jika tidak ingin diubah")

    for t in data_tiket:
        if t['idTiket'] == tiketId:
            namaTiket = input(f"Masukan Nama Baru Tiket ({t['namaTiket']}): ").strip() or t['namaTiket']
            harga = input(f"Masukan Harga Baru ({t['harga']}): ").strip() or t['harga']
            jenis = input(f"Masukan Jenis Baru ({t['jenis']}): ").strip().lower() or t['jenis']
            t['jenis'] = jenis
            if t['jenis'] == 'transportasi':
                asal = input(f"Masukan Asal Baru ({t['asal']}): ").strip() or t['asal']
                tujuan = input(f"Masukan Tujuan Baru ({t['tujuan']}): ").strip() or t['tujuan']
            else:
                print(f"jenis tiket yang terdaftar adalah: {t['jenis']}")
                asal = input(f"Masukan Daerah Hiburan ({t['asal']}): ").strip() or t['asal']
                tujuan = "-"

            t['namaTiket'] = namaTiket
            t['harga'] = harga
            t['jenis'] = jenis
            t['asal'] = asal
            t['tujuan'] = tujuan
            break

    with open(FILE_TIKET, 'w') as f:
        for t in data_tiket:
            f.write(f"{t['idTiket']}|{t['mitraId']}|{t['namaTiket']}|{t['harga']}|{t['jenis']}|{t['asal']}|{t['tujuan']}\n")

def delete_tiket(mitraId):
    load_data()
    print("\n === HAPUS DATA TIKET ===")

    list_tiket(mitraId)

    tiketId = input("Masukan Data Id: ")

    for t in data_tiket:
        if t['idTiket'] == tiketId:
            data_tiket.remove(t)

    with open(FILE_TIKET, 'w') as f:
        for t in data_tiket:
            f.write(f"{t['idTiket']}|{t['mitraId']}|{t['namaTiket']}|{t['harga']}|{t['jenis']}|{t['asal']}|{t['tujuan']}\n")
