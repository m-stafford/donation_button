import mechanize
import boto3
import os

sns=boto3.client('sns')
phone_number='PHONE NUMBER'

from base64 import b64decode
CC_number=os.environ['CC_number']
CC_expiration_month_as_num=os.environ['CC_expiration_month_as_num']
CC_expiration_year=os.environ['CC_expiration_year']
CC_CSC=os.environ['CC_CSC']

br = mechanize.Browser(factory=mechanize.RobustFactory())
br.set_handle_robots(False)

def handle(event, context):
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
    br.open("https://dsausa.nationbuilder.com/donate")
    br.select_form(nr=1)

    br.form['donation[amount]']="5"

    br.form['donation[first_name]']="FIRST NAME"
    br.form['donation[last_name]']="LAST NAME"
    br.form['donation[email]']="EMAIL"

    br.form['donation[billing_address_attributes][address1]']="ADDRESS 1"
    br.form['donation[billing_address_attributes][address2]']="ADDRESS 2"
    br.form['donation[billing_address_attributes][city]']="CITY"
    state_us = br.find_control(name="donation[billing_address_attributes][state]", nr=1)
    state_us.value = ["STATE"]
    br.form['donation[billing_address_attributes][zip]']="ZIP"
    br.form['donation[billing_address_attributes][country_code]']=["US"] 

    br.form['donation[billing_address_attributes][phone_number]']=phone_number

    br.form['donation[card_number]']=CC_number
    br.form['donation[card_expires_on(2i)]']=[CC_expiration_month_as_num]
    br.form['donation[card_expires_on(1i)]']=[CC_expiration_year]
    br.form['donation[card_verification]']=CC_CSC

    response = br.submit()

    if "Thank you for contributing!" in response.read():
        message = '$5 donated to the DSA! Thanks, comrade!'
        sns.publish(PhoneNumber=phone_number, Message=message)
    else:
        message = 'Error: no donation occurred'
        sns.publish(PhoneNumber=phone_number, Message=message)

