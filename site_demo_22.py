import streamlit as st
import time
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- 1. Page Configuration & Initial State ---
st.set_page_config(
    page_title="Rodrigo Eslava | AI Demo",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# --- 2. Custom CSS for Styling (MODIFIED FOR DARK MODE) ---
st.markdown("""
<style>
    /* CSS Geral */
    .block-container { padding-top: 2rem; }
    .main-content-container { max-width: 1100px; margin: auto; }
    
    /* CSS dos Cards de Projeto (AGORA COMPATÍVEL COM DARK MODE) */
    .project-card { 
        background-color: var(--secondary-background-color); /* Usa a cor de fundo secundária do tema */
        border: 1px solid var(--gray-200);
        border-radius: 10px; 
        padding: 25px; 
        height: 100%; 
    }
    .project-card:hover { 
        border-color: var(--gray-400); 
        box-shadow: 0 8px 24px rgba(0,0,0,0.07); 
    }
    .project-title { 
        font-size: 1.5rem; 
        font-weight: 600; 
        color: var(--text-color); /* Usa a cor de texto principal do tema */
        margin-bottom: 1rem; 
    }
    .metric-number { font-size: 2.2rem; font-weight: bold; color: #00A98F; }
    h3 { 
        font-weight: 600; 
        color: var(--text-color); /* Usa a cor de texto principal do tema */
    }

    /* CSS dos Botões de Prompt (AGORA COMPATÍVEL COM DARK MODE) */
    .stButton>button { 
        background-color: var(--secondary-background-color); /* Fundo do botão acompanha o tema */
        border: 1px solid #00A98F; 
        color: #00A98F; 
        font-weight: bold; 
    }
    .stButton>button:hover { 
        border: 1px solid #007A68; 
        color: #007A68; 
    }

    /* CSS PARA OS CARDS DA SEÇÃO DE VISÃO (AGORA COMPATÍVEL COM DARK MODE) */
    .vision-card {
        background-color: var(--secondary-background-color);
        border: 1px solid var(--gray-200);
        border-radius: 10px;
        padding: 20px;
        height: 100%;
        text-align: center;
    }
    .vision-card h4 {
        font-weight: 600;
        color: var(--text-color);
        margin-top: 10px;
    }
    .vision-card p {
        color: var(--text-color);
    }
</style>
""", unsafe_allow_html=True)


# --- 3. ENHANCED RESPONSE FUNCTIONS ---

def display_pump_maintenance_response():
    st.markdown("**Consolidated Maintenance History for the Transfer Pump Unit**")
    st.caption("Data sources: IBM Maximo, SAP")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="response-card">
            <h5>Pump P-102 (Centrifugal)</h5>
            <ul>
                <li><b>07/15/2025:</b> Pump-motor realignment after vibration alert. <i>(Cost: $2,200.00)</i></li>
                <li><b>05/28/2025:</b> Mechanical seal replacement (preventive). <i>(Cost: $850.00)</i></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="response-card">
            <h5>Pump P-103 (Positive Displacement)</h5>
            <ul>
                <li><b>06/20/2025:</b> Bearing lubrication and operational check. <i>(Cost: $450.00)</i></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="response-card">
            <h5>Pump P-104 (Vacuum)</h5>
            <ul>
                <li><b>03/12/2025:</b> Major overhaul (bearing and shaft replacement). <i>(Cost: $8,200.00)</i></li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

def display_fermentation_response():
    st.markdown("**Optimization Parameters for Stem Cell Fermentation Process**")
    st.caption("Data sources: QMS, PI System")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="response-card"><b>1. pH</b><br>Affects enzymatic activity.<br><code>PI-FERM-F-301-PH</code></div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="response-card"><b>2. Temperature</b><br>Controls reaction kinetics.<br><code>PI-FERM-F-301-TEMP-PV</code></div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="response-card"><b>3. Dissolved Oxygen (DO)</b><br>Crucial for aerobic microorganisms.<br><code>PI-FERM-F-301-O2</code></div>', unsafe_allow_html=True)
            
    with st.expander("**Related Literature (source: QMS)**"):
        st.markdown("""
        * [Book] "Bioprocess Engineering Principles" by Pauline M. Doran
        * [DOI] https://doi.org/10.1016/C2009-0-22348-8
        * [Manual] `MAN-ENG-FERM-301-V02` - Fermentor F-301 Operation Manual
        """)

def display_salicylic_acid_response():
    st.markdown("**Consolidated Tag List for the Salicylic Acid Manufacturing Process (Synthesis Stage):**")
    data = {
        'Tag ID': ['PI-R101-TEMP-PV', 'PI-R101-PRESS-PV', 'PI-R101-ACID-FLOW', 'PI-P-103-RUN'],
        'Description': ['Reactor R-101 Temperature', 'Reactor R-101 Pressure', 'Sulfuric Acid Flow', 'Pump P-103 Status'],
        'Tag Type': ['Temperature', 'Pressure', 'Flow', 'Motor'],
        'Process Stage': ['Synthesis Reactor', 'Synthesis Reactor', 'Synthesis Reactor', 'Product Transfer']
    }
    df = pd.DataFrame(data)
    st.dataframe(df, hide_index=True, use_container_width=True)
    
    st.markdown("**Related Drawings (source: EDMS):**")
    st.markdown("* [P&ID-PROD-SA-REV04] - Piping and Instrumentation Diagram")
    
    st.markdown("""
    ---
    **Would you like to check the current status of any of these tags or view the alarm history for the Synthesis Reactor?**
    """)

# --- 4. Main Page Layout ---
with st.container():
    st.markdown('<div class="main-content-container">', unsafe_allow_html=True)
    
    # --- A. Hero Section ---
    st.title("Rodrigo Eslava")
    st.caption("Developed by Rodrigo Eslava")
    st.header("Beyond Dashboards: A Strategy to Address the Pain Points of Industrial Data")
    st.markdown("""
    Welcome,

    While dashboards are essential, they often only scratch the surface of what is possible with industrial data. The true challenge, and the 'hidden pain' for many operators and engineers, is bridging the gap between simply viewing data and scaling intelligence across an entire facility.

    Below, I've provided two practical examples of how I've used Seeq to turn industrial data into measurable impact, followed by my vision for how we can tackle the next generation of industrial data challenges.
    """)
    st.markdown("---")

    # --- B. Impactful Projects Section ---
    st.header("Impactful Projects with Seeq")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="project-title">🏭 Golden Batch Automation</h2>', unsafe_allow_html=True)
        st.markdown("<h3>Challenge:</h3> <p>To reduce the high variability and cycle time in batch processes, a common problem across multiple global sites.</p>", unsafe_allow_html=True)
        st.markdown("<h3>My Solution with Seeq:</h3> <p>I created a fully automated analytical template in Seeq Data Lab that standardizes KPIs and asset structures from just 3 base signals (Batch ID, recipe, and operation).</p>", unsafe_allow_html=True)
        st.markdown("<h3>Impact:</h3>", unsafe_allow_html=True)
        st.markdown(f'<p class="metric-number">$2 Million/year</p>', unsafe_allow_html=True)
        st.markdown("<p>in savings per plant, with a <b>5-10% reduction in cycle time</b>. The solution was replicated globally.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="project-card">', unsafe_allow_html=True)
        st.markdown('<h2 class="project-title">🧪 Soft Sensor & Digital Twin</h2>', unsafe_allow_html=True)
        st.markdown("<h3>Challenge:</h3> <p>To predict product quality (acid number) in real time for a fast process with scarce lab data and imprecise measurements.</p>", unsafe_allow_html=True)
        st.markdown("<h3>My Solution with Seeq:</h3> <p>I developed a hybrid model combining a phenomenological model (mass balance) with a <b>Physics-Informed Neural Network (PINN)</b> to create a reactor Digital Twin, integrated into the Seeq environment.</p>", unsafe_allow_html=True)
        st.markdown("<h3>Impact:</h3>", unsafe_allow_html=True)
        st.markdown(f'<p class="metric-number">$350k/year</p>', unsafe_allow_html=True)
        st.markdown("<p>in reduced off-spec product losses. A scalable solution for other sulfation units.</p>", unsafe_allow_html=True)
        with st.expander("The following example illustrates why the PINN approach was crucial"):
            st.markdown("""
            In the Soft Sensor project, lab data was sparse (one sample per hour for a process of minutes). A standard Neural Network (NN) or XGBoost would struggle to predict what occurs between samples, potentially leading to incorrect conclusions.

            The solution was to use a **PINN**, which combines two sources of information:
            1.  **Process Data:** The few measurement points we had.
            2.  **Laws of Physics:** The mass balance equations of the reactor.

            The AI model is penalized if its predictions violate the laws of physics. The result is a model that not only fits the data but is also **consistent with the process reality**, as the animation below illustrates.
            """)
            st.image("pinn_animation.gif")
        st.markdown('</div>', unsafe_allow_html=True)
        
    st.markdown('</div>', unsafe_allow_html=True)


# --- C. MVP Section - The Guided Conversation ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="main-content-container">', unsafe_allow_html=True)
st.markdown("---")
st.header("MVP: A Conceptual Demonstration")
st.markdown("""
This is a **conceptual demonstration** that illustrates a core vision: solving the pain of data that lacks context. In many plants, even when data is collected in one place, it is not truly connected, for example, a pressure reading does not ‘know’ its own maintenance history. This demo shows how Generative AI **could** build those relationships, enabling an engineer to 'talk' to their plant and get instant answers.
""")
st.info("This is a guided demonstration. Click the button that appears at each step to continue the conversation.", icon="👇")

if "messages" not in st.session_state:
    st.session_state.messages = []
    st.session_state.conversation_step = 0
    st.session_state.is_thinking = False

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        message["function"]()

if st.session_state.is_thinking:
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            time.sleep(1.5)
            if st.session_state.conversation_step == 1:
                response_func = display_pump_maintenance_response
            elif st.session_state.conversation_step == 2:
                response_func = display_fermentation_response
            elif st.session_state.conversation_step == 3:
                response_func = display_salicylic_acid_response
            st.session_state.messages.append({"role": "assistant", "function": response_func})
            st.session_state.is_thinking = False
            st.rerun()

elif not st.session_state.is_thinking:
    if st.session_state.conversation_step == 0:
        if st.button("pump maintenance history from unit 1"):
            st.session_state.messages.append({"role": "user", "function": lambda: st.markdown("pump maintenance history from unit 1")})
            st.session_state.conversation_step = 1
            st.session_state.is_thinking = True
            st.rerun()
    elif st.session_state.conversation_step == 1:
        if st.button("fermentation parameters from unit 1"):
            st.session_state.messages.append({"role": "user", "function": lambda: st.markdown("fermentation parameters from unit 1")})
            st.session_state.conversation_step = 2
            st.session_state.is_thinking = True
            st.rerun()
    elif st.session_state.conversation_step == 2:
        if st.button("salicylic acid tags from unit 2"):
            st.session_state.messages.append({"role": "user", "function": lambda: st.markdown("salicylic acid tags from unit 2")})
            st.session_state.conversation_step = 3
            st.session_state.is_thinking = True
            st.rerun()
    elif st.session_state.conversation_step == 3:
        st.success("This concludes the guided demonstration. The full chat history is available above.", icon="✅")

st.markdown('</div>', unsafe_allow_html=True)


# --- D. My Vision Section ---
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown('<div class="main-content-container">', unsafe_allow_html=True)
st.markdown("---")
st.header("My Vision: From Industrial Pains to Scalable Solutions")
st.markdown("My experience has highlighted three key areas where I believe we can deliver immense value by solving common industry pains. My vision is to transform these challenges into scalable, integrated solutions:")
st.markdown("<br>", unsafe_allow_html=True)

v_col1, v_col2 = st.columns(2)
with v_col1:
    st.markdown("""
    <div class="vision-card">
        <h2>🚀</h2>
        <h4>Scalable AI Models</h4>
        <p>Move beyond slow, one-off projects toward scalable deployment. My vision is to create foundational models for asset classes that can be rapidly <b>fine-tuned</b> to fit specific assets. A perfect application is developing predictive maintenance templates for <b>motor vibration signals</b>: a model is trained on an initial pump, and then rapidly deployed to all other similar pumps in a unit. This approach automates deployment and empowers customers to scale advanced analytics across their entire plant.</p>
    </div>
    """, unsafe_allow_html=True)
    
with v_col2:
    st.markdown("""
    <div class="vision-card">
        <h2>🧠</h2>
        <h4>Industrial Knowledge Partner</h4>
        <p>Bridge the critical "context gap" where engineers waste hours searching for information. My goal is to evolve the MVP into a full <b>knowledge partner</b> that connects siloed data tags, manuals, P&IDs, and logs—into a single, conversational interface, making the plant's collective knowledge instantly accessible.</p>
    </div>
    """, unsafe_allow_html=True)


st.markdown('</div>', unsafe_allow_html=True)
