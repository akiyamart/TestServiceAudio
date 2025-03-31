import datetime
import aiofiles

from typing import Literal

class Logger:
    def __init__(self, filename):
        self.filename = filename

    async def write(self, log_message: str, status: Literal["INFO", "ERROR"] = "INFO"):
        try:
            async with aiofiles.open(self.filename, "a") as file:
                await file.write(
                    f"{datetime.datetime.today()}:{status}: {log_message}" + "\n"
                )
        except Exception as e:
            print(f"Error writing to log file: {e}")

    async def write_exception_log(
        self,
        error: str,
    ) -> None:
        message = f"Occurs an exception. Detail: {error}"
        await self.write(message, status="ERROR")


logger = Logger(filename="backend.log")
