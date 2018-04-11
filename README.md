# thetaviewMaker
Automatic generation script for omnidirectional image viewing page<br>
(全天球画像閲覧用WebページのHTMLコード自動生成スクリプト)

## 概要
全天球画像をaframeを使って閲覧するための，一覧ページのコード自動生成スクリプト．
`photos`ディレクトリの中になる画像群を，`set.json`で指定されたページ，セクションで一覧表示するページを作成する．

## 条件
* 対応画像フォーマット(現状)
    * JPG
    * jpg
    * PNG
    * png
* 通常画像・全天球画像の判断はEXIF情報から
    * MODELに`THETA`が含まれるかどうか
* `python 3.x系`を使用
* python3で使うライブラリ
    * os : <br>
    ディレクトリ・ファイルの存在確認と作成
    * sys : <br>
    コマンドライン引数の取得
    * tqdm : <br>
    プログレスバーの表示
    * PIL.Image : <br>
    サムネイル画像作成，全天球画像判断(EXIF情報取得)
    * re : <br>
    正規表現

## version
### 1.x
version参照

### 2.x
version参照
### 3.x
#### 入力
* 前提ファイル構造
    ```
    [target]/
    -- photos/
    -- set.json
    ```

* 生成後ファイル構造
    ```
    [target]/
    -- photos/
    -- thumbs/
    -- pages/
    -- views/
    -- index.html
    -- set.json
    ```

* ファイル・フォルダ説明
    * photos/ : <br>
    表示させたい画像を入れるディレクトリ
    * thumbs/ : <br>
    表示させたい画像のサムネイル画像が保存されるディレクトリ
    * pages/ : <br>
    一覧用ページが保存されるディレクトリ
    * views/ : <br>
    全天球画像閲覧用ページが保存されるディレクトリ
    * index.html : <br>
    `set.json`にて、一番上に設定しているページでリダイレクトするページ
    * set.json : <br>
    生成したいページ・セクション・画像の設定が書かれるファイル

* コマンド
    ```
    python (...)/make.py [dir]
    ```
    * `python`は3.x系を使用
    * `[dir]`は作成したいディレクトリへのパス
    * デフォルト(指定しない)ではカレントディレクトリ

* set.json
    ```
    [
        {
            "pagename" : (pagename),
            "sections" : [
                {
                    "secname" : (secname),
                    "iamges" : [
                        "\\w+.JPG",
                    ]
                },
                {
                    "secname" : (secname),
                    "images" : [
                        "R00101(5[012]|49).JPG"
                    ]
                }
            ]
        }
    ]
    ```
    * 正規表現可能
    * 画像対応フォーマット(現状)
        * JPG
        * jpg
        * PNG
        * png