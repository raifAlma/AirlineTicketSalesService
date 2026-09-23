from fastapi import APIRouter, Depends, HTTPException, Query


router = APIRouter(
    prefix="/airline",
    tags=["Airline"],
)

