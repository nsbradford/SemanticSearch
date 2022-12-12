# SemanticSearch



## Install

You might want to use `pyenv` to create a virtualenv in which to install Python dependencies:

    $ pyenv virtualenv 3.10.1 myenvname
    $ pyenv activate myenvname
    (myenvname) $ pip install -r requirements.txt


## Run

### FastAPI

Start the server
    $ uvicorn main:app --reload

Ask a question

    $ curl -X POST http://localhost:8000/query \
        -H 'Content-Type: application/json' \
        -d '{"query": "MY QUESTION HERE"}'

(didn't work) Upload a file https://superuser.com/questions/1054742/how-to-post-file-contents-using-curl

    $ curl -X POST http://localhost:8000/upload \
        --data-binary @data/essays/ace.txt 

Take 2 https://medium.com/@petehouston/upload-files-with-curl-93064dcccc76

    $ curl http://localhost:8000/upload \
        -F "files=@data/essays/ace.txt"

Send multiple files at once:

    $ curl -X POST http://localhost:8000/upload \
        -H "Content-Type: multipart/form-data" \
        -F "files=@data/essays/ace.txt" \
        -F "files=@data/essays/top.txt"


### CLI

Run the CLI:

    $ cd ./backend 
    $ python run.py "YOUR QUERY HERE"

Run the FastAPI backend (port 8000):

    $ cd ./backend 
    $ uvicorn main:app --reload


## Testing

Use pytest with to run tests in `./backend/test_main.py`:

    $ cd ./backend
    $ python -m pytest -v

For a specific test:

    $ python -m pytest -v test_main.py::test_step0 

For some reason pytest has weird behavior with relative/absolute imports, which prevents you from running `pytest` directly, but the above should be fine.


## Misc

### Pinecone

https://docs.pinecone.io/docs/quickstart

    $ curl -i https://controller.us-west1-gcp.pinecone.io/actions/whoami -H 'Api-Key: MY_KEY'

### MongoDB

CLI (after adding your IP address and creating a user):

    $ brew install mongosh
    $ mongosh "mongodb+srv://cluster0.hlqhjo4.mongodb.net/myFirstDatabase" --apiVersion 1 --username nsbradford

