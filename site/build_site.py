#!/usr/bin/python
# -*- coding: utf-8 -*-

# import site_defs
# import templates
import markdown
import os
import pprint


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

def render_markup(source, source_form):
    if source_form == "None":
        return "<pre>\n%s\n</pre>\n" % source
    if source_form == "markdown":
        return markdown.markdown(source)

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

def files(some_dir):
    for filename in os.listdir("src"):
        if os.path.isfile(os.path.join("src", filename)):
            yield filename

def parse_source_data(page):
    parts = []
    process = page
    while True:
        index = process.find("{%")
        if index == -1:
            if len(process) > 0:
                parts.append(("passthrough", process))
                process = ""
            break # No more parts to process
        if index > 0:
                parts.append(("passthrough", process[:index]))
        process = process[index+2:]
        index = process.find("%}")
        if index == -1:
            print "UNMATCHED {%, aborting unprocessed"
            if len(process) > 0:
                parts.append(("passthrough", process))
                process = ""
            break # No more parts to process
        if index > 0:
                parts.append(("process", process[:index]))
                process = process[index+2:]
    return parts

def process_directive(raw_directive):
    if "panel(" in raw_directive:
        raw_id = raw_directive[:raw_directive.find("=")]
        raw_id = raw_id.strip()
        part_args = raw_directive[raw_directive.find("panel(")+7:]
        filename = part_args[:part_args.find('"')]

        with open("src/"+filename) as f:
            raw_contents = f.read()

        meta, source_data = get_meta(raw_contents)
        return source_data

    return "??"+raw_directive  ## DIRECTIVE PASS IN, BUT UNKNOWN

def process_directives(source_data):
    result = []
    for page_part_type, page_part in parse_source_data(source_data):
        if page_part_type == "passthrough":
            result.append(page_part)
        elif page_part_type == "process":
            part_result = process_directive(page_part)
            print page_part
            print "PRE LEN", len(part_result)
            while "{%" in part_result: # panels may contain sub panels after all.
                print "RECURSING!"
                part_result = process_directives(part_result)
                print "POST LEN", len(part_result)
            result.append(part_result)
        else:
            result.append(page_part)
    return "".join(result)

site_meta = {}
for filename in files("src"):
    print filename
    stripped = filename[:filename.rfind(".")]
    result_file = stripped.lower() + ".html"
    source_data = open("src/"+ filename ).read()

    meta, source_data = get_meta(source_data)
    meta["_stripped"] = stripped
    meta["_source_data"] = source_data
    meta["_result_file"] = result_file

    site_meta[filename] = meta

sidebar = "<br>\n" + build_sidebar(site_meta, " <br> ")
count = 0

for filename in files("src"):
    meta, source_data = site_meta[filename],site_meta[filename]["_source_data"]
    if meta.get("skip", False):
        print "Skipping", filename
        continue
    print "PROCESSING", filename

    stripped = meta["_stripped"]
    result_file = meta["_result_file"]

    tmpl_name = meta.get("template", "None")
    source_form = meta.get("source_form", "None")
    source_data = process_directives(source_data)
    processed = render_markup(source_data, source_form)

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

try:
    import build_site_local
    from build_site_local import run_local

    run_local(site_meta, process_directives)
    print "LOCAL RUN"

except ImportError:
    print "No build_site_local customisations"

print "Success!", count, "files published."
