from dotenv import load_dotenv
import os

load_dotenv()
host = os.environ.get('NEO4J_HOST')
password = os.environ.get('NEO4J_PASSWORD')
user = os.environ.get('NEO4J_USER')
port = os.environ.get('NEO4J_BOLT_PORT')

if __name__ == '__main__':
    print(host)
    print(password)
    print(user)
    print(port)
