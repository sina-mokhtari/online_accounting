from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from users.schemas import UserCreate, UserDisplay
from users import crud

router = APIRouter(
    prefix="/user",
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=UserDisplay)
async def signup(
        user: UserCreate, db: Session = Depends(get_db)
):
    if crud.get_user(db, user.username):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="username not available")
    if crud.get_user_by_email(db,user.email):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="email not available")

    return crud.create_user(db, user)

# @router.get("/")
# async def read_items():
#     return fake_items_db


# @router.get("/{item_id}")
# async def read_item(item_id: str):
#     if item_id not in fake_items_db:
#         raise HTTPException(status_code=404, detail="Item not found")
#     return {"name": fake_items_db[item_id]["name"], "item_id": item_id}
#
#
# @router.put(
#     "/{item_id}",
#     tags=["custom"],
#     responses={403: {"description": "Operation forbidden"}},
# )
# async def update_item(item_id: str):
#     if item_id != "plumbus":
#         raise HTTPException(
#             status_code=403, detail="You can only update the item: plumbus"
#         )
#     return {"item_id": item_id, "name": "The great Plumbus"}
#
