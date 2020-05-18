import requests
from datetime import datetime
class ScoreGet:
    def __init__(self):
        self.url_get_all_matches="http://cricapi.com/api/matches"
        self.get_score="http://cricapi.com/api/cricketScore"
        self.apikey="hJ0xcmh5O6eMKXpvpixRDs9uFEe2"
        self.unique_id=""
    def get_unique_id(self):
        uri_params={"apikey":self.apikey}
        resp=requests.get(self.url_get_all_matches,params=uri_params)
        resp_dict=resp.json()
        uid_found=0

        for i in resp_dict['matches']:
            if (i['team-1']=='Afghanistan' or ['team-2']=='Afghanistan' and i['matchstarted']):
                todays_date=datetime.today().strftime('%Y-%m-%d')
                if todays_date== i['date'].split("T")[0]:
                    self.unique_id=i['unique_id']
                    uid_found=1
                    break

        if not uid_found:
            self.unique_id=-1
        send_data=self.get_score_current(self.unique_id)
        return send_data

    def get_score_current(self,unique_id):
        data=""
        if unique_id==-1:
            data="No India matches today"
        else:
            uri_params={'apikey':self.apikey,"unique_id":unique_id}
            resp=requests.get(self.get_score,params=uri_params)
            data_json=resp.json()
            try:
                data="Here is the score:\n"+data_json['stat'] + "\n"+data_json['score']
            except KeyError as e:
                print(e)
        return data
if __name__=="__main__":
    obj_score=ScoreGet()
    whatsapp_message=obj_score.get_unique_id()
    from twilio.rest import Client
    a_sid="AC1481ee7c8597830393f08bf4f95aadea"
    auth_token="d4168609a842ac9d9fe215c00bfd5df2"
    client = Client(a_sid,auth_token)
    message = client.messages.create(body=whatsapp_message, from_='whatsapp:+14155238886',to='whatsapp:+917011157445')
