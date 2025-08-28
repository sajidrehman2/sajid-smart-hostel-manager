import streamlit as st
import pandas as pd
import logging
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import os
import PyPDF2
from io import BytesIO
import openpyxl
import random

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('sshm_system.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger('SSHMSystem')

# Page configuration
st.set_page_config(
    page_title='Sajid\'s Smart Hostel Manager (SSHM)',
    page_icon='🏨',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Enhanced CSS with file upload styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Global Styling */
    .stApp {
        background: #f8fafc;
        font-family: 'Inter', sans-serif;
    }
    
    .main .block-container {
        padding: 2rem;
        max-width: 1400px;
    }
    
    /* Dashboard Header */
    .dashboard-header {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        color: white;
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .dashboard-title {
        font-size: 2.5rem;
        font-weight: 800;
        margin: 0;
        text-align: center;
    }
    
    .dashboard-subtitle {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-top: 0.5rem;
        text-align: center;
        font-weight: 400;
    }
    
    /* File Upload Section */
    .file-upload-section {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 2px dashed #d1d5db;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .file-upload-section:hover {
        border-color: #3b82f6;
        background: #f8fafc;
    }
    
    .file-upload-icon {
        font-size: 3rem;
        color: #6b7280;
        margin-bottom: 1rem;
    }
    
    .file-upload-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 0.5rem;
    }
    
    .file-upload-subtitle {
        color: #6b7280;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    
    .file-info-card {
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: left;
    }
    
    .file-info-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
    }
    
    .file-info-name {
        font-weight: 600;
        color: #1f2937;
    }
    
    .file-info-details {
        font-size: 0.9rem;
        color: #6b7280;
    }
    
    .file-type-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
    }
    
    .file-type-csv {
        background: #dcfce7;
        color: #166534;
    }
    
    .file-type-pdf {
        background: #fef2f2;
        color: #991b1b;
    }
    
    .file-type-xlsx {
        background: #f0f9ff;
        color: #1e40af;
    }
    
    .file-type-txt {
        background: #f3f4f6;
        color: #374151;
    }
    
    .file-type-other {
        background: #fef3c7;
        color: #92400e;
    }
    
    /* Stats Cards */
    .stat-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .stat-card.blue::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #3b82f6, #1d4ed8);
    }
    
    .stat-card.green::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #10b981, #059669);
    }
    
    .stat-card.red::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #ef4444, #dc2626);
    }
    
    .stat-card.yellow::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, #f59e0b, #d97706);
    }
    
    .stat-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
    }
    
    .stat-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 1rem;
    }
    
    .stat-icon {
        font-size: 2.5rem;
        opacity: 0.8;
    }
    
    .stat-number {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1f2937;
        line-height: 1;
        margin: 0.5rem 0;
    }
    
    .stat-label {
        color: #1f2937;
        font-size: 0.95rem;
        font-weight: 700;
        margin-bottom: 0.25rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .stat-sublabel {
        color: #6b7280;
        font-size: 0.8rem;
        font-weight: 400;
    }
    
    /* Section Cards */
    .section-card {
        background: white;
        border-radius: 12px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    
    .section-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    
    .section-title::before {
        content: '';
        width: 4px;
        height: 24px;
        background: linear-gradient(135deg, #1e40af, #7c3aed);
        border-radius: 2px;
    }
    
    /* Log Entry Styling */
    .log-entry {
        background: white;
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 0.75rem;
        transition: all 0.3s ease;
        border-left: 4px solid #6b7280;
    }
    
    .log-entry.info {
        border-left-color: #3b82f6;
        background: #f0f9ff;
    }
    
    .log-entry.success {
        border-left-color: #10b981;
        background: #ecfdf5;
    }
    
    .log-entry.error {
        border-left-color: #ef4444;
        background: #fef2f2;
    }
    
    .log-entry.warning {
        border-left-color: #f59e0b;
        background: #fffbeb;
    }
    
    .log-entry:hover {
        transform: translateX(4px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    
    .log-header {
        display: flex;
        align-items: center;
        justify-content: between;
        margin-bottom: 0.5rem;
        gap: 1rem;
    }
    
    .log-level {
        font-size: 0.75rem;
        font-weight: 700;
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    .log-level.info {
        background: #dbeafe;
        color: #1e40af;
    }
    
    .log-level.success {
        background: #d1fae5;
        color: #065f46;
    }
    
    .log-level.error {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .log-level.warning {
        background: #fef3c7;
        color: #92400e;
    }
    
    .log-timestamp {
        font-size: 0.8rem;
        color: #6b7280;
        font-weight: 500;
    }
    
    .log-message {
        font-weight: 600;
        color: #1f2937;
        margin-bottom: 0.25rem;
    }
    
    .log-details {
        font-size: 0.9rem;
        color: #6b7280;
        line-height: 1.4;
    }
    
    /* Filter Controls */
    .filter-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    
    .filter-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1f2937;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Professional Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #1e40af 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s ease;
        width: 100%;
        box-shadow: 0 2px 4px rgba(30, 64, 175, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(30, 64, 175, 0.4);
    }
    
    /* Alert Messages */
    .success-alert {
        background: #ecfdf5;
        border: 1px solid #a7f3d0;
        color: #065f46;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #10b981;
        font-weight: 500;
    }
    
    .info-alert {
        background: #f0f9ff;
        border: 1px solid #bfdbfe;
        color: #1e40af;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #3b82f6;
        font-weight: 500;
    }
    
    .warning-alert {
        background: #fffbeb;
        border: 1px solid #fed7aa;
        color: #92400e;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #f59e0b;
        font-weight: 500;
    }
    
    .error-alert {
        background: #fef2f2;
        border: 1px solid #fecaca;
        color: #991b1b;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        border-left: 4px solid #ef4444;
        font-weight: 500;
    }
    
    /* Charts and Visualizations */
    .chart-container {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
    }
    
    /* Room Allocation Cards */
    .room-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        border-left: 5px solid #3b82f6;
        transition: all 0.3s ease;
    }
    
    .room-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);
    }
    
    .room-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 1rem;
        font-weight: 700;
        font-size: 1.1rem;
    }
    
    .occupancy-badge {
        padding: 0.25rem 0.75rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    
    .occupancy-full {
        background: #fee2e2;
        color: #991b1b;
    }
    
    .occupancy-partial {
        background: #fef3c7;
        color: #92400e;
    }
    
    .occupancy-empty {
        background: #d1fae5;
        color: #065f46;
    }
</style>
""", unsafe_allow_html=True)

# File Processing Functions
class FileProcessor:
    @staticmethod
    def get_file_type(filename):
        """Get file type from filename"""
        extension = filename.split('.')[-1].lower()
        return extension
    
    @staticmethod
    def get_file_icon(file_type):
        """Get appropriate icon for file type"""
        icons = {
            'csv': '📊',
            'xlsx': '📈', 
            'xls': '📈',
            'pdf': '📄',
            'txt': '📝',
            'json': '🔧',
            'xml': '🔧'
        }
        return icons.get(file_type, '📎')
    
    @staticmethod
    def format_file_size(size_bytes):
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0B"
        size_names = ["B", "KB", "MB", "GB"]
        import math
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_names[i]}"
    
    @staticmethod
    def process_csv(file):
        """Process CSV file and return basic info"""
        try:
            # Reset pointer if file-like
            try:
                file.seek(0)
            except Exception:
                pass
            df = pd.read_csv(file)
            return {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'preview': df.head().to_dict('records'),
                'data': df  # Store actual dataframe
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def process_excel(file):
        """Process Excel file and return basic info"""
        try:
            try:
                file.seek(0)
            except Exception:
                pass
            df = pd.read_excel(file)
            return {
                'rows': len(df),
                'columns': len(df.columns),
                'column_names': list(df.columns),
                'preview': df.head().to_dict('records'),
                'data': df  # Store actual dataframe
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def process_pdf(file):
        """Process PDF file and return basic info"""
        try:
            try:
                file.seek(0)
            except Exception:
                pass
            pdf_reader = PyPDF2.PdfReader(file)
            text_preview = ""
            if len(pdf_reader.pages) > 0:
                try:
                    text_preview = pdf_reader.pages[0].extract_text() or ""
                except Exception:
                    text_preview = ""
            return {
                'pages': len(pdf_reader.pages),
                'text_preview': (text_preview[:200] + "...") if text_preview else ""
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def process_text(file):
        """Process text file and return basic info"""
        try:
            try:
                file.seek(0)
            except Exception:
                pass
            content = file.read()
            if isinstance(content, bytes):
                content = content.decode('utf-8', errors='ignore')
            return {
                'lines': len(content.split('\n')),
                'characters': len(content),
                'preview': content[:200] + "..." if len(content) > 200 else content
            }
        except Exception as e:
            return {'error': str(e)}

# Room Allocation Algorithm Class
class RoomAllocator:
    def __init__(self):
        self.students_df = None
        self.allocation_results = None
        
    def load_student_data(self, df):
        """Load and validate student data"""
        required_columns = ['student_id', 'name', 'gender']
        
        # Check for required columns (flexible naming)
        df_columns_lower = [col.lower() for col in df.columns]
        
        # Map common variations
        column_mapping = {}
        for req_col in required_columns:
            found = False
            for df_col in df.columns:
                if any(variation in df_col.lower() for variation in [req_col.replace('_', ''), req_col]):
                    column_mapping[req_col] = df_col
                    found = True
                    break
            if not found and req_col in ['student_id']:
                # Try alternatives for student_id
                for df_col in df.columns:
                    if any(alt in df_col.lower() for alt in ['id', 'student', 'roll']):
                        column_mapping[req_col] = df_col
                        found = True
                        break
            
            if not found:
                raise ValueError(f"Missing required column: {req_col}")
        
        # Create normalized dataframe
        self.students_df = pd.DataFrame()
        for req_col, actual_col in column_mapping.items():
            self.students_df[req_col] = df[actual_col]
        
        # Add optional columns with defaults
        optional_columns = ['course', 'year', 'sleep_time', 'study_hours', 'social_level', 'cleanliness']
        for col in optional_columns:
            if col in df.columns:
                self.students_df[col] = df[col]
            else:
                # Try to find similar columns
                found_col = None
                for df_col in df.columns:
                    if col.lower() in df_col.lower():
                        found_col = df_col
                        break
                
                if found_col:
                    self.students_df[col] = df[found_col]
                else:
                    # Set defaults
                    if col in ['sleep_time', 'study_hours', 'social_level', 'cleanliness']:
                        self.students_df[col] = 'medium'
                    elif col == 'course':
                        self.students_df[col] = 'General'
                    elif col == 'year':
                        self.students_df[col] = 1
        
        return True
    
    def calculate_compatibility_score(self, student1, student2):
        """Calculate compatibility between two students"""
        score = 0
        
        # Gender matching (mandatory)
        if student1['gender'] == student2['gender']:
            score += 10
        else:
            return 0  # Cannot room together
            
        # Academic compatibility
        if student1.get('course') == student2.get('course'):
            score += 5
        if student1.get('year') == student2.get('year'):
            score += 3
            
        # Lifestyle compatibility
        lifestyle_factors = ['sleep_time', 'study_hours', 'social_level', 'cleanliness']
        for factor in lifestyle_factors:
            if student1.get(factor) == student2.get(factor):
                score += 2
                
        return score
    
    def allocate_rooms(self, max_students_per_room=2, total_rooms=None):
        """Allocate students to rooms using compatibility scoring"""
        if self.students_df is None:
            raise ValueError("No student data loaded")
            
        students = self.students_df.to_dict('records')
        allocated_students = set()
        room_allocations = []
        room_number = 1
        
        # Sort students by gender for better grouping
        students_sorted = sorted(students, key=lambda x: (x['gender'], x.get('course', ''), x.get('year', 0)))
        
        for student in students_sorted:
            if student['student_id'] in allocated_students:
                continue
                
            current_room = {
                'room_number': f"R{room_number:03d}",
                'students': [student],
                'capacity': max_students_per_room,
                'gender': student['gender']
            }
            allocated_students.add(student['student_id'])
            
            # Find compatible roommates
            if max_students_per_room > 1:
                best_matches = []
                for other_student in students_sorted:
                    if (other_student['student_id'] not in allocated_students and 
                        len(current_room['students']) < max_students_per_room):
                        
                        compatibility = self.calculate_compatibility_score(student, other_student)
                        if compatibility > 0:
                            best_matches.append((other_student, compatibility))
                
                # Sort by compatibility and add best matches
                best_matches.sort(key=lambda x: x[1], reverse=True)
                for match_student, score in best_matches:
                    if len(current_room['students']) < max_students_per_room:
                        current_room['students'].append(match_student)
                        allocated_students.add(match_student['student_id'])
            
            room_allocations.append(current_room)
            room_number += 1
            
            # Stop if we've reached room limit
            if total_rooms and len(room_allocations) >= total_rooms:
                break
        
        self.allocation_results = room_allocations
        return room_allocations
    
    def get_allocation_summary(self):
        """Get summary statistics of allocation"""
        if not self.allocation_results:
            return None
            
        total_students = sum(len(room['students']) for room in self.allocation_results)
        total_rooms = len(self.allocation_results)
        
        # Calculate occupancy rates
        occupancy_rates = []
        for room in self.allocation_results:
            rate = len(room['students']) / room['capacity'] * 100
            occupancy_rates.append(rate)
        
        avg_occupancy = sum(occupancy_rates) / len(occupancy_rates) if occupancy_rates else 0
        
        # Gender distribution
        male_rooms = len([r for r in self.allocation_results if r['gender'] == 'Male'])
        female_rooms = len([r for r in self.allocation_results if r['gender'] == 'Female'])
        
        return {
            'total_students': total_students,
            'total_rooms': total_rooms,
            'average_occupancy': round(avg_occupancy, 1),
            'male_rooms': male_rooms,
            'female_rooms': female_rooms,
            'unallocated_students': len(self.students_df) - total_students if self.students_df is not None else 0
        }

# Logging System Class (Enhanced)
class SSHMLoggingSystem:
    def __init__(self):
        self.log_file = 'sshm_system.log'
        self.session_logs = []
        self.uploaded_files = []
        
    def log_action(self, level, category, action, details, user="Admin", metadata=None):
        """Log an action with structured data"""
        log_entry = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'level': level,
            'category': category,
            'action': action,
            'details': details,
            'user': user,
            'metadata': metadata or {}
        }
        
        self.session_logs.append(log_entry)
        
        # Also log to file
        if level == 'ERROR':
            logger.error(f"{category.upper()} - {action}: {details}")
        elif level == 'WARNING':
            logger.warning(f"{category.upper()} - {action}: {details}")
        else:
            logger.info(f"{category.upper()} - {action}: {details}")
            
        return log_entry
    
    def log_file_upload(self, filename, file_type, file_size, processing_result):
        """Log file upload activity"""
        if 'error' in processing_result:
            self.log_action('ERROR', 'UPLOAD', 'File Upload Failed', 
                          f'Failed to process {filename}: {processing_result["error"]}',
                          metadata={'filename': filename, 'file_type': file_type, 'size': file_size})
        else:
            self.log_action('SUCCESS', 'UPLOAD', 'File Uploaded Successfully', 
                          f'{filename} uploaded and processed successfully',
                          metadata={'filename': filename, 'file_type': file_type, 'size': file_size, **{k:v for k,v in processing_result.items() if k != 'data'}})
        
        # Store file info
        file_info = {
            'filename': filename,
            'file_type': file_type,
            'size': file_size,
            'upload_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'processing_result': processing_result
        }
        self.uploaded_files.append(file_info)
        return file_info
    
    def get_logs(self, level_filter=None, hours_back=24):
        """Get filtered logs"""
        if level_filter:
            return [log for log in self.session_logs if log['level'] == level_filter]
        return self.session_logs
    
    def get_log_stats(self):
        """Get logging statistics"""
        total = len(self.session_logs)
        success = len([l for l in self.session_logs if l['level'] == 'SUCCESS'])
        errors = len([l for l in self.session_logs if l['level'] == 'ERROR'])
        warnings = len([l for l in self.session_logs if l['level'] == 'WARNING'])
        info = len([l for l in self.session_logs if l['level'] == 'INFO'])
        
        return {
            'total': total,
            'success': success,
            'errors': errors,
            'warnings': warnings,
            'info': info,
            'files_uploaded': len(self.uploaded_files)
        }

# Initialize logging system
if 'logging_system' not in st.session_state:
    st.session_state.logging_system = SSHMLoggingSystem()

logging_system = st.session_state.logging_system

# Initialize room allocator
if 'room_allocator' not in st.session_state:
    st.session_state.room_allocator = RoomAllocator()

# Add some sample logs if none exist
if not logging_system.session_logs:
    logging_system.log_action('SUCCESS', 'ALLOCATION', 'Room Allocation Completed', 
                            '60 students allocated to 20 rooms successfully', 
                            metadata={'students': 60, 'rooms': 20, 'duration': '2.3s'})
    
    logging_system.log_action('INFO', 'UPLOAD', 'CSV File Uploaded', 
                            'student_data_2025.csv uploaded with 60 records', 
                            metadata={'filename': 'student_data_2025.csv', 'records': 60})
    
    logging_system.log_action('WARNING', 'DATA', 'Missing Data Detected', 
                            '5 students missing sleep_time preference', 
                            metadata={'missing_fields': ['sleep_time'], 'affected': 5})
    
    logging_system.log_action('SUCCESS', 'EXPORT', 'Results Exported', 
                            'room_allocations.csv downloaded successfully', 
                            metadata={'format': 'csv', 'rooms': 18})
    
    logging_system.log_action('ERROR', 'ALLOCATION', 'Allocation Failed', 
                            'Insufficient data for clustering algorithm', 
                            metadata={'error': 'DataError', 'students': 5})

# Dashboard Header
st.markdown("""
<div class="dashboard-header">
    <h1 class="dashboard-title">🏨 Sajid's Smart Hostel Manager (SSHM)</h1>
    <p class="dashboard-subtitle">Advanced File Processing, Intelligent Room Allocation & Comprehensive Activity Monitoring System</p>
</div>
""", unsafe_allow_html=True)

# File Upload Section
st.markdown("""
<div class="file-upload-section">
    <div class="file-upload-icon">📁</div>
    <div class="file-upload-title">Upload Files</div>
    <div class="file-upload-subtitle">
        Support for CSV, Excel, PDF, Text files and more. Upload student data, documents, or configuration files.
    </div>
</div>
""", unsafe_allow_html=True)

# File Upload Widget
uploaded_files = st.file_uploader(
    "Choose files to upload",
    accept_multiple_files=True,
    type=['csv', 'xlsx', 'xls', 'pdf', 'txt', 'json', 'xml'],
    help="Upload multiple files at once. Supported formats: CSV, Excel, PDF, Text, JSON, XML"
)

# Process uploaded files
if uploaded_files:
    processor = FileProcessor()
    
    for uploaded_file in uploaded_files:
        file_type = processor.get_file_type(uploaded_file.name)
        file_size = uploaded_file.size
        file_icon = processor.get_file_icon(file_type)
        
        # Create file info display
        st.markdown(f"""
        <div class="file-info-card">
            <div class="file-info-header">
                <span style="font-size: 1.5rem;">{file_icon}</span>
                <span class="file-info-name">{uploaded_file.name}</span>
                <span class="file-type-badge file-type-{file_type}">{file_type.upper()}</span>
            </div>
            <div class="file-info-details">
                Size: {processor.format_file_size(file_size)} • 
                Type: {uploaded_file.type} • 
                Uploaded: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Process file based on type
        try:
            if file_type == 'csv':
                result = processor.process_csv(uploaded_file)
                if 'error' not in result:
                    st.success(f"✅ CSV processed: {result['rows']} rows, {result['columns']} columns")
                    with st.expander("View CSV Preview"):
                        st.write("**Columns:**", ", ".join(result['column_names']))
                        st.dataframe(pd.DataFrame(result['preview']))
                else:
                    st.error(f"❌ Error processing CSV: {result['error']}")
                    
            elif file_type in ['xlsx', 'xls']:
                result = processor.process_excel(uploaded_file)
                if 'error' not in result:
                    st.success(f"✅ Excel processed: {result['rows']} rows, {result['columns']} columns")
                    with st.expander("View Excel Preview"):
                        st.write("**Columns:**", ", ".join(result['column_names']))
                        st.dataframe(pd.DataFrame(result['preview']))
                else:
                    st.error(f"❌ Error processing Excel: {result['error']}")
                    
            elif file_type == 'pdf':
                result = processor.process_pdf(uploaded_file)
                if 'error' not in result:
                    st.success(f"✅ PDF processed: {result['pages']} pages")
                    with st.expander("View PDF Preview"):
                        st.text_area("First Page Preview", result['text_preview'], height=150)
                else:
                    st.error(f"❌ Error processing PDF: {result['error']}")
                    
            elif file_type == 'txt':
                result = processor.process_text(uploaded_file)
                if 'error' not in result:
                    st.success(f"✅ Text file processed: {result['lines']} lines, {result['characters']} characters")
                    with st.expander("View Text Preview"):
                        st.text_area("Content Preview", result['preview'], height=150)
                else:
                    st.error(f"❌ Error processing text file: {result['error']}")
                    
            else:
                result = {'info': 'File uploaded successfully but no specific processing available for this type'}
                st.info(f"ℹ️ {uploaded_file.name} uploaded successfully")
            
            # Log the file upload
            logging_system.log_file_upload(uploaded_file.name, file_type, file_size, result)
            
        except Exception as e:
            st.error(f"❌ Error processing {uploaded_file.name}: {str(e)}")
            logging_system.log_file_upload(uploaded_file.name, file_type, file_size, {'error': str(e)})

# Room Allocation Section
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">🏠 Smart Room Allocation System</div>', unsafe_allow_html=True)

allocator = st.session_state.room_allocator

# Check if we have suitable student data
student_data_available = False
suitable_files = []

for file_info in logging_system.uploaded_files:
    if (file_info['file_type'] in ['csv', 'xlsx', 'xls'] and 
        'error' not in file_info['processing_result'] and
        'data' in file_info['processing_result']):
        suitable_files.append(file_info)

if suitable_files:
    st.markdown("""
    <div class="info-alert">
        📊 Student data files detected. You can now proceed with room allocation.
    </div>
    """, unsafe_allow_html=True)
    
    # File selection for allocation
    file_options = [f"{file['filename']} ({file['processing_result']['rows']} rows)" for file in suitable_files]
    selected_file_index = st.selectbox(
        "Select student data file for allocation:",
        options=range(len(file_options)),
        format_func=lambda x: file_options[x],
        help="Choose the file containing student information"
    )
    
    selected_file = suitable_files[selected_file_index]
    
    # Allocation parameters
    col_param1, col_param2, col_param3 = st.columns(3)
    
    with col_param1:
        max_per_room = st.number_input(
            "Max Students per Room",
            min_value=1,
            max_value=4,
            value=2,
            help="Maximum number of students per room"
        )
    
    with col_param2:
        total_rooms = st.number_input(
            "Total Available Rooms",
            min_value=1,
            max_value=200,
            value=50,
            help="Total number of rooms available"
        )
    
    with col_param3:
        allocation_method = st.selectbox(
            "Allocation Method",
            options=["Compatibility-based", "Random", "Course-based"],
            help="Method for allocating students to rooms"
        )
    
    # Allocation button
    if st.button("🚀 Start Room Allocation", type="primary"):
        try:
            # Load the selected file data
            student_df = selected_file['processing_result']['data']
            
            # Load data into allocator
            allocator.load_student_data(student_df)
            
            # Perform allocation
            with st.spinner("Allocating rooms... This may take a moment."):
                results = allocator.allocate_rooms(
                    max_students_per_room=max_per_room,
                    total_rooms=total_rooms
                )
            
            # Log the allocation
            summary = allocator.get_allocation_summary()
            logging_system.log_action(
                'SUCCESS', 'ALLOCATION', 'Room Allocation Completed',
                f"Allocated {summary['total_students']} students to {summary['total_rooms']} rooms",
                metadata=summary
            )
            
            st.success(f"✅ Allocation completed! {summary['total_students']} students allocated to {summary['total_rooms']} rooms.")
            
        except Exception as e:
            logging_system.log_action('ERROR', 'ALLOCATION', 'Allocation Failed', str(e))
            st.error(f"❌ Allocation failed: {str(e)}")

else:
    st.markdown("""
    <div class="warning-alert">
        ⚠️ No suitable student data files found. Please upload a CSV or Excel file with student information including columns like: student_id, name, gender, course, year.
    </div>
    """, unsafe_allow_html=True)
    
    # Sample data generation for demo
    if st.button("🎯 Generate Sample Data for Demo"):
        sample_students = pd.DataFrame({
            'student_id': [f'STU{i:03d}' for i in range(1, 61)],
            'name': [f'Student {i}' for i in range(1, 61)],
            'gender': ['Male', 'Female'] * 30,
            'course': ['CS', 'EE', 'ME', 'CE'] * 15,
            'year': [1, 2, 3, 4] * 15,
            'sleep_time': ['early', 'late', 'medium'] * 20,
            'study_hours': ['low', 'medium', 'high'] * 20,
            'social_level': ['introvert', 'extrovert', 'ambivert'] * 20,
            'cleanliness': ['high', 'medium', 'low'] * 20
        })
        
        # Store as if it was uploaded
        result = {
            'rows': len(sample_students),
            'columns': len(sample_students.columns),
            'column_names': list(sample_students.columns),
            'preview': sample_students.head().to_dict('records'),
            'data': sample_students
        }
        
        logging_system.log_file_upload('sample_students.csv', 'csv', 1024, result)
        st.success("✅ Sample data generated! You can now run room allocation.")
        st.rerun()

# Display allocation results
if allocator.allocation_results:
    st.markdown("### 📋 Allocation Results")
    
    # Summary statistics
    summary = allocator.get_allocation_summary()
    
    col_sum1, col_sum2, col_sum3, col_sum4 = st.columns(4)
    
    with col_sum1:
        st.metric("Total Students", summary['total_students'])
    with col_sum2:
        st.metric("Total Rooms", summary['total_rooms'])
    with col_sum3:
        st.metric("Avg Occupancy", f"{summary['average_occupancy']}%")
    with col_sum4:
        st.metric("Unallocated", summary['unallocated_students'])
    
    # Room details in expandable cards
    st.markdown("### 🏠 Room Details")
    
    # Show first 10 rooms in detail
    for room in allocator.allocation_results[:10]:
        with st.expander(f"Room {room['room_number']} - {len(room['students'])}/{room['capacity']} students"):
            room_df = pd.DataFrame(room['students'])
            st.dataframe(room_df, use_container_width=True)
    
    if len(allocator.allocation_results) > 10:
        st.info(f"Showing first 10 rooms. Total rooms: {len(allocator.allocation_results)}")
    
    # Full allocation table
    room_data = []
    for room in allocator.allocation_results:
        for i, student in enumerate(room['students']):
            room_data.append({
                'Room': room['room_number'],
                'Student ID': student['student_id'],
                'Name': student['name'],
                'Gender': student['gender'],
                'Course': student.get('course', 'N/A'),
                'Year': student.get('year', 'N/A'),
                'Occupancy': f"{len(room['students'])}/{room['capacity']}"
            })
    
    results_df = pd.DataFrame(room_data)
    
    # Export results
    col_export1, col_export2 = st.columns(2)
    
    with col_export1:
        if st.button("💾 Export Allocation Results"):
            csv = results_df.to_csv(index=False)
            st.download_button(
                label="Download Results CSV",
                data=csv,
                file_name=f"sshm_room_allocation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            logging_system.log_action('SUCCESS', 'EXPORT', 'Results Exported', 
                                    'Room allocation results exported successfully')
    
    with col_export2:
        if st.button("🔄 Clear Allocation"):
            st.session_state.room_allocator = RoomAllocator()
            st.success("Allocation cleared!")
            st.rerun()

st.markdown('</div>', unsafe_allow_html=True)

# Get log statistics
stats = logging_system.get_log_stats()

# Statistics Cards
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="stat-card blue">
        <div class="stat-header">
            <div class="stat-icon">📊</div>
        </div>
        <div class="stat-number">{stats['total']}</div>
        <div class="stat-label">Total Events</div>
        <div class="stat-sublabel">All logged activities</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="stat-card green">
        <div class="stat-header">
            <div class="stat-icon">✅</div>
        </div>
        <div class="stat-number">{stats['success']}</div>
        <div class="stat-label">Successful</div>
        <div class="stat-sublabel">Completed actions</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="stat-card red">
        <div class="stat-header">
            <div class="stat-icon">❌</div>
        </div>
        <div class="stat-number">{stats['errors']}</div>
        <div class="stat-label">Errors</div>
        <div class="stat-sublabel">Failed operations</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="stat-card yellow">
        <div class="stat-header">
            <div class="stat-icon">⚠️</div>
        </div>
        <div class="stat-number">{stats['warnings']}</div>
        <div class="stat-label">Warnings</div>
        <div class="stat-sublabel">Attention needed</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="stat-card blue">
        <div class="stat-header">
            <div class="stat-icon">📁</div>
        </div>
        <div class="stat-number">{stats['files_uploaded']}</div>
        <div class="stat-label">Files Uploaded</div>
        <div class="stat-sublabel">Total files processed</div>
    </div>
    """, unsafe_allow_html=True)

# Sidebar Configuration
with st.sidebar:
    st.markdown("""
    <div class="filter-container">
        <div class="filter-title">🔧 SSHM Log Controls</div>
    """, unsafe_allow_html=True)
    
    log_level = st.selectbox(
        'Filter by Level',
        options=['All', 'SUCCESS', 'INFO', 'WARNING', 'ERROR'],
        index=0
    )
    
    time_range = st.selectbox(
        'Time Range',
        options=['Last Hour', 'Last 24 Hours', 'Last Week', 'All Time'],
        index=1
    )
    
    if st.button('🔄 Refresh Logs'):
        st.rerun()
    
    if st.button('🧹 Clear Logs'):
        logging_system.session_logs = []
        st.success("Logs cleared!")
        st.rerun()
        
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Quick Actions
    st.markdown("""
    <div class="filter-container">
        <div class="filter-title">⚡ Quick Actions</div>
    """, unsafe_allow_html=True)
    
    if st.button('📁 Test File Upload'):
        logging_system.log_action('INFO', 'UPLOAD', 'Test File Uploaded', 
                                'test_students.csv uploaded for testing')
        st.success("Upload logged!")
    
    if st.button('🏠 Test Allocation'):
        logging_system.log_action('SUCCESS', 'ALLOCATION', 'Test Allocation', 
                                'Test allocation completed successfully')
        st.success("Allocation logged!")
    
    if st.button('⚠️ Test Warning'):
        logging_system.log_action('WARNING', 'SYSTEM', 'Test Warning', 
                                'This is a test warning message')
        st.warning("Warning logged!")
    
    if st.button('❌ Test Error'):
        logging_system.log_action('ERROR', 'SYSTEM', 'Test Error', 
                                'This is a test error message')
        st.error("Error logged!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# File Management Section
if logging_system.uploaded_files:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">📂 Uploaded Files Management</div>', unsafe_allow_html=True)
    
    processor = FileProcessor()
    
    # Display uploaded files in a nice format
    for i, file_info in enumerate(reversed(logging_system.uploaded_files[-10:])):  # Show last 10 files
        file_icon = processor.get_file_icon(file_info['file_type'])
        
        col_file1, col_file2, col_file3 = st.columns([2, 1, 1])
        
        with col_file1:
            st.markdown(f"""
            <div style="display: flex; align-items: center; gap: 0.75rem; padding: 0.75rem; 
                       background: #f8fafc; border-radius: 8px; margin-bottom: 0.5rem;">
                <span style="font-size: 1.5rem;">{file_icon}</span>
                <div>
                    <div style="font-weight: 600; color: #1f2937;">{file_info['filename']}</div>
                    <div style="font-size: 0.85rem; color: #6b7280;">
                        Uploaded: {file_info['upload_time']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_file2:
            st.markdown(f"""
            <div style="text-align: center; padding: 0.75rem;">
                <span class="file-type-badge file-type-{file_info['file_type']}">{file_info['file_type'].upper()}</span>
                <br><small style="color: #6b7280;">{processor.format_file_size(file_info['size'])}</small>
            </div>
            """, unsafe_allow_html=True)
        
        with col_file3:
            if 'error' in file_info['processing_result']:
                st.markdown('<div style="text-align: center; color: #ef4444;">❌ Error</div>', unsafe_allow_html=True)
            else:
                st.markdown('<div style="text-align: center; color: #10b981;">✅ Processed</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main Content Area
col1, col2 = st.columns([2, 1])

with col1:
    # Recent Logs Section
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">🕒 Recent Activity Logs</div>', unsafe_allow_html=True)
    
    # Filter logs
    filtered_logs = logging_system.get_logs()
    if log_level != 'All':
        filtered_logs = [log for log in filtered_logs if log['level'] == log_level]
    
    # Display logs
    if filtered_logs:
        for log in reversed(filtered_logs[-20:]):  # Show last 20 logs
            level_class = log['level'].lower()
            if level_class not in ['info', 'success', 'warning', 'error']:
                level_class = 'info'
            details_html = log.get('details', '')
            meta = log.get('metadata', {})
            meta_html = ""
            if meta:
                try:
                    meta_html = "<pre style='background:#f8fafc;padding:8px;border-radius:6px;'>"+json.dumps(meta, indent=2)+"</pre>"
                except Exception:
                    meta_html = ""
            st.markdown(f"""
            <div class="log-entry {level_class}">
                <div class="log-header">
                    <span class="log-level {level_class}">{log['level']}</span>
                    <span class="log-timestamp">{log['timestamp']}</span>
                </div>
                <div class="log-message">{log['action']}</div>
                <div class="log-details">
                    <strong>Category:</strong> {log['category']} | 
                    <strong>User:</strong> {log['user']}<br>
                    <strong>Details:</strong> {details_html}
                </div>
                {meta_html}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown('<div class="info-alert">ℹ️ No logs found for selected filters</div>', 
                   unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Log Level Distribution Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('### 📈 Log Distribution')
    
    if filtered_logs:
        log_df = pd.DataFrame(filtered_logs)
        level_counts = log_df['level'].value_counts()
        
        fig = px.pie(values=level_counts.values, names=level_counts.index,
                    color_discrete_map={
                        'SUCCESS': '#10b981',
                        'INFO': '#3b82f6', 
                        'WARNING': '#f59e0b',
                        'ERROR': '#ef4444'
                    })
        fig.update_layout(height=300, showlegend=True, 
                         font=dict(family="Inter", size=12))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data for chart")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Recent Categories
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('### 📂 Activity Categories')
    
    if filtered_logs:
        category_counts = log_df['category'].value_counts()
        for cat, count in category_counts.items():
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; 
                       align-items: center; padding: 0.5rem; 
                       background: #f8fafc; border-radius: 6px; margin-bottom: 0.5rem;">
                <span style="font-weight: 600;">{cat}</span>
                <span style="background: #3b82f6; color: white; 
                           padding: 0.25rem 0.75rem; border-radius: 20px; 
                           font-size: 0.8rem;">{count}</span>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Export Functionality
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">💾 Export & Download</div>', unsafe_allow_html=True)

col_exp1, col_exp2, col_exp3 = st.columns(3)

with col_exp1:
    if st.button('📥 Download Logs (CSV)'):
        if filtered_logs:
            export_df = pd.DataFrame(filtered_logs)
            csv = export_df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"sshm_logs_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            logging_system.log_action('SUCCESS', 'EXPORT', 'Logs Exported', 
                                    f'{len(filtered_logs)} logs exported to CSV')

with col_exp2:
    if st.button('📊 Download File Report'):
        if logging_system.uploaded_files:
            files_df = pd.DataFrame(logging_system.uploaded_files)
            csv = files_df.to_csv(index=False)
            st.download_button(
                label="Download File Report",
                data=csv,
                file_name=f"sshm_files_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )

with col_exp3:
    if st.button('🔍 View Raw Logs'):
        if st.checkbox("Show raw log data"):
            st.json(filtered_logs)

st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div style="text-align: center; padding: 2rem; color: #6b7280; font-size: 0.9rem;">
    <hr style="border: none; height: 1px; background: #e5e7eb; margin: 2rem 0;">
    🏨 <strong>Sajid's Smart Hostel Manager (SSHM) v4.0</strong> • Advanced File Processing, Intelligent Room Allocation & Real-time Activity Monitoring<br>
    <em>Built with Streamlit • Smart File Processing • AI-Powered Room Allocation • Comprehensive Activity Monitoring</em>
</div>
""", unsafe_allow_html=True)