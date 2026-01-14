import os

posts = []
comments = []


FILE_COMMENT = "database/comments.txt"
FILE_POST = "database/posts.txt"
file = os.path.exists(FILE_COMMENT) and os.path.exists(FILE_POST)

# 
                    
def load_data():
    posts.clear()
    comments.clear()
    if file:
        with open(FILE_POST, "r") as f:
            for line in f:
                bagian = line.strip().split("|")
                posts.append({
                    'postId': int(bagian[0]),
                    'content': bagian[1],
                    'likes': int(bagian[2]),
                })
        
        with open(FILE_COMMENT, "r") as f:
            lines = f.readlines()
            for line in lines:
                bagian = line.strip().split("|")
                comments.append({
                    'postId': int(bagian[0]),
                    'comment': bagian[1]
                    })
    else:
        print("Tidak ditemukan file untuk menyimpan data")

    
    
def add_post():
    postId = len(posts) + 1
    content = input("Masukkan konten post: ")
    post = {
        'postId': postId,
        'content': content,
        'likes': 0,
        'comments': []
    }
    posts.append(post)
    with open(FILE_POST, "a") as f:
        f.write(f"{postId}|{content}|0\n")
    print("Post berhasil diupload")

def add_comment():
    load_data()

    if len(posts) == 0:
        print("Belum ada post untuk dikomentari.")
        return

    for post in posts:
        print(f"ID: {post['postId']}, Konten: {post['content']}")

    post_id = int(input("Masukkan ID post yang ingin dikomentari: "))
    comment_text = input("Masukkan komentar Anda: ")

    # CEK POST, BUKAN COMMENTS
    post_ada = False
    for post in posts:
        if post['postId'] == post_id:
            post_ada = True
            break

    if not post_ada:
        print("Post dengan ID tersebut tidak ditemukan.")
        return

    # LANGSUNG TAMBAHKAN KOMENTAR
    comments.append({
        'postId': post_id,
        'comment': comment_text
    })

    with open(FILE_COMMENT, "w") as f:
        for c in comments:
            f.write(f"{c['postId']}|{c['comment']}\n")

    print("Komentar berhasil ditambahkan.")

        

def view_posts():
    load_data()
    if len(posts) == 0:
        print("Belum ada post yang diupload.")
        return
    i = 1
    for post in posts:
        print(f"ID: {post['postId']}")
        print(f"konten: {post['content']}")
        print(f"Likes: {post['likes']}")
        print("Komentar:")
        for c in comments:
            if c['postId'] == post['postId']:
                print(f"  {i}. {c['comment']}")
                i += 1
        print("-" * 20)

def like_post():
    if len(posts) == 0:
        print("Belum ada post")
        return
    
    for post in posts:
        print(f"ID: {post['postId']}, Konten: {post['content']}, Likes: {post['likes']}")

    postId = int(input("Masukkan Id post yang ingin di-like: "))

    for post in posts:
        if post['postId'] == postId:
            post['likes'] += 1
            
            with open(FILE_POST, "w") as f:
                for p in posts:
                    f.write(f"{p['postId']}|{p['content']}|{p['likes']}\n")
            
            print("Post telah di-like")
            return
        
    print("Post dengan ID tersebut tidak ditemukan.")

def delete_post():
    if len(posts) == 0:
        print("Belum ada post")
        return
    
    for post in posts:
        print(f"ID: {post['postId']}, Konten: {post['content']}, Likes: {post['likes']}")

    postId = int(input("Masukkan Id post yang ingin dihapus: "))

    for post in posts:
        if post['postId'] == postId:
            posts.remove(post)
            delete_comment_by_admin(postId)
            with open(FILE_POST, "w") as f:
                for p in posts:
                    f.write(f"{p['postId']}|{p['content']}|{p['likes']}\n")
            
            print("Post telah dihapus")
            return
        
    print("Post dengan ID tersebut tidak ditemukan.")

# def delete_comment():
#     if len(posts) == 0:
#         print("Belum ada post")
#         return

#     for post in posts:
#         print(f"ID: {post['postId']}, Konten: {post['content']}, Likes: {post['likes']}")

#     postId = int(input("Masukkan Id post yang ingin dihapus komentarnya: "))

#     for post in posts:
#         if post['postId'] == postId:
#             for i, c in enumerate(comments, start=1):
#                 print(f"{i}. {c}")
            

#     print("Post dengan ID tersebut tidak ditemukan.")

def delete_comment_by_admin(postId):
    for c in comments:
        if c['postId'] == postId:
            if not c['comment']:
                print("Post tidak memiliki komentar.")
                return
            comments.remove(c)
            with open(FILE_COMMENT, "w") as f:
                for c in comments:
                    f.write(f"{c['postId']}|{c['comment']}\n")
            print("Komentar telah dihapus.")
            return

def CommunityMenu():
    load_data()
    print("SELAMAT DATANG DI KOMUNITAS \n")

    while True:
        print("opsi: \n")
        print(" 1.Lihat Postingan \n 2.Tambah Postingan \n 3.Tambah Komentar \n 4.Like Post \n 5.Hapus Post \n 0.Keluar \n")
        choice = input("Pilih opsi: ")
        if choice == '1':
            view_posts()
        elif choice == '2':
            add_post()
        elif choice == '3':
            add_comment()
        elif choice == '4':
            like_post()
        elif choice == '5':
            delete_post()
        elif choice == '0':
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")

def menuCustomer():
    load_data()
    print("SELAMAT DATANG DI KOMUNITAS \n")

    while True:
        print("opsi: \n")
        print(" 1.Lihat Postingan \n 2.Tambah Postingan \n 3.Tambah Komentar \n 4.Like Post \n \n 0.Keluar \n")
        choice = input("Pilih opsi: ")
        if choice == '1':
            view_posts()
        elif choice == '2':
            add_post()
        elif choice == '3':
            add_comment()
        elif choice == '4':
            like_post()
        elif choice == '0':
            break
        else:
            print("Opsi tidak valid. Silakan coba lagi.")
            
if __name__ == "__main__":
    load_data()
    CommunityMenu()
