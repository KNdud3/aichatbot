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

#Handles the AI prompting. Args is needed as it is passed in when bind is used.
def handleConversation(*args): 
    global history
    enterButton.state(['disabled']) 
    userInput = prompt.get()
    aiOutput = chain.invoke({"history": history, "question": userInput})
    history += "\n User: "+ userInput+" \n AI: " + aiOutput

    outputText.config(state=NORMAL)  # Enable text editing to change text
    outputText.delete(1.0, END)  #
    outputText.insert(END, history)  
    outputText.config(state=DISABLED)  
    enterButton.state(['!disabled']) 

root = Tk()
root.geometry("800x600")
root.title("AI Chatbot")

mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

root.columnconfigure(0, weight=1) # Fills any extraspace if the window is resized
root.rowconfigure(0, weight=1)

label = ttk.Label(mainframe, text='Ask the AI')
label.grid(column=1,row=3, sticky=(W, E))

prompt = StringVar()
promptEntry = ttk.Entry(mainframe, width=50, textvariable=prompt)
promptEntry.grid(column=2, row=3, sticky=(W, E))


# Create a Text widget for the output
outputText = Text(mainframe, wrap=WORD, height=20, width=50)
outputText.grid(column=2, row=4, sticky=(W, E))
outputText.config(state=DISABLED)  # Make the text widget read-only initially

# Add a scrollbar for the Text widget
scrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=outputText.yview)
scrollbar.grid(column=3, row=4, sticky=(N, S))
outputText['yscrollcommand'] = scrollbar.set

scrollbar = ttk.Scrollbar(mainframe, orient=VERTICAL, command=outputText.yview)
scrollbar.grid(column=3, row=4, sticky=(N, S))
outputText['yscrollcommand'] = scrollbar.set

enterButton = ttk.Button(mainframe, text="Enter", command=handleConversation)
enterButton.grid(column=3, row=3, sticky=W)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)
promptEntry.focus()
root.bind("<Return>", handleConversation) 

root.mainloop()