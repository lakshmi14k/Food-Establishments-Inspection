use midterm_project

select * from Fact_Inspection

delete from Fact_Inspection




select BusinessLicense_SK, count(BusinessLicense_SK) 
from Dim_Business_License
group by BusinessLicense_SK
having count(BusinessLicense_SK) > 1




select count(*) from Dim_Business_License

select * from stg_data_dallas

select * from Dim_Facility_Type


delete from Dim_Business_License

delete from Dim_Date

delete from Dim_Facility_Type

delete from Dim_Food_Inspections_Results

delete from Dim_Inspection_Type

delete from Dim_Risk_Category

delete from Dim_Violation

truncate table Fact_Inspection

select * from Fact_Inspection

drop table Fact_Inspection

select count(*) from stg_chicago

select count(*) from Fact_Inspection


drop table Dim_Date



select count(*) from Dim_Business_License

select * from Dim_Date

select count(*) from Dim_Facility_Type

select count(*) from Dim_Food_Inspections_Results

select count(*) from Dim_Inspection_Type

select count(*) from Dim_Risk_Category

select count(*) from Dim_Violation







