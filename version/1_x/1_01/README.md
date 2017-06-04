# make_pnrm_html.py
全天球画像閲覧用WebページのHTMLコード自動生成スクリプト

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
    * `filename` : 画像ファイル名 and 表示名
    * `description` : 画像の説明 (なくても良い)

    例)

```
[
    {
        "filename" : "test1",
        "description" : "説明１"
    },
    {
        "filename" : "test3",
        "description" : "説明３"
    },
    {
        "filename" : "test4",
    }
]
```

* 説明 (description) が必要なくても、画像の表示順を設定したい場合も `setting.json` を記述する必要がある
* まず `setting.json` の記述順に表示され、その後それ以外の画像を名前順に表示される

## 注意
* MAC OS X 濁点問題<br>
    MAC OS X のファイルに日本語濁点を用いると、その文字列は2文字に分かれて扱われる. 具体的には、「ゲ」は「ケ」と「゛」となる. これによりこのコードの文字列マッチングはうまくいかずにエラーの原因となっている. 現状対応できていないため、MAC OS X 以外のOS でファイルの命名を行っていただきたい.
* pics, view ディレクトリのパーミッション<br>
    view ディレクトリに index.html(or .php)がないため、ディレクト内部が丸見えである.とりあえず、chmod コマンド等でパーミッションを変えておく.<br>
    今後, このコード内で pics, view ディレクトリ用の index.html を作成する方向でも考える. 
* アップロードした画像のパーミッション<br>
    アップロートした画像のパーミッションが 400とかだと見れないので注意

## TODO
- [ ] MAC OS X ファイル名濁点問題への対応
- [ ] .JPG への対応
- [ ] 他の画像フォーマットへの対応 (JPG, jpg, PNG, png)
- [ ] pics, view ディレクトリ内部丸見え問題への対応
- [ ] リスト表示の幅による列挙個数の調整表示
- [ ] リスト表示の際リサイズした画像を表示(通信量軽減)
- [ ] "filename", "description" を "fn", "desc" でも大丈夫にする(filename, description は長い)


