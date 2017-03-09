This was forked from https://github.com/nathanpryor/donation_button 

In addition to the instructions below, you'll also need to have to make sure your AWS SNS stuff is set up to send texts.

Instructions for SNS here: https://docs.aws.amazon.com/sns/latest/dg/sms_publish-to-phone.html

# donation_button
This Python script was a quick-and-dirty solution to build an Amazon Dash button that would donate to the DSA!

The script requires the Mechanize library (http://wwwsearch.sourceforge.net/mechanize/).

Replace the obvious placeholders with your own information. 

It's set up to be run on Amazon's AWS Lambda service, with the credit card info stored as the following encrypted environment variables for a tiny bit more security:
	CC_number
	CC_expiration_month
	CC_expiration_year_as_num
	CC_CSC
If you're not doing that, go ahead and put them in as strings.
