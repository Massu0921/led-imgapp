import os, shutil
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

# ファイルアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'
# uploadを許可する拡張子
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 拡張子のチェック
def check_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':

        if 'file' not in request.files:
            return redirect(request.url)

        # データの取り出し
        img_file = request.files['file']

        if img_file.filename == '':
            return redirect(request.url)

        # ファイルのチェック
        if img_file and check_file(img_file.filename):
            # サニタイズ処理
            filename = secure_filename(img_file.filename)

            # uploads内削除
            shutil.rmtree("uploads")
            os.mkdir("uploads")

            # ファイルの保存
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = '/uploads/' + filename

            return render_template('index.html', img_url=img_url)

        else:
            return redirect(request.url)

    else:
        return render_template('index.html')
        

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8000, threaded=True)

