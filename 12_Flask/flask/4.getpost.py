from flask import Flask,render_template,request
'''
 It creates an instance of the Flask class, 
 which will be your WSGI (Web Server Gateway Interface) application.
'''
###WSGI Application
app=Flask(__name__)

@app.route("/")
def welcome():
    return "<html><H1>Welcome to the flask course</H1></html>"

@app.route("/index",methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

# capture the post request when submit button is hit
@app.route('/form',methods=['GET','POST'])
def form():
    if request.method=='POST':
        name=request.form['name']
        # return f'Hello {name}!'
    return render_template('form.html')


# When you use the same route for both displaying a form and processing it, this happens:

# Step 1 (GET): You type .../submit in the URL bar and hit enter. Your browser sends a GET request. Flask skips the if block and executes return render_template('form.html'). You see the empty form.

# Step 2 (POST): You fill in the name and click the Submit button. Because your HTML form has method="post", the browser sends a POST request to the URL. Flask now enters the if block, grabs the name, and returns the "Hello" string.

@app.route('/submit',methods=['GET','POST'])
def submit():
    if request.method=='POST': # browser is get request but becuase form do a POST it get true and returns the result
        name=request.form['name1']
        return f'Hello {name}! invoked from /submit route'
    return render_template('form.html')


if __name__=="__main__":
    app.run(host='0.0.0.0', port=5000)
    # app.run(debug=True)