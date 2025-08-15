# In file: my-firebase-app/functions/main.py

# Import the necessary libraries
from firebase_functions import https_fn
from start_server import app
# Initialize the Flask app



# This is the entry point that Firebase will call
@https_fn.on_request()
def my_api_function(req: https_fn.Request) -> https_fn.Response:
    """The main entry point for the Firebase Function."""
    # The 'with' statement is crucial for Flask to work correctly
    # in the Firebase Functions environment.
    with app.request_context(req.environ):
        
        return app.full_dispatch_request()