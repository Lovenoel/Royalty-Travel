import paramiko
import os
import time
import getpass

# Set path to your private key file
private_key = os.path.expanduser("~/.ssh/id_rsa")

# Environment variables fetched from os.environ directly
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

def get_passphrase():
    passphrase = getpass.getpass(prompt="Enter passphrase for private key: ")
    return passphrase

def run_ssh_command(ssh, command, description, retries=3, delay=5):
    print(f"Running: {description}")
    for attempt in range(retries):
        stdin, stdout, stderr = ssh.exec_command(command)
        stdout.channel.recv_exit_status()  # Wait for the command to finish
        output = stdout.read().decode()
        error = stderr.read().decode()
        if error:
            print(f"Error: {description} (Attempt {attempt + 1}/{retries})")
            print(error)
            if "dpkg" in error and "lock" in error:
                print("Waiting for dpkg lock to be released...")
                time.sleep(delay)
            else:
                break
        else:
            print(f"Success: {description}")
            print(output)
            break

def wait_for_dpkg_unlock(ssh, retries=5, delay=5):
    for _ in range(retries):
        stdin, stdout, stderr = ssh.exec_command("sudo lsof /var/lib/dpkg/lock-frontend")
        stdout.channel.recv_exit_status()
        output = stdout.read().decode()
        if not output:
            return True
        print("Waiting for dpkg lock to be released...")
        time.sleep(delay)
    return False

# List of servers with SSH key details
servers = [
    {"host": "100.25.16.64", "user": "ubuntu", "private_key": private_key},
]

project_dir = "/var/www/Royalty-Travel/backend"
repo_url = "https://github.com/Lovenoel/Royalty-Travel.git"

def connect_to_server(server):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    passphrase = get_passphrase()

    private_key_file = paramiko.RSAKey.from_private_key_file(
        server["private_key"],
        password=passphrase
    )

    try:
        ssh.connect(server["host"], username=server["user"], pkey=private_key_file)
        return ssh
    except paramiko.AuthenticationException as e:
        print(f"Authentication failed for {server['host']}: {e}")
        return None
    except paramiko.SSHException as e:
        print(f"SSH error for {server['host']}: {e}")
        return None

def deploy_to_servers():
    for server in servers:
        ssh = connect_to_server(server)
        if ssh:
            try:
                pre_commands = [
                    ("sudo killall apt apt-get dpkg", "Terminate package management processes"),
                    ("sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock", "Remove dpkg locks"),
                    # ("sudo dpkg --configure -a", "Configure dpkg for interrupted installs"),
                ]

                for command, description in pre_commands:
                    run_ssh_command(ssh, command, description)

                if not wait_for_dpkg_unlock(ssh):
                    print("Failed to acquire dpkg lock after several attempts.")
                    ssh.close()
                    continue

                commands = [
                    # Install Python 3.8 and venv
                    #("sudo apt update", "Update package lists"),
                    #("sudo apt install -y python3.8 python3.8-venv", "Install Python 3.8 and venv"),

                    # ("sudo apt-get install -y python3-pip python3-dev nginx supervisor python3-venv", "Install necessary packages"),

                    (f"sudo mkdir -p {project_dir}", "Create project directory"),
                    (f"sudo chown -R ubuntu:ubuntu {project_dir}", "Adjust ownership"),
                    (f"sudo chmod -R 755 {project_dir}", "Adjust permissions"),
                    (f"git clone {repo_url} {project_dir}", "Clone the project repository"),

                    # Create a virtual environment and install dependencies
                    #(f"sudo apt-get install -y python3-venv", "Install python3-venv package"),
                    (f"python3 -m venv {project_dir}/venv", "Create virtual environment"),
                    (f"source {project_dir}/venv/bin/activate && pip install -r {project_dir}/requirements.txt", "Install project dependencies"),
                    (f"echo 'SECRET_KEY={SECRET_KEY}\nSQLALCHEMY_DATABASE_URI={SQLALCHEMY_DATABASE_URI}' > {project_dir}/.env", "Create .env file"),

                    # Create Gunicorn systemd service file
                    (f"echo '[Unit]\nDescription=Gunicorn instance to serve Royalty-Travel/backend\nAfter=network.target\n\n[Service]\nUser=root\nGroup=www-data\nWorkingDirectory={project_dir}\nEnvironment=\"PATH={project_dir}/venv/bin\"\nExecStart={project_dir}/venv/bin/gunicorn --workers 3 --bind unix:{project_dir}/Royalty-Travel/backend.sock -m 007 wsgi:app\n\n[Install]\nWantedBy=multi-user.target' | sudo tee /etc/systemd/system/Royalty-Travel/backend.service", "Create Gunicorn systemd service file"),
                    ("sudo systemctl daemon-reload", "Reload systemd to recognize new service file"),

                    # Start and enable Gunicorn service
                    ("sudo systemctl start Royalty-Travel", "Start Gunicorn service"),
                    ("sudo systemctl enable Royalty-Travel", "Enable Gunicorn service"),

                    # Create Nginx configuration file
                    (f"echo 'server {{\n    listen 80;\n    server_name 100.25.16.64;\n\n    location / {{\n        include proxy_params;\n        proxy_pass http://unix:{project_dir}/Royalty-Travel/backend.sock;\n    }}\n\n    location /static/ {{\n        alias {project_dir}/app/static/;\n    }}\n}}' | sudo tee /etc/nginx/sites-available/Royalty-Travel/backend", "Create Nginx configuration file"),

                    # Enable Nginx site
                    ("sudo ln -s /etc/nginx/sites-available/Royalty-Travel/bcakend /etc/nginx/sites-enabled", "Enable Nginx site"),

                    # Test and restart Nginx
                    ("sudo nginx -t", "Test Nginx configuration"),
                    ("sudo systemctl restart nginx", "Restart Nginx"),

                    # Install Certbot for SSL
                    ("sudo apt install certbot python3-certbot-nginx -y", "Install Certbot for SSL"),

                    # Obtain SSL certificate
                    (f"sudo certbot --nginx -d kinglovenoel.tech --non-interactive --agree-tos -m kinglovenoel@gmail.com", "Obtain SSL certificate"),

                    # Run database migrations
                    (f"{project_dir}/venv/bin/flask db upgrade", "Run database migrations"),
                ]

                for command, description in commands:
                    run_ssh_command(ssh, command, description)
            finally:
                ssh.close()

if __name__ == "__main__":
    deploy_to_servers()


