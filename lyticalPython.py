import pandas as pd 
import numpy as np 
from math import log10, sqrt, floor, ceil

z_r = pd.read_csv('right_ZTABLE.csv')

def Digits(number):		#Quantifies the ammount of digits in the given number
	if type(number) == np.float64 or type(number) == float:
		return (len(str(number)) - 1 ) # To remove the period from the couting
	else:
		return (len(str(number)))

def DecimalDigits(number):		#Quantifies the ammount of decimal digits
	number = str(number)
	i = 0
	while number[i] != '.':
		i += 1
	i += 1
	return i

def IsNumerical(column):
	for i in range(len(column)):
		if type(column[i]) != np.float64 and type(column[i]) != np.int64:
			raise Exception(f'The {i}th element " {number} " is not a number')	#Checks if all values on the column are numerical

def Range(column):
	IsNumerical(column)
	lista = []
	for i in range(len(column)):
		lista.append(column[i])
	lista.sort()
	return lista[-1] - lista[0]		#Returns the range of the column. 

def SignificantFigures(number, n):		#Returns number with n signficant figures
	return round(number, n - int(floor(log10(abs(number)))) - 1)

def SmallestNumber(column):		#Returns the smallest figures number
	sizes = []
	for i in range(len(column)):
		sizes.append(Digits(column[i]))
		i += 1
	sizes.sort()
	return sizes[0]

def Average(column, figures = False):		#returns column's average
	soma = 0
	for i in range(len(column)):
		soma += column[i]
		i += 1
	if figures:
		return SignificantFigures(soma/len(column), SmallestNumber(column))
	else:
		return soma/len(column)

def Median(column, figures = False):		#Returns the median of the column
	even = len(column) % 2 == 0
	lista = [a for a in column]
	lista.sort()
	if even:
		a = ceil(len(column) / 2) - 1
		print('A : ' , a)
		b = floor(len(column) / 2)
		print('B : ' , b)
		median = (lista[a] + lista[b]) / 2
	else:
		a = ceil(len(column) / 2) - 1
		median = lista[a]
	if figures:
		median = SignificantFigures(median, SmallestNumber(column))
	return (median)

def PopulationStandardDeviation(column, figures = False):		#Returns the population standard deviation
	n = len(column)
	i = 0
	a = 0
	sizes = []
	avr = Average(column)
	for i in range(len(column)):
		a += (column[i] - avr) * (column[i] - avr)
		i += 1
	sizes.sort()
	if not figures:
		return sqrt(a/n)
	if figures:
		return (SignificantFigures(sqrt(a/n), SmallestNumber(column)))

def ConfidenceInterval(column, p = 95, string = False, figures = False):		#Returns the Confidence Interval in the p probability
	n_1 = int(str(p)[0])
	n_2 = int(str(p)[1])
	z = z_r.iat[n_1, n_2]
	avr = Average(column)
	n = len(column)
	dev = PopulationStandardDeviation(column)
	c = z * dev / sqrt(n)
	if string:
		return str(f'{avr} +- {c}')
	if figures:
		return SignificantFigures(c, SmallestNumber(column))
	if not figures:
		return c

def Variance(column, figures = False):		#Returns varience
	dev = PopulationStandardDeviation(column)
	v = dev * dev
	if figures:
		v = SignificantFigures(v, SmallestNumber(column))
	return v

def StandardDeviation(column, figures = False):		#Different from the Population Standard Deviation
	n = len(column) - 1
	a = 0
	avr = Average(column)
	for i in range(len(column)):
		a += (column[i] - avr) * (column[i] - avr)
		i += 1
	c = sqrt(a / (n))
	if figures:
		c = SignificantFigures(c, SmallestNumber(column))
	return c

def ZScore(column, x,u = 0, std_deviation = 0, figures = False):		#Returns the z score at the x element
	if std_deviation == 0:
		std_deviation = PopulationStandardDeviation(column)
	if u == 0:
		x = Average(column)
	z = (x - u) / std_deviation
	a_X = DecimalDigits(x)
	a_U = DecimalDigits(x)
	a_Devi = DecimalDigits(std_deviation)
	if figures:
		z = SignificantFigures(z, SmallestNumber(column))
	return z

def RelativeStandardError(column, figures = False):
	drp = StandardDeviation(column) / Average(column)
	if figures:
		drp = SignificantFigures(drp, SmallestNumber(column))
	return drp

def ViariationCoefficient(column, figures = False):
	drp = RelativeStandardError(column)
	if figures:
		drp = SignificantFigures(drp, SmallestNumber(column))
	return drp * 100
