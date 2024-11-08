from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import uuid
import json
import boto3

from llama_copilot.chat_llm import generate_llm_response
from llama_copilot.markdown_to_html import markdown_to_html

app = Flask(__name__)
CORS(app)

# initialize S3 client
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"),
)

S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

# In-memory storage for user sessions
user_sessions = {}


@app.route("/api/test", methods=["POST"])
def test():
    data = request.get_json()
    query = data.get("query")
    session_id = data.get("session_id") 

    # construct markdown and convert to html
    markdown_string = f"This is an test api response!\n\n**User input**: {query}\n\n"
    markdown_string += f'This is some example code formatting:\n\n```def some_function():\n\tprint("hello world!")```'
    html_content = markdown_to_html(markdown_string)

    return jsonify({"response": html_content, "session_id": session_id})


@app.route("/api/initialize", methods=["POST"])
def initialize():
    data = request.get_json()
    api_key = data.get("api_key")
    username = data.get("username")
    if not api_key or not username:
        return jsonify({"error": "API key or username not provided"}), 400

    # store API key in environment variable for this session
    os.environ["OPENAI_API_KEY"] = api_key

    session_id = str(uuid.uuid4())

    user_sessions[session_id] = {"username": username, "conversation": []}

    download_user_data_from_s3(username, session_id)

    return jsonify({"message": "Session initialized", "session_id": session_id}), 200


def download_user_data_from_s3(username, session_id):
    try:
        key = f"{username}/conversation.json"
        if not os.path.exists("chat_logs"):
            os.makedirs("chat_logs")
        s3_client.download_file(S3_BUCKET_NAME, key, f"chat_logs/{session_id}.json")
        with open(f"chat_logs/{session_id}.json", "r") as file:
            conversation = json.load(file)
            user_sessions[session_id]["conversation"] = conversation
        print(f"Downloaded previous conversation for user {username}")
    except Exception as e:
        print(f"No previous data for user {username}: {e}")


@app.route("/api/get_response", methods=["POST"])
def get_response():
    data = request.get_json()
    query = data.get("query")
    session_id = data.get("session_id")

    if not query:
        return jsonify({"error": "No query provided"}), 400
    if not session_id or session_id not in user_sessions:
        return jsonify({"error": "Invalid session ID"}), 400

    username = user_sessions[session_id]["username"]

    conversation = user_sessions[session_id]["conversation"]

    response = generate_llm_response(
        query,
        session_id=session_id,
        generation_model="gpt-4o",
        searched_response=None,
    )

    conversation.append({"prompt": query, "response": response})

    log_file_path = os.path.join("chat_logs", f"{session_id}.json")
    with open(log_file_path, "w") as file:
        json.dump(conversation, file)

    upload_user_data_to_s3(username, session_id)

    return jsonify({"response": response, "session_id": session_id})


def upload_user_data_to_s3(username, session_id):
    try:
        key = f"{username}/conversation.json"
        local_file_path = os.path.join("chat_logs", f"{session_id}.json")
        s3_client.upload_file(local_file_path, S3_BUCKET_NAME, key)
        print(f"Uploaded conversation for user {username} to S3")
    except Exception as e:
        print(f"Error uploading data for user {username}: {e}")


if __name__ == "__main__":
    if not os.path.exists("chat_logs"):
        os.makedirs("chat_logs")
    app.run(port=8080, host="0.0.0.0", debug=False)
