#Importing the necessary libraries.
import csv
import json
import re
import pandas as pd

class PIIDetector:
    def __init__(self):
        # Basically this will use Regex to go through all the highly personal data and detect them further.
        self.patterns = {
            'phone': [
                r'\b(?:\+91[-.\s]?)?[6-9]\d{9}\b',
                r'\b\d{10}\b'
            ],
            'email': [
                r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            ],
            'aadhar': [
                r'\b\d{12}\b'
            ],
            'passport': [
                r'\b[A-Z]\d{7}\b'
            ],
            'upi_id': [
                r'\b[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\b'
            ],
            'ip_address': [
                r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b'
            ],
            'pin_code': [
                r'\b[1-9]\d{5}\b'
            ]
        }
        
        # Fields to check from CSV.
        self.pii_fields = {
            'name', 'first_name', 'last_name', 'customer_name', 'full_name',
            'phone', 'mobile', 'contact', 'telephone', 
            'email', 'email_id', 'mail',
            'address', 'location', 'addr',
            'aadhar', 'aadhaar', 'passport', 'pan',
            'upi_id', 'ip_address'
        }
    # Now we will not fully encryt the PII values.
    # We will be masking/redacting them by the character "X".
    # Like this less characters from the PII will be visible.
    def mask_value(self, value, pii_type):
        if pii_type in ['phone', 'aadhar'] and len(value) >= 4:
            return f"{value[:2]}{'X' * (len(value) - 4)}{value[-2:]}"
        elif pii_type == 'email' and '@' in value:
            local, domain = value.split('@', 1)
            return f"{local[0]}{'X' * (len(local) - 1)}@{domain}"
        elif pii_type == 'ip_address':
            parts = value.split('.')
            if len(parts) == 4:
                return f"{parts[0]}.{parts[1]}.XXX.XXX"
        elif pii_type == 'passport' and len(value) > 1:
            return f"{value[0]}{'X' * (len(value) - 1)}"
        elif pii_type in ['name', 'address']:
            words = value.split()
            if len(words) > 1:
                return f"{words[0][0]}XXX {words[-1][0]}XXX"
            return "XXXX"
        
        return "[REDACTED]"

    # Detection of PII like Phone no, Email id, Aadhar Card no, Passports, UPI IDs, etc.
    # This will be done becaue the Regex will detect it.
    def detect_pii_patterns(self, text):
        found_pii = []
        
        for pii_type, patterns in self.patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    value = match.group()
                    if self.validate_pii(value, pii_type):
                        found_pii.append((value, pii_type))
        
        return found_pii

    # Double-checks if what we found is really sensitive data. For example, "1234567890" might look like a phone number.
    # But this function checks if it's actually a valid phone format which it is not.
    def validate_pii(self, value, pii_type):
        if pii_type == 'phone':
            digits = re.sub(r'\D', '', value)
            return 10 <= len(digits) <= 13
        elif pii_type == 'aadhar':
            return len(re.sub(r'\D', '', value)) == 12
        elif pii_type == 'email':
            return '@' in value and '.' in value.split('@')[-1]
        elif pii_type == 'pin_code':
            return len(value) == 6
        return True

    # Looks at the name of the data field. If it's called "email" or "phone".
    # We are extra careful that it contains personal information.
    def check_field_name(self, field_name):
        field_lower = field_name.lower()
        return any(pii_field in field_lower for pii_field in self.pii_fields)

    # Main working function.
    # It takes a record of data, examines each piece of information
    # Then decides if it's sensitive, and either masks it or leaves it alone.
    def process_json_data(self, data):
        has_pii = False
        redacted_data = {}
        
        for field_name, value in data.items():
            if not isinstance(value, str) or not value.strip():
                redacted_data[field_name] = value
                continue   
            original_value = value
            if self.check_field_name(field_name):
                if field_name.lower() in ['name', 'first_name', 'last_name', 'customer_name']:
                    redacted_value = self.mask_value(value, 'name')
                    has_pii = True
                elif 'address' in field_name.lower():
                    redacted_value = self.mask_value(value, 'address')  
                    has_pii = True
                else:
                    pii_found = self.detect_pii_patterns(value)
                    if pii_found:
                        redacted_value = value
                        for pii_value, pii_type in pii_found:
                            mask = self.mask_value(pii_value, pii_type)
                            redacted_value = redacted_value.replace(pii_value, mask)
                        has_pii = True
                    else:
                        redacted_value = value
            else:
                pii_found = self.detect_pii_patterns(value)
                if pii_found:
                    redacted_value = value
                    for pii_value, pii_type in pii_found:
                        mask = self.mask_value(pii_value, pii_type)
                        redacted_value = redacted_value.replace(pii_value, mask)
                    has_pii = True
                else:
                    redacted_value = value
            
            redacted_data[field_name] = redacted_value
                    
        return redacted_data, has_pii

# Handling the entire operation - opens the input file, processes each record one by one.
# And saves the cleaned results to a new file.
def process_csv_file(input_file, output_file):
    detector = PIIDetector()
    results = []
    
    print(f"Reading {input_file}...")
    
    try:
        df = pd.read_csv(input_file)
        total_records = len(df)
        pii_count = 0
        
        print(f"Processing {total_records} records...")
        
        for index, row in df.iterrows():
            record_id = row['record_id']
            json_str = row['data_json']
            
            try:
                # Parse JSON data.
                original_data = json.loads(json_str)
                
                # Process for PII.
                redacted_data, has_pii = detector.process_json_data(original_data)
                
                if has_pii:
                    pii_count += 1
                
                # Create result.
                results.append({
                    'record_id': record_id,
                    'redacted_data_json': json.dumps(redacted_data),
                    'is_pii': has_pii
                })
                
                if (index + 1) % 100 == 0:
                    print(f"Processed {index + 1}/{total_records} records...")
                    
            except json.JSONDecodeError:
                print(f"JSON error in record {record_id}")
                results.append({
                    'record_id': record_id,
                    'redacted_data_json': json_str,
                    'is_pii': False
                })
        
        # Saving the results.
        output_df = pd.DataFrame(results)
        output_df.to_csv(output_file, index=False)
        
        print(f"\nCompleted!")
        print(f"Total records: {total_records}")
        print(f"Records with PII: {pii_count}")
        print(f"PII detection rate: {(pii_count/total_records)*100:.1f}%")
        print(f"Output saved to: {output_file}")
        
        # Showing some Sample Data.
        pii_examples = output_df[output_df['is_pii'] == True].head(3)
        print(f"\nSample results:")
        for _, row in pii_examples.iterrows():
            print(f"Record {row['record_id']}: {row['redacted_data_json']}")
      
    except FileNotFoundError:
        print(f"File not found: {input_file}")
    except Exception as e:
        print(f"Error: {e}")

# Handles the entire operation - opens the input file, processes each record one by one.
# And saves the cleaned results to a new file.
if __name__ == "__main__":
    import sys
    import os
    import time
    
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = "iscp_pii_dataset.csv"  # Given dataset.
    
    output_file = "redacted_output_jui_kalan.csv"
    try:
        if os.path.exists(output_file):
            with open(output_file, 'a'):
                pass
        process_csv_file(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}") 



