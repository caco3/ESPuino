import os
import requests
import shutil

# List of all external JS  and CSS files
EXTERNAL_JS_FILES = [
    "https://cdnjs.cloudflare.com/ajax/libs/jquery/3.7.0/jquery.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.13.2/jquery-ui.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/js/bootstrap.bundle.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.16/jstree.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/toastr.js/2.1.4/toastr.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/11.0.2/bootstrap-slider.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/i18next/23.7.11/i18next.min.js",
	"https://cdnjs.cloudflare.com/ajax/libs/i18next-http-backend/2.4.2/i18nextHttpBackend.min.js",
	"https://cdn.jsdelivr.net/npm/loc-i18next@0.1.6/dist/umd/loc-i18next.min.js",
	"https://cdn.jsdelivr.net/gh/sourcefrog/natsort@f8a6b0c/natcompare.js"
]

EXTERNAL_CSS_FILES = [
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.3/css/bootstrap.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.16/themes/default/style.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.16/themes/default-dark/style.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/toastr.js/2.1.4/toastr.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/bootstrap-slider/11.0.2/css/bootstrap-slider.min.css"
]

# Additional files which are required by Font-Awesome but can not be part of the combined JS-/CSS-Files
EXTERNAL_EXTRA_FILES = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/webfonts/fa-solid-900.ttf",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/webfonts/fa-solid-900.woff2",
    "https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.16/themes/default/throbber.gif",
    "https://cdnjs.cloudflare.com/ajax/libs/jstree/3.3.16/themes/default/32px.png"
]

TEMPORARY_FOLDER = "temp"
DISTRIBUTION_FOLDER = "sd-card/zzz_html"


def fetch_url(url, use_full_url_path_for_filename=True):
    if use_full_url_path_for_filename:  # create filename based on full URL path
        filename = (url # Generate filename based on full URL path
                .replace("https://cdnjs.cloudflare.com/ajax/libs/", "")
                .replace("https://cdn.jsdelivr.net/", "")
                .replace("/", "_"))
    else: # Only use last part of the URL path as filename
        filename = url.split("/")[-1]

    print("Downloading " + url + " -> " + filename + "...")
    r = requests.get(url, allow_redirects=True)
    if r.status_code != 200:
        print("Failed to download " + url + "!")
        exit(1)

    # Fix Font-Awesome dependencies (references to the EXTERNAL_EXTRA_FILES)
    content = r.content.replace(b"../webfonts/", b"zzz_html/")
    #content = r.content

    # Save file
    filepath = TEMPORARY_FOLDER + "/" + filename
    open(filepath, "wb").write(content)
    return filename


def main():
    js_files = []
    css_files = []
    extra_files = []

    if os.path.exists(TEMPORARY_FOLDER):
        shutil.rmtree(TEMPORARY_FOLDER)
    os.makedirs(TEMPORARY_FOLDER)

    if os.path.exists(DISTRIBUTION_FOLDER):
        shutil.rmtree(DISTRIBUTION_FOLDER)
    os.makedirs(DISTRIBUTION_FOLDER)

    # Download all files
    for url in EXTERNAL_JS_FILES:
        js_files.append(fetch_url(url))
    for url in EXTERNAL_CSS_FILES:
        css_files.append(fetch_url(url))
    for url in EXTERNAL_EXTRA_FILES:
        extra_files.append(fetch_url(url, use_full_url_path_for_filename=False))

    # Combine JS- and CSS-files
    with open(DISTRIBUTION_FOLDER + '/combined.js', 'w') as outfile:
        for filename in js_files:
            with open(TEMPORARY_FOLDER + "/" + filename) as infile:
                outfile.write(infile.read())

    with open(DISTRIBUTION_FOLDER + '/combined.css', 'w') as outfile:
        for filename in css_files:
            with open(TEMPORARY_FOLDER + "/" + filename) as infile:
                outfile.write(infile.read())

    # Copy extra files
    for filename in extra_files:
        shutil.copyfile(TEMPORARY_FOLDER + "/" + filename, DISTRIBUTION_FOLDER + "/" + filename)


if __name__ == "__main__":
    main()
