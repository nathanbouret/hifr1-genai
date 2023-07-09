# ChatCEO Project  

## About this project  
Life Science – CxO Trend Analysis for Business.  
Who needs strategy consultants when you’ve got ChatCEO.    

### Problem Statement and Target Users  

Companies spend millions of dollars trying to beat their competition by anticipating and maturing on innovative solutions. Those ideas usually do not come by themselves. Most companies use consultant firms in order to gain useful insights into the new business opportunities and trends (provide source), and if they don’t, or their services are not accurate, they risk on losing many opportunities. Those solutions are costly, and not easily available, at least not at THE CLICK of a button. This is where our solution fits in. It is the ideal solution for the busy CEO who just needs quick insights to make quick and informed decision, for the people in the legal department who need to keep up with the inevitable frequent changes in legislations, for the business analyst who hasn’t finished his slide deck and has to get quick bullet points in a rush. This is ChatCeo.  

### Solution and Technical Components    

Our solution is a LLM chat solution. We want the user to be able to either quickly have access to predefined prompts or be able to communicate directly with the engine. We want the user to have a quick and easy experience. To do so, we have created two different user experiences.  
The first one is straight forward for the user. Depending on his profile, a couple different prompts are predefined and are directly given to them so they can get results within seconds without having to think about the prompt they want. The question we have defined are based on surveys we have collected from CxOs, and what we anticipate they might want and require out of such an app.  
The second option allows the user, whatever their profile might be, to directly interact with the engine through a chatbot experience. With this chatbot, the user can directly ask whatever question they might have, and the model will only respond based on the corpus that we have provided it with. This last feature is what really differentiates our model from our competition.  
 
## Prerequisite
1- On the backend side, ChatCEO solution calls models from VertexAI Google Cloud Platform & the corpus data (in .pdf format) is hosted in a dedicated Google 'BUCKET'. As a prerequisite to use the app, you need to setup a gcp project and prepare the following informations:    
'PROJECT_NAME':  
'PROJECT_ID' :  
'PROJECT_NUMBER'  
'REGION' :  
'BUCKET' :  
'BUCKET_NAME':  
The corpus pdf files should be loaded into your custom 'BUCKET'.  
2- The app was developped so far in Windows environnement. The following environment steps were defined for a Windows machine. The app will be adapted for Linux and MacOS environnements in next versions.   

## Environment Setup (local Windows machine OR VM)  

1/ Create a virtual environnement:   
example with conda:  
    $ conda create --name myenv  

2/ Navigate to the project root folder:  
    $ cd ../HIFR1-GenAI  

3/ 
Option 1:    
Run installation command:  
    $ pip install .  
The command will use setup.py file to prepare the environnement and install all required packages  
*** pip environment solver may not be able to install all the packages. In this case, we recommend to follow the second option.  

Option 2:  
Run installation command:  
    $ pip install -r requirements.txt  

and then complete installation using :  
    $ conda install missing_package==version  
Note that the order of packages installation should be respected as mentionned in the setup.py file.   

## Launch the ChatCEO App  

To launch the app, follow these two simple steps:  

1/ Navigate to the project root folder:   
    $ cd ../HIFR1-GenAI  

2/ Run launch command:  
    $ streamlit run app.py  

You can now view the app in your default browser.  
Local URL: http://localhost:8501  
## used tools and services
1. From Vertex AI:
  PaLM 2 for Text (text-bison@001) For QA feature
  PaLM 2 for Chat (chat-bison@001) For Chat feature

2. From Document AI:
  Document OCR processor to Convert pdf to txt
  batch processor service to process many document parallelly 

3. Google cloud storage (Bucket) to store our corpus and results
4. From workbench:
  User-managed notebooks

6. Vertex AI Matching Engine:
We tried this service to create a vector store and retrieve similar documents. Unfortunately, we could not integrate it to our pipeline due to the technical issues.

Other tools:
1. LangChain
2. streamlit
3. strealit-chat
4.FAISS
5.Chromadb

## Update the corpus data

In default mode, the app uses a local vector store containing preprocessed data from the corpus.  
In order to add new documents into the corpus, you need to do the following steps:  
1- Load the new document into your gcp bucket  
2- Update the config.py file ("gcp_config()" method) with your custom gcp config information.   
3- In config.py file, set "vector_store_flag" to "False".  
4- Run the app as described above.    
Due to the preprocessing step, the app may take a few minutes to run.   
5- The steps 1, 2, 3, 4 are needed when add a new document into the corpus and they should be executed once.  
To return to the default running mode, You need to "Stop" the app -> set "vector_store_flag" to "True" in config.py file -> Launch the app again.   
