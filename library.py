#Importing all the packages and modules that we might need

from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import codecs
import base64


#API and app initialisation 

app = Flask(__name__)
api = Api(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books_database.db"
db = SQLAlchemy(app)

#Database Model Design

class BookModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cover_img = db.Column(db.Binary, unique=True, nullable=False)
    num_cop = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Book_ID = {id}, Title = {title}, Author = {author}, Cover_Image = {cover_img}, Availability = {num_cop})"

#Creating an instance of the database

db.create_all()

#Book request parsing arguments - PUT

book_put_args = reqparse.RequestParser()

book_put_args.add_argument(
    "title", type=str, help="A book title is required", required=True
)
book_put_args.add_argument(
    "author", type=str, help="An author is required", required=True
)
book_put_args.add_argument(
    "cover_img", type=str, help="A cover image is required", required=True
)
book_put_args.add_argument(
    "num_cop", type=int, help="Number of copies available is required", required=True
)

#Defining the resource fields for marshal with decorator for extracting data from JSON 

resource_fields = {
    "id": fields.Integer,
    "title": fields.String,
    "author": fields.String,
    "cover_img": fields.String,
    "num_cop": fields.Integer,
}

#getBookDetails Class

class getBookDetails(Resource):
    @marshal_with(resource_fields)
    def get(self, book_id):
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Could not find any book with that ID!")
        
        return result

#addNewBook Class

class addNewBook(Resource):
    @marshal_with(resource_fields)
    def put(self, book_id):
        args = book_put_args.parse_args()
        result = BookModel.query.filter_by(id=book_id).first()
        if result:
            abort(409, message="This Book ID is already taken, update the book count!")
        byteData = codecs.encode(args["cover_img"], "UTF-8")
        imgData = base64.decodebytes(byteData)
        book = BookModel(
            id=book_id,
            title=args["title"],
            author=args["author"],
            cover_img=imgData,
            num_cop=args["num_cop"],
        )
        db.session.add(book)
        db.session.commit()
        return book, 201

#updateBookCount Class

class updateBookCount(Resource):
    @marshal_with(resource_fields)
    def patch(self, book_id, changeType):
        result = BookModel.query.filter_by(id=book_id).first()
        if not result:
            abort(404, message="Could not find any book with that ID, register this book!")
        temp = result.num_cop
        if changeType == 0:
            temp = temp - 1
        else:
            temp = temp + 1
        result.num_cop = temp
        db.session.commit()

#Adding resources to all the endpoints

api.add_resource(getBookDetails, "/book/id=<int:book_id>")
api.add_resource(addNewBook, "/registerBook/new_id=<int:book_id>")
api.add_resource(updateBookCount, "/updateCount/id=<int:book_id>/inc=<int:changeType>")

#Enabling debug

if __name__ == "__main__":
    app.run(debug=True)







