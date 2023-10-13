from utils import *
from closed_source import *

#This is the embedding model
model_name = "thenlper/gte-small"
# model_name = "sentence-transformers/all-MiniLM-L6-v2"
# model_name = "hkunlp/instructor-large"


def decision_gpt(summ_gpt,temp_file_path):
    hf_embeddings = embed(model_name) 
    docs, docsearch = embedding_store(temp_file_path,hf_embeddings)   
      
    if summ_gpt:
         
        st.write("#### *SARA Recommendation*")
        
        query ="Is invoice is billed to cardholder or someone else?"
        contexts = docsearch.similarity_search(query, k=5) 
        prompt = f" You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
        cardholder's name,adress can be identified from cardholder information. Customer is the person who is the owner of the card, customer can also be referenced as the victim with home fraud has taken place.\n\n\
        Identify name and details mentioned in merchant invoice (Detials mentioned in invoice is of the person who made the transaction,it may be or may not be of the customer)\n\n\
        Compare both the details, if details mentioned in invoice matches the cardholder details, then invoice is billed to customer else it is billed to someone else who misued the card.\n\n\
            Context: {contexts}\n\
            Response (Give me a concise response.)"
        response_5 = usellm(prompt) 

        
        query ="Is there a mention of potential suspect?"
        contexts = docsearch.similarity_search(query, k=5) 
        prompt = f" You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
        Perform Name Enitity Recognition to identify the Suspect name as accurately as possible, given the context. Suspect is the Person who has committed the fraud with the Customer. Respond saying :The Suspect Name is not Present, if there is no suspect in the given context.\n\n\
            Context: {contexts}\n\
            Response (Give me a concise response.)"
        response_6 = usellm(prompt) 


        query ="Give your recommendation if SAR filling is required or not?"
        contexts = docsearch.similarity_search(query, k=5) 
        prompt = f" You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
        SAR refers to Suspicious activity Report, which is a document that financial institutions must file with the Financial Crimes Enforcement Network (FinCEN) based on the Bank Secrecy Act whenever there is a suspicious activity.\n\n\
        If The transaction/disputed amount > 5,000 USD value threshold, then check below points to make sure if it is a suspicious activity or not: \n\
        1. {response_5} analyse this response,if details matches or not? If matches then there is no suspicion else, it can be a suspicipos activity.\n\n\
        2. {response_6} analyse this response, if a potential suspect is identified or not? If identified then this can be a suspicious activity, else not.\n\n\
        If no suspicious activity is detected based on above mentioned points, write your response as - There is no indication of suspicious activity.Therefore,no requirement to file SAR with FinCEN.\n\n\
        Context: {contexts}\n\
        Response (Give me a concise response in few pointers.)"       
        
        response_sara_gpt = usellm(prompt) 
        response_sara_gpt = response_sara_gpt.replace("$", " ")
        response_sara_gpt = response_sara_gpt.replace("5,000", "5,000 USD")
        response_sara_gpt = response_sara_gpt.replace("5,600", "5,600 USD")

        st.markdown(f'''<em>{response_sara_gpt}</em>''',unsafe_allow_html=True)

        st.warning('Please carefully review the recommendation and case details before the final submission',icon="⚠️")

   
            
def decision_llama(summ_llama,temp_file_path):
    hf_embeddings = embed(model_name) 
    docs, docsearch = embedding_store(temp_file_path,hf_embeddings) 
    if summ_llama: 

        query ="Is invoice is billed to cardholder or someone else?"
        contexts = docsearch.similarity_search(query, k=5) 
        prompt = f" You are professional Fraud Analyst. Find answer to the questions as truthfully and in as detailed as possible as per given context only,\n\n\
        Identify cardholder's name,adress from cardholder information. Customer is the person who is the owner of the card.\n\n\
        Identify name and address to whom merchant invoice is billed \n\n\
        Identify if Invoice is billed to cardholder or someone else based on above information. \n\n\
            Context: {contexts}\n\
            Response (Give me a concise response.)"
        response_7 = llama_llm(llama_13b,prompt) 


            
        query = "What is the suspect's name?"
        context_1 = docsearch.similarity_search(query, k=5)
        prompt_1 =  f'''Act as a professional fraud analyst.You need to check the document and compare if any name discrepencies are present that points towards the suspect who used the card without the consent of the cardholder.
                    Perform Name Enitity Recognition to identify the Suspect Name as accurately as possible, given the context.Suspect is the person who has committed the fraud with the customer/cardholder. If suspect name is not present, respond saying: Suspect name is not mentioned.\n\n\
                    Context: {context_1}\n\
                    Response: (Give a short response in a single sentence.Do not give me any Explanation or Note)'''
        response_8 = llama_llm(llama_13b,prompt_1) 

        query = "Is SAR filling is required or not?"
        context_1 = docsearch.similarity_search(query, k=5)
        prompt = f'''Act as a financial analyst and give concise answer to the question, with given Context.\n\n\
        SAR refers to Suspicious activity Report, which is a document that financial institutions must file with the Financial Crimes Enforcement Network (FinCEN) based on the Bank Secrecy Act whenever there is a suspicious activity.\n\n\
        If The transaction/disputed amount > 5,000 USD value threshold, then check below points to make sure if it is a suspicious activity or not: \n\
        1. {response_7} analyse this response,if invoice is billed to cardholder then there is no suspicion else, it can be a suspicious activity. (kindly mention the mismatched details in your response).\n\n\
        2. {response_8} analyse this response,If a potential suspect is identified then this can be a suspicious activity, else it is not a suspicious activity.\n\n\
        If no suspicious activity is detected based on above mentioned points, write your response as - There is no indication of suspicious activity.Therefore,no requirement to file SAR with FinCEN.\n\n\
                Question: {query}\n\
                Context: {context_1}\n\                      
                Response: (Give me a concise response in points.)'''
                
                
        response_sara_llama = llama_llm(llama_13b,prompt)
        response_sara_llama = response_sara_llama.replace("$", " ")
        response_sara_llama = response_sara_llama.replace("5,000", "5,000 USD")
        response_sara_llama = response_sara_llama.replace("5,600", "5,600 USD")
        
       
        st.markdown(f'''<em>{response_sara_llama}</em>''',unsafe_allow_html=True)

        st.warning('Please carefully review the recommendation and case details before the final submission',icon="⚠️")

def selection1(summ):  
    if summ: 
        selected_rad = st.radio(":blue", ["Yes", "No", "Refer for review"], horizontal=True,disabled=st.session_state.disabled)
        if selected_rad == "Refer for review":
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            email_id = st.text_input("Enter email ID")
            if email_id and not re.match(email_regex, email_id):
                st.error("Please enter a valid email ID")


        if st.button("Submit"):
            if selected_rad in ("Yes"):
                st.warning("Thanks for your review, your response has been submitted")
            elif selected_rad in ("No"):
                st.success("Thanks for your review, your response has been submitted")

            else:
                st.info("Thanks for your review, Case has been assigned to the next reviewer")


def selection2(summ):
    if summ:       
        selected_rad = st.radio(":blue", ["No", "Yes", "Refer for review"], horizontal=True,disabled=st.session_state.disabled)
        if selected_rad == "Refer for review":
            email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            email_id = st.text_input("Enter email ID")
            if email_id and not re.match(email_regex, email_id):
                st.error("Please enter a valid email ID")


        if st.button("Submit"):
            if selected_rad in ("Yes"):
                st.warning("Thanks for your review, your response has been submitted")
            elif selected_rad in ("No"):
                st.success("Thanks for your review, your response has been submitted")
            else:
                st.info("Thanks for your review, Case has been assigned to the next reviewer")





