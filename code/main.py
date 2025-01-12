from flask import Flask, render_template, request, redirect, url_for, jsonify
# from flask import session
import mysql.connector
import random
import matplotlib.pyplot as plt
from io import BytesIO
import base64
# from werkzeug.security import generate_password_hash

app = Flask(__name__)
# user_id = -1

# MySQL database configuration
'''db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'database': 'flightsdatabase2',
    'port': '3306',
}'''

connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')

# Create a MySQL connection
# connection = mysql.connector.connect(**db_config, auth_plugin='mysql_native_password')
cursor = connection.cursor()

@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    connection = None
    cursor = None
    try:
        if request.method == 'POST':
            username = request.form['uname']
            password = request.form['psw']
            phone_number = request.form['phonenum']
            user_id_exists = True
            connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
            cursor = connection.cursor()
            while user_id_exists:
                user_id = random.randint(1000, 9999)
                cursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %s)", (user_id,))
                user_id_exists = cursor.fetchone()[0]
            try:
                cursor.execute("INSERT INTO Users (userID, username, password, phoneNumber) VALUES (%s, %s, %s, %s)", (user_id, username, password, phone_number))
                connection.commit()
            except mysql.connector.Error as err:
                return render_template('create-acct.html', error=str(err))
            return render_template('login-acct.html') 
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
    return render_template('create-acct.html')

'''@app.route('/create-account', methods=['GET', 'POST'])
def create_account():
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['psw']
        phone_number = request.form['phonenum']
        user_id_exists = True
        while user_id_exists:
            user_id = random.randint(1000, 9999)
            cursor.execute("SELECT EXISTS(SELECT 1 FROM Users WHERE userID = %s)", (user_id,))
            user_id_exists = cursor.fetchone()[0]

        # Insert user into the Users table
        cursor.execute("INSERT INTO Users (userID, username, password, phoneNumber) VALUES (%s, %s, %s, %s)", (user_id, username, password, phone_number))
        connection.commit()
        return redirect(url_for('user_login'))  
    else:
        return render_template('create-acct.html')'''

@app.route('/') 
def home():
	return render_template("index.html")

'''@app.route('/login')
def login():
     return render_template("login-acct.html")'''



@app.route('/login', methods=['GET', 'POST'])
def user_login():
    connection = None
    cursor = None
    message = ''
    try:
        if request.method == 'POST':
            username = request.form['uname']
            password = request.form['psw']
            connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
            # connection = mysql.connect()
            cursor = connection.cursor()

            query = """SELECT userID, password FROM Users WHERE username = %s"""
            cursor.execute(query, (username,))
            user = cursor.fetchone()
            '''if user:
                user_id, user_password = user
                if user_password == password:
                    session['user_id'] = user_id  
                    return redirect(url_for('home_after_login'))  
                else:
                    return 'Invalid username or password'
            else:
                return 'Invalid username or password' '''
            if user:
                user_id, user_password = user
                # user_password = user[0]
                if user_password == password:
                    # return 'Logged in successfully'
                    # session['user_id'] = user_id
                    # return redirect(url_for('home_after_login'))  
                    return render_template('home2.html', data = user_id)
                else:
                    return 'Invalid password'
            else:
                return 'Invalid password'
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()
    return render_template('login-acct.html')

@app.route('/home-after-login')
def home_after_login():
    # get the user's user id 
    return render_template('home2.html')

@app.route('/worst-times-to-fly')
def worst_times_to_fly():
    return render_template('worst-times-to-fly.html')

@app.route('/rate-airline')
def rate_an_airline():
    return render_template('rate-an-airline.html')

@app.route('/keyword_search', methods=['GET'])
def keyword_search():
    connection = None
    cursor = None
    try:
        month = request.args.get('month')     
        connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        query = """
        SELECT month as Month, day as Day, COUNT(*) AS Total_Flights,
        COUNT(CASE WHEN (departureDelay IS NOT NULL AND departureDelay != '0') OR (cancelled = 1) THEN 1 END) AS Number_of_Delays_or_Cancellations
        FROM Flights
        WHERE Month = %s
        GROUP BY Month, Day
        ORDER BY Number_of_Delays_or_Cancellations DESC
        LIMIT 5;
        """
        cursor.execute(query, (month,))
        results = cursor.fetchall()
        return render_template('worst-times-to-fly.html', data = results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

@app.route('/plot', methods=['GET'])
def plot():
    connection = None
    cursor = None
    try: 
        month = request.args.get('month')
        connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
        cursor = connection.cursor() 
        query = """
            SELECT month, COUNT(CASE WHEN departureDelay IS NOT NULL AND departureDelay != '0' THEN 1 END) AS NumDepartureDelays, COUNT(CASE WHEN cancelled = 1 THEN 1 END) as NumCancellations
            FROM Flights
            WHERE month = %s
            GROUP BY month
            ORDER BY NumDepartureDelays DESC, NumCancellations DESC;
        """
        cursor.execute(query, (month,))

        results = cursor.fetchall()
        connection.close()

        months = [row[0] for row in results]
        departure_delays = [row[1] for row in results]
        cancellations = [row[2] for row in results]
        
        bar_width = 0.35
        indices = range(len(months))

        plt.figure(figsize=(5, 3))
        plt.bar([index - bar_width / 2 for index in indices], departure_delays, width=bar_width, label='Departure Delays')
        plt.bar([index + bar_width / 2 for index in indices], cancellations, width=bar_width, label='Cancellations')

        plt.xlabel('Month')
        plt.ylabel('Count')
        plt.title(f'Delays and Cancellations for Month {month}')
        plt.xticks(indices, months)
        plt.legend()
        plt.tight_layout()

        img = BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()
        return f'<img src="data:image/png;base64,{plot_url}" />' 
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

# ratings 
def check_exist(user_id, airline):
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users WHERE userID = %s", (user_id,))
        if cursor.fetchone()[0] == 0:
            return False, 'User ID does not exist'
        cursor.execute("SELECT COUNT(*) FROM airlines WHERE IATAcodeAirline = %s", (airline,))
        if cursor.fetchone()[0] == 0:
                        return False, 'Airline does not exist'          
        return True, ''
    except Exception as e:
                return False, str(e)     
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

@app.route('/create_rating', methods=['POST'])
def create_rating():
    connection = None
    cursor = None
    try:
        user_id = request.form['user_id']
        airline = request.form['airline']
        try:
            user_rating = int(request.form['user_rating'])
        except ValueError:
            # result = 'Invalid rating format. Rating must be a number.'
            return jsonify({'error': 'Invalid rating format. Rating must be a number.'}), 400
        if not (1 <= user_rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        exists, message = check_exist(user_id, airline)
        if not exists:
            # result = message
            return jsonify({'error': message}), 400
        connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        query = """
            INSERT INTO userRating (userID, airline, userRating) 
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (user_id, airline, user_rating))
        connection.commit()
        # return jsonify({'message': 'Rating created successfully'}), 200
        result = "Successful!"
        return render_template('rate-an-airline.html', message = result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

@app.route('/read_rating', methods=['GET'])
def read_rating():
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        # query tells us average user rating for each airline
        query = """
            SELECT A.IATAcodeAirline, A.airline, AVG(U.userRating) AS AvgUserRating
            FROM Airlines A 
            JOIN userRating U ON A.IATAcodeAirline = U.airline
            GROUP BY A.IATAcodeAirline, A.airline
        """
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template('rate-an-airline.html', data=results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

@app.route('/update_rating', methods=['POST'])
def update_rating():
    connection = None
    cursor = None
    try:
        user_id = request.form['user_id']
        airline = request.form['airline']
        try:
            user_rating = int(request.form['user_rating'])
        except ValueError:
            return jsonify({'error': 'Invalid rating format. Rating must be a number.'}), 400
        if not (1 <= user_rating <= 5):
            return jsonify({'error': 'Rating must be between 1 and 5'}), 400
        exists, message = check_exist(user_id, airline)
        if not exists:
            return jsonify({'error': message}), 400
        connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
        cursor = connection.cursor()
        query = """
            UPDATE userRating 
            SET userRating = %s
            WHERE userID = %s AND airline = %s
        """
        cursor.execute(query, (user_rating, user_id, airline))
        connection.commit()
        if cursor.rowcount == 0:
            return jsonify({'message': 'No rating found to update'}), 404
        # return jsonify({'message': 'Rating updated successfully'}), 200
        result = "Successful!"
        return render_template('rate-an-airline.html', message = result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

@app.route('/delete_rating', methods=['POST'])
def delete_rating():
    connection = None
    cursor = None
    try: 
        user_id = request.form['user_id']
        airline = request.form['airline']

        exists, message = check_exist(user_id, airline)
        if not exists:
            return jsonify({'error': message}), 400

        connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
        cursor = connection.cursor()

        cursor.execute("SELECT COUNT(*) FROM userRating WHERE userID = %s AND airline = %s", (user_id, airline))
        if cursor.fetchone()[0] == 0:
            return jsonify({'message': 'No rating found to delete'}), 404


        query = """
        DELETE FROM userRating
        WHERE userID = %s AND airline = %s
        """
        cursor.execute(query, (user_id, airline))
        connection.commit()

        if cursor.rowcount == 0:
            return jsonify({'error': 'Error deleting rating'}), 500

        # return jsonify({'message': 'Rating deleted successfully'}), 200
        result = "Successful!"
        return render_template('rate-an-airline.html', message = result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

@app.route('/best_airports_to_fly')
def best_airports_to_fly():
    return render_template('best-airports-to-fly.html')

@app.route('/stored-procedure')
def stored_procedure():
    cursor = None
    connection = None
    try:
        connection = mysql.connector.connect(user='root', password='Chatt$1608', host='127.0.0.1', database='flightsdatabase2', port = '3306', auth_plugin='mysql_native_password')
        cursor = connection.cursor(dictionary=True)
        cursor.callproc('Proced')
        airports=[]
        for result in cursor.stored_results():
            airports = result.fetchall()
        # print("hi")
        # print(airports)
        return render_template('best-airports-to-fly.html', data=airports)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        if cursor is not None:
            cursor.close()
        if connection is not None and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    app.run(debug=True) 