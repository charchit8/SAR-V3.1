from utils import *

# Setting Env
if st.secrets["OPENAI_API_KEY"] is not None:
    os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
else:
    os.environ["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY")

#This is the embedding model
model_name = "thenlper/gte-small"
# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# model_name = "hkunlp/instructor-large"   
    
# Memory setup for gpt-3.5
llm = ChatOpenAI(temperature=0.1)
memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=500)
conversation = ConversationChain(llm=llm, memory =memory,verbose=False)

def key_questions():
    # creating columns
    col1,col2 = st.columns(2)
    with col1:
        st.markdown("""<span style="font-size: 24px; ">Key Questions</span>""", unsafe_allow_html=True)
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
            df_fixed["S.No."] = df_fixed.index
            df_fixed = df_fixed.loc[:,['S.No.','Questions']]
            st.markdown(df_fixed.style.hide(axis="index").to_html(), unsafe_allow_html=True)


def generate_insights_gpt(temp_file_path):

    hf_embeddings = embed(model_name) 
    docs, docsearch = embedding_store(temp_file_path,hf_embeddings)   

    with st.spinner('Wait for it...'):
        # if 'clicked1' not in st.session_state:
        #     st.session_state.clicked1 = False
        
        # def set_clicked1():
        #     st.session_state.clicked1 = True
        #     st.session_state.disabled = True

        if st.button("Generate Insights", disabled=st.session_state.disabled):
                            
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

    st.markdown("---")

    # Text Input
    # st.markdown("""<span style="font-size: 24px; ">Ask Additional Questions</span>""", unsafe_allow_html=True)

    query = st.text_input(':black[Ask Additional Questions]',disabled=st.session_state.disabled)
    text_dict = {}
    @st.cache_data
    def LLM_Response(query,context):
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        response = llm_chain.run({"query":query, "context":context})
        return response
    
    with st.spinner('Getting you information...'):      
        if query:
            # Text input handling logic
            #st.write("Text Input:")
            #st.write(text_input)

            context_1 = docsearch.similarity_search(query, k=5)
            st.session_state.context_1 = context_1
            if query.lower() == "what is the victim's name?":
                prompt_1 = f'''Perform Name Enitity Recognition to identify the Customer name as accurately as possible, given the context. The Customer can also be referenced as the Victim or the person with whom the Fraud has taken place.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''
                
            elif query.lower() == "what is the suspect's name?":
                prompt_1 = f'''Perform Name Enitity Recognition to identify the Suspect name as accurately as possible, given the context. Suspect is the Person who has committed the fraud with the Customer. Respond saying "The Suspect Name is not Present" if there is no suspect in the given context.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                
            elif query.lower() == "list the merchant name":
                prompt_1 = f'''Perform Name Enitity Recognition to identify all the Merchant Organizations as accurately as possible, given the context. A merchant is a type of business or organization that accepts payments from the customer account. Give a relevant and concise response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                
            elif query.lower() == "how was the bank notified?":
                prompt_1 = f''' You need to act as a Financial analyst to identify how was the bank notified of the Supicious or Fraud event with in the given context. The means of communication can be a call, an email or in person. Give a relevant and concise response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                
            elif query.lower() == "when was the bank notified?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the when the bank was notified of the Fraud i.e., the disputed date. Given the context, provide a relevant and concise response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                
            elif query.lower() == "what type of fraud is taking place?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the type of fraud or suspicious activity has taken place amd summarize it, within the given context. Also mention the exact fraud code. Give a relevant and concise response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

            
            elif query.lower() == "when did the fraud occur?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the when the did the fraud occur i.e., the Transaction Date. Given the context, provide a relevant and concise response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                    
            elif query.lower() == "was the disputed amount greater than 5000 usd?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the disputed amount and perform a mathematical calculation to check if the disputed amount is greater than 5000 or no, given the context. Give a relevant and concise response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                
            elif query.lower() == "what type of cards are involved?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the type of card and card's brand involved, given the context. On a higher level the card can be a Credit or Debit Card. VISA, MasterCard or American Express, Citi Group, etc. are the different brands with respect to a Credit card or Debit Card . Give a relevant and concise response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                
            elif query.lower() == "was the police report filed?":
                prompt_1 = f''' You need to act as a Financial analyst to identify if the police was reported of the Fraud activity, given the context. Give a relevant and concise response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                    
            elif query.lower() == "Is this a valid SAR case?":
                prompt_1 = f''' You need to act as a Financial analyst to check if this is a SAR or not, given the following context, if the transaction amount is less than 5000 USD we cannot categorize this as SAR (Suspicious activity Report).Give a relevant and concise response. \n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: '''

                
            else:
                prompt_1 = f'''Act as a financial analyst and give concise answer to below Question as truthfully as possible, with given Context.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\                      
                            Response: '''


            #prompt = PromptTemplate(template=prompt, input_variables=["query", "context"])
            response = usellm(prompt_1) #LLM_Response()
            text_dict[query] = response
            # resp_dict_obj.update(text_dict)
            st.write(response)
            
            if response:
                df = pd.DataFrame(text_dict.items(), columns=['Question','Answer'])
            else:
                df = pd.DataFrame()

            st.session_state["tmp_table_gpt"] = pd.concat([st.session_state.tmp_table_gpt, df], ignore_index=True)
            st.session_state.tmp_table_gpt.drop_duplicates(subset=['Question'])

    return st.session_state["tmp_table_gpt"], st.session_state["sara_recommendation_gpt"]



def summarize_gpt():
    with st.spinner('Summarization ...'):
        # if 'clicked2' not in st.session_state:
        #     st.session_state.clicked2 = False
        
        # def set_clicked2():
        #     st.session_state.clicked2 = True
        #     st.session_state.disabled = True

        st.markdown("""<span style="font-size: 24px; ">Summarize key findings of the case.</span>""", unsafe_allow_html=True)
        st.write()
        summ_gpt = st.button("Summarize",disabled=st.session_state.disabled)

        if summ_gpt:
            st.session_state.disabled=False
            summ_dict_gpt = st.session_state.tmp_table_gpt.set_index('Question')['Answer'].to_dict()
            # chat_history = resp_dict_obj['Summary']
            memory = ConversationSummaryBufferMemory(llm=llm, max_token_limit=300)
            memory.save_context({"input": "This is the entire summary"}, 
                                {"output": f"{summ_dict_gpt}"})
            conversation = ConversationChain(
            llm=llm, 
            memory = memory,
            verbose=True)
            response_summ_gpt = conversation.predict(input="Provide a detailed summary of the text provided by reframing the sentences. Provide the summary in a single paragraph. Please don't include words like these: 'chat summary', 'includes information' in my final summary.")
            response_summ_gpt = response_summ_gpt.replace("$", " ")
            response_summ_gpt = response_summ_gpt.replace("5,000", "5,000 USD")
            response_summ_gpt = response_summ_gpt.replace("5,600", "5,600 USD")
            st.session_state["tmp_summary_gpt"] = response_summ_gpt
            st.write(st.session_state["tmp_summary_gpt"])
    
    return st.session_state["tmp_summary_gpt"],summ_gpt



