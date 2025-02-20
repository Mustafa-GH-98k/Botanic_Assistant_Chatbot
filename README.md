# Chatbot API
This project is a chatbot application that provides two main endpoints: `/chat` for interacting with the chatbot and `/generateImage` for generating images. 

The API requires authentication with an API key.

Made using Python and Flask

# Table of contents
                                            
1. [Chatbot API](#chatbot-api)
2. [Running the app](#running-the-app)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
3. [Interacting with the app](#interacting-with-the-app)
   - [Postman](#postman)
    - [Swagger](#swagger)
4. [API Documentation](#api-documentation)
- [POST /chatbot/chat](#post-chatbotchat)
- [POST /chatbot/generateImage](#post-chatbotgenerateimage)
- [GET /chatbot/generateApiKey](#get-chatbotgenerateapikey)
- [GET /](#get)
5. [Tests](#tests)
- [Test scenarios covered](#test-scenarios-covered)
6. [Approach](#approach)
- [TimeLine](#timeline)
- [Technologies](#technologies)
- [Addon Decisions](#addon-decisions)
7. [Time taken](#time-taken)
- [Day 1](#day-1)
- [Day 2](#day-2)
8. [Bonus](#bonus)
- [Features](#features)
- [Requirements](#requirements)
- [Hosted Version](#hosted-verison)


# Running the app

### Prerequisites

Make sure you have the following installed:

- Python 
- Pip 


### Installation


1. Clone the repository:
   ```bash
        git clone https://github.com/your-username/chatbot-api.git
        cd chatbot-api
   ```

2. **Create a Python virtual environment:**
   ```bash
        python -m venv venv
   ```

   - **For Windows:**
     ```bash
         venv\Scripts\activate
     ```
   - **For macOS/Linux:**
     ```bash
        source venv/bin/activate
     ```

3. Install the required dependencies:
   ```bash
        pip install -r requirements.txt
   ```

4. Set up environment 'OPENAI_API_KEY' inside an `.env` file:
    ```bash
        OPENAI_API_KEY="your-openai-key"
    ```

5. Start the application
   ```bash
        python run.py
    ```

6. [Bonus Addon Environment Variables](#requirements)


# Interacting with the app

### Postman
You can use this [postman collection](https://github.com/user-attachments/files/18877701/itxi_flask_assigment.postman_collection.json) to interact with the app

### Swagger
In the browser navigate to http://127.0.0.1:5000/apidocs/


# API Documentation 

### POST /chatbot/chat
Send a message to the chatbot and receive a response.

#### Request:

    POST /chatbot/chat 
    Content-Type: application/json 
    x-api-key: your-api-key 
    Body: { "content": "Hello, chatbot!" }

#### Response:
    {
        "status_code": 200,
        "success": true,
        "response": {
            "message": "Hello! How can I assist you today?"
        },
        "error_messages": null,
        "version": "0.1.0"
    }

### POST /chatbot/generateImage 
Generate an image based on a prompt.
`imageType` header can be : `image` , `base64`

- With `base64` : 
    ##### Request:
        POST /chatbot/generateImage
        Content-Type: application/json
        x-api-key: your-api-key
        imageType: base64
        Body: 
        {
            "content": "A futuristic city at sunset"
        }

    ##### Response:
        {
            "status_code": 200,
            "success": true,
            "response": {
                "base64": "base64_image"
            },
            "error_messages": null,
            "version": "0.1.0"
        }

- With `image` : 
    ##### Request:
        POST /chatbot/generateImage
        Content-Type: application/json
        x-api-key: your-api-key
        imageType: image
        Body: 
        {
            "content": "A futuristic city at sunset"
        }

    ##### Response:
        generated image file

### GET /chatbot/generateApiKey
Returns a valid `x-api-key` to use
This endpoint is strictly for testing , it uses temporary volatile storage to store the keys 

#### Request:
    GET /chatbot/generateApiKey 

#### Response:
    {
        "api_key": "valid-api-key"
    }

### GET /
Returns `Hello World!`
Ensures that the API is healthy 

#### Request:
    GET / 

#### Response:
    `Hello, World!`
    


# Tests 
Pytest was used to conduct the testing 

### Test scenarios covered 

##### /chatbot/chat :
- With a valid API key and valid request
- Without an API key
- With an invalid API key
- With an invalid JSON body
- When the chatbot service fails

##### /chatbot/generateImage :
- With a valid API key and base64 image type
- With a valid API key and image type
- With an invalid image type
- With a missing `imageType` header
- With an invalid API key
- With schema validation errors
- With an unexpected error

##### /chatbot/generateApiKey :
- Test for successful API key generation

##### / :
- Test for a successful "Hello, World!" response


# Approach
### TimeLine
Use `git --no-pager log --oneline` / github to follow with the commits 
- `Requirements` : read , analysed , understood and took notes regardingn the requiremetns + [some assumptions](#addon-decisions)
- `Architecture :` created a branch `folder_structure_sample` to make a sample mini flask app that samples the chosen architecture
-  `Architecture initialization` : initialized the API's SOA based architecture with the routes endpoints setup 
- `Service Layer` : implemented the bussiness logic + custom exceptions for service-controller communication
- `Controller` : Implemented the controller for the endpoints 
- `Body validation` : used marshmellow in controllers for valdation
- `Generic API Response Model` ; added and used the generic API model for an consistent API response everytime
- `Header validatoin` : made a custom header validator decorator to validate the image header in the generateImage endpoint
- `Authentication` : made a custom `x-api-key` authentication header validation decorator + generateApiKey endpoint to generate random keys
- `Testing` : created tests for various scenarios for each endpoint
- `Swagger Docs Testing` : tested swagger-flask integration on the other branch using flask-restx , flast-restplus and flagger
- `Documentation` : configured Swagger documentation for flask for each endpoint and their metadata

### Technologies
- `Service Layer` : Langchain , OpenAi
- `Validation` : Marshmellow
- `Documentation` ; Swagger with Flagger
- `API` : Flask 

### Addon Decisions
- `/ Endpoints ` : kept the hello world without authentication as it's for checking the api health
- `/generateApiKey Endpoint` : created to provide api keys with no restrictions using GET as there's user registration is out of scope  ONLY FOR TESTING , keys are not saved to a persistent storage  
- `Generic response instead of specified response` : made a generic response as it's a best practice


# Time taken
Taking a look at the commit history using 'git --no-pager log' / github
- Day 1 : 14/2/2024

| **Action** | **Message**                  | **Time**  | **Commit Hash**                                |
|------------|------------------------------|-----------|-----------------------------------------------|
| **Start**  | PAUSE: finished chat tests   | 1:26 PM   | 522a4959d57001fa13457d06b07f4e80acef2e37      |
| **End**    | Initial commit               | 3:01 AM   | f26669d4c9d62d2628148a2740bc1d797ea59f13      |


- Day 2 : 15/2/2024

| **Action** | **Message**                  | **Time**  | **Commit Hash**                                  |
|------------|------------------------------|-----------|-------------------------------------------------|
| **Start**  | RESUME: generateImage tests   | 10:51 AM  | b0d6ee90a947ec5c1e86cdce5bf0797ed34cf155        |
| **End**    | swagger docs complete         | 2:50 PM   | c46d562ae80d3c62a0d190b68156b14601d361f0        |

# Bonus
### Features
1. Message History : langchain , firestore
2. Image Gen & Analysis : langchain , langsmith, agents (tried bind_tools , initialize_agent , create_react_agent + StructuredTool)
3. Generated Image Storage : tried imgbb , imgur ,  supabase 
4. Image Generation Awareness : langchain , langsmith , ChatPromptTemplate
5. Chatbot UI : streamlit
6. Image analysis optimization : pillow
7. Deployment : gcloud , render , gunicorn 

### Requirements
If you want to just try only the api with no bonus features go to commit cd36081d21de6cc6e6fb32562eff280ee926d6ae and just run the app.py as specified before

To use the bonus features locally , you need to setup additional `services` & add more `environment variables` to the `.env` file pr you can try them on the [hosted version](#hosted-verison)

- Flask orign that the front end will use , locally the value would be the local host url
     ```bash
        FLASK_ORIGIN ="http://localhost:5000"
    ```
- Generate a Gcloud service acount json key file and set the variable to the json file path , with the firebase project id and firestore collection name 
    ```bash
        GOOGLE_APPLICATION_CREDENTIALS="./gcloud.json"
        FIREBASE_PROJECT_ID = "project_id"
        FIREBASE_COLLECTION_NAME = "chat_history"
    ```
- Create a supabase storage public bucker , add an allow-create policy for the service and set these environment vartiables 
    ```bash
        SUPABASE_URL= "url"
        SUPABASE_ANON_KEY= "anon_key"

    ```
- OPTIONAL : for monnitoring the llm reasoning you can set langsmith environment varibales
    ```bash
        LANGSMITH_TRACING=true
        LANGSMITH_ENDPOINT="endpoint"
        LANGSMITH_API_KEY="api_key"
        LANGSMITH_PROJECT="project_name"

    ```

### Hosted verison
- [Frontend](https://frontend-itxi-flask-chatbot-assignment.onrender.com)
- [Backend](https://backend-itxi-flask-chatbot-assignment.onrender.com)