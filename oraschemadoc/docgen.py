#!/usr/bin/env python
#

# Doc Generator

__author__ = 'Aram Kananov <arcanan@flashmail.com>'

__version__ = '$Version: 0.1'

import os, string, docwidgets

class OraSchemaDoclet:

    def __init__(self, schema, doc_dir, name, description):
        self.schema = schema
        self.doc_dir = doc_dir
        self.name = name
        self.description = description
        self.html = docwidgets.HtmlWidgets(self.name)
        self.index = {}
 

        self._print_table_list_page()
        self._print_tables()
        self._print_table_index_frame()
        self._print_index_list_page()
        self._print_index_index_frame()
        self._print_constraint_list_page()
        self._print_constraint_index_frame()
        self._print_view_list_page()
        self._print_view_index_frame()
        self._print_views()
        self._print_symbol_index_page()
        self._print_common_pages()

    def _print_common_pages(self):
        text = self.html._index_page(self.name)
        file_name = os.path.join(self.doc_dir, "index.html")
        self._write(text, file_name)
        text = self.html._global_nav_frame(self.name)
        file_name = os.path.join(self.doc_dir, "nav.html")
        self._write(text, file_name)
        text = self.html._main_frame(self.name)
        file_name = os.path.join(self.doc_dir, "main.html")
        self._write(text, file_name)
    
    def _print_table_list_page(self):
        text = self.html.page_header("Tables")
        text = text + self.html.context_bar( None)
        text = text + self.html.hr()
        rows = []
        for table in self.schema.tables:
            name = self.html.href_to_table(table.name)
            if table.secondary == 'Yes':
                name = self.html.i(name)
            comments = table.comments 
            if comments:
                comments = comments[:100]+'...'
            rows.append(( name, comments ))
        headers = "Table", "Description"
        name = "Tables"
        text = text + self.html.table(name, headers, rows)
        text = text + self.html.page_footer()
        file_name = os.path.join(self.doc_dir, "tables-list.html")
        self._write(text, file_name)

    def _print_table_index_frame(self):
        text = self.html.frame_header("Tables")
        text = text + self.html.heading("Tables",3)
        text = text + self.html.hr()
        rows = []
        for table in self.schema.tables:
            link = self.html.href_to_table(table.name, "Main")
            if table.secondary == 'Yes':
                link = self.html.i(link)
            text = text + link + '<br>'
        text = text + self.html.frame_footer()
        file_name = os.path.join(self.doc_dir, "tables-index.html")
        self._write(text, file_name)

    def _print_index_index_frame(self):
        text = self.html.frame_header("Indexes")
        text = text + self.html.heading("Indexes",3)
        text = text + self.html.hr()
        rows = []
        for index in self.schema.indexes:
            link = self.html.href_to_index(index.name, index.table_name, index.name, "Main")
            text = text + link + '<br>'
        text = text + self.html.frame_footer()
        file_name = os.path.join(self.doc_dir, "indexes-index.html")
        self._write(text, file_name)

    def _print_constraint_index_frame(self):
        text = self.html.frame_header("Constraints")
        text = text + self.html.heading("Constraints",3)
        text = text + self.html.hr()
        rows = []
        for constraint in self.schema.constraints:
            link = self.html.href_to_constraint(constraint.name, constraint.table_name, constraint.name, "Main")
            text = text + link + '<br>'
        text = text + self.html.frame_footer()
        file_name = os.path.join(self.doc_dir, "constraints-index.html")
        self._write(text, file_name)

    def _print_view_index_frame(self):
        text = self.html.frame_header("Views")
        text = text + self.html.heading("Views",3)
        text = text + self.html.hr()
        rows = []
        for view in self.schema.views:
            link = self.html.href_to_view(view.name, "Main")
            text = text + link + '<br>'
        text = text + self.html.frame_footer()
        file_name = os.path.join(self.doc_dir, "views-index.html")
        self._write(text, file_name) 

    def _print_tables(self):
        for table in self.schema.tables:
            self._print_table(table)
            
    def _print_views(self):
        for view in self.schema.views:
            self._print_view(view)

    def _print_table(self, table):
        "print table page"
        # create header and context bar
        text = self.html.page_header("Table-" + table.name)
        local_nav_bar = []
        local_nav_bar.append(("Description", "t-descr"))
        local_nav_bar.append(("Columns", "t-cols"))
        local_nav_bar.append(("Primary key", "t-pk"))
        local_nav_bar.append(("Check Constraints", "t-cc"))
        local_nav_bar.append(("Foreign keys", "t-fk"))
        local_nav_bar.append(("Unique Keys", "t-uc"))
        local_nav_bar.append(("Options", "t-opt"))
        local_nav_bar.append(("Indexes", "t-ind"))
        local_nav_bar.append(("Referenced by", "t-refs"))        
        text = text + self.html.context_bar(local_nav_bar)
        text = text + self.html.hr()
        text = text + self.html.heading(table.name, 2)
        # punt entry in doc index
        self._add_index_entry(table.name, self.html.href_to_table(table.name), "table")
        # print comments
        if table.comments:
            text = text + self.html.heading("Description:",3) + self.html.anchor("t-descr")
            text = text + self.html.pre(table.comments)
        #print columns
        rows = []
        # fixme iot table overflow segment column problem
        if len(table.columns) > 0:
            print table.name
            for i in range(len(table.columns)):
                column = table.columns[i+1]
                self._add_index_entry(column.name, self.html.href_to_column(column.name, table.name, column.name), "column of table %s" % table.name)
                rows.append((column.name+self.html.anchor('col-%s' % column.name), column.data_type, column.nullable, column.data_default, column.comments))
            headers = "Name", "Type", "Nullable", "Default value", "Comment"
            text = text + self.html.table("Columns" + self.html.anchor('t-cols'), headers, rows)
        # print primary key
        if table.primary_key:
            title = "Primary key:" + self.html.anchor("t-pk")
            pk_name = table.primary_key.name + self.html.anchor("cs-%s" % table.primary_key.name)
            pk_columns = ''
            for i in range(len(table.primary_key.columns)):
                pk_columns = pk_columns + self.html.href_to_column(table.primary_key.columns[i+1],table.name, table.primary_key.columns[i+1])
                if i+1 != len(table.primary_key.columns):
                    pk_columns = pk_columns + ', '
            headers = "Constraint Name" , "Columns"
            rows = []
            rows.append((pk_name, pk_columns))
            text = text + self.html.table( title, headers, rows)
        # print check constraints
        if table.check_constraints:
            title = "Check Constraints:" + self.html.anchor("t-cc")
            rows = []
            for constraint in table.check_constraints:
                rows.append((constraint.name + self.html.anchor("cs-%s" % constraint.name),constraint.check_cond))
            text = text + self.html.table(title, ("Constraint Name","Check Condition"), rows)
        # print referential constraints
        if table.referential_constraints:
            title = "Foreign Keys:" + self.html.anchor("t-fk")
            rows = []
            for constraint in table.referential_constraints:
                columns = ''
                for i in range(len(constraint.columns)):
                    columns = columns + self.html.href_to_column(constraint.columns[i+1], \
                                                        table.name, constraint.columns[i+1])
                    if i+1 != len(constraint.columns):
                        columns = columns + ', '
                name = constraint.name + self.html.anchor("cs-%s" % constraint.name)
                r_table = self.html.href_to_table(constraint.r_table)
                r_constraint_name = self.html.href_to_constraint(constraint.r_constraint_name, constraint.r_table, constraint.r_constraint_name)
                rows.append((name, columns, r_table, r_constraint_name, constraint.delete_rule))
            headers = "Constraint Name", "Columns", "Referenced table", "Referenced Constraint", "On Delete Rule"  
            text = text + self.html.table(title,headers, rows)
        # print unique keys
        if table.unique_keys:
            title = "Unique Keys:" + self.html.anchor("t-uc")
            rows = []           
            for constraint in table.unique_keys:
                columns = ''
                for i in range(len(constraint.columns)):
                    columns = columns + self.html.href_to_column(constraint.columns[i+1],table.name, constraint.columns[i+1])
                    if i+1 != len(constraint.columns):
                        columns = columns + ', '
                name = constraint.name + self.html.anchor("cs-%s" % constraint.name)
                rows.append((name, columns))
            text = text + self.html.table(title,("Constraint name","Columns"), rows)
        # print table options
        title = "Options:" + self.html.anchor("t-opt")
        rows = []
        rows.append(("Index Organized", table.index_organized))
        rows.append(("Generated by Oracle", table.secondary))
        rows.append(("Clustered", table.clustered))
        if table.clustered == 'Yes':
            rows.append(("Cluster", table.cluster_name))
        rows.append(("Nested", table.nested))
        rows.append(("Temporary", table.temporary))                
        headers = "Option","Settings"
        text = text + self.html.table(title, headers, rows)
        # print indexes
        if table.indexes:
           title = "Indexes:" + self.html.anchor("t-ind")
           rows = []
           
           for index in table.indexes:
               columns = ''
               for i in  range(len(index.columns)):
                    columns = columns + self.html.href_to_column(index.columns[i+1],table.name, index.columns[i+1])
                    if i+1 != len(index.columns):
                        columns = columns + ', '
               name = index.name + self.html.anchor("ind-%s" % index.name)
               rows.append((name, index.type, index.uniqueness, columns))
           headers = "Index Name", "Type", "Unuqueness","Columns"
           text = text + self.html.table(title, headers, rows)

        # print list of tables with references to this table
        if table.referenced_by:
           title = "Referenced by:" + self.html.anchor("t-refs")
           rows = []
           for table_name, constraint_name in table.referenced_by:
               constraint_name = self.html.href_to_constraint(constraint_name, table_name, constraint_name)
               table_name = self.html.href_to_table(table_name)
               rows.append((table_name, constraint_name))
           headers = "Table", "Constraint"
           text = text + self.html.table(title, headers, rows)
               
        
        text = text + self.html.page_footer()
        file_name = os.path.join(self.doc_dir, "table-%s.html" % table.name)
        self._write(text, file_name)

    def _print_index_list_page(self):
        text = self.html.page_header("Indexes")
        text = text + self.html.context_bar( None)
        text = text + self.html.hr()
        rows = []
        for index in self.schema.indexes:
            name = self.html.href_to_index(index.name, index.table_name, index.name)
            #add entry to do index
            self._add_index_entry(index.name, name, "index on table %s" % index.table_name)
            type = index.type
            table_name = self.html.href_to_table(index.table_name)
            rows.append(( name, type, table_name ))
        headers = "Index", "Type", "Table"
        name = "Indexes"
        text = text + self.html.table(name, headers, rows)
        text = text + self.html.page_footer()
        file_name = os.path.join(self.doc_dir, "indexes-list.html")
        self._write(text, file_name)

    def _print_constraint_list_page(self):
        text = self.html.page_header("Constraints")
        text = text + self.html.context_bar( None)
        text = text + self.html.hr()
        rows = []
        for constraint in self.schema.constraints:
            name = self.html.href_to_constraint(constraint.name, constraint.table_name, constraint.name)
            # add entry to doc index
            self._add_index_entry(constraint.name, name, "constraint on table %s" % constraint.table_name)
            type = constraint.type
            table_name = self.html.href_to_table(constraint.table_name)
            rows.append(( name, type, table_name ))
        headers = "Name", "Type", "Table"
        name = "Constraints"
        text = text + self.html.table(name, headers, rows)
        text = text + self.html.page_footer()
        file_name = os.path.join(self.doc_dir, "constraints-list.html")
        self._write(text, file_name)        

    def _print_view_list_page(self):
        text = self.html.page_header("Views")
        text = text + self.html.context_bar( None)
        text = text + self.html.hr()
        rows = []
        for view in self.schema.views:
            name = self.html.href_to_view(view.name)
            # add entry to doc index
            self._add_index_entry(view.name, name, "view")
            comments = view.comments 
            if comments:
                comments = comments[:100]+'...'
            rows.append(( name, comments ))
        headers = "View", "Description"
        name = "Views"
        text = text + self.html.table(name, headers, rows)
        text = text + self.html.page_footer()
        file_name = os.path.join(self.doc_dir, "views-list.html")
        self._write(text, file_name)

    def _print_view(self, view):
        "print view page"
        # create header and context bar
        text = self.html.page_header("View-" + view.name)
        local_nav_bar = []
        local_nav_bar.append(("Description", "v-descr"))
        local_nav_bar.append(("Columns", "v-cols"))
        local_nav_bar.append(("Query", "v-query"))
        local_nav_bar.append(("Constraints", "v-cc"))
        text = text + self.html.context_bar(local_nav_bar)
        text = text + self.html.hr()
        text = text + self.html.heading(view.name, 2)
        # print comments
        if view.comments:
            text = text + self.html.heading("Description:",3) + self.html.anchor("v-descr")
            text = text + self.html.pre(view.comments)
        #print columns
        rows = []
        for i in range(len(view.columns)):
            column = view.columns[i+1]
            # add entry to doc index
            self._add_index_entry(column.name, self.html.href_to_view_column(column.name, view.name, column.name), "column of of view %s" % view.name)
            rows.append((column.name+self.html.anchor('col-%s' % column.name), column.data_type, column.nullable,\
                         column.insertable, column.updatable, column.deletable, column.comments))
        headers = "Name", "Type", "Nullable","Insertable","Updatable", "Deletable", "Comment"
        text = text + self.html.table("Columns" + self.html.anchor('v-cols'), headers, rows)
        # print query
        text = text + self.html.heading("Query:",3) + self.html.anchor("v-query")
        text = text + self.html.pre(view.text)
        # print constraints
        if view.constraints:
            title = "Constraints:" + self.html.anchor("v-cc")
            rows = []
            for constraint in view.constraints:
                rows.append((constraint.name + self.html.anchor("cs-%s" % constraint.name),constraint.check_cond))
            text = text + self.html.table(title, ("Constraint Name","Check Condition"), rows)
        text = text + self.html.page_footer()
        file_name = os.path.join(self.doc_dir, "view-%s.html" % view.name)
        self._write(text, file_name)

    def _print_symbol_index_page(self):
        text = self.html.page_header("Schema Objects Index")
        local_nav_bar = []

        keys = self.index.keys()
        keys.sort()
        letter = ""
        for key in keys:
            if (key[:1] != letter):
                letter = key[:1] 
                local_nav_bar.append((letter,letter))
        text = text + self.html.context_bar(local_nav_bar)
        text = text + self.html.hr()
        
        letter = ""
        for key in keys:
            if (key[:1] != letter):
                letter = key[:1]
                text = text + self.html.heading(letter, 3) + self.html.anchor(letter)
            for entry in self.index[key]:
                text = text + '%s %s<br>' % entry
        text = text + self.html.page_footer()
        file_name = os.path.join(self.doc_dir, "symbol-index.html")
        self._write(text, file_name)        
        
    def _write(self, text, file_name):
        f = open(file_name, 'w')
        f.write(text)
        f.close()

    def _add_index_entry(self, key , link, description):
        t = self.index.get(key)
        if not t:
            self.index[key] = t = []
        t.append((link, description))

    
if __name__ == '__main__':
    import cx_Oracle
    import orasdict
    import oraschema
    connection = cx_Oracle.connect('aram_v1/aram_v1')
    s = orasdict.OraSchemaDataDictionary(connection, 'Oracle')
    schema = oraschema.OracleSchema(s)
    doclet = OraSchemaDoclet(schema, "/tmp/oraschemadoc/", "vtr Data Model", "Really cool project")
        
    