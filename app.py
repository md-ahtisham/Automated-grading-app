import streamlit as st
import pdfplumber 
import pathlib
import textwrap

import google.generativeai as genai
import os
from IPython.display import display
from IPython.display import Markdown



st.set_page_config(page_title="My Webpage", page_icon=":tada:", layout="wide")

with st.container():
    st. subheader ("Hi , Wanna check your answer sheet :wave:")
    st.markdown("# :rainbow[Automated grading app ]")
    st.write("upload your answer sheel here and get your analytical report ")

st.sidebar.success("select")



def extract_text_from_pdf(file):
    # Open the PDF file
    text=""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"  # Add a newline character to separate pages

        return text



def evaluate_and_score(extracted_text):
            questions_and_answers = extracted_text.strip().split('\n\n')  # Split at double newlines for questions and answers

            print("Questions and Answers Parsed:")
            for q_and_a in questions_and_answers:
                print(q_and_a.strip())
            return questions_and_answers


def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))


file = st.file_uploader("Uploade your answe sheet pdf here", type=["pdf"])

if file is not None:

    extracted_text = extract_text_from_pdf(file)
    st.text_area("Extracted Text", extracted_text, height=300)
    if st.button("Evaluate and Score"):
       
        
        parsed_questions_and_answers = evaluate_and_score(extracted_text)


        os.environ['GOOGLE_API_KEY']="AIzaSyAuurUeeTVzmZmKCQeOqG94jqlMILSooMY"
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])
        model = genai.GenerativeModel('gemini-1.5-pro')
        response = model.generate_content(f"Is the following answer correct?\n\nQuestion: {parsed_questions_and_answers}\n\nAnswer with only 'Yes' or 'No' for each question in parsed_questions_and_answers.")
        to_markdown(response.text)


        lol = response.text
        
        responses = lol.split('\n')

        total_yes = responses.count("Yes")
        total_no = responses.count("No")
        total = total_yes + total_no
        score = total_yes

        for response in responses:
            if "Yes" in response:
                total_yes += 1
            elif "No" in response:
                total_no += 1

        total = total_yes + total_no
        score = total_yes

        st.write(f"Total: {total}, Score: {score}")
        
        # Data for the pie chart
        
       
        st. subheader ("worng question in your answersheet")



        response2 = model.generate_content(f" extract only the worng answers and corresponding question from the following questions and answers from {parsed_questions_and_answers} , it has to be easy to read formate & don't give it  coorect answer")
        to_markdown(response2.text)
        lal=response2.text
        st.text_area(lal)



        st. subheader ("A.I -powered Assistance")
        
        response3= model.generate_content(f" make step by step solution of each incorrected answers{lal}")
        to_markdown(response2.text)
        lel=response3.text
        st.text_area(lel)






    
