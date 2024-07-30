from fastapi import FastAPI,HTTPException,Request,status, Form , Header
from pydantic import BaseModel,Field
from typing import Optional
from uuid import UUID
from starlette.responses import JSONResponse

app = FastAPI()

class NegativeNumberException(Exception):
    def __init__(self,books_to_return):
        self.books_to_return = books_to_return


class Book(BaseModel):
    id:UUID
    title : str = Field(min_length=1)
    author :str =Field(min_length=1, max_length=100)
    description : Optional[str] = Field(title="Description of the book",max_length=100,min_length=1)
    rating: int = Field(gt=-1,lt=101)
    class Config:
        json_schema_extra = {
            "example":{
                "id":"1fa85f64-5717-4562-b3fc-2c963f66afa6",
                "title":"Python Learning",
                "author":"Codingwithfahad",
                "description":"A very nice description of a book",
                "rating":75
            }
        }
class BooksNoRating(BaseModel):
    id: UUID
    title : str=Field(min_length=1)
    author : str
    description : Optional[str] = Field(title="Description of the book",
                                        max_length=100,
                                        min_length=1
                                        )
    

BOOKS =[]

@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request:Request,exception: NegativeNumberException ):
    return JSONResponse(
        status_code=418,
        content={"message":f"Hey, Why do you want {exception.books_to_return} books? You need to read more!"}
    )

@app.get("/")
async def read_all_books(books_to_return : Optional[int] = None):
    if books_to_return and books_to_return<0:
        raise NegativeNumberException(books_to_return)
    if len(BOOKS)<1:
        create_books_no_api()
    if books_to_return and len(BOOKS)>=books_to_return>0:
        i=1
        new_book = []
        while i <=books_to_return:
            new_book.append(BOOKS[i-1])
            i+=1
        return new_book
    return BOOKS

@app.get("/book/{book_id}")
async def read_book_by_id(id : UUID):
    for book in BOOKS:
        if book.id == id:
            return book
    raise raise_item_not_found()

@app.get("/book/rating/{book_id}",response_model=BooksNoRating)
async def read_book_no_rating_by_id(id : UUID):
    for book in BOOKS:
        if book.id == id:
            return book
    raise raise_item_not_found()

@app.post("/",status_code=status.HTTP_201_CREATED)
async def create_book(book:Book):
    BOOKS.append(book)
    return book

@app.delete("/{book_id}")
async def delete_book(book_id : UUID):
    counter = 0
    for book in BOOKS:
        if book_id == book.id:
            del BOOKS[counter]
            return f"ID {book_id} is deleted"
        counter+=1
    raise raise_item_not_found()

@app.post("/books/login")
async def book_login(username:str= Form(), password : str = Form()):
    return {"username" : username , "password":password}

@app.get("/header")
async def read_header(random_header : Optional[str] = Header(None)):
    return {"Random-Header": random_header}

def create_books_no_api():
    book_1 = Book(id="3fa85f64-5717-4562-b3fc-2c963f66afa6",
                  title="Title 1",
                  author="Author 1",
                  description="description 1",
                  rating=60
                  )
    book_2 = Book(id="4fa85f64-5717-4562-b3fc-2c963f66afa6",
                  title="Title 2",
                  author="Author 2",
                  description="description 2",
                  rating=70
                  )
    book_3 = Book(id="5fa85f64-5717-4562-b3fc-2c963f66afa6",
                  title="Title 3",
                  author="Author 3",
                  description="description 3",
                  rating=80
                  )
    book_4 = Book(id="6fa85f64-5717-4562-b3fc-2c963f66afa6",
                  title="Title 4",
                  author="Author 4",
                  description="description 4",
                  rating=90
                  )
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)

def raise_item_not_found():
    return HTTPException(status_code=404,detail="Book not found",headers={"X-Header-Error":"Nothing to be at the UUID"} )