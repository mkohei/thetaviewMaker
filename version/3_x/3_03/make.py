#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Code to generate HTML source file to view panomara pictures automatically.

~ Preconditions ~
* The specified directory contains the `pics` directory.
  (Put the image you want to display in the `pics` directory.)
* The specified directory contains the `set.json` file.
  (If there is no file, create it.)

~ Command ~
$ python make_pnrm_html.py [dir_path]

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
* 3.00 (2018/04/11)
    - pageから生成できるように
    - layout変更
    - 正規表現使用可
* 3.01 (2018/04/12)
    - 'Last Updated'の追加
* 3.02 (2018/04/12)
    - Menuが長いと省略し一行で表示
* 3.03 (2018/04/18)
    - windowサイズに応じて横並び数を変更
"""



import os                   # confirm eistence of directory and file
import sys                  # get command-line arguments
import json                 # json
from tqdm import tqdm       # processing bar
from PIL import Image       # make thumbs
import re                   # regex
from datetime import datetime   # update date & time



###############################
########## CONSTANTS ##########
###############################
EXIF_MODEL = 272
THUMBNAIL_LEN = 200
MENU_MAX_LEN = 15



##########################
########## MAIN ##########
##########################
def main():
    ### get directory path from command-line arguments
    PATH = get_path()

    ### get set.json
    setdata = get_set_json(PATH)

    ### confirm existence of directory
    for dir in ["photos", "pages", "views", "thumbs"]:
        mkdir(PATH + "/" + dir)

    ### get image file names
    photos = get_list_byRegex(os.listdir(PATH + "/photos"), r".+\.(JPG|jpg|PNG|png)")
    thumbs = get_list_byRegex(os.listdir(PATH + "/thumbs"), r".+\.(JPG|jpg|PNG|png)")

    ### tqdm
    pbar = tqdm(total=len(photos)+1)

    ### make thumbs
    for photo in photos:
        if (photo in thumbs) is False:
            make_thumb(PATH, photo)
        pbar.update(1)

    ### make html
    make_htmls(setdata, PATH, photos)
    pbar.update(1)



###############################
########## FUNCTIONS ##########
###############################
def get_list_byRegex(flist, pattern):
    newlist = []
    for f in flist:
        if (re.fullmatch(pattern, f)):
            newlist.append(f)
    return newlist


def get_path():
    ### get path
    PATH = "."
    if len(sys.argv) > 1:
        PATH = sys.argv[1]
    
    ### confirm existence of specified directory
    if os.path.exists(PATH) is False:
        print("[Error] % is not found." % PATH)
        sys.exit()
    
    return PATH


def get_set_json(PATH):
    ### confirm existence of 'set.json' file
    if os.path.exists(PATH + "/set.json") is False:
        print("[Error] %s/set.json is not found." % PATH)
        sys.exit()
    
    else:
        ### open set.json & decoding
        try:
            setdata = json.loads(
                open("%s/set.json" % PATH, "r").read()
            )
        except json.decoder.JSONDecodeError:
            print("[Error] raised JSON Decode Error.")
            sys.exit()

    return setdata


def mkdir(dir):
    if os.path.exists(dir) is False:
        os.mkdir(dir)


def make_index_html(url):
    source = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>album</title>
        </head>
        <body>
        <script>
        window.location = "{}"
        </script>
        </body>
        </html>
    """
    return source.format(url)


def make_htmls(setdata, PATH, photos):
    nav = make_nav_source(setdata)

    for j, page in enumerate(setdata):
        sections_source = ""
        for i, section in enumerate(page["sections"]):
            images_source = ""
            for image in section["images"]:
                for img in get_list_byRegex(photos, image):
                    if (isTakenByTheta(PATH, img)):
                        images_source += make_theta_source(img)
                        open("{}/views/{}.html".format(PATH, img), "w").write(make_theta_view_source(PATH, img))
                    else:
                        images_source += make_image_source(img)
            sections_source += make_section_source(i, section["secname"], images_source)
        open("{}/pages/{}.html".format(PATH, page["pagename"]), "w").write(
            make_html_source(
                page["pagename"], nav, 
                make_content_source(page["pagename"], sections_source)
            )
        )
        if j==0:
            open("{}/index.html".format(PATH), "w").write(make_index_html("{}/pages/{}.html".format(PATH, page["pagename"])))


def make_nav_source(setdata):
    pageitems = ""
    for page in setdata:
        secitems = ""
        for i, sec in enumerate(page["sections"]):
            secitems += make_sec_item(i, sec["secname"])
        pageitems += make_page_item(page["pagename"]+".html", page["pagename"], secitems)
    return pageitems


def make_page_item(url, name, secitems):
    # url, name, secitems
    source = """
        <li class="drawer-dropdown">
        <a class="drawer-menu-item" data-target="#" href="{}" data-toggle="dropdown" role="button" aria-expanded="false">
        {} <span class="drawer-caret"></span>
        </a>
        <ul class="drawer-dropdown-menu">
        {}
        </ul>
        </li>
    """
    return source.format(url, make_abbreviation(name), secitems)


def make_sec_item(num, name):
    # num, name
    source = """
        <li><a class="drawer-dropdown-menu-item" href="#{}">{}</a></li>
    """
    return source.format(num, make_abbreviation(name))


def make_html_source(title, nav, content):
    # title, nav, datetime, content
    source = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>{}</title>
        <!-- drawer.css -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/drawer/3.2.2/css/drawer.min.css">
        <!-- jquery & iScroll -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/iScroll/5.2.0/iscroll.min.js"></script>
        <!-- drawer.js -->
        <script src="https://cdnjs.cloudflare.com/ajax/libs/drawer/3.2.2/js/drawer.min.js"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/3.3.7/js/bootstrap.min.js"></script>
        </head>
        <style>
        body {{
        margin: 0;
        padding: 0 2vw 0 1.5vw;
        }}
        img {{
        width: 31vw;
        margin: 0 0.5vw 0 0.5vw;
        }}
        @media screen and (min-width: 540px) {{
        img {{
        width: 23vw;
        }}
        }}
        @media screen and (min-width: 720px) {{
        body {{
        padding: 0 2.5vw 0 2vw;
        }}
        img {{
        width: 18vw;
        }}
        }}
        ul.thumbnail {{
        list-style-type: none;
        margin: 0;
        padding: 0;
        display: block;
        }}
        li.thumbnail {{
        float: left;
        margin: 0;
        }}
        br {{
        clear: left;
        }}
        div.section {{
        clear: left;
        padding: 0;
        margin: 20px 0 20px 0;
        }}
        h2 {{
        margin: 20px 0 0 10vw;
        }}
        a.drawer-dropdown-menu-item {{
        white-space: nowrap;
        }}
        a.drawer-menu-item {{
        white-space: nowrap;
        }}
        </style>
        <body class="drawer drawer--left">
        <header role="banner">
        <button type="button" class="drawer-toggle drawer-hamburger">
        <span class="sr-only">toggle navigation</span>
        <span class="drawer-hamburger-icon"></span>
        </button>
        <nav class="drawer-nav" role="navigation">
        <ul class="drawer-menu">
        {}
        </ul>
        </nav>
        </header>
        <main role="main">
        <!-- Page content -->
        <div style="text-align: right">
        Last Updated: {}
        </div>
        {}
        <div style="text-align: right; font-size: small;">
        Scripted by Kohei Matsumoto
        </div>
        </main>
        <script>
        $(document).ready(function() {{
        $(".drawer").drawer();
        }});
        </script>
        </body>
        </html>
    """
    return source.format(title, nav, datetime.now().strftime("%Y/%m/%d_%H:%M:%S"), content)


def make_content_source(pagename, sections_source):
    # title, sections_source
    source = """
        <h2>{}</h2>
        {}
    """
    return source.format(pagename, sections_source)


def make_section_source(num, secname, images_source):
    # num, secname, images_source
    source = """
        <div class="section" id="{}">{}</div>
        <ul class="thumbnail">
        {}
        </ul>
        <br>
    """
    return source.format(num, secname, images_source)


def make_image_source(name):
    # name, name
    source = """
        <li class="thumbnail">
        <a href="../photos/{}">
        <img src="../thumbs/{}">
        </a>
        </li>
    """
    return source.format(name, name)


def make_theta_source(name):
    # name, name
    source = """
        <li class="thumbnail">
        <a href="../views/{}.html">
        <img src="../thumbs/{}">
        </a>
        </li>
    """
    return source.format(name, name)


def make_thumb(PATH, filename):
    # open
    img = Image.open(PATH + "/photos/" + filename)
    # resize
    r = THUMBNAIL_LEN / min(img.width, img.height)
    img2 = img.resize((int(img.width*r), int(img.height*r)), Image.LANCZOS)
    # trim
    cx, cy, l = img2.width//2, img2.height//2, THUMBNAIL_LEN//2
    img3 = img2.crop((cx-l, cy-l, cx+l, cy+l))
    # save
    img3.save(PATH + "/thumbs/" + filename)

    return "THETA" in img._getexif()[EXIF_MODEL]


def isTakenByTheta(PATH, filename):
    # open
    img = Image.open(PATH + "/photos/" + filename)
    return "THETA" in img._getexif()[EXIF_MODEL]


def make_theta_view_source(PATH, filename):
    source = """
        <!DOCTYPE html>
        <html lang="ja">
        <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <meta http-equiv="X-UA-Compatible" content="ie=edge">
        <title>{}</title>
        <script src="https://aframe.io/releases/0.4.0/aframe.min.js"></script>
        </head>
        <body>
        <a-scene>
        <a-sky src="../photos/{}" rotation="0 0 0"></a-sky>
        </a-scene>
        </body>
        </html>
    """
    return source.format(filename, filename)


def make_abbreviation(name):
    if len(name) > MENU_MAX_LEN:
        return name[:MENU_MAX_LEN] + "..."
    else:
        return name[:]



##########################
########## MAIN ##########
##########################
if __name__ == "__main__":
    main()
