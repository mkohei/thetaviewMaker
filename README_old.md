# thetaviewMaker
Automatic generation script for omnidirectional image viewing page<br>
(全天球画像閲覧用WebページのHTMLコード自動生成スクリプト)

## 概要
全天球画像をaframeを持ちて閲覧するための、一覧ページのコード自動生成スクリプト．picsディレクトリの中にある全天球画像群を, `setting.json`で指定された設定によって一覧表示ページコードを生成する．

## version
### 1.x
#### 表示形式
* ページタイトル
* 画像一覧 : 画像一枚それぞれにタイトルを付けられる
#### 入力
* コマンド
```
$python make_thetaview_html.py [dir_path] [title]
```
* setting.jon
```
[
    {
        "filename" : "title1",
        "description" : "説明1"
    },
    {"fn":"title2", "desc":"説明2"},
    {"fn":"title3"},
    ...
]
```
* ファイル構造
```
[dir]
-- [pics]
-- setting.json
```

### 2.x
#### 表示形式
* ページタイトル
* 大タイトル, 小タイトルがあり, 小タイトルの中に画像一覧が並ぶ
#### 入力
* コマンド
```
$python make_thetaview_html.py [dir_path] [title]
```
* setting.json
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
* ファイル構造
```
[dir]
-- [pics]
-- setting.json
```

### 3.x
#### 表示形式
* 2.x の集まりが対象
* メニューバーで[dir], [smalltitle]を選択可能に
#### 入力
* コマンド
```
$python make_thetaview_html.py [dir_path] [title]
```
* setting.json
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
* ファイル構造
```
[target]
-- [dir1]
   -- [pics]
   -- setting.json
-- [dir2]
   -- [pics]
   -- setting.json
...
```

## 注意
* MAC OS X 濁点問題<br>
    MAC OS X のファイルに日本語濁点を用いると、その文字列は2文字に分かれて扱われる. 具体的には、「ゲ」は「ケ」と「゛」となる. これによりこのコードの文字列マッチングはうまくいかずにエラーの原因となっている. 現状対応できていないため、MAC OS X 以外のOS でファイルの命名を行っていただきたい.
* pics, view ディレクトリのパーミッション<br>
    view ディレクトリに index.html(or .php)がないため、ディレクト内部が丸見えである.とりあえず、chmod コマンド等でパーミッションを変えておく.<br>
    今後, このコード内で pics, view ディレクトリ用の index.html を作成する方向でも考える. 
* アップロードした画像のパーミッション<br>
    アップロートした画像のパーミッションが 400とかだと見れないので注意．0644とかに変更する．

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