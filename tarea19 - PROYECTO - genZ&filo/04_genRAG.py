import os
import time

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings 
from langchain_chroma import Chroma
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

def main():
    # Limpiar pantalla inicial
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("--------------------------------------------------")
    print(" RAG PROYECTO 3: GEN Z")
    print("--------------------------------------------------")
    
    # 1. CARGAR DATOS
    print("buscando la data en la carpeta...")
    if not os.path.exists('./archivos'):
        print("f, no encontre la carpeta archivos. checa si ya corriste el script anterior")
        return

    class UTF8TextLoader(TextLoader):
        def __init__(self, file_path: str, **kwargs):
            super().__init__(file_path, **kwargs, encoding="utf-8")

    loader = DirectoryLoader('./archivos', glob="*.txt", loader_cls=UTF8TextLoader)

    documents = loader.load()
    print(f"listo, se subieron {len(documents)} documentos")

    # 2. PREPARAR TEXTO
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)

    # 3. CREAR BASE DE DATOS (EMBEDDINGS)
    print("procesando los vectores, dame un segundo...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    db = Chroma.from_documents(texts, embeddings)
    retriever = db.as_retriever(search_kwargs={"k": 4}) 

    # 4. CONECTAR LLM
    print("conectando con ollama, el llama 3.2 ya esta activo...")
    llm = ChatOllama(model="llama3.2:1b", temperature=0.3, keep_alive="1h")

    # 5. CREAR LA TUBERÍA (CHAIN)
    template = """Eres un filósofo de la era digital. Tu vibra es analítica, madura y con un toque de frescura Gen Z. 

    ### MANDATO CRÍTICO:
    Tu conocimiento del mundo está LIMITADO ÚNICAMENTE al 'Contexto' proporcionado abajo. 
    No puedes usar tus propios conocimientos previos, aunque sepas la respuesta.

    ### PROTOCOLO DE RESPUESTA:
    1. Si la información NO está en el contexto:
    Responde únicamente: "Ese dato no ha cruzado mi radar todavía, la vdd." y NO añadidas nada más.
    
    2. Si la información SÍ está en el contexto:
    - Analiza con profundidad pero con lenguaje directo.
    - Usa comillas para citar frases literales de los datos.
    - Conecta los puntos como un observador de la cultura.

    ---
    CONTEXTO:
    {context}
    ---

    PREGUNTA:
    {question}

    INTERPRETACIÓN FILOSÓFICA:"""
    
    prompt = ChatPromptTemplate.from_template(template)

    def format_docs(docs):
        return "\n\n".join([d.page_content for d in docs])

    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )

    print("todo bien, ya puedes preguntar lo que quieras")
    print("escribe 'salir' o 'exit' cuando termines\n")

    # --- BUCLE DE CHAT ---
    while True:
        try:
            pregunta = input("dime algo > ")
            
            if pregunta.lower() in ['salir', 'exit', 'adios', 'bye']:
                print("\nnos vemos, cerrando todo")
                break
            
            if not pregunta.strip():
                continue

            print("pensando...", end="\r")
            
            inicio = time.time()
            respuesta = rag_chain.invoke(pregunta)
            tiempo = time.time() - inicio
            
            print(f"lo que encontre ({tiempo:.1f}s):")
            print(f"{respuesta}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nbye, saliste del programa")
            break
        except Exception as e:
            print(f"hubo un error: {e}")

if __name__ == "__main__":
    main()