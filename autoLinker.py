from importlib.machinery import all_suffixes
import json
import os
import re

WIKI = "wiki"
LINK_TEXT = "Links: "
TAGS_TEXT = "Tags: "
WIKI_DATA = "wikidata"

LINK_PATTERN = "\[([\w\s\d]*)\]"

EOW = [",", ";", "!", ".", " ", "\n", "\t", "—"]

from config import WikmdConfig

cfg = WikmdConfig()

def auto_link(filename):
    with open(filename) as f:
        fin = f.read()
    doc_length = len(fin)
    links = re.finditer(LINK_PATTERN, fin)
    padding = 0
    for link in links:
        index = link.end() + padding
        if index == doc_length + padding:
            url = fin[link.start()+padding+1:index-1]
            fin = fin[:index] + "(" + url + ")" + fin[index:]
            padding += len(url) + 2
            break
        if fin[index] == '(': 
            continue
        else:
            url = fin[link.start()+padding+1:index-1]
            fin = fin[:index] + "(" + url + ")" + fin[index:]
            padding += len(url) + 2
                
    with open(filename, "w") as f:
        f.write(fin)

def total_auto_link(filename):
    linkables = set()
    # data = ["states", "races", "subraces"]
    # for doc in data:
    #     with open(os.path.join(WIKI_DATA, f"{doc}.txt")) as f:
    #         for line in f.readlines():
    #             linkables.add(line.strip())

    for mdfile in os.listdir(cfg.wiki_directory):
        path = os.path.join(cfg.wiki_directory, mdfile)
        if (".DS_Store" in path) or ("img" in path) or (".git" in path): continue
        linkables.add(mdfile.replace(".md", ""))

    with open(filename) as f:
        fin = f.read()

    flexnames_to_file = {}
    with open(os.path.join(WIKI_DATA, "autolink.json")) as f:
        file_to_flexnames = json.load(f)
    for md_file, flexnames in file_to_flexnames.items():
        for flexname in flexnames:
            flexnames_to_file[flexname] = md_file

    for linkable in linkables:
        padding = 0
        links = re.finditer(linkable, fin, re.IGNORECASE)
        for link in links:
            index = link.end() + padding
            try:
                if (fin[index] not in EOW):
                    continue
                if (fin[link.start()-1] not in EOW):
                    continue
                else:
                    url = fin[link.start()+padding:index]
                    insertion = f"[{url}]({linkable})"
                    fin = fin[:index-len(url)] + insertion + fin[index:]
                    padding += len(url) + 4
            except:
                pass

    for flexname in flexnames_to_file.keys():
        padding = 0
        links = re.finditer(flexname, fin, re.IGNORECASE)
        for link in links:
            index = link.end() + padding
            # start_index = link.start() + padding
            try:
                # if (fin[start_index-1] != " " or fin[start_index-1] != "\n"): continue
                if (fin[index] not in EOW):
                    continue
                if (fin[link.start()-1] not in EOW):
                    continue
                else:
                    match = fin[link.start()+padding:index]
                    match_length = len(match)
                    insertion = f"[{match}]({flexnames_to_file[flexname.lower()]})"
                    # print("insertion:", insertion)
                    fin = fin[:index-match_length] + insertion + fin[index:]
                    padding += len(insertion) - match_length
            except:
                pass

    with open(filename, "w") as f:
        f.write(fin)

def main():
    # for filename in os.listdir(cfg.wiki_directory):
    #     path = os.path.join(cfg.wiki_directory, filename)
    #     if (".DS_Store" in path) or ("img" in path) or (".git" in path): continue
    #     pass
    total_auto_link("wiki/ztest.md")
    auto_link("wiki/ztest.md")

if __name__ == '__main__':
    main()