from activitypub.activities.objects import ALLOWED_TYPES, Object, Actor
from activitypub.activities.objects import Person, Note
from activitypub.activities import errors

from copy import copy

class Activity(Object):

    attributes = Object.attributes + ["actor", "object"]
    type = "Activity"

    def get_audience(self):
        audience = []
        for attr in ["to", "bto", "cc", "bcc", "audience"]:
            value = getattr(self, attr, None)
            if not value:
                continue

            if isinstance(value, str):
                value = [value]
            audience += value
        return set(audience)

    def strip_audience(self):
        new = copy(self)
        if getattr(new, "bto", None):
            delattr(new, "bto")
        if getattr(new, "bcc", None):
            delattr(new, "bcc")
        return new

    def validate(self):
        pass

class Create(Activity):

    type = "Create"

    def validate(self):
        msg = None
        if not getattr(self, "actor", None):
            msg = "Invalid Create activity, actor is missing"
        elif not getattr(self, "object", None):
            msg = "Invalid Create activity, object is missing"
        elif not isinstance(self.actor, Actor) and not isinstance(self.actor, str):
            msg = "Invalid actor type, must be an Actor or a string"
        elif not isinstance(self.object, Object):
            msg = "Invalid object type, must be an Object"

        if msg:
            raise errors.ASValidateException(msg)

ALLOWED_TYPES.update({
    "Activity": Activity,
    "Create": Create,
})

