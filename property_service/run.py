from property_service.app import app


if __name__ == "__main__":
    app.run(debug=True,port=app.config['PORT'])
