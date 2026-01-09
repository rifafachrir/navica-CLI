import os

FILE_TIKET = "database/tiket.txt"
FILE_MITRA = "database/dataMitra.txt"

data_tiket = []
mitra_data = []

def load_data():
    with open(FILE_TIKET, 'r') as f:
        for line in f:
            bagian = line.strip().split("|")
            if len(bagian) == 7:
                data_tiket.append({
                    "idTiket": bagian[0],
                    "mitraId": bagian[1],
                    'namaTiket': bagian[2],
                    "harga": bagian[3],
                    "jenis": bagian[4],
                    "asal": bagian[5],
                    "tujuan": bagian[6]
                })
            else:
                print("Format data tiket tidak valid:", line.strip())
    with open(FILE_MITRA, 'r') as f:
        lines = f.readlines()
        for line in lines:
            bagian = line.strip().split("|")
            if len(bagian) == 5:
                mitra_data.append({
                    "mitraId": bagian[0],
                    "userId": bagian[1],
                    "namaMitra": bagian[2],
                    "alamat": bagian[3],
                    "noTelepon": bagian[4]
                })
            else:
                print("Format data mitra tidak valid:", line.strip())


def generateId():
    jumlah = len(data_tiket) + 1
    return  "T"+str(jumlah).zfill(3)

def input_jenis():
    while True:
        jenis = input("Jenis (Transportasi/Hiburan): ").strip().lower()
        if jenis in ['transportasi', 'hiburan']:
            return jenis.capitalize()
        print("❌ Jenis hanya boleh 'Transportasi' atau 'Hiburan'!")

def create_tiket(mitraId):
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
            print(f"Asal: {t['asal']}")
            print(f"Tujuan: {t['tujuan']}")
            print("-" * 30)

def update_tiket(mitraId):
    print("\n === UPDATE DATA TIKET ===")

    list_tiket(mitraId)

    tiketId = input("Masukan Data Id")

    for t in data_tiket:
        if t['idTiket'] == tiketId:
            t['namaTiket'] = input("Nama Tiket: ").strip()
            t['harga'] = input("Harga: ").strip()
            t['jenis'] = input("Jenis: ").strip()
            t['asal'] = input("Asal: ").strip()
            t['tujuan'] = input("Tujuan: ").strip()

    with open(FILE_TIKET, 'w') as f:
        for t in data_tiket:
            f.write(f"{t['idTiket']}|{t['mitraId']}|{t['namaTiket']}|{t['harga']}|{t['jenis']}|{t['asal']}|{t['tujuan']}\n")

def delete_tiket(mitraId):
    print("\n === HAPUS DATA TIKET ===")

    list_tiket(mitraId)

    tiketId = input("Masukan Data Id")

    for t in data_tiket:
        if t['idTiket'] == tiketId:
            data_tiket.remove(t)

    with open(FILE_TIKET, 'w') as f:
        for t in data_tiket:
            f.write(f"{t['idTiket']}|{t['mitraId']}|{t['namaTiket']}|{t['harga']}|{t['jenis']}|{t['asal']}|{t['tujuan']}\n")
