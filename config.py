# Keys in Wikepedia Event Response
class EventResponseKeys:
    META = 'meta'
    DOMAIN = 'domain'
    PERFORMER = 'performer'
    USER_TEXT = 'user_text'
    USER_EDIT_COUNT = 'user_edit_count'
    USER_IS_BOT = 'user_is_bot'


WIKIPEDIA_REVISION_CREATE_STREAMING_URL = 'https://stream.wikimedia.org/v2/stream/revision-create'
EN_WIKIPEDIA_DOMAIN_NAME = 'en.wikipedia.org'

DATA_POLLING_TIME_IN_SEC = 60  # 1 minutes
NUM_OF_VALID_PAST_EVENTS_FOR_REPORTS = 5
