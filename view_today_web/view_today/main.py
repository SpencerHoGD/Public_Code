from flask import Flask, render_template, request
from show_todayhot import show_top_message

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        rows = request.form.get('rows')

        # 判断输入是否符合要求
        # 如果有数字以外的字符
        if not rows.isdigit():
            return render_template('index.html')

        rows = int(rows)
        # 如果数字不在 1-100之间
        if rows < 1 or rows > 101:
            return render_template('index.html')

        df = show_top_message(rows)
        text = ''
        for i, row in df.iterrows():
            message = str(i) + row['content'] + '\t来自:' + row['source'] + '\n'
            text += message
        return render_template('index.html', df=df)


if __name__ == '__main__':
    app.run(debug=True)
