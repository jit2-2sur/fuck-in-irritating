"""main module for running the app"""

import uvicorn


if __name__ == "__main__":
    uvicorn.run("myapi:app", host="127.0.0.1", port=8000, reload=True)
