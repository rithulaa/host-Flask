from flask import Flask, render_template_string, request
from gpt4all import GPT4All

app = Flask(__name__)

# Initialize the GPT-4All model once during application startup
MODEL_PATH = "Meta-Llama-3.1-8B-Instruct-128k-Q4_0.gguf"  # Provide the correct path to the model
try:
    gpt4all_model = GPT4All(MODEL_PATH)
except Exception as e:
    gpt4all_model = None
    print(f"Failed to load GPT-4All model. Error: {e}")


@app.route("/", methods=["GET", "POST"])
def chat():
    """
    Handles GET and POST requests for the chat interface.
    """
    result_message = ""  # Store GPT-4All's response
    error_message = ""  # Store error messages

    if request.method == "POST":
        # Retrieve user input from the form
        user_input = request.form.get("text_input", "").strip()

        if user_input:
            if gpt4all_model:
                try:
                    # Use GPT-4All to generate a response
                    with gpt4all_model.chat_session() as session:
                        result_message = session.generate(prompt=user_input, max_tokens=1024)
                except Exception as e:
                    error_message = f"An error occurred while processing your request: {e}"
            else:
                error_message = "GPT-4All model failed to initialize. Please check the model path or configuration."
        else:
            error_message = "Please enter some input before submitting."

        # Render the HTML template with the result and error messages
    return render_template_string(
    '''
    <html>
        <head>
            <title>GPT-4All Chat</title>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css" rel="stylesheet">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 20px;
                    background-color: #f4f4f9;
                }
                h1 {
                    text-align: center;
                    color: #333;
                }
                .input-area {
                    margin-top: 20px;
                    padding: 20px;
                    background-color: #f9f9f9;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    max-width: 600px;
                    box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.1);
                    margin-left: auto;
                    margin-right: auto;
                    position: relative;
                    display: flex;
                    align-items: center;
                }
                .input-area i {
                    font-size: 24px;
                    color: #333;
                    margin-right: 10px;
                }
                textarea {
                    width: 100%;
                    height: 150px;
                    padding: 40px;  /* Increased padding to fill up more space */
                    border: 1px solid #ccc;
                    border-radius: 4px;
                    font-size: 14px;
                    resize: vertical;
                    box-shadow: inset 0 1px 3px rgba(0, 0, 0, 0.1);
                    margin-bottom: 20px; /* Space between textarea and form submission */
                    background-color: #fff;  /* Added a white background to the textarea */
                    box-sizing: border-box;  /* Ensures padding is included in width/height calculation */
                }
                .response-area {
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #e9ecef;
                    border: 1px solid #ddd;
                    border-radius: 4px;
                    display: flex;
                    align-items: center;
                }
                .response-area i {
                    font-size: 24px;
                    color: #333;
                    margin-right: 10px;
                }
                .response {
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #d4edda;
                    border: 1px solid #c3e6cb;
                    border-radius: 4px;
                    color: #155724;
                }
                .error {
                    margin-top: 20px;
                    padding: 10px;
                    background-color: #fee;
                    border: 1px solid #fcc;
                    border-radius: 4px;
                    color: red;
                }
            </style>
        </head>
        <body>
            <h1>GPT-4All Chat Interface</h1>
            <div class="input-area">
                <!-- Person Icon for Input -->
                <i class="fas fa-user"></i>
                <form method="POST" onsubmit="return handleSubmit(event)">
                    <textarea name="text_input" placeholder="Enter your text here (you can paste paragraphs)" id="text_input"></textarea>
                </form>
            </div>
            {% if result_message %}
                <div class="response-area">
                    <!-- Computer Icon for Response -->
                    <i class="fas fa-laptop"></i>
                    <div class="response">
                        <h2>Response:</h2>
                        <p>{{ result_message }}</p>
                    </div>
                </div>
            {% endif %}
            {% if error_message %}
                <div class="error">
                    <p>{{ error_message }}</p>
                </div>
            {% endif %}
            <script>
                // Function to handle form submission when Enter key is pressed
                document.getElementById('text_input').addEventListener('keydown', function(event) {
                    if (event.key === 'Enter' && !event.shiftKey) {  // Check if Enter key is pressed (without Shift)
                        event.preventDefault();  // Prevent new line from being added
                        document.forms[0].submit();  // Submit the form
                    }
                });
            </script>
        </body>
    </html>
    ''',
    result_message=result_message,
    error_message=error_message,
)

# Main driver function
if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("localhost", 10000, app)
