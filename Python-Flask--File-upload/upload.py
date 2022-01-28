from flask import * 
from FBD import main
address = ""
app = Flask(__name__)  
 
@app.route('/')  
def upload():  
    return render_template("file_upload_form.html")  

# def ret(x):
#     return x
@app.route('/success', methods = ['POST'])  
def success():  
    if request.method == 'POST':  
        f = request.files['file']  
        f.save(f.filename)  
        global address
        address = f.filename
        # ret(address)
        return render_template("success.html", name = f.filename)  
if address != "":
    print(address)  
if __name__ == '__main__':  
    app.run(debug = True)
