import configparser
from flask import Flask, request, jsonify, redirect
from urlshortener import URLShortener

app = Flask(__name__)

# Read the configuration from the INI file
config = configparser.ConfigParser()
config.read('config.ini')

# Retrieve the values from the 'URLShortener' section
database_file = config.get('URLShortener', 'database_file')
website_url = config.get('URLShortener', 'website_url')

# Initialize the URLShortener instance
shortener = URLShortener(database_file, website_url)


@app.route('/short', methods=['GET', 'POST'])
def shorten_url():
    if request.method == 'POST':
        original_url = request.form['url']
    else:
        original_url = request.args.get('url')
    if not original_url:
        return jsonify({'error': 'URL cannot be empty'}), 400
    if shortener.is_shortened_url(original_url):
        return jsonify({'shortened_url': shortener.get_shortened_url(original_url)})

    shortened_url = shortener.shorten_url(original_url)
    return jsonify({'shortened_url': shortened_url})


@app.route('/<shortcode>', methods=['GET'])
def redirect_url(shortcode):
    original_url = shortener.get_original_url(shortcode)
    if original_url is None:
        return jsonify({'error': 'URL not found'}), 404
    return redirect(original_url, code=302)


if __name__ == '__main__':
    app.run()
