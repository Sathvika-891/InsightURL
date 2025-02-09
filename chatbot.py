from langchain_together import ChatTogether
from langchain_huggingface.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_chroma import Chroma
from dotenv import load_dotenv
from prompt import get_prompt_template
import os
from uuid import uuid4
import requests
from urllib.parse import urlparse
import hashlib

load_dotenv()
os.environ["TOGETHER_API_KEY"]=os.environ.get("TOGETHER_API_KEY")
os.environ["HUGGINGFACE_ACCESS_TOKEN"]=os.environ.get("HUGGINGFACE_ACCESS_TOKEN")

class Chatbot:
    def __init__(self):
        self.session_id = str(uuid4())
        self.text_splitter = CharacterTextSplitter(
            separator="n",chunk_size=1000,chunk_overlap=300
        )
        print("loading llm")
        self.llm = ChatTogether(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            together_api_key=os.environ.get("TOGETHER_API_KEY")
        )
        print("loading embeddings")
        self.embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-m3"
        )
        print("embeddings are loaded")
        self.db = None
        self.prompt = get_prompt_template()

    def get_persist_directory(self, urls):
       
        sorted_urls = sorted(urls)
        urls_string = "".join(sorted_urls)
        urls_hash = hashlib.md5(urls_string.encode()).hexdigest()[:10]
        persist_dir = f"chromadb_{urls_hash}"
        os.makedirs("chromadb", exist_ok=True)
        return os.path.join("chromadb", persist_dir)

    def validate_url(self, url):
        try:
            result = urlparse(url)
            if not all([result.scheme, result.netloc]):
                return False
            response = requests.head(url, timeout=5)
            return response.status_code == 200
        except:
            return False

    def load_urls(self, urls):
        valid_urls = []
        invalid_urls = []
        
        for url in urls:
            if self.validate_url(url):
                valid_urls.append(url)
            else:
                invalid_urls.append(url)
        
        if not valid_urls:
            return {"error": "No valid URLs provided", "invalid_urls": invalid_urls}
            
        try:
            print("loading documents")
            loader = UnstructuredURLLoader(urls=valid_urls)
            data = loader.load()
            docs = self.text_splitter.split_documents(data)
            return {"success": True, "docs": docs, "invalid_urls": invalid_urls}
        except Exception as e:
            return {"error": f"Error loading URLs: {str(e)}", "invalid_urls": invalid_urls}

    def get_vectorstore(self, urls):
        try:
            persist_directory = self.get_persist_directory(urls)
            
            if self.db is None:
                self.db = Chroma(
                    embedding_function=self.embeddings,
                    persist_directory=persist_directory
                )
                print(f"loaded from persist dir: {persist_directory}")
            
            if len(self.db.get()["documents"]) == 0:
                print("adding docs")
                result = self.load_urls(urls)
                if "error" in result:
                    return result
                self.db.add_documents(result["docs"])
            return {"success": True, "invalid_urls": result.get("invalid_urls", [])}
        except Exception as e:
            return {"error": f"Error in vectorstore: {str(e)}"}

    def generate_response(self, query, urls):
        if self.db is None:
            result = self.get_vectorstore(urls)
            if "error" in result:
                yield f"Error: {result['error']}"
                return
        try:
            relevant_documents = self.db.similarity_search(query=query, k=5)
            formatted_Query = self.prompt.format(query=query, relevant_docs=relevant_documents)
            
            for chunk in self.llm.stream(formatted_Query):
                yield str(chunk.content)
        except Exception as e:
            yield f"Error generating response: {str(e)}"