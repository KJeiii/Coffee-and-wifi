from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, SelectField
from wtforms.validators import DataRequired, URL
import csv

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)


class CafeForm(FlaskForm):
    cafe = StringField('Cafe name', validators=[DataRequired()])
    location = URLField('Cafe Location on Google Maps (URL)', validators=[URL(), DataRequired()])
    opening = StringField('Opening time e.g. 8AM', validators=[DataRequired()])
    closing = StringField('Closing time e.g. 9PM', validators=[DataRequired()])
    rating = SelectField('Coffee Raing', choices=['☕','☕☕','☕☕☕','☕☕☕☕','☕☕☕☕☕'], validators=[DataRequired()])
    wifi = SelectField('Wifi Strenth Raing', choices=['✗','👍','👍👍','👍👍👍','👍👍👍👍','👍👍👍👍👍'], validators=[DataRequired()])
    power = SelectField('Power Socket Availability', choices=['✗','🔌','🔌🔌','🔌🔌🔌','🔌🔌🔌🔌','🔌🔌🔌🔌🔌'], validators=[DataRequired()])
    submit = SubmitField('Submit')

# Exercise:
# add: Location URL, open time, closing time, coffee rating, wifi rating, power outlet rating fields
# make coffee/wifi/power a select element with choice of 0 to 5.
#e.g. You could use emojis ☕️/💪/✘/🔌
# make all fields required except submit
# use a validator to check that the URL field has a URL entered.
# ---------------------------------------------------------------------------


# all Flask routes below
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=['POST','GET'])
def add_cafe():
    form = CafeForm()
    if form.validate_on_submit():
        with open('/Users/changkaichieh/coffee-and-wifi/cafe-data.csv', mode='a',newline='') as csv_file:
            csv_writer = csv.writer(csv_file, delimiter=',')
            csv_writer.writerow([form.cafe.data,
                                form.location.data,
                                form.opening.data,
                                form.closing.data,
                                form.rating.data,
                                form.wifi.data,
                                form.power.data])
        return redirect(url_for('cafes'))
    # 這邊使用redirect而不使用render_template的原因是，
    # 要在輸入完後，直接跳轉到cafes的頁面，並且讓cafes頁面能"正常運作"，
    # 如果這邊改用render_template的話，他會在add_cafe function下，
    # 讀取cafes.html，但cafes.html裡面有來自cafes fucntion的變數，
    # 必須在cafes function下，才能把變數e.g.list_of_rows 或 data_amount，
    # 傳到cafes.html進行運算，呈現畫面；反之如果在add_cafe function下，
    # 因為沒有list_of_rows等等資料傳入，html模版無法順利呈現資料；
    # redirect可以直接呼叫cafes function，進行運算，並且透過cafes.html的模版呈現資訊。

    # Exercise:
    # Make the form write a new row into cafe-data.csv
    # with   if form.validate_on_submit()
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    with open('/Users/changkaichieh/coffee-and-wifi/cafe-data.csv', newline='') as csv_file:
        csv_data = csv.reader(csv_file, delimiter=',')
        list_of_rows = []
        for row in csv_data:
            list_of_rows.append(row)
        data_amount = len(list_of_rows)
    return render_template('cafes.html', cafes=list_of_rows, data_amount = data_amount)


if __name__ == '__main__':
    app.run(debug=True)
