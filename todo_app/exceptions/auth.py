from fastapi import HTTPException,status

def get_user_exception():
    return HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Could Not Validate Credentials",
        headers={"WWW-Authenticate":"Bearer"}
    )
def token_exception():
    return HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect Username or password",
        headers={"WWW-Authenticate":"Bearer"}
    )