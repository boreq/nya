"""
    Application must be created somewhere outside of the main package to avoid
    doing that every time a package is imported since it is preferred to use
    a custom instance of an app in certain situations, for example in unit
    tests.  To serve this application simply pass an app object created here to
    your WSGI server.
"""


from nya import create_app
app = create_app()
