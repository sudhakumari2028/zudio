from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

# Configure MySQL connection
db_config = {
    'host': 'zudio.c1umwkcyeg8m.ap-south-1.rds.amazonaws.com',
    'user': 'admin',
    'password': 'zudiobca123',
    'database': 'database'
}


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/students')
def view_students():
    print("view students")
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM students")
            students = cursor.fetchall()
            for student in students:
                print(student[0], student[1], student[2], student[3],student[4],student[5])
    finally:
        connection.close()
    return render_template('view_students.html', students=students)

@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        contact_number = request.form['contact_number'] 
        section = request.form['section'] 
        college = request.form['college']       


        connection = pymysql.connect(**db_config)
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO students (name, email, contact_number,section,college) VALUES (%s, %s, %s,%s, %s)"
                cursor.execute(sql, (name, email,contact_number,section,college))
            connection.commit()
        finally:
            connection.close()

        return redirect(url_for('view_students'))
    return render_template('add_student.html')

@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    print("edit student::",id)

    
    connection = pymysql.connect(**db_config)

    if request.method == 'GET':
        with connection.cursor() as cursor:

            cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
            student = cursor.fetchone()
            print("student::",student)
        return render_template('edit_student.html', student=student)
    try:
        with connection.cursor() as cursor:
            if request.method == 'POST':
                name = request.form['name']
                email = request.form['email']
                contact_number = request.form['contact_number'] 
                section = request.form['section'] 
                college = request.form['college'] 
                sql = "UPDATE students SET name=%s, email=%s, contact_number=%s, section=%s, college=%s WHERE id=%s"
                cursor.execute(sql, (name, email, contact_number,section,college, id))
                connection.commit()
                return redirect(url_for('view_students'))
            else:
                cursor.execute("SELECT * FROM students WHERE id=%s", (id,))
                student = cursor.fetchone()
                print("student::",student)
    finally:
        connection.close()
    return render_template('edit_student.html', student=student)
    

@app.route('/delete_student/<int:id>', methods=['GET','POST'])
def delete_student(id):
    print("delete student::",id)
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM students WHERE id=%s", (id,))
            connection.commit()
    finally:
        connection.close()
    return redirect(url_for('view_students'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')