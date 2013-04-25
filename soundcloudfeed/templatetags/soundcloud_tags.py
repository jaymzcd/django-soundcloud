from django import template

register = template.Library()


@register.inclusion_tag('soundcloud/embed.html')
def soundcloud_embed(track_id):
    return {
        'code': track_id,
    }
