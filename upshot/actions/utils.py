from django.contrib.contenttypes.models import ContentType
import datetime
from django.utils import timezone
from .models import Action


def create_action(user, verb, target=None):
    """
    Creates a record of what action user made
    """
    # check for any similar action made in last minute
    now = timezone.now()
    last_minute = now - datetime.timedelta(seconds=60)
    similar_actions = Action.objects.filter(
        user_id=user.id, verb=verb, created__gte=last_minute
    )

    # checks similar action for same object
    if target:
        target_ct = ContentType.objects.get_for_model(target)
        similar_actions = similar_actions.filter(
            target_ct=target_ct, target_id=target.id
        )

    # if no existing actions found from last minute till now
    if not similar_actions:
        action = Action(user=user, verb=verb, target=target)
        action.save()
        return True

    return False
