# importing packages
from flask import Flask, request, Response, stream_template
import openai
import os

# get api key and declare flask app
# remember to set the api key
openai.api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

# define index route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        messages = request.json['messages']
        
        def event_stream():
            # completion
            stream = openai.chat.completions.create(
                model="gpt-3.5-turbo", # gpt-4 or other models also work
                messages=messages,
                stream=True
            )
            # stream chunks of data as they generate
            for chunk in stream:
                text = chunk.choices[0].delta.content or ""
                if len(text): 
                    yield text
        # sends stream of data to client
        return Response(event_stream(), mimetype='text/event-stream')
    else:
        # renders index.html as a STREAM TEMPLATE (not a normal render_template)
        return stream_template('index.html')

# run app
if __name__ == '__main__':
    app.run(debug=True)