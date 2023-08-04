import streamlit as st
import os
from langchain.document_loaders import YoutubeLoader
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import OpenAIEmbeddings, HuggingFaceInstructEmbeddings
from langchain.vectorstores import FAISS
from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from htmlTemplates import css, bot_template, user_template
from langchain.llms import HuggingFaceHub
from io import StringIO
import tempfile
from langchain.prompts.prompt import PromptTemplate
from langchain.chains import LLMChain
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)


api_key = os.environ['OPENAI_API_KEY']

def handle_userinput(user_question):

    if st.session_state.chat_history is None:
        st.session_state.chat_history = []

    response = st.session_state.conversation({'question': user_question})
    st.session_state.chat_history = response['chat_history']

    for i, message in enumerate(st.session_state.chat_history):
        if i % 2 == 0:
            st.write(user_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)
        else:
            st.write(bot_template.replace(
                "{{MSG}}", message.content), unsafe_allow_html=True)


def create_db(video_url):
    
    loader = YoutubeLoader.from_youtube_url(video_url)

    transcript = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(transcript)

    embeddings = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(docs, embeddings)

    return vectorstore


def get_conversation_chain(vectorstore, user_question):

    qa_template = """
You are Andrew Tate, a confident and outspoken individual with a high level of openness, conscientiousness, and assertiveness. As you provide advice based on the video interview or context, remember to focus on important and big picture ideas, exuding optimism and intellectual prowess. Emphasize the value of industriousness, discipline, and seeking achievements to help individuals reach their full potential.

Be straightforward and unafraid of confrontation, reflecting your low agreeableness trait. Encourage people to speak their minds, stand by their beliefs, and not be deterred by potential offense. Remind them that being assertive and vocal is essential in making their voices heard.

Though some have accused you of being a narcissist, clarify that your outspoken nature is driven by a desire to share your knowledge and convictions, not merely seeking attention. Reiterate the importance of staying true to oneself without relying on controversy for recognition.

In addressing daily concerns, remember to highlight the significance of remaining calm and composed under pressure, drawing from your low neuroticism trait. Encourage practical problem-solving and forward-thinking approaches, inspiring individuals to stay focused on their goals and not succumb to anxiety or self-doubt.

As you embody the personality traits of Andrew Tate, always aim to inspire and motivate others to lead successful and fulfilling lives. Your candid advice and belief in personal growth will guide them to become the best versions of themselves.
        Context: {context}
     
        Question: {question}
        """
    messages = [
        SystemMessagePromptTemplate.from_template(qa_template)
        ]
        
    QA_PROMPT = ChatPromptTemplate.from_messages(messages)

    #QA_PROMPT = PromptTemplate(template=qa_template)
    #QA_PROMPT = PromptTemplate(template=qa_template, input_variables=["context","question" ])

   
    llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.2)

    param_similarity=dict(k=3,search_type="similarity")
    retriever = vectorstore.as_retriever(search_kwargs=param_similarity)

    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    
    chain = ConversationalRetrievalChain.from_llm(llm=llm,
    retriever=retriever, verbose=True, return_source_documents=False, memory = memory,
      max_tokens_limit=4097, combine_docs_chain_kwargs={'prompt': QA_PROMPT})
    
    #chain_input = {'chat_history': st.session_state["chat_history"], 'question': user_question}

    #result = chain({'chat_history': st.session_state["chat_history"], 'question': user_question}, return_only_outputs=True)

    return chain

def main():
   
    st.set_page_config(page_title="Andrew Tate Chatbot",
                       page_icon=":bust_in_silhouette:",
                       layout="centered",
                    )
    st.write(css, unsafe_allow_html=True)


    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    

    st.markdown(
        """
        <style>
        body {
            background-image: url('https://media.discordapp.net/attachments/991481596182020177/1136461314156417155/tacticalblob_flat_website_header_design_massive_treasure_pile_k_59ba54cd-ea1b-46f8-aca2-c51d5f4ebbb0.png?width=993&height=662');
            background-size: cover;
        }
        .stApp {
            max-width: 1000px;
        }
        .stTextInput > div > input {
            border-radius: 25px;
            border-color: #e0e0e0;
            font-size: 18px;
            padding: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.header("Welcome to Andrew Tate's Motivational Chatbot :muscle:")

    st.write(
        """
        The Andrew Tate Chatbot is your personal motivational coach. 
        Ask any question, and the chatbot will provide you with valuable life advice 
        in Andrew Tate's unique style, empowering you to overcome challenges and achieve greatness. 
        """
    )

    user_question = st.text_input("What worries you today?")
    if user_question:
        handle_userinput(user_question)

    video_url = 'https://www.youtube.com/watch?v=d9_YWu9WAvg'
    # create vector store
    vectorstore = create_db(video_url)

    # create conversation chain
    st.session_state.conversation = get_conversation_chain(
    vectorstore, user_question)


if __name__ == '__main__':
    main()