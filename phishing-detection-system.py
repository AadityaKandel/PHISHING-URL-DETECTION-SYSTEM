'''
This is an application designed by Aaditya Kandel.
It delves in the system of automation where it 
analyzes the links given to it by running a cloud AI 
called Gemini and responds accordingly. 

However, it is a warning that the entire application
doesn't depend on my coding skills as it uses a freely
available AI to analyze the data given to it. The reason
for doing so is because using a locally available data
seems quite unreasonable and limited as well. 

But, the good thing is that the entire interface is
designed without the help of an AI. The only part that
AI plays is the analyzation of data, not even the output.
The checking and conditioning is also from my end. 
Thank You.
'''

from google import genai
import google.generativeai as genai
from tkinter import *
import tkinter.messagebox as tmsg
from tkinter import scrolledtext as st

root = Tk()

'''
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)
'''

# Key Variables
api_key="api-key"
genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])
# response1 = chat.send_message("Hello, I have a cat.")
ENTER_URL = StringVar()
EAC = IntVar()
safe_text = '''
Checking from the locally available data, your link seems completely safe\n
However, we recommend you to use advanced checking that may take time but\n
increases accuracy. Thank You...
'''
unsafe_text = '''
If you want to check deeper into the link, you can use advanced checking.\n 
It may take time but it has increased accuracy. Thank You...
'''
phishing_blocklist = {
    # Patterns commonly used for typosquatting (using numbers for letters, etc.)
    "typosquatting": [
        "micr0soft", "g00gle", "app1e", "amz0n", "faceb00k", "paypa1"
    ],

    # Keywords often found in fraudulent subdomains or paths
    "suspicious_keywords": [
        "login", "secure", "verify", "account", "update", "signin", "password",
        "billing", "payment", "support-ticket", "suspension", "alert", "c0nfirm"
    ],

    # Common URL shorteners used to hide the true destination
    "url_shorteners": [
        "bit.ly", "goo.gl", "tinyurl.com", "t.co", "rebrand.ly", "is.gd", "cutt.ly"
    ],
    
    # Non-traditional or frequently abused top-level domains (TLDs)
    "suspicious_tlds": [
        ".xyz", ".top", ".club", ".biz", ".info", ".tk", ".cf", ".gq", ".ml", ".ga"
    ],

    # Specific brand-impersonating patterns and domains
    "brand_impersonation": [
        "wellsfargo-online.co", "amazon-security-us.site", "paypal-service.net", 
        "apple-icloud-recovery.com", "netflix-update.org", "chase-account-info.ru"
    ],
    
    # IP addresses used instead of domain names
    "ip_address_as_domain": [
        "http://192.", "http://10.", "http://172.", "http://127.", "http://1.1.1.1" # Example IPs
    ],

    # The use of '@' in the URL, which can be used to hide the true host
    "at_symbol": ["@"]
}
phishing_description = [
'Patterns commonly used for typosquatting (using numbers for letters, etc.)',
'Keywords often found in fraudulent subdomains or paths',
'Common URL shorteners used to hide the true destination',
'Non-traditional or frequently abused top-level domains (TLDs)',
'Specific brand-impersonating patterns and domains',
'IP addresses used instead of domain names',
"The use of '@' in the URL, which can be used to hide the true host",
]
phishing_titles = list(phishing_blocklist.keys())
# phishing_blocklist[phishing_titles[0]] = Displays the list of 'typosquatting'
# total_phishing_titles = len(phishing_titles)
# print(phishing_titles.index("suspicious_keywords")) = Displays 1
gemini_training_text='''
You are being used inside a python application that checks links to identify
whether they are phishing links. Your response must be in a pattern rather
than random. The pattern is the following for following scenarios:

Scenario 1: Response for Phishing Link
Your link seems unsafe as it is the prime example of [what_type_of_phishing_attack_is_it] in which [how_is_it_executed]. In the url [url], [short_explanation].
Example: Your link seems unsafe as it is the prime example of url_shorteners in which Common URL shorteners are used to hide the true destination. In the url "bit.ly/Hello", "bit.ly" is the example of url shortner and "/Hello" is the example of the shortened destination.

Like this scenario, your job is only to give me the response of what the example shows. If there is another type of phishing attack, you can feel free to replace [what_type_of_phishing_attack_is_it] & [how_is_it_executed] respectively and same goes for [url] & [short_explanation] accordingly.
Other than this, please do not give any extra response. Thank You for being in this session. Now, the questions will come in the format of links and your response is directed towards a single objective only.
'''


# Setting Variables
URL_EXAMPLE = "Eg: www.google.com"
ENTER_URL.set(URL_EXAMPLE)


# Applying Configuration
root.title("Phishing Link Detection System")
# root.geometry("550x450")
root.minsize(550,450)
root.maxsize(550,450)
root.iconbitmap("Icon/favicon.ico")
root.config(bg="white")


# Important Functions
def train_artificial_intelligence():
	chat.send_message(gemini_training_text)

def e1_enter(event):
	if ENTER_URL.get()!=URL_EXAMPLE:
		pass
	else:
		ENTER_URL.set("") # Empty the entry point
		e1.config(state=NORMAL)

def e1_leave(event):
	if ENTER_URL.get()=="":
		ENTER_URL.set(URL_EXAMPLE)
		e1.config(state=DISABLED)
	else:
		pass

def empty_spacing(frame_name):
	Label(frame_name,text=" ",bg="white").pack()

def artificial_intelligence_algorithm(url):
	try:
		response = chat.send_message(url)
		display_log.insert(1.0,response.text)
	except:
		tmsg.showerror('Error','Internet Access is Required to Use This Feature.')

def custom_checking_algorithm(url):
	phishing_type_finder = []
	for titles in phishing_titles:
		for urls in phishing_blocklist[titles]:
			if urls in url:
				phishing_type_finder.append(phishing_titles.index(titles))

	phishing_type_finder = list(set(phishing_type_finder)) # Making the list unique to remove repititon

	if len(phishing_type_finder)<1:
		display_log.insert(1.0,safe_text)
	else:
		if len(phishing_type_finder)<2:
			index=phishing_type_finder[0]
			display_log.insert(1.0,f'Your link seems unsafe as it is the prime example of {phishing_titles[index]} in which {phishing_description[index]}'+unsafe_text)
		else:
			text=''
			for x in phishing_type_finder:
				text+=f'\n{phishing_type_finder.index(x)+1}){phishing_titles[x]}\n{phishing_description[x]}'

			display_log.insert(1.0,f'Your link seems unsafe as it is the prime example of the following phishing tactics\n'+text)	

def initiate_ai_checking_system():
	display_log.config(state=NORMAL)
	display_log.delete(1.0,END)

	if ENTER_URL.get()==URL_EXAMPLE:
		tmsg.showinfo('Info','Please Provide A Link To Begin Phishing Detection')
		return

	if EAC.get() == 1:
		artificial_intelligence_algorithm(ENTER_URL.get())
	else:
		custom_checking_algorithm(ENTER_URL.get())
	
	display_log.config(state=DISABLED)

# Training the AI Before Applying Changes To Tkinter Window
train_artificial_intelligence()

# Creating Frames
f1 = Frame(borderwidth=10,bg="white")

# Creating Widgets
l1 = Label(
	text="Please Insert an URL Inside....",
	bg="white",
	fg="black",
	font="comicsansms 13 bold"
)
e1 = Entry(
	textvariable=ENTER_URL,
	width=50,
	font="Verdana 14 italic",
	justify=CENTER,
	state=DISABLED,
)
b1 = Button(f1,
	text="Check The Link",
	bg="grey",
	fg="white",
	font="comicsansms 13 bold",
	command=initiate_ai_checking_system,
	justify=CENTER,
)
ch1 = Checkbutton(f1,
	text="Enable Advanced Checking",
	variable=EAC,
	onvalue=1,
	offvalue=0,
	bg="white",
	fg="black",
)
display_log = st.ScrolledText(
	bg="lightgrey",
	fg="black",
	font="Verdana 12 italic",
	state=NORMAL,
	wrap=WORD,
)


# Making Hover Effects
e1.bind('<Enter>',e1_enter)
e1.bind('<Leave>',e1_leave)

# Packing Widgets
l1.pack()
e1.pack()
empty_spacing(root) # To create spacing between widgets in root
f1.pack(anchor=CENTER)
b1.pack(side=LEFT)
ch1.pack(side=LEFT)
empty_spacing(root)
display_log.pack()


root.mainloop()
