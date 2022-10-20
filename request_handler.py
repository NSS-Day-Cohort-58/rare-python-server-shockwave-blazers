from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from views.categories_requests import create_category, delete_category, get_all_categories, get_single_category, update_category
from views.comment_requests import get_all_comments, get_single_comment
from views.post_requests import create_post, delete_post, get_all_posts, get_single_post, update_post
from views.reaction_requests import get_all_reactions, get_single_reaction
from views.subscriptions_requests import delete_subscription, get_all_subscriptions, get_single_subscription, update_subscription
from views.tags_requests import get_all_tags, get_single_tag

from views.user import create_user, login_user, get_single_user,get_all_user


class HandleRequests(BaseHTTPRequestHandler):
    """Handles the requests to this server"""

    def parse_url(self):
        """Parse the url into the resource and id"""
        path_params = self.path.split('/')
        resource = path_params[1]
        if '?' in resource:
            param = resource.split('?')[1]
            resource = resource.split('?')[0]
            pair = param.split('=')
            key = pair[0]
            value = pair[1]
            return (resource, key, value)
        else:
            id = None
            try:
                id = int(path_params[2])
            except (IndexError, ValueError):
                pass
            return (resource, id)

    def _set_headers(self, status):
        """Sets the status code, Content-Type and Access-Control-Allow-Origin
        headers on the response

        Args:
            status (number): the status code to return to the front end
        """
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        """Sets the OPTIONS headers
        """
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods',
                         'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers',
                         'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def do_GET(self):
        """Handle Get requests to the server"""
        # Set the response code to 'Ok'
        self._set_headers(200)
        response = {}  # Default response

        # Parse URL and store entire tuple in a variable
        resource, id = self.parse_url()
        if resource == "posts":
            if id is not None:
                response = get_single_post(id)

            else:
                response = get_all_posts()

        elif resource == "categories":
            if id is not None:
                response = get_single_category(id)

            else:
                response = get_all_categories()

        elif resource == "subscriptions":
            if id is not None:
                response = get_single_subscription(id)

            else:
                response = get_all_subscriptions()

        elif resource == "reactions":
            if id is not None:
                response = get_single_reaction(id)

            else:
                response = get_all_reactions()

        elif resource == "tags":
            if id is not None:
                response = get_single_tag(id)

            else:
                response = get_all_tags()

        elif resource == "users":
            if id is not None:
                response = get_single_user(id)

            else:
                response = get_all_user()

        elif resource == "comments":
            if id is not None:
                response = get_single_comment(id)

            else:
                response = get_all_comments()

        self.wfile.write(response.encode())

    def do_POST(self):
        """Make a post request to the server"""
        self._set_headers(201)
        content_len = int(self.headers.get('content-length', 0))
        post_body = json.loads(self.rfile.read(content_len))
        response = ''
        resource, _ = self.parse_url()
        new_thing = None

        if resource == 'login':
            response = login_user(post_body)
        if resource == 'register':
            response = create_user(post_body)

        if resource == "posts":
            new_thing = create_post(post_body)

        if resource == "category":
            new_thing = create_category(post_body)
        
        self.wfile.write(response.encode())

        

        # Encode the new thing and send in response
       

    def do_PUT(self):
        """Handles PUT requests to the server"""
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

        success = False

        if resource == "posts":
            success = update_post(id, post_body)

    # rest of the elif's
        elif resource == "subscriptions":
            success = update_subscription(id, post_body)

        elif resource == "categories":
            success = update_category(id, post_body)

        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())

    def do_DELETE(self):
        """Handle DELETE Requests"""
        # Set a 204 response code
        self._set_headers(204)

    # Parse the URL
        (resource, id) = self.parse_url(self.path)

    # Delete a single post from the list
        if resource == "posts":
            delete_post(id)

        if resource == "subscription":
            delete_subscription(id)

        if resource == "category":
            delete_category(id)

        if resource == "user":
            self._set_headers(405)

        self.wfile.write("".encode())


def main():
    """Starts the server on port 8088 using the HandleRequests class
    """
    host = ''
    port = 8088
    HTTPServer((host, port), HandleRequests).serve_forever()


if __name__ == "__main__":
    main()
