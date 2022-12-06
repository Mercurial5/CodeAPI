from dotenv import load_dotenv

load_dotenv()

from codeapi.api import app


def main():
    app.run()


if __name__ == '__main__':
    main()
