#!/usr/bin/env python
#

# OraSchemaDataDictionary class queries data from Oracle Data Dictionary 

__author__ = 'Aram Kananov <arcanan@flashmail.com>'

__version__ = '$Version: 0.1'

class OracleSchema:

    def __init__(self, data_dict):
        self.tables = self._get_all_tables(data_dict)
        self.indexes = self._get_all_indexes(data_dict)
        self.constraints = self._get_all_constraints(data_dict)
        self.views = self._get_all_views(data_dict)
        self.name = "Foobarizm" 

    def _get_all_tables(self, data_dict):
        tables = []
        for table_name in data_dict.all_table_names:
            tables.append(OracleTable(table_name, data_dict))
        return tables
    
    def _get_all_indexes(self, data_dict):
        indexes = []
        for index_name in data_dict.all_index_names:
            indexes.append(OracleIndex(index_name, data_dict))
        return indexes
    
    def _get_all_constraints(self, data_dict):
        constraints = []
        for name in data_dict.all_constraint_names:
             table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[name]
             if type in ("P", "U"):
                 constraints.append(OracleUniqueConstraint(name, data_dict))
             elif type == "R":
                 constraints.append(OracleReferentialConstraint(name, data_dict))
             elif type == "C":
                 constraints.append(OracleCheckConstraint(name, data_dict))
        return constraints

    def _get_all_views(self, data_dict):
        views = []
        for view_name in data_dict.all_view_names:
            views.append(OracleView(view_name, data_dict))
        return views

class OracleTable:

    def __init__(self, name, data_dict):
        self.name = name
        self.partitioned, self.secondary, self.index_organized, self.clustered, self.cluster_name, self.nested, self.temporary = data_dict.all_tables[name]
        self.comments = data_dict.all_table_comments.get(name)
        self.columns = self._get_columns(data_dict)

        self.primary_key             = self._get_primary_key(name, data_dict)
        self.unique_keys             = self._get_unique_keys(name, data_dict)
        self.check_constraints       = self._get_check_constraints(name, data_dict)
        self.referential_constraints = self._get_ref_constraints(name, data_dict)
        self.indexes                 = self._get_indexes(name, data_dict)
        self.referenced_by = None
        if data_dict.table_referenced_by.has_key(name):
            self.referenced_by       = data_dict.table_referenced_by[name]
        

    def _get_primary_key(self, table_name, data_dict):
        _primary_key_name = data_dict.table_primary_key_map.get(table_name)
        primary_key = None
        if _primary_key_name:
            primary_key = OracleUniqueConstraint(_primary_key_name, data_dict)
        return primary_key

    def _get_unique_keys(self, table_name, data_dict):
        unique_keys = []
        t = data_dict.table_unique_key_map.get(table_name)
        if not t:
            return None
        for key_name in t:
            unique_key = OracleUniqueConstraint(key_name, data_dict)
            unique_keys.append(unique_key)
        return unique_keys

    def _get_check_constraints(self, table_name, data_dict):
        check_constraints = []
        t = data_dict.table_check_constraint_map.get(table_name)
        if not t:
            return None
        for constraint_name in t:
            constraint = OracleCheckConstraint(constraint_name, data_dict)
            check_constraints.append(constraint)
        return check_constraints

    def _get_ref_constraints(self, table_name, data_dict):
        referential_constraints = []
        t = data_dict.table_foreign_key_map.get(table_name)
        if not t:
            return None
        for constraint_name in t:
            constraint = OracleReferentialConstraint(constraint_name, data_dict)
            referential_constraints.append(constraint)
        return referential_constraints
    

    def _get_columns(self, data_dict):
        columns = {}
        # Fixme: need proper hadling iot overflow segment columns
        if data_dict.all_columns.has_key(self.name):
            for column, data_type, nullable, column_id, data_default in data_dict.all_columns[self.name]:
                if data_dict.all_col_comments.has_key((self.name, column)):
                    comments = data_dict.all_col_comments[self.name, column]
                else:
                    comments = ''
                columns[column_id] = OracleColumn(column, column_id, data_type, nullable, data_default, comments)
        return columns


    def _get_indexes(self, table_name, data_dict):
        indexes = []
        if  data_dict.table_index_map.has_key(table_name):
            for index_name in data_dict.table_index_map[table_name]:
                index = OracleIndex(index_name, data_dict)
                indexes.append(index)
        return indexes
            

class OracleColumn:

    def __init__(self, name, column_id, data_type, nullable, data_default, comments):
        self.column_id = column_id
        self.name = name
        self.data_type =data_type
        self.nullable = nullable
        self.data_default = data_default
        self.comments = comments

class OracleUniqueConstraint:

    def __init__(self, name, data_dict):
        self.name = name
        self.table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[name]
        if type == "P":
            self.type = "Primary key"
        else:
            self.type = "Unique key"
        self.columns ={}
        for table_name, column_name, position in data_dict.all_constraited_columns[name]:
            self.columns[position]=column_name

class OracleCheckConstraint:

    def __init__(self, name, data_dict):
        self.name = name
        self.table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[name]
        self.type = "Check"
        self.check_cond = check_cond
        self.columns = {}
        for table_name, column_name, position in data_dict.all_constraited_columns[name]:
            self.columns[position]=column_name        

class OracleReferentialConstraint:

    def __init__(self, name, data_dict):
        self.name = name
        self.table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[name]
        self.type = "Referential"
        self.r_owner = r_owner
        self.r_constraint_name = r_constraint_name
        self.delete_rule = delete_rule
        table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[self.r_constraint_name]
        self.r_table = table_name
        self.columns = {}
        for table_name, column_name, position in data_dict.all_constraited_columns[name]:
            self.columns[position]=column_name



class OracleIndex:

    def __init__(self, name, data_dict):
        self.name = name
        table_name, type, uniqueness, include_column, generated, secondary = data_dict.all_indexes[name]
        self.table_name = table_name
        self.type = type
        self.uniqueness = uniqueness
        self.include_column = include_column
        self.generated = generated
        self.secondary = secondary

        self.columns = {}
        if data_dict.all_index_columns.has_key(name):
            for table_name, column , position in data_dict.all_index_columns[name]:
                self.columns[position] = column
        if data_dict.all_index_expressions.has_key(name):
            for table_name, expression , position in data_dict.all_index_expressions[name]:
                self.columns[position] = expression

class OracleView:

    def __init__(self, name, data_dict):
        self.name = name
        self.text = data_dict.all_views[name]
        self.columns = self._get_columns(data_dict)
        self.constraints = self._get_constraints(data_dict)
        self.comments = data_dict.all_table_comments.get(name)
        
    def _get_columns(self, data_dict):
        columns = {}
        for column, data_type, nullable, column_id, data_default in data_dict.all_columns[self.name]:
            if data_dict.all_col_comments.has_key((self.name, column)):
                comments = data_dict.all_col_comments[self.name, column]
            else:
                comments = ''
            columns[column_id] = OracleViewColumn(column, column_id, data_type, nullable, data_default, comments, self.name, data_dict)
        return columns
    
    def _get_constraints(self, data_dict):
        constraints = []
        t = data_dict.view_constraint_map.get(self.name)
        if not t:
            return None
        for constraint_name in t:
            constraint = OracleViewConstraint(constraint_name, data_dict)
            constraints.append(constraint)
        return constraints

class OracleViewColumn(OracleColumn):

    def __init__(self, name, column_id, data_type, nullable, data_default, comments, table_name, data_dict):
        OracleColumn.__init__(self, name, column_id, data_type, nullable, data_default, comments)
        self.insertable, self.updatable, self.deletable = data_dict.all_updatable_columns[table_name, name]
    

class OracleViewConstraint:

    def __init__(self, name, data_dict):
        self.name = name
        self.table_name, type, check_cond, r_owner, r_constraint_name, delete_rule = data_dict.all_constraints[name]
        if type == 'O':
            self.type = "With read only on view"
        else:
            self.type = "With check option on view"
        self.check_cond = check_cond
        self.columns = {}
        for table_name, column_name, position in data_dict.all_constraited_columns[name]:
            self.columns[position]=column_name


if __name__ == '__main__':
    import cx_Oracle
    import orasdict
    connection = cx_Oracle.connect('aram_v1/aram_v1')
    s = orasdict.OraSchemaDataDictionary(connection, 'Oracle')
    schema = OracleSchema(s)
        
    