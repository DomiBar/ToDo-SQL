from views import app

app.config['SECRET_KEY'] = 'nafiwefnp4636'


if __name__ == "__main__":
    app.config['ENV'] = 'development'
    app.config['JSON_AS_ASCII'] = False
    app.run(debug=False, load_dotenv=True)
