from app.main import Login
from pydantic import BaseModel
from fastapi import Response, status, APIRouter

router = APIRouter()
class BaseLogin(BaseModel):
    npm: int
    password: str

@router.post(
  "/login",
  response_model=dict,
  tags=["Login"],
  summary="Login ke sikma.uajy.ac.id",
  description="API untuk login ke sikma.uajy.ac.id",
  responses={
    200: {
      "description": "Berhasil login", 
      "content": {
        "application/json": {
          "example": {
            "message": "Berhasil Login!", 
            "npm": 1234567890, 
            "name": "John Abe", 
            "cookies": {
              "ASP.NET_SessionId": "abc123"
              }
            }
          }
        }
      },
    401: {
      "description": "Gagal login, password salah",
      "content": {
        "application/json": {
          "example": {
            "message": "Gagal Login! Password salah."
            }
          }
        }
      },
    404: {
      "description": "Gagal login, data pengguna tidak ditemukan",
      "content": {
        "application/json": {
          "example": {
            "message": "Gagal Login! Data pengguna tidak ditemukan."
            }
          }
        }
      },
    500: {
      "description": "Error", 
      "content": {
        "application/json": {
          "example": {
            "message": "Error!"
            }
          }
        }
      }
  }
)
def login(login: BaseLogin, response: Response):
  login_service = Login(login.npm, login.password)
  message = login_service.login()

  if message["message"] == "Berhasil Login!":
    response.status_code = status.HTTP_200_OK
  elif message["message"] == "Gagal Login! Password salah.":
    response.status_code = status.HTTP_401_UNAUTHORIZED
  elif message["message"] == "Gagal Login! Data pengguna tidak ditemukan.":
    response.status_code = status.HTTP_404_NOT_FOUND
  else:
    response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    return {"message": "Error!"}
  
  return message