# -*- coding: utf-8 -*-
# Problem Set 5: Experimental Analysis
# Name: David
# Collaborators (discussion):
# Time: Start: 6/14/21, 9pm

import pylab
import re
import numpy
import math

# cities in our weather data
CITIES = [
    'BOSTON',
    'SEATTLE',
    'SAN DIEGO',
    'PHILADELPHIA',
    'PHOENIX',
    'LAS VEGAS',
    'CHARLOTTE',
    'DALLAS',
    'BALTIMORE',
    'SAN JUAN',
    'LOS ANGELES',
    'MIAMI',
    'NEW ORLEANS',
    'ALBUQUERQUE',
    'PORTLAND',
    'SAN FRANCISCO',
    'TAMPA',
    'NEW YORK',
    'DETROIT',
    'ST LOUIS',
    'CHICAGO'
]

TRAINING_INTERVAL = range(1961, 2010)
TESTING_INTERVAL = range(2010, 2016)

"""
Begin helper code
"""
class Climate(object):
    """
    The collection of temperature records loaded from given csv file
    """
    def __init__(self, filename):
        """
        Initialize a Climate instance, which stores the temperature records
        loaded from a given csv file specified by filename.

        Args:
            filename: name of the csv file (str)
        """
        self.rawdata = {}

        f = open(filename, 'r')
        header = f.readline().strip().split(',')
        for line in f:
            items = line.strip().split(',')

            date = re.match('(\d\d\d\d)(\d\d)(\d\d)', items[header.index('DATE')])
            year = int(date.group(1))
            month = int(date.group(2))
            day = int(date.group(3))

            city = items[header.index('CITY')]
            temperature = float(items[header.index('TEMP')])
            if city not in self.rawdata:
                self.rawdata[city] = {}
            if year not in self.rawdata[city]:
                self.rawdata[city][year] = {}
            if month not in self.rawdata[city][year]:
                self.rawdata[city][year][month] = {}
            self.rawdata[city][year][month][day] = temperature
            
        f.close()

    def get_yearly_temp(self, city, year):
        """
        Get the daily temperatures for the given year and city.

        Args:
            city: city name (str)
            year: the year to get the data for (int)

        Returns:
            a 1-d pylab array of daily temperatures for the specified year and
            city
        """
        temperatures = []
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        for month in range(1, 13):
            for day in range(1, 32):
                if day in self.rawdata[city][year][month]:
                    temperatures.append(self.rawdata[city][year][month][day])
        return pylab.array(temperatures)

    def get_daily_temp(self, city, month, day, year):
        """
        Get the daily temperature for the given city and time (year + date).

        Args:
            city: city name (str)
            month: the month to get the data for (int, where January = 1,
                December = 12)
            day: the day to get the data for (int, where 1st day of month = 1)
            year: the year to get the data for (int)

        Returns:
            a float of the daily temperature for the specified time (year +
            date) and city
        """
        assert city in self.rawdata, "provided city is not available"
        assert year in self.rawdata[city], "provided year is not available"
        assert month in self.rawdata[city][year], "provided month is not available"
        assert day in self.rawdata[city][year][month], "provided day is not available"
        return self.rawdata[city][year][month][day]

def se_over_slope(x, y, estimated, model):
    """
    For a linear regression model, calculate the ratio of the standard error of
    this fitted curve's slope to the slope. The larger the absolute value of
    this ratio is, the more likely we have the upward/downward trend in this
    fitted curve by chance.
    
    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by a linear
            regression model
        model: a pylab array storing the coefficients of a linear regression
            model

    Returns:
        a float for the ratio of standard error of slope to slope
    """
    assert len(y) == len(estimated)
    assert len(x) == len(estimated)
    EE = ((estimated - y)**2).sum()
    var_x = ((x - x.mean())**2).sum()
    SE = pylab.sqrt(EE/(len(x)-2)/var_x)
    return SE/model[0]

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])

"""
End helper code
"""

def generate_models(x, y, degs):
    """
    Generate regression models by fitting a polynomial for each degree in degs
    to points (x, y).

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        degs: a list of degrees of the fitting polynomial

    Returns:
        a list of pylab arrays, where each array is a 1-d array of coefficients
        that minimizes the squared error of the fitting polynomial
    """
    models = []
    for i in degs:
        models.append(pylab.polyfit(x,y,i))    
    
    return models
    #test returns 'rankwarning, polyfit may be poorly conditioned'.  check answers later

def r_squared(y, estimated):
    """
    Calculate the R-squared error term.
    
    Args:
        y: 1-d pylab array with length N, representing the y-coordinates of the
            N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the R-squared error term
    """
    error = ((estimated - y)**2).sum()
    meanError = error/len(y)
    
    return 1 - (meanError/numpy.var(y))

def evaluate_models_on_training(x, y, models):
    """
    For each regression model, compute the R-squared value for this model with the
    standard error over slope of a linear regression line (only if the model is
    linear), and plot the data along with the best fit curve.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        R-square of your model evaluated on the given data points,
        and SE/slope (if degree of this model is 1 -- see se_over_slope). 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    
    for model in models:
        
        #plot measured points
        pylab.plot(x, y, 'bo',label="Measured Points")

        estYvals = pylab.polyval(model,x)
        r2 = r_squared(y, estYvals)
        
        #plot best fit line
        pylab.plot(x, estYvals,'-r', label = "R^2="+format(r2, '.5f'))
        pylab.legend(loc='best')
        
        pylab.xlabel('Year')
        pylab.ylabel('Temperature')
        
        r2_trunc = truncate(r2,3)
        seos_trunc = truncate(se_over_slope(x,y,estYvals,model),3)
        title = (len(model) - 1, "Degree Model, R = " , r2_trunc , "SE/slope =" , seos_trunc)
                    
        pylab.title(title)

"""
x = pylab.array(range(50))
y = pylab.array(range(0,100,2))
degrees = [1, 2]
models = generate_models(x, y, degrees)     

evaluate_models_on_training(x, y, models)
"""

def get_avg_temp(temps):
    """
    Args:
        temps: a 1-d pylab array of daily temps for a given year & city
        length of temps *should* be the number of years
            
    Returns: 
        annual_avg_temp (an int): the average of the 
        daily temperatures in temps
    """
    tot = 0
    for i in range(len(temps)):
        tot += temps[i]
    annual_avg_temp = tot / len(temps)
    return annual_avg_temp

def gen_cities_avg(climate, multi_cities, years):
    """
    Compute the average annual temperature over multiple cities.

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to average over (list of str)
        years: the range of years of the yearly averaged temperature (list of
            int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the average annual temperature over the given
        cities for a given year.
    """
    y = []
    for i in years:        
        tot_temp_over_cities = 0        
        for j in multi_cities:
            temp = climate.get_yearly_temp(city=j,year=i)
            avg = get_avg_temp(temp)            
            tot_temp_over_cities += avg        
        y.append(tot_temp_over_cities/len(multi_cities))
        
    y_array = pylab.array(y)
    
    return y_array

def moving_average(y, window_length):
    """
    Compute the moving average of y with specified window length.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        window_length: an integer indicating the window length for computing
            moving average

    Returns:
        an 1-d pylab array with the same length as y storing moving average of
        y-coordinates of the N sample points
    """
    
    m_a = []    
    for i in range(len(y)):       
        num_vals = 0
        tot = 0       
        for j in range(window_length):
            index = i - j
            
            if index >=0:
                num_vals += 1
                tot += y[index]
            else:
                pass        
        m_a.append(tot/num_vals)
    
    m_a_arr = pylab.array(m_a)
        
    return m_a_arr


def rmse(y, estimated):
    """
    Calculate the root mean square error term.

    Args:
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        estimated: an 1-d pylab array of values estimated by the regression
            model

    Returns:
        a float for the root mean square error term
    """
    sum_sq_err = 0
    
    for i in range(len(y)):
        sq_err = (y[i] - estimated[i])**2
        sum_sq_err += sq_err
        
    rmse = (sum_sq_err/len(y))**0.5
    return rmse
        

def gen_std_devs(climate, multi_cities, years):
    """
    For each year in years, compute the standard deviation over the averaged yearly
    temperatures for each city in multi_cities. 

    Args:
        climate: instance of Climate
        multi_cities: the names of cities we want to use in our std dev calculation (list of str)
        years: the range of years to calculate standard deviation for (list of int)

    Returns:
        a pylab 1-d array of floats with length = len(years). Each element in
        this array corresponds to the standard deviation of the average annual 
        city temperatures for the given cities in a given year.
    """
    #1: Calculate temperature for each day in the year, by averaging temps for 
    #that day across multi_cities
    

    
    stdevs = []
    
    for i in range(len(years)):
        year_temps = []
        
        #creates a matrix of cities x days, with each value 
        #corresponding to a daily average temp for that city and day
        
        for j in range(len(multi_cities)):
            temp = climate.get_yearly_temp(city=multi_cities[j],year=years[i]) 
            #returns 1d array of daily temps
            temp = temp.tolist()
            year_temps.append(temp)
                
        daily_avgs = []

        #get average temperature of a given day across cities
        for k in range(len(temp)):
            daily_tot = 0
            for l in range(len(multi_cities)):
                daily_tot += year_temps[l][k]
            daily_avgs.append(daily_tot/len(multi_cities))               
        stdevs.append(numpy.std(daily_avgs))
   
    s_array = pylab.array(stdevs)
    
    return s_array    
    
    

def evaluate_models_on_testing(x, y, models):
    """
    For each regression model, compute the RMSE for this model and plot the
    test data along with the model’s estimation.

    For the plots, you should plot data points (x,y) as blue dots and your best
    fit curve (aka model) as a red solid line. You should also label the axes
    of this figure appropriately and have a title reporting the following
    information:
        degree of your regression model,
        RMSE of your model evaluated on the given data points. 

    Args:
        x: an 1-d pylab array with length N, representing the x-coordinates of
            the N sample points
        y: an 1-d pylab array with length N, representing the y-coordinates of
            the N sample points
        models: a list containing the regression models you want to apply to
            your data. Each model is a pylab array storing the coefficients of
            a polynomial.

    Returns:
        None
    """
    
    for model in models:
        
        #plot measured points
        pylab.plot(x, y, 'bo',label="Measured Points")

        estYvals = pylab.polyval(model,x)
        RMSE = rmse(y, estYvals)
        
        #plot best fit line
        pylab.plot(x, estYvals,'-r', label = "RMSE="+format(RMSE, '.3f'))
        pylab.legend(loc='best')
        
        pylab.xlabel('Year')
        pylab.ylabel('Temperature')
        
        RMSE_trunc = truncate(RMSE,5)
        title = (len(model) - 1, "Degree Model, RMSE = " , RMSE_trunc)
                    
        pylab.title(title)

if __name__ == '__main__':

    #Problem 4 & 5
    
    Climate = Climate('data.csv')

    #generates list of x values from 1961 to 2009
    x = TRAINING_INTERVAL
        
    def lta(x,y):
        #formats list to array
        xvals = pylab.array(x)
        yvals = pylab.array(y)
        return xvals,yvals
    
        
    # Part 4.A.1

    #Jan 10 temps in New York

    """
    #1: generate data samples 
    
    #generates list of y values (Jan 10 of each year in New York City)
    y = []
    for i in x:
        temp = Climate.get_daily_temp(city='NEW YORK',month=1,day=10,year=i)
        y.append(temp)
        
    xvals = pylab.array(x)
    yvals = pylab.array(y)
    
    #2: fit data to degree one polynomial w/ generate_models
    mods = generate_models(xvals,yvals,[1])
    
    #3: plot regression results using evaluate_models_on_training
    print("Plot: Jan 10 in New York")
    evaluate_models_on_training(xvals,yvals,mods)
    """

    # Part 4.A.2
    # Annual Temperatures
    
    #generates list of y values (average annual temperature in New York City)

    #gets average temperature for a year

    """
    y = []
    for i in x:
        temp = Climate.get_yearly_temp(city='NEW YORK',year=i)
        avg = get_avg_temp(temp)
        y.append(avg)
        
    xvals,yvals = lta(x,y)    
    mods = generate_models(xvals,yvals,[1])    
    evaluate_models_on_training(xvals,yvals,mods)
    """
    
    """
    # Part 4.B
    y = []

    yvals = gen_cities_avg(Climate, CITIES, TRAINING_INTERVAL)
    
    xvals = pylab.array(x)   
    mods = generate_models(xvals,yvals,[1])
    evaluate_models_on_training(xvals,yvals,mods)
    """
    
    # Part C: 5 Year Moving Average
    """
    y = gen_cities_avg(Climate, CITIES, TRAINING_INTERVAL)
    yvals = moving_average(y, 5)

    xvals = pylab.array(x)   
    mods = generate_models(xvals,yvals,[1])
    
    evaluate_models_on_training(xvals,yvals,mods)
    """
    # Part D.2: Prediction
    """
    #Using the training interval to predict the testing interval
    x = TRAINING_INTERVAL
    y = gen_cities_avg(Climate, CITIES, TRAINING_INTERVAL)

    xvals,yvals = lta(x,y)   
    
    mods = generate_models(xvals,yvals,[1])
    
    x_test = TESTING_INTERVAL
    y_test = gen_cities_avg(Climate, CITIES, TESTING_INTERVAL)
    
    xvals,yvals = lta(x_test,y_test)   

    evaluate_models_on_testing(xvals,yvals,mods)
    """
    
    #2.I
    #Using a 5yr moving average of all cities in the data set,
    #as well as 1,2,20 degrees of freedom to train the predictions
    #and test them on the testing interval
    
    # Part D.2.II
    """
    y = gen_cities_avg(Climate, CITIES, TRAINING_INTERVAL)
    yvals = moving_average(y, 5)

    xvals = pylab.array(x)   
    mods = generate_models(xvals,yvals,[1,2,20])
    
    x_test = TESTING_INTERVAL
    y_test = gen_cities_avg(Climate, CITIES, TESTING_INTERVAL)
    
    xvals,yvals = lta(x_test,y_test)   

    evaluate_models_on_testing(xvals,yvals,mods)  
    """
    
    #Part D.2.II New York, no 5 yr MA
    """
    y = []
    for i in x:
        temp = Climate.get_yearly_temp(city='NEW YORK',year=i)
        avg = get_avg_temp(temp)
        y.append(avg)        
    xvals, yvals = lta(x,y)    
    mods = generate_models(xvals,yvals,[1,2,20])    
    x_test = TESTING_INTERVAL
    y_test = gen_cities_avg(Climate, CITIES, TESTING_INTERVAL)    
    xvals,yvals = lta(x_test,y_test)   
    evaluate_models_on_testing(xvals,yvals,mods)      
    """
    
    # Part E
    #Compute 5-year moving averages on the yearly standard deviations
    #over a degree-one polynomial

    y = gen_std_devs(Climate, CITIES, TRAINING_INTERVAL)
    yvals = moving_average(y, 5)

    xvals = pylab.array(x)   
    mods = generate_models(xvals,yvals,[1])
    
    #if we want to begin predicting over the testing interval
    #x_test = TESTING_INTERVAL
    #y_test = gen_std_devs(Climate, CITIES, TESTING_INTERVAL)
    #xvals,yvals = lta(x_test,y_test)   

    evaluate_models_on_testing(xvals,yvals,mods)  
