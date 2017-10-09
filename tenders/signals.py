from django.dispatch import Signal

# providing_args mandates the sender and receiver to contain these arguments otherwise raises a TypeError
tender_created = Signal(providing_args=["instance", "user"])
tender_modified = Signal(providing_args=["instance", "user"])
tender_deleted = Signal(providing_args=["instance", "user"])
