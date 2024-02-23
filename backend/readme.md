# e_TA backend

## File sturcture

backend/
├── README.md
├── setup.py
├── env/                        # environment setting
│   ├──
│   ├── requirements.yml        # environment setting for reference
│   └── ...
│
├── eTA/
│   │
│   ├── app.py                  # main file, run this to start server
│   │
│   │
│   ├── controller/
│   │   ├── __init__.py
│   │   └── handleQuery.py       # Getting response from embedding and LLM
│   │
│   └── service/
│       ├── embedding/           # embedding model
│       │   ├── __init__.py
│       │   ├── src/             # data needed for embedding model
│       │   ├── getAnswer.py     # get similar Q&A from database
│       │   └── voc2Doc.py       # model training
│       │
│       └── LLM/                 # LLM API
│            ├── __init__.py
│            ├── gpt.py          # call GPT
│            └── llama2.py       # call llama2
│
│
└── README.md

# Development

## Module Management Strategy

Please adhere to the following guidelines to maintain our MVC architecture:

* **Development Guidelines**:

  * **app.py **: Handles HTTP requests and routes to controllers, return data back to frontend.
  * **controller/ **: Manage business logic and call services.
  * **services/ **: Interact with backend data.
* **Module Management**:

  * Use `pip install -e .` for editable installs.
  * import new module in the project

    ```
    # Make sure there is a __init__.py file in each module directory, so setup.py can scan it and add it into package. 
    # Once correctly configured the, import like this, eTA is the name configured in setup.py
    from eTA.xxx import xxx
    ```
  * Keep a minimal `setup.py` at the project root.

Your cooperation ensures a scalable and maintainable project.

# Devops

## Run conda envirment before run the program

```
conda activate DirRes #Mario's env
```

## Running backend program on the backend(always run)

```
nohup python3 app.py > output.log 2>&1 &
```

## Check the PID of the program occupying the certain port

```
lsof -i :PORT
```
