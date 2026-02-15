"""
Food Establishments Inspection - Master File Creation
Combines Chicago and Dallas cleaned data
Keeps only common columns for Tableau visualization
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

print("="*60)
print("FOOD INSPECTIONS - MASTER FILE CREATION")
print("="*60)

def load_cleaned_data(chicago_file, dallas_file):
    """Load cleaned Chicago and Dallas data"""
    print("\nLoading cleaned data files...")
    print("  [1/2] Loading Chicago...")
    chicago = pd.read_csv(chicago_file, low_memory=False)
    print(f"        Loaded {len(chicago):,} records")
    print("  [2/2] Loading Dallas...")
    dallas = pd.read_csv(dallas_file, low_memory=False)
    print(f"        Loaded {len(dallas):,} records")
    print(f"\n  Total records loaded: {len(chicago) + len(dallas):,}")
    return chicago, dallas

def standardize_chicago(chicago):
    """Standardize Chicago data to common schema"""
    print("\n[1/2] Standardizing Chicago columns...")
    chicago_std = pd.DataFrame({
        'inspection_id': chicago['Inspection ID'],
        'city': 'Chicago',
        'inspection_date': pd.to_datetime(chicago['Inspection Date'], errors='coerce'),
        'establishment_name': chicago['DBA Name'],
        'aka_name': chicago.get('AKA Name', ''),
        'license_number': chicago.get('License #', ''),
        'facility_type': chicago.get('Facility Type', 'UNKNOWN'),
        'inspection_type': chicago.get('Inspection Type', 'UNKNOWN'),
        'result': chicago.get('Results', 'UNKNOWN'),
        'violation_code': chicago.get('Violation_Code', ''),
        'violation_description': chicago.get('Violation_Description', ''),
        'violation_comment': chicago.get('Violation_Comment', ''),
        'address': chicago.get('Address', 'UNKNOWN'),
        'city_name': chicago.get('City', 'Chicago'),
        'state': chicago.get('State', 'IL'),
        'zip_code': chicago.get('Zip', '00000'),
        'latitude': chicago.get('Latitude', 0),
        'longitude': chicago.get('Longitude', 0)
    })
    chicago_std['year'] = chicago_std['inspection_date'].dt.year
    chicago_std['month'] = chicago_std['inspection_date'].dt.month
    chicago_std['month_name'] = chicago_std['inspection_date'].dt.month_name()
    chicago_std['inspection_date'] = chicago_std['inspection_date'].dt.date
    chicago_std['establishment_name'] = chicago_std['establishment_name'].fillna('UNKNOWN')
    chicago_std['facility_type'] = chicago_std['facility_type'].fillna('UNKNOWN')
    chicago_std['inspection_type'] = chicago_std['inspection_type'].fillna('UNKNOWN')
    chicago_std['result'] = chicago_std['result'].fillna('UNKNOWN')
    chicago_std['violation_description'] = chicago_std['violation_description'].fillna('')
    chicago_std['address'] = chicago_std['address'].fillna('UNKNOWN')
    chicago_std['zip_code'] = chicago_std['zip_code'].fillna('00000').astype(str)
    chicago_std['latitude'] = chicago_std['latitude'].fillna(0)
    chicago_std['longitude'] = chicago_std['longitude'].fillna(0)
    print(f"  ✓ Standardized {len(chicago_std):,} Chicago records")
    return chicago_std

def standardize_dallas(dallas):
    """Standardize Dallas data to common schema"""
    print("\n[2/2] Standardizing Dallas columns...")
    dallas_std = pd.DataFrame({
        'inspection_id': dallas.get('DI_Process_ID', range(len(dallas))),
        'city': 'Dallas',
        'inspection_date': pd.to_datetime(dallas['Inspection Date'], errors='coerce'),
        'establishment_name': dallas['Restaurant Name'],
        'aka_name': '',
        'license_number': '',
        'facility_type': 'Restaurant',
        'inspection_type': dallas.get('Inspection Type', 'UNKNOWN'),
        'result': 'Pass',
        'violation_code': '',
        'violation_description': dallas.get('Violation_Description', ''),
        'violation_comment': dallas.get('Violation_Detail', ''),
        'address': dallas['Street Address'],
        'city_name': 'Dallas',
        'state': 'TX',
        'zip_code': dallas.get('Zip Code', '00000'),
        'latitude': dallas.get('Lat Long Location', '').apply(lambda x: x.split(',')[0] if isinstance(x, str) and ',' in x else 0),
        'longitude': dallas.get('Lat Long Location', '').apply(lambda x: x.split(',')[1] if isinstance(x, str) and ',' in x else 0)
    })
    dallas_std['year'] = dallas_std['inspection_date'].dt.year
    dallas_std['month'] = dallas_std['inspection_date'].dt.month
    dallas_std['month_name'] = dallas_std['inspection_date'].dt.month_name()
    dallas_std['inspection_date'] = dallas_std['inspection_date'].dt.date
    if 'Inspection Score' in dallas.columns:
        dallas_std['result'] = dallas['Inspection Score'].apply(
            lambda x: 'Pass' if pd.notna(x) and x >= 70 else 'Fail' if pd.notna(x) else 'UNKNOWN'
        )
    dallas_std['establishment_name'] = dallas_std['establishment_name'].fillna('UNKNOWN')
    dallas_std['facility_type'] = dallas_std['facility_type'].fillna('Restaurant')
    dallas_std['inspection_type'] = dallas_std['inspection_type'].fillna('UNKNOWN')
    dallas_std['result'] = dallas_std['result'].fillna('UNKNOWN')
    dallas_std['violation_description'] = dallas_std['violation_description'].fillna('')
    dallas_std['address'] = dallas_std['address'].fillna('UNKNOWN')
    dallas_std['zip_code'] = dallas_std['zip_code'].fillna('00000').astype(str)
    dallas_std['latitude'] = pd.to_numeric(dallas_std['latitude'], errors='coerce').fillna(0)
    dallas_std['longitude'] = pd.to_numeric(dallas_std['longitude'], errors='coerce').fillna(0)
    print(f"  ✓ Standardized {len(dallas_std):,} Dallas records")
    return dallas_std

def add_calculated_fields(master):
    """Add useful calculated fields for Tableau"""
    print("\nAdding calculated fields...")
    master['has_violation'] = master['violation_description'].apply(lambda x: len(str(x).strip()) > 0)
    master['season'] = master['month'].apply(lambda x: 
        'Winter' if x in [12, 1, 2] else
        'Spring' if x in [3, 4, 5] else
        'Summer' if x in [6, 7, 8] else
        'Fall'
    )
    master['result_simple'] = master['result'].apply(lambda x:
        'Pass' if 'Pass' in str(x).upper() else
        'Fail' if 'Fail' in str(x).upper() else
        'Other'
    )
    print("  ✓ Added: has_violation, season, result_simple")
    return master

def save_master_file(master, output_file):
    """Save the master file"""
    print(f"\nSaving master file...")
    master = master.sort_values(['inspection_date', 'city']).reset_index(drop=True)
    master.to_csv(output_file, index=False)
    print(f"  ✓ Saved to: {output_file}")
    print(f"  ✓ Total rows: {len(master):,}")
    print(f"  ✓ Total columns: {len(master.columns)}")
    estimated_cells = len(master) * len(master.columns)
    print(f"\n  Tableau Public estimate:")
    print(f"    Cells: {estimated_cells:,} / 15,000,000 limit")
    print(f"    Usage: {estimated_cells/15000000*100:.1f}%")
    if estimated_cells < 15000000:
        print(f"    ✓ Fits in Tableau Public!")
    else:
        print(f"    ⚠ May exceed Tableau Public limit")
    return master

def print_summary(master):
    """Print summary statistics"""
    print("\n" + "="*60)
    print("MASTER DATASET SUMMARY")
    print("="*60)
    print("\nRecords by City:")
    print(master['city'].value_counts().to_string())
    print("\nRecords by Year:")
    year_counts = master['year'].value_counts().sort_index()
    print(year_counts.to_string())
    print("\nInspection Results:")
    print(master['result_simple'].value_counts().to_string())
    print("\nTop 10 Violation Types:")
    violations = master[master['violation_description'] != '']['violation_description'].value_counts().head(10)
    print(violations.to_string())
    print(f"\nTotal Statistics:")
    print(f"  Total Inspections: {len(master):,}")
    print(f"  Total Establishments: {master['establishment_name'].nunique():,}")
    print(f"  Inspections with Violations: {master['has_violation'].sum():,}")
    print(f"  Pass Rate: {(master['result_simple'] == 'Pass').sum() / len(master) * 100:.1f}%")

if __name__ == "__main__":
    print("\nStarting data combination process...\n")
    chicago_input = "C:/Users/laksh/OneDrive/Desktop/Project Cleanup/Food Establishments Inspection/Datasets/Processed/chicago_cleaned.csv"
    dallas_input = "C:/Users/laksh/OneDrive/Desktop/Project Cleanup/Food Establishments Inspection/Datasets/Processed/dallas_cleaned.csv"
    master_output = "C:/Users/laksh/OneDrive/Desktop/Project Cleanup/Food Establishments Inspection/Datasets/Processed/Food_Inspections_Master.csv"
    
    try:
        chicago, dallas = load_cleaned_data(chicago_input, dallas_input)
        chicago_std = standardize_chicago(chicago)
        dallas_std = standardize_dallas(dallas)
        print("\nCombining datasets...")
        master = pd.concat([chicago_std, dallas_std], ignore_index=True)
        print(f"  ✓ Combined: {len(master):,} total records")
        master = add_calculated_fields(master)
        master = save_master_file(master, master_output)
        print_summary(master)
        print("\n" + "="*60)
        print("✓ MASTER FILE CREATION COMPLETE!")
        print("="*60)
        print(f"\nYour master file is ready for Tableau:")
        print(f"  {master_output}")
        print("\nNext step: Load this file into Tableau Public")
        print("="*60)
    except FileNotFoundError as e:
        print(f"\n❌ ERROR: Could not find input file")
        print(f"   {e}")
        print("\n   Make sure the file paths are correct!")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()