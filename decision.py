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
        # st.markdown("""<span style="font-size: 18px;">*Based on the following findings for the underlying case, under Bank Secrecy Act, it is recommended to file this case as a suspicious activity:*</span>""", unsafe_allow_html=True)
        # st.markdown("""<span style="font-size: 18px;">*1. Transaction amount is above the $5,000 value threshold*</span>""", unsafe_allow_html=True)
        # st.markdown("""<span style="font-size: 18px;">*2. There is an indication of suspicion with involvement of multiple individuals, mismatch of customer details on merchant invoice and identification of a potential suspect*.</span>""", unsafe_allow_html=True)           

        query = "Give your recommendation if SAR filling is required or not?"
        context_1 = docsearch.similarity_search(query, k=5)
        prompt = f'''Act as a financial analyst and give concise answer to the question, with given Context.\n\n\
        SAR is a document that financial institutions must file with the Financial Crimes Enforcement Network (FinCEN) based on the Bank Secrecy Act whenever there is a suspicious activity.\n\n\
        If The transaction/disputed amount > 5,000 USD value threshold, then check below points to make sure if it is a suspicious activity or not: 
        1. Details mentioned in Invoice doesnot matches the customer (Customer details can be identified from cardholder information).\n\n\
        2. A potential suspect is identified? \n\n\
        Even if transaction/disputed amount > 5,000 USD but no suspect is identified, then this cannot be considered as a suspicious activity and no SAR filling is required. \n\n\
        Based the above findings, identify if this can be considered as Suspicious Activity or not.\n\n\
        If transaction/disputed amount is < 5000 USD threshold and no suspect is identified, write your response as - There is no indication of suspicious activity.Therefore,no requirement to file SAR with FinCEN.\n\n\
                Question: {query}\n\
                Context: {context_1}\n\                      
                Response: (Based on your analysis give a concise response in pointers.Mention whom to file based on Bank Secrecy Act.)'''
            
            
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
        query = "Give your recommendation if SAR filling is required or not?"
        context_1 = docsearch.similarity_search(query, k=5)
        prompt = f'''Act as a financial analyst and give concise answer to the question, with given Context.\n\n\
        SAR refers to Suspicious activity Report, which is a document that financial institutions must file with the Financial Crimes Enforcement Network (FinCEN) based on the Bank Secrecy Act whenever there is a suspicious activity.\n\n\
        You need to act as a Financial analyst, to check below points to confirm this as a suspicious activity or not-
        1. Identify the disputed amount and perform a mathematical calculation to check if the disputed amount is greater than 5000 or not? If amount is < 5000 USD then there is no suspicious activity, else if amount is > 5000 USD,this can be considered as suspicious activity. 
        2. Identify multiple individual name in the context compare with the customer name (customer name can be identified from cardholder information). If details match then there is no suspicious activity, else if details donot match, this can be considered as suspicious activity.
        3. A potential suspect name is identified? Suspect is the Person who has committed the fraud with the Customer (customer is the cardholder).\n\n\
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





