from fastapi import FastAPI


app = FastAPI(
    title="Medical Questionnaire Templates API",
    description="Read-only API for available medical questionnaire templates.",
    version="1.0.0",
)


@app.get("/health", tags=["system"])
async def health() -> dict[str, str]:
    return {"status": "ok"}