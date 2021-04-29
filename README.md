# aws_lambda_basketball_check
I built an AWS lambda function that checks if a basketball league is available and sends me an email (AWS SES) if it is.

## Background
My friends and I were looking to join a basketball league that played on Saturdays or Sundays. Instead of checking the website each day (the leagues go quick) I decided to make a Python AWS Lambda function that checked for me. I also wanted it to email me with the leagues that fit our criteria. 

## AWS Lambda Function
I utilized a cron cloud watch event to trigger the function everyday at 4 PM. I also used the Lambda Layers functionality to use a package that is not apart of the standard Python packages in Lambda, the package is requests. From there I would just read in the return data and filter through the list of dictionaries using list comprension to see if any of the leagues matched our criteria. If we did find a match it would then email my email with the number of leagues and all the necessary data.

I used AWS SES to send the email to mine. It is really simple and was a perfect use case for it.
