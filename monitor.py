import paramiko
import os
import smtplib


def send_alert_email(subject, body):
    # Taking environment variables
    sender_email = os.environ.get('EMAIL_USER')
    sender_password = os.environ.get('EMAIL_PASS')

    if not sender_email or not sender_password:
        print("❌ Credential email (EMAIL_USER/EMAIL_PASS) Not Found. Skip sending email.")
        return

    # email
    message = f"Subject: {subject}\n\n{body}"

    try:
        print("Sending Notification email...")
        # Connecting to SMTP Google server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()  # Mengamankan koneksi
        server.login(sender_email, sender_password)
        # Sending email to self
        server.sendmail(sender_email, sender_email, message)
        server.quit()
        print("✅ Email notifikasi Sent!")
    except Exception as e:
        print(f"❌ Failed sending email: {e}")


HOST = "44.205.250.234"  # AwS Public IP
USER = "ubuntu"
KEY_FILENAME = "labsuser.pem"  # Public Key File
LOG_FILE = "/var/log/auth.log"
SEARCH_PATTERNS = ["Failed password", "invalid user", "Failed publickey for"]

# Inisialisasi SSH client
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    print(f"Connecting to server {HOST}...")
    ssh.connect(hostname=HOST, username=USER, key_filename=KEY_FILENAME)
    print("✅ Connection Succeed!")
    print(f"Reading log: {LOG_FILE}...")
    stdin, stdout, stderr = ssh.exec_command(f"sudo cat {LOG_FILE}")

    # Convert output to string
    log_content = stdout.read().decode()
    error_output = stderr.read().decode()

    if error_output:
        print(f"❌ Error: {error_output}")
    else:
        print("✅ Log Read.")

        # Search for suspicious activity
        print(f"Searching for '{SEARCH_PATTERNS}'...")
        suspicious_lines_found = []
        for line in log_content.splitlines():
            for pattern in SEARCH_PATTERNS:
                if pattern in line:
                    suspicious_lines_found.append(line)
                    break

        if suspicious_lines_found:
            print(
                f"🚨 Founded {len(suspicious_lines_found)} Suspicious Activity! 🚨")

            # Making email body
            email_body = "Founded Suspicious Activity in server:\n\n"
            for suspicious_line in suspicious_lines_found:
                print(f"   - {suspicious_line}")
                email_body += suspicious_line + "\n"

            # Sending alert email
            send_alert_email("Server Security Alert!", email_body)
        else:
            print("✅ No Suspicious Activity Founded.")

finally:
    # Close SSH connection
    print("Closing SSH...")
    ssh.close()
    print("--- Skrip Finish ---")
