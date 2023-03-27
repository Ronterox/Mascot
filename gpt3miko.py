from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from time import sleep, time
import json

# -------------------- Settings --------------------

URL = "https://platform.openai.com/playground/p/default-tweet-classifier"
LOCAL_STORAGE_TOKEN ={ '@@auth0spajs@@::DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD::https://api.openai.com/v1::openid profile email offline_access' : '{"body":{"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJyaWNhcmRpdG9tb250c2VycmF0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1MTcxNTExNTM2OTQ3NjQ1NTAxIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY3ODc0NzAzMiwiZXhwIjoxNjc5OTU2NjMyLCJhenAiOiJEUml2c25tMk11NDJUM0tPcHFkdHdCM05ZdmlIWXp3RCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MifQ.amq6BRbX8blBxRyrhXXtdgAKzSRr1JBXY9KjbQncD5ZX5IHSV6kKUxvfEQlS6_Rz95X0ETphHAcKHuqxdUYiNZCpXXZdUWR2ISn3LxTo5H7z6ipFh4e0w4dC6zRYZu7xvVZ6T5VedP3XkkT5i77QXFiCog7bUR-AjrY9sSgwEKNHN2tqS2lDtfrVrZlpK0889_umVgbECgkyl68uqXOiJhmrsXntld0ec4iDmJACdi5i2Vd2O5M4xpwlFk3qNZXUm1Pa3bjLHcxJY9SXNjCjtsvsKe1e78ayChUMOegZdOkvKEewHcl_brCLyQyXTMiFTySfSG94E7RZI-ZcpYvXZw","refresh_token":"v1.MXOswFu_eEx5JQ95YXoHYfpcBzr4tkoJlS-R85Pjp20KH_HOhxob81nh33uEgGlHcVDZOGqBEWn6OuXvO3NSlzM","id_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL29uYm9hcmQub3BlbmFpLmNvbS9nZW9pcCI6eyJjb250aW5lbnRfY29kZSI6IkVVIiwiY291bnRyeV9jb2RlIjoiRVMiLCJjb3VudHJ5X2NvZGUzIjoiRVNQIiwiY291bnRyeV9uYW1lIjoiU3BhaW4iLCJ0aW1lX3pvbmUiOiJFdXJvcGUvTWFkcmlkIn0sImdpdmVuX25hbWUiOiJSaWNhcmRvIiwiZmFtaWx5X25hbWUiOiJNb250c2VycmF0Iiwibmlja25hbWUiOiJyaWNhcmRpdG9tb250c2VycmF0IiwibmFtZSI6IlJpY2FyZG8gTW9udHNlcnJhdCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhibER3VlRwUGVDMWNkelVlVkh6TmVHMGhvVWhMYjBRYkhOakUwMT1zOTYtYyIsImxvY2FsZSI6ImVuLUdCIiwidXBkYXRlZF9hdCI6IjIwMjMtMDMtMTNUMjI6Mzc6MDMuNDQ3WiIsImVtYWlsIjoicmljYXJkaXRvbW9udHNlcnJhdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsImF1ZCI6IkRSaXZzbm0yTXU0MlQzS09wcWR0d0IzTll2aUhZendEIiwiaWF0IjoxNjc4NzQ3MDMyLCJleHAiOjE2Nzk5NTY2MzIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1MTcxNTExNTM2OTQ3NjQ1NTAxIiwiYXV0aF90aW1lIjoxNjc4NzQ3MDIzLCJzaWQiOiJCOUtzWG94bFdublk5OGItdmh4LUJEOVBlWk92aUwtMSIsIm5vbmNlIjoiYWpoUlpUbEtWWE5MVEdGMU9EVndlUzVRWjFSdFlWazJTVFZGYjNoYVQyeFNZa1ZmT0dkSE1ERTNXUT09In0.XTyJp3R2TKdJF2i0kchTqcn1RsIRLnWO8dcNbfLhYnvZfy17uONhiKQT5SbV9RxAw0Gj4Rfp0AN5cbDlzttBFrU8etS_3-jABVihSlKh1B-AeuIJ1hbWR8cJiYssG3Eqbeq-R1Z0LzEKjIBfOv7_E_Wfpo9IZWuz81zMCJm60T8XSOjMIpnfNh2JgO3zEZ4QIW4R4baNckn3yNz9QFusezoVI-IUKGZj4YmAaOQNjqReZnJidGDQJNQw9Y_bD0hqzyvmjn2qXKx5eJjOOzWpPYq_Elp-oikz3eypiCoEfng9Tds7k_FHG0CGEgb9IggVR-rDLnmXY0qOB-zANqRgyw","scope":"openid profile email offline_access","expires_in":1209600,"token_type":"Bearer","decodedToken":{"encoded":{"header":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9","payload":"eyJodHRwczovL29uYm9hcmQub3BlbmFpLmNvbS9nZW9pcCI6eyJjb250aW5lbnRfY29kZSI6IkVVIiwiY291bnRyeV9jb2RlIjoiRVMiLCJjb3VudHJ5X2NvZGUzIjoiRVNQIiwiY291bnRyeV9uYW1lIjoiU3BhaW4iLCJ0aW1lX3pvbmUiOiJFdXJvcGUvTWFkcmlkIn0sImdpdmVuX25hbWUiOiJSaWNhcmRvIiwiZmFtaWx5X25hbWUiOiJNb250c2VycmF0Iiwibmlja25hbWUiOiJyaWNhcmRpdG9tb250c2VycmF0IiwibmFtZSI6IlJpY2FyZG8gTW9udHNlcnJhdCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhibER3VlRwUGVDMWNkelVlVkh6TmVHMGhvVWhMYjBRYkhOakUwMT1zOTYtYyIsImxvY2FsZSI6ImVuLUdCIiwidXBkYXRlZF9hdCI6IjIwMjMtMDMtMTNUMjI6Mzc6MDMuNDQ3WiIsImVtYWlsIjoicmljYXJkaXRvbW9udHNlcnJhdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsImF1ZCI6IkRSaXZzbm0yTXU0MlQzS09wcWR0d0IzTll2aUhZendEIiwiaWF0IjoxNjc4NzQ3MDMyLCJleHAiOjE2Nzk5NTY2MzIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1MTcxNTExNTM2OTQ3NjQ1NTAxIiwiYXV0aF90aW1lIjoxNjc4NzQ3MDIzLCJzaWQiOiJCOUtzWG94bFdublk5OGItdmh4LUJEOVBlWk92aUwtMSIsIm5vbmNlIjoiYWpoUlpUbEtWWE5MVEdGMU9EVndlUzVRWjFSdFlWazJTVFZGYjNoYVQyeFNZa1ZmT0dkSE1ERTNXUT09In0","signature":"XTyJp3R2TKdJF2i0kchTqcn1RsIRLnWO8dcNbfLhYnvZfy17uONhiKQT5SbV9RxAw0Gj4Rfp0AN5cbDlzttBFrU8etS_3-jABVihSlKh1B-AeuIJ1hbWR8cJiYssG3Eqbeq-R1Z0LzEKjIBfOv7_E_Wfpo9IZWuz81zMCJm60T8XSOjMIpnfNh2JgO3zEZ4QIW4R4baNckn3yNz9QFusezoVI-IUKGZj4YmAaOQNjqReZnJidGDQJNQw9Y_bD0hqzyvmjn2qXKx5eJjOOzWpPYq_Elp-oikz3eypiCoEfng9Tds7k_FHG0CGEgb9IggVR-rDLnmXY0qOB-zANqRgyw"},"header":{"alg":"RS256","typ":"JWT","kid":"MThENUJGNEM1QTE4M0FBMjdCNTg5MDU1RTUwQUJDMEMwRkFEQkEzRg"},"claims":{"__raw":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL29uYm9hcmQub3BlbmFpLmNvbS9nZW9pcCI6eyJjb250aW5lbnRfY29kZSI6IkVVIiwiY291bnRyeV9jb2RlIjoiRVMiLCJjb3VudHJ5X2NvZGUzIjoiRVNQIiwiY291bnRyeV9uYW1lIjoiU3BhaW4iLCJ0aW1lX3pvbmUiOiJFdXJvcGUvTWFkcmlkIn0sImdpdmVuX25hbWUiOiJSaWNhcmRvIiwiZmFtaWx5X25hbWUiOiJNb250c2VycmF0Iiwibmlja25hbWUiOiJyaWNhcmRpdG9tb250c2VycmF0IiwibmFtZSI6IlJpY2FyZG8gTW9udHNlcnJhdCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhibER3VlRwUGVDMWNkelVlVkh6TmVHMGhvVWhMYjBRYkhOakUwMT1zOTYtYyIsImxvY2FsZSI6ImVuLUdCIiwidXBkYXRlZF9hdCI6IjIwMjMtMDMtMTNUMjI6Mzc6MDMuNDQ3WiIsImVtYWlsIjoicmljYXJkaXRvbW9udHNlcnJhdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsImF1ZCI6IkRSaXZzbm0yTXU0MlQzS09wcWR0d0IzTll2aUhZendEIiwiaWF0IjoxNjc4NzQ3MDMyLCJleHAiOjE2Nzk5NTY2MzIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1MTcxNTExNTM2OTQ3NjQ1NTAxIiwiYXV0aF90aW1lIjoxNjc4NzQ3MDIzLCJzaWQiOiJCOUtzWG94bFdublk5OGItdmh4LUJEOVBlWk92aUwtMSIsIm5vbmNlIjoiYWpoUlpUbEtWWE5MVEdGMU9EVndlUzVRWjFSdFlWazJTVFZGYjNoYVQyeFNZa1ZmT0dkSE1ERTNXUT09In0.XTyJp3R2TKdJF2i0kchTqcn1RsIRLnWO8dcNbfLhYnvZfy17uONhiKQT5SbV9RxAw0Gj4Rfp0AN5cbDlzttBFrU8etS_3-jABVihSlKh1B-AeuIJ1hbWR8cJiYssG3Eqbeq-R1Z0LzEKjIBfOv7_E_Wfpo9IZWuz81zMCJm60T8XSOjMIpnfNh2JgO3zEZ4QIW4R4baNckn3yNz9QFusezoVI-IUKGZj4YmAaOQNjqReZnJidGDQJNQw9Y_bD0hqzyvmjn2qXKx5eJjOOzWpPYq_Elp-oikz3eypiCoEfng9Tds7k_FHG0CGEgb9IggVR-rDLnmXY0qOB-zANqRgyw","https://onboard.openai.com/geoip":{"continent_code":"EU","country_code":"ES","country_code3":"ESP","country_name":"Spain","time_zone":"Europe/Madrid"},"given_name":"Ricardo","family_name":"Montserrat","nickname":"ricarditomontserrat","name":"Ricardo Montserrat","picture":"https://lh3.googleusercontent.com/a/AGNmyxblDwVTpPeC1cdzUeVHzNeG0hoUhLb0QbHNjE01=s96-c","locale":"en-GB","updated_at":"2023-03-13T22:37:03.447Z","email":"ricarditomontserrat@gmail.com","email_verified":true,"iss":"https://auth0.openai.com/","aud":"DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD","iat":1678747032,"exp":1679956632,"sub":"google-oauth2|105171511536947645501","auth_time":1678747023,"sid":"B9KsXoxlWnnY98b-vhx-BD9PeZOviL-1","nonce":"ajhRZTlKVXNLTGF1ODVweS5QZ1RtYVk2STVFb3haT2xSYkVfOGdHMDE3WQ=="},"user":{"https://onboard.openai.com/geoip":{"continent_code":"EU","country_code":"ES","country_code3":"ESP","country_name":"Spain","time_zone":"Europe/Madrid"},"given_name":"Ricardo","family_name":"Montserrat","nickname":"ricarditomontserrat","name":"Ricardo Montserrat","picture":"https://lh3.googleusercontent.com/a/AGNmyxblDwVTpPeC1cdzUeVHzNeG0hoUhLb0QbHNjE01=s96-c","locale":"en-GB","updated_at":"2023-03-13T22:37:03.447Z","email":"ricarditomontserrat@gmail.com","email_verified":true,"sub":"google-oauth2|105171511536947645501"}},"audience":"https://api.openai.com/v1","oauthTokenScope":"openid profile email offline_access","client_id":"DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD"},"expiresAt":1679956632}'}

# -------------------- Options --------------------

HEADLESS = False
REQUEST_REFRESH_LIMIT = 3
SECS_PER_REFRESH = 1

# -------------------------------------------------

key = list(LOCAL_STORAGE_TOKEN.keys())[0]
script = f"window.localStorage.setItem('{key}', '{LOCAL_STORAGE_TOKEN[key]}');"
expireDate = json.loads(LOCAL_STORAGE_TOKEN[key])["expiresAt"]
secsToExpire = expireDate - time()

print(f"Token expires at {datetime.fromtimestamp(expireDate)}")
if secsToExpire < 0:
    print("Token expired")
    exit(1)
else:
    print(f"Token expires in {expireDate - time():.0f} seconds")

options = Options()
options.add_argument("--headless" if HEADLESS else "--no-headless")

driver = webdriver.Firefox(options=options)
driver.implicitly_wait(3)
driver.get(URL)
driver.execute_script(script)
driver.refresh()

def predict_gpt3(input):
    textbox = driver.find_element(By.CSS_SELECTOR, 'div[role="textbox"]')
    try:
        textbox.click()
    except:
        textbox.click()
    textbox.send_keys(Keys.CONTROL + "a")
    textbox.send_keys(input.strip())

    # Submit
    oldInput = textbox.text
    textbox.send_keys(Keys.CONTROL + Keys.ENTER)

    # Wait prediction
    refreshCount = 0
    while refreshCount < REQUEST_REFRESH_LIMIT:
        sleep(SECS_PER_REFRESH)
        if oldInput != textbox.text:
            refreshCount = 0
            oldInput = textbox.text
        refreshCount += 1

    return textbox.text.strip()

if __name__ == "__main__":
    while True:
        try:
            prediction = predict_gpt3(input("Ask me something: "))
            print(prediction)
        except KeyboardInterrupt:
            print("Exiting...")
            driver.quit()
            break
