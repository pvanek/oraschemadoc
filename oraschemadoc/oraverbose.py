#!/usr/bin/env python

# OraSchemaDoc v0.23
# Copyright (C) Aram Kananov <arcanan@flashmail.com>, 2002
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

# used for printing more debuging messages if app runs in verbose mode 

__verbose_mode = None


def debug_message(text):
    global __verbose_mode
    if __verbose_mode:
        print text
    return

def set_verbose_mode(mode):
    global __verbose_mode
    __verbose_mode = mode
    return
