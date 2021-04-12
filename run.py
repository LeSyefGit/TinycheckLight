from tinycheckweb import create_app

app = create_app()

def return_app():
    return app

if __name__=='__main__':
    app.run(debug=True)