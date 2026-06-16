
import os
from uuid import uuid4

class FileService:

    @staticmethod
    def save_file(file, upload_dir):

        ext=file.filename.split(".")[-1]

        filename=f"{uuid4()}.{ext}"

        path=os.path.join(
            upload_dir,
            filename
        )

        with open(path,"wb") as f:
            f.write(file.file.read())

        return path
