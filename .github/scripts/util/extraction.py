import re


def extract_time(issue_body):
    match = re.search(r'TOTAL TIME SPENT ON THIS ISSUE BY ASSIGNEE =\s*(\d{1,2}:\d{2})', issue_body)
    try:
        hours, minutes = map(int, match.group(1).split(':'))
        return hours + minutes / 60
    except (AttributeError, ValueError) as e:
        raise ValueError('Time not found in issue body.') from e
    

def extract_title_price(issue_title):
    match = re.search(r'\[.*?\]\[\$(\d+\.?\d*)\]', issue_title)
    try:
        return float(match.group(1))
    except (AttributeError, ValueError) as e:
        raise ValueError('Price not found in issue title.') from e


def extract_expected_price(issue_body):
    match = re.search(r'USD:\**\s*\$?(\d+\.?\d*)', issue_body)
    try:
        return float(match.group(1))
    except (AttributeError, ValueError) as e:
        raise ValueError('Bonus price not found in issue body.') from e