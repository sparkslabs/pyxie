#!/usr/bin/python
# -*- coding: utf-8 -*-

# import site_defs
# import templates
import markdown
import os


def get_meta(source):
    meta = {}
    if source.startswith("---\n"):
        source = source[4:]
        pos = source.find("---\n")
        meta_lines = source[:pos].split("\n")
        source = source[pos+4:]
        if meta_lines[-1]=="":
            meta_lines = meta_lines[:-1]
            for line in meta_lines:
                pos = line.find(":")
                key = line[:pos]
                value = line[pos+1:].strip()
                meta[key] = value
    return meta, source

def prepare_source(source, source_form):
    if source_form == "None":
        return "<pre>\n%s\n</pre>\n" % source
    if source_form == "markdown":
        return markdown.markdown(source)


site_meta = {}

for filename in os.listdir("src"):
    stripped = filename[:filename.rfind(".")]
    result_file = stripped.lower() + ".html"
    source_data = open("src/"+ filename ).read()

    meta, source_data = get_meta(source_data)
    meta["_stripped"] = stripped
    meta["_source_data"] = source_data
    meta["_result_file"] = result_file

    site_meta[filename] = meta

def build_sidebar(site_meta, divider):

    sidebar_parts = []
    filenames = site_meta.keys()
    filenames.sort()
    for filename in filenames:
        page_meta = site_meta[filename]
        if page_meta.get("skip", False):
            continue
        stripped = filename[:filename.rfind(".")]
        result_file = stripped.lower() + ".html"
        link = '<a href="%s">%s</a>' % (result_file, page_meta.get("name", "None"))
        sidebar_parts.append(link)

    return divider.join(sidebar_parts)

sidebar = "<br>\n" + build_sidebar(site_meta, " <br> ")
count = 0

for filename in os.listdir("src"):
    stripped = filename[:filename.rfind(".")]
    result_file = stripped.lower() + ".html"

    meta, source_data = site_meta[filename],site_meta[filename]["_source_data"]

    if meta.get("skip", False):
        print "Skipping", filename
        continue

    tmpl_name = meta.get("template", "None")
    source_form = meta.get("source_form", "None")
    processed = prepare_source(source_data, source_form)

    tmpl = open("templates/%s.tmpl" % tmpl_name, "rb").read()

    result_html = tmpl
    result_html = result_html.replace("{% page.body %}", processed)
    result_html = result_html.replace(u"{% site.sidebar %}", str(sidebar))
    result_html = result_html.replace(u"{% page.updated %}", meta.get("updated", "na"))
    try:
        result_html = result_html.replace(u"{% page.title %}",meta.get("title", meta["_stripped"]))
    except KeyError as e:
        print "KEYERROR meta",meta
        raise

    out = open("site/"+ result_file,"w")
    out.write(result_html)
    out.close()
    count += 1

print "Success!", count, "files published."
