import os
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from dotenv import load_dotenv

# 1. เทคนิคหา Path โปรเจกต์หลักอัตโนมัติ (ป้องกันปัญหาหาไฟล์ CSV ไม่เจอ)
# ดึง Path ของไฟล์ปัจจุบัน แล้วถอยกลับไป 2 ชั้นเพื่อไปที่ Root Folder
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 2. โหลดไฟล์ .env ที่อยู่หน้า Root 
env_path = os.path.join(BASE_DIR, '.env')
load_dotenv(env_path)

db_url = os.getenv('DATABASE_URL')
if not db_url:
    raise ValueError("❌ หา DATABASE_URL ไม่เจอ! ตรวจสอบไฟล์ .env อีกครั้ง")

engine = create_engine(db_url)

def run_pipeline(csv_file_path):
    print(f"🚀 เริ่มต้นการ Ingest ข้อมูลจาก: {csv_file_path}")
    
    
    columns_to_keep = [
        ' Destination Port', ' Flow Duration', ' Total Fwd Packets', 
        ' Total Backward Packets', 'Total Length of Fwd Packets', 
        ' Total Length of Bwd Packets', 'Flow Bytes/s', ' Flow Packets/s', ' Label'
    ]
    
    # 3. Extract: อ่านไฟล์ CSV (ใช้ตัวแปรที่ประกาศด้านบน)
    df = pd.read_csv(csv_file_path, usecols=columns_to_keep)
    
    # 4. Transform: ทำ Data Cleaning
    print("🧹 กำลังทำความสะอาดข้อมูล (Cleaning)...")
    df.columns = df.columns.str.strip()
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True)
    
    df.rename(columns={
        'Destination Port': 'destination_port',
        'Flow Duration': 'flow_duration',
        'Total Fwd Packets': 'total_fwd_packets',
        'Total Backward Packets': 'total_bwd_packets',
        'Total Length of Fwd Packets': 'total_length_fwd_packets',
        'Total Length of Bwd Packets': 'total_length_bwd_packets',
        'Flow Bytes/s': 'flow_bytes_per_sec',
        'Flow Packets/s': 'flow_packets_per_sec',
        'Label': 'label'
    }, inplace=True)

    # 5. Load: นำข้อมูลเข้า PostgreSQL
    print("💾 กำลังโหลดข้อมูลเข้าฐานข้อมูล...")
    df.to_sql('network_traffic', engine, if_exists='append', index=False, chunksize=10000)
    
    print("✅ โหลดข้อมูลสำเร็จ!")

if __name__ == "__main__":
  
    target_csv = os.path.join(BASE_DIR, 'data', 'raw', 'Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')
    
   
    if os.path.exists(target_csv):
        run_pipeline(target_csv)
    else:
        print(f"❌ หาไฟล์ CSV ไม่เจอที่ตำแหน่ง: {target_csv}")