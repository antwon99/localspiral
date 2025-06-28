"""Minimal Flask stub for tests."""
from typing import Callable, Dict, Any
from urllib.parse import parse_qs, urlparse


class _Request:
    def __init__(self) -> None:
        self.args: Dict[str, Any] = {}


session: Dict[str, Any] = {}


request = _Request()


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
                parsed = urlparse(path)
                view = app.routes.get(parsed.path)
                if view is None:
                    return Response(None, 404)
                args = {k: v[0] for k, v in parse_qs(parsed.query).items()}
                request.args = args
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
