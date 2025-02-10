import bcrypt

password_crypto = "AAAAC3NzaC1lZDI1NTE5AAAAIGATfV9mGNGUUma34e3n0Nrwqi1qq1N5TTWwyPLn"

def encrypt_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed_password.decode("utf-8")

def verify_password(password, hashed_password):
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))