"""
NyayaSutra Citizen Portal - Pure Clean Vernacular Web Interface.
Includes Satbara Sentinel Geo-Boundary AI & Live Voice Speech Assistant.
"""

import pandas as pd
import streamlit as st

from nyayasutra.bns_engine.concordance import BNSKnowledgeEngine
from nyayasutra.bns_engine.sentinel import SatbaraSentinelEngine
from nyayasutra.core.models import LanguageCode
from nyayasutra.drafting.templates import LegalDraftingEngine
from nyayasutra.voice.assistant import VoiceAssistantBridge

st.set_page_config(
    page_title="NyayaSutra (न्यायसूत्र)",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom High-Contrast Styling
st.markdown(
    """
<style>
    .main-header { font-size: 2.2rem; font-weight: 700; color: #1E3A8A; }
    .sub-header { font-size: 1.05rem; color: #4B5563; margin-bottom: 8px; }
    .law-card {
        background-color: #F8FAFC;
        border-left: 5px solid #2563EB;
        padding: 16px;
        margin-bottom: 14px;
        border-radius: 6px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .sentinel-box {
        background-color: #FEF2F2;
        border: 1px solid #F87171;
        padding: 18px;
        border-radius: 8px;
        margin-bottom: 15px;
    }
    .badge-bns {
        background-color: #DCFCE7;
        color: #166534;
        padding: 4px 10px;
        border-radius: 4px;
        font-weight: 600;
        font-size: 0.9rem;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Localization Dictionary (100% pure language per selection)
I18N = {
    LanguageCode.GUJARATI: {
        "lang_label": "ભાષા પસંદ કરો",
        "sub_title": "ગામડાં અને શહેરો માટે અવાજ-આધારિત કાનૂની સહાય અને BNS ૨૦૨૩ કાયદા માર્ગદર્શન",
        "tab1_title": "📄 દસ્તાવેજ અને FIR તપાસ",
        "tab2_title": "📝 જમીન દબાણ કાનૂની નોટિસ",
        "tab3_title": "🛰️ સાતબારા સેન્ટિનેલ (જમીન સુરક્ષા AI)",
        "tab4_title": "🔍 IPC થી BNS ૨૦૨૩ કાયદા કોશ",
        # Tab 1
        "tab1_header": "૧. દસ્તાવેજ અથવા FIR ની વિગત તપાસો",
        "tab1_input_label": "દસ્તાવેજની વિગત, કોર્ટ સમન્સ અથવા FIR નું લખાણ અહીં લખો:",
        "tab1_default_text": "આરોપી વિરુદ્ધ IPC 420 અને IPC 506 મુજબ જમીન છેતરપિંડી અને ધમકીની ફરિયાદ નોંધાઈ છે.",
        "tab1_btn": "કાયદાકીય કલમો તપાસો",
        "tab1_spinner": "BNS કાયદા સાથે મેળવી રહ્યું છે...",
        "tab1_success_prefix": "મળેલી કાયદાકીય જોગવાઈઓ:",
        "tab1_old_ipc": "જૂની IPC",
        "tab1_bns_sec": "BNS ૨૦૨૩ કલમ",
        "tab1_summary_label": "સરળ અર્થ",
        "tab1_voice_label": "વાણી સહાયક અવાજ પ્રતિસાદ:",
        "tab1_no_match": "કોઈ ગંભીર ફોજદારી કલમ મળી નથી. સામાન્ય મહેસૂલી અથવા દીવાની લખાણ હોઈ શકે છે.",
        # Tab 2
        "tab2_header": "૨. જમીન દબાણ અટકાવવા કાનૂની નોટિસ તૈયાર કરો",
        "app_name": "અરજદારનું પૂરું નામ:",
        "app_name_def": "રમેશભાઈ ગોવિંદભાઈ પટેલ",
        "app_addr": "અરજદારનું સરનામું:",
        "app_addr_def": "ગામ: સાણંદ, જિલ્લો: અમદાવાદ",
        "app_phone": "સંપર્ક નંબર:",
        "app_phone_def": "+91 9876543210",
        "survey_no": "જમીન ખાતા / સર્વે નંબર:",
        "survey_no_def": "સર્વે નં. 402/1, ખાતા નં. 128",
        "opp_name": "સામેવાળા (દબાણકર્તા) નું નામ:",
        "opp_name_def": "સુરેશભાઈ કુમાર",
        "opp_addr": "સામેવાળાનું સરનામું:",
        "opp_addr_def": "ગામ: સાણંદ, જિલ્લો: અમદાવાદ",
        "inc_date": "દબાણ અથવા છેડછાડની તારીખ:",
        "inc_date_def": "10-11-2026",
        "district": "તાલુકો અને જિલ્લો:",
        "district_def": "સાણંદ, અમદાવાદ",
        "tab2_btn": "કાનૂની નોટિસ તૈયાર કરો",
        "tab2_result_label": "તૈયાર થયેલ ઔપચારિક કાનૂની નોટિસ:",
        "tab2_download_btn": "📥 નોટિસ ડાઉનલોડ કરો (.txt)",
        # Tab 3 (Sentinel)
        "tab3_header": "૩. સાતબારા સેન્ટિનેલ — જમીન સરહદ સુરક્ષા અને છેતરપિંડી તપાસ AI",
        "sentinel_sub": "કોઈપણ સર્વે નંબર નાખીને જમીન પર ગેરકાયદેસર ફેરફાર, સરહદી દબાણ કે બોજાની વિગત ચકાસો:",
        "sentinel_village": "ગામ:",
        "sentinel_taluka": "તાલુકો:",
        "sentinel_survey": "સર્વે નંબર:",
        "sentinel_btn": "🛡️ સેટેલાઇટ જમીન જોખમ ચકાસો (Inspect Land Security)",
        # Tab 4
        "tab4_header": "૪. કાયદા કોશ (IPC થી નવી BNS ૨૦૨૩ કલમ શોધો)",
        "tab4_search_label": "કોઈપણ IPC અથવા BNS કલમ લખો (દા.ત. 420, 302, 354, 506):",
        "tab4_offense": "ગુનો:",
        "tab4_bailable": "જામીનપાત્ર:",
        "tab4_cognizable": "પોલીસ સીધી ધરપકડ કરી શકે (Cognizable):",
        "yes": "હા",
        "no": "ના (બિનજામીનપાત્ર)",
        "tab4_not_found": "આ કલમ હજુ પ્રારંભિક રજિસ્ટ્રીમાં દાખલ થઈ રહી છે.",
    },
    LanguageCode.HINDI: {
        "lang_label": "भाषा चुनें",
        "sub_title": "नागरिकों और किसानों के लिए आवाज-आधारित कानूनी सहायता एवं बी.एन.एस. २०२३ कानून मार्गदर्शिका",
        "tab1_title": "📄 दस्तावेज़ और FIR जांच",
        "tab2_title": "📝 भूमि विवाद कानूनी नोटिस",
        "tab3_title": "🛰️ सातबारा सेंटिनल (भूमि सुरक्षा AI)",
        "tab4_title": "🔍 IPC से BNS २०२३ कानून शब्दकोश",
        # Tab 1
        "tab1_header": "१. दस्तावेज़ या FIR का विवरण जांचें",
        "tab1_input_label": "दस्तावेज़ का अंश, कोर्ट समन या FIR का विवरण यहाँ दर्ज करें:",
        "tab1_default_text": "आरोपी के खिलाफ IPC 420 और IPC 506 के तहत जमीन कब्जा और धोखाधड़ी का मामला दर्ज किया गया है।",
        "tab1_btn": "कानूनी धाराएं जांचें",
        "tab1_spinner": "BNS कानूनों के साथ मिलान किया जा रहा है...",
        "tab1_success_prefix": "पाई गई कानूनी धाराएं:",
        "tab1_old_ipc": "पुरानी IPC",
        "tab1_bns_sec": "BNS २०२३ धारा",
        "tab1_summary_label": "सरल अर्थ",
        "tab1_voice_label": "वॉइस असिस्टेंट उत्तर:",
        "tab1_no_match": "कोई गंभीर आपराधिक धारा नहीं मिली। यह सामान्य राजस्व या दीवानी मामला हो सकता है।",
        # Tab 2
        "tab2_header": "२. अवैध भूमि कब्जा रोकने हेतु औपचारिक कानूनी नोटिस तैयार करें",
        "app_name": "आवेदक का पूरा नाम:",
        "app_name_def": "रमेशभाई गोविंदभाई पटेल",
        "app_addr": "आवेदक का पता:",
        "app_addr_def": "ग्राम: सानंद, जिला: अहमदाबाद",
        "app_phone": "संपर्क नंबर:",
        "app_phone_def": "+91 9876543210",
        "survey_no": "जमीन खाता / खसरा नंबर:",
        "survey_no_def": "सर्वे नं. 402/1, खाता नं. 128",
        "opp_name": "विपक्षी (अवैध कब्जाकर्ता) का नाम:",
        "opp_name_def": "सुरेश कुमार",
        "opp_addr": "विपक्षी का पता:",
        "opp_addr_def": "ग्राम: सानंद, जिला: अहमदाबाद",
        "inc_date": "अवैध कब्जे के प्रयास की तिथि:",
        "inc_date_def": "10-11-2026",
        "district": "तहसील और जिला:",
        "district_def": "सानंद, अहमदाबाद",
        "tab2_btn": "कानूनी नोटिस तैयार करें",
        "tab2_result_label": "तैयार औपचारिक कानूनी नोटिस:",
        "tab2_download_btn": "📥 नोटिस डाउनलोड करें (.txt)",
        # Tab 3 (Sentinel)
        "tab3_header": "३. सातबारा सेंटिनल — उपग्रह भूमि सीमा सुरक्षा एवं धोखाधड़ी निवारक AI",
        "sentinel_sub": "खसरा / सर्वे नंबर दर्ज करके अवैध दाखिल-खारिज और सीमा अतिक्रमण की जांच करें:",
        "sentinel_village": "ग्राम / मौजा:",
        "sentinel_taluka": "तहसील / ब्लॉक:",
        "sentinel_survey": "खसरा / सर्वे नंबर:",
        "sentinel_btn": "🛡️ सैटेलाइट भूमि सुरक्षा जांचें (Inspect Land Security)",
        # Tab 4
        "tab3_header_dict": "४. कानून शब्दकोश (IPC से नई BNS २०२३ धारा खोजें)",
        "tab4_search_label": "कोई भी IPC या BNS धारा दर्ज करें (उदा. 420, 302, 354, 506):",
        "tab4_offense": "अपराध:",
        "tab4_bailable": "जमानती:",
        "tab4_cognizable": "पुलिस बिना वारंट गिरफ्तार कर सकती है (Cognizable):",
        "yes": "हाँ",
        "no": "नहीं (गैर-जमानती)",
        "tab4_not_found": "यह धारा अभी रजिस्ट्री में जोड़ी जा रही है।",
    },
    LanguageCode.ENGLISH: {
        "lang_label": "Select Language",
        "sub_title": "Voice-First Vernacular Legal Intelligence & BNS 2023 Guidance for Bharat",
        "tab1_title": "📄 Document & FIR Scanner",
        "tab2_title": "📝 Land Encroachment Notice",
        "tab3_title": "🛰️ Satbara Sentinel (Land Risk AI)",
        "tab4_title": "🔍 IPC to BNS 2023 Concordance",
        # Tab 1
        "tab1_header": "1. Analyze Legal Document or FIR Excerpt",
        "tab1_input_label": "Enter text excerpt, court summons, or FIR description here:",
        "tab1_default_text": "FIR filed alleging offenses under Section 420 (Cheating) and Section 506 (Criminal Intimidation).",
        "tab1_btn": "Analyze Legal Provisions",
        "tab1_spinner": "Scanning BNS Knowledge Graph...",
        "tab1_success_prefix": "Detected Legal Provisions:",
        "tab1_old_ipc": "Old IPC",
        "tab1_bns_sec": "BNS 2023 Section",
        "tab1_summary_label": "Plain Summary",
        "tab1_voice_label": "Voice Assistant Prompt:",
        "tab1_no_match": "No severe penal sections detected. Likely standard civil or regulatory text.",
        # Tab 2
        "tab2_header": "2. Generate Formal Land Encroachment Cessation Notice",
        "app_name": "Applicant Full Name:",
        "app_name_def": "Rameshbhai Govindbhai Patel",
        "app_addr": "Applicant Address:",
        "app_addr_def": "Village: Sanand, Dist: Ahmedabad",
        "app_phone": "Contact Phone Number:",
        "app_phone_def": "+91 9876543210",
        "survey_no": "Land Survey / Khata No:",
        "survey_no_def": "Survey No. 402/1, Khata No. 128",
        "opp_name": "Opponent / Encroacher Name:",
        "opp_name_def": "Suresh Kumar",
        "opp_addr": "Opponent Address:",
        "opp_addr_def": "Village: Sanand, Dist: Ahmedabad",
        "inc_date": "Incident Date of Encroachment:",
        "inc_date_def": "10-11-2026",
        "district": "Taluka & District:",
        "district_def": "Sanand, Ahmedabad",
        "tab2_btn": "Generate Legal Notice Draft",
        "tab2_result_label": "Generated Formal Legal Notice:",
        "tab2_download_btn": "📥 Download Notice (.txt)",
        # Tab 3 (Sentinel)
        "tab3_header": "3. Satbara Sentinel — Geo-Boundary AI & Title Fraud Detection",
        "sentinel_sub": "Enter any land survey number to inspect mutation integrity, boundary overlap, and civil dispute risks:",
        "sentinel_village": "Village:",
        "sentinel_taluka": "Taluka / Block:",
        "sentinel_survey": "Survey / Khasra No:",
        "sentinel_btn": "🛡️ Inspect Satellite Land Security",
        # Tab 4
        "tab4_header": "4. Law Concordance Dictionary (Search IPC or BNS 2023)",
        "tab4_search_label": "Enter any IPC or BNS section (e.g. 420, 302, 354, 506):",
        "tab4_offense": "Offense:",
        "tab4_bailable": "Bailable:",
        "tab4_cognizable": "Cognizable (Arrest without warrant):",
        "yes": "Yes",
        "no": "No (Non-Bailable)",
        "tab4_not_found": "This section is currently being indexed in the concordance registry.",
    },
}

# Initialize engines
bns_engine = BNSKnowledgeEngine()
drafting_engine = LegalDraftingEngine()
voice_bridge = VoiceAssistantBridge()
sentinel_engine = SatbaraSentinelEngine()

# Header Section
col1, col2 = st.columns([3, 1])

with col2:
    selected_lang = st.selectbox(
        "🌐 Language / ભાષા / भाषा",
        options=[LanguageCode.GUJARATI, LanguageCode.HINDI, LanguageCode.ENGLISH],
        format_func=lambda x: (
            "ગુજરાતી (Gujarati)"
            if x == LanguageCode.GUJARATI
            else ("हिन्दी (Hindi)" if x == LanguageCode.HINDI else "English")
        ),
    )

t = I18N[selected_lang]

with col1:
    st.markdown(
        '<div class="main-header">⚖️ NyayaSutra (न्यायसूत्र)</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div class="sub-header">{t["sub_title"]}</div>',
        unsafe_allow_html=True,
    )

st.divider()

# Navigation Tabs
tab1, tab2, tab3, tab4 = st.tabs(
    [t["tab1_title"], t["tab2_title"], t["tab3_title"], t["tab4_title"]]
)

with tab1:
    st.subheader(t["tab1_header"])

    # Optional Voice Simulation Input
    c_voice1, c_voice2 = st.columns([3, 1])
    with c_voice1:
        doc_input = st.text_area(t["tab1_input_label"], value=t["tab1_default_text"], height=120)
    with c_voice2:
        st.write("🎙️ **અવાજ / બોલીને પૂછો (Voice Assistant)**")
        if st.button("🎤 બોલો (Simulate Voice Input)"):
            st.success("Audio Stream Detected! Auto-transcribed excerpt.")

    if st.button(t["tab1_btn"], type="primary"):
        with st.spinner(t["tab1_spinner"]):
            matched = bns_engine.scan_text_for_laws(doc_input)

            if matched:
                st.success(f"{t['tab1_success_prefix']} {len(matched)}")

                lang_code = selected_lang.value
                for m in matched:
                    summary = m.simplified_summary.get(lang_code) or m.simplified_summary.get(
                        "en", ""
                    )
                    st.markdown(
                        f"""
                    <div class="law-card">
                        <span class="badge-bns">{t["tab1_bns_sec"]}: {m.bns_section}</span>
                        &nbsp;&nbsp;<b>({t["tab1_old_ipc"]}: {m.ipc_section})</b> - <i>{m.offense_name}</i>
                        <p style="margin-top: 8px; margin-bottom: 0;"><b>{t["tab1_summary_label"]}:</b> {summary}</p>
                    </div>
                    """,
                        unsafe_allow_html=True,
                    )

                voice_prompt = voice_bridge.synthesize_response_prompt(
                    selected_lang, f"{len(matched)} legal provisions detected."
                )
                st.info(f"🎙️ **{t['tab1_voice_label']}** {voice_prompt}")
            else:
                st.warning(t["tab1_no_match"])

with tab2:
    st.subheader(t["tab2_header"])

    with st.form("notice_form"):
        c1, c2 = st.columns(2)
        with c1:
            app_name = st.text_input(t["app_name"], value=t["app_name_def"])
            app_address = st.text_input(t["app_addr"], value=t["app_addr_def"])
            app_contact = st.text_input(t["app_phone"], value=t["app_phone_def"])
            survey_no = st.text_input(t["survey_no"], value=t["survey_no_def"])
        with c2:
            enc_name = st.text_input(t["opp_name"], value=t["opp_name_def"])
            enc_address = st.text_input(t["opp_addr"], value=t["opp_addr_def"])
            inc_date = st.text_input(t["inc_date"], value=t["inc_date_def"])
            district = st.text_input(t["district"], value=t["district_def"])

        generate_btn = st.form_submit_button(t["tab2_btn"], type="primary")

    if generate_btn:
        notice_draft = drafting_engine.generate_land_encroachment_notice(
            applicant_name=app_name,
            applicant_address=app_address,
            applicant_contact=app_contact,
            encroacher_name=enc_name,
            encroacher_address=enc_address,
            land_survey_number=survey_no,
            village_district=district,
            incident_date=inc_date,
        )
        st.text_area(t["tab2_result_label"], value=notice_draft, height=260)
        st.download_button(
            label=t["tab2_download_btn"],
            data=notice_draft,
            file_name=f"Legal_Notice_{survey_no.replace('/', '_')}.txt",
            mime="text/plain",
        )

with tab3:
    st.subheader(t["tab3_header"])
    st.markdown(t["sentinel_sub"])

    sc1, sc2, sc3 = st.columns(3)
    with sc1:
        s_village = st.text_input(t["sentinel_village"], value="Sanand")
    with sc2:
        s_taluka = st.text_input(t["sentinel_taluka"], value="Sanand")
    with sc3:
        s_survey = st.text_input(t["sentinel_survey"], value="402/1")

    if st.button(t["sentinel_btn"], type="primary"):
        with st.spinner("Analyzing Geo-Spatial Land Registry and Satellite Perimeter..."):
            parcel = sentinel_engine.inspect_land_parcel(
                survey_number=s_survey, village=s_village, taluka=s_taluka
            )

            m_col1, m_col2, m_col3 = st.columns(3)
            with m_col1:
                st.metric(
                    label="Dispute Risk Score",
                    value=f"{parcel.dispute_risk_score} / 100",
                    delta=f"{parcel.risk_level}",
                )
            with m_col2:
                st.metric(
                    label="Total Registered Area",
                    value=f"{parcel.total_area_hectares} Hectares",
                )
            with m_col3:
                st.metric(label="Khata / Account No.", value=f"#{parcel.khata_number}")

            st.write(
                f"**નોંધાયેલ ખાતેદારો (Registered Title Holders):** {', '.join(parcel.recorded_owners)}"
            )

            # Spatial Map Visualization
            st.markdown("#### 🗺️ સેટેલાઇટ જમીન સીમા નકશો (Geo-Spatial Perimeter Map)")
            coords = parcel.boundary_coordinates
            df_map = pd.DataFrame(coords, columns=["lat", "lon"])
            st.map(df_map, zoom=14)

            # Encroachment Alerts
            st.markdown("#### ⚠️ સુરક્ષા ચેતવણીઓ (Sentinel Alerts & Civil Risk)")
            for a in parcel.encroachment_alerts:
                st.error(f"🚨 {a}")

with tab4:
    st.subheader(t.get("tab4_header", "૪. કાયદા કોશ"))
    query_sec = st.text_input(t["tab4_search_label"], value="420")
    if query_sec:
        match = bns_engine.find_by_ipc(query_sec) or bns_engine.find_by_bns(query_sec)
        if match:
            st.success(
                f"{t['tab1_bns_sec']}: {match.bns_section} | {t['tab1_old_ipc']}: {match.ipc_section}"
            )
            st.write(f"**{t['tab4_offense']}** {match.offense_name}")
            bailable_text = t["yes"] if match.bailable else t["no"]
            cognizable_text = t["yes"] if match.cognizable else t["no"]
            st.write(f"**{t['tab4_bailable']}** {bailable_text}")
            st.write(f"**{t['tab4_cognizable']}** {cognizable_text}")
            lang_code = selected_lang.value
            clean_summary = match.simplified_summary.get(lang_code) or match.simplified_summary.get(
                "en", ""
            )
            st.info(f"**{t['tab1_summary_label']}:** {clean_summary}")
        else:
            st.info(t["tab4_not_found"])
