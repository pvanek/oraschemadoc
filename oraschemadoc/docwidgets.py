# Copyright (C) Petr Vanek <petr@scribus.info> , 2005
# Copyright (C) Aram Kananov <arcanan@flashmail.com> , 2002
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
#

"""XHTML Widgets"""

__author__ = 'Aram Kananov <arcanan@flashmail.com>, Petr Vanek <petr@scribus.info>'

__version__ = '$Version: 0.25'

import string
import time

class HtmlWidgets:

    def __init__(self, name, css, webEncoding):
        self.name = name
        self.css = css
        self.webEncoding = webEncoding

    def i(self, text):
        return "<i>%s</i>" %text

    def anchor(self, name):
        return '<a name="%s"></a>' % name 

    def heading(self, text, level):
        return '''<h%s>%s</h%s>\n''' % (level,text,level)

    def href(self, url, text, target_frame = None):
        if not target_frame: 
            return '''<a href="%s">%s</a>''' % (url, text)
        else:
            return '''<a href="%s" target="%s">%s</a>''' % (url, target_frame, text)

    def page_header(self, title):
        return '''<?xml version="1.0" encoding="%s" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head><title> %s - %s </title>
        <link rel="stylesheet" type="text/css" href="%s" />
        <meta http-equiv="Content-Type" content="text/html;charset=%s" />
        <meta name="author" content="Petr Vanek, petr@scribus.info" />
        <meta name="generator" content="oraschemadoc" />
        </head>
        <body>''' % (self.webEncoding, self.name , title, self.css, self.webEncoding)

    def context_bar(self, local_nav_bar):
        text = '''
            <div class="contextbar">
            <a href="main.html">Main</a>
            <a href="tables-list.html">Tables</a>
            <a href="views-list.html">Views</a>
            <a href="mviews-list.html">Materialized&nbsp;Views</a>
            <a href="indexes-list.html">Indexes</a>
            <a href="constraints-list.html">Constraints</a>
            <a href="triggers-list.html">Triggers</a>
            <a href="procedures-list.html">Procedures</a>
            <a href="functions-list.html">Functions</a>
            <a href="packages-list.html">Packages</a>
            <a href="sequences.html">Sequences</a>
            <a href="java-sources-list.html">Java&nbsp;Sources</a>
            <a href="sanity-check.html">Sanity&nbsp;Check</a>
            <a href="symbol-index.html">Index</a>
            </div>'''

        if local_nav_bar:
            text = text + '''
                <div class="subcontextbar">'''
            for label, link in local_nav_bar:
                text = text + '<a href="#%s">%s</a> ' % (link, label)
            text = text + '</div>'
        return text


    def frame_header(self, title):
        header = '''<?xml version="1.0" encoding="%s" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head><title> %s</title>
        <link rel="stylesheet" type="text/css" href="%s" />
        <meta http-equiv="Content-Type" content="text/html;charset=%s" />
        <meta name="author" content="Petr Vanek, petr@scribus.info" />
        <meta name="generator" content="oraschemadoc" />
        </head>
        <body class="navigationframe">''' % (self.webEncoding, title, self.css, self.webEncoding)
        return header + self.heading(title,1)

    def frame_footer(self):
        return "</body></html>"

    def page_footer(self):
        return '''<div class="footer">
        Generated by  <a href="http://www.yarpen.cz/oraschemadoc">OraSchemaDoc</a>,
        (c) Petr Vanek, 2005; Aram Kananov, 2002, on ''' + time.ctime() + '''</div>\n</body></html>\n'''

    def href_to_column(self, label, table_name, column_name):
        return '<a href="table-%s.html#col-%s">%s </a>\n' % (table_name, column_name, label)

    def href_to_constraint(self, label, table_name, constraint_name, target_frame = None):
        if not target_frame:
            return '<a href="table-%s.html#cs-%s">%s </a>\n' % (table_name, constraint_name, label)
        else:
            return '<a href="table-%s.html#cs-%s" target="%s">%s </a>\n' % (table_name, constraint_name, target_frame, label) 

    def href_to_trigger(self, label, table_name, trigger_name, target_frame = None):
        if not target_frame:
            return '<a href="table-%s.html#trg-%s">%s </a>\n' % (table_name, trigger_name, label)
        else:
            return '<a href="table-%s.html#trg-%s" target="%s">%s </a>\n' % (table_name, trigger_name, target_frame, label)

    def href_to_index(self, label, table_name, index_name, target_frame = None):
        if not target_frame:
            return '<a href="table-%s.html#ind-%s">%s </a>\n' % (table_name, index_name, label)
        else:
            return '<a href="table-%s.html#ind-%s" target="%s">%s </a>\n' % (table_name, index_name, target_frame, label)

    def href_to_table(self, table_name, target_frame = None):
        if not target_frame:
            return '<a href="table-%s.html"> %s </a>' % (table_name, table_name)
        else:
            return '<a href="table-%s.html" target="%s"> %s </a>' % (table_name, target_frame, table_name) 
    def href_to_sequence(self, name, target_frame = None):
        if not target_frame:
            return '<a href="sequences.html#%s"> %s </a>' % (name, name)
        else:
            return '<a href="sequences.html#%s" target="%s"> %s </a>' % (name, target_frame, name) 

    def href_to_view(self, view_name, target_frame = None):
        if not target_frame:
            return '<a href="view-%s.html"> %s </a>' % (view_name, view_name)
        else:
            return '<a href="view-%s.html" target="%s"> %s </a>' % (view_name, target_frame, view_name)

    def href_to_mview(self, mview_name, target_frame = None):
        if not target_frame:
            return '<a href="mview-%s.html"> %s </a>' % (mview_name, mview_name)
        else:
            return '<a href="mview-%s.html" target="%s"> %s </a>' % (mview_name, target_frame, mview_name)

    def href_to_procedure(self, procedure_name, target_frame = None):
        if not target_frame:
            return '<a href="procedure-%s.html"> %s </a>' % (procedure_name, procedure_name)
        else:
            return '<a href="procedure-%s.html" target="%s"> %s </a>' % (procedure_name, target_frame, procedure_name)

    def href_to_function(self, function_name, target_frame = None):
        if not target_frame:
            return '<a href="function-%s.html"> %s </a>' % (function_name, function_name)
        else:
            return '<a href="function-%s.html" target="%s"> %s </a>' % (function_name, target_frame, function_name)

    def href_to_package(self, package_name, target_frame = None):
        if not target_frame:
            return '<a href="package-%s.html"> %s </a>' % (package_name, package_name)
        else:
            return '<a href="package-%s.html" target="%s"> %s </a>' % (package_name, target_frame, package_name)

    def href_to_view_column(self, label, view_name, column_name):
        return '<a href="view-%s.html#col-%s">%s </a>\n' % (view_name, column_name, label)

    def href_to_java_source(self, name, target_frame = None):
        if not target_frame:
            return '<a href="java-source-%s.html"> %s </a>' % (name.replace("/","-"), name)
        else:
            return '<a href="java-source-%s.html" target="%s"> %s </a>' % (name.replace("/","-"), target_frame, name)


    def hr(self):
        return '<hr>\n'

    def pre(self, text):
        return "<pre>\n"+text+"</pre>\n"


    def p(self, text):
        return "<p>" + str(text) + "</p>"


    def table(self, name, headers, rows, width = None):
        text = ""
        if name:
            text = self.heading(name,3)
        if not rows:
            return text + "<p>None"
        if width:
            text = text + '<table width='+width+'%>'
        else:
            text = text + '<table>\n'
        text = text + '<tr>'
        for header in headers:
            text = text + '<th>' + str(header) + '</th>'
        text = text + '</tr>'
        for row in rows:
            text = text + '<tr>'
            for column in row:
                if column:
                   text = text + '<td>' + str(column) + '</td>'
                else:
                   text = text + '<td>&nbsp;</td>'
            text = text + '</tr>\n'
        text = text + '</table>'
        return text

    def _index_page(self, name):
        return '''<?xml version="1.0" encoding="'''+ self.webEncoding +'''" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "XHTML1-f.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head><title>''' + name + '''</title>
        <meta http-equiv="Content-Type" content="text/html;charset='''+ self.webEncoding + '''" />
        <meta name="author" content="Petr Vanek, petr@scribus.info" />
        <meta name="generator" content="oraschemadoc" />
        </head>
        <frameset cols="21%,79%">
          <frame src="nav.html" name="List" />
          <frame src="main.html" name="Main" />
        <noframes>
        <body>
        <h2>Frame Alert</h2>
        <p>This document is designed to be viewed using the frames feature.
        If you see this message, you are using a non-frame-capable web client.</p>
        <p>Link to<a href="main.html">Non-frame version.</a></p>
        </body>
        </noframes>
        </frameset>
        </html>'''


    def _global_nav_frame(self, name):
        return '''<?xml version="1.0" encoding="%s" ?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "DTD/xhtml1-transitional.dtd">
        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
        <head><title> %s</title>
        <link rel="stylesheet" type="text/css" href="%s" />
        <meta http-equiv="Content-Type" content="text/html;charset=%s" />
        <meta name="author" content="Petr Vanek, petr@scribus.info" />
        <meta name="generator" content="oraschemadoc" />
        </head>
        <body class="navigationframe">
                  <a href="tables-index.html">Tables</a>
                  <a href="views-index.html">Views</a>
                  <a href="mviews-index.html">Materialized&nbsp;Views</a>
                  <a href="indexes-index.html">Indexes</a>
                  <a href="constraints-index.html">Constraints</a>
                  <a href="triggers-index.html">Triggers</a>
                  <a href="procedures-index.html">Procedures</a>
                  <a href="functions-index.html">Functions</a>
                  <a href="packages-index.html">Packages</a>
                  <a href="sequences-index.html">Sequences</a>
                  <a href="java-sources-index.html">Java&nbsp;Sources</a>
                  <a href="sanity-check.html" target="Main">Sanity&nbsp;Check</a>
        </body></html>''' % (self.webEncoding, name, self.css, self.webEncoding)

    def _quotehtml (self, text):
        text = string.replace(text, "&", "&amp;")
        text = string.replace(text, "\\", "&quot;")
        text = string.replace(text, "<", "&lt;")
        text = string.replace(text, ">", "&gt;")
        return text

    def _main_frame(self, name, description, highlight):
        text = text = self.page_header("name")
        text = text + self.context_bar( None)
        text = text + self.heading(name,1)
        text = text + self.p(description)
        if highlight:
            h = 'Yes'
        else:
            h = 'No'
        text = text + self.p('<b>Using syntax highlighting:</b> ' + h)
        text = text + self.p('<b>Character set:</b> ' + self.webEncoding)
        text = text + self.page_footer()
        return text

