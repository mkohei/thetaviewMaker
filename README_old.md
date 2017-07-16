# thetaviewMaker
Automatic generation script for omnidirectional image viewing page<br>
(全天球画像閲覧用WebページのHTMLコード自動生成スクリプト)

## versino
* 1.x: `setting.json`非不可欠、一覧
* 2.x: `setting.json`不可欠、bigtitle, smalltitle

## コマンド

```
$python make_thetaview_html.py [dir_path] [title]
```

* python 3.x 使用
* [dir_path] : 生成先のディレクトリのパス
* [title] : 生成する Web ページのタイトル<br>
    指定しなくても良い (その場合 `untitled` になる)

## 前提条件
* 生成先のディレクトリに `pics` ディレクトリが存在すること<br>
    `pics` ディレクトリに表示させたい画像を置く

## 処理結果
* リストページ `index.html` ファイル生成
* リストページ用スタイルシート `list.css` ファイル生成
* 閲覧ページ群 `view` ディレクトリ生成
* 閲覧ページ `[title].html` ファイルの生成

## その他処理について
* 設定ファイル `setting.json` により表示内容の設定が可能<br>
    * ~~`filename` or `fn` : 画像ファイル名 and 表示名~~
    * ~~`description` or `desc` : 画像の説明 (なくても良い)~~
    * `bigtitle` or `bt` or `b` : Big Title
    * `contents` or `c` : Contents
    * `smalltitle` or `st` or `s` : Small Title
    * `images` or `i` : omnidirectinal image file name (without extension)
    * bigtitle, smalltitle を設定しない場合は `other` となる
    

旧例)

```
[
    {
        "filename" : "test1",
        "description" : "説明１"
    },
    {
        "fn" : "test3",
        "desc" : "説明３"
    },
    {
        "fn" : "test4",
    }
]
```

新例)

```
[
    {
        "bigtitle" : "BIG_TITLE_1",
        "contents" : [
            {
                "smalltitle" : "SMALL_TITLE_1",
                "images" : ["img1", "img2"]
            }
        ]
    },
    {"b":"BIG", "c":[
        {"s":"SMALL1", "i":["1", "2", "3", "4"]},
        {"s":"SMALL2", "i":["5", "6", "7", "8"]}
    ]}
]
```

* ~~説明 (description) が必要なくても、~~ 画像の表示順を設定したい場合は `setting.json` を記述する必要がある
* まず `setting.json` の記述順に表示され、その後それ以外の画像を名前順に表示される

## 注意
* MAC OS X 濁点問題<br>
    MAC OS X のファイルに日本語濁点を用いると、その文字列は2文字に分かれて扱われる. 具体的には、「ゲ」は「ケ」と「゛」となる. これによりこのコードの文字列マッチングはうまくいかずにエラーの原因となっている. 現状対応できていないため、MAC OS X 以外のOS でファイルの命名を行っていただきたい.
* pics, view ディレクトリのパーミッション<br>
    view ディレクトリに index.html(or .php)がないため、ディレクト内部が丸見えである.とりあえず、chmod コマンド等でパーミッションを変えておく.<br>
    今後, このコード内で pics, view ディレクトリ用の index.html を作成する方向でも考える. 
* アップロードした画像のパーミッション<br>
    アップロートした画像のパーミッションが 0400とかだと見れないので注意．0644とかに変更する．

## TODO
- [ ] MAC OS X ファイル名濁点問題への対応
- [ ] .JPG への対応
- [ ] 他の画像フォーマットへの対応 (JPG, jpg, PNG, png)
- [ ] pics, view ディレクトリ内部丸見え問題への対応
- [x] リスト表示の幅による列挙個数の調整表示
- [x] リスト表示の際リサイズした画像を表示(通信量軽減)
- [x] "filename", "description" を "fn", "desc" でも大丈夫にする(filename, description は長い)
- [ ] JS の Warning を無くす (開発者ツールで確認)
- [x] layout の修正<br>
    メニューの iframe をコンテンツの iframe より前に持ってきて float を調整<br>
    min-width をつけることや js でウィンドウに合わせた横幅の調整<br>
- [x] 新レイアウトの作成
- [ ] thetaview/index.html (複数のリストページまとめページ)の自動生成
- [ ] setting.json の非必須化
