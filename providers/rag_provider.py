from langchain_openai.embeddings import AzureOpenAIEmbeddings
import pinecone
from langchain.vectorstores import Pinecone
from langchain_openai import AzureChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser
from langchain_core.runnables import RunnableParallel
from dependencies.config import Settings


def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)


def query_rag(input, settings: Settings):

    pc = pinecone.Pinecone(api_key=settings.pinecone_api_key)
    index_name = "beevify-mvp"
    index = pc.Index(index_name)
    embed = AzureOpenAIEmbeddings(
        api_key=settings.azure_openai_embeddings_api_key,
        base_url=settings.azure_openai_embeddings_host_url,
    )
    vectorstore = Pinecone(
        index, embed.embed_query, "content", namespace="dev"
    )

    template = """You are an assistant for question-answering tasks. 
        Use the following pieces of retrieved context to answer the question. 
        If you don't know the answer, just say that you don't know. 
        Use three sentences maximum and keep the answer concise, also
        include the title of the sources you are extracting the response.
        Question: {question} 
        Context: {context} 
        Answer:
        """
    prompt = ChatPromptTemplate.from_template(template)

    retriever = vectorstore.as_retriever()
    print("antes de crear el azurechatopenai")
    llm = AzureChatOpenAI(
        api_key=settings.azure_openai_gpt4omini_api_key,
        base_url=settings.azure_openai_gpt4omini_host_url,
        api_version="2024-08-01-preview",
        temperature=0.0,
    )
    print("despu'es de crear el azurechatopenai")

    rag_chain = (
        RunnablePassthrough.assign(context=(lambda x: format_docs(x["context"])))
        | prompt 
        | llm
        | StrOutputParser() 
    )

    rag_chain_with_source = RunnableParallel(
        {"context": retriever, "question": RunnablePassthrough()}
    ).assign(answer=rag_chain)

    print("antes de llamar el rag")
    return rag_chain_with_source.invoke(input)


