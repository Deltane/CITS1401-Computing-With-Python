#24211939 github link:

def parse_csv(file_path):
    """
    Parse the CSV file into a list of records as dictionaries.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        tuple: A tuple containing headers as a list and data as a list of dictionaries.
    """
    # trying to open the file
    try:
        with open(file_path, 'r') as file:
            # reading the first line for headers
            headers = file.readline().strip().lower().split(',')
            # reading the rest of the lines for data
            # ensure each line has the same number of fields as the header.
            # reference: https://stackoverflow.com/questions/24662571/python-import-csv-to-list
            data = [dict(zip(headers, line.strip().split(','))) for line in file if
                    len(line.strip().split(',')) == len(headers)]
            # ensure the data is not empty.
        return headers, data
    except IOError:
        # handle file not found or other io errors.
        print(f"error opening file: {file_path}")
        return [], []


def validate_record(record):
    """
    Check if a record is valid by confirming age, ID, and engagement score criteria.

    Args:
        record (dict): A dictionary containing a single record data.

    Returns:
        bool: True if the record is valid, False otherwise.
    """
    # make sure age is a digit and non-negative, id is alphanumeric, and engagement score is a float.
    # works for both student and non-student records.
    # reference: https://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float
    return (
            record.get('age', '').isdigit() and int(record['age']) >= 0 and
            record.get('id', '').isalnum() and
            record.get('engagement_score', '').replace('.', '', 1).isdigit()
    )


def calculate_mean(data):
    return sum(data) / len(data) if data else 0.0


def calc_standard_dev(data, mean):
    """Computes the standard deviation for a set of data, a measure of data spread."""
    # reference: project 1 solution
    if len(data) < 2:
        return 0.0
    variance = sum((x - mean) ** 2 for x in data) / (len(data) - 1)
    return variance ** 0.5


def cosine_similarity(vec1, vec2):
    """Determines the cosine similarity between two vectors, a measure of orientation and not magnitude."""
    # calculating dot product
    # reference: https://www.machinelearningplus.com/nlp/cosine-similarity/
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
    magnitude2 = sum(b ** 2 for b in vec2) ** 0.5
    return dot_product / (magnitude1 * magnitude2) if magnitude1 and magnitude2 else 0


def cohen_d(x, y):
    """Calculates Cohen's d, an effect size used to indicate the standardised difference between two means."""
    # get the length of both lists
    nx, ny = len(x), len(y)
    # calculate the mean of both lists
    mean_x, mean_y = calculate_mean(x), calculate_mean(y)
    # calculate the standard deviation of both lists
    std_x, std_y = calc_standard_dev(x, mean_x), calc_standard_dev(y, mean_y)
    # calculate the pooled standard deviation
    # reference: https://www.statisticshowto.com/probability-and-statistics/hypothesis-testing/effect-size/
    pooled_std = (((nx - 1) * std_x ** 2 + (ny - 1) * std_y ** 2) / (nx + ny - 2)) ** 0.5
    # calculate cohen's d and round it to 4 decimal places
    return round((mean_x - mean_y) / pooled_std, 4) if pooled_std else 0


def main(csvfile):
    """Drives the data parsing, processing, and analysis for the given CSV file."""
    # parse the csv file
    headers, data = parse_csv(csvfile)
    # if no data is returned, return None
    if not data:
        return None

    # initialize dictionaries and lists to store data
    students = {}
    non_students = {}
    platforms = {}
    age_students = []
    income_students = []
    engagement_students = []
    age_non_students = []
    income_non_students = []
    engagement_non_students = []

    # process each record in the dataset
    for record in data:
        # validate the record
        if not validate_record(record):
            continue

        # extract data from the record
        age, time_spent, engagement_score = int(record['age']), float(record['time_spent_hour']), float(
            record['engagement_score'])
        income, engagement_time = float(record['income']), (time_spent * engagement_score) / 100
        group_key = record['id'].lower()
        platform = record['platform'].lower()

        # organise data into students and non-students
        target_dict = students if record['profession'].lower() == 'student' else non_students
        target_dict[group_key] = [age, time_spent, engagement_score]
        age_list = age_students if record['profession'].lower() == 'student' else age_non_students
        income_list = income_students if record['profession'].lower() == 'student' else income_non_students
        engagement_list = engagement_students if record['profession'].lower() == 'student' else engagement_non_students
        age_list.append(age)
        income_list.append(income)
        engagement_list.append(engagement_time)

        # collect data by platform for later aggregation
        platforms.setdefault(platform, []).append(engagement_time)
        # reference: https://stackoverflow.com/questions/1024847/add-new-keys-to-a-dictionary
        # If the key does not exist, it adds the key with a default value and then returns that default value.

    # prepare the output
    OP1 = [students, non_students]
    OP2 = {k: [round(sum(v), 4), round(calculate_mean(v), 4), round(calc_standard_dev(v, calculate_mean(v)), 4)] for
           k, v in platforms.items()}
    OP3 = [round(cosine_similarity(age_students, income_students), 4),
           round(cosine_similarity(age_non_students, income_non_students), 4)]
    OP4 = cohen_d(engagement_students, engagement_non_students)
    return OP1, OP2, OP3, OP4