import io
import base64
from flask import Flask, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename
from ledctrl import LEDCtrl


# ファイルアップロード先のディレクトリ
UPLOAD_FOLDER = './uploads'

# uploadを許可する拡張子
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif'])

# Flaskのインスタンス生成
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# LEDインスタンス格納用
led = None

def show_uploadimage(led, imgpath):
    """アップロードした画像をLEDに表示
    """
    led.clear()
    img = led.loadimg(imgpath)
    led.showimage(img)

def check_file(filename):
    """拡張子のチェック
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def index():
    global led
    # 初回のみ，LEDのインスタンス生成
    if led == None:
        led = LEDCtrl()
        led.setup()

    # LED表示をクリア
    led.clear()

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
            fileformat = filename.split(".")[1]

            # ページに表示する画像のフォーマットを作成
            img_base64 = base64.b64encode(img_file.read())
            img_base64_str = "data:image/{};base64,".format(fileformat) + str(img_base64).split("'")[1]

            # LED表示用の画像のフォーマットを作成
            data = str(img_base64).split("'")[1]

            # LEDに画像表示
            show_uploadimage(led, io.BytesIO(base64.b64decode(data)))

            # ページに画像表示
            return render_template('index.html', img_base=img_base64_str)

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
