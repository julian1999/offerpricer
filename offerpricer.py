import sys

# can create an excel sheet with this information, and this will read it
# [Optimize your real estate cashflow search with PYTHON]
# thumbnail has excel sheet with cashlow, YES/NO red-green rows, picture of me cracking fingers with hoodie
# provide github link
# assumes that the property has positive cashflow
# Youtube Title: HOW MUCH should you offer for cash-on-cash return goal?
def calculateMortgage(loanAmount, years, interestRate, annualPropertyTaxes, monthlyPMI):

  # Formula for mortgage calculator
  # M = L(I(1 + I)**N) / ((1 + I)**N - 1)
  # M = Monthly Payment, L = Loan, I = Interest, N = Number of payments, ** = exponent

  # Declares and asks for user to input loan amount. Then converts to float
  loanAmount = float(loanAmount)

  # Declares and asks user to input number of payments in years. Then converts to float. Years * 12 to get
  #  total number of months
  years = float(years) * 12

  # Declares and asks user to input interest rate. Then converts to float and input interest rate is /100/12
  interestRate = float(interestRate) / 100 / 12

  # Formula to calculate monthly payments
  mortgagePayment = loanAmount * (interestRate * (1 + interestRate)
                                  ** years) / ((1 + interestRate) ** years - 1) + (annualPropertyTaxes / 12) + monthlyPMI

  return mortgagePayment

def findOfferPrice(askingPrice, downPayment, years, interestRate, annualPropertyTaxes, monthlyPMI, monthlyRevenue, closingCosts, targetROI, annualROI, offerHigher):
  cashDownPayment = askingPrice * (downPayment / 100)
  loanAmount = askingPrice - cashDownPayment
  monthlyPayment = calculateMortgage(loanAmount, years, interestRate, annualPropertyTaxes, monthlyPMI)
  monthlyCashflow = monthlyRevenue - monthlyPayment
  annualCashflow = monthlyCashflow * 12
  totalCashInvested = cashDownPayment + closingCosts
  annualROI = annualCashflow / totalCashInvested 
  if (offerHigher):
    if (annualROI > targetROI): #offer more
      return findOfferPrice(askingPrice + 1000, downPayment, years, interestRate, annualPropertyTaxes, monthlyPMI, monthlyRevenue, closingCosts, targetROI, annualROI, offerHigher)
    elif (annualROI <= targetROI):
      return askingPrice
  else:
    if (annualROI <= targetROI): #offer less
      return findOfferPrice(askingPrice - 1000, downPayment, years, interestRate, annualPropertyTaxes, monthlyPMI, monthlyRevenue, closingCosts, targetROI, annualROI, offerHigher)
    elif (annualROI > targetROI):
      return askingPrice

inputDataFile = open(sys.argv[1])
outputDataFile = open(sys.argv[2], 'w')
targetROI = float(sys.argv[3])

# header
inputDataFile.readline()
outputHeader = 'address,city,state,postalCode,askingPrice,offerPrice,difference\n'
outputDataFile.write(outputHeader)
for line in inputDataFile:
    row = line.replace('\n', '').split(',')
  
    address = row[0]
    city = row[1]
    state = row[2]
    postalCode = row[3]
    askingPrice = float(row[4])
    downPayment = float(row[5])
    years = float(row[6])
    interestRate = float(row[7])
    annualPropertyTaxes = float(row[8])
    monthlyPMI = float(row[9])
    monthlyRevenue = float(row[10])
    closingCosts = float(row[11])

    cashDownPayment = askingPrice * (downPayment / 100)
    monthlyPayment = calculateMortgage(askingPrice  - cashDownPayment, years, interestRate, annualPropertyTaxes, monthlyPMI)
    monthlyCashflow = monthlyRevenue - monthlyPayment

    totalCashInvested = cashDownPayment + closingCosts
    annualROI = monthlyCashflow * 12 / totalCashInvested

    offerPrice = 0

    if (annualROI > targetROI): # offer higher
        offerPrice = findOfferPrice(askingPrice, downPayment, years, interestRate, annualPropertyTaxes, monthlyPMI, monthlyRevenue, closingCosts, targetROI, annualROI, True)
        outputLine = "{},{},{},{},${},${},+${}\n".format(address,city,state,postalCode,askingPrice,offerPrice,abs(askingPrice - offerPrice))
        outputDataFile.write(outputLine)
    if (annualROI < targetROI): # offer lower
        offerPrice = findOfferPrice(askingPrice, downPayment, years, interestRate, annualPropertyTaxes, monthlyPMI, monthlyRevenue, closingCosts, targetROI, annualROI, False)
        outputLine = "{},{},{},{},${},${},-${}\n".format(address,city,state,postalCode,askingPrice,offerPrice,abs(askingPrice - offerPrice))
        outputDataFile.write(outputLine)

inputDataFile.close()
outputDataFile.close()
