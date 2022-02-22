from flask import Flask, request, render_template, request, url_for, flash, redirect
import sqlite3
import hashlib
import socket
from datetime import datetime, timedelta

# https://www.digitalocean.com/community/tutorials/how-to-make-a-web-application-using-flask-in-python-3-ru
# https://www.delftstack.com/ru/howto/python/get-ip-address-python/

# s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# s.connect(("8.8.8.8", 80))
# MYADDRESS = s.getsockname()[0]


app = Flask(__name__)
app.config['SECRET_KEY'] = 'your secret key'


# def get_db_connection():
#     conn = sqlite3.connect('database.db')
#     conn.row_factory = sqlite3.Row
#     return conn
#
# @app.route('/dbPage')
# def index():
#     if request.remote_addr == MYADDRESS:
#         conn = get_db_connection()
#         posts = conn.execute('SELECT * FROM usersData').fetchall()
#         conn.close()
#         return render_template('dataBaseTable.html',posts = posts)
#     else:
#         return render_template('permissionDenied.html')

@app.route('/', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        initialSum = int(request.form['sum'])
        months = int(request.form['srok'])
        percent = float(request.form['stavka'])
        t = []
        percentOnMonth = percent / 1200
        itog1 = initialSum * percentOnMonth
        t.append({'N': 1, 'sum1': round(initialSum + itog1, 2), 'itog': round(itog1, 2)})
        for i in range(2, months+1):
            lastOfT = t[i - 2]
            itog1 = lastOfT['itog'] * percentOnMonth + lastOfT['itog']
            t.append({'N': i, 'sum1': round(lastOfT['sum1'] + itog1, 2), 'itog': round(itog1, 2)})

        profit = (initialSum * percentOnMonth * months)
        endSum = profit + initialSum
        return render_template('index.html',
                               table=t,
                               summaItog="Итоговая сумма = {} руб".format(round(endSum, 3)),
                               plus="Доход = {} руб".format(round(profit, 3)))

    #     if request.method == 'POST':
    #         login = request.form['login']
    #         password = request.form['password']
    #
    #         if not login or not password:
    #             flash('Логин и/или пароль не должны быть пустыми')
    #         else:
    #             conn = get_db_connection()
    #             passwordForInter = hashlib.md5(password.encode())
    #             conn.execute("INSERT INTO usersData (login, password) VALUES (?, ?)",
    #                         (login,passwordForInter.hexdigest()))
    #             conn.commit()
    #             conn.close()
    #             flash('Вы успешно зарегестрировались')
    #             return redirect(url_for('signup'))
    #
    #     return render_template('signup.html')
    # else:
    #     if request.method == "POST":
    #         login = request.form['login']
    #         password = request.form['password']
    #         if not login or not password:
    #             flash('Логин и/или пароль не должны быть пустыми')
    #         else:
    #             conn = get_db_connection()
    #
    #             loginsFromDB = list(map(lambda x: x[0], conn.execute("""SELECT login from usersData""").fetchall()))
    #             dtNow = datetime.now()
    #             dtNowInString = dtNow.isoformat(":", "auto")
    #
    #             #СЕРВЕР
    #             if login in loginsFromDB: #Если есть логин в БДf
    #                 #Перезаписываем временную метку и пишем срок в БД (now + 1 неделя)
    #                 conn.execute("Update usersData set t = ?, t_end = ? where login = ?",(dtNow ,dtNow + timedelta(weeks=1),login))
    #                 conn.commit()
    #
    #                 #Шифруем время
    #                 md5TS = hashlib.md5(dtNowInString.encode()).hexdigest()
    #
    #                 #КЛИЕНТ
    #                 md5C = hashlib.md5((md5TS + hashlib.md5(password.encode()).hexdigest()).encode()).hexdigest()
    #
    #                 #СЕРВЕР
    #                 curr = conn.cursor()
    #                 passwordFromDB = curr.execute('SELECT password from usersData where login = ?',(login,)).fetchall()[0][0]
    #                 md5S = hashlib.md5((md5TS + passwordFromDB).encode()).hexdigest()
    #
    #                 timeFromDB = curr.execute('SELECT t_end from usersData where login = ?',(login,)).fetchall()[0][0]
    #                 timeFromDB = datetime.strptime(timeFromDB, "%Y-%m-%d %H:%M:%S.%f")
    #
    #                 if timeFromDB>datetime.now() and md5C == md5S:
    #                     return render_template('userIn.html', login = login)
    #                 else:
    #                     flash('Введен неправильный пароль')
    #             else:
    #                 flash('Клиент с введенным логином не зарегистрирован')
    #             conn.close()
    #         return redirect(url_for('signup'))
    #     else:
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
