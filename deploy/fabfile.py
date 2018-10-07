# test
# 80 - порт да размещения за nginx
# fab -u gallary -p gallary --sudo-password=gallary -H 10.0.3.126 deploy:80
# fab -u gallary -p gallary --sudo-password=gallary -H 10.0.3.126 pre_deploy:80


REPO_URL = "ayudin@192.168.6.232:~/VirtualBox/GIT-HUB/gallary"
REPO_BRANCH = "master"
MEDIA_ROOT = '/home/gallary/media/photos'

import random

from fabric.api import env
from fabric.contrib.files import exists, sed, append
from fabric.operations import run, local, sudo


class Install:
    def install_python(self, version):
        sudo("apt install nano mc wget -y")
        sudo("apt install build-essential -y")
        sudo("apt install libreadline-gplv2-dev libncursesw5-dev libssl-dev libsqlite3-dev tk-dev libgdbm-dev libc6-dev libbz2-dev -y")
        sudo(f"wget https://www.python.org/ftp/python/{version}/Python-{version}.tar.xz &&  tar xvf Python-{version}.tar.xz && cd Python-{version}/ && ./configure --enable-shared && make && make install")


class Deploy(Install):
    def __init__(self, REPO_URL, REPO_BRANCH, PYTHON_VERSION="3.6.6", project_dir_name="project", manage_module_name="manage.py"):
        self.REPO_URL = REPO_URL
        self.REPO_BRANCH = REPO_BRANCH
        self.PYTHON_VERSION = PYTHON_VERSION
        self.project_dir_name = project_dir_name
        self.manage_module_name = manage_module_name

    def getSiteName(self, port_servise=80):
        return f"{env.host}.{port_servise}"

    def pre_deploy(self):
        if not exists(f"/home/Python-{self.PYTHON_VERSION}"):
            self.install_python(self.PYTHON_VERSION)
            sudo("apt install python3-pip sudo -y")

            sudo("apt remove apache2 -y")
            sudo("apt purge apache2 -y")
            sudo("apt autoremove -y")
            sudo("apt purge apache2.* -y")
            sudo("apt install nginx -y")
            sudo("apt install curl -y")
            sudo("apt install python-software-properties -y")
            sudo("curl -sL https://deb.nodesource.com/setup_10.x | sudo -E bash -")
            sudo("apt install git nodejs -y")
            sudo("npm install -g grunt-cli -y")
            sudo("ln -s /usr/bin/nodejs /usr/bin/node")

    def deploy(self, port_servise=80):
        self.siteName = self.getSiteName(port_servise)
        self.siteFolder = f"/home/{env.user}/sites/{self.siteName}"
        run(f"rm -rf {self.siteFolder}")
        self.sourceFolder = f"{self.siteFolder}/source"

        sudo("apt update")
        sudo("apt dist-upgrade -y")

        self.deployProcs()
        self.serviceProcs(port=port_servise)

    def deployProcs(self):
        self.createDirectoryStructure()
        self.getSources(sourceFolder=self.sourceFolder, REPO_BRANCH=self.REPO_BRANCH, REPO_URL=self.REPO_URL)
        run(f"/usr/local/bin/pip3 install --user --upgrade pip")
        run(f"/usr/local/bin/pip3 install --user --no-cache-dir -r {self.sourceFolder}/requirements.txt")
        self.updateSetting()
        self.updateDatabase()
        self.nmpUpdate()
        self.updateStatic()

    def createDirectoryStructure(self):
        for subfolder in ("source", "static", "database"):
            run(f"mkdir -p {self.siteFolder}/{subfolder}")
        run(f"mkdir -p {MEDIA_ROOT}")

    def getSources(self, sourceFolder, REPO_BRANCH, REPO_URL):
        if exists(f"{sourceFolder}/.git"):
            run(f"cd {sourceFolder} && git fetch")
        else:
            run(f"git clone --single-branch -b {REPO_BRANCH} {REPO_URL} {sourceFolder}")

        current_commit = local(f"git log -n 1 --format=%H", capture=True)
        run(f"cd {sourceFolder} git reset --hard {current_commit}")

    def updateSetting(self):
        settingPath = f"{self.sourceFolder}/{self.project_dir_name}/settings.py"
        if not exists(settingPath):
            raise Exception(f"File: {settingPath} not exists.")
        sed(settingPath, "DEBUG = True", "DEBUG = False")
        sed(settingPath, "ALLOWED_HOSTS =.+$", f'ALLOWED_HOSTS = ["{env.host}"]')

        secretKeyFile = f"{self.sourceFolder}/{self.project_dir_name}/secret_key.py"
        if not exists(secretKeyFile):
            chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
            key = "".join(random.SystemRandom().choice(chars) for _ in range(50))
            append(secretKeyFile, f'SECRET_KEY="{key}"')
        append(settingPath, '\nfrom .secret_key import SECRET_KEY')

    def updateDatabase(self):
        run(f"cd {self.sourceFolder} && /usr/local/bin/python3.6 {self.manage_module_name} migrate --noinput")

    def updateStatic(self):
        run(f"cd {self.sourceFolder} && /usr/local/bin/python3.6 {self.manage_module_name} collectstatic --noinput")

    def nmpUpdate(self):
        if exists(f"{self.sourceFolder}/package.json"):
            run(f"cd {self.sourceFolder} && npm install && grunt")

    def test(self, port_servise=80):
        self.siteName = self.getSiteName(port_servise)
        self.siteFolder = f"/home/{env.user}/sites/{self.siteName}"
        self.sourceFolder = f"{self.siteFolder}/source"

        run(f"cd {self.sourceFolder} && make -f Makefile.dist check")

    def makeService(self, port_servise=80):
        self.siteName = self.getSiteName(port_servise)
        self.siteFolder = f"/home/{env.user}/sites/{self.siteName}"
        self.sourceFolder = f"{self.siteFolder}/source"

        self.serviceProcs(env.user, port_servise)

    def restartService(self, port_servise=80):
        self.siteName = self.getSiteName(port_servise)
        self._restartService()

    def _restartService(self):
        sudo("systemctl daemon-reload")
        sudo(f"systemctl enable {self.siteName}")
        sudo(f"systemctl restart {self.siteName}")
        sudo(f"systemctl status {self.siteName}")

    def serviceProcs(self, port=80):
        sitesAvailableCfg = f"/etc/nginx/sites-available/{self.siteName}"
        sudo(f"cp /home/{env.user}/.local/lib/python3.6/site-packages/isc_common/deploy/nginx-site-avalabel.conf {sitesAvailableCfg}")
        sed(sitesAvailableCfg, "SITENAME", self.siteName, use_sudo=True)
        sed(sitesAvailableCfg, "SERVERNAME", env.host, use_sudo=True)
        sed(sitesAvailableCfg, "PORT", str(port), use_sudo=True)
        sed(sitesAvailableCfg, "USERNAME", env.user, use_sudo=True)
        if not exists(f"/etc/nginx/sites-enabled/{self.siteName}"):
            sudo(f"ln -s /etc/nginx/sites-available/{self.siteName} /etc/nginx/sites-enabled/{self.siteName}")
        if exists(f"/etc/nginx/sites-enabled/default"):
            sudo("rm /etc/nginx/sites-enabled/default")
        sudo("systemctl reload nginx")
        sudo("systemctl restart nginx")
        servisePath = f"/etc/systemd/system/{self.siteName}.service"
        sudo(f"cp /home/{env.user}/.local/lib/python3.6/site-packages/isc_common/deploy/gunicorn-SITENAME.service {servisePath}")
        sed(servisePath, "SITENAME", self.siteName, use_sudo=True)
        sed(servisePath, "WORKERS", "3", use_sudo=True)
        sed(servisePath, "SMTP_SECRET", "Uandrew1965", use_sudo=True)
        sed(servisePath, "SECRET", "mt30718tm", use_sudo=True)
        sed(servisePath, "USERNAME", env.user, use_sudo=True)
        sed(servisePath, "PROJECT_DIR_NAME", self.project_dir_name, use_sudo=True)
        self._restartService()


deploy = Deploy(REPO_URL=REPO_URL, REPO_BRANCH=REPO_BRANCH).deploy
pre_deploy = Deploy(REPO_URL=REPO_URL, REPO_BRANCH=REPO_BRANCH).pre_deploy
