# Makers Final project - Data Engineering in the Cloud 

## Background on the project
20 Databases are being updated in real-time on student performance and education insights globally, using the PISA 2018 dataset.

## Task
Develop a functioning dashboard that has been provided to visualise the data through a poll-able API endpoint.
We had 3 levels to the challenge on how old the data should be:
- Level 1: 1 hour old
- Level 2: 1 minute old
- Level 3: 1 second old

This is what the empty dashbaord looked like.

![Empty Dashboard](/imgs/empty.png)


## Phase One: Getting Our Bearings

Our first plan was to try transform the data manually to get an idea on how the final data should look. This would involve creating an analytical database to store transformed data, and then poll that data into the dashboard.
We immediately noticed some challenges that the data was being added into the source databases randomly, rather than appending at the end and incrementing the ID.

![Plan 1 diagram](/imgs/one.png)


## Phase Two: The Maximalist Solution

We wanted an automated solution without using an analytical database, since we didn't see the advantage of querying 20 databases regularly, then having to query another one for the transformed results regularly. We could just query the 20 databases using DAGs on airflow, and use airflow API endpoints to access the data. We also wanted to make sure we were working on the same environment, so we set up a docker-compose file with environment variables for the databases. This was also something we could deploy to an EC2 to have running once the DAGs were complete.

![Plan 2 diagram](/imgs/two.png)

We ran into troubles when the EC2 instances available could not handle Docker, due to trying smaller instances to reduce costs. We did just set up Airflow on an EC2, and it was running well, but the endpoints were not correctly formatted for the dashboard so would need transforming. We discovered the use of Lambda's, and then we had a lightbulb moment.

## Phase Three: The Lightbulb Moment

What if we just use lambda's to run when the API is accessed every second through API Gateway, query the databases, and return the required data?

![Plan 3 diagram](/imgs/three.png)

## Challenges:
- Creating log statements and understanding CloudWatch logs to see where errors were occuring.
- Data not having timestamps when being generated in the databases made it difficult to understand what were the most recent additions.
- Learning how to deploy packages onto lambda such as psycopg2.

## Successes:
- We were very flexible and pivoted quickly and efficiently when an approach wasn't working for us.
- Identified bottlenecks quickly and solved them.
- Staying within the AWS ecosystem to make it easy for data to move around.

## Looking forward:
If we had time to extend the project or do it again, we would likely add the use of DynamoDB to make some transformations easier and more efficient.
We would also look through the lambda's to refactor.
