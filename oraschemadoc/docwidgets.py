# OraSchemaDoc v0.10
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

# HTML Widgets

__author__ = 'Aram Kananov <arcanan@flashmail.com>'

__version__ = '$Version: 0.1'

import string

class HtmlWidgets:
    
    def __init__(self, name):
        self.name = name
        self.table_bgcolor =  "#CCCCFF"
    
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
        return '''<html><head><title> %s - %s </title></head>
        <body bgcolor="#ffffff">
        ''' % (self.name , title)

    def context_bar(self, local_nav_bar):
        text = '''<table width="100%" border=0>
        <tr>
           <td colspan=2 bgcolor="#EEEEFF">
             <table>
                <tr>
                  <td><a href="main.html"><b>Main</b></a></td>
                  <td><a href="tables-list.html"><b>Tables</b></a></td>
                  <td><a href="views-list.html"><b>Views</b></a></td>
                  <td><a href="indexes-list.html"><b>Indexes</b></a></td>
                  <td><a href="constraints-list.html"><b>Constraints</b></a></td>
                  <td><a href="symbol-index.html"><b>Index</b></a></td>
                </tr>
             </table>
           </td>\n'''
        text = text + '<td align="right" valign="top" rowspan=2><h3> %s</h3> </td>\n' % self.name 
        text = text + '</tr>\n'
        text = text + '<tr><td colspan =2><table><tr>\n'
        if local_nav_bar:
            for label, link in local_nav_bar:
                text = text + '<td bgcolor="white"><font size="-1"><a href="#%s"> %s </font> </td>' % (link, label)
            text = text + '</tr></table></tr>'
        text = text + '</table>'
        return text
        
        

    def frame_header(self, title):
        header = '''<html><head><title> %s </title></head><body bgcolor="#ffffff">''' %title
        return header + self.heading(title,1)

    def frame_footer(self):
        return "</body></html>"
    
    def page_footer(self):
        return '''<br><hr size=1 noshade>
        <small>Generated by  <a href="http://oraschemadoc.sourceforge.net/">OraSchemaDoc</a>,
        (c) Aram Kananov, 2002</small>\n</body></html>\n'''
    
    def href_to_column(self, label, table_name, column_name):
        return '<a href="table-%s.html#col-%s">%s </a>\n' % (table_name, column_name, label)

    def href_to_constraint(self, label, table_name, constraint_name, target_frame = None):
        if not target_frame:
            return '<a href="table-%s.html#cs-%s">%s </a>\n' % (table_name, constraint_name, label)
        else:
            return '<a href="table-%s.html#cs-%s" target="%s">%s </a>\n' % (table_name, constraint_name, target_frame, label) 


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

    def href_to_view(self, view_name, target_frame = None):
        if not target_frame:
            return '<a href="view-%s.html"> %s </a>' % (view_name, view_name)
        else:
            return '<a href="view-%s.html" target="%s"> %s </a>' % (view_name, target_frame, view_name)

    def href_to_view_column(self, label, view_name, column_name):
        return '<a href="view-%s.html#col-%s">%s </a>\n' % (view_name, column_name, label)

    def hr(self):
        return '<hr>\n'

    def pre(self, text):
        return "<pre>\n"+text+"</pre>\n"

    def table(self, name, headers, rows):
        text = ""
        if name:
            text = self.heading(name,3)
        if not rows:
            return text + "<p>None"
        text = text + '<table border=1>\n'
        text = text + '<tr bgcolor="' +self.table_bgcolor + '">'
        for header in headers:
            text = text + '<th>' + header + '</th>'
        text = text + '</tr>'
        for row in rows:
            text = text + '<tr>'
            for column in row:
                if column:
                   text = text + '<td>' + column + '</td>'
                else:
                   text = text + '<td>&nbsp;</td>'
            text = text + '</tr>\n'
        text = text + '</table>'
        return text

    def _index_page(self, name):
        return '<html><head><title>' + name + '''</title></head>
                  <frameset cols="20%,80%">
                    <frameset rows="10%,90%">
                       <frame src="nav.html" name="GlobalNav">
                       <frame src="tables-index.html" name="List">
                    </frameset>
                    <frame src="main.html" name="Main">
                  </frameset>
                  <noframes>
                  <h2>Frame Alert</h2><p>
                  This document is designed to be viewed using the frames feature. If you see this message, you are using a non-frame-capable web client.
                  <br>
                  Link to<a HREF="main.html">Non-frame version.</a></noframes>
                  </html>''' 

    def _global_nav_frame(self, name):
        return '''<html>
                  <head><title>%s</title></head><body bgcolor="#ffffff">
                  <a href="tables-index.html" target="List"><b>Tables</b></a><br>
                  <a href="views-index.html" target="List"><b>Views</b></a><br>
                  <a href="indexes-index.html" target="List"><b>Indexes</b></a><br>
                  <a href="constraints-index.html" target="List"><b>Constraints</b></a><br>
                  </body><html>''' % name 

    def _quotehtml (self, text):
        text = string.replace(text, "&", "&amp;")
        text = string.replace(text, "\\", "&quot;")
        text = string.replace(text, "<", "&lt;")
        text = string.replace(text, ">", "&gt;")
        return text
    
    def _main_frame(self, name):
        text = text = self.page_header("name")
        text = text + self.context_bar( None)
        text = text + self.hr()
        text = text + self.heading(name,1)
        text = text + self.page_footer()
        return text

