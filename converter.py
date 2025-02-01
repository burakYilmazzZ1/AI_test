!pip install openai==0.27.0
!pip install PyPDF2 gradio
import os
import openai

openai.api_key = "----"
# API can be stored using environment(.env)
import PyPDF2
from google.colab import files


def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text = ''
        for page in reader.pages:
            text += page.extract_text()
    return text

def split_text_into_chunks(text, max_chunk_size=1000):
    words = text.split()
    for i in range(0, len(words), max_chunk_size):
        yield ' '.join(words[i:i + max_chunk_size])

def transform_text_to_lecture(input_text):
    prompt = (
        "Transform the following casual conversation into a comprehensive and highly detailed lecture. Start with a well-structured introduction that outlines the importance of the topic and provides a roadmap for the lecture."
        "Explain why this topic is important in both historical and contemporary contexts, ensuring the introduction sets a clear tone for the lecture."
        "Include engaging opening questions or facts to capture attention."
        "For the body of the lecture, provide highly detailed explanations and break the content into logically sequenced sections and subsections."
        "Incorporate expert opinions, research findings, or key studies where applicable."
        "For each key concept, provide practical examples and real-world applications. These examples should be relatable and demonstrate how the concept works in practice."
        "Include at least two detailed case studies to illustrate the topic's relevance in different contexts (e.g., industry, academia, or society)."
        "Provide discussion prompts for students to analyze these case studies critically."
        "For every section, include three to five thought-provoking questions designed to encourage deeper understanding and engagement."
        "Questions should range from simple comprehension checks to complex analytical problems that require critical thinking."
        "At the end of each section, provide a concise summary of the key takeaways and relate them to the overall theme of the lecture."
        "Include a discussion prompt that connects the section to future implications or broader topics."
        "Create a dedicated section for frequently asked questions. Address at least five potential student questions with clear, in-depth explanations."
        "Include questions that clarify common points of confusion or address the practical use of the concepts discussed."
        "Conclude the lecture by summarizing all sections and showing how they tie together."
        "Include recommendations for further exploration, such as books, research papers, online courses, or tools that students can use to deepen their understanding."
        "End with a forward-looking statement about future trends or innovations related to the topic."
        "Ensure the lecture is between 4500 and 9000 words, with a preference for the upper range. Each section should be expanded with detailed analysis, examples, and references where appropriate."
    )

    lectures = []
    for chunk in split_text_into_chunks(input_text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an expert lecturer, skilled in creating detailed, structured, and engaging lectures with examples, case studies, and discussion prompts to enhance learning."},
                {"role": "user", "content": f"{prompt}\n\n{chunk}"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        lectures.append(response.choices[0].message['content'].strip())

    return "\n\n".join(lectures)

def upload_pdf_and_generate_lecture():
    uploaded = files.upload()

    pdf_path = next(iter(uploaded))

    text = extract_text_from_pdf(pdf_path)

    structured_lecture = transform_text_to_lecture(text)

    print(structured_lecture)

upload_pdf_and_generate_lecture()