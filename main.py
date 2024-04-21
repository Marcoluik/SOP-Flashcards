from website import create_app
#instance af app laves
app = create_app()
##opstart af program
if __name__ == "__main__":
    app.run(debug=True)
    