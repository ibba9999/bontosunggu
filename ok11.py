import requests
import json
import random
import string
import time
import os
from difflib import SequenceMatcher

# Menghasilkan User-Agent acak
def generate_user_agent():
    android_version = "Android " + str(random.randint(10, 13)) + "." + str(random.randint(0, 3))
    build_info = "Build/" + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"Dalvik/2.1.0 (Linux; U; {android_version}; {build_info})"

# Menghasilkan deviceId acak
def generate_device_id():
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

# Meminta pengguna memasukkan alamat email
email = input("Masukkan alamat email Anda: ")

# Mengirim permintaan untuk mendapatkan kode
send_code_url = "https://app.api.30sec.net/v1/common/sms/SendCode"

user_agent = generate_user_agent()
device_id = generate_device_id()

send_code_headers = {
    "Authorization": "Bearer",
    "User-Agent": user_agent,
    "s": "NdHXn2jopvZKM95JCyyjvg==",
    "version": "2.1.1",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": "160",
    "Host": "app.api.30sec.net",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

send_code_payload = {
    "couponExpiredPush": False,
    "couponId": 0,
    "email": email,
    "focusBrandPush": False,
    "originPlatform": "1",
    "osType": "Android",
    "phoneNum": "",
    "type": 1001
}

# Mengirim permintaan POST untuk mendapatkan kode
send_code_response = requests.post(send_code_url, headers=send_code_headers, json=send_code_payload)
send_code_response_data = send_code_response.json()

print(send_code_response_data['code']) # Output: 200
print(send_code_response_data['tips']) # Output: Verifikasi kode telah berhasil dikirim

# Melanjutkan proses registrasi dengan input kode yang dimasukkan oleh pengguna
code = input("Masukkan kode yang telah dikirim: ")

# Meminta pengguna memasukkan deviceId
device_id = device_id

# Melakukan proses registrasi
register_url = "https://app.api.30sec.net/v1/user/login"

register_payload = {
    "channel": 101,
    "code": code,
    "couponExpiredPush": False,
    "couponId": 0,
    "deviceId": device_id,
    "email": email,
    "fcmToken": "",
    "focusBrandPush": False,
    "originPlatform": "1",
    "osType": "Android",
    "phoneNum": "",
    "type": 201,
    "version": "2.1.1"
}

register_headers = {
    "Authorization": "Bearer",
    "User-Agent": user_agent,
    "s": "",
    "version": "2.1.1",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": str(len(json.dumps(register_payload))),
    "Host": "app.api.30sec.net",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

# Mengirim permintaan POST untuk proses registrasi
register_response = requests.post(register_url, headers=register_headers, json=register_payload)
register_response_data = register_response.json()

print(register_response_data['code']) # Output: 200
print(register_response_data['data']['token']) # Output: Token yang diberikan dalam response

# Mengisi kunci
url = "https://app.api.30sec.net/v1/finance/wallet"
bearer_token = "Bearer "  # Ganti dengan format yang sesuai untuk otentikasi, misalnya "Bearer "
token = register_response_data['data']['token']  # Mengambil token dari respons registrasi

headers = {
    "Authorization": bearer_token + token,
    "User-Agent": user_agent,
    "version": "2.1.1",
    "Content-Type": "application/json; charset=UTF-8",
    "Accept-Encoding": "gzip"
}

address = input("Masukkan alamat Anda: ")
data = {
    "address": address,
    "key": ""
}

response = requests.post(url, headers=headers, data=json.dumps(data))

print(response.json())

#aktivate code
url = 'https://app.api.30sec.net/v1/user/UserInfo/10557/activate'
headers = {
    "Authorization": bearer_token + token,
    "User-Agent": user_agent,
    "s": '',
    'version': '2.1.1',
    'Content-Type': 'application/json; charset=UTF-8',
    'Content-Length': '19',
    'Host': 'app.api.30sec.net',
    'Connection': 'Keep-Alive',
    'Accept-Encoding': 'gzip'
}

code = input("Masukkan kode aktivasi: ")

data = {
    "code": code
}

response = requests.put(url, headers=headers, json=data)

print(response.json())

# Mengambil ID dari video.txt untuk mencari data video
def get_video_id():
    # Mengambil ID dari video.txt untuk mencari data video
    with open("video.txt", "r") as file:
        lines = file.readlines()
    last_line = lines[-1].strip()
    url = "https://app.api.30sec.net/v1/content/Advert/" + last_line

    # Menghapus baris terakhir dalam file video.txt
    with open("video.txt", "w") as file:
        file.writelines(lines[:-1])

    # Headers
    bearer_token = "your_bearer_token"
    token = "your_token"
    user_agent = "your_user_agent"
    headers = {
        "Authorization": bearer_token + token,
        "User-Agent": user_agent,
        "s": "",
        "version": "2.1.1",
        "Host": "app.api.30sec.net",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip"
    }

    # Mengirim permintaan GET ke URL API
    response = requests.get(url, headers=headers)
    data = response.json()

    # Menyimpan data yang diperlukan dalam variabel
    video_id = None
    content_video_url = None
    duration = None
    name = None
    english_name = None
    question_id = None
    question_content = None
    answer_list = []

    if "data" in data and isinstance(data["data"], dict):
        video_data = data["data"]
        video_id = video_data.get("id")
        content_video_url = video_data.get("contentVideoUrl")
        duration = video_data.get("duration")
        name = video_data.get("name")
        english_name = video_data.get("brand", {}).get("englishName")
        question_data = video_data.get("question", {})
        question_id = question_data.get("id")
        question_content = question_data.get("content")
        answer_list = question_data.get("answerList", [])

    # Menampilkan informasi yang diperoleh
    if video_id:
        print("id:", video_id)
    if content_video_url:
        print("Video URL:", content_video_url)
    if duration:
        print("Duration:", duration, "seconds")
    if name:
        print("NamaVideo:", name)
    if english_name:
        print("NamaEnglish:", english_name)
    if question_id:
        print("Question ID:", question_id)
    if question_content:
        print("Question Content:", question_content)
    print("Answer List:")
    for answer in answer_list:
        answer_id = answer.get("id")
        answer_text = answer.get("answer")
        if answer_id and answer_text:
            print("Answer ID {}: Answer Text: {}".format(answer_id, answer_text))

    # Mencari kata yang sama
    similar_answers = []

    for answer in answer_list:
        answer_id = answer.get("id")
        answer_text = answer.get("answer")
        if name and english_name and answer_text:
            if name.lower() in answer_text.lower() or english_name.lower() in answer_text.lower():
                # Split answer text into words
                words = answer_text.split()
                # Check if only one word is the same
                same_word_count = 0
                for word in words:
                    if word.lower() == name.lower() or word.lower() == english_name.lower():
                        same_word_count += 1
                if same_word_count == 1:
                    question_id = answer.get("question", {}).get("id")  # Mengambil question_id jika ada
                    if question_id:
                        similar_answers.append("{} {} {}".format(answer_text, question_id, content_video_url))

    # Menulis hasil ke file answer.txt
    with open("answer.txt", "w") as file:
        for answer_text in similar_answers:
            file.write(answer_text + "\n")

    # Mengulangi proses pencarian jika list "answer.txt" kosong atau None
    def cek_isi_file_answer_txt():
        # Membaca isi file "answer.txt"
        with open("answer.txt", "r") as file:
            lines = file.readlines()

        if not lines:
            print("List 'answer.txt' kosong atau None!")
            return None

        answer_text = None

        # Lakukan semua proses pencarian dan pengecekan yang diperlukan untuk answer_text
        # ...

        # Jika answer_text ditemukan, tulis ke file "answer.txt" dan keluar dari fungsi
        if answer_text is not None:
            with open("answer.txt", "w") as file:
                file.write(answer_text)

    while True:
        hasil_cek = cek_isi_file_answer_txt()
        if hasil_cek is None:
            break

get_video_id()


# Memulai Nonton Video
url = "https://app.api.30sec.net/v1/user/UserOperation"
headers = {
    "Authorization": bearer_token + token,
    "User-Agent": user_agent,
    "s": "",
    "version": "2.1.1",
    "Content-Type": "application/json; charset=UTF-8",
    "Host": "app.api.30sec.net",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

payload = {
    "couponExpiredPush": False,
    "couponId": 0,
    "email": "",
    "focusBrandPush": False,
    "originPlatform": "1",
    "osType": "Android",
    "phoneNum": "",
    "targetId": "",
    "type": '202'
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    result = response.json()
    print(result["message"])
else:
    print("Gagal memulai misi menonton.")

# Nonton Video
    with open("video.txt", "r") as file:
        lines = file.readlines()
    last_line = lines[-1].strip()
    url = "https://app.api.30sec.net/v1/content/Advert/" + last_line

    # ...

    file_name = "video.mp4"

    response = requests.get(url, stream=True)

    with open(file_name, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

    if duration:
        os.system(f"mpv {file_name} --end={duration + 20}")

    # Kode lainnya...

while True:
    hasil_cek = cek_isi_file_answer_txt()
    if hasil_cek is None:
        break
    return def get_video_id

# Lanjutan program setelah menonton video
print("Video selesai!")

# Menutup Misi
url = 'https://app.api.30sec.net/v1/user/UserOperation'
headers = {
    "Authorization": bearer_token + token,
    "User-Agent": user_agent,
    "s": "s",
    'version': '2.1.1',
    'Content-Type': 'application/json; charset=UTF-8',
    'Accept-Encoding': 'gzip'
}

payload = {
    'couponExpiredPush': False,
    'couponId': 0,
    'email': '',
    'focusBrandPush': False,
    'originPlatform': '1',
    'osType': 'Android',
    'phoneNum': '',
    "targetId": "",
    'type': '203'
}

response = requests.post(url, headers=headers, json=payload)

if response.status_code == 200:
    print("Misi menonton ditutup berhasil.")
else:
    print("Terjadi kesalahan dalam menutup misi menonton.")

time.sleep(5)

# Menjawab Pertanyaan dengan Membaca isi file answer.txt
with open("answer.txt", "r") as file:
    lines = file.readlines()

# Mengambil kata kedua pada line terakhir sebagai questionId
last_line = lines[-1].strip().split()
questionId = last_line[1]

# Mengambil kata pertama pada line terakhir sebagai jawaban
answer = last_line[0]

# Mengambil ID dari video.txt untuk mencari data video

# Memasukkan nilai jawaban dan questionId ke dalam payload
payload = {
    "answer": answer,
    "questionId": questionId
}

url = 'https://app.api.30sec.net/v2/user/UserAnswer'

# Menentukan header
headers = {
    "Authorization": bearer_token + token,
    "User-Agent": user_agent,
    "s": "s",
    "version": "2.1.1",
    "Content-Type": "application/json; charset=UTF-8",
    "Content-Length": "37",
    "Host": "app.api.30sec.net",
    "Connection": "Keep-Alive",
    "Accept-Encoding": "gzip"
}

# Mengirim permintaan POST
response = requests.post(url, json=payload, headers=headers)

# Mendapatkan respons
data = response.json()

# Jika respons memiliki value "Video hasn't finished playing",
# maka kembali ke proses "Mengambil ID dari video.txt untuk mencari data video"

if data == "Video hasn't finished playing":
    # Mengambil ID dari video.txt untuk mencari data video
    # ...
    pass
else:
    # Menampilkan respons
    print(data)