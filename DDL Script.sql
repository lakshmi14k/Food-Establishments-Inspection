create database midterm_check

use midterm_check

select * from stg_check_chicago

select * from stg_dallas_check

/* DDL script */

/*
 * ER/Studio Data Architect SQL Code Generation
 * Project :      DimensionModel_Midterm.DM1
 *
 * Date Created : Monday, March 04, 2024 22:32:58
 * Target DBMS : Microsoft SQL Server 2019
 */

USE midterm_check
go
/* 
 * TABLE: Dim_Business_License 
 */

CREATE TABLE Dim_Business_License(
    BusinessLicense_SK     int             NOT NULL,
    AKA_Name               char(10)        NULL,
    LicenseID              int             NULL,
    LegalName              varchar(255)    NULL,
    DBA_Name               varchar(255)    NULL,
    Address                varchar(255)    NULL,
    City                   varchar(255)    NULL,
    State                  varchar(255)    NULL,
    ZipCode                varchar(255)    NULL,
    Latitude               real            NULL,
    Longitude              real            NULL,
    DI_CreateDate          date            NULL,
    DI_WorkflowFileName    varchar(255)    NULL,
    Location               varchar(255)    NULL,
    CONSTRAINT PK5 PRIMARY KEY NONCLUSTERED (BusinessLicense_SK)
)

go


IF OBJECT_ID('Dim_Business_License') IS NOT NULL
    PRINT '<<< CREATED TABLE Dim_Business_License >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Dim_Business_License >>>'
go

/* 
 * TABLE: Dim_Date 
 */

CREATE TABLE Dim_Date(
    Date_SK                char(10)    NOT NULL,
    Year                   char(10)    NULL,
    Quater                 char(10)    NULL,
    Month                  char(10)    NULL,
    Week                   char(10)    NULL,
    DI_Creation_Date       char(10)    NULL,
    DI_workflowFileName    char(10)    NULL,
    CONSTRAINT PK11 PRIMARY KEY NONCLUSTERED (Date_SK)
)

go


IF OBJECT_ID('Dim_Date') IS NOT NULL
    PRINT '<<< CREATED TABLE Dim_Date >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Dim_Date >>>'
go

/* 
 * TABLE: Dim_Facility_Type 
 */

CREATE TABLE Dim_Facility_Type(
    Facility_SK            int             NOT NULL,
    FaciltyType            varchar(255)    NULL,
    DI_CreateDate          datetime        NULL,
    DI_WorkflowFileName    varchar(255)    NULL,
    CONSTRAINT PK10 PRIMARY KEY NONCLUSTERED (Facility_SK)
)

go


IF OBJECT_ID('Dim_Facility_Type') IS NOT NULL
    PRINT '<<< CREATED TABLE Dim_Facility_Type >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Dim_Facility_Type >>>'
go

/* 
 * TABLE: Dim_Food_Inspections_Results 
 */

CREATE TABLE Dim_Food_Inspections_Results(
    Result_SK              int             NOT NULL,
    Result                 varchar(255)    NULL,
    DI_CreateDate          date            NULL,
    DI_WorkflowFileName    varchar(255)    NULL,
    CONSTRAINT PK8 PRIMARY KEY NONCLUSTERED (Result_SK)
)

go


IF OBJECT_ID('Dim_Food_Inspections_Results') IS NOT NULL
    PRINT '<<< CREATED TABLE Dim_Food_Inspections_Results >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Dim_Food_Inspections_Results >>>'
go

/* 
 * TABLE: Dim_Inspection_Type 
 */

CREATE TABLE Dim_Inspection_Type(
    InspectionType_SK      int             NOT NULL,
    InspectionType         varchar(255)    NULL,
    DI_CreateDate          datetime        NULL,
    DI_WorkflowFileName    varchar(255)    NULL,
    CONSTRAINT PK1 PRIMARY KEY NONCLUSTERED (InspectionType_SK)
)

go


IF OBJECT_ID('Dim_Inspection_Type') IS NOT NULL
    PRINT '<<< CREATED TABLE Dim_Inspection_Type >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Dim_Inspection_Type >>>'
go

/* 
 * TABLE: Dim_Risk_Category 
 */

CREATE TABLE Dim_Risk_Category(
    Risk_SK                int             NOT NULL,
    Risk                   varchar(255)    NULL,
    DI_CreateDate          datetime        NULL,
    DI_WorkflowFileName    varchar(255)    NULL,
    CONSTRAINT PK3 PRIMARY KEY NONCLUSTERED (Risk_SK)
)

go


IF OBJECT_ID('Dim_Risk_Category') IS NOT NULL
    PRINT '<<< CREATED TABLE Dim_Risk_Category >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Dim_Risk_Category >>>'
go

/* 
 * TABLE: Dim_Violation 
 */

CREATE TABLE Dim_Violation(
    Violation_SK             int             NOT NULL,
    Violation_Code           varchar(255)    NULL,
    Violation_Description    varchar(255)    NULL,
    Violation_Comment        varchar(255)    NULL,
    DI_CreateDate            char(10)        NULL,
    DI_WorkflowFileName      char(10)        NULL,
    CONSTRAINT PK9 PRIMARY KEY NONCLUSTERED (Violation_SK)
)

go


IF OBJECT_ID('Dim_Violation') IS NOT NULL
    PRINT '<<< CREATED TABLE Dim_Violation >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Dim_Violation >>>'
go

/* 
 * TABLE: Fact_Inspection 
 */

CREATE TABLE Fact_Inspection(
    Inspection_SK          int             NOT NULL,
    Facility_SK            int             NOT NULL,
    Risk_SK                int             NOT NULL,
    InspectionType_SK      int             NOT NULL,
    Result_SK              int             NOT NULL,
    BusinessLicense_SK     int             NOT NULL,
    InspectionScore        varchar(255)    NULL,
    Inspection_Date        date            NULL,
    Licence_Number         varchar(255)    NULL,
    DI_CreateDate          datetime        NULL,
    DI_WorkflowFileName    varchar(255)    NULL,
    Date_SK                char(10)        NOT NULL,
    CONSTRAINT PK2 PRIMARY KEY NONCLUSTERED (Inspection_SK)
)

go


IF OBJECT_ID('Fact_Inspection') IS NOT NULL
    PRINT '<<< CREATED TABLE Fact_Inspection >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Fact_Inspection >>>'
go

/* 
 * TABLE: Fact_Violation 
 */

CREATE TABLE Fact_Violation(
    FactViolationSK        int             NOT NULL,
    Violation_SK           int             NOT NULL,
    Inspection_SK          int             NOT NULL,
    Violation_Points       varchar(255)    NULL,
    DI_CreateDate          date            NULL,
    DI_WorkflowFileName    varchar(255)    NULL,
    CONSTRAINT PK7 PRIMARY KEY NONCLUSTERED (FactViolationSK)
)

go


IF OBJECT_ID('Fact_Violation') IS NOT NULL
    PRINT '<<< CREATED TABLE Fact_Violation >>>'
ELSE
    PRINT '<<< FAILED CREATING TABLE Fact_Violation >>>'
go

/* 
 * TABLE: Fact_Inspection 
 */

ALTER TABLE Fact_Inspection ADD CONSTRAINT RefDim_Risk_Category2 
    FOREIGN KEY (Risk_SK)
    REFERENCES Dim_Risk_Category(Risk_SK)
go

ALTER TABLE Fact_Inspection ADD CONSTRAINT RefDim_Business_License4 
    FOREIGN KEY (BusinessLicense_SK)
    REFERENCES Dim_Business_License(BusinessLicense_SK)
go

ALTER TABLE Fact_Inspection ADD CONSTRAINT RefDim_Food_Inspections_Results6 
    FOREIGN KEY (Result_SK)
    REFERENCES Dim_Food_Inspections_Results(Result_SK)
go

ALTER TABLE Fact_Inspection ADD CONSTRAINT RefDim_Facility_Type7 
    FOREIGN KEY (Facility_SK)
    REFERENCES Dim_Facility_Type(Facility_SK)
go

ALTER TABLE Fact_Inspection ADD CONSTRAINT RefDim_Date11 
    FOREIGN KEY (Date_SK)
    REFERENCES Dim_Date(Date_SK)
go

ALTER TABLE Fact_Inspection ADD CONSTRAINT RefDim_Inspection_Type1 
    FOREIGN KEY (InspectionType_SK)
    REFERENCES Dim_Inspection_Type(InspectionType_SK)
go


/* 
 * TABLE: Fact_Violation 
 */

ALTER TABLE Fact_Violation ADD CONSTRAINT RefFact_Inspection9 
    FOREIGN KEY (Inspection_SK)
    REFERENCES Fact_Inspection(Inspection_SK)
go

ALTER TABLE Fact_Violation ADD CONSTRAINT RefDim_Violation10 
    FOREIGN KEY (Violation_SK)
    REFERENCES Dim_Violation(Violation_SK)
go



