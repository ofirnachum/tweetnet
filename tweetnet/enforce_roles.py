import functools

# make this configurable
ROLE_ATTRIBUTE = 'role'

def restrict_to_roles(*roles):
    """
    decorator that wraps a method and makes sure
    the the method can only be called if the
    instance attribute 'role_attribute' is one of the provided ones
    """
    def decorator(f):

        @functools.wraps(f)
        def inner(self, *args, **kwargs):
            try:
                role = getattr(self, ROLE_ATTRIBUTE)
            except AttributeError:
                raise ValueError("%r has no attribute %s" % (self, ROLE_ATTRIBUTE))

            if not role in set(roles):
                raise ValueError("%s can only be called with roles %r, not %s" % (
                    f.func_name,
                    roles,
                    str(role),
                ))

            # Otherwise we're good.
            return f(self, *args, **kwargs)
        return inner

    return decorator
