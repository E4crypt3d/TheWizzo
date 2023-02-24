from users.models import User
import random


def get_suggestions(current_user):
    suggestions = []
    user = User.objects.prefetch_related(
        'profile', 'follows').get(username=current_user)
    for following in user.profile.follows.all():
        for follow_following in following.profile.follows.all():
            if follow_following in suggestions or follow_following == user:
                continue
            if follow_following in user.profile.follows.all():
                continue
            suggestions.append(follow_following)
    if len(suggestions) >= 5:
        return random.sample(suggestions, 5)
    else:
        return suggestions
