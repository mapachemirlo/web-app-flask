from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Connection
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# Settings
app.secret_key = 'mysecretkey'

################################# OBTENER ######################################################
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    print(data)
    return render_template('index.html', contacts = data) #le paso los datos

################################# AGREGAR #######################################################
@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',(fullname, phone, email))
        mysql.connection.commit()
        flash('Contacto agregado satisfactoriamente')

        print(fullname)
        print(phone)
        print(email)
        #return 'received'
        return redirect(url_for('Index')) #Metodo un poco tosco
    

###################################### EDITAR ##################################################

@app.route('/edit/<id>')
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = {0}'.format(id)) #Formatear siempre el id
    data = cur.fetchall()
    cur.close()
    print(id)
    print(data[0])
    return render_template('edit-contact.html', contact=data[0]) #La variable contact carga la vista del archivo edit-contact
    

###################################### ACTUALIZAR ##############################################
@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        fullname = request.form['fullname']
        phone = request.form['phone']
        email = request.form['email']

        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE contacts
        SET fullname = %s,
            email = %s,
            phone = %s
        WHERE id = %s
     """, (fullname, email, phone, id)) #Como está en el orden de la query
    mysql.connection.commit()
    flash('Contacto actualizado Satisfactoriamente') 
    return redirect(url_for('Index'))


####################################### BORRAR ##################################################
#@app.route('/delete')
#def delete():
    #return 'Delete contact'
@app.route('/delete/<string:id>') #Recibe un parámetro que es un string del tipo id (debe tener al lado un número)
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto removido satisfactoriamente')
    return redirect(url_for('Index'))
    #return(id)
    

if __name__ == '__main__':
    app.run(port = 3000, debug = True)