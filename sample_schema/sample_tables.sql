drop table plan_table;
@$ORACLE_HOME/rdbms/admin/utlxplan.sql

-- sample standard table
drop table STD_TABLE;
CREATE TABLE STD_TABLE
(
  ID NUMBER(10) NOT NULL,
  ATEXT VARCHAR2(4000),
CONSTRAINT STD_TABLE_PK PRIMARY KEY (ID)
)
  STORAGE (BUFFER_POOL DEFAULT);

COMMENT ON TABLE STD_TABLE IS 'a standard table';
COMMENT ON COLUMN STD_TABLE.ID IS 'pk';
COMMENT ON COLUMN STD_TABLE.ATEXT IS 'some text';

drop index STD_TABLE_INDEX1;
CREATE BITMAP INDEX STD_TABLE_INDEX1 ON STD_TABLE (ATEXT) NOPARALLEL;
drop sequence STD_TABLE_SEQ;
CREATE SEQUENCE STD_TABLE_SEQ;

drop trigger std_table_trg;
create
trigger std_table_trg
 before insert on STD_TABLE 
for each row 
BEGIN
  SELECT STD_TABLE_SEQ.NEXTVAL INTO :NEW.ID FROM DUAL;
END;
/

-- IOT
drop table osd.iot_table;
  CREATE TABLE "OSD"."iot_table"
   (	"COL1" NUMBER NOT NULL ENABLE, 
	"COLUMN8" VARCHAR2(4000 BYTE), 
	"COLUMN1" VARCHAR2(4000 BYTE), 
	"COLUMN2" VARCHAR2(4000 BYTE), 
	"COLUMN3" VARCHAR2(4000 BYTE), 
	"COLUMN4" VARCHAR2(4000 BYTE), 
	"COLUMN5" VARCHAR2(4000 BYTE), 
	"COLUMN6" VARCHAR2(4000 BYTE), 
	"COLUMN7" CLOB, 
	 CONSTRAINT "iot_table_PK" PRIMARY KEY ("COL1") ENABLE,
	 CONSTRAINT "iot_table_UK1" UNIQUE ("COLUMN8")
  USING INDEX PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT)
  TABLESPACE "USERS"  ENABLE
   ) ORGANIZATION INDEX NOCOMPRESS PCTFREE 10 INITRANS 2 MAXTRANS 255 LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT)
  TABLESPACE "USERS" 
 PCTTHRESHOLD 50 MAPPING TABLE INCLUDING "COL1" OVERFLOW
 PCTFREE 10 PCTUSED 40 INITRANS 1 MAXTRANS 255 LOGGING
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT)
  TABLESPACE "USERS" 
 LOB ("COLUMN7") STORE AS "USERS"(
  TABLESPACE "USERS" ENABLE STORAGE IN ROW CHUNK 8192 PCTVERSION 10
  NOCACHE LOGGING 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT)) ;

drop index osd.iot_table_UK1;
  CREATE UNIQUE INDEX "OSD"."iot_table_UK1" ON "OSD"."iot_table" ("COLUMN8")
  PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT)
  TABLESPACE "USERS" ;

drop index osd.iot_table_INDEX1;
CREATE INDEX "OSD"."iot_table_INDEX1" ON "OSD"."iot_table" ("COLUMN3" DESC)
  PCTFREE 10 INITRANS 2 MAXTRANS 255 
  STORAGE(INITIAL 65536 NEXT 1048576 MINEXTENTS 1 MAXEXTENTS 2147483645
  PCTINCREASE 0 FREELISTS 1 FREELIST GROUPS 1 BUFFER_POOL DEFAULT)
  TABLESPACE "USERS" ;
 

