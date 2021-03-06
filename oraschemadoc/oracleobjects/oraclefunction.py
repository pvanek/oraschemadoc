# Copyright (C) Petr Vanek <petr@yarpen.cz>, 2005
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

__author__ = 'Aram Kananov <arcanan@flashmail.com>, Petr Vanek, <petr@yarpen.cz>'


from oracleprocedure import OracleProcedure


class OracleFunction(OracleProcedure):

    def __init__(self, name, arguments, return_data_type, source = None):
        #debug_message("debug: generating plsql function %s" % name)
        OracleProcedure.__init__(self, name, arguments, source)
        self.return_data_type = ''
        if return_data_type:
            self.return_data_type = return_data_type

    def getXML(self):
        """get function metadata"""
        xml_text = '''<function id="procedure-%s">
                        <name>%s</name>
                        <returns>%s</returns>
                        <source>%s</source>''' % (self.name, self.name, self.return_data_type, 
                                                              self.source.getXML())
        if self.arguments:
            xml_text += '<arguments>'
            for argument in self.arguments:
                xml_text += argument.getXML()
            xml_text += '</arguments>'

        xml_text += '</function>'
        return xml_text
