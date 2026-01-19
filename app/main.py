from fastapi import FastAPI

app = FastAPI(title="Crypto Observability API")


@app.get("/health")
def health():
    return {"status": "ok"}
