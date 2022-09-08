from Pizza import app, db
from Pizza.models import pizza, customer, c_order
from flask import Flask, render_template, request, flash, session, redirect, g



@app.route('/', methods=["GET","Post"])
def home():

    return render_template("home.html")

@app.route('/user', methods=["GET","Post"])
def user():  #this should work as both a login and register
    if request.method == "POST":
        user = request.form.get('username')
        on = True #when the user is tagging the name, we make the user inactive.
        name = customer.query.filter_by(name=user).first()
        
        if name:
            print (name.active)
            if name.active == True:
                flash ("use a diffrent username, this one is being used")
                print("sssss")
                return render_template("home.html")
            else:
                flash ("username confirmed, coining name. logged in correctly, ")
                session["Current_Customer"] = user
                ustomer = request.form['username']
                update = customer.query.filter_by(name=user).first()
                print(update.id)
                print("user id")
                update.name = ustomer
                update.active = True

                db.session.commit()
                results = pizza.query.all()

                return render_template("menu.html", results = results)
        elif name == None:
            new_customer = customer()
            new_customer.name = user
            new_customer.active = on

            session["Current_Customer"] = user
            print(user)
            db.session.add(new_customer)
            print (new_customer)
            db.session.commit()

            results = pizza.query.all()
            return render_template("menu.html", results = results)
        
        else:
            flash("server error occured, please try again later")



@app.route('/menu', methods=["GET","Post"])
def menu():
    if request.method == "POST":
        print ("hello")
        results = pizza.query.all()
        print (results)
        return render_template("menu.html", results = results)


@app.route('/cart', methods=["GET", "Post"])
def cart():
    if request.method == "POST":
        print ("cart")
        user = session["Current_Customer"]
        name = customer.query.filter_by(name=user).first()

        user_id = name.id
        print (user_id)
        print ("user id")
        id = request.form.get("pizzaid")
        print (id)
        price = request.form.get("pizzaprice")

        pizz = c_order()
        pizz.pizza_id = id
        pizz.customer_id = user_id
        pizz.pizza_price = price

        db.session.add(pizz)
        db.session.commit()

        results = pizza.query.all()
        flash("Added Pizza")
        print (results)
        return render_template("menu.html", results = results)


@app.route('/checkout', methods=["Post"])
def checkout():
    if request.method == "POST":
        print("checkout")
        user = session["Current_Customer"]
        name = customer.query.filter_by(name=user).first()
        user_id = name.id
        print (user_id)

        check = c_order.query.filter_by(customer_id=user_id).all()
        if check == None:
            flash("you have nothing in your cart")
            return render_template("fail.html")

        else:
            total = 0
            for item in check:
                total += item.pizza_price
            print(total)

            return render_template("checkout.html", total = total)
            
        return render_template("fail.html")


@app.route('/admin', methods=["GET","Post"])
def admin():
    if request.method == "POST":
        
        
        return render_template("fail.html")


@app.route('/fail')
def fail():
    flash ("how the hell did you get here? ")
    return render_template("fail.html")




@app.route('/logout')
def logout():
    # remove the username from the session if it's there

    Current_Customer = session["Current_Customer"] 
    print (Current_Customer)
    print ("current customer")
    session.pop('Current_Customer', None)

    update = customer.query.filter_by(name=Current_Customer).first()
    user_id = update.id
    update.active = False
    
    db.session.commit()
    check = c_order.query.filter_by(customer_id=user_id).delete()
    db.session.commit()

    flash("asasad")
    return render_template("fail.html")
        

