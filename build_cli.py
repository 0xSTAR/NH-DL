import PyInstaller.__main__

_TARGET = 'src/cli.py'

OPTIONS = [
    _TARGET,
    "-n=NH_cli",
    "-y",
    "--clean",
    "--onefile",
    "-i=nh.ico"
]

def main():
    PyInstaller.__main__.run(OPTIONS)

if __name__ == '__main__':
    main()