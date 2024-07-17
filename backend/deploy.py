import paramiko
import os

# Set path to your private key file (replace with your actual path)
private_key = os.path.expanduser("/c/Users/USER/.ssh/id_rsa")

# Define your environment variables here (or fetch from os.environ directly)
SECRET_KEY = os.getenv('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')

def run_ssh_command(ssh, command, description):
    print(f"Running: {description}")
    stdin, stdout, stderr = ssh.exec_command(command)
    stdout.channel.recv_exit_status()  # Wait for the command to finish
    output = stdout.read().decode()
    error = stderr.read().decode()
    if error:
        print(f"Error: {description}")
        print(error)
    else:
        print(f"Success: {description}")
        print(output)

# List of servers with SSH key details
servers = [
    {"host": "100.25.16.64", "user": "ubuntu", "private_key": private_key},
    {"host": "54.237.217.181", "user": "ubuntu", "private_key": private_key},
    # Add more servers as needed
]

project_dir = "/var/www/Royalty-Travel"
repo_url = "https://github.com/Lovenoel/Royalty-Travel.git"

def connect_to_server(server):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    private_key_file = paramiko.RSAKey.from_private_key_file(server["private_key"])
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
                # Commands to run on the server
                commands = [
                    ("sudo apt update && sudo apt upgrade -y", "Update and upgrade the server"),
                    ("sudo apt install python3-pip python3-dev nginx supervisor -y", "Install necessary packages"),
                    (f"mkdir -p {project_dir}", "Create project directory"),
                    (f"git clone {repo_url} {project_dir}", "Clone the project repository"),
                    (f"python3 -m venv {project_dir}/venv", "Create virtual environment"),
                    (f"source {project_dir}/venv/bin/activate && pip install -r {project_dir}/requirements.txt", "Install project dependencies"),
                    (f"echo 'SECRET_KEY={SECRET_KEY}\nSQLALCHEMY_DATABASE_URI={SQLALCHEMY_DATABASE_URI}' > {project_dir}/.env", "Create .env file"),
                    # Create Gunicorn systemd service file
                    (f"echo '[Unit]\nDescription=Gunicorn instance to serve your_project\nAfter=network.target\n\n[Service]\nUser=root\nGroup=www-data\nWorkingDirectory={project_dir}\nEnvironment=\"PATH={project_dir}/venv/bin\"\nExecStart={project_dir}/venv/bin/gunicorn --workers 3 --bind unix:{project_dir}/your_project.sock -m 007 wsgi:app\n\n[Install]\nWantedBy=multi-user.target' | sudo tee /etc/systemd/system/your_project.service", "Create Gunicorn systemd service file"),
                    ("sudo systemctl daemon-reload", "Reload systemd to recognize new service file"),
                    # Start and enable Gunicorn service
                    ("sudo systemctl start your_project", "Start Gunicorn service"),
                    ("sudo systemctl enable your_project", "Enable Gunicorn service"),
                    # Create Nginx configuration file
                    (f"echo 'server {{\n    listen 80;\n    server_name your_server_domain_or_IP;\n\n    location / {{\n        include proxy_params;\n        proxy_pass http://unix:{project_dir}/your_project.sock;\n    }}\n\n    location /static/ {{\n        alias {project_dir}/app/static/;\n    }}\n}}' | sudo tee /etc/nginx/sites-available/your_project", "Create Nginx configuration file"),
                    # Enable Nginx site
                    ("sudo ln -s /etc/nginx/sites-available/your_project /etc/nginx/sites-enabled", "Enable Nginx site"),
                    # Test and restart Nginx
                    ("sudo nginx -t", "Test Nginx configuration"),
                    ("sudo systemctl restart nginx", "Restart Nginx"),
                    # Install Certbot for SSL
                    ("sudo apt install certbot python3-certbot-nginx -y", "Install Certbot for SSL"),
                    # Obtain SSL certificate
                    (f"sudo certbot --nginx -d your_server_domain_or_IP --non-interactive --agree-tos -m your_email@example.com", "Obtain SSL certificate"),
                    # Run database migrations
                    (f"/var/www/your_project/venv/bin/flask db upgrade", "Run database migrations"),
                ]
                for command, description in commands:
                    run_ssh_command(ssh, command, description)
            finally:
                ssh.close()

if __name__ == "__main__":
    deploy_to_servers()