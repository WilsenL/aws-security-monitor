# AWS Server Security Monitor

Sebuah skrip Python otomatis untuk memantau keamanan dasar server Linux di AWS EC2 dan mengirimkan notifikasi email jika terdeteksi adanya aktivitas login yang mencurigakan.

Proyek ini dibuat sebagai bagian dari sprint pengembangan 2 minggu untuk membangun sistem fungsional dari nol.

## Fitur Utama

- **Koneksi Aman:** Menggunakan Paramiko untuk terhubung ke server melalui SSH dengan autentikasi kunci privat.
- **Analisis Log Otomatis:** Membaca file log otentikasi (`/var/log/auth.log`) secara otomatis.
- **Deteksi Pola Anomali:** Mengidentifikasi beberapa pola login yang mencurigakan, seperti "Failed password", "invalid user", dan "Failed publickey".
- **Sistem Peringatan Real-time:** Mengirimkan notifikasi darurat melalui email menggunakan SMTP jika anomali terdeteksi.
- **Konfigurasi Aman:** Menggunakan environment variables untuk menyimpan kredensial sensitif (kunci AWS & email), bukan menuliskannya di dalam kode.

## Teknologi yang Digunakan

- **Cloud:** AWS EC2 (Ubuntu Server 22.04 LTS)
- **Bahasa:** Python 3
- **Library Utama:**
  - `boto3`: Untuk berinteraksi dengan API AWS.
  - `paramiko`: Untuk konektivitas SSH.
  - `smtplib`: Untuk mengirim email.

## Cara Menjalankan

1.  **Clone Repositori:**

    ```bash
    git clone [URL_GITHUB_ANDA]
    cd aws-honeypot-monitor
    ```

2.  **Buat dan Aktifkan Virtual Environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # Untuk Mac/Linux
    # .\venv\Scripts\activate # Untuk Windows
    ```

3.  **Install Dependensi:**

    ```bash
    pip install -r requirements.txt
    ```

4.  **Atur Environment Variables:**

    - Atur kredensial AWS (Access Key, Secret Key, Session Token) dan kredensial Email (Email User, App Password) di terminal Anda.

5.  **Konfigurasi Skrip:**

    - Buka `monitor.py` dan ganti nilai variabel `HOST` dengan alamat IP server Anda dan `KEY_FILENAME` dengan nama file kunci `.pem` Anda.

6.  **Jalankan Skrip:**
    ```bash
    python monitor.py
    ```
