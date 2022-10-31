import os

from flask import Flask, request, render_template

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")


@app.route("/perform_query/")
def perform_query(cmd1=None, value1=None, cmd2=None, value2=None, file_name=None):

    try:
        file_name = os.path.join(DATA_DIR, request.args.get('file_name'))
    except TypeError:
        return f'Не передан аргумент "file_name"', 400

    try:
        cmd1 = request.args.get("cmd1")
        cmd2 = request.args.get("cmd2")
        value1 = request.args.get("value1")
        value2 = request.args.get("value2")


        with open(file_name, 'r', encoding='UTF-8') as f:

            result = []

            if cmd1 == 'filter':
                result = [i.strip() for i in f if value1 in i]

            elif cmd1 == 'map':
                result = [i.strip().split()[int(value1)] for i in f]

            elif cmd1 == 'unique':
                all_data = [i.strip().split()[0] for i in f]
                for i in all_data:
                    if i not in result:
                        result.append(i)

            elif cmd1 == 'sort' and value1 == 'asc':
                result = sorted([i.strip() for i in f])

            elif cmd1 == 'sort' and value1 == 'desc':
                result = sorted([i.strip() for i in f], reverse=True)

            elif cmd1 == 'limit':
                n = 1
                for i in f:
                    if n <= int(value1):
                        n += 1
                        result.append(i.strip())

            if cmd2 == 'filter':
                result = [i.strip() for i in result if value2 in i]

            elif cmd2 == 'map':
                result = [i.strip().split()[int(value2)] for i in result]

            elif cmd2 == 'unique':
                all_data = [i.strip().split()[0] for i in result]
                for i in all_data:
                    if i not in result:
                        result.append(i)

            elif cmd2 == 'sort' and value2 == 'asc':
                result = sorted([i.strip() for i in result])

            elif cmd2 == 'sort' and value2 == 'desc':
                result = sorted([i.strip() for i in result], reverse=True)

            elif cmd2 == 'limit':
                n = 1
                for i in result:
                    if n <= int(value2):
                        n += 1
                        result.append(i.strip())

            return render_template("response.html", data=result)
    except FileNotFoundError:
        return f'Заданный файл {file_name} не найден', 400


    # return app.response_class('', content_type="text/plain")


if __name__ == '__main__':
    app.run()
