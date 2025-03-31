import traceback

from fastapi import HTTPException

from ...utils.logger import logger
from .interfaces.handler import IHandler

class ErrorHandler(IHandler):
    
    @staticmethod
    def _process_exception(name: str) -> None:
        match name:
            case "IntegrityError":
                raise HTTPException(
                    status_code=400, detail="Violation integrity. Check if the request do not violates some constraints. Some fields in provided data is incorrect"
                )
            case "ValueError":
                raise HTTPException(
                    status_code=400, detail="Value error. Check if provided data is correct"
                ) 
            case "NoResultFound":
                raise HTTPException(
                    status_code=404, detail="No result found with this data"
                )
            case "ExpiredSignatureError":
                raise HTTPException(
                    status_code=401, detail="Access token has expired"
                )
            case "JWTError":
                raise HTTPException(
                    status_code=401, detail="Invalid authentication credentials"
                )
            case "ValidationError":
                raise HTTPException(
                    status_code=400, detail="Could not validate credentials"
                )
    
    async def handle(self, e: Exception):
        if isinstance(e, HTTPException):
            raise e
        self._process_exception(e.__class__.__name__)
        await logger.write_exception_log(
            error="".join(
                traceback.format_exception(type(e), e, e.__traceback__)
            )
        )
    
error_handler = ErrorHandler()