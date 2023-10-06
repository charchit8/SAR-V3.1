from utils import *

#This is the embedding model
model_name = "thenlper/gte-small"
# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# model_name = "hkunlp/instructor-large"

temp_file_path = []

# Memory setup for gpt-3.5
llm = ChatOpenAI(temperature=0.1)
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=500)
conversation = ConversationChain(llm=llm, memory =memory,verbose=False)



# Adding condition on embedding
try:
    if temp_file_path:
        hf_embeddings = embed(model_name) 
    else:
        pass
except NameError:
    pass



try:
    if temp_file_path:
        docs, docsearch = embedding_store(temp_file_path)
    else:
        pass
except Exception:
    pass



def generate_insights():
    
    # Creating header
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("""<span style="font-size: 24px; ">Key Questions</span>""", unsafe_allow_html=True)
        # st.subheader('Key Questions')
        # Create a Pandas DataFrame with your data
        data = {'Questions': [" What is the victim's name?","What is the suspect's name?",' List the merchant name',' How was the bank notified?',' When was the bank notified?',' What is the fraud type?',' When did the fraud occur?',' Was the disputed amount greater than 5000 USD?',' What type of cards are involved?',' Was the police report filed?']}
        df_fixed = pd.DataFrame(data)
        df_fixed.index = df_fixed.index +1
    with col2:
        # Create a checkbox to show/hide the table
        cols1, cols2, cols3, cols4 = st.columns([1,1,1,1])
        with cols1:
            show_table = tog.st_toggle_switch(label="", 
                                key="Key1", 
                                default_value=False, 
                                label_after = False, 
                                inactive_color = '#D3D3D3', 
                                active_color="#11567f", 
                                track_color="#29B5E8"
                                )
        # Show the table if the checkbox is ticked
        if show_table:
            # st.write(df_fixed)
            # st.dataframe(df_fixed, width=1000)
            df_fixed["S.No."] = df_fixed.index
            df_fixed = df_fixed.loc[:,['S.No.','Questions']]
            st.markdown(df_fixed.style.hide(axis="index").to_html(), unsafe_allow_html=True)

    