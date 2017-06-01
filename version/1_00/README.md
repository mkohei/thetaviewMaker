# make_pnrm_html.py
全天球画像閲覧用WebページのHTMLコード自動生成スクリプト

## コマンド

```
$python make_pnrm_html.py [dir_path] [title]
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

