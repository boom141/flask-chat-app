from webApplication import create_app

app, sio = create_app()

@app.route('/test')
def foo():
    return " TESTING PAGE: FLASK-CHAT APP "

if __name__ == '__main__':
    sio.run(app, debug=True)
