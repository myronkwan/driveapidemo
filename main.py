import webapp2
import httplib2
import os
from apiclient import discovery
from oauth2client.contrib.appengine import OAuth2DecoratorFromClientSecrets

SCOPES = 'https://www.googleapis.com/auth/drive.readonly'
CLIENT_SECRET = 'client_secret.json'
MAX_RESULTS=50

decorator=OAuth2DecoratorFromClientSecrets(os.path.join(os.path.dirname(__file__),CLIENT_SECRET),SCOPES)
service = discovery.build('drive', 'v2')
class MainPage(webapp2.RequestHandler):
		
		@decorator.oauth_required
		def get(self):
				self.response.headers['Content-Type']='text/plain'
				if decorator.has_credentials():
						results=service.files().list(maxResults=MAX_RESULTS).execute(decorator.http())
						files=results.get('items')
						if not files:
								self.response.write('no files found')
						else:
							self.response.write('Files: \n')
							for file in files:
								self.response.write(file['title'].encode('ascii','ignore').decode('ascii')+'\n')
app=webapp2.WSGIApplication([('/',MainPage),(decorator.callback_path,decorator.callback_handler()),], debug=True)
