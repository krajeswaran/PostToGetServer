#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi

class PostHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        redirect_uri = "https://foobar.uri/?"

        # Parse the form data to cgi
        form = cgi.FieldStorage(
                fp=self.rfile, 
                headers=self.headers,
                environ={'REQUEST_METHOD':'POST',
                'CONTENT_TYPE':self.headers['Content-Type'],
                })

        # print client info 
        print 'Client: %s\n' % str(self.client_address)
        print 'User-agent: %s\n' % str(self.headers['user-agent'])
        print 'Path: %s\n' % self.path
        print 'Form data:\n'

        # parse form posted
        for field in form.keys():
            field_item = form[field]
            if field_item.filename:
                # The field contains an uploaded file
                file_data = field_item.file.read()
                file_len = len(file_data)
                del file_data
                print '\tUploaded %s as "%s" (%d bytes)\n' % (field, field_item.filename, file_len)
            else:
                # Regular form value
                print '\t%s=%s\n' % (field, form[field].value)
                redirect_uri = redirect_uri + field + '=' + form[field].value + '&'

        # issue a GET based on post
        print('Issuing get request for %s' % redirect_uri)
        self.send_response(301)
        self.send_header('Location', redirect_uri)
        self.end_headers()

        return


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('0.0.0.0', 8000), PostHandler)
    print 'Starting server on 8000, use <Ctrl-C> to stop'
    server.serve_forever()
