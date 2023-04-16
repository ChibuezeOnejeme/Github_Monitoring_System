
This project is  a Github monitoring system, Where the WatchEvent, PullRequestEvent and IssuesEvent are tracked through this  Github API (https://api.github.com/events )

Note: app.scheduler calls the Github API (https://api.github.com/events )  every 10mins once the flask web server is running

These are the endpoints to access the functionalities of the project:
1) `http://127.0.0.1:5000/`         :  Return the total number of events grouped by the event type for an offset 10mins.
   Note: An Interval appscheduler was set to `10 minutes` as a decorator to ensure that the stipulated offset is serverd fresh.A cronjob can also be set for pinpoint accuracy when the user wants to collect this information at a particular date and time

2) `http://127.0.0.1:5000/avg`      : Renders Calculated average time between pull requests for a given repository.



3) `http://127.0.0.1:5000/chart`    : This end point renders `chart.html` template serving Bar chart for the total universe of events types  in the database ie how many Pull,issue or watch event have occurred.The library used for charting can be found on this link:`https://www.chartjs.org/docs/latest/getting-started/`

Find below a simple system architecture of C4 (level 1)


![Alt text](./my%20github.drawio.png "Title")


The project is coded primarily in python utilizing framework and libraries such as flask,pandas, numpy ,datetime ,pytz,apscheduler.
To keep things simple Csv file was used as backend storage system.

## Prerequisites

Before you begin, ensure you have met the following requirements:
<!--- These are just example requirements. Add, duplicate or remove as required --->
* You have installed the latest version of `python or 3.8 and above`
* You have a `Windows/Linux/Mac` machine.
.

## Installing Github Monitoring system

 Follow these steps:
 1) create virtual environment
 2) clone project
 3) Install requirements.txt using pip `pip install -r requirements. txt `

4) in the  command line run `python api.py` to start flask server and choose end point to see result


# contact me incase of queries or observations:

Email: onejemechibueze33@gmail.com
Twitter:@chibuezemiller