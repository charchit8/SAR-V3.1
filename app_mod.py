#-*- coding: utf-8 -*-
#!/usr/bin/python

from utils import *
from data import data_display,create_temp_file
from closed_source import generate_insights,summarize,run_doc
from report import summ_table_report,save_report1,save_report2,download_report
from decision import decision_gpt,decision_llama,selection1,selection2


# Setting Config for Llama-2
login(token=st.secrets["HUGGINGFACEHUB_API_TOKEN"])
os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]


# Setting globals
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = True
if "stored_session" not in st.session_state:
    st.session_state["stored_session"] = []
if "tmp_table_gpt" not in st.session_state:
    st.session_state.tmp_table_gpt=pd.DataFrame()
if "tmp_table_llama" not in st.session_state:
    st.session_state.tmp_table_llama=pd.DataFrame()
if "tmp_summary_gpt" not in st.session_state:
    st.session_state["tmp_summary_gpt"] = ''
if "tmp_summary_llama" not in st.session_state:
    st.session_state["tmp_summary_llama"] = ''
if "sara_recommendation_gpt" not in st.session_state:
    st.session_state["sara_recommendation_gpt"] = ''
if "sara_recommendation_llama" not in st.session_state:
    st.session_state["sara_recommendation_llama"] = ''
if "case_num" not in st.session_state:
    st.session_state.case_num = ''
if "fin_opt" not in st.session_state:
    st.session_state.fin_opt = ''
if "context_1" not in st.session_state:
    st.session_state.context_1 = ''
if "llm" not in st.session_state:
    st.session_state.llm = 'Closed-Source'



# Apply CSS styling to resize the buttons
st.markdown("""
    <style>
        .stButton button {
            width: 145px;
            height: 35px;
        }
    </style>
""", unsafe_allow_html=True)




####### This markdown is to manage app style
st.markdown("""

<style>
            

.st-d5 {
    line-height: 1;
}


.css-1upf7v9 { 
    gap: 0.5rem;
}

.css-1balh2r{
    gap: 0;
}

.css-1544g2n {
    padding: 0;
    padding-top: 2rem;
    padding-right: 1rem;
    padding-bottom: 1.5rem;
    padding-left: 1rem;
}

.css-1q2g7hi {
    top: 2px;
    min-width: 350px;
    max-width: 600px;
    }

.st-ah {
    line-height: 1;
}

.st-af {
    font-size: 1.5rem;
}

.css-1a65djw {
    gap: 0;
    }

.css-1y4p8pa {
    width: 100%;
    padding: 3rem 1rem 10rem;
    padding-top: 3rem;
    padding-bottom: 10rem;
    max-width: 60rem;
}

.css-xujc5b p{
   font-size: 25px;
}

.css-jzprzu {
    height: 2rem;
    min-height: 1rem;
    }

</style>
""", unsafe_allow_html=True)

# Addding markdown styles(Global)
st.markdown("""
<style>
.big-font {
    font-size:60px !important;
}
</style>
""", unsafe_allow_html=True)


# Set Sidebar
st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: FBFBFB;
    }
</style>
""", unsafe_allow_html=True)

#Adding llm type-> st.session_state.llm
st.session_state.llm = st.radio("",options = pd.Series(["Closed-Source","Open-Source"]), horizontal=True)

st.markdown("---")

st.title("Suspicious Activity Reporting Assistant")
with st.sidebar:
    # st.sidebar.write("This is :blue[test]")
    # Navbar
    st.markdown('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">', unsafe_allow_html=True)

    st.markdown("""
    <nav class="navbar fixed-top navbar-expand-lg navbar-dark" style="background-color: #000000;">
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <style>
    .navbar-brand img {
      max-height: 50px; /* Adjust the height of the logo */
      width: auto; /* Allow the width to adjust based on the height */
    }
    </style>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
        <li class="nav-item active">
            <a class="navbar-brand" href="#">
                <img src="https://www.exlservice.com/themes/exl_service/exl_logo_rgb_orange_pos_94.png" width="50" height="30" alt="">
                <span class="sr-only">(current)</span>
                <strong>| Operations Process Automation</strong>
            </a>
        </li>
        </ul>
    </div>
    </nav>
    """, unsafe_allow_html=True)

    st.markdown("""
    <nav class="navbar fixed-bottom navbar-expand-lg navbar-dark" style="background-color: #000000;">
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav">
        <li class="nav-item active">
        <!--p style='color: white;'><b>Powered by EXL</b></p--!>
        <p style='color: white;'> <strong>Powered by EXL</strong> </p>
            <!--a class="nav-link disabled" href="#">
                <img src="https://www.exlservice.com/themes/exl_service/exl_logo_rgb_orange_pos_94.png" width="50" height="30" alt="">
                <span class="sr-only">(current)</span>
            </a--!>
        </li>
        </ul>
    </div>
    </nav>
    """, unsafe_allow_html=True)

    # Add the app name
    st.sidebar.markdown('<p class="big-font">SARA</p>', unsafe_allow_html=True)
    # st.sidebar.header("SARA")
    st.markdown("---")

    # Add a drop-down for case type
    option1 = ["Select Case Type", "Fraud transaction dispute", "Money Laundering", "Insider Trading"]
    selected_option_case_type = st.sidebar.selectbox("", option1)
    st.markdown("---")
    
    # Add a single dropdown
    option2 = ["Select Case ID", "SAR-2023-24680", "SAR-2023-13579", "SAR-2023-97531", "SAR-2023-86420", "SAR-2023-24681"]
    selected_option = st.sidebar.selectbox("", option2)
    # Add the image to the sidebar below options
    st.sidebar.image("MicrosoftTeams-image (3).png", use_column_width=True)

    
# Adding action to the main section
if selected_option_case_type == "Select Case Type":
    st.header("")
elif selected_option_case_type == "Fraud transaction dispute":
    st.markdown("### :blue[Fraud transaction dispute]")

# st.markdown('---')

# Selecting case type here
    
    if selected_option == "SAR-2023-24680":
        st.session_state.case_num = "SAR-2023-24680"

        col1,col2 = st.columns(2)
        # Row 1
        with col1:
            st.markdown("##### **Case number&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:** SAR-2023-24680")
            st.markdown("##### **Customer name  :** John Brown")


        with col2:
            st.markdown("##### **Case open date&nbsp;&nbsp;&nbsp;&nbsp;:** Feb 02, 2021")
            st.markdown("##### **Case type&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:** Fraud transaction")


        # Row 2
        with col1:
            st.markdown("##### **Customer ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:** 9659754")


        with col2:
            st.markdown("##### **Case Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:** Open")

    elif selected_option == "SAR-2023-13579":
        st.session_state.case_num = "SAR-2023-13579"

        col1,col2 = st.columns(2)
        # Row 1
        with col1:
            st.markdown("##### **Case number&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:** SAR-2023-13579")
            st.markdown("##### **Customer name  :** John Brown")


        with col2:
            st.markdown("##### **Case open date&nbsp;&nbsp;&nbsp;&nbsp;:** Feb 02, 2021")
            st.markdown("##### **Case type&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:** Fraud transaction")


        # Row 2
        with col1:
            st.markdown("##### **Customer ID&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:** 9659754")


        with col2:
            st.markdown("##### **Case Status&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;:** Open")

    st.markdown("---")


 
## Case where Suspect is not mentioned           
    if st.session_state.case_num == "SAR-2023-24680":
        col1_up, col2_up, col3_up, col4_up, col5_up = st.tabs(["Data", "Generate Insights","Summarization","Download Report", "Make a Decision"])
        
        with col1_up:
            directory_path = "data/"
            fetched_files = read_pdf_files(directory_path)
            data_display(directory_path,fetched_files)
            temp_file_path =  create_temp_file(directory_path,fetched_files)

        with col2_up:  
                   
             tmp_table_gpt, sara_recommendation_gpt,generate_button = generate_insights(temp_file_path)

        with col3_up:
            tmp_summary_gpt = summarize()
        
        with col4_up:
            col_d1, col_d2 = st.tabs(["Download Report", "Download Case Package"])

            with col_d1:
                if st.session_state.llm == "Closed-Source":
                # Applying to download button -> download_button
                    st.markdown("""
                        <style>
                            .stButton download_button {
                                width: 100%;
                                height: 70%;
                            }
                        </style>
                    """, unsafe_allow_html=True)

                    tmp_summary, tmp_table = summ_table_report(tmp_table_gpt,tmp_summary_gpt)
                    doc = save_report1(tmp_table,tmp_summary,sara_recommendation_gpt)
                    bio = io.BytesIO()
                    if doc:
                        st.download_button(
                        label="Download Report",
                        data=bio.getvalue(),
                        file_name="Report.docx",
                        mime="docx",
                        disabled=st.session_state.disabled
                         )
            with col_d2:
                if st.session_state.llm == "Closed-Source": 
                    st.write("")            
                    download_report(doc,directory_path,fetched_files)
        
        with col5_up:
            st.markdown("""<span style="font-size: 24px;color:#0000FF">Is SAR filing required?</span>""", unsafe_allow_html=True)
            if st.session_state.llm == "Closed-Source": 
                decision_gpt(generate_button,temp_file_path)
            
            selection1()

## Case where Suspect is not mentioned
    elif st.session_state.case_num == "SAR-2023-13579":
        col1_up, col2_up, col3_up, col4_up, col5_up = st.tabs(["Data", "Generate Insights","Summarization","Download Report", "Make a Decision"])
        
        with col1_up:
            directory_path = "data2/"
            fetched_files = read_pdf_files(directory_path)
            data_display(directory_path,fetched_files)
            temp_file_path =  create_temp_file(directory_path,fetched_files)   

        with col2_up:
            if st.session_state.llm == "Closed-Source":
                tmp_table_gpt, sara_recommendation_gpt, generate_button = generate_insights(temp_file_path)
        
        with col3_up:
            if st.session_state.llm == "Closed-Source":
                tmp_summary_gpt = summarize()

        with col4_up:
            col_d1, col_d2 = st.tabs(["Download Report", "Download Case Package"])

            with col_d1:
                if st.session_state.llm == "Closed-Source":
                # Applying to download button -> download_button
                    st.markdown("""
                        <style>
                            .stButton download_button {
                                width: 100%;
                                height: 70%;
                            }
                        </style>
                    """, unsafe_allow_html=True)

                    tmp_summary, tmp_table = summ_table_report(tmp_table_gpt,tmp_summary_gpt)
                    doc = save_report1(tmp_table,tmp_summary,sara_recommendation_gpt)
                    bio = io.BytesIO()
                    if doc:
                        st.download_button(
                        label="Download Report",
                        data=bio.getvalue(),
                        file_name="Report.docx",
                        mime="docx",
                        disabled=st.session_state.disabled
                         )
            with col_d2:
                if st.session_state.llm == "Closed-Source":   
                    st.write("")        
                    download_report(doc,directory_path,fetched_files)
        
        with col5_up:
            st.markdown("""<span style="font-size: 24px;color:#0000FF">Is SAR filing required?</span>""", unsafe_allow_html=True)     
            if st.session_state.llm == "Closed-Source": 
                decision_gpt(generate_button,temp_file_path)
            
            selection2()
        


    


elif selected_option_case_type == "Money Laundering":
    st.markdown("### :red[Money Laundering]")
     
       #Add code for AML here

elif selected_option_case_type == "Insider Trading":
    st.markdown("### :red[Insider Trading]")

      #Add code for IT here


# Footer
st.markdown(
    """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """
    , unsafe_allow_html=True)
st.markdown('<div class="footer"><p></p></div>', unsafe_allow_html=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)


padding = 0
st.markdown(f""" <style>
    .reportview-container .main .block-container{{
        padding-top: {padding}rem;
        padding-right: {padding}rem;
        padding-left: {padding}rem;
        padding-bottom: {padding}rem;
    }} </style> """, unsafe_allow_html=True)




