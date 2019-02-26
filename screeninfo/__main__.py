from .screeninfo import get_monitors


def main():
    for m in get_monitors():
        print(str(m))


if __name__ == "__main__":
    main()
