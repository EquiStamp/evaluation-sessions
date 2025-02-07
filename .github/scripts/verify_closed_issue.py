import os
import pathlib
import re
import sys

import requests

from util.extraction import (extract_expected_price, extract_time,
                             extract_title_price)


def check_time(issue, success_messages, error_messages):
    """Verify the time can spent can be extracted from the issue."""
    try:
        time = extract_time(issue['body'])
        success_messages.append(f'Time spent on issue: {time:.2f} hours')
        return True
    except ValueError as e:
        error_messages.append(str(e))
        return False


def check_expected_price(issue, success_messages, error_messages):
    """Verify the expected price can be extracted from the issue."""
    try:
        expected_price = extract_expected_price(issue['body'])
        success_messages.append(f'Expected/bonus price: ${int(expected_price)}')
        return True
    except ValueError as e:
        error_messages.append(str(e))
        return False


def check_charge_labels(issue, success_messages, error_messages):
    """Verify that the issue has exactly one charge-to label."""
    charge_labels = [label for label in issue['labels'] if label.startswith('charge-to-')]

    if len(charge_labels) == 1:
        success_messages.append(f'Charge label found: {charge_labels[0]}')
        return True

    if len(charge_labels) == 0:
        error_messages.append(f'No charge label found: had {len(issue["labels"])} labels.')
        return False

    error_messages.append(f'Multiple charge labels found: {charge_labels}')
    return False


def check_assignee(issue, success_messages, error_messages):
    """Verify that the issue has one and only one assignee."""
    if len(issue['assignees']) == 1:
        success_messages.append(f'Assignee found: {issue["assignees"][0]}')
        return True

    if len(issue['assignees']) == 0:
        error_messages.append('No assignee found.')
        return False

    error_messages.append(f'Multiple assignees found: {issue["assignees"]}')
    return False


def update_github_issue_title_price(issue, new_price, token):
    """Edit the issue title on GitHub to the given price."""
    updated_title = re.sub(r'\[\$\d+\.?\d*\]', f'[${round(new_price)}]', issue['title'])

    url = f'https://api.github.com/repos/{issue["repo"]}/issues/{issue["number"]}'
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    response = requests.patch(url, headers=headers, json={'title': updated_title})

    if response.status_code == 200:
        print(f'Successfully updated issue title to: {updated_title}')
    else:
        print(f'Failed to update issue title. Status code: {response.status_code}, Response: {response.text}')


def check_and_update_title_price(issue, usd_rate, token, success_messages, error_messages):
    """Check if the title price is lower than the hourly price and update if so."""
    try:
        title_price = int(extract_title_price(issue['title']))
        bonus_price = int(extract_expected_price(issue['body']))
        time = extract_time(issue['body'])
        hourly_price = round(time * usd_rate)
        paid_price = 0

        if hourly_price < bonus_price:
            paid_price = bonus_price
            bonus_amount = bonus_price - hourly_price
            success_messages.append(f'Issue completed with bonus. Bonus price: ${bonus_price}, but completed in {time:.2f} hours. Bonus amount: ${bonus_amount}')
        else:
            paid_price = hourly_price
            success_messages.append(f'Issue completed without bonus. Total price: {time:.2f} hours * ${usd_rate} = ${hourly_price}')

        if title_price != paid_price:
            print('Updating issue title...')
            update_github_issue_title_price(issue, paid_price, token)
            success_messages.append(f'Updated issue title from ${title_price} to ${paid_price}')

        return True
    except ValueError as e:
        error_messages.append(str(e))
        return False


def perform_all_checks(issue, usd_rate, token, success_messages, error_messages):   
    time_ok = check_time(issue, success_messages, error_messages)
    bonus_price_ok = check_expected_price(issue, success_messages, error_messages)
    labels_ok = check_charge_labels(issue, success_messages, error_messages)
    assignee_ok = check_assignee(issue, success_messages, error_messages)

    if time_ok and bonus_price_ok:
        print('Time and bonus price found, updating price in title...')
        title_ok = check_and_update_title_price(issue, usd_rate, token, success_messages, error_messages)
        if not title_ok:
            return False
    return time_ok and bonus_price_ok and labels_ok and assignee_ok


def get_issue_data():
    return {
        'number': os.getenv('ISSUE_NUMBER'),
        'title': os.getenv('ISSUE_TITLE'),
        'body': os.getenv('ISSUE_BODY'),
        'labels': os.getenv('ISSUE_LABELS').split(','),
        'assignees': os.getenv('ISSUE_ASSIGNEES').split(',') if os.getenv('ISSUE_ASSIGNEES') else [],
        'repo': os.getenv('REPOSITORY')
    }


def main():
    issue = get_issue_data()
    token = os.getenv('GITHUB_TOKEN')
    usd_rate = 50
    success_messages = []
    error_messages = []

    checks_ok = perform_all_checks(issue, usd_rate, token, success_messages, error_messages)

    if success_messages:
        success_messages.insert(0, 'These checks passed:')
    pathlib.Path('success_messages.txt').write_text('\n- '.join(success_messages), encoding='utf-8')

    if checks_ok:
        print('Checks passed, issue closed successfully!')
    else:
        print('Checks failed, reopening issue...')
        error_messages.insert(0, 'Reopening issue due to failed verification:')
        pathlib.Path('error_messages.txt').write_text('\n- '.join(error_messages), encoding='utf-8')
        sys.exit(1)


if __name__ == '__main__':
    main()