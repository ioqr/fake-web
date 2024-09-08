# fake-web

Generate a set of HTML files that link to each other.

## Usage

```bash
python fake-web.py <output_dir> (pages) (mu) (sigma)
# (cd output; python -m http.server)
```

*	output_dir: The directory where the HTML files will be saved.
*	pages: (Optional) The number of pages to generate (default: 10000).
*	mu: (Optional) The average number of backlinks per page (default: 5.0).
*	sigma: (Optional) The standard deviation for backlinks (default: 2.0).
