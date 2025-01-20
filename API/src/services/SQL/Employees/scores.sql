select sender as employee, round(avg(sentiment_score), 2) as score
from sentimail.emails
group by employee;