from utils import *

if "pdf_files" not in st.session_state:
    st.session_state.pdf_files = ''


# To convert generated to pdf and save in temp direc.
def create_pdf(text,file_name,tmp_dir_,temp_file_path):
    # Create a new FPDF object
    pdf = FPDF()
    # Add a new page to the PDF
    pdf.add_page()
    # Set the font and font size
    pdf.set_font('Arial', size=12)
    pdf.cell(200, 10, txt=text.encode('utf-8').decode('latin-1'), ln = 1, align = 'C')
    # Write the text to the PDF
    # pdf.write(text.encode('utf-8').decode('latin-1'), ln = 1, align = 'C')
    # Save the PDF
    pdf.output(os.path.join(tmp_dir_,file_name))
    file_pth = os.path.join(tmp_dir_,file_name)
    temp_file_path.append(file_pth)


def data_display(directory_path,fetched_files):
    
    # reading files from local directory from fetch evidence button

    bt1_up, bt2_up = st.tabs(["Fetch Evidence", "Upload Evidence"])

    with bt1_up:
        # Set the color
        # st.markdown(
        #     """
        #     <div style="display: flex; justify-content: center; align-items: center; height: 48px; border: 1px solid #ccc; border-radius: 5px; background-color: #f2f2f2;">
        #         <span style="font-size: 16px;  ">Fetch Evidence</span>
        #     </div>
        #     """,
        #     unsafe_allow_html=True
        # )
        if 'clicked' not in st.session_state:
            st.session_state.clicked = False
        
        def set_clicked():
            st.session_state.clicked = True
            st.session_state.disabled = True
        st.write("") #for the gap
        st.button('Fetch Evidence', on_click=set_clicked)

        if st.session_state.clicked:
            # st.write("Evidence Files:") 
            # st.markdown(html_str, unsafe_allow_html=True)
            
            # Showing files
            # show_files = fetched_files.copy()
            # show_files = show_files + ['Other.pdf']
            # files_frame = pd.DataFrame(show_files, columns=["File Name"])
            # # files_frame["Select"] = [True for _ in range(len(files_frame))]
            # files_frame = files_frame.reset_index(drop=True)

            # # Add checkboxes to the DataFrame
            # df_with_checkboxes = add_checkboxes_to_dataframe(files_frame)
            
            # # Iterate through each row and add checkboxes
            # for index, row in df_with_checkboxes.iterrows():
            #     if index < len(df_with_checkboxes) - 1:
            #         checkbox_state = st.checkbox(f" {row['File Name']}", value=True)
            #         df_with_checkboxes.loc[index, 'Select'] = checkbox_state
            #     else:
            #         st.checkbox(f"{row['File Name']}", value=False)



            # st.dataframe(files_frame)
            # st.write(df_reset.to_html(index=False), unsafe_allow_html=True)
            # st.markdown(files_frame.style.hide(axis="index").to_html(), unsafe_allow_html=True)
            
            
            
            #select box to select file
            selected_file_name = st.selectbox(":blue[Select a file to View]",fetched_files)
            st.write("Selected File: ", selected_file_name)
            st.session_state.disabled = False
            file_ext = tuple("pdf")
            if selected_file_name.endswith(file_ext):
                selected_file_path = os.path.join(directory_path, selected_file_name)
                #converting pdf data to bytes so that render_pdf_as_images could read it
                file = pdf_to_bytes(selected_file_path)
                pdf_images = render_pdf_as_images(file)
                #showing content of the pdf
                st.subheader(f"Contents of {selected_file_name}")
                for img_bytes in pdf_images:
                    st.image(img_bytes, use_column_width=True)
            else:
                selected_file_path = os.path.join(directory_path, selected_file_name)
                # This is showing png,jpeg files
                st.image(selected_file_path, use_column_width=True)



    with bt2_up:
        pdf_file = st.file_uploader("", type=["pdf","png","jpeg","docx","xlsx"], accept_multiple_files=True)
        st.session_state.pdf_files = pdf_file
        # showing files
        for uploaded_file in pdf_file:
            #This code is to show pdf files
            file_ext = tuple("pdf")
            if uploaded_file.name.endswith(file_ext):
                # Show uploaded files in a dropdown
                # if pdf_files:
                st.subheader("Uploaded Files")
                file_names = [file.name for file in pdf_file]
                selected_file = st.selectbox(":blue[Select a file]", file_names)
                # Enabling the button
                st.session_state.disabled = False
                # Display selected PDF contents
                if selected_file:
                    selected_pdf = [pdf for pdf in pdf_file if pdf.name == selected_file][0]
                    pdf_images = render_pdf_as_images(selected_pdf)
                    st.subheader(f"Contents of {selected_file}")
                    for img_bytes in pdf_images:
                        st.image(img_bytes, use_column_width=True)

            else:
                # This is showing png,jpeg files
                st.image(uploaded_file, use_column_width=True)





def create_temp_file(directory_path,fetched_files):

    #creating temp directory to have all the files at one place for accessing
    tmp_dir_ = tempfile.mkdtemp()
    temp_file_path= []

    for fetched_pdf in fetched_files:
        file_ext = tuple("pdf")
        if fetched_pdf.endswith(file_ext):
            file_pth = os.path.join(directory_path, fetched_pdf)
            # st.write(file_pth)
            temp_file_path.append(file_pth) 
        else:
            pass   
 

    for uploaded_file in st.session_state.pdf_files:
        file_ext = tuple("pdf")
        if uploaded_file.name.endswith(file_ext):
            file_pth = os.path.join(tmp_dir_, uploaded_file.name)
            with open(file_pth, "wb") as file_opn:
                file_opn.write(uploaded_file.getbuffer())
                temp_file_path.append(file_pth)
        else:
            pass
    
    return temp_file_path





def pytesseract_code(directory_path,fetched_files):

    tmp_dir_ = tempfile.mkdtemp()
    temp_file_path= []

    # Pytesseract code 
    #file path for uploaded files
    file_pth = []
    for uploaded_file in st.session_state.pdf_files:
        file_ext1 = tuple("pdf")
        file_ext2 = tuple(["png","jpeg"])
        if uploaded_file.name.endswith(file_ext1):
            file_pth_= os.path.join(tmp_dir_, uploaded_file.name)
            with open(file_pth_, "wb") as file_opn:
                file_opn.write(uploaded_file.getbuffer())
                file_pth.append(file_opn)
        elif uploaded_file.name.endswith(file_ext2):
            file_pth_= os.path.join(tmp_dir_, uploaded_file.name)
            file_pth.append(file_pth_)
        else:
            pass



    # For uploaded files
    for file in file_pth:
        st.write(file.name)
        file_ext1 = tuple("pdf")
        file_ext2 = tuple(["png","jpeg"])
        if file.endswith(file_ext1):
            if is_searchable_pdf(file)==False:
                text = convert_scanned_pdf_to_searchable_pdf(file)
                create_pdf(text,'uploaded_file.pdf')
            else:
                with open(file, "wb") as file_opn:
                    file_opn.write(file.getbuffer())
                    temp_file_path.append(file_opn)           
        elif file.endswith(file_ext2):
            text = convert_image_to_searchable_pdf(file)
            create_pdf(text,'uploaded_file.pdf') 
        else:
            pass          
    
    
    #for fetched files
    for fetched_pdf in fetched_files:
        file_ext1 = tuple("pdf")
        file_ext2 = tuple(["png","jpeg"])
        if fetched_pdf.endswith(file_ext1):
            selected_file_path = os.path.join(directory_path, fetched_pdf)
            if is_searchable_pdf(selected_file_path)==False:
                text = convert_scanned_pdf_to_searchable_pdf(selected_file_path)
                file_name = os.path.basename(selected_file_path)
                split_name = file_name.split('.')
                create_pdf(text,f'{split_name[0]}.pdf')
            else:
                file_pth = os.path.join(directory_path, fetched_pdf)
                temp_file_path.append(file_pth)
        elif fetched_pdf.endswith(file_ext2):
            selected_file_path = os.path.join(directory_path, fetched_pdf)
            text = convert_image_to_searchable_pdf(selected_file_path)
            file_name = os.path.basename(selected_file_path)
            split_name = file_name.split('.')
            create_pdf(text,f'{split_name[0]}.pdf')

        else:
            pass

    return temp_file_path
    

    


