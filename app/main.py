import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import google.generativeai as generative_ai

app = FastAPI()

class Settings:
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY")

settings = Settings()


class PromptRequest(BaseModel):
    prompt: str
    
generative_ai.configure(api_key=settings.GOOGLE_API_KEY)


@app.get("health/")
async def health():
    return {"message": "Hello World"}


@app.post("/classify-sentiment")
async def classify_sentimental(request: PromptRequest):
    try:
        model = generative_ai.GenerativeModel('gemini-1.5-pro')
        formatted_prompt = f"Analiza el sentimiento de los siguiente frase y clasifícalos solamente como POSITIVO, NEGATIVO o NEUTRO(NO DEBES DAR MAS EXPLICACION, SOLO INDICAME POSITIVO, NEGATIVO O NEUTRO). {request.prompt}."
        response = model.generate_content(formatted_prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))