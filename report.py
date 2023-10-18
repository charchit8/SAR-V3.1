from utils import *

@st.cache_data
def create_zip_file(file_paths, zip_file_name):
    with zipfile.ZipFile(zip_file_name, 'w') as zipf:
        for file_path in file_paths:
            zipf.write(file_path, os.path.basename(file_path))

def summ_table_report(tmp_table_llm,tmp_summary_llm):
    tmp_summary = []
    tmp_table = pd.DataFrame() 
    try:
        st.session_state.disabled=False
        tmp_summary.append(tmp_summary_llm)
        tmp_table = pd.concat([tmp_table, tmp_table_llm], ignore_index=True)
        tmp_table.drop_duplicates(inplace=True)
    except: 
        e = Exception("")
        st.exception(e)
    return tmp_summary, tmp_table


def save_report1(tmp_table,tmp_summary,sara_recommendation):
    try:
        # initiate the doc file
        doc = docx.Document()
        # doc.add_section(WD_SECTION.NEW_PAGE)
        doc.add_heading(f"Case No.: {st.session_state.case_num}",0)

        # Add a subheader for case details
        subheader_case = doc.add_paragraph("Case Details")
        subheader_case.style = "Heading 2"
        # Addition of case details
        paragraph = doc.add_paragraph(" ")
        case_info = {
            "Case Number                            ": " SAR-2023-24680",
            "Customer Name                       ": " John Brown",
            "Customer ID                              ": " 9659754",
            "Case open date                         ": " Feb 02, 2021",
            "Case Type                                  ": " Fraud Transaction",
            "Case Status                                ": " Open"
        }
        for key_c, value_c in case_info.items():
            doc.add_paragraph(f"{key_c}: {value_c}")
        paragraph = doc.add_paragraph(" ")

        # Add a subheader for customer info to the document ->>
        subheader_paragraph = doc.add_paragraph("Customer Information")
        subheader_paragraph.style = "Heading 2"
        paragraph = doc.add_paragraph(" ")

        # Add the customer information
        customer_info = {
            "Name                                           ": " John Brown",
            "Address                                      ": " 858 3rd Ave, Chula Vista, California, 91911 US",
            "Phone                                          ": " (619) 425-2972",
            "A/C No.                                        ": " 4587236908230087",
            "SSN                                               ": " 653-30-9562"
        }

        for key, value in customer_info.items():
            doc.add_paragraph(f"{key}: {value}")
        paragraph = doc.add_paragraph()
        # Add a subheader for Suspect infor to the document ->>
        subheader_paragraph = doc.add_paragraph("Suspect's Info")
        subheader_paragraph.style = "Heading 2"
        paragraph = doc.add_paragraph()
        #""" Addition of a checkbox where unticked box imply unavailability of suspect info"""

        # Add the customer information
        sent_val = "Suspect has been reported."
        paragraph = doc.add_paragraph()
        runner = paragraph.add_run(sent_val)
        runner.bold = True
        runner.italic = True
        suspect_info = {
            "Name                                             ": "Mike White",
            "Address                                        ": "520, WintergreenCt,Vancaville,CA,95587",
            "Phone                                             ": "NA",
            "SSN                                                 ": "NA",
            "Relationship with Customer  ": "NA"
        }

        for key, value in suspect_info.items():
            doc.add_paragraph(f"{key}: {value}")

        doc.add_heading('Summary', level=2)
        paragraph = doc.add_paragraph()
        doc.add_paragraph(tmp_summary)
        paragraph = doc.add_paragraph()
        doc.add_heading('Key Insights', level=2)
        paragraph = doc.add_paragraph()
        columns = list(tmp_table.columns)
        table = doc.add_table(rows=1, cols=len(columns), style="Table Grid")
        table.autofit = True
        for col in range(len(columns)):
            # set_cell_margins(table.cell(0, col), top=100, start=100, bottom=100, end=50) # set cell margin
            table.cell(0, col).text = columns[col]
        # doc.add_table(st.session_state.tmp_table.shape[0]+1, st.session_state.tmp_table.shape[1], style='Table Grid')
        
        for i, row in enumerate(tmp_table.itertuples()):
            table_row = table.add_row().cells # add new row to table
            for col in range(len(columns)): # iterate over each column in row and add text
                table_row[col].text = str(row[col+1]) # avoid index by adding col+1
        # save document
        # output_bytes = docx.Document.save(doc, 'output.docx')
        # st.download_button(label='Download Report', data=output_bytes, file_name='evidence.docx', mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        paragraph = doc.add_paragraph()
        paragraph = doc.add_paragraph()
        doc.add_heading('SARA Recommendation', level=2)
        doc.add_paragraph()       
        paragraph = doc.add_paragraph(sara_recommendation)         

        bio = io.BytesIO()
        doc.save(bio)
    except:
        e = Exception("")
        st.exception(e)

    return doc


def save_report2(tmp_table,tmp_summary,sara_recommendation):
    try:
        # initiate the doc file
        doc = docx.Document()
        # doc.add_section(WD_SECTION.NEW_PAGE)
        doc.add_heading(f"Case No.: {st.session_state.case_num}",0)

        # Add a subheader for case details
        subheader_case = doc.add_paragraph("Case Details")
        subheader_case.style = "Heading 2"
        # Addition of case details
        paragraph = doc.add_paragraph(" ")
        case_info = {
            "Case Number                            ": " SAR-2023-24680",
            "Customer Name                       ": " John Brown",
            "Customer ID                              ": " 9659754",
            "Case open date                         ": " Feb 02, 2021",
            "Case Type                                  ": " Fraud Transaction",
            "Case Status                                ": " Open"
        }
        for key_c, value_c in case_info.items():
            doc.add_paragraph(f"{key_c}: {value_c}")
        paragraph = doc.add_paragraph(" ")

        # Add a subheader for customer info to the document ->>
        subheader_paragraph = doc.add_paragraph("Customer Information")
        subheader_paragraph.style = "Heading 2"
        paragraph = doc.add_paragraph(" ")

        # Add the customer information
        customer_info = {
            "Name                                           ": " John Brown",
            "Address                                      ": " 858 3rd Ave, Chula Vista, California, 91911 US",
            "Phone                                          ": " (619) 425-2972",
            "A/C No.                                        ": " 4587236908230087",
            "SSN                                               ": " 653-30-9562"
        }

        for key, value in customer_info.items():
            doc.add_paragraph(f"{key}: {value}")
        paragraph = doc.add_paragraph()
        # Add a subheader for Suspect infor to the document ->>
        subheader_paragraph = doc.add_paragraph("Suspect's Info")
        subheader_paragraph.style = "Heading 2"
        paragraph = doc.add_paragraph()
        #""" Addition of a checkbox where unticked box imply unavailability of suspect info"""

        # Add the customer information
        sent_val = "Suspect has been reported."
        paragraph = doc.add_paragraph()
        runner = paragraph.add_run(sent_val)
        runner.bold = True
        runner.italic = True
        suspect_info = {
            "Name                                             ": "NA",
            "Address                                        ": "NA",
            "Phone                                             ": "NA",
            "SSN                                                 ": "NA",
            "Relationship with Customer  ": "NA"
        }

        for key, value in suspect_info.items():
            doc.add_paragraph(f"{key}: {value}")

        doc.add_heading('Summary', level=2)
        paragraph = doc.add_paragraph()
        doc.add_paragraph(tmp_summary)
        paragraph = doc.add_paragraph()
        doc.add_heading('Key Insights', level=2)
        paragraph = doc.add_paragraph()
        columns = list(tmp_table.columns)
        table = doc.add_table(rows=1, cols=len(columns), style="Table Grid")
        table.autofit = True
        for col in range(len(columns)):
            # set_cell_margins(table.cell(0, col), top=100, start=100, bottom=100, end=50) # set cell margin
            table.cell(0, col).text = columns[col]
        # doc.add_table(st.session_state.tmp_table.shape[0]+1, st.session_state.tmp_table.shape[1], style='Table Grid')
        
        for i, row in enumerate(tmp_table.itertuples()):
            table_row = table.add_row().cells # add new row to table
            for col in range(len(columns)): # iterate over each column in row and add text
                table_row[col].text = str(row[col+1]) # avoid index by adding col+1
        # save document
        # output_bytes = docx.Document.save(doc, 'output.docx')
        # st.download_button(label='Download Report', data=output_bytes, file_name='evidence.docx', mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document')

        paragraph = doc.add_paragraph()
        paragraph = doc.add_paragraph()
        doc.add_heading('SARA Recommendation', level=2)
        doc.add_paragraph()       
        paragraph = doc.add_paragraph(sara_recommendation)         

        bio = io.BytesIO()
        doc.save(bio)
    except:
        e = Exception("")
        st.exception(e)

    return doc
        

def download_report(doc,directory_path,fetched_files):
        # initiating a temp file
    tmp_dir = tempfile.mkdtemp()

    file_paths= []

    for uploaded_file in st.session_state.pdf_files:
        file_pth = os.path.join(tmp_dir, uploaded_file.name)
        with open(file_pth, "wb") as file_opn:
            file_opn.write(uploaded_file.getbuffer())
        file_paths.append(file_pth)

    for fetched_pdf in fetched_files:
        # st.write(fetched_pdf)
        file_pth = os.path.join(directory_path, fetched_pdf)
        # st.write(file_pth)
        file_paths.append(file_pth)

    
    combined_doc_path = os.path.join(tmp_dir, "report.docx")
    doc.save(combined_doc_path)



    # Create a zip file with the uploaded PDF files and the combined document
    zip_file_name = "package_files.zip"
    if file_paths:
        files =  [combined_doc_path] + file_paths
        create_zip_file(files, zip_file_name)
        # create_zip_file(file_paths, zip_file_name)
    else:
        pass

    
    # Download the package

    with open(zip_file_name, "rb") as file:
        st.download_button(
            label="Download Case Package", 
            data=file, 
            file_name=zip_file_name,
            disabled=st.session_state.disabled)


    # # Cleanup: Delete the temporary directory and its contents
    # for file_path in file_paths + [combined_doc_path]:
    #     os.remove(file_path)
    # os.rmdir(tmp_dir)

        