from pathlib import Path
import sys


project_dir = Path(__file__).resolve().parent / "Pet_Care"
sys.path.insert(0, str(project_dir))

from app import create_app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)