import os, sys, inspect

# ensure pyeq3 can be imported
if -1 != sys.path[0].find('pyeq3-master'):raise Exception('Please rename git checkout directory from "pyeq3-master" to "pyeq3"')
exampleFileDirectory = sys.path[0][:sys.path[0].rfind(os.sep)]
pyeq3IimportDirectory =  os.path.join(os.path.join(exampleFileDirectory, '..'), '..')
if pyeq3IimportDirectory not in sys.path:
    sys.path.append(pyeq3IimportDirectory)
    
import pyeq3


# see IModel.fittingTargetDictionary
equation = pyeq3.Models_2D.BioScience.HyperbolicLogistic('SSQABS')

data = '''
  X        Y
5.357    10.376
5.457    10.489
5.797    10.874
5.936    11.049
6.161    11.327
6.697    12.054
6.731    12.077
6.775    12.138
8.442    14.744
9.769    17.068
9.861    17.104
'''
pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(data, equation, False)
equation.Solve()


##########################################################


print("Equation:", equation.GetDisplayName(), str(equation.GetDimensionality()) + "D")
print("Fitting target of", equation.fittingTargetDictionary[equation.fittingTarget], '=', equation.CalculateAllDataFittingTarget(equation.solvedCoefficients))
print("Fitted Parameters:")
for i in range(len(equation.solvedCoefficients)):
    print("    %s = %-.16E" % (equation.GetCoefficientDesignators()[i], equation.solvedCoefficients[i]))


equation.CalculateModelErrors(equation.solvedCoefficients, equation.dataCache.allDataCacheDictionary)
print()
for i in range(len(equation.dataCache.allDataCacheDictionary['DependentData'])):
    print('X:', equation.dataCache.allDataCacheDictionary['IndependentData'][0][i],)
    print('Y:', equation.dataCache.allDataCacheDictionary['DependentData'][i],)
    print('Model:', equation.modelPredictions[i],)
    print('Abs. Error:', equation.modelAbsoluteError[i],)
    if not equation.dataCache.DependentDataContainsZeroFlag:
        print('Rel. Error:', equation.modelRelativeError[i],)
        print('Percent Error:', equation.modelPercentError[i])
    else:
        print()
print()


##########################################################


equation.CalculateCoefficientAndFitStatistics()

if equation.upperCoefficientBounds or equation.lowerCoefficientBounds:
    print('You entered coefficient bounds. Parameter statistics may')
    print('not be valid for parameter values at or near the bounds.')
    print()

print('Degress of freedom error',  equation.df_e)
print('Degress of freedom regression',  equation.df_r)

if equation.rmse == None:
    print('Root Mean Squared Error (RMSE): n/a')
else:
    print('Root Mean Squared Error (RMSE):',  equation.rmse)

if equation.r2 == None:
    print('R-squared: n/a')
else:
    print('R-squared:',  equation.r2)

if equation.r2adj == None:
    print('R-squared adjusted: n/a')
else:
    print('R-squared adjusted:',  equation.r2adj)

if equation.Fstat == None:
    print('Model F-statistic: n/a')
else:
    print('Model F-statistic:',  equation.Fstat)

if equation.Fpv == None:
    print('Model F-statistic p-value: n/a')
else:
    print('Model F-statistic p-value:',  equation.Fpv)

if equation.ll == None:
    print('Model log-likelihood: n/a')
else:
    print('Model log-likelihood:',  equation.ll)

if equation.aic == None:
    print('Model AIC: n/a')
else:
    print('Model AIC:',  equation.aic)

if equation.bic == None:
    print('Model BIC: n/a')
else:
    print('Model BIC:',  equation.bic)


print()
print("Individual Parameter Statistics:")
for i in range(len(equation.solvedCoefficients)):
    if type(equation.tstat_beta) == type(None):
        tstat = 'n/a'
    else:
        tstat = '%-.5E' %  ( equation.tstat_beta[i])

    if type(equation.pstat_beta) == type(None):
        pstat = 'n/a'
    else:
        pstat = '%-.5E' %  ( equation.pstat_beta[i])

    if type(equation.sd_beta) != type(None):
        print("Coefficient %s = %-.16E, std error: %-.5E" % (equation.GetCoefficientDesignators()[i], equation.solvedCoefficients[i], equation.sd_beta[i]))
    else:
        print("Coefficient %s = %-.16E, std error: n/a" % (equation.GetCoefficientDesignators()[i], equation.solvedCoefficients[i]))
    print("          t-stat: %s, p-stat: %s, 95 percent confidence intervals: [%-.5E, %-.5E]" % (tstat,  pstat, equation.ci[i][0], equation.ci[i][1]))


print()
print("Coefficient Covariance Matrix:")
for i in  equation.cov_beta:
    print(i)


print()
print('Java Source Code:')
print(pyeq3.outputSourceCodeService().GetOutputSourceCodeJAVA(equation))