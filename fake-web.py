import os
import sys
import uuid
import time
import jinja2
import numpy as np


class Page:
    def __init__(self, filename):
        self.filename = filename
        self.links = set()
        self._n_backlinks = -1

    def __repr__(self):
        return f"Page[filename={self.filename}, backlinks={self._n_backlinks} links={self.links}]"

    def render_html(self):
        return jinja2.Template("""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{{ page_title }}</title>
        </head>
        <body>
            <h1>{{ page_title }}</h1>
            <ol>
                {% for link in links %}
                <li><a href="{{link}}">{{ link }}</a></li>
                {% endfor %}
            </ol>
        </body>
        </html>
        """).render(
            page_title=self.filename,
            links=sorted(self.links))


def fake_web_pages(n_pages, mean_backlinks, std_backlinks):
    print('Creating pages and backlink counts in memory...')
    pages = [Page(f"page_{i}_{uuid.uuid4()}.html") for i in range(n_pages)]
    ipages = np.arange(len(pages))
    backlinks_per_page = np.random.normal(mean_backlinks, std_backlinks, len(pages))
    print('OK')
    count = 0
    g = np.random.Generator(np.random.PCG64())
    for page, n_backlinks in zip(pages, backlinks_per_page):
        count += 1
        if count % 10000 == 0:
            print(f'[backlinks-loop] time={time.time():.2f}, count={count} ({count/n_pages*100.0:.2f}%)')
        n_backlinks = max(0, int(round(n_backlinks)))
        page._n_backlinks = n_backlinks
        if n_backlinks > 0:
            selected_backlinks = g.choice(ipages, n_backlinks, replace=False)
            for backlink_ix in selected_backlinks:
                pages[backlink_ix].links.add(page.filename)
    for i in ipages:
        yield i, pages[i]


def main():
    if len(sys.argv) < 2:
        sys.exit(f"Usage: {sys.argv[0]} <output_dir> (n_pages) (mean_backlinks) (std_backlinks)")

    output_dir = sys.argv[1]
    n_pages = 10000 if len(sys.argv) < 3 else int(sys.argv[2])
    mean_backlinks = 5.0 if len(sys.argv) < 4 else float(sys.argv[3])
    std_backlinks = 2.0 if len(sys.argv) < 5 else float(sys.argv[4])

    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    index_links = set()

    for i, page in fake_web_pages(n_pages, mean_backlinks, std_backlinks):
        output_path = os.path.join(output_dir, page.filename)
        print(f"[{(i+1)/n_pages*100:.2f}% - {time.time():.2f}] Rendering to {output_path}: page={page.filename}, backlinks={page._n_backlinks}, links={len(page.links)}")
        index_links.add(page.filename)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(page.render_html())

    index_path = os.path.join(output_dir, "index.html")
    index_page = Page(index_path)
    index_page.links = index_links
    with open(index_path, "w", encoding="utf-8") as f:
        f.write(index_page.render_html())
    print("Wrote index page. Done.")

if __name__ == "__main__":
    main()
