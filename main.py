from fastapi import FastAPI, File, UploadFile, Form, HTTPException, Depends
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from gtts import gTTS
from PIL import Image
from typing import List
from io import BytesIO
import chardet
import os
from langdetect import detect
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from api.user_api.user import user_router

app = FastAPI(docs_url="/", tags=["Создание аудиокниги"])

app.include_router(user_router)
# SQLAlchemy setup
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, unique=True, index=True)
    language = Column(String)
    slow = Column(Boolean)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/convert/")
async def convert_book_to_audio(
        file: UploadFile = File(...),
        images: List[UploadFile] = File(...),
        language: str = Form(default="auto"),
        slow: bool = Form(default=False),
        max_image_size: int = Form(default=1024),
        db: Session = Depends(get_db)
):
    # Чтение содержимого файла
    contents = await file.read()

    # Определение типа файла и извлечение текста
    if file.filename.endswith('.txt'):
        text = contents.decode('utf-8')
    else:
        # Определение кодировки для других текстовых форматов
        result = chardet.detect(contents)
        encoding = result['encoding']

        try:
            text = contents.decode(encoding)
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="Unable to decode the file content")

    # Определение языка текста
    if language == "auto":
        detected_language = detect(text)
        if detected_language == "ru":
            language = "ru"
        elif detected_language == "en":
            language = "en"
        else:
            raise HTTPException(status_code=400, detail="Unsupported language detected")
    elif language not in ["ru", "en"]:
        raise HTTPException(status_code=400, detail="Unsupported language")

    # Сохранение аудиофайла в папку static
    audio_path = "static/output.mp3"
    tts = gTTS(text, lang=language, slow=slow)
    tts.save(audio_path)

    # Сохранение записи в базу данных
    db_audio_file = AudioFile(filename="output.mp3", language=language, slow=slow)
    db.add(db_audio_file)
    db.commit()

    # Сохранение изображений
    image_paths = []
    for i, image in enumerate(images):
        image_extension = image.filename.split('.')[-1].lower()
        if image_extension not in ["jpg", "jpeg", "png"]:
            raise HTTPException(status_code=400, detail="Unsupported image format")

        img = Image.open(BytesIO(await image.read()))
        img.thumbnail((max_image_size, max_image_size))

        image_path = f"static/image_{i}.{image_extension}"
        img.save(image_path)
        image_paths.append(image_path)

    return JSONResponse(content={
        "audio_file": f"/files/output.mp3",
        "images": [f"/files/{os.path.basename(path)}" for path in image_paths]
    })


@app.get("/audio/{filename}")
async def get_audio(filename: str):
    audio_path = f'static/{filename}.mp3'
    if not os.path.exists(audio_path):
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(audio_path)


@app.delete("/audio/{filename}")
async def delete_audio(filename: str, db: Session = Depends(get_db)):
    db_audio_file = db.query(AudioFile).filter(AudioFile.filename == filename).first()
    if not db_audio_file:
        raise HTTPException(status_code=404, detail="Audio file not found")

    # Удаление файла из системы
    os.remove(f'static/{filename}')

    # Удаление записи из базы данных
    db.delete(db_audio_file)
    db.commit()

    return JSONResponse(content={"detail": "Audio file deleted successfully"})


# Маршрут для обслуживания статических файлов
app.mount("/files", StaticFiles(directory="static"), name="static")

# Запуск приложения (например, с помощью uvicorn)
# uvicorn main:app --reload
