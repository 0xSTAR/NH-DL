import PyInstaller.__main__

_TARGET = "src/__main__.py"

OPTIONS = [_TARGET, "-n=NH", "-y", "--clean", "--onefile", "--windowed", "-i=nh.ico"]


def main():
    PyInstaller.__main__.run(OPTIONS)


if __name__ == "__main__":
    main()
