from dotenv import load_dotenv
import os

load_dotenv()

from codeapi.api import app


def main():
    app.run(host=os.getenv('FLASK_HOST'), port=os.getenv('FLASK_PORT'))


if __name__ == '__main__':
    main()
