from flask import Flask,render_template
#make an app
app=Flask(__name__)

#endpoint
@app.route("/")
def hello():
    return render_template('index.html')
#about route endpoint

@app.route("/about")
def soumik():
    name="soumik"
    #first name is from template ,second from python
    return render_template('about.html',name=name) # accessed from html file



#static is a public folder but templates is not

@app.route("/bootstrap")
def bootstrap():

    #first name is from template ,second from python
    return render_template('bootstrap.html') # accessed from html file

app.run(debug=True)
