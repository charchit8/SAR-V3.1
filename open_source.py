from utils import *

# Setting Config for Llama-2
login(token=st.secrets["HUGGINGFACEHUB_API_TOKEN"])
os.environ["HUGGINGFACEHUB_API_TOKEN"] = st.secrets["HUGGINGFACEHUB_API_TOKEN"]

#This is the embedding model
# model_name = "thenlper/gte-small"
model_name = "sentence-transformers/all-MiniLM-L6-v2"
# model_name = "hkunlp/instructor-large" 

def generate_insights_llama(temp_file_path):

    hf_embeddings = embed(model_name) 
    docs, docsearch = embedding_store(temp_file_path,hf_embeddings) 

    with st.spinner('Wait for it...'):
        # if 'clicked3' not in st.session_state:
        #     st.session_state.clicked3 = False
        
        # def set_clicked3():
        #     st.session_state.clicked3 = True
        #     st.session_state.disabled = True

        if st.button("Generate Insights", disabled=st.session_state.disabled):

            chat_history = {}

            query = "What is the victim's name?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 = f'''You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
            Perform Name Enitity Recognition to identify the victim's name. Victim is the person with whom fraud has taken place and who is the owner of the account/card. \n\n\
                    Question: {query}\n\
                    Context: {context_1}\n\
                    Response: (Give me response in one sentence. Do not give me any Explanation or Note)'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response


            query = "What is the suspect's name?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 =  f'''Act as a professional fraud analyst.You need to check the document and compare if any name discrepencies are present that points towards the suspect who used the card without the consent of the cardholder.
                        Perform Name Enitity Recognition to identify the Suspect Name as accurately as possible, given the context.Suspect is the person who has committed the fraud with the customer/cardholder. If suspect name is not present, respond saying: Suspect name is not mentioned.\n\n\
                        Context: {context_1}\n\
                        Response: (Give a short response in a single sentence.Do not give me any Explanation or Note)'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response
            
            
            query = "list the merchant name"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 = f'''You are a professional fraud analyst, perform Name Enitity Recognition to identify Merchant as accurately as possible from the provided information.A merchant is a type of business or organization that accepts payments from the customer account. Give a relevant and short response.\n\n\
                Take the provided information as accurate.\n\n\
                        Question: {query}\n\
                        Context: {context_1}\n\
                        Response: (Give a short response in a single sentence. Do not add any extra Note.)'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response


            query = "How was the bank notified?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 =  f'''You need to act as a Financial analyst to identify how was the bank notified of the Supicious or Fraud event with in the given context. The means of communication can be a call, an email or in person. Give a concise response.\n\n\
                        Question: {query}\n\
                        Context: {context_1}\n\
                        Response: (Give me a concise response in one sentence. Do not give me any further Explanation, Note )'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response

            
            query = "When was the bank notified?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 =  f'''You need to act as a Financial analyst to identify when the bank was notified of the Fraud. Look for the disputed date. Given the context, provide a relevant and concise response.\n\n\
                        Question: {query}\n\
                        Context: {context_1}\n\
                        Response: (Give me a concise response in one sentence.Do not add any prefix like 'Response' or 'Based on the document'. Do not add any extra Explanation, Note)'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response               


            query = "What is the Fraud Type?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 =  f''' You need to act as a Financial analyst to identify the type of fraud or suspicious activity has taken place amd summarize it, within the given context. Also mention the exact fraud code. Give a relevant and concise response.\n\n\
                        Question: {query}\n\
                        Context: {context_1}\n\
                        Response: (Give me response in one sentence. Do not add prefix like 'Response' or 'based on the document. Do not give me any Explanation or Note)'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response


            query = "When did the fraud occur?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 =  f''' You need to act as a Financial analyst to identify the when the did the fraud occur i.e., the Transaction Date. Given the context, provide a relevant and concise response.\n\n\
                        Question: {query}\n\
                        Context: {context_1}\n\
                        Response: (Give me a concise response in one sentence. Do not add prefix like 'based on the document. Do not add any further Explanation or Note.)'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response


            query = "Was the disputed amount greater than 5000 usd?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 =  f''' You need to act as a Financial analyst to identify the disputed amount mentioned in the context.Perform a mathematical calculation to check if the disputed amount is greater than 5000 USD or not.Given the context, give a relevant and concise response.\n\n\
                                Take the provided information as accurate. \n\n\
                        Question: {query}\n\
                        Context: {context_1}\n\
                        Response: (Give a short response in a single sentence. Do not give any extra Explanation, Note, Descricption, Information.)'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response


            query = "What type of cards are involved?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 =  f''' You need to act as a Financial analyst to identify the type of card and card network involved, given the context. On a higher level the card can be a Credit Visa, Debit Visa Card.Based on the context give a relevant and concise response.\n\n\
                        Question: {query}\n\
                        Context: {context_1}\n\
                        Response: (Give me a concise response in one sentence.Do not add prefix like: ['based on the document']. Do not add any further Explanation, Note.')'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response


            query = "was the police report filed?"
            context_1 = docsearch.similarity_search(query, k=5)
            prompt_1 =  f''' You need to act as a Financial analyst to identify if the police was reported of the Fraud activity, given the context. Give a relevant and concise response.\n\n\
                        Question: {query}\n\
                        Context: {context_1}\n\
                        Response: (Provide a concise Response in a single sentence. Do not write any extra [Explanation, Note, Descricption].)'''
            response = llama_llm(llama_13b,prompt_1)
            chat_history[query] = response


            try:
                res_df_llama = pd.DataFrame(list(chat_history.items()), columns=['Question','Answer'])
                res_df_llama.reset_index(drop=True, inplace=True)
                index_ = pd.Series([1,2,3,4,5,6,7,8,9,10])
                res_df_llama = res_df_llama.set_index([index_])
                # st.write(res_df_llama)
            except IndexError: 
                pass
            st.table(res_df_llama)
            st.session_state["tmp_table_llama"] = pd.concat([st.session_state.tmp_table_llama, res_df_llama], ignore_index=True)
        
            ## SARA Recommendation
            query ="Is invoice is billed to cardholder or someone else?"
            contexts = docsearch.similarity_search(query, k=5) 
            prompt = f" You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
            cardholder's name,adress can be identified from cardholder information. Customer is the person who is the owner of the card.\n\n\
            Identify name and address to whom merchant invoice is billed \n\n\
            Compare both the details, if details mentioned in invoice matches the cardholder details, then invoice is billed to customer else it is billed to someone else who misued the card.\n\n\
                Context: {contexts}\n\
                Response (Give me a concise response.)"
            response_3 = llama_llm(llama_13b,prompt) 

            st.write(response_3)

            
            query ="Is there a mention of potential suspect?"
            contexts = docsearch.similarity_search(query, k=5) 
            prompt = f" You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
            Perform Name Enitity Recognition to identify the Suspect name as accurately as possible, given the context. Suspect is the Person who has committed the fraud with the Customer. Respond saying :The Suspect Name is not Present, if there is no suspect in the given context.\n\n\
                Context: {contexts}\n\
                Response (Give me a concise response.)"
            response_4 = llama_llm(llama_13b,prompt) 

            st.write(response_4)


            query ="Is this is a Suspicious activity or not?"
            contexts = docsearch.similarity_search(query, k=5) 
            prompt = f" You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
                If The transaction/disputed amount > 5,000 USD value threshold, then check below points to make sure if it is a suspicious activity or not: \n\
                1. {response_3} analyse this response,if details matches then there is no suspicion else, it can be a suspicipos activity. (kindly mention the mismatched details in your response).\n\n\
                2. {response_4} analyse this response,If a potential suspect is identified then this can be a suspicious activity, else not.\n\n\
                Even if transaction/disputed amount > 5,000 USD but if above criteria does not met, then this can not be considered as a suspicious activity. \n\n\
                Based on above points identify if this is a case of suspicious activity or not based on the given context only? \n\n\
                Context: {contexts}\n\
                Response (Give me a concise response in few pointers.)"

                        
                                    
            response1 = llama_llm(llama_13b,prompt) 
            response1 = response1.replace("$", " ")
            response1 = response1.replace("5,000", "5,000 USD")
            response1 = response1.replace("5,600", "5,600 USD")          
            
            
            st.session_state["sara_recommendation_llama"] = response1                    

            st.markdown("### SARA Recommendation")
            st.markdown(response1)


    st.markdown("---")
    
    query = st.text_input(':black[Ask Additional Questions]',disabled=st.session_state.disabled)
    text_dict = {}

    with st.spinner('Getting you information...'):      
        if query:
            # Text input handling logic
            #st.write("Text Input:")
            #st.write(text_input)

            context_1 = docsearch.similarity_search(query, k=5)
            st.session_state.context_1 = context_1
            if query.lower() == "what is the victim's name?":
                prompt_1 = f'''Perform Name Enitity Recognition to identify the Customer name as accurately as possible, given the context. The Customer can also be referenced as the Victim or the person with whom the Fraud has taken place.
                            Customer/Victim is cardholder, whose card is used without their consent.
                            Do not provide any extra [Explanation, Note] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: (Provide a concise Response.) '''

                
            elif query.lower() == "what is the suspect's name?":
                prompt_1 = f''''Perform Name Enitity Recognition to identify the Suspect name as accurately as possible, given the context. Suspect is the Person who has committed the fraud with the Customer (customer is the cardholder). Respond saying "The Suspect Name is not Present" if there is no suspect in the given context.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: (Give me response in one sentence.Do not give me any Explanation or Note)'''


                
            elif query.lower() == "list the merchant name":
                prompt_1 = f'''Perform Name Enitity Recognition to identify all the Merchant Organizations as accurately as possible, given the context. A merchant is a type of business or organization that accepts payments from the customer account. Give a relevant and concise response.
                            Do not provide any extra [Explanation, Note] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: (Provide a concise Response without any extra [Explanation, Note, Descricption] below the Response.)'''

                
            elif query.lower() == "how was the bank notified?":
                prompt_1 = f''' You need to act as a Financial analyst to identify how was the bank notified of the Supicious or Fraud event with in the given context. The means of communication can be a call, an email or in person. Give a relevant and concise response.
                            Do not provide any extra [Explanation, Note] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response:(Provide a concise Response.) '''

                
            elif query.lower() == "when was the bank notified?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the when the bank was notified of the Fraud i.e., the disputed date. Given the context, provide a relevant and concise response.
                            Do not provide any extra [Explanation, Note] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: (Provide a concise Response.)'''

                
            elif query.lower() == "what type of fraud is taking place?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the type of fraud or suspicious activity has taken place amd summarize it, within the given context. Also mention the exact fraud code. Give a relevant and concise response.
                            Do not provide any extra [Explanation, Note] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: (Provide a concise Response without any extra [Explanation, Note, Descricption] below the Response.)'''

            
            elif query.lower() == "when did the fraud occur?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the type of card and card network involved, given the context. On a higher level the card can be a Credit Visa, Debit Visa Card.Based on the context give a relevant and concise response..
                            Do not provide any extra [Explanation, Note] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: (Provide a concise Response without any extra [Explanation, Note, Descricption] below the Response.)'''

                    
            elif query.lower() == "was the disputed amount greater than 5000 usd?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the disputed amount and perform a mathematical calculation to check if the disputed amount is greater than 5000 or not, given the context. Give a relevant and concise response.
                            Kindly do not provide any extra [Explanation, Note, Description] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response:(Provide a concise Response without any extra [Explanation, Note, Descricption] below the Response.) '''

                
            elif query.lower() == "what type of cards are involved?":
                prompt_1 = f''' You need to act as a Financial analyst to identify the type of Card and Card Network involved, given the context. On a higher level the card can be a Dedit, Crebit Card. VISA, MasterCard, American Express, Citi Group, etc. are the different brands with respect to a Credit Card or Debit Card . Give a relevant and concise response.
                            Do not provide any extra [Explanation, Note] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response:(Act like a professional and provide me a concise Response . Do not add any extra [Explanation, Note, Descricption] below the context.) '''

                
            elif query.lower() == "was the police report filed?":
                prompt_1 = f''' You need to act as a Financial analyst to identify if the police was reported of the Fraud activity, given the context. Give a relevant and concise response.
                            Do not provide any extra [Explanation, Note] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: (Provide a concise Response without any extra [Explanation, Note, Descricption] below the Response.)'''

            elif query.lower() == "is this a valid sar case?":
                prompt_1 =  f''' You are a Fraud Analyst.Check if there is evidence for this case to address as SAR or not. A SAR case is a case of financial Suspicious/Fraud Activity which can be observed given the context.
                            If there is any activity without the consent of the cardholder, also if there is a suspect who used the card without the consent.
                            Then we can address this as a valid SAR case.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response: (Provide a concise response in single sentence.Do not add prefix like ['Respone', 'based on the document']. Do not add any further Explanation,Note.)'''        
            
            
            elif query.lower() == "is there any evidence of a sar case?":
                prompt_1 = f''' You are a Fraud Analyst.Check if there is evidence for this case to address as SAR or not. A SAR case is a case of financial Suspicious/Fraud Activity which can be observed given the context.
                            If there is any activity without the consent of the cardholder, also if there is a suspect who used the card without the consent.
                            Then we can address this as a SAR case.Give a concise response with the suspect name. \n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\
                            Response:(Do not add prefix like ['Respone', 'based on the document']. Do not add any further Explanation,Note.) '''

                
            else:
                prompt_1 = f'''Act as a financial analyst and give concise answer to below Question as truthfully as possible, with given Context.
                            Do not provide any extra [Explanation, Note,Description] block below the Response.\n\n\
                            Question: {query}\n\
                            Context: {context_1}\n\                      
                            Response: (Act like a professional and provide me a concise Response . Do not add any extra [Explanation, Note, Descricption] below the Response.)'''


            #prompt = PromptTemplate(template=prompt, input_variables=["query", "context"])
            # response = usellm(prompt_1) #LLM_Response()
            response = llama_llm(llama_13b,prompt_1)
            text_dict[query] = response

            st.write(response)

            if response:
                df = pd.DataFrame(text_dict.items(), columns=['Question','Answer'])
            else:
                df = pd.DataFrame()

            st.session_state["tmp_table_llama"] = pd.concat([st.session_state.tmp_table_llama, df], ignore_index=True)
            st.session_state.tmp_table_llama.drop_duplicates(subset=['Question'])
            st.write(st.session_state.tmp_table_llama)
    
    return st.session_state["tmp_table_llama"], st.session_state["sara_recommendation_llama"]


def summarize_llama():
    with st.spinner('Summarization ...'):
        # if 'clicked4' not in st.session_state:
        #     st.session_state.clicked4 = False
        
        # def set_clicked4():
        #     st.session_state.clicked4 = True
        #     st.session_state.disabled = True

        st.markdown("""<span style="font-size: 24px; ">Summarize key findings of the case.</span>""", unsafe_allow_html=True)
        summ_llama = st.button("Summarize",disabled=st.session_state.disabled)
        if summ_llama:
            st.session_state.disabled=False
            template = """Write a detailed summary of the text provided.
            ```{text}```
            Response: (Return your response in a single paragraph.) """
            prompt = PromptTemplate(template=template,input_variables=["text"])
            llm_chain_llama = LLMChain(prompt=prompt,llm=llama_13b)

            summ_dict_llama = st.session_state.tmp_table_llama.set_index('Question')['Answer']
            text = []
            for key,value in summ_dict_llama.items():
                text.append(value)
            response_summ_llama = llm_chain_llama.run(text)
            response_summ_llama = response_summ_llama.replace("$", " ")
            response_summ_llama = response_summ_llama.replace("5,000", "5,000 USD")
            response_summ_llama = response_summ_llama.replace("5,600", "5,600 USD")
            st.session_state["tmp_summary_llama"] = response_summ_llama
            st.write(st.session_state["tmp_summary_llama"])
        
    return st.session_state["tmp_summary_llama"],summ_llama