from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    "book_1":{"title":"title 1","Author" : "Author 1"},
    "book_2":{"title":"title 2","Author" : "Author 2"},
    "book_3":{"title":"title 3","Author" : "Author 3"},
    "book_4":{"title":"title 4","Author" : "Author 4"},
    "book_5":{"title":"title 5","Author" : "Author 5"},
}
class DirectionName(str,Enum):
    north = "NORTH"
    south = "SOUTH"
    east = "EAST"
    west = "WEST"
@app.get("/")
async def read_all_books(skip_book: Optional[str] = None):
    if skip_book:
        new_books= BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS

@app.get("/books/mybook")
async def read_fav_book():
    return {"book_title" : "My favourite book"}

@app.get("/book/{book_id}")
async def read_specific_book(book_id: str):
    return BOOKS.get(book_id)
    
@app.get("/direction/{direction_name}")
async def get_direction(direction_name : DirectionName):
    if direction_name == DirectionName.north:
        return {"Direction":direction_name,"sub":"Up" }
    if direction_name == DirectionName.south:
        return {"Direction":direction_name,"sub":"Down" }
    if direction_name == DirectionName.west:
        return {"Direction":direction_name,"sub":"Left" }
    if direction_name == DirectionName.east:
        return {"Direction":direction_name,"sub":"Right" }

@app.post("/")
async def create_book(book_title :str, book_author:str):
    current_id = 0
    if len(BOOKS) > 0:
        for book in BOOKS:
            x =  int(book.split("_")[-1])
        if x>current_id:
            current_id = x
    BOOKS[f"book_{current_id+1}"] = {"title":book_title,"Author":book_author}
    return BOOKS[f"book_{current_id+1}"]

@app.put("/{book_id}")
async def update_book(book_id:str, book_title:str, book_author:str):
    book_information = {"title":book_title,"Author":book_author}
    BOOKS[book_id] = book_information
    return book_information

@app.delete("/{book_id}")
async def delete_book(book_id:str):
    del BOOKS[book_id]
    return f"Book {book_id} deleted"

@app.get("/assignment")
async def read_book_assignment(book_id:str):
    return BOOKS[book_id]

@app.delete("/assignment")
async def delete_book_assignment(book_id:str):
    del BOOKS[book_id]
    return f"{book_id} is deleted"











