from langchain_ollama import OllamaLLM # type: ignore
from langchain_core.prompts import ChatPromptTemplate # type: ignore
from langchain_community.document_loaders.pdf import PyPDFLoader  # type: ignore
from langchain_chroma import Chroma # type: ignore
from langchain_community.embeddings.ollama import OllamaEmbeddings # type: ignore
from tkinter import *
from tkinter import filedialog 
from tkinter import ttk

#Ai prompting set-up
template = """
Context: {history}

Question: {question}

Answer the question using the context
"""
history = ""
prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="gemma2:2b")
chain = prompt | model

#Used for when pdfs are used 
embedTemplate = """
"Answer the question using the following information: {result}
Question: {userInput}"
"""
embedPrompt = ChatPromptTemplate.from_template(embedTemplate)
embedChain = embedPrompt | model

#Set up embedding database
embedding_model = OllamaEmbeddings(model="mxbai-embed-large")
vectorDB = Chroma(embedding_function=embedding_model)

#Loads a PDF into the embeddings database
def loadDocuments():
    global history
    path = filedialog.askopenfilename(
        title="Select a PDF file",
        filetypes=[("PDF files", "*.pdf")])
    loader = PyPDFLoader(path)
    docs = loader.load_and_split() 
    vectorDB.add_texts([doc.page_content for doc in docs])
    history += "\n User uploaded a PDF"
    changeTextBox(history)

#Handles the AI prompting. Args is needed as it is passed in when bind is used.
def handleConversation(*args): 
    global history
    enterButton.state(['disabled'])  # prevent spamming
    userInput = prompt.get()
    prompt.set('')
    if pdfMode.get():
        results = vectorDB.similarity_search(userInput)
        aiOutput = embedChain.invoke({"result": results, "userInput": userInput})
    else:
        aiOutput = chain.invoke({"history": history, "question": userInput})
    history += "\n User: "+ userInput+" \n AI: " + aiOutput
    changeTextBox(history)

#Changes the context of the responses text
def changeTextBox(String):
    outputText.config(state=NORMAL)  
    outputText.delete(1.0, END)  
    outputText.insert(END, String)  
    outputText.config(state=DISABLED)  
    enterButton.state(['!disabled']) #Only needed for handleConversation() as that can use enter button to run

#Widgets and main loop set-up
root = Tk()
root.geometry("800x600")
root.title("AI Chatbot")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1) # Fills any extraspace if the window is resized
root.rowconfigure(0, weight=1)

label = ttk.Label(mainframe, text='Ask the AI')
label.grid(column=1,row=3, sticky=(W, E))

#Textbox for users to prompt the AI
prompt = StringVar()
promptEntry = ttk.Entry(mainframe, width=50, textvariable=prompt)
promptEntry.grid(column=2, row=3, sticky=(W, E))

#Create a Text widget for the output
outputText = Text(mainframe, wrap=WORD, height=20, width=50)
outputText.grid(column=2, row=4, sticky=(W, E))
outputText.config(state=DISABLED)  # Make the text widget read-only initially

#Add a scrollbar for the Text widget
scrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=outputText.yview)
scrollbar.grid(column=3, row=4, sticky=(N, S))
outputText['yscrollcommand'] = scrollbar.set

enterButton = ttk.Button(mainframe, text="Enter", command=handleConversation)
enterButton.grid(column=3, row=3, sticky=W)

#Checkbox to determine whether the AI should use pdf data or not
pdfMode = BooleanVar()
check = ttk.Checkbutton(mainframe, variable=pdfMode, text='Use PDFs to answer questions', onvalue=True, offvalue=False)
check.grid(column=4, row=4, sticky=W)

#Button to allow users to upload a pdf
pdfButton = ttk.Button(mainframe, text="Upload PDF", command= loadDocuments)
pdfButton.grid(column=4, row=3, sticky=W)

for child in mainframe.winfo_children():  #Creates gaps between widgets
    child.grid_configure(padx=5, pady=5)
promptEntry.focus()
root.bind("<Return>", handleConversation) #Enter key works the same as enterButton

root.mainloop()