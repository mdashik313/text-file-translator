
<h2> A text file translation microservice using FastAPI and LLM APIs.</h2>

## Running the Application
Before starting you need [Python](https://www.python.org/downloads/), [pip and virtual environment](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) ti be installed.

1. Clone the repository

```
git clone "https://github.com/mdashik313/text-file-translator.git"
```
2. Navigate to the project folder
```
cd text-file-translator
```
3. Create virtual environment
```
python3 -m venv .venv
```
4. Activate virtual environment

For Windows(shell):
```
source venv/Scripts/activate
```
For Linux:
```
. .venv/bin/activate
```
5. Install project dependencies
```
pip install -r requirements.txt
```
6. Setup environment variables: create a .env file in the project directory add the variables.
```
GEMINI_API_KEY = <your_api_key>
MONGODB_CONNECTION_URI = <your_mongoDB_atlas_connection_url>
```
7. Run the application
```
uvicorn main:app --reload
```
