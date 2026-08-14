from fastapi import APIRouter
from fastapi import Depends, HTTPException

router = APIRouter(
    prefix="/messeges",
    tags=["Messeges"],
)

