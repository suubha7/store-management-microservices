from app.auth import hash_password, verify_password


def test_hash_password():

    hashed = hash_password("Suubha@090")

    assert hashed != "Suubha@090"
    assert len(hashed) > 0

def test_verity_password():
    hashed = hash_password("TestPassword")
    verify = verify_password("TestPassword", hashed)

    assert verify == True

def test_wrong_password():
    hashed = hash_password("TestPassword")
    verify = verify_password("Password", hashed)

    assert verify == False


