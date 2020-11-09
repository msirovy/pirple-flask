import string
import secrets


def generate_password(length):
    return ''.join(
        secrets.choice(
            string.ascii_lowercase + string.digits + string.ascii_uppercase + string.digits
        ) for i in range(length))
    



if __name__ == "__main__":
    print("10 char password: ", generate_password(10))