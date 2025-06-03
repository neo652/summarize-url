import os
import validators
import streamlit as st
from dotenv import load_dotenv
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import UnstructuredURLLoader


## sstreamlit APP
st.set_page_config(page_title="Summarize Text From Website", page_icon="🦜")
st.title("Summarize Text From Website")
st.subheader('Summarize URL')



## Get the Groq API Key and url(website)to be summarized
# Get API key from environment or user input
with st.sidebar:
    default_api_key = os.getenv("GROQ_API_KEY", "")
    groq_api_key = st.text_input("Groq API Key", 
                                value=default_api_key, 
                                type="password",
                                help="Enter your API key or use the one from .env file")

generic_url=st.text_input("URL",label_visibility="collapsed")

## Gemma Model USsing Groq API
llm =ChatGroq(model="Gemma2-9b-It", groq_api_key=groq_api_key)

prompt_template="""
Provide a summary of the following content in 300 words:
Content:{text}

"""
prompt=PromptTemplate(template=prompt_template,input_variables=["text"])

if st.button("Summarize the Content Website"):
    ## Validate all the inputs
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. It should be a website url")

    else:
        try:
            with st.spinner("Waiting..."):
                ## loading the website data
                loader = UnstructuredURLLoader(
                    urls=[generic_url],
                    ssl_verify=False,
                    headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"}
                )
                docs = loader.load()

                ## Chain For Summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.invoke(docs)

                 # Display summary
                summary = output_summary.get("output_text", str(output_summary))
                if summary.strip() and "Please provide the content" not in summary:
                    st.success(summary)
                else:
                    st.error("Could not generate a proper summary from the content.")
        except Exception as e:
            st.exception(f"Exception:{e}")
                    
