# URL Shortener API

The URL Shortener API is a simple web service that allows you to shorten long URLs into shorter, more manageable ones. It provides an easy way to generate unique shortcodes for URLs and redirect users to the original URLs when they access the shortened links.


- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Configuration](#configuration)
- [Contributing](#contributing)

## Features

- Shorten long URLs into shorter, unique shortcodes.
- Redirect users to the original URLs when accessing the shortened links.
- Supports both GET and POST methods for shortening URLs.
- Checks if the URL is already shortened to prevent duplicate entries.
- Stores the data in a configurable database file.
- Configuration options provided through a `config.ini` file.
- Uses Flask framework for the web API implementation.

## Getting Started

### Prerequisites

- Python 3.6 or higher installed.
- Flask library installed (`pip install Flask`).

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MehrunAskrnzhad/url-shortener.git
   ```
2. Navigate to the project directory:
   ```bash
   cd url-shortener
   ```
3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Edit the config.ini file to configure the database file path and the website URL.

5. Start the server:
   ```bash 
   python main.py
   ```

The URL Shortener service should now be running on http://localhost:5000.

## Usage 
### Shorten URL
To shorten a long URL, send a POST request to the /short endpoint with the url parameter containing the URL you want to shorten. Here's an example using cURL:

   ```bash
   curl -X POST -d "url=https://www.example.com" http://localhost:5000/short
   ```
The response will contain the shortened URL in JSON format:
   ```json
   {
    "shortened_url": "http://localhost:5000/abc123"
   }
   ```
### Redirect to Original URL
To access the original URL associated with a shortcode, simply make a GET request to the corresponding shortcode endpoint. For example:
   ```bash
   curl http://localhost:5000/abc123
   ```
If the shortcode exists in the database, the server will respond with a redirect to the original URL. If the shortcode does not exist, a JSON response with an error message will be returned.

## API Endpoints
- **POST / GET `/short`** - Shorten a URL
- **GET `/{shortcode}`** - Redirect to the original URL

## Configuration
The URL Shortener service can be configured using the `config.ini` file. The following configuration options are available:

- `database_file` : Path to the database file
- `website_url` : Base URL of the shortened URLs

## Contributing

Contributions to the URL Shortener project are always welcome! If you have any bug reports, feature requests, or suggestions, please open an issue on the [GitHub repository](https://github.com/MehrunAskrnzhad/url-shortener).

If you would like to contribute code, you can fork the repository, make your changes, and submit a pull request.
