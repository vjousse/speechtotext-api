from app.core.init import create_app

app = create_app()

for route in app.routes:
    if hasattr(route, "methods"):
        print(f"{route.path} {route.methods}: {route.name}")
    else:
        print(f"{route.path}: {route.name}")
