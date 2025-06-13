import os.path
from time import strftime, localtime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

class DataService:

    AUTH_SCOPES = ["https://mail.google.com/"]
    AUTH_CREDS  = None
    GMAIL_SERVICE = None

    SAMPLE_DATA = [{"id": 1, "threadId": 1, "snippet": "Setup APIs. Kindly setup IAM and EAI apis", "labelIds": ["inbox"]},
                   {"id": 2, "threadId": 1, "snippet": "Re: Setup APIs. API are setup. Please validate. There are accessible at https://mydomain.com/apis/<iam|eai>", "labelIds": ["inbox"]},
                   {"id": 3, "threadId": 1, "snippet": "Re: Re: Setup APIs. I have restarted them. Please check again", "labelIds": ["sent"]},
                   {"id": 4, "threadId": 2, "snippet": "Can we catchup for coffee on friday at 4pm?", "labelIds": ["inbox"]},
                   {"id": 5, "threadId": 2, "snippet": "Sure I can make it this friday. I will send an invite", "labelIds": ["sent"]},
                   {"id": 6, "threadId": 3, "snippet": "I found out that lunar module of 1968 Apollo 10 mission was called snoopy. It was inserted into heliocentric orbit. Since then, it has been revolving along side earth around the sun", "labelIds": ["inbox"]},]

    def __init__(self):
        self.glogin()

    def glogin(self):
        if os.path.exists("token.json"):
            self.AUTH_CREDS = Credentials.from_authorized_user_file("token.json", self.AUTH_SCOPES)
        if not self.AUTH_CREDS or not self.AUTH_CREDS.valid:
            if self.AUTH_CREDS and self.AUTH_CREDS.expired and self.AUTH_CREDS.refresh_token:
                self.AUTH_CREDS.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", self.AUTH_SCOPES)
                self.AUTH_CREDS = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(self.AUTH_CREDS.to_json())
        self.GMAIL_SERVICE = build("gmail","v1",credentials=self.AUTH_CREDS)
        return True
    
    def gecho(self,any : str | None):
        return any

    #API    = GET https://gmail.googleapis.com/gmail/v1/users/{userId}/labels
    def glabels(self):
        try:
            labels = (self.GMAIL_SERVICE.users().labels().list(userId="me").execute().get('labels',[]))
            result = ["all"]
            for l in labels:
                result.append(l["name"])
            return result
        except HttpError as error: 
            return ["all"]

    #API    = GET https://gmail.googleapis.com/gmail/v1/users/{userId}/messages
    def gmessages(self,
                  query : str | None,
                  label : str = "all" ):
        try:
            if (label and label != "all"):
                queryStr = f"in:{label} {query}"
            else:
                queryStr = f"{query}"

            result = []
            messages = (self.GMAIL_SERVICE.users().messages().list(userId="me",q=queryStr).execute().get('messages', []))
            limit = 10
            init  = 0
            for m in messages:
                try:
                    init += 1
                    if init > limit:
                        break
                    msg = (self.GMAIL_SERVICE.users().messages().get(userId="me",id=m["id"],format="metadata").execute())

                    summary = msg["snippet"]
                    for h in msg["payload"]["headers"]:
                        if h["name"] == "Subject" :
                            summary += h["value"]
                            break

                    result.append({
                        "id":msg["id"],
                        "snippet":summary,
                        "date": strftime('%a %d %b %Y, %I:%M%p', localtime(int(msg["internalDate"])/1000))
                    })
                except Exception as err:
                    print(f"{err}")
                    continue;
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []

    #API    = GET https://gmail.googleapis.com/gmail/v1/users/{userId}/threads
    def gthreads(self,
                 query : str | None):
        try:
            result = []
            threads = (self.GMAIL_SERVICE.users().threads().list(userId="me",q=query).execute().get('threads', []))
            for t in threads:
                result.append({
                    "threadId":t["id"],
                    "snippet":t["snippet"]
                })
            return result
        except HttpError as error:
            print(f"An error occurred: {error}")
            return []