from fastapi import HTTPException

def successful_response(status_code:int):
    return{"status":status_code,"transaction" : "Successful"}
    
def http_Exception():
    return HTTPException(status_code=404, detail= "Todo not Found")