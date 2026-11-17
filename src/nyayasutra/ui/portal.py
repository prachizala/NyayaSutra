"""
NyayaSutra Citizen Portal - High-Contrast Vernacular Web Interface.
Built with Streamlit for rural and semi-urban citizen accessibility.
"""

import streamlit as st

from nyayasutra.bns_engine.concordance import BNSKnowledgeEngine
from nyayasutra.core.models import LanguageCode
from nyayasutra.drafting.templates import LegalDraftingEngine
from nyayasutra.voice.assistant import VoiceAssistantBridge

st.set_page_config(
    page_title="NyayaSutra (न्यायसूत्र)",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for high contrast citizen accessibility
st.markdown("""
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; }
    .sub-header { font-size: 1.1rem; color: #4B5563; }
    .law-card {
        background-color: #F8FAFC;
        border-left: 5px solid #2563EB;
        padding: 15px;
        margin-bottom: 12px;
        border-radius: 4px;
    }
    .badge-bns {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 8px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.85rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize engines
bns_engine = BNSKnowledgeEngine()
drafting_engine = LegalDraftingEngine()
voice_bridge = VoiceAssistantBridge()

# Header
col1, col2 = st.columns([3, 1])
with col1:
    st.markdown('<div class="main-header">⚖️ NyayaSutra (न्यायसूत्र)</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Democratizing Citizen Legal Entitlements across Bharat via Vernacular Voice & BNS 2023 Intelligence</div>', unsafe_allow_html=True)

with col2:
    selected_lang = st.selectbox(
        "ભાષા પસંદ કરો / भाषा चुनें (Language)",
        options=[LanguageCode.GUJARATI, LanguageCode.HINDI, LanguageCode.ENGLISH],
        format_func=lambda x: "ગુજરાતી (Gujarati)" if x == LanguageCode.GUJARATI else ("हिन्दी (Hindi)" if x == LanguageCode.HINDI else "English")
    )

st.divider()

# Mode selection tabs
tab1, tab2, tab3 = st.tabs(["📄 Document & FIR Scanner", "📝 Land Dispute Notice Generator", "🔍 IPC ➔ BNS 2023 Concordance Lookup"])

with tab1:
    st.subheader("૧. દસ્તાવેજ / FIR તપાસો (Scan Document Excerpt)")
    
    sample_texts = {
        LanguageCode.GUJARATI: "આરોપી વિરુદ્ધ IPC 420 અને IPC 506 મુજબ જમીન છેતરપિંડી અને ધમકીની ફરિયાદ નોંધાઈ છે.",
        LanguageCode.HINDI: "आरोपी के खिलाफ IPC 420 और IPC 441 के तहत जमीन कब्जा और धोखाधड़ी का मामला दर्ज किया गया है।",
        LanguageCode.ENGLISH: "FIR filed alleging offenses under Section 420 (Cheating) and Section 329 BNS (Criminal Trespass)."
    }
    
    doc_input = st.text_area(
        "દસ્તાવેજની વિગત અથવા એફ.આઈ.આર. લખાણ અહીં લખો (Enter Legal Excerpt or FIR Text):",
        value=sample_texts.get(selected_lang, ""),
        height=120
    )
    
    if st.button("વિશ્લેષણ કરો (Analyze Law Provisions)", type="primary"):
        with st.spinner("BNS Knowledge Graph તપાસી રહ્યું છે..."):
            matched = bns_engine.scan_text_for_laws(doc_input)
            
            if matched:
                st.success(f"મળેલા કાયદાકીય કલમો (Detected Legal Provisions): {len(matched)}")
                
                lang_code = selected_lang.value
                for m in matched:
                    summary = m.simplified_summary.get(lang_code) or m.simplified_summary.get("en", "")
                    st.markdown(f"""
                    <div class="law-card">
                        <span class="badge-bns">BNS 2023 કલમ: {m.bns_section}</span>
                        &nbsp;&nbsp;<b>(જૂની IPC: {m.ipc_section})</b> - <i>{m.offense_name}</i>
                        <p style="margin-top: 8px; margin-bottom: 0;"><b>સરળ અર્થ:</b> {summary}</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Audio playback simulation prompt
                voice_prompt = voice_bridge.synthesize_response_prompt(selected_lang, f"{len(matched)} કાયદાકીય જોગવાઈઓ મળી છે.")
                st.info(f"🎙️ **વાણી સહાયક પ્રતિસાદ (Voice Synthesis Prompt):** {voice_prompt}")
            else:
                st.warning("કોઈ ફોજદારી કલમ મળી નથી. સામાન્ય મહેસૂલી અથવા દીવાની લખાણ હોઈ શકે છે.")

with tab2:
    st.subheader("૨. જમીન દબાણ અટકાવ નોટિસ ડ્રાફ્ટ (Land Encroachment Formal Notice)")
    
    with st.form("notice_form"):
        c1, c2 = st.columns(2)
        with c1:
            app_name = st.text_input("અરજદારનું પૂરું નામ (Applicant Full Name):", value="રમેશભાઈ ગોવિંદભાઈ પટેલ")
            app_address = st.text_input("સરનામું (Applicant Address):", value="ગામ: સાણંદ, જિલ્લો: અમદાવાદ")
            app_contact = st.text_input("સંપર્ક નંબર (Phone Number):", value="+91 9876543210")
            survey_no = st.text_input("જમીન ખાતા / સર્વે નંબર (Survey / Account No):", value="સર્વે નં. 402/1, ખાતા નં. 128")
        with c2:
            enc_name = st.text_input("સામેવાળાનું નામ (Opponent / Encroacher Name):", value="સુરેશભાઈ કુમાર")
            enc_address = st.text_input("સામેવાળાનું સરનામું (Opponent Address):", value="ગામ: સાણંદ, જિલ્લો: અમદાવાદ")
            inc_date = st.text_input("દબાણ પ્રયાસ તારીખ (Incident Date):", value="10-11-2026")
            district = st.text_input("તાલુકો / જિલ્લો (Taluka & District):", value="સાણંદ, અમદાવાદ")
            
        generate_btn = st.form_submit_button("નોટિસ તૈયાર કરો (Generate Legal Notice Draft)", type="primary")
        
    if generate_btn:
        notice_draft = drafting_engine.generate_land_encroachment_notice(
            applicant_name=app_name,
            applicant_address=app_address,
            applicant_contact=app_contact,
            encroacher_name=enc_name,
            encroacher_address=enc_address,
            land_survey_number=survey_no,
            village_district=district,
            incident_date=inc_date
        )
        st.text_area("તૈયાર થયેલ ઔપચારિક નોટિસ (Drafted Legal Notice):", value=notice_draft, height=260)
        st.download_button(
            label="📥 નોટિસ ડાઉનલોડ કરો (.txt / PDF ready)",
            data=notice_draft,
            file_name=f"Legal_Notice_{survey_no.replace('/', '_')}.txt",
            mime="text/plain"
        )

with tab3:
    st.subheader("૩. કાયદા કોશ (IPC ➔ BNS 2023 Fast Concordance)")
    query_sec = st.text_input("IPC કલમ અથવા BNS કલમ લખો (e.g. 420, 302, 506, 329):", value="420")
    if query_sec:
        match = bns_engine.find_by_ipc(query_sec) or bns_engine.find_by_bns(query_sec)
        if match:
            st.success(f"BNS 2023 કલમ: {match.bns_section} | IPC કલમ: {match.ipc_section}")
            st.write(f"**ગુનો:** {match.offense_name}")
            st.write(f"**જામીનપાત્ર (Bailable):** {'હા (Yes)' if match.bailable else 'ના - બિનજામીનપાત્ર (No - Non-bailable)'}")
            st.write(f"**પોલીસ અધિકાર (Cognizable):** {'હા (Yes)' if match.cognizable else 'ના (No)'}")
            st.json(match.simplified_summary)
        else:
            st.info("આ કલમ હજુ પ્રારંભિક રજિસ્ટ્રીમાં દાખલ થઈ રહી છે.")
