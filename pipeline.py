import os
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# 1.  Database 
load_dotenv()
db_url = os.getenv('DATABASE_URL')
engine = create_engine(db_url)

def run_pipeline(csv_file_path):
    print(f"🚀 เริ่มต้นการ Ingest ข้อมูลจาก: {csv_file_path}")
    
    # 2. Extract: อ่านไฟล์ CSV
    # ใช้ usecols เพื่อดึงมาเฉพาะคอลัมน์ที่ใช้จริง ลดการใช้ Memory
    columns_to_keep = [
        ' Destination Port', ' Flow Duration', ' Total Fwd Packets', 
        ' Total Backward Packets', 'Total Length of Fwd Packets', 
        ' Total Length of Bwd Packets', 'Flow Bytes/s', ' Flow Packets/s', ' Label'
    ]
    df = pd.read_csv(csv_file_path, usecols=columns_to_keep)
    
    # 3. Transform: ทำ Data Cleaning
    print("🧹 กำลังทำความสะอาดข้อมูล (Cleaning)...")
    
    # 3.1 ลบช่องว่าง (Space) หน้าชื่อคอลัมน์ที่เป็นปัญหาสุดคลาสสิกของ Dataset นี้
    df.columns = df.columns.str.strip()
    
    # 3.2 จัดการ Dirty Data (Infinity และ NaN)
    # ชุดข้อมูลนี้เวลามีการหารด้วย 0 มักจะหลุดค่า Infinity มา
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(inplace=True) # ลบแถวที่มีค่า NaN ทิ้ง
    
    # 3.3 เปลี่ยนชื่อคอลัมน์ให้ตรงกับ Database Schema
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

    # 4. Load: นำข้อมูลเข้า PostgreSQL
    print("💾 กำลังโหลดข้อมูลเข้าฐานข้อมูล (PostgreSQL)...")
    # chunksize คือการแบ่งส่งข้อมูลทีละ 10,000 แถว ป้องกัน RAM เต็ม
    df.to_sql('network_traffic', engine, if_exists='append', index=False, chunksize=10000)
    
    print("✅ โหลดข้อมูลสำเร็จ!")

# สั่งรัน Pipeline (เปลี่ยนชื่อไฟล์ตามที่คุณโหลดมา)
if __name__ == "__main__":
    run_pipeline('Friday-WorkingHours-Afternoon-DDos.pcap_ISCX.csv')