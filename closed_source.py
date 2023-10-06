from utils import *

# Setting Env
if st.secrets["OPENAI_API_KEY"] is not None:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")


# Chunking with overlap
text_splitter = RecursiveCharacterTextSplitter(
chunk_size = 1000,
chunk_overlap  = 100,
length_function = len,
separators=["\n\n", "\n", " ", ""]
)


#This is the embedding model
model_name = "thenlper/gte-small"
# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# model_name = "hkunlp/instructor-large"




@st.cache_resource
def embed(model_name):
    hf_embeddings = HuggingFaceEmbeddings(model_name=model_name)
    return hf_embeddings


@st.cache_data
def embedding_store(pdf_files,hf_embeddings):
    merged_pdf = merge_pdfs(pdf_files)
    final_pdf = PyPDF2.PdfReader(merged_pdf)
    text = ""
    for page in final_pdf.pages:
        text += page.extract_text()

    texts =  text_splitter.split_text(text)
    docs = text_to_docs(texts)
    docsearch = FAISS.from_documents(docs, hf_embeddings)
    return docs, docsearch
    
    
# Memory setup for gpt-3.5
llm = ChatOpenAI(temperature=0.1)
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=500)
conversation = ConversationChain(llm=llm, memory =memory,verbose=False)


@st.cache_data
def usellm(prompt):
    """
    Getting GPT-3.5 Model into action
    """
    service = UseLLM(service_url="https://usellm.org/api/llm")
    messages = [
      Message(role="system", content="You are a fraud analyst, who is an expert at finding out suspicious activities"),
      Message(role="user", content=f"{prompt}"),
      ]
    options = Options(messages=messages)
    response = service.chat(options)
    return response.content




def generate_insights(temp_file_path):

    # Adding condition on embedding
    try:
        if temp_file_path:
            hf_embeddings = embed(model_name) 
        else:
            pass
    except NameError:
        pass

    # # Chunking with overlap
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size = 1000,
    #     chunk_overlap  = 100,
    #     length_function = len,
    #     separators=["\n\n", "\n", " ", ""]
    # )

    
    try:
        if temp_file_path:
            docs, docsearch = embedding_store(temp_file_path)
        else:
            pass
    except Exception:
        pass
    
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

    with st.spinner('Wait for it...'):
          generate_button =  st.button("Generate Insights",disabled=st.session_state.disabled)

          if generate_button:

                if st.session_state.llm == "Closed-Source":
                    queries ="Please provide the following information regarding the possible fraud case: What is the name of the customer name,\
                    has any suspect been reported, list the merchant name, how was the bank notified, when was the bank notified, what is the fraud type,\
                    when did the fraud occur, was the disputed amount greater than 5000 USD, what type of cards are involved, was the police report filed,\
                    and based on the evidence, is this a suspicious activity(Summarize all the questions asked prior to this in a detailed manner),that's the answer of\
                    whether this is a suspicious activity\
                    "
                    contexts = docsearch.similarity_search(queries, k=5) 
                    prompts = f" Give a the answer to the below questions as truthfully and in as detailed in the form of sentences\
                    as possible as per given context only,\n\n\
                            What is the victim's name?\n\
                            What is the suspect's name?\n\
                            List the merchant name\n\
                            How was the bank notified?\n\
                            When was the bank notified?\n\
                            What is the fraud type?\n\
                            When did the fraud occur?\n\
                            Was the disputed amount greater than 5000 USD?\n\
                            What type of cards are involved?\n\
                            Was the police report filed?\n\
                        Context: {contexts}\n\
                        Response (in the python dictionary format\
                        where the dictionary key would carry the questions and its value would have a descriptive answer to the questions asked): "
                        
                    response = usellm(prompts)

                    try:
                        resp_dict_obj = json.loads(response)
                        res_df_gpt = pd.DataFrame(resp_dict_obj.items(), columns=['Question','Answer'])
                    except:
                        e = Exception("")
                        st.exception(e)

                               

                    # try:
                        # res_df_gpt.Question = res_df_gpt.Question.apply(lambda x: x.split(".")[1])
                        # res_df_gpt.index = res_df.index + 1
                        # df_base_gpt = res_df_gpt.copy(deep=True)
                        # df_base_gpt["S.No."] = df_base_gpt.index
                        # df_base_gpt = df_base_gpt.loc[:,['S.No.','Question','Answer']]
                        # st.write(df_base_gpt)
                    # except IndexError:
                    #     pass
                    # #st.table(res_df_gpt)
                    # st.markdown(df_base_gpt.style.hide(axis="index").to_html(), unsafe_allow_html=True)
                    # st.session_state["tmp_table_gpt"] = pd.concat([st.session_state.tmp_table_gpt, res_df_gpt], ignore_index=True)
                    
                    try:
                        res_df_gpt.reset_index(drop=True, inplace=True)
                        index_ = pd.Series([1,2,3,4,5,6,7,8,9,10])
                        res_df_gpt = res_df_gpt.set_index([index_])   
                    except IndexError: 
                        pass

                    st.table(res_df_gpt)
                    st.session_state["tmp_table_gpt"] = pd.concat([st.session_state.tmp_table_gpt, res_df_gpt], ignore_index=True)

                    
                    query ="Is this is a Suspicious activity or not?"
                    contexts = docsearch.similarity_search(query, k=5) 
                    prompt = f" You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
                        If The transaction/disputed amount > 5,000 USD value threshold and a potential suspect name is identified? Then only this can be addressed as a suspicious activity.\n\n\
                        Suspect is the person who has committed the fraud with the Customer (customer is the cardholder).\n\n\
                        Even if transaction/disputed amount > 5,000 USD but if no suspect is identified, then this cannot be considered as a suspicious activity. \n\n\
                        If transaction/disputed amount is < 5000 USD threshold and no suspect is identified, write your response as - There is no indication of suspicious activity.\n\n\
                        Based the above findings, identify if this can be consider as Suspicious Activity or not.\n\n\
                        Context: {contexts}\n\
                        Response (Give me a concise response in three-four pointers.)"
                    response1 = usellm(prompt) 
                    
                    # This replace text is basically to stop rendering of $ to katex (that creates the text messy, hence replacing $)
                    response1 = response1.replace("$", " ")
                    response1 = response1.replace("5,000", "5,000 USD")
                    response1 = response1.replace("5,600", "5,600 USD")
                    st.session_state["sara_recommendation_gpt"] = response1                
                    
                    st.markdown("### SARA Recommendation")
                    st.markdown(response1)


    