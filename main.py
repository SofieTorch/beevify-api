from typing import Annotated
from fastapi import Depends, FastAPI
from providers.mail_provider import send_challenge_answer_results
import dependencies.config as config
import models
from providers.rag_provider import query_rag

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/typeform")
async def process_typeform_response(
    event: models.Event,
    settings: Annotated[config.Settings, Depends(config.get_settings)]
):
    answers_content = []
    
    for answer in event.form_response.answers:
        content = answer.text or answer.email or answer.boolean

        answers_content.append({
            "field_id": answer.field.id,
            "field_type": answer.field.type,
            "content": content
        })
    
    response = query_rag(answers_content[0]["content"], settings)
    print("despues de llamar el rag")
    
    await send_challenge_answer_results(
        email=answers_content[1]["content"],
        answer_content=response['answer'],
        settings=settings
    )
    
    return {"answers": answers_content}