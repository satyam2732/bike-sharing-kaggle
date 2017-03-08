import pylab
import calendar
import numpy as np
import seaborn as sn
from scipy import stats
import missingno as msno
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
dailydata = pd.read_csv("C:/Users/satyam chauhan/Desktop/bike sharing/train.csv")
dailydata.head()
dailydata = pd.read_csv("C:/Users/satyam chauhan/Desktop/bike sharing/train.csv")
dailydata['date']=dailydata.datetime.apply(lambda x:x.split()[0])
dailydata['hour']=dailydata.datetime.apply(lambda x:x.split()[1].split(":")[0])
dailydata['hour']=dailydata.datetime.apply(lambda x : x.split()[1].split(":")[0])
dailydata['weekday']=dailydata.date.apply(lambda datestring : calendar.day_name[datetime.strptime(datestring,"%Y-%m-%d").weekday()])
dailydata['month']=dailydata.date.apply(lambda datestring : calendar.month_name[datetime.strptime(datestring,"%Y-%m-%d").month])
dailydata.head()

dailydata['season']=dailydata.season.map({1:"spring",2:"summer",3:"fall",4:"winter"})
dailydata=dailydata.drop(["datetime","atemp"],axis=1)

msno.matrix(dailydata, figsize=(8,3))

#plotting graph for count by month and days
fig,(ax1,ax2)= plt.subplots(nrows=2)
fig.set_size_inches(9,10)

monthaggregated=pd.DataFrame(dailydata.groupby("month")['count'].mean()).reset_index()
monthsorted=monthaggregated.sort_values(by="count",ascending=False)
sn.barplot(data=monthsorted,x='month',y='count',ax=ax1)
ax1.set(xlabel='Month',ylabel='Averagecount',title="Average Count By Month")

monthweekaggregated=pd.DataFrame(dailydata.groupby(["month","weekday"],sort=True)["count"].mean()).reset_index()
monthweekdaysorted=monthweekaggregated.sort_values(by=['count'],ascending=False)
sn.barplot(data=monthweekdaysorted,x='month',y='count',hue='weekday',ax=ax2)
ax2.set(xlabel='Month',ylabel='Average count',title="Average Count By Month splited by day")
sn.plt.show()


#plotting graph for season by month and days
fig,(ax1,ax2)=plt.subplots(nrows=2)
fig.set_size_inches(9,10)

monthAggregated=pd.DataFrame(dailydata.groupby("season")["count"].mean()).reset_index()
monthSorted=monthAggregated.sort_values(by='count',ascending=False)
sn.barplot(data=monthSorted,x="season",y="count",ax=ax1)
ax1.set(xlabel="season",ylabel="count",title="Average Count By Season")

monthweekaggregated=pd.DataFrame(dailydata.groupby(["season","weekday"],sort=True)["count"].mean()).reset_index()
monthweeksorted=monthweekaggregated.sort_values(by='count',ascending=False)
sn.barplot(data=monthweeksorted,x="season",y="count",hue="weekday" ,ax=ax2)
ax2.set(xlabel="season",ylabel="average count",title="Average Count By Season splited by days")
sn.plt.show()

#skewness
fig,(ax1,ax2)=plt.subplots(ncols=2)
fig.set_size_inches(9,6)
sn.distplot(dailydata["count"],ax=ax1)
stats.probplot(dailydata["count"],dist='norm',fit=True,plot=ax2)
sn.plt.show()
#box plot to check outliers
fig,axes=plt.subplots(nrows=2,ncols=2)
fig.set_size_inches(9,10)
sn.boxplot(data=dailydata,y="count",orient="v",ax=axes[0][0])
sn.boxplot(data=dailydata,y="count",x="season",orient="v",ax=axes[0][1])
sn.boxplot(data=dailydata,y="month",x="count" ,orient="h", ax=axes[1][0])
sn.boxplot(data=dailydata, y="month",x="count",orient="h", hue="workingday", ax=axes[1][1])
sn.plt.show()
corrmatt=dailydata.corr()

#group different hour in set of four hours each and ploting count against combined hour
mask=np.array(corrmatt)
mask[np.tril_indices_from(mask)]=False
fig,ax=plt.subplots()
fig.set_size_inches(20,10)
sn.heatmap(corrmatt,mask=mask,vmax=.8,square=True,annot=True)
sn.plt.show()
fig,(ax1,ax2)=plt.subplots(nrows=2)
fig.set_size_inches(9,12)
dailydatamodified=dailydata.replace({'hour':{"00":"12AM-04AM","01":"12AM-04AM","02":"12AM-04AM","03":"12AM-04AM","04":"05AM-08AM","05":"05AM-08AM","06":"05AM-08AM","07":"05AM-08AM","08":"09AM-12PM","09":"09AM-12PM","10":"09AM-12PM","11":"09AM-12PM","12":"01PM-04PM","13":"01PM-04PM","14":"01PM-04PM","15":"01PM-4PM","16":"05PM-08PM","17":"05PM-08PM","18":"05PM-08PM","19":"05PM-08PM","20":"09PM-12AM","21":"09PM-12AM","22":"09PM-12AM","23":"09PM-12AM",}})
dailydatamean=pd.DataFrame(dailydatamodified.groupby("hour")["count"].mean()).reset_index()
dailydatameansorted=dailydatamean.sort_values(by="count",ascending=False)
sn.barplot(data=dailydatameansorted,x="hour",y="count",ax=ax1)

sn.barplot(data=dailydatameansorted,x="hour",y="count",ax=ax1)
ax1.set(xlabel="Hour",ylabel="Average Count", title="Average Count By Hour")
bike_week=pd.DataFrame.groupby(dailydatamodified,by="hour",as_index=False)['casual','registered'].mean()
bike_week['casual_prct']=bike_week.casual*100/(bike_week.casual+bike_week.registered)
bike_week['registered_prct']=bike_week.registered*100/(bike_week.casual+bike_week.registered)
bike_week['total_prct']=bike_week.registered_prct+bike_week.casual_prct
sn.set_context({"figure.figsize":(12,4)})
sn.barplot(x="hour",y="total_prct",data=bike_week,color="#008000")
sn.barplot(x="hour",y="casual_prct",data=bike_week,color="#111199")
ax2.set(xlabel="Hour",ylabel="Average Count", title="Percentage of Casual User By Time Interval")
green=plt.Rectangle((0,0),1,1,fc="#008000",edgecolor='none')
blue=plt.Rectangle((0,0),1,1,fc="#111199",edgecolor='none')
legend=plt.legend([green,blue],['Registered Users','Casual User by Time INTERVAL'],loc=9,ncol=2,fancybox=True,shadow=True,prop={'size':16},borderpad=-2)
legend.draw_frame(False)
sn.plt.show()
