"""Minimal Flask stub for tests."""
from typing import Callable, Dict, Any


class Response:
    """Simplified response object."""

    def __init__(self, data: Any, status_code: int = 200) -> None:
        self.data = data
        self.status_code = status_code

    def get_json(self) -> Any:
        return self.data


class Blueprint:
    def __init__(self, name: str, import_name: str) -> None:
        self.name = name
        self.import_name = import_name
        self.routes: Dict[str, Callable] = {}

    def route(self, path: str, methods=None) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes[path] = func
            return func

        return decorator


class Flask:
    def __init__(self, import_name: str, template_folder: str | None = None) -> None:
        self.import_name = import_name
        self.template_folder = template_folder
        self.routes: Dict[str, Callable] = {}

    def route(self, path: str, methods=None) -> Callable:
        def decorator(func: Callable) -> Callable:
            self.routes[path] = func
            return func

        return decorator

    def register_blueprint(self, bp: Blueprint) -> None:
        self.routes.update(bp.routes)

    def test_client(self) -> "_Client":
        app = self

        class _Client:
            def get(self, path: str) -> Response:
                view = app.routes.get(path)
                if view is None:
                    return Response(None, 404)
                result = view()
                if isinstance(result, Response):
                    return result
                return Response(result, 200)

        return _Client()

    def run(self, debug: bool = False) -> None:
        """Mimic ``Flask.run`` without starting a server."""
        print(f"Stub Flask app running (debug={debug})")


def jsonify(data: Any) -> Any:
    return data


def render_template(template_name: str) -> str:
    return f"Rendered {template_name}"
