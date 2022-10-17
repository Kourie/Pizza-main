from Pizza import app, db
from Pizza.models import pizza, customer, c_order
from flask import Flask, render_template, request, flash, session, redirect, g
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/', methods=["GET","Post"])
def home():

    return render_template("home.html")

@app.route('/user', methods=["GET","Post"])
def user():  #this should work as both a login and register
    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')
        print(password)
        encrypted = generate_password_hash(password)  
        print (encrypted)  

        name = customer.query.filter_by(username=user).first()
        
        if name:

            #if username is in database
            print("shit")
            if name.username == user:
                check_password_hash(encrypted, password)


                if check_password_hash(name.password, password) == True:
                    flash("yay")
                    print (name.password)
                    print(encrypted)
                    session["Current_Customer"] = user
                    user_id = name.id
                    check = c_order.query.filter_by(customer_id=user_id).all()
                    results = pizza.query.all()
                    if check == None:
                         flash("you have nothing in your cart")
                    
                    else:

                        total = 0
                        for item in check:
                            total += item.pizza_price
                        print(total)
                    
                    
                    return render_template("menu.html", results = results, total = total, check = check )


                else:
                    flash("nay, wrong username or password")

                    return render_template("fail.html")
                
        elif name == None:
            print("new user")
            new_customer = customer()
            new_customer.username = user
            new_customer.password = encrypted

            session["Current_Customer"] = user
            print(user)
            db.session.add(new_customer)
            db.session.commit()

            results = pizza.query.all()
            
            name = customer.query.filter_by(username=user).first()
            user_id = name.id

            check = c_order.query.filter_by(customer_id=user_id).all()
            if check == None:
                flash("you have nothing in your cart")
            
            else:

                total = 0
                for item in check:
                    total += item.pizza_price
                print(total)
            return render_template("menu.html", results = results, total = total, check = check )
        
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
        name = customer.query.filter_by(username=user).first()

        user_id = name.id
        print (user_id)
        print ("user id")
        id = request.form.get("pizzaid")
        print (id)
        price = request.form.get("pizzaprice")
        pname = request.form.get("pizzaname")

        pizz = c_order()
        pizz.pizza_id = id
        pizz.customer_id = user_id
        pizz.pizza_price = price
        pizz.pizza_name = pname

        db.session.add(pizz)
        db.session.commit()

        results = pizza.query.all()
        flash("Added Pizza")
        print (results)

        check = c_order.query.filter_by(customer_id=user_id).all()
        if check == None:
            flash("you have nothing in your cart")
        else:

            total = 0
            for item in check:
                total += item.pizza_price
            print(total)

        return render_template("menu.html", results = results, total = total, check = check)


@app.route('/checkout', methods=["Post"])
def checkout():
    if request.method == "POST":
        print("checkout")
        user = session["Current_Customer"]
        name = customer.query.filter_by(username=user).first()
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

            return render_template("checkout.html", total = total, check = check)
            
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

    username = session["Current_Customer"] 
    print (username)
    print ("current customer")
    session.pop('Current_Customer', None)
    name = customer.query.filter_by(username=username).first()
    user_id = name.id
    print(user_id)
    
    check = c_order.query.filter_by(customer_id=user_id).all()
    for item in check:
        print(item.pizza_name)

    pizz = c_order.query.filter_by(customer_id=user_id).delete()

    db.session.commit()

    flash("asasad")
    return render_template("fail.html")
        

