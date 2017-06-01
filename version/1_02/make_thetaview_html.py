#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Code to generate HTML source file to view panorama pictures automatically.

~ Preconditions ~
* The specified directory contains the `pics` directory.
  (Put the omnidirectional image you want to display in the `pics` directory.)
* The specified directory contains the `prnm.json` file.
  (If there is no file, create it.)

~ Command ~
$ python make_pnrm_html.py [dir_path] ([page_title])

~ author ~
Kohei Matsumoto

~ version ~
* 1.00 (2017/05/12)
* 1.01 (2017/05/19)
    - "[Warning] `description` key is not undefined." でどのファイル名に対してかを表示するように変更
* 1.02 (22017/05/20)
    - 一覧画面用に画像リサイズ
    - filename, description を fn, desc でも可に
"""

import os
import sys
import json
import datetime
from tqdm import tqdm

#####################
##### constants #####
#####################

CONTENT_CSS = """
/* --- リストエリア --- */ 
ul.thumbnail {
    /* リストエリアの幅 */
    width: 100%;
    /* リストエリアの最小幅（不要な場合は削除）*/
    min-width: 660px;
    margin: 0;
    /* リストエリアのパッディング（上、左右、下）*/
    padding: 30px 0 0;
    list-style-type: none;
}

/* --- リスト項目 --- */
ul.thumbnail li {
    /* 項目の幅 */
    width: 30%;
    /*width: 30%;*/
    /*width: 100%;*/
    float: left;
}

/* --- 項目内容 --- */
ul.thumbnail dl {
    /* 内容の幅 */
    /*width: 142px;/*
    width: 30%
    /* 内容のセンタリング */
    margin: 0 auto;
    font-size: 80%;
}

/* --- 写真エリア --- */
ul.thumbnail dt {
    /* 写真エリアの高さ（dt要素の高さを指定する場合）*/
    /*height: 102px;*/
    /* 写真エリアの下マージン */
    margin-bottom: 5px;
}
ul.thumbnail dt img {
    /* 写真の境界線 */
    border: 1px #808080 solid;
}

/* --- キャプションエリア ---*/
ul.thumbnail dd {
    /* キャプションエリアのマージン（上、左右、下）*/
    margin: 0 0 3px;
    /* キャプションエリアの高さ */
    height: 6.5em;
    line-height: 120%
}

/* --- clearfix --- */
.clearFix:after {
    content: ". ";
    display: block;
    height: 0;
    clear: both;
    visibility: hidden;
}
.clearFix {
    min-height: 1px;
}
"""

# CONTENT_HTML % (title, date, title, list_item<li>)
CONTENT_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>%s</title>
    <link rel="stylesheet" type="text/css" href="list.css" media="all">
    <meta name="description" content="panorama view list">
</head>
<body>
    <div align="right">
        <font size="4">Updated on %s</font><br/>
        <font size="2">Scripted by Kohei Matsumoto</font>
    </div>
    <h2>%s</h2>
    <ul class="thumbnail clearFix">
    %s
    </ul>
    <br><br>
    VR対応ブラウザでご覧ください (対応確認済ブラウザ：Chrome, Firefox, Edge, Safari)
</body>
</html>
"""

#ITEM_HTML % (name(html_path), name(img_path), name(html_path), name(title), description)
ITEM_HTML = """
<li>
    <dl>
        <dt><a href="view/%s.html" target="_top"><img src="resize/%s.jpg" alt="Photo" width="200" height="100"></a></dt>
        <dd><strong><a href="view/%s.html" target="_top">%s</a></strong><br> %s
        </dd>
    </dl>
</li>
"""

# CONTENT_HTML_VIEW % (name(title), name(img_path))
CONTENT_HTML_VIEW = """
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>%s</title>
<meta name="description" content="panorama view">
<script src="https://aframe.io/releases/0.4.0/aframe.min.js"></script>
</head>

<body>
<a-scene>
<a-sky src="../pics/%s.jpg" rotation="0 0 0"></a-sky>
</a-scene>
</body>
</html>
"""


######################
###### functions #####
######################

def makecss(path):
    """ makecss 関数
            生成する HTML コードに伴う CSS ファイルを作成
        * out : void
        * path : CSS ファイル作成先ディレクトリのパス
    """
    csspath = '%s/list.css' % path
    #os.system('touch %s' % csspath)
    open(csspath, 'w').write(CONTENT_CSS)
    return

def makehtml(imgs, path, title=None):
    """ makehtml 関数
            パノラマ画像閲覧のための HTML コードの生成
        * out : void
        * igms : 画像一覧(thumbnail)に入れる画像のパラメタのリスト
            --> [(name, description), ...]
    """
    title = title if title is not None else 'untitled'
    if os.path.exists('%s/view' % path) is False:
        os.system('mkdir %s/view' % path)
    list_items = ""
    for params in imgs:
        # add liss item (for index.html)
        list_items = list_items + ITEM_HTML % (params[0], params[0], params[0], params[0], params[1] if params[1] is not None else '')

        # generate HTML file (to view individually)
        open('%s/view/%s.html' % (path, params[0]), 'w').write(CONTENT_HTML_VIEW % (params[0], params[0]))

    # generate HTML file (view list)
    open('%s/index.html' % path, 'w').write(CONTENT_HTML % (title, str(datetime.date.today()), title, list_items))
    return



################
##### main #####
################

if __name__ == '__main__':

    ### --- directory specification --- ###
    # get directory path from command-line arguments
    if len(sys.argv) > 1:
        PATH = sys.argv[1]
    else:
        print("[Input Error] Please enter as follows.")
        print("--> $ python make_pnrm_html.py [directory path]")
        sys.exit()

    # Confirm existence of specified directory
    if os.path.exists(PATH) is False:
        print("[Directory Existence Error] %s is not found." % PATH)
        sys.exit()

    # Confirm existence of `pics` directory
    if os.path.exists(PATH + '/pics') is False:
        print("[Directory Existence Error] %s/pics is not found." % PATH)


    ### --- get setting --- ###
    # Confirm existence of `setting.json` file
    if os.path.exists(PATH + '/setting.json') is False:
        print("[Warning] %s/setting.json is not found." % PATH)
        SETTING = None

    else:
        # open JSON file & decoding JSON
        try:
            SETTING = json.loads(
                open('%s/setting.json' % PATH, 'r').read()
            )
        except json.decoder.JSONDecodeError:
            print("[Warning] raised JSON Decode Error.")
            SETTING = None


    ### --- generate HTML (and CSS)--- ###
    # prepate imgs (image parameter array) to use argument of makehtml function
    img_list = []

    # load json and files
    names_list = []
    if SETTING is not None:
        # load setting (JSON)
        for params in SETTING:
            # Comfirm existence of key `name`
            if 'filename' in params:
                name = params['filename']
            elif 'fn' in params:
                name = params['fn']
            else:
                print("[Name Key Existence Error] `filename` key is undefined.")
                continue
            names_list.append(name)

            # Confirm existence of key `description`
            if 'description' in params:
                description = params['description']
            elif 'desc' in params:
                description = params['desc']
            else:
                print("[Warning] `description` key is not undefined. (filename:%s)" % name)
                description = None
            img_list.append((name, description))

    # resize image directory
    if os.path.exists('%s/resize' % PATH) is False:
        os.system('mkdir %s/resize' % PATH)

    # search files (pics directory)
    files = os.listdir('%s/pics/' % PATH)
    pbar = tqdm(total=len(files))
    for file in files:
        pbar.set_description("resizing")
        pbar.update(1)

        # do processing only JPEG file (you cat change only JPEG file -> image files) (:*1)
        #if not file[-4:] in [".JPG", ".jpg", ".png", ".PNG"]:
        if not file[-4:] == ".jpg":
            continue

        # resize
        os.system('convert -resize 200x %s/pics/%s %s/resize/%s' % (PATH, file, PATH, file))

        # ignore the files included in the SETTING(setting.json)
        if file[:-4] in names_list:
            continue
        img_list.append((file[:-4], None))

    # get page title from command-line arguments
    if len(sys.argv) > 2:
        TITLE = sys.argv[2]
    else:
        print("[Warning] Page title is not entered")
        TITLE = None

    # generate HTML file
    makehtml(imgs=img_list, path=PATH, title=TITLE)

    # gennerate CSS file
    makecss(PATH)


    ### --- complete --- ###
    print('complete')




















