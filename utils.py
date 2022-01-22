from functools import reduce
from collections import OrderedDict
from rich.console import Console

import config
from config import EventResponseKeys


console = Console()


def _is_valid_event(event):
    if not event.get(EventResponseKeys.PERFORMER) or not event[EventResponseKeys.PERFORMER].get(EventResponseKeys.USER_EDIT_COUNT):
        return False
    if event[EventResponseKeys.PERFORMER][EventResponseKeys.USER_IS_BOT]:
        return False
    return True


def _get_updated_domain_wise_performers(domain_wise_performers, event):
    domain = event[EventResponseKeys.META][EventResponseKeys.DOMAIN]
    performer_details = {
        'user_name': event[EventResponseKeys.PERFORMER][EventResponseKeys.USER_TEXT],
        'user_edit_count': event[EventResponseKeys.PERFORMER][EventResponseKeys.USER_EDIT_COUNT],
    }

    domain_wise_performers[domain].append(performer_details) if domain in domain_wise_performers else domain_wise_performers.update({domain: [performer_details]})

    return domain_wise_performers


def _get_domains_report(domain_wise_performers):
    domains_report = ""
    for key, value in domain_wise_performers.items():
        domains_report += f"[bold green]{key}[/bold green]: {len(value)}\n"

    return domains_report


def _get_users_report(domain_wise_performers):
    users_report = ""

    en_wikipedia_users = domain_wise_performers[config.EN_WIKIPEDIA_DOMAIN_NAME] if config.EN_WIKIPEDIA_DOMAIN_NAME in domain_wise_performers else []
    if len(en_wikipedia_users):
        en_wikipedia_users.sort(key=lambda user: user['user_edit_count'] or 0, reverse=True)
        for user in en_wikipedia_users:
            users_report += f"[bold yellow]{user['user_name']}[/bold yellow]: {user['user_edit_count']}\n"
    else:
        users_report += f"No updates in [i][bold red]{config.EN_WIKIPEDIA_DOMAIN_NAME}[/bold red][/i]\n"

    return users_report


def print_reports(offset, events):
    console.print(f'Minute {offset+1} Report - Minute {max(0, offset - config.NUM_OF_VALID_PAST_EVENTS_FOR_REPORTS + 1)}-{offset + 1} data', style="red bold")

    filtered_events = list(filter(_is_valid_event, events))
    domain_wise_performers = dict(reduce(_get_updated_domain_wise_performers, filtered_events, {}))
    domain_wise_performers = OrderedDict(sorted(domain_wise_performers.items()))

    domains_report = _get_domains_report(domain_wise_performers)
    users_report = _get_users_report(domain_wise_performers)

    console.print(f"Total number of Wikipedia Domains Updated: {len(domain_wise_performers)}", style="blue bold")
    console.print(domains_report)
    console.print(f"\nUsers who made changes to [i][bold cyan]{config.EN_WIKIPEDIA_DOMAIN_NAME}[/bold cyan][/i]", style="magenta bold")
    console.print(users_report)
