from django.dispatch import Signal

# providing_args mandates the sender and receiver to contain these arguments otherwise raises a TypeError
quote_created = Signal(providing_args=["instance", "user"])
quote_modified = Signal(providing_args=["instance", "user"])
quote_deleted = Signal(providing_args=["instance", "user"])
