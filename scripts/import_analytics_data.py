import csv
import re
import os
import uuid
from datetime import datetime, timedelta
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import random

# Database Setup (Re-using model definitions implicitly)
DATABASE_URL = "sqlite:///./savemom.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class VitalsRecord(Base):
    __tablename__ = "VitalsRecord"
    id = Column(String, primary_key=True)
    health_id = Column(String, index=True)
    bloodPressureH = Column(Integer)
    bloodPressureL = Column(Integer)
    bloodSaturation = Column(Float)
    temperature = Column(Float)
    heartRate = Column(Integer)
    bloodGlucose = Column(Float)
    createdAt = Column(DateTime)
    riskStatus = Column(String, default="LOW")

# Target Data
TARGET_HEALTH_ID = "f2d9ec44e2e14a9bacdc89e197c73223"

def parse_nurse_vitals(text):
    data = {}
    # Extract BP: 120/80
    bp_match = re.search(r'bp\s*(\d+)/(\d+)', text.lower())
    if bp_match:
        data['bloodPressureH'] = int(bp_match.group(1))
        data['bloodPressureL'] = int(bp_match.group(2))
    
    # Extract HR: hr 80 or pulse 80
    hr_match = re.search(r'(hr|pulse)\s*(\d+)', text.lower())
    if hr_match:
        data['heartRate'] = int(hr_match.group(2))
    
    # Extract Temp: temp 98.6
    temp_match = re.search(r'temp\s*(\d+\.?\d*)', text.lower())
    if temp_match:
        data['temperature'] = float(temp_match.group(1))
    
    # Extract O2: oxygen sat is 96%
    o2_match = re.search(r'oxygen sat is\s*(\d+)', text.lower())
    if o2_match:
        data['bloodSaturation'] = float(o2_match.group(1))
        
    return data

def parse_lab_vitals(text):
    data = {}
    # Extract Glucose: Sugar and it's 300 or Sugar entry: 11.5
    glucose_match = re.search(r'(sugar|glucose).*?(\d+\.?\d*)', text.lower())
    if glucose_match:
        val = float(glucose_match.group(2))
        # Handle mmol/L vs mg/dL (rough heuristic)
        if val < 30: # Likely mmol/L
            val = val * 18
        data['bloodGlucose'] = val
    return data

def main():
    db = SessionLocal()
    records = []
    
    # Parse Nurse Dataset
    nurse_csv = "../Nurse_NLP_model/nurse/dataset.csv"
    if os.path.exists(nurse_csv):
        print(f"Parsing {nurse_csv}...")
        with open(nurse_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('label') == '1': # Vitals label
                    extracted = parse_nurse_vitals(row['text'])
                    if extracted:
                        records.append(extracted)

    # Parse Lab Dataset
    lab_csv = "../Lab_NLP_model/dataset.csv"
    if os.path.exists(lab_csv):
        print(f"Parsing {lab_csv}...")
        with open(lab_csv, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get('label') == '3': # add_lab_reading label
                    extracted = parse_lab_vitals(row['text'])
                    if extracted:
                        records.append(extracted)

    print(f"Extracted {len(records)} raw data points.")
    
    # Filter for valid records
    valid_records = [r for r in records if len(r) > 0]
    random.shuffle(valid_records)
    valid_records = valid_records[:30] # Limit to 30 for a clean chart
    
    # Insert into DB
    start_date = datetime.now() - timedelta(days=30)
    for i, data in enumerate(valid_records):
        # Default values for missing pieces to ensure charts look 
        bp_h = data.get('bloodPressureH', random.randint(110, 130))
        bp_l = data.get('bloodPressureL', random.randint(70, 85))
        hr = data.get('heartRate', random.randint(70, 90))
        gl = data.get('bloodGlucose', random.randint(80, 120))
        sat = data.get('bloodSaturation', 98.0)
        temp = data.get('temperature', 98.4)
        
        # Spread records over 30 days
        created_at = start_date + timedelta(days=i) + timedelta(hours=random.randint(0, 23))
        
        v = VitalsRecord(
            id=str(uuid.uuid4()),
            health_id=TARGET_HEALTH_ID,
            bloodPressureH=bp_h,
            bloodPressureL=bp_l,
            heartRate=hr,
            bloodGlucose=gl,
            bloodSaturation=sat,
            temperature=temp,
            createdAt=created_at,
            riskStatus="LOW" if bp_h < 140 else "MEDIUM"
        )
        db.add(v)
    
    db.commit()
    print(f"Successfully imported {len(valid_records)} records for Health ID: {TARGET_HEALTH_ID}")
    db.close()

if __name__ == "__main__":
    main()
