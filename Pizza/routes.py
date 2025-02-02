# oooo, look, imports
from Pizza import app, db
from Pizza.models import pizza, customer, c_order  # databases
from flask import Flask, render_template, request, flash, session, redirect, g
# this is the hashing and stuff imports
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=["GET", "Post"])
def home():

    return render_template("home.html")

# ah yes, the s#### login system of mine


@app.route('/user', methods=["GET", "Post"])
def user():  # this should work as both a login and register
    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')
        encrypted = generate_password_hash(password)

        name = customer.query.filter_by(username=user).first()

        if name:
            check_password_hash(encrypted, password)

            if check_password_hash(name.password, password) == True:
                session["Current_Customer"] = user
                user_id = name.id
                session["Customer_ID"] = name.id
                check = c_order.query.filter_by(customer_id=user_id).all()
                results = pizza.query.all()
                if check == None:
                    flash("you have nothing in your cart")

                else:
                    # over here is a small loop for the stuff in the user's cart, since if they are reaccruing and didn't place an order, they might still have something inside of it
                    ttotal = 0
                    for item in check:
                        ttotal += item.pizza_price
                    total = round(ttotal, 2)
            

                return render_template("menu.html", results=results, total=total, check=check)

            else:
                flash("error: wrong username or password")
                # this means that the user inputed the wrong username or password,
                # if password and user was true, it would pass above, but it would fail upon the password checker, dumping the user here
                return render_template("fail.html")

        elif name == None:
            # registering user, beep boop baap
            new_customer = customer()  # we make a new class for the user
            new_customer.username = user
            new_customer.password = encrypted

            session["Current_Customer"] = user
            db.session.add(new_customer)  # and add the user
            db.session.commit()

            results = pizza.query.all()  # get all results for the menu (get used to this)

            name = customer.query.filter_by(username=user).first()
            user_id = name.id
            session["Customer_ID"] = name.id

            check = c_order.query.filter_by(customer_id=user_id).all()
            if check == None:
                flash("you have nothing in your cart")

            else:

                ttotal = 0
                for item in check:
                    ttotal += item.pizza_price
                total = round(ttotal, 2)  # oh, and the fun rounding thing

            return render_template("menu.html", results=results, total=total, check=check)

        else:
            flash("server error occured, please try again later")


@app.route('/clear', methods=["GET", "Post"])
def clear():
    if request.method == "POST":
        # if the user has made a mistake, they can clear they're order
        user = session["Current_Customer"]
        user_id = session["Customer_ID"]
        pizz = c_order.query.filter_by(customer_id=user_id).delete()
        db.session.commit()
        results = pizza.query.all()
        total = ("0")
        return render_template("menu.html", results=results, total=total)


@app.route('/menu', methods=["GET", "Post"])
def menu():
    results = pizza.query.all()
    if "Customer_ID" in session:
        user_id = session["Customer_ID"]
        check = c_order.query.filter_by(customer_id=user_id).all()
        if check == None:
            flash("you have nothing in your cart")
        else:

            ttotal = 0
            for item in check:
                ttotal += item.pizza_price
            total = round(ttotal, 2)
            return render_template("menu.html", results=results, total=total, check=check)
    else:
        flash("you must be logged in!")
        return render_template("fail.html")


@app.route('/cart', methods=["GET", "Post"])
def cart():
    if request.method == "POST":
        if "Customer_ID" in session:
            user = session["Current_Customer"]
            user_id = session["Customer_ID"]
            id = request.form.get("pizzaid")
            price = request.form.get("pizzaprice")
            pname = request.form.get("pizzaname")

            # here's a fun little thing, I made hidden tags/names to be inputted by the user when they pick a Pizza, it's really cool
            # Wonder where I learnt it from.

            pizz = c_order()
            pizz.pizza_id = id
            pizz.customer_id = user_id
            pizz.pizza_price = price
            pizz.pizza_name = pname
            # and here we add the Pizza, carefully named pizz since I didn't want to call it Pizza, in fear it might break since it would have the same name as the module
            db.session.add(pizz)
            db.session.commit()

            results = pizza.query.all()
            flash("Added " + pname)  # just a little user feedback

            check = c_order.query.filter_by(customer_id=user_id).all()
            if check == None:
                flash("you have nothing in your cart")
            else:

                ttotal = 0
                for item in check:
                    ttotal += item.pizza_price
                total = round(ttotal, 2)
                return render_template("menu.html", results=results, total=total, check=check)

        else:
            flash("you must be logged in!")
            return render_template("fail.html")


@app.route('/checkout', methods=["Post"])
def checkout():
    if request.method == "POST":
        # over here, if you check the menu, clear and checkout are in the same form, but inputting diffrent textlines
        # this is because I wanted for them to be beside each other, so it looks neater. =)
        if "Customer_ID" in session:
            if request.form.get("clear") == ("clear"):
                # so if the request form is clear, go to the redirect function
                return redirect("/clear")
            else:
                # if not, then it must be the checkout button!!!
                user = session["Current_Customer"]
                user_id = session["Customer_ID"]

                check = c_order.query.filter_by(customer_id=user_id).all()
                if check == None:
                    # now put something in!
                    flash("you have nothing in your cart")
                    return render_template("fail.html")

                else:
                    ttotal = 0
                    for item in check:
                        ttotal += item.pizza_price
                    total = round(ttotal, 2)

                    return render_template("checkout.html", total=total, check=check)
        else:
            flash("Error: why are you not logged in?")

        return render_template("fail.html")



@app.route('/fail')
def fail():
    flash("how the hell did you get here? ")
    return render_template("fail.html")


@app.route('/orderplaced')
def orderplaced():
    if "Customer_ID" in session:
        username = session["Current_Customer"]
        user_id = session["Customer_ID"]

        pizz = c_order.query.filter_by(customer_id=user_id).delete()

        # and laslty, pop the customer ID
        db.session.commit()
        return render_template("orderplaced.html")
    else:
        flash("you must be logged in!")
    
        return render_template("fail.html")


@app.route('/logout')
def logout():
    session.pop('Current_Customer', None)
    session.pop('Customer_ID', None)
    # remove the username from the session if it's there
    return redirect("/")
    # and finally return Home
