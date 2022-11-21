# stock-news-alert
## Setting up Twilio keys as environment variables
To run the script, `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` need to be added to environment variables.

```
echo "export TWILIO_ACCOUNT_SID='YOUR_SID_HERE'" > twilio.env
echo "export TWILIO_AUTH_TOKEN='YOUR_AUTH_TOKEN_HERE'" >> twilio.env
source ./twilio.env
```
