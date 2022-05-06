"""Server for INVESTABLE app."""
from flask import request, Flask, render_template, redirect, flash, session
import crud
from model import connect_to_db, db
# from importlib_metadata import files
import os #to access os.environ to access secrets.sh values
from jinja2 import StrictUndefined


app = Flask(__name__)
#tried resetting secret key a few times but still not working using a string for now
# app.secret_key = os.environ.get('SECRET_KEY')
app.secret_key = 'daskdaskdj'
#StrictUndefined is used to configure a Jinja2 setting that make it throw errors for undefined variables, helpful for debugging

app.jinja_env.undefined = StrictUndefined

@app.route('/')
def index():
    '''return homepage'''
    testing_session = session.get('price')
    session.modified = True
    return render_template('index.html')


@app.route('/calculator', methods=['POST'])
def to_calculate():
    '''return calculator interface'''
    
    price = request.form.get('price')
    down_payment = request.form.get('downpayment')
    rate = request.form.get('rate')
    mortgage = request.form.get('mortgage')
    closing = request.form.get('closing')
    rehab = request.form.get('rehab')
    rent = request.form.get('rent')
    taxes = request.form.get('taxes')
    insurance = request.form.get('insurance')
    hoa = request.form.get('hoa')
    utilities = request.form.get('utilities')
    maintenance = request.form.get('maintenance')
    pm = request.form.get('pm')
    vacancy = request.form.get('vacancy')
    capex = request.form.get('capex')
    
    flash('Running numbers')
    total_monthly_expenses = int(taxes) + int(insurance) + int(hoa) + int(utilities) + int(maintenance) + int(pm) + int(vacancy) + int(capex) + int(mortgage)
    cashflow = int(rent) - total_monthly_expenses
    
    #if user clicks SAVE, prompt LOGIN/SIGNUP and save data to db



    return render_template('calculator.html', cashflow=cashflow, price=price, downpayment=down_payment, rate=rate, closing=closing, rehab=rehab, rent=rent, taxes=taxes, insurance=insurance, hoa=hoa, utilities=utilities, maintenance=maintenance, pm=pm, vacancy=vacancy, capex=capex, mortgage=mortgage )


@app.route('/forum')
def to_read_post():
    '''if user is logged in, show dashboard features'''
    return render_template('forum.html')


@app.route('/news')
def get_news():
    '''show industry insight from news API'''
    return render_template('news.html')


@app.route('/books')
def get_books():
    '''show industry insight from goodreads API'''
    return render_template('books.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


@app.route('/register')
def register_page():
    '''landing page for register.'''
    return render_template('register.html')
    

@app.route('/register', methods=['POST'])
def register_user():
    '''Create a new user.'''

    first = request.form.get('first')
    last = request.form.get('last')
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if user:
        flash('Cannot create an account with that email. Try again.')
    else:
        user = crud.create_user(first, last, email, password)
        db.session.add(user)
        db.session.commit()
        flash('Account created! Please log in.')

    return redirect('/users')

@app.route('/login')
def login_page():
    '''Landing page for user login.'''

    return render_template('login.html')

@app.route('/login', methods=['POST'])
def process_login():
    '''Process user login.'''

    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.get_user_by_email(email)
    if not user or user.password != password:
        flash('The email or password you entered was incorrect.')
    else:
        # Log in user by storing the user's email in session
        session['user_email'] = user.email
        flash(f'Welcome back, {user.email}!')

    return redirect('/users')

@app.route('/users')
def profile_page():
    #how to show certain features when signed in (Login, Sign up shouldn't be there on the nav bar)
    
    email = request.form.get('email')
    password = request.form.get('password')
    return render_template('profile_page.html', email=email)

if __name__ == "__main__":
    # DebugToolbarExtension(app)
    connect_to_db(app)
    app.run(debug=True)
