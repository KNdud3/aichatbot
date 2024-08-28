from langchain_ollama import OllamaLLM # type: ignore
from langchain_core.prompts import ChatPromptTemplate # type: ignore
from tkinter import *
from tkinter import ttk

template = """
Context: {history}

Question: {question}

Answer: 
"""
history = ""

prompt = ChatPromptTemplate.from_template(template)
model = OllamaLLM(model="gemma2:2b")
chain = prompt | model

def handleConversation():
    global history
    enterButton.state(['disabled']) 
    userInput = prompt.get()
    aiOutput = chain.invoke({"history": history, "question": userInput})
    output.set("Bot: " + aiOutput)
    history += "\n User: "+ userInput+" \n AI: " + aiOutput
    enterButton.state(['!disabled']) 

root = Tk()
root.geometry("800x600")
root.title("AI Chatbot")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1) # Fills any extraspace if the window is resized
root.rowconfigure(0, weight=1)

prompt = StringVar()
promptEntry = ttk.Entry(mainframe, width=7, textvariable=prompt)
promptEntry.grid(column=2, row=1, sticky=(W, E))


output = StringVar()
ttk.Label(mainframe, textvariable=output).grid(column=2, row=2, sticky=(W, E))

enterButton = ttk.Button(mainframe, text="Enter", command=handleConversation)
enterButton.grid(column=3, row=3, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
promptEntry.focus()
root.bind("<Return>", handleConversation) 

root.mainloop()

#print(model.invoke(input="hello man"))

#if __name__ == "__main__":
    #handleConversation()