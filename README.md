# SemanticSearch

Minimal RAG (Retrieval Augmented Generation) website with Pinecone, FastAPI, NextJS, MongoDB


## Install

You might want to use `pyenv` to create a virtualenv in which to install Python dependencies:

    $ pyenv virtualenv 3.10.1 myenvname
    $ pyenv activate myenvname
    (myenvname) $ pip install -r requirements.txt

Assuming you have Node/npm (perhaps with [nvm](https://github.com/nvm-sh/nvm)), simply clone this repo, and then from the `./ui` folder (with `package.json` in it) install dependencies:

    $ cd ./ui
    $ npm install 


## Run

### Web App

Start the server (port 8000):

    $ cd ./backend
    $ uvicorn main:app --reload

Now you're ready to run the server locally (port 3000) from within `./ui`:

    $ cd ./ui
    $ npm run dev

And just head over to `http://localhost:3000` to demo!


### Test APIs with Curl

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

Load everything in ./data/essays (WARNING: this will take ~10 minutes)

    $ curl -X POST http://localhost:8000/reupload_all


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

## Future Work
This is built with FastAPI, NextJS, MongoDB, and Pinecone.

Next:
- hyperlink to raw document
- oneclick "explore more", combine found vector
- threshold warning color result likely quality
- NER

