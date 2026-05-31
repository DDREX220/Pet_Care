import importlib.util
import sys
from pathlib import Path


def load_app():
    package_dir = Path(__file__).resolve().parent / "app"
    spec = importlib.util.spec_from_file_location(
        "pet_care_app",
        package_dir / "__init__.py",
        submodule_search_locations=[str(package_dir)],
    )

    if spec is None or spec.loader is None:
        raise RuntimeError("Unable to load the Flask application package.")

    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module.create_app()


app = load_app()


if __name__ == "__main__":
    app.run(debug=True)

