"""module to implement fast api"""

from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import mychromadb

app = FastAPI()


class File(BaseModel):
    """class for file"""
    file_path: str
    file_name: str


class Question(BaseModel):
    """class for question"""
    pdf_name: str
    question: str


@app.get("/")
async def root():
    """api function for root path"""
    return "Welcome to my Q&A application"


@app.post(
    "/upload/{pdf_path}/{pdf_name}",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
)
async def upload_docs(pdf_path: str, pdf_name: str):
    """for uploading files"""
    try:
        new_file = pdf_path + pdf_name
        mychromadb.embed_document(file_path=new_file, file_name=pdf_name)
        db = mychromadb.get_db()
        docs = db.get(where={"file_name": pdf_name})
        response_data = {"message": "File uploaded successfully", "file": pdf_name, "content": docs}
        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=500, detail="error in uploading file"
        ) from e


@app.get("/answers/{pdf_name}/{question}", status_code=status.HTTP_200_OK)
async def get_answers(pdf_name: str, question: str):
    """for asking answers"""
    try:
        ans = mychromadb.get_answer_from_palm(question, pdf_name)
        response_data = {"message": "search was successful", "question": question, "answer": ans}
        return response_data

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="internal server error"
        ) from e


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
