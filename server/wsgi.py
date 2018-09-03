from server import create_app


def wsgi():
    app = create_app()
    app.run()
