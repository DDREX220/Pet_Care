# Entry point for the PetCare Flask application
from app import create_app

# Initialize the Flask app using the application factory pattern
app = create_app()

if __name__ == "__main__":
    # Run the development server with debug mode enabled
    # debug=True auto-reloads on code changes and shows detailed error pages
    app.run(debug=True)
