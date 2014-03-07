from bs4 import BeautifulSoup
import re
import os

link_exp = re.compile('https?://')


def is_external_source(url):
    return link_exp.match(url)


def open_file(rel_path):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path)
    return f


def open_output_file(rel_path):
    script_dir = os.path.dirname(__file__)
    abs_file_path = os.path.join(script_dir, rel_path)
    f = open(abs_file_path, 'w')
    return f


def get_html():
    soup = BeautifulSoup(open_file("h5bp/index.html"))
    return soup


def output(soup):
    print soup.find_all('script')[0]['src']
    f = open_output_file('output.html')
    f.write(str(soup))
    f.close()
    return


def append_media_url(url):
    return


def script_converter(soup):
    for script in soup.find_all('script'):
        if script.has_attr('src'):
            print 'src'
            if is_external_source(script['src']):
                pass
            else:
                print "non http"
                script['src'] = 'changedsrc'
    return soup


def css_converter(soup):
    for link in soup.find_all('link'):
        if link.has_attr('href'):
            if is_external_source(link['href']):
                pass
            else:
                link['href'] = 'changedsrc'
    return soup
