from Pizza import app, db
from Pizza.models import pizza, customer
from flask import Flask, render_template, request, flash, session, redirect, g





@app.route('/', methods=["GET","Post"])
def home():

    return render_template("home.html")

@app.route('/user', methods=["GET","Post"])
def user():  #this should work as both a login and register
    if request.method == "POST":
        user = request.form.get('username')
        on = False #when the user is tagging the name, we make the user inactive.
        name = customer.query.filter_by(name=user).first()
        
        if name:
            print (name.active)
            if name.active == True:
                flash ("use a diffrent username, this one is being used")
                print("sssss")
                return render_template("home.html")
            else:
                flash ("username confirmed, coining name. logged in correctly, ")
                ustomer = request.form['username']
                update = customer.query.filter_by(name=user).first()
                flash("CRY")
                update.name = ustomer
                update.active = True

                db.session.commit()
                results = customer.query.all()

                return render_template("logged.html", results = results)
        elif name == None:
            new_customer = customer()
            new_customer.name = user
            new_customer.active = on

            session["Current_Customer"] = user
            print(user)
            db.session.add(new_customer)
            print (new_customer)
            db.session.commit()

            results = customer.query.all()
            return render_template("logged.html", results = results)
        
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

        id = request.form.get("pizzaid")
        print (id)

        pizz = customer()
        pizz.pizza_id = id
        pizz.name = user.name
        db.session.commit()
        print(hi)




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
    
    update = customer.query.filter_by(name=Current_Customer).first()

    update.active = False
    update.pizza_id = None

    db.session.commit()

    session.pop('Current_Customer', None)

    results = customer.query.filter_by(name=user).first()    
    print(results)
    return redirect(url_for('home'))

