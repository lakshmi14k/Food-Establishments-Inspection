import pandas as pd
import re
from datetime import datetime

# ============================================
# CHICAGO DATA CLEANING
# ============================================

print("Loading Chicago data...")
chicago = pd.read_csv(r'C:\Users\laksh\OneDrive\Desktop\Project Cleanup\Food Establishments Inspection\Datasets\Chicago.tsv', 
                      sep='\t', encoding='utf-8', low_memory=False, on_bad_lines='skip')

print(f"Original Chicago records: {len(chicago)}")

# Clean column names
chicago.columns = chicago.columns.str.strip()

# Convert date columns
chicago['Inspection Date'] = pd.to_datetime(chicago['Inspection Date'], errors='coerce')

# Add DI metadata columns
chicago['DI_Process_ID'] = range(1, len(chicago) + 1)
chicago['DI_CurrentDate'] = datetime.now().strftime('%Y-%m-%d')
chicago['DI_WorkflowFileName'] = 'chicago_food_inspections'

# Handle Violations column (normalize - split into separate rows)
# Each violation is separated by | symbol
chicago_normalized = chicago.copy()

# Split violations if they exist
def split_violations(row):
    if pd.isna(row['Violations']) or row['Violations'] == '':
        return [{'violation_text': None}]
    
    violations = str(row['Violations']).split('|')
    return [{'violation_text': v.strip()} for v in violations if v.strip()]

# Create expanded dataset
chicago_expanded = []
for idx, row in chicago.iterrows():
    violations = split_violations(row)
    for violation in violations:
        new_row = row.to_dict()
        new_row['violation_text'] = violation['violation_text']
        chicago_expanded.append(new_row)

chicago_clean = pd.DataFrame(chicago_expanded)

# Extract violation components using regex
def extract_violation_code(text):
    if pd.isna(text):
        return None
    match = re.match(r'^(\d+)\.', str(text))
    return match.group(1) if match else None

def extract_violation_description(text):
    if pd.isna(text):
        return None
    match = re.match(r'^\d+\.\s*(.+?)\s*-', str(text))
    return match.group(1) if match else None

def extract_violation_comment(text):
    if pd.isna(text):
        return None
    match = re.search(r'-\s*Comments:\s*(.+)', str(text))
    return match.group(1) if match else None

chicago_clean['Violation_Code'] = chicago_clean['violation_text'].apply(extract_violation_code)
chicago_clean['Violation_Description'] = chicago_clean['violation_text'].apply(extract_violation_description)
chicago_clean['Violation_Comment'] = chicago_clean['violation_text'].apply(extract_violation_comment)

# Drop original violations column
chicago_clean = chicago_clean.drop(columns=['Violations', 'violation_text'])

print(f"Cleaned Chicago records (after normalization): {len(chicago_clean)}")

# Save cleaned Chicago data
chicago_clean.to_csv(r'C:\Users\laksh\OneDrive\Desktop\Project Cleanup\Food Establishments Inspection\Datasets\chicago_cleaned.csv', index=False)
print("✓ Chicago cleaned data saved!")

# ============================================
# DALLAS DATA CLEANING
# ============================================

print("\nLoading Dallas data...")
dallas = pd.read_csv(r'C:\Users\laksh\OneDrive\Desktop\Project Cleanup\Food Establishments Inspection\Datasets\Dallas.tsv', 
                     sep='\t', encoding='utf-8', low_memory=False, on_bad_lines='skip')

print(f"Original Dallas records: {len(dallas)}")

# Clean column names
dallas.columns = dallas.columns.str.strip()

# Convert date
dallas['Inspection Date'] = pd.to_datetime(dallas['Inspection Date'], errors='coerce')

# Add DI metadata
dallas['DI_Process_ID'] = range(1, len(dallas) + 1)
dallas['DI_CurrentDate'] = datetime.now().strftime('%Y-%m-%d')
dallas['DI_WorkflowFileName'] = 'dallas_food_inspections'

# Combine violation columns (Dallas has Violation Description-1 through -25, etc.)
violation_cols_desc = [col for col in dallas.columns if 'Violation Description' in col]
violation_cols_memo = [col for col in dallas.columns if 'Violation Memo' in col]
violation_cols_detail = [col for col in dallas.columns if 'Violation Detail' in col]
violation_cols_points = [col for col in dallas.columns if 'Violation Points' in col]

# Normalize Dallas data
dallas_expanded = []

for idx, row in dallas.iterrows():
    # Collect all violations for this inspection
    violations = []
    
    for i in range(1, 26):  # 25 possible violations
        desc_col = f'Violation Description - {i}'
        memo_col = f'Violation Memo - {i}'
        detail_col = f'Violation Detail - {i}'
        points_col = f'Violation Points - {i}'
        
        if desc_col in dallas.columns and pd.notna(row.get(desc_col)):
            violations.append({
                'description': row.get(desc_col),
                'memo': row.get(memo_col),
                'detail': row.get(detail_col),
                'points': row.get(points_col)
            })
    
    # If no violations, create one row with NULLs
    if not violations:
        violations = [{'description': None, 'memo': None, 'detail': None, 'points': None}]
    
    # Create row for each violation
    for violation in violations:
        new_row = {
            'Restaurant Name': row.get('Restaurant Name'),
            'Street Number': row.get('Street Number'),
            'Street Name': row.get('Street Name'),
            'Street Type': row.get('Street Type'),
            'Street Direction': row.get('Street Direction'),
            'Street Unit': row.get('Street Unit'),
            'Street Address': row.get('Street Address'),
            'Zip Code': row.get('Zip Code'),
            'Inspection Date': row.get('Inspection Date'),
            'Inspection Score': row.get('Inspection Score'),
            'Inspection Type': row.get('Inspection Type'),
            'Inspection Year': row.get('Inspection Year'),
            'Inspection Month': row.get('Inspection Month'),
            'Lat Long Location': row.get('Lat Long Location'),
            'Violation_Description': violation['description'],
            'Violation_Memo': violation['memo'],
            'Violation_Detail': violation['detail'],
            'Violation_Points': violation['points'],
            'DI_Process_ID': row['DI_Process_ID'],
            'DI_CurrentDate': row['DI_CurrentDate'],
            'DI_WorkflowFileName': row['DI_WorkflowFileName']
        }
        dallas_expanded.append(new_row)

dallas_clean = pd.DataFrame(dallas_expanded)

print(f"Cleaned Dallas records (after normalization): {len(dallas_clean)}")

# Save cleaned Dallas data
dallas_clean.to_csv(r'C:\Users\laksh\OneDrive\Desktop\Project Cleanup\Food Establishments Inspection\Datasets\dallas_cleaned.csv', index=False)
print("✓ Dallas cleaned data saved!")

print("\n" + "="*50)
print("CLEANING COMPLETE!")
print("="*50)
print(f"Chicago: {len(chicago_clean)} rows → chicago_cleaned.csv")
print(f"Dallas: {len(dallas_clean)} rows → dallas_cleaned.csv")