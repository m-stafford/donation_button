import mechanize
import boto3
import os

sns=boto3.client('sns')
phone_number='PHONE_INCLUDING_COUNTRYCODE_AND_AREA_CODE'

from base64 import b64decode
CC_number=boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['CC_number']))['Plaintext']
CC_expiration_month=boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['CC_expiration_month_as_num']))['Plaintext']
CC_expiration_year=boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['CC_expiration_year']))['Plaintext']
CC_CSC=boto3.client('kms').decrypt(CiphertextBlob=b64decode(os.environ['CC_CSC']))['Plaintext']

br = mechanize.Browser(factory=mechanize.RobustFactory()) 

def lambda_handler(event, context):
	br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
	br.open("https://dsausa.nationbuilder.com/donate")
	br.select_form(nr=3)

	br.form['submitted[donation][aclu_recurring]']=0 
	br.form['donation[amount_option]']=["other"]
	br.form['donation[amount]']="5"

	br.form['donation[first_name]']="FIRST_NAME"
	br.form['donation[last_name]']="LAST_NAME"
	br.form['donation[email]']="EMAIL"

	br.form['donation[billing_address_attributes][address1]']="ADDRESS_1"
	br.form['donation[billing_address_attributes][address2]']="ADDRESS_2"
	br.form['donation[billing_address_attributes][city]']="CITY"
	br.form['donation[billing_address_attributes][state]']=["STATE_CODE"] 
	br.form['donation[billing_address_attributes][zip]']="ZIP_CODE"
	br.form['donation[billing_address_attributes][country_code]']=["COUNTRY_CODE"] 

	br.form['donation[card_number]']=CC_number
	br.form['donation[card_expires_on(2i)]']=[CC_expiration_month_as_num]
	br.form['donation[card_expires_on(1i)]']=[CC_expiration_year]
	br.form['donation[card_verification]']=CC_CSC

	response = br.submit()
	if "Thank You" in response.read():
    	message = '$5 donated to the DSA! Thanks, comrade!'
    	sns.publish(PhoneNumber=phone_number, Message=message)
	else:
		message = 'Error: no donation occurred'
		sns.publish(PhoneNumber=phone_number, Message=message)
