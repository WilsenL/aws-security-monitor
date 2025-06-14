import paramiko
import os
import smtplib  # Library baru untuk mengirim email

# --- Blok 1: Fungsi Pengirim Email ---


def send_alert_email(subject, body):
    """Fungsi untuk mengirim notifikasi email."""
    # Mengambil kredensial dari environment variables
    sender_email = os.environ.get('EMAIL_USER')
    sender_password = os.environ.get('EMAIL_PASS')

    if not sender_email or not sender_password:
        print("❌ Kredensial email (EMAIL_USER/EMAIL_PASS) tidak ditemukan. Melewatkan pengiriman email.")
        return

    # Pesan email
    message = f"Subject: {subject}\n\n{body}"

    try:
        print("Mengirim notifikasi email...")
        # Menghubungkan ke server SMTP Google
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Mengamankan koneksi
        server.login(sender_email, sender_password)
        # Mengirim email ke diri sendiri
        server.sendmail(sender_email, sender_email, message)
        server.quit()
        print("✅ Email notifikasi berhasil dikirim!")
    except Exception as e:
        print(f"❌ Gagal mengirim email: {e}")


# --- Blok 1: Konfigurasi ---
# Ganti nilai di bawah ini sesuai dengan detail Anda.
HOST = "44.205.250.234"  # Ganti dengan IP Publik EC2 Anda
USER = "ubuntu"
# Pastikan path ke file kunci Anda benar.
# Jika file .pem ada di folder yang sama, cukup tulis namanya.
KEY_FILENAME = "labsuser.pem"
LOG_FILE = "/var/log/auth.log"
SEARCH_PATTERNS = ["Failed password", "invalid user", "Failed publickey for"]

print("--- Skrip Pemantau Honeypot Dimulai ---")

# Inisialisasi SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # --- Blok 2: Membangun Koneksi SSH ---
    print(f"Menghubungkan ke server {HOST}...")
    ssh.connect(hostname=HOST, username=USER, key_filename=KEY_FILENAME)
    print("✅ Koneksi berhasil!")

    # --- Blok 3: Mengeksekusi Perintah & Membaca Log ---
    print(f"Membaca file log: {LOG_FILE}...")
    # Menjalankan perintah 'cat' untuk membaca file log di server
    stdin, stdout, stderr = ssh.exec_command(f"sudo cat {LOG_FILE}")

    # Membaca output dari perintah dan mengubahnya menjadi teks
    log_content = stdout.read().decode()
    error_output = stderr.read().decode()

    if error_output:
        print(f"❌ Terjadi error saat eksekusi perintah: {error_output}")
    else:
        print("✅ Log berhasil dibaca.")

        # --- Blok 4: Mencari Jejak Mencurigakan ---
        print(f"Mencari baris yang mengandung '{SEARCH_PATTERNS}'...")
        suspicious_lines_found = []
        for line in log_content.splitlines():
            for pattern in SEARCH_PATTERNS:
                if pattern in line:
                    suspicious_lines_found.append(line)
                    break

        if suspicious_lines_found:
            print(
                f"🚨 DITEMUKAN {len(suspicious_lines_found)} AKTIVITAS MENCURIGAKAN! 🚨")

            # Membuat isi email dari log yang mencurigakan
            email_body = "Ditemukan aktivitas mencurigakan pada server Anda:\n\n"
            for suspicious_line in suspicious_lines_found:
                print(f"   - {suspicious_line}")
                email_body += suspicious_line + "\n"

            # --- MODIFIKASI: Panggil fungsi pengirim email ---
            send_alert_email("Peringatan Keamanan Server!", email_body)
        else:
            print("✅ Tidak ada aktivitas mencurigakan yang ditemukan.")

finally:
    # --- Blok 5: Menutup Koneksi (Penting!) ---
    print("Menutup koneksi SSH...")
    ssh.close()
    print("--- Skrip Selesai ---")
