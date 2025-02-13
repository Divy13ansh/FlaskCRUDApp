from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
import os 

basedir=os.path.abspath(os.path.dirname(__file__))

app=Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///"+os.path.join(basedir,"app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False

db=SQLAlchemy(app)

class Product(db.Model):

    __tabelename__="product"

    productid=db.Column(db.Integer(),primary_key=True)
    name=db.Column(db.String(100),nullable=False)
    price=db.Column(db.Integer())
    quantity=db.Column(db.Integer())
    category=db.Column(db.String(100))

    def _reper_(self):
        return f"ProductID:{self.productid} Name:{self.name} Price:{self.price} Quantity:{self.quantity} category:{self.category}"
    
with app.app_context():
    db.create_all()

@app.route("/")
def home ():
    return render_template("index.html")

@app.route("/product" ,methods=["GET","POST"])
def product():
    
    if request.method=="POST":
        name= request.form.get("name")
        price= request.form.get("price")
        quantity= request.form.get("quantity")
        category= request.form.get("category")

        product = Product(name=name, price=price, quantity=quantity, category=category)
        db.session.add(product)
        db.session.commit()

    products=Product.query.all()
    return render_template ("product.html", products=products)

@app.route("/delete/<int:id>")
def delete(id):
    product=db.session.get(Product,id)
    db.session.delete(product)
    db.session.commit()
    return redirect(url_for("product"))

@app.route("/update/<int:id>")
def update(id):
    product = db.session.get(Product, id)
    if request.method == "POST":
        name = request.form.get("name")
        price = request.form.get("price")
        quantity = request.form.get("quantity")
        category = request.form.get("category")


        product.name = name
        product.price = price
        product.quantity = quantity
        product.category = category


        db.session.add(product)
        db.session.commit()
        return redirect(url_for("product"))


    return render_template("update_product.html", product=product)



if __name__ =="__main__":
    app.run(debug=True)