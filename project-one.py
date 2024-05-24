def readCSV(filepath): #works 12/4
    with open(filepath, 'r') as file:
        lines = file.readlines()
    headers = [header.strip().lower() for header in lines[0].split(',')]
    #splits by commas
    data = [line.strip().split(',') for line in lines[1:]]
    return data, headers

def sortUsersByCountry(data, headers, country):
    countryPosition = headers.index('country')
    debtPosition = headers.index('indebt')
    timeSpentPosition = headers.index('time_spent_hour')
    incomePosition = headers.index('income')
    idPosition = headers.index('id')
    sortedUsers = []
    for entry in data:
        #make sure lowercase
        if entry[countryPosition].lower() == country.lower() and entry[debtPosition].lower() == 'true' and float(entry[timeSpentPosition]) > 7:
            sortedUsers.append([entry[idPosition], float(entry[incomePosition])])
    sortedUsers.sort(key=lambda x: int(x[0]))
    return sortedUsers

def uniqueCountries(data, headers, ageGroup):
    countryPosition = headers.index('country')
    agePosition = headers.index('age')
    countries = set(entry[countryPosition].strip().lower() for entry in data if ageGroup[0] <= int(entry[agePosition]) <= ageGroup[1])
    return sorted(list(countries))

#2024-04-14 19:43:26 fails test case?? why
#2024-04-15 09:43:59 fixedd
def calcStandardDeviation(values):
    length = len(values)
    mean = sum(values) / length
    squSumDiff = sum((x - mean) ** 2 for x in values)
    return (squSumDiff / (length - 1)) ** 0.5

def getAgeStats(data, headers, ageGroup):
    agePosition = headers.index('age')
    timeSpentPosition = headers.index('time_spent_hour')
    incomePosition = headers.index('income')
    demographicPosition = headers.index('demographics')

    ageData = [entry for entry in data if ageGroup[0] <= int(entry[agePosition]) <= ageGroup[1]]
    if not ageData:
        return [0, 0, '']

    timeSpent = [float(d[timeSpentPosition]) for d in ageData]
    avgTimeSpent = sum(timeSpent) / len(timeSpent)
    incomes = [float(d[incomePosition]) for d in ageData]
    standardDeviationIncome = calcStandardDeviation(incomes)

    demographicTime = {}
    for d in ageData:
        demo = d[demographicPosition].strip().lower()
        demographicTime.setdefault(demo, []).append(float(d[timeSpentPosition]))

    demographicAvgTime = {k: sum(v) / len(v) for k, v in demographicTime.items() if v}
    demographicMinTime = sorted(demographicAvgTime.items(), key=lambda item: (item[1], item[0]))[0][0]

    return [round(avgTimeSpent, 4), round(standardDeviationIncome, 4), demographicMinTime]
#2024-04-16 14:42:39 out of bounds fix
#
def popularPlatformAndCorrelation(data, headers):
    platformPosition = headers.index('platform')
    agePosition = headers.index('age')
    incomePosition = headers.index('income')
    platform_users = {}
    for entry in data:
        platform = entry[platformPosition]
        if platform in platform_users:
            platform_users[platform].append((int(entry[agePosition]), float(entry[incomePosition])))
        else:
            platform_users[platform] = [(int(entry[agePosition]), float(entry[incomePosition]))]
    popularPlatform = None
    maxUsers = 0
    for platform, users in platform_users.items():
        if len(users) > maxUsers:
            maxUsers = len(users)
            popularPlatform = platform
        elif len(users) == maxUsers:
            if popularPlatform is None or platform < popularPlatform:
                popularPlatform = platform
    if popularPlatform is None:
        return 0 #error handle

    ages, incomes = zip(*platform_users[popularPlatform]) #merge into tuple work 18/04
    meanAge = sum(ages) / len(ages)
    meanIncome = sum(incomes) / len(incomes)
    covariance = sum((a - meanAge) * (i - meanIncome) for a, i in zip(ages, incomes)) / len(ages)
    deviatedAge = (sum((a - meanAge) ** 2 for a in ages) / len(ages)) ** 0.5
    deviatedIncome = (sum((i - meanIncome) ** 2 for i in incomes) / len(incomes)) ** 0.5
    correlation = covariance / (deviatedAge * deviatedIncome) if deviatedAge and deviatedIncome else 0
    return round(correlation, 4)

def main(csvfile, ageGroup, country):
    data, headers = readCSV(csvfile)
    OP1 = sortUsersByCountry(data, headers, country)
    OP2 = uniqueCountries(data, headers, ageGroup)
    OP3 = getAgeStats(data, headers, ageGroup)
    OP4 = popularPlatformAndCorrelation(data, headers)
    return OP1, OP2, OP3, OP4
