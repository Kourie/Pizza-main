# oooo, look, imports
from Pizza import app, db    
from Pizza.models import pizza, customer, c_order  #databases
from flask import Flask, render_template, request, flash, session, redirect, g
from werkzeug.security import generate_password_hash, check_password_hash  #this is the hashing and stuff imports

@app.route('/', methods=["GET","Post"])
def home():

    return render_template("home.html")

#ah yes, the s#### login system of mine

@app.route('/user', methods=["GET","Post"])
def user():  #this should work as both a login and register
    if request.method == "POST":
        user = request.form.get('username')
        password = request.form.get('password')
        encrypted = generate_password_hash(password)  
        # print (encrypted)  
        # that print statment is debug
        name = customer.query.filter_by(username=user).first()
        
        if name:
            check_password_hash(encrypted, password)

            if check_password_hash(name.password, password) == True:
                print (name.password)
                print(encrypted)
                # I wonder if I should remove these print statments? they were here to verify that both items are encrypted
                session["Current_Customer"] = user
                user_id = name.id
                session["Customer_ID"] = name.id
                print (session["Customer_ID"])
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
                    print(total)
                
                
                return render_template("menu.html", results = results, total = total, check = check )


            else:
                flash("error: wrong username or password")
                # this means that the user inputed the wrong username or password, 
                # if password and user was true, it would pass above, but it would fail upon the password checker, dumping the user here 
                return render_template("fail.html")
                
        elif name == None:
            print("new user") #registering user, beep boop baap
            new_customer = customer() #we make a new class for the user
            new_customer.username = user
            new_customer.password = encrypted

            session["Current_Customer"] = user
            print(user)
            db.session.add(new_customer) #and add the user
            db.session.commit()

            results = pizza.query.all() #get all results for the menu (get used to this)
            
            name = customer.query.filter_by(username=user).first()
            user_id = name.id
            session["Customer_ID"] = name.id
            print (session["Customer_ID"])

            check = c_order.query.filter_by(customer_id=user_id).all()
            if check == None:
                flash("you have nothing in your cart")
            
            else:
                
                ttotal = 0
                for item in check:
                    ttotal += item.pizza_price
                total = round(ttotal, 2) #oh, and the fun rounding thing
                print(total)
            return render_template("menu.html", results = results, total = total, check = check )
        
        else:
            flash("server error occured, please try again later")


@app.route('/clear', methods=["GET", "Post"])
def clear():
    if request.method == "POST":
        # if the user has made a mistake, they can clear they're order
        print("clear")
        user = session["Current_Customer"]
        print (user)
        user_id = session["Customer_ID"] 
        print(user_id)
        print ("clearinnginignig")

        pizz = c_order.query.filter_by(customer_id=user_id).delete()
        db.session.commit()
        results = pizza.query.all()
        total = ("0")
        return render_template("menu.html", results = results, total = total)





@app.route('/cart', methods=["GET", "Post"])
def cart():
    if request.method == "POST":
        print ("cart")
        user = session["Current_Customer"]
        user_id = session["Customer_ID"] 
        print(user_id)
        print ("user id")
        id = request.form.get("pizzaid")
        price = request.form.get("pizzaprice")
        pname = request.form.get("pizzaname")
        print (id)

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
        flash("Added " + pname) #just a little user feedback
        print (results)

        check = c_order.query.filter_by(customer_id=user_id).all()
        if check == None:
            flash("you have nothing in your cart")
        else:

            ttotal = 0
            for item in check:
                ttotal += item.pizza_price
            total = round(ttotal, 2)
            print(total)

        return render_template("menu.html", results = results, total = total, check = check)


@app.route('/checkout', methods=["Post"])
def checkout():
    if request.method == "POST":
        # over here, if you check the menu, clear and checkout are in the same form, but inputting diffrent textlines
        # this is because I wanted for them to be beside each other, so it looks neater. =)

        if request.form.get("clear") == ("clear"):
            # so if the request form is clear, go to the redirect function
            print (request.form.get("clear"))
            return redirect("/clear")
        else:    
            # if not, then it must be the checkout button!!!
            print(request.form.get("checkout"))
            print("crapapidadfweofwifwfb") #I know, right?
            user = session["Current_Customer"]
            user_id = session["Customer_ID"] 
            print(user_id)
            
            check = c_order.query.filter_by(customer_id=user_id).all()
            print ("REEEEEEEEEEEEEEEEEEEEEEEEE") #bro, Dat's Crazyyy!!!
            if check == None:
                flash("you have nothing in your cart") #now put something in!
                return render_template("fail.html")

            else:
                ttotal = 0
                for item in check:
                    ttotal += item.pizza_price
                total = round(ttotal, 2)
                print(total)


                return render_template("checkout.html", total = total, check = check)
                
        return render_template("fail.html")


# @app.route('/admin', methods=["GET","Post"])
# def admin():
#     if request.method == "POST":
        
        
#         return render_template("fail.html")


@app.route('/fail')
def fail():
    flash ("how the hell did you get here? ")
    return render_template("fail.html")



@app.route('/orderplaced')
def orderplaced():
    username = session["Current_Customer"] 
    print (username)
    print ("current customer")
    user_id = session["Customer_ID"] 
    print(user_id)
            
    check = c_order.query.filter_by(customer_id=user_id).all()
    for item in check:
        print(item.pizza_name)

    pizz = c_order.query.filter_by(customer_id=user_id).delete()
    
    # and laslty, pop the customer ID
    db.session.commit()
    return render_template("orderplaced.html")



@app.route('/logout')
def logout():
    session.pop('Current_Customer', None)
    session.pop('Customer_ID', None)
    # remove the username from the session if it's there
    return redirect("/")
        #and finally return Home 

