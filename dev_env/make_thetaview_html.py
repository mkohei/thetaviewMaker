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
* 1.03 (2017/06/03)
    - layout 微修正 (thetaview/index.html の話)
    - リスト表示の幅による列挙個数の調整表示
* 2.00 (2017/06/04)
    - layout の大幅修正 (それに伴う setting.json 等の変更)
    - setting.json の必須化(?)

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
        /* min-width: 660px; */
        margin: 0;
        /* リストエリアのパッディング（上、左右、下）*/
        /* padding: 30px 0 0; */
        list-style-type: none;
    }
    /* --- リスト項目 --- */
    
    ul.thumbnail li {
        /* 項目の幅 */
        width: 220px;
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
        /* margin-bottom: 5px; */
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
    
    hr.bigline {
        width: 50%;
        margin-bottom: 60px;
    }
    
    h3.smalltitle {
        margin-top: 30px;
    }
"""

# CONTENT_HTML % (title, date, title, big_titles)
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
    <h1>%s</h1>
    <hr size="3" color="black">
    %s
    <br><br>
    VR対応ブラウザでご覧ください (対応確認済ブラウザ：Chrome, Firefox, Edge, Safari)
</body>
</html>
"""

# BIGTITLE_HTML % (big_title, small_titles)
BIGTITLE_HTML = """
<h2>%s</h2>
%s
<hr class="bigline" align="left">
"""

# SMALLTITLE_HTML % (small_title, image_items)
SMALLTITLE_HTML = """
<h3 class="smalltitle">%s</h3>
<ul class="thumbnail clearFix">
%s
</ul>
"""

# IMAGE_ITEM_HTML % (name(html_path), name(img_path))
IMAGE_ITEM_HTML = """
<li>
    <dl>
        <dt><a href="view/%s.html" target="_top"><img src="resize/%s.jpg" alt="Photo" width="200" height="100"></a></dt>
    </dl>
</li>
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
    """ 生成する HTML コードに伴う CSS ファイルを作成

        Parameters
        ----------
        * path: CSS ファイル作成先ディレクトリのパス

        Returns
        -------
        * void

    """
    csspath = '%s/list.css' % path
    #os.system('touch %s' % csspath)
    open(csspath, 'w').write(CONTENT_CSS)
    return


def makehtml_old(imgs, path, title=None):
    """ パノラマ画像閲覧のための HTML コードの生成

        Parameters
        ----------
        * igms: 画像一覧(thumbnail)に入れる画像のパラメタのリスト
            --> [(name, description), ...]
        * path: HTML ファイル作成先ディレクトリのパス
        * title: ページタイトル

        Returns
        -------
        * void
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


def make_smalltitle(smalltitle, imgs):
    """ small_title 部分の HTML コードを作成

        Paramters
        ---------
        * smalltitle: str
            small title
        * imgs: str array
            表示する画像ファイル名リスト (without extension)

        Returns
        ----
        * stcode: small_title 部分の HTML コード
    """
    img_items = ""
    for imgname in imgs:
        img_items += IMAGE_ITEM_HTML % (imgname, imgname)
    return SMALLTITLE_HTML % (smalltitle, img_items)


def make_bigtitle(bigtitle, smalltitle_codes):
    """ big_title 部分の HTML コードの作成

        Parameters
        ----------
        * bigtitle: str
            big title
        * smalltitle_codes: str array
            small title 部分の HTML コードのリスト

        Returns
        -------
        * btcode: big_title 部分の HTML コード
    """
    smalltitles = ""
    for stcode in smalltitle_codes:
        smalltitles += stcode
    return BIGTITLE_HTML % (bigtitle, smalltitles)


def makehtml(path, bigtitle_codes, title=None):
    """ パノラマ画像閲覧用のための HTML コードの生成

        Parameters
        ----------
        * path: str
            ファイルを作成するディレクトリへのパス
        * bigtitle_codes: str array
            big title 部分の HTML コードリスト
        * title: str
            ページタイトル

        Returns
        -------
        * void
    """
    # conmfirmation of title is defined or not
    title = title if title is not None else 'untitled'

    bigtitles = ""
    for btcode in bigtitle_codes:
        bigtitles += btcode

    # generate HTML file (view list)
    open('%s/index.html' % path, 'w').write(CONTENT_HTML % (title, str(datetime.date.today()), title, bigtitles))
    return


def resize(path, imgs):
    """ リサイズ

        Parameters
        ----------
        * path: resize ディレクトリを置くディレクトリへのパス
        * imgs: リサイズする画像のリスト

        Returns
        -------
        * void
    """
    # resize image directory
    if os.path.exists('%s/resize' % path) is False:
        os.system('mkdir %s/resize' % path)

    #pbar = tqdm(total=len(imgs))
    for img in imgs:
        #pbar.set_description("resizing")
        #pbar.update(1)

        # resize
        file = img + ".jpg"
        os.system('convert -resize 200x %s/pics/%s %s/resize/%s' % (path, file, path, file))
    return


def make_view(path, imgs):
    """ 全天球閲覧ページの作成

        Parameters
        ----------
        * path: view ディレクトリを置くディレクトリへのパス
        * imgs: 閲覧ページで表示する画像リスト

        Returns
        -------
        * void
    """
    # view directory
    if os.path.exists('%s/view' % path) is False:
        os.system('mkdir %s/view' % path)

    #pbar = tqdm(total=len(imgs))
    for img in imgs:
        #pbar.set_description("making view")
        #pbar.update(1)

        open('%s/view/%s.html' % (path, img), 'w').write(CONTENT_HTML_VIEW % (img, img))
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
            sys.exit()

    # get page title from command-line arguments
    if len(sys.argv) > 2:
        TITLE = sys.argv[2]
    else:
        print("[Warning] Page title is not entered.")
        TITLE = None

    ### --- generate HTML (and CSS)--- ###
    # lists
    allimgs, bigtitle_codes = [], []

    # load setting (JSON)
    for bt_params in SETTING:
        # big title
        if 'bigtitle' in bt_params:
            bigtitle = bt_params['bigtitle']
        elif 'b' in bt_params:
            bigtitle = bt_params['b']
        else:
            print("[Name Key Existence Error] `bigtitle` key is undefined.")
            continue

        # contents (small title list)
        if 'contents' in bt_params:
            contents = bt_params['contents']
        elif 'c' in bt_params:
            contents = bt_params['c']
        else:
            ...
        smalltitle_codes = []
        for st_params in contents:
            # small title
            if 'smalltitle' in st_params:
                smalltitle = st_params['smalltitle']
            elif 's' in st_params:
                smalltitle = st_params['s']
            else:
                print("[Name Key Existence Error] `smalltitle` key is undefined.")
                continue
            # imgs
            if 'images' in st_params:
                imgs = st_params['images']
            elif 'i' in st_params:
                imgs = st_params['i']
            allimgs.extend(imgs)
            smalltitle_codes.append(
                make_smalltitle(smalltitle, imgs)
            )
        bigtitle_codes.append(
            make_bigtitle(bigtitle, smalltitle_codes)
        )

    # generate
    makehtml(PATH, bigtitle_codes, TITLE)
    makecss(PATH)
    make_view(PATH, allimgs)
    resize(PATH, allimgs)

    ### --- complete --- ###
    print('complete')




















