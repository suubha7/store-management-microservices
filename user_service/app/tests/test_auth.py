from app.auth import create_access_token
from jose import jwt
from app.auth import SECRET_KEY, ALGORITHM

def test_create_access_token():

    token = create_access_token(user_id= 1, role= "user")

    assert isinstance(token, str)

    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms= ALGORITHM
    )
    
    assert payload['sub'] == '1'
    assert payload['role'] == "user"


