import os

from celery import Celery
from kombu import Queue, Exchange

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

app = Celery("safe_transaction_service")

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object("django.conf:settings")
# app.config_from_object("django.conf:settings", namespace="CELERY")


############################################################################

# default:
app.conf.task_default_queue = 'default'
app.conf.task_default_exchange_type = 'direct'
app.conf.task_default_routing_key = 'default'
app.conf.task_always_eager = False
app.conf.timezone = "UTC"
app.conf.enable_utc = True

# celery queues
app.conf.task_queues = {
    Queue("default", Exchange("default"), routing_key="default"),
    Queue("tokens", Exchange("tokens"), routing_key="tokens"),
    Queue("notifications", Exchange("notifications"), routing_key="notifications"),
    Queue("contracts", Exchange("contracts"), routing_key="contracts"),

    #
    # history group:
    #
    Queue("history.index_new_proxies_task", Exchange("history"), routing_key="history.index_new_proxies_task"),
    Queue("history.index_internal_txs_task", Exchange("history"), routing_key="history.index_internal_txs_task"),
    Queue("history.index_safe_events_task", Exchange("history"), routing_key="history.index_safe_events_task"),
    Queue("history.index_erc20_events_task", Exchange("history"), routing_key="history.index_erc20_events_task"),
    Queue("history.process_decoded_internal_txs_task", Exchange("history"),
          routing_key="history.process_decoded_internal_txs_task"),
    Queue("history.process_decoded_internal_txs_for_safe_task", Exchange("history"),
          routing_key="history.process_decoded_internal_txs_for_safe_task"),
    Queue("history.check_reorgs_task", Exchange("history"), routing_key="history.check_reorgs_task"),
    Queue("history.send_webhook_task", Exchange("history"), routing_key="history.send_webhook_task"),
    Queue("history.index_contract_metadata", Exchange("history"), routing_key="history.index_contract_metadata"),
}

# celery routes
app.conf.task_routes = {
    #
    # tokens tasks: mapper taskFn with queue.
    #
    "safe_transaction_service.tokens.tasks.calculate_token_eth_price_task": {
        "queue": "tokens",
        "routing_key": "tokens"
    },
    "safe_transaction_service.tokens.tasks.fix_pool_tokens_task": {
        "queue": "tokens",
        "routing_key": "tokens"
    },
    "safe_transaction_service.tokens.tasks.get_token_info_from_blockchain": {
        "queue": "tokens",
        "routing_key": "tokens"
    },

    #
    # notifications tasks:
    #
    "safe_transaction_service.notifications.tasks.send_notification_task": {
        "queue": "notifications",
        "routing_key": "notifications"
    },
    "safe_transaction_service.notifications.tasks.send_notification_owner_task": {
        "queue": "notifications",
        "routing_key": "notifications"
    },

    #
    # contracts
    #
    "safe_transaction_service.contracts.tasks.index_contracts_metadata_task": {
        "queue": "contracts",
        "routing_key": "contracts"
    },

    #
    # history
    #
    "safe_transaction_service.history.tasks.index_new_proxies_task": {
        "queue": "history.index_new_proxies_task",
        "routing_key": "history.index_new_proxies_task"
    },

    "safe_transaction_service.history.tasks.index_internal_txs_task": {
        "queue": "history.index_internal_txs_task",
        "routing_key": "history.index_internal_txs_task"
    },
    "safe_transaction_service.history.tasks.index_safe_events_task": {
        "queue": "history.index_safe_events_task",
        "routing_key": "history.index_safe_events_task"
    },
    "safe_transaction_service.history.tasks.index_erc20_events_task": {
        "queue": "history.index_erc20_events_task",
        "routing_key": "history.index_erc20_events_task"
    },
    "safe_transaction_service.history.tasks.process_decoded_internal_txs_task": {
        "queue": "history.process_decoded_internal_txs_task",
        "routing_key": "history.process_decoded_internal_txs_task"
    },
    "safe_transaction_service.history.tasks.process_decoded_internal_txs_for_safe_task": {
        "queue": "history.process_decoded_internal_txs_for_safe_task",
        "routing_key": "history.process_decoded_internal_txs_for_safe_task"
    },
    "safe_transaction_service.history.tasks.check_reorgs_task": {
        "queue": "history.check_reorgs_task",
        "routing_key": "history.check_reorgs_task"
    },
    "safe_transaction_service.history.tasks.send_webhook_task": {
        "queue": "history.send_webhook_task",
        "routing_key": "history.send_webhook_task"
    },
    "safe_transaction_service.history.tasks.index_contract_metadata": {
        "queue": "history.index_contract_metadata",
        "routing_key": "history.index_contract_metadata"
    },
}

############################################################################


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()
