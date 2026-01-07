import os

posts = []

FILE_COMMENT = "database/comments.txt"
FILE_POST = "database/posts.txt"
file = os.path.exists(FILE_COMMENT) and os.path.exists(FILE_POST)

def load_comments(postId):
    comments = []
    if file: 
        with open(FILE_COMMENT, "r") as f:
            for line in f:
                bagian = line.strip().split("|")
                if int(bagian[0]) == postId:
                    comments.append(bagian[1])
    return comments
                    
def load_data():
    if file:
        with open(FILE_POST, "r") as f:
            for line in f:
                bagian = line.strip().split("|")
                posts.append({
                    'postId': int(bagian[0]),
                    'content': bagian[1],
                    'likes': int(bagian[2]),
                    'comments': load_comments(int(bagian[0]))
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
    if len(posts) == 0:
        print("Belum ada post untuk dikomentari.")
        return
    
    for post in posts:
        print(f"ID: {post['postId']}, Konten: {post['content']}")
        
    post_id = int(input("Masukkan ID post yang ingin dikomentari: "))
    
    for post in posts:
        if post['postId'] == post_id:
            comment = input("Masukkan komentar Anda: ")
            post['comments'].append(comment)
            with open(FILE_COMMENT, "a") as f:
                f.write(f"{post_id}|{comment}\n")
            print("Komentar berhasil ditambahkan.")
            return
        
    print("Post dengan ID tersebut tidak ditemukan.")

def view_posts():
    if len(posts) == 0:
        print("Belum ada post yang diupload.")
        return
    
    for post in posts:
        print(f"ID: {post['postId']}, Konten: {post['content']}, Likes: {post['likes']}, Jumlah Komentar: {len(post['comments'])} \n ")
            # Show comments for the post (supports plain strings or dicts)
        if post['comments']:
            print("  - Komentar:")
            for i, c in enumerate(post['comments'], start=1):
                print(f"    {i}. {c} \n")
        else:
            print("  - Belum ada komentar. \n")
        print()

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

def CommunityMenu():
    print("SELAMAT DATANG DI KOMUNITAS \n")

    while True:
        print("opsi: \n")
        print(" 1.Lihat Postingan \n 2.Tambah Postingan \n 3.Tambah Komentar \n 4.Like Post \n 0.Keluar \n")
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
