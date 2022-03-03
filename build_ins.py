import platform
import PyInstaller.__main__

_TARGET = 'installer/installer.py'

plat = platform.system()
name = 'NH_installer_windows'  

OPTIONS = [
    _TARGET,
    "-n=NH",
    "-y",
    "--clean",
    "--onefile",
    "--windowed",
    "-i=nh.ico"
]

def main():
    PyInstaller.__main__.run(OPTIONS)

if __name__ == '__main__':
    main()