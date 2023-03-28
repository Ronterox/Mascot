from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from datetime import datetime
from time import sleep, time
import json

# -------------------- Settings --------------------

URL = "https://platform.openai.com/playground/p/default-tweet-classifier"
LOCAL_STORAGE_TOKEN ={ '@@auth0spajs@@::DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD::https://api.openai.com/v1::openid profile email offline_access' : '{"body":{"access_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL2FwaS5vcGVuYWkuY29tL3Byb2ZpbGUiOnsiZW1haWwiOiJyaWNhcmRpdG9tb250c2VycmF0QGdtYWlsLmNvbSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlfSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1MTcxNTExNTM2OTQ3NjQ1NTAxIiwiYXVkIjpbImh0dHBzOi8vYXBpLm9wZW5haS5jb20vdjEiLCJodHRwczovL29wZW5haS5vcGVuYWkuYXV0aDBhcHAuY29tL3VzZXJpbmZvIl0sImlhdCI6MTY3OTk4ODk4NiwiZXhwIjoxNjgxMTk4NTg2LCJhenAiOiJEUml2c25tMk11NDJUM0tPcHFkdHdCM05ZdmlIWXp3RCIsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwgb2ZmbGluZV9hY2Nlc3MifQ.d8FPsgDZcIbSmekhWTtaSIeoIB286C8jWjDZUtqRawRwcnlChTVuG0tc5ZvPbg8-_p7VNlRvBZcF-DNyHS9YO3uUVmPguS5FpnOhgw92IUAD0dn2_XgOMsEETKcG6gykvIAHoeZ_JL420DvC8UzLwb6OtY9Y98s-Uk7JCaNd7dxiztD2XTvzVV8fDOtp0NtLQyS08RAdh3lZExgsTBjQb2ew6Pb4_3xc40UZ9FpcI4snW94PfSV9vsJ7Exn8sDOXP4YRyyKP6EnCNncHWETiS1IFCT-qlfrkzplB23ubFay4cMWvDKql6xT16m9TaAIm_BuiAnS6WUyO6sdqRbV-mw","refresh_token":"v1.Mbf5kY3fa_ctfcmm54rzCLmRh1ivJLQ1t7NjEdJTBU0b52dJSSOsMrZqu-IvJ1f_KMrU-NAXClAYiS7D-A2L6Hc","id_token":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL29uYm9hcmQub3BlbmFpLmNvbS9nZW9pcCI6eyJjb250aW5lbnRfY29kZSI6IkVVIiwiY291bnRyeV9jb2RlIjoiRVMiLCJjb3VudHJ5X2NvZGUzIjoiRVNQIiwiY291bnRyeV9uYW1lIjoiU3BhaW4iLCJ0aW1lX3pvbmUiOiJFdXJvcGUvTWFkcmlkIn0sImdpdmVuX25hbWUiOiJSaWNhcmRvIiwiZmFtaWx5X25hbWUiOiJNb250c2VycmF0Iiwibmlja25hbWUiOiJyaWNhcmRpdG9tb250c2VycmF0IiwibmFtZSI6IlJpY2FyZG8gTW9udHNlcnJhdCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhibER3VlRwUGVDMWNkelVlVkh6TmVHMGhvVWhMYjBRYkhOakUwMT1zOTYtYyIsImxvY2FsZSI6ImVuLUdCIiwidXBkYXRlZF9hdCI6IjIwMjMtMDMtMjVUMjE6NTQ6NTYuNzQ4WiIsImVtYWlsIjoicmljYXJkaXRvbW9udHNlcnJhdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsImF1ZCI6IkRSaXZzbm0yTXU0MlQzS09wcWR0d0IzTll2aUhZendEIiwiaWF0IjoxNjc5OTg4OTg2LCJleHAiOjE2ODExOTg1ODYsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1MTcxNTExNTM2OTQ3NjQ1NTAxIiwic2lkIjoiMWV3Q0JNMmpLNGM1X2ZVTGR4X0FZcktqTnVXRGVtWlMiLCJub25jZSI6Ik1taERVRWhvTW5KRVIwNUJNRkJMUms1VVFUVnFUVWRCY0d4b2NrUkNZVFppZFdVMmFrWnRVMVpYUVE9PSJ9.2BjzOUinrTdD6JkOikQhQsIIn_tuh80Jm4lnBYvRdDnz3ZYOeIrzPD5RRG1AoxQSTLw0iYO04G0fMbchWkxMkAuTbQe6CURIyu26_hEBbzUuOzqCNL4RvPBd8y9aZ9_ubxpobDI3m4JtgfFjsGtJpKsRsbHy3izhNbGTGzwU4-mZVq-HSCQ_izLKDcrpBEt1OExjRZqpUJk2lz5FgkUAGPhQy_BR9WwzAdnJYLxYtHaSmSoVNup1kLtMeHFfSvKSSwLKkkh2Dh7IB6oBOe0aBaUkDaYgf2sNrM2mYejOBuMnjhnL46WjSUojytj4COCAcr5YahDHgdxdk39YK0Q9ZQ","scope":"openid profile email offline_access","expires_in":1209600,"token_type":"Bearer","decodedToken":{"encoded":{"header":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9","payload":"eyJodHRwczovL29uYm9hcmQub3BlbmFpLmNvbS9nZW9pcCI6eyJjb250aW5lbnRfY29kZSI6IkVVIiwiY291bnRyeV9jb2RlIjoiRVMiLCJjb3VudHJ5X2NvZGUzIjoiRVNQIiwiY291bnRyeV9uYW1lIjoiU3BhaW4iLCJ0aW1lX3pvbmUiOiJFdXJvcGUvTWFkcmlkIn0sImdpdmVuX25hbWUiOiJSaWNhcmRvIiwiZmFtaWx5X25hbWUiOiJNb250c2VycmF0Iiwibmlja25hbWUiOiJyaWNhcmRpdG9tb250c2VycmF0IiwibmFtZSI6IlJpY2FyZG8gTW9udHNlcnJhdCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhibER3VlRwUGVDMWNkelVlVkh6TmVHMGhvVWhMYjBRYkhOakUwMT1zOTYtYyIsImxvY2FsZSI6ImVuLUdCIiwidXBkYXRlZF9hdCI6IjIwMjMtMDMtMjVUMjE6NTQ6NTYuNzQ4WiIsImVtYWlsIjoicmljYXJkaXRvbW9udHNlcnJhdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsImF1ZCI6IkRSaXZzbm0yTXU0MlQzS09wcWR0d0IzTll2aUhZendEIiwiaWF0IjoxNjc5OTg4OTg2LCJleHAiOjE2ODExOTg1ODYsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1MTcxNTExNTM2OTQ3NjQ1NTAxIiwic2lkIjoiMWV3Q0JNMmpLNGM1X2ZVTGR4X0FZcktqTnVXRGVtWlMiLCJub25jZSI6Ik1taERVRWhvTW5KRVIwNUJNRkJMUms1VVFUVnFUVWRCY0d4b2NrUkNZVFppZFdVMmFrWnRVMVpYUVE9PSJ9","signature":"2BjzOUinrTdD6JkOikQhQsIIn_tuh80Jm4lnBYvRdDnz3ZYOeIrzPD5RRG1AoxQSTLw0iYO04G0fMbchWkxMkAuTbQe6CURIyu26_hEBbzUuOzqCNL4RvPBd8y9aZ9_ubxpobDI3m4JtgfFjsGtJpKsRsbHy3izhNbGTGzwU4-mZVq-HSCQ_izLKDcrpBEt1OExjRZqpUJk2lz5FgkUAGPhQy_BR9WwzAdnJYLxYtHaSmSoVNup1kLtMeHFfSvKSSwLKkkh2Dh7IB6oBOe0aBaUkDaYgf2sNrM2mYejOBuMnjhnL46WjSUojytj4COCAcr5YahDHgdxdk39YK0Q9ZQ"},"header":{"alg":"RS256","typ":"JWT","kid":"MThENUJGNEM1QTE4M0FBMjdCNTg5MDU1RTUwQUJDMEMwRkFEQkEzRg"},"claims":{"__raw":"eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1UaEVOVUpHTkVNMVFURTRNMEZCTWpkQ05UZzVNRFUxUlRVd1FVSkRNRU13UmtGRVFrRXpSZyJ9.eyJodHRwczovL29uYm9hcmQub3BlbmFpLmNvbS9nZW9pcCI6eyJjb250aW5lbnRfY29kZSI6IkVVIiwiY291bnRyeV9jb2RlIjoiRVMiLCJjb3VudHJ5X2NvZGUzIjoiRVNQIiwiY291bnRyeV9uYW1lIjoiU3BhaW4iLCJ0aW1lX3pvbmUiOiJFdXJvcGUvTWFkcmlkIn0sImdpdmVuX25hbWUiOiJSaWNhcmRvIiwiZmFtaWx5X25hbWUiOiJNb250c2VycmF0Iiwibmlja25hbWUiOiJyaWNhcmRpdG9tb250c2VycmF0IiwibmFtZSI6IlJpY2FyZG8gTW9udHNlcnJhdCIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhibER3VlRwUGVDMWNkelVlVkh6TmVHMGhvVWhMYjBRYkhOakUwMT1zOTYtYyIsImxvY2FsZSI6ImVuLUdCIiwidXBkYXRlZF9hdCI6IjIwMjMtMDMtMjVUMjE6NTQ6NTYuNzQ4WiIsImVtYWlsIjoicmljYXJkaXRvbW9udHNlcnJhdEBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly9hdXRoMC5vcGVuYWkuY29tLyIsImF1ZCI6IkRSaXZzbm0yTXU0MlQzS09wcWR0d0IzTll2aUhZendEIiwiaWF0IjoxNjc5OTg4OTg2LCJleHAiOjE2ODExOTg1ODYsInN1YiI6Imdvb2dsZS1vYXV0aDJ8MTA1MTcxNTExNTM2OTQ3NjQ1NTAxIiwic2lkIjoiMWV3Q0JNMmpLNGM1X2ZVTGR4X0FZcktqTnVXRGVtWlMiLCJub25jZSI6Ik1taERVRWhvTW5KRVIwNUJNRkJMUms1VVFUVnFUVWRCY0d4b2NrUkNZVFppZFdVMmFrWnRVMVpYUVE9PSJ9.2BjzOUinrTdD6JkOikQhQsIIn_tuh80Jm4lnBYvRdDnz3ZYOeIrzPD5RRG1AoxQSTLw0iYO04G0fMbchWkxMkAuTbQe6CURIyu26_hEBbzUuOzqCNL4RvPBd8y9aZ9_ubxpobDI3m4JtgfFjsGtJpKsRsbHy3izhNbGTGzwU4-mZVq-HSCQ_izLKDcrpBEt1OExjRZqpUJk2lz5FgkUAGPhQy_BR9WwzAdnJYLxYtHaSmSoVNup1kLtMeHFfSvKSSwLKkkh2Dh7IB6oBOe0aBaUkDaYgf2sNrM2mYejOBuMnjhnL46WjSUojytj4COCAcr5YahDHgdxdk39YK0Q9ZQ","https://onboard.openai.com/geoip":{"continent_code":"EU","country_code":"ES","country_code3":"ESP","country_name":"Spain","time_zone":"Europe/Madrid"},"given_name":"Ricardo","family_name":"Montserrat","nickname":"ricarditomontserrat","name":"Ricardo Montserrat","picture":"https://lh3.googleusercontent.com/a/AGNmyxblDwVTpPeC1cdzUeVHzNeG0hoUhLb0QbHNjE01=s96-c","locale":"en-GB","updated_at":"2023-03-25T21:54:56.748Z","email":"ricarditomontserrat@gmail.com","email_verified":true,"iss":"https://auth0.openai.com/","aud":"DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD","iat":1679988986,"exp":1681198586,"sub":"google-oauth2|105171511536947645501","sid":"1ewCBM2jK4c5_fULdx_AYrKjNuWDemZS","nonce":"MmhDUEhoMnJER05BMFBLRk5UQTVqTUdBcGxockRCYTZidWU2akZtU1ZXQQ=="},"user":{"https://onboard.openai.com/geoip":{"continent_code":"EU","country_code":"ES","country_code3":"ESP","country_name":"Spain","time_zone":"Europe/Madrid"},"given_name":"Ricardo","family_name":"Montserrat","nickname":"ricarditomontserrat","name":"Ricardo Montserrat","picture":"https://lh3.googleusercontent.com/a/AGNmyxblDwVTpPeC1cdzUeVHzNeG0hoUhLb0QbHNjE01=s96-c","locale":"en-GB","updated_at":"2023-03-25T21:54:56.748Z","email":"ricarditomontserrat@gmail.com","email_verified":true,"sub":"google-oauth2|105171511536947645501"}},"audience":"https://api.openai.com/v1","oauthTokenScope":"openid profile email offline_access","client_id":"DRivsnm2Mu42T3KOpqdtwB3NYviHYzwD"},"expiresAt":1681198586}'}

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
    return textbox.text.replace(input, "").strip()

if __name__ == "__main__":
    while True:
        try:
            prediction = predict_gpt3(input("Ask me something: "))
            print(prediction)
        except KeyboardInterrupt:
            print("Exiting...")
            driver.quit()
            break
