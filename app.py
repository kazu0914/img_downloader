from flask import Flask, request,render_template
from icrawler.builtin import GoogleImageCrawler
import uuid, shutil, os

app = Flask(__name__, static_folder="./static")

MIN_DOWNLOAD_IMG_NUM = 3 # ダウンロード枚数未入力時の最小ダウンロード数
MAX_NUM = 20 # ユーザーが1回でダウンロードできる最大枚数

@app.route('/', methods=['GET', 'POST'])
def index():
    file_name = uuid.uuid4().hex
    folder_name = "./static/" + file_name
    if request.method == "POST":
        img = request.form['img'] if request.form['img'] != "" else "犬"
        num = int(request.form['num']) if request.form['num'] != "" else  MIN_DOWNLOAD_IMG_NUM 
        num = num if num < 20 else MAX_NUM

        crawler = GoogleImageCrawler(storage={"root_dir": folder_name})
        # Googleから指定画像と指定枚数をクローリング
        crawler.crawl(keyword=img, max_num=int(num))
        # zipファイルに解凍
        shutil.make_archive(folder_name, 'zip', root_dir=folder_name)
        # html側で表示する必要な変数を渡す
        return render_template('index.html', img=img, num=num ,folder_name=folder_name, file_name=file_name)
    else:
        return render_template('index.html')

if __name__ == "__main__":
    app.run(port=8000, debug=True)