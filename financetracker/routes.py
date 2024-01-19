from flask import render_template, request, redirect, url_for, session
from financetracker import app, db
from financetracker.models import User, Transaction, Asset


@app.route("/")
def home():
    return render_template("log-in.html")


# View for Log-In Page
@app.route("/log-in", methods=["GET", "POST"])
def logIn():
    try:
        if request.method == "POST":
            username = request.form.get("username").lower()
            password = request.form.get("password")
            user = User.query.filter_by(username=username).first()

            # Checks if users password is the same as in the database
            if password == user.password:
                # Grants Log-In
                session["USER_ID"] = user.id
                return redirect(url_for("dashboard"))
            else:
                # Redirects to Log-in
                print("Incorrect Password")
                message = "Incorrect Password"
                return render_template("log-in.html", log_in_message=message)
    
    # If User has the Wrong Username
    except AttributeError:
        print("No Account with that username")
        message = "No Account Found With That Username"
        return render_template("log-in.html", log_in_message=message)

    return render_template("log-in.html")


# View for Register Page
@app.route("/register", methods=["GET", "POST"])
def register():
    try:
        if request.method == "POST":
            # Adds data to the database
            username = request.form.get("username").lower()
            password = request.form.get("password")
            net_worth_goal = request.form.get("net_worth_goal")
            savings_goal = request.form.get("savings_goal")
            new_user = User(username=username,password=password, net_worth_goal=net_worth_goal, savings_goal=savings_goal)
            
            # Commits data
            db.session.add(new_user)
            db.session.commit()

            # Redirects to Log-In Page
            return redirect(url_for("logIn"))
    
    # If Username already taken
    except:
        print("Username Already Taken")
        message = "Username Already Taken"
        return render_template("register.html", register_message=message)

    return render_template("register.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html", active_page="dashboard")


@app.route("/income&expenses")
def income_expenses():
    # Retrieves users credentials
    USER_ID = session.get('USER_ID')
    user = User.query.get(USER_ID)

    # Checks for users salary and formats salary
    if user.salary:
        salary = "{:,}".format(user.salary)
    else:
        salary = "{:,}".format(36000)

    return render_template("income-expenses.html", active_page="income_expenses", salary=salary)


@app.route("/add-transaction", methods=["GET", "POST"])
def addTransaction():
    return render_template("add-transaction.html", active_page="income_expenses")


@app.route("/edit-salary", methods=["GET", "POST"])
def editSalary():
    if request.method == "POST":
        # Retrieves the salary from the form and the credentials of the logged in user
        salary = int(request.form.get("salary"))
        USER_ID = session.get('USER_ID')
        user = User.query.get(USER_ID)

        # Changes the users salary to the new salary
        user.salary = salary
        db.session.commit()

        return redirect(url_for("income_expenses"))
    return render_template("edit-salary.html", active_page="income_expenses")


@app.route("/delete-transaction")
def deleteTransaction():
    return render_template("delete-transaction.html", active_page="income_expenses")


@app.route("/assets")
def assets():
    return render_template("assets.html", active_page="assets")


@app.route("/add-assets", methods=["GET", "POST"])
def addAssets():
    if request.method == "POST":
        USER_ID = session.get('USER_ID')

        # Adds data to the database
        asset_name = str(request.form.get("asset-name")).capitalize()
        asset_value = request.form.get("asset-value")
        new_asset = Asset(user_id=USER_ID, asset_name=asset_name, asset_value=asset_value)

        # Commits data
        db.session.add(new_asset)
        db.session.commit()

        # Redirects to asset page
        return redirect(url_for("assets"))
    return render_template("add-asset.html", active_page="assets")


@app.route("/delete-assets", methods=["GET", "POST"])
def deleteAssets():
    if request.method == "POST":
        USER_ID = session.get('USER_ID')
        assets = Asset.query.filter_by(user_id=USER_ID).all()
        asset_name = str(request.form.get("asset-name")).capitalize()

        # Iterate through the assets and delete the one with the specified name
        for asset in assets:
            if asset.asset_name == asset_name:
                db.session.delete(asset)

        # Commit the changes to the database
        db.session.commit()

        # Redirects to asset page
        return redirect(url_for("assets"))
    
    return render_template("delete-asset.html", active_page="assets")