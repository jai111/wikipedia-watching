import json
from datetime import datetime
from sseclient import SSEClient as EventSource

import config
import utils


if __name__ == '__main__':

    current_minute = 0
    last_event_req_id = None
    curr_time = datetime.now()

    events_in_current_time_window = []
    events_in_current_minute = []

    for event in EventSource(config.WIKIPEDIA_REVISION_CREATE_STREAMING_URL, last_id=last_event_req_id):
        if event.event == 'message':
            try:
                change = json.loads(event.data)
                last_event_req_id = change['meta']['request_id']
                events_in_current_minute.append(change)

                if (datetime.now() - curr_time).seconds >= config.DATA_POLLING_TIME_IN_SEC:
                    events_in_current_time_window.append(events_in_current_minute)
                    events_in_current_time_window = events_in_current_time_window[len(
                        events_in_current_time_window) - config.NUM_OF_VALID_PAST_EVENTS_FOR_REPORTS:]  # Removing stale event i.e events before 5 mins

                    utils.print_reports(current_minute, sum(events_in_current_time_window, []))

                    curr_time = datetime.now()
                    events_in_current_minute = []
                    current_minute += 1

            except ValueError:
                pass
