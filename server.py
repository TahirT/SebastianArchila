from flask import Flask, render_template, request
from waitress import serve
from openai import OpenAI

client = OpenAI()

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index ():
    return render_template('index.html')

@app.route('/answer', methods=["GET", "POST"])

def answer():

    data = request.get_json()
    message = data["message"]

    def generate():
        stream = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                "role": "system",
                "content": "Generate just a boolean query and nothing more, no descriptions",
            },
                {
                "role": "user",
                "content":message
                }],
            stream = True
        )

        for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                yield(chunk.choices[0].delta.content)
    
    return generate(), {"Content-Type": "text/plain"}


if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8000)