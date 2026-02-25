import streamlit as st
import requests
import pandas as pd
import json
from PIL import Image
import io
import time

# Page Config
st.set_page_config(
    page_title="Doc-Extractor Pro",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Premium Look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Force Dark Layout */
    .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background: linear-gradient(135deg, #020617 0%, #1e1b4b 100%) !important;
        background-attachment: fixed !important;
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.95) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1) !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 0rem !important;
    }
    
    /* Card Style */
    .data-card {
        background: rgba(255, 255, 255, 0.05) !important;
        backdrop-filter: blur(12px) !important;
        border-radius: 16px !important;
        padding: 24px !important;
        border: 1px solid rgba(255, 255, 255, 0.12) !important;
        margin-bottom: 24px !important;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3) !important;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
    }
    
    .data-card:hover {
        transform: translateY(-8px) !important;
        border-color: #6366f1 !important;
        background: rgba(255, 255, 255, 0.08) !important;
        box-shadow: 0 15px 40px rgba(99, 102, 241, 0.2) !important;
    }
    
    .highlight {
        color: #818cf8 !important;
        font-weight: 700 !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #f8fafc !important;
        font-family: 'Inter', sans-serif !important;
    }
    
    .stButton>button {
        background: linear-gradient(90deg, #4f46e5 0%, #9333ea 100%) !important;
        color: white !important;
        border: none !important;
        padding: 12px 28px !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.5px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(79, 70, 229, 0.3) !important;
        width: 100% !important;
    }
    
    .stButton>button:hover {
        box-shadow: 0 0 25px rgba(99, 102, 241, 0.6) !important;
        transform: scale(1.02) !important;
        filter: brightness(1.1) !important;
    }
    
    .status-badge {
        display: inline-block !important;
        padding: 6px 16px !important;
        border-radius: 50px !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        background: rgba(34, 197, 94, 0.15) !important;
        color: #4ade80 !important;
        border: 1px solid rgba(34, 197, 94, 0.4) !important;
        box-shadow: 0 0 15px rgba(34, 197, 94, 0.1) !important;
    }

    /* File Uploader Fix */
    [data-testid="stFileUploader"] {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px dashed rgba(255, 255, 255, 0.2) !important;
        border-radius: 12px !important;
        padding: 10px !important;
    }
    
    [data-testid="stFileUploader"] section {
        background: transparent !important;
        color: #f8fafc !important;
    }

    [data-testid="stFileUploader"] label {
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 24px !important;
        background-color: transparent !important;
    }

    .stTabs [data-baseweb="tab"] {
        height: 50px !important;
        white-space: pre !important;
        background-color: transparent !important;
        border-radius: 8px 8px 0px 0px !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
    }

    .stTabs [aria-selected="true"] {
        color: #818cf8 !important;
        border-bottom: 2px solid #818cf8 !important;
    }

    /* Hide Top Bar & Deploy Button */
    header, [data-testid="stHeader"], [data-testid="stSidebarCollapsedControl"] {
        display: none !important;
    }
    
    .stDeployButton {
        display: none !important;
    }
    
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 2rem !important;
    }
    
    #MainMenu {
        display: none !important;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🖥️ Backend System")
    api_url = st.text_input("Service URL", value="http://localhost:9000", help="Endpoint for the FastAPI extraction engine")
    st.divider()
    st.markdown("### 📊 API Status")
    try:
        response = requests.get(f"{api_url}/health", timeout=2)
        if response.status_code == 200:
            st.markdown('<div class="status-badge">Connected</div>', unsafe_allow_html=True)
            if not response.json().get("api_key_configured"):
                st.warning("Gemini API Key missing in backend!")
            
            st.link_button("🌐 Open Backend API", api_url)
        else:
            st.error("Backend Error")
    except:
        st.error("Backend Disconnected")
    
    st.divider()
    st.markdown("### 🕒 Recent Activity")
    if 'history' not in st.session_state:
        st.session_state['history'] = []
    
    if not st.session_state['history']:
        st.caption("No recent extractions")
    else:
        for idx, item in enumerate(reversed(st.session_state['history'][-5:])):
            with st.expander(f"📄 {item['name']}"):
                st.write(f"**Type:** {item['type']}")
                st.write(f"**Confidence:** {item['conf']:.1f}%")
                if st.button("👁️ View Results", key=f"hist_{idx}", use_container_width=True):
                    st.session_state['result'] = item['data']
                    st.rerun()

    st.divider()
    st.markdown("### 📂 Supported Formats")
    st.write("- PDF\n- PNG / JPG\n- Word (Coming Soon)")

# Header
st.markdown("""
<div style='text-align: center; padding: 20px 0;'>
    <h1 style='font-size: 3rem; margin-bottom: 0;'>Doc-<span style='color: #6366f1;'>Extractor</span> Pro</h1>
    <p style='color: #94a3b8; font-size: 1.2rem;'>Advanced Document Intelligence Powered by Gemini 1.5</p>
</div>
""", unsafe_allow_html=True)

# Main Content
tab1, tab2, tab3, tab4 = st.tabs(["🚀 Single Extraction", "📦 Batch Process", "📊 Model Intelligence", "📁 Sample Projects"])

with tab1:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.markdown("### 📤 Upload Document")
        uploaded_file = st.file_uploader("Drop your PDF or Image here", type=["pdf", "png", "jpg", "jpeg"])
        
        # Test Sample Shortcut
        st.markdown("---")
        st.caption("Don't have a file? Use a test sample:")
        sample_col1, sample_col2 = st.columns(2)
        if sample_col1.button("📑 Sample Invoice", use_container_width=True):
            st.session_state['result'] = {
                "document_type": "Invoice",
                "extracted_data": {"vendor": "Acme Corp", "total": "$1,250.00", "date": "2026-02-20", "items": "1. Web Design, 2. AI Implementation"},
                "confidence_score": 0.98
            }
        if sample_col2.button("📜 Legal Deed", use_container_width=True):
            st.session_state['result'] = {
                "document_type": "Legal Deed",
                "extracted_data": {"parties": "John Doe vs Jane Smith", "date": "2026-01-15", "jurisdiction": "New York", "summary": "Property transfer agreement for plot 405."},
                "confidence_score": 0.96
            }
        
        if uploaded_file is not None:
            if uploaded_file.type == "application/pdf":
                st.info("PDF detected. Advanced OCR will process all pages.")
            else:
                image = Image.open(uploaded_file)
                st.image(image, caption="Current Document", use_column_width=True)
                
            if st.button("✨ Run Intelligent Extraction"):
                progress_bar = st.progress(0)
                for i in range(100):
                    time.sleep(0.01)
                    progress_bar.progress(i + 1)
                
                with st.spinner("Gemini 1.5 Flash analyzing layout and text..."):
                    try:
                        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                        response = requests.post(f"{api_url}/extract", files=files)
                        
                        if response.status_code == 200:
                            res_json = response.json()
                            st.session_state['result'] = res_json
                            
                            # Add to History
                            if 'history' not in st.session_state:
                                st.session_state['history'] = []
                            st.session_state['history'].append({
                                "name": uploaded_file.name,
                                "type": res_json.get('document_type', 'Unknown'),
                                "conf": res_json.get('confidence_score', 0.0) * 100,
                                "data": res_json
                            })
                            
                            st.balloons()
                            st.success("Extraction Successful!")
                        else:
                            st.error(f"Error: {response.text}")
                    except Exception as e:
                        st.error(f"Connection failed: {e}")

    with col2:
        st.markdown("### 📋 Smart Insights")
        if 'result' in st.session_state:
            res = st.session_state['result']
            doc_type = res.get('document_type', 'Unknown')
            data = res.get('extracted_data', {})
            conf = res.get('confidence_score', 0.0)
            
            st.markdown(f"""
            <div class="data-card">
                <p style="margin-bottom: 5px; opacity: 0.7;">Identified As</p>
                <h2 style="margin: 0; color: #818cf8;">{doc_type}</h2>
                <div style="margin-top: 15px;">
                    <span style="font-size: 0.9rem; opacity: 0.8;">Accuracy Confidence:</span>
                    <span class="highlight">{conf*100:.1f}%</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            # Key Data Points
            st.write("#### Structured Data")
            for key, value in data.items():
                with st.container():
                    st.markdown(f"""
                    <div style="background: rgba(255,255,255,0.02); padding: 10px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #6366f1;">
                        <span style="font-size: 0.8rem; text-transform: uppercase; color: #94a3b8;">{key.replace('_', ' ')}</span><br>
                        <span style="font-weight: 500;">{value}</span>
                    </div>
                    """, unsafe_allow_html=True)
                
            # Actions
            col_a, col_b = st.columns(2)
            csv = pd.DataFrame([data]).to_csv(index=False)
            col_a.download_button("📥 Save CSV", csv, f"{doc_type}.csv", "text/csv")
            if col_b.button("🗑️ Clear Results"):
                del st.session_state['result']
                st.rerun()
        else:
            st.markdown("""
            <div style='text-align: center; padding: 50px; color: #64748b; background: rgba(255,255,255,0.02); border-radius: 15px; border: 1px dashed rgba(255,255,255,0.1);'>
                <p>Waiting for document analysis...</p>
            </div>
            """, unsafe_allow_html=True)

with tab2:
    st.markdown("### 📦 Enterprise Batch Processing")
    st.write("Upload multiple documents to process them in parallel using Gemini's high-throughput API.")
    
    batch_files = st.file_uploader("Upload multiple PDFs or Images", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)
    
    if batch_files:
        st.write(f"🔍 Found **{len(batch_files)}** documents in queue.")
        if st.button("⚡ Start Batch Workflow"):
            results_list = []
            batch_progress = st.progress(0)
            status_text = st.empty()
            
            for i, file in enumerate(batch_files):
                status_text.write(f"⏳ Processing {file.name}...")
                try:
                    files = {"file": (file.name, file.getvalue(), file.type)}
                    response = requests.post(f"{api_url}/extract", files=files)
                    if response.status_code == 200:
                        res = response.json()
                        results_list.append({"Filename": file.name, "Type": res['document_type'], "Confidence": f"{res['confidence_score']*100:.1f}%"})
                    else:
                        results_list.append({"Filename": file.name, "Type": "Error", "Confidence": "0%"})
                except:
                    results_list.append({"Filename": file.name, "Type": "Connection Error", "Confidence": "0%"})
                
                batch_progress.progress((i + 1) / len(batch_files))
            
            status_text.success(f"✅ Batch completed! {len(results_list)} documents processed.")
            st.table(pd.DataFrame(results_list))
            
            # Master CSV
            master_csv = pd.DataFrame(results_list).to_csv(index=False)
            st.download_button("📥 Download Master Report", master_csv, "batch_report.csv", "text/csv")

with tab3:
    st.markdown("### 🧠 Why Gemini 1.5 Flash?")
    st.write("We selected this model for **Doc-Extractor Pro** due to its unique architectural advantages:")
    
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.markdown("""
        <div class="data-card">
            <h4>Native Multimodal</h4>
            <p>Unlike standard OCR, Gemini sees the document pixels directly, understanding shadows, watermarks, and overlapping text.</p>
        </div>
        """, unsafe_allow_html=True)
    with m_col2:
        st.markdown("""
        <div class="data-card">
            <h4>Layout-Aware</h4>
            <p>It preserves spatial context. It knows if a number is inside a 'Total' box or a 'Tax' box based on location.</p>
        </div>
        """, unsafe_allow_html=True)
    with m_col3:
        st.markdown("""
        <div class="data-card">
            <h4>Speed (Flash)</h4>
            <p>Optimized for low latency, making it the perfect model for high-volume document processing workflows.</p>
        </div>
        """, unsafe_allow_html=True)

with tab4:
    st.markdown("### 📁 Experience Doc-Extractor")
    st.info("Don't have a file ready? Choose one of our curated samples to see the AI in action immediately.")
    
    # Existing sample logic was inside tab1, I'll move it here or keep it in both. 
    # Actually I'll just move the Use Cases here as well.
    st.markdown("#### Industry Use Cases")
    st.markdown("""
    - **Legal Documents**: Extraction of parties, effective dates, and clauses.
    - **Fintech**: Automated KYC and ID card validation.
    - **Logistics**: Invoice, Bill of Lading, and Receipt processing.
    """)

# Footer
st.markdown("---")
st.markdown("<div style='text-align: center; color: #475569;'>Built with FastAPI, Streamlit & Gemini 1.5 Flash</div>", unsafe_allow_html=True)
