"""
This creates a decorator that allows us to keep the documentation for each URL in memory.

When you create a function that you want to map a URL to, you do it like this:

@app.route('/')
def index():
    return 'hello'

Now, what would be nice is to have an additional decorator so that you could say:

@documentation.route('/', 'this prints out hello')
@app.route('/')
def index():
    return 'hello'

Then, documentation would store the routing information, and then we could have a function that would print
out the URL's and their corresponding documentation.

I modeled what the user should see after this:

https://developer.spotify.com/web-api/endpoint-reference/

"""
import html

class URLDocumentation():
    """
    Every URL definition gets a unique ID.

    This should make it easier to construct the links for more information about the URL.
    """
    def __init__(self):
        self.url_docs = dict()
        self.id_to_url = dict()
        self.current_id = 1
        
    def route(self, route_url, method, usage, returns_summary):
        def decorator(f):
            if route_url not in self.url_docs:
                self.url_docs[route_url] = dict()
            self.url_docs[route_url]['method'] = method
            self.url_docs[route_url]['usage'] = usage
            self.url_docs[route_url]['returns'] = returns_summary
            self.url_docs[route_url]['id'] = self.current_id
            self.id_to_url[self.current_id] = route_url
            self.current_id += 1
            
            return f
        
        return decorator

    """

    path_params, header_params, and query_params are of the following form:
    [(param_name_1, param_explanation, required) OR (param_name, param_explanation, required, default)]

    required is True if the parameter is required, False if it is optional.

    You can specify a default if you want.

    Path params are parts of the url. For example:

    /hello/<a>/bye

    <a> would be a path param.

    Header params are used in the headers sent to the server.

    Query parameters are either:
       a) The parameters that are put in the URL after ? if it is a GET request
       b) If it is a POST request, then the fields that should be in the JSON object being sent.

    If you don't want any of these (other than the URL) to appear in the documentation (e.g. if you have no fields for that),
    then simply pass in None for that parameter.
    """
    def set_params(self, url, path_params, header_params, query_params):
        def decorator(f):
            if url not in self.url_docs:
                self.url_docs[url] = dict()
            
            if path_params is not None:
                if 'path_params' in self.url_docs[url]:
                    raise NameError('path_params already defined for the URL: ' + url)
                else:
                    self.url_docs[url]['path_params'] = path_params
            if header_params is not None:
                if 'header_params' in self.url_docs[url]:
                    raise NameError('header_params already defined for the URL: ' + url)
                else:
                    self.url_docs[url]['header_params'] = header_params

            if query_params is not None:
                if 'query_params' in self.url_docs[url]:
                    raise NameError('query_params already defined for the URL: ' + url) 
                else:
                    self.url_docs[url]['query_params'] = query_params
            
            return f
        return decorator
    
    def returns(self, url, description):
        def decorator(f):
            if url not in self.url_docs:
                self.url_docs[url] = dict()
                
            if 'return_description' in self.url_docs[url]:
                raise NameError('return_description already defined for the URL: ' + url)
            else:
                self.url_docs[url]['return_description'] = description
            

            return f
        return decorator

    """

    This documents the fields that will be in the return object. json_fields is of the form:
    [(field_name, field_description)...]
    """
    def json_returns(self, url, json_fields):
        def decorator(f):
            if url not in self.url_docs:
                self.url_docs[url] = dict()
            
            if 'json_return_fields' in self.url_docs[url]:
                raise NameError('json_return_fields is already defined for the URL: ' + url)
            else:
                self.url_docs[url]['json_return_fields'] = json_fields
            
            
            return f
        return decorator
    def get_docs(self):
        return self.url_docs

    """
    This returns the HTML string for the main page 
    Parameter: id_to_url. This is a function, that when given an endpoint ID, generates the URL that will be placed into the table.
"""
    def get_docs_string(self, id_to_url):
        html_string = "<html><body><table><tr><th>Method</th><th>URL</th><th>Usage</th><th>Returns</th></tr>"
        rows = list()
        for url, doc in self.url_docs.items():
            rows.append('<tr><td>' + html.escape(doc['method']) + '</td><td><a href="' + id_to_url(doc['id']) + '">' + html.escape(url) + '</a></td><td>' + html.escape(doc['usage']) + '</td><td>' + html.escape(doc['returns']) + '</td></tr>')
        return html_string + '\n'.join(rows)
        
    def get_docs_for_id(self, url_id):
        return self.url_docs[self.id_to_url[url_id]]

    def get_docs_string_for_id(self, url_id):
        print(self.id_to_url)
        url = self.id_to_url[int(url_id)]
        docs = self.url_docs[url]
        string = "<h2>" + html.escape(url) + "</h2>"
        chunks = list()
        chunks.append(string)
        chunks.append('Method: ' + html.escape(docs['method']))
        chunks.append('Usage: ' + html.escape(docs['usage']))
        chunks.append('Returns: ' + html.escape(docs['returns']))
        for k in ['path_params', 'header_params', 'query_params']:
            if k in docs:
                if k == 'path_params':
                    chunks.append('Path Parameters:')
                elif k == 'header_params':
                    chunks.append('Header Parameters:')
                elif k == 'query_params':
                    chunks.append('Query Parameters:')
                table_chunks = list()
                table_chunks.append('<table border="1"><tr><th>Param</th><th>Description</th><th>Required</th><th>Default Value</th></tr>')
                for x in docs[k]:
                    table_chunks.append('<tr>')
                    table_chunks.append('<td>' + html.escape(x[0]) + '</td>')
                    table_chunks.append('<td>' + html.escape(x[1]) + '</td>')
                    table_chunks.append('<td>' + ('<i> Required </i>' if x[2] else '<i> Optional </i>') + '</td>')
                    if len(x) == 3:
                        table_chunks.append('<td></td>')
                    else:
                        table_chunks.append('<td>' + html.escape(x[3]) + '</td>')
                    table_chunks.append('<tr>')
                table_chunks.append('</table>')
                table_string = ''.join(table_chunks)
                chunks.append(table_string)
        chunks.append('<h3>Returns</h3>')
        chunks.append(html.escape(docs['returns']))
        if 'json_return_fields' in docs:
            chunks.append('<table><tr><th>Field</th><th>Description</th></tr>')
            for field_name, description in docs['json_return_fields']:
                chunks.append('<tr><td>' + html.escape(field_name) + '</td><td>' + html.escape(description) + '</td></tr>')
            chunks.append('</table>')
        return '<br />'.join(chunks)
        
                
                
            

