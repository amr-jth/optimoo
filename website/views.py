from flask import Blueprint,render_template

views=Blueprint('views',__name__,template_folder='template')

@views.route('/')
def home():
    return render_template('home.html')

# @views.route('/loginpage')
# def loginpage():
#     return render_template('login.html')