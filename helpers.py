from dateutil.relativedelta import relativedelta
import datetime

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def get_default_cafe_thumbnail() -> bytes:
    """Get default cafe thumbnail in bytes format."""
    with open("static/images/base_cafe_thumbnail.jpg", "rb") as thumbnail:
        return thumbnail.read()


def split_list(lst: list, n: int):
    """Yield successive n-sized chunks from lst."""
    lists = []
    for i in range(0, len(lst), n):
        lists.append(lst[i:i + n])
    return lists


def allowed_file(filename: str) -> bool:
    """Check if provided filename has proper extension from ALLOWED_EXTENSIONS."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_last_updated_string(update_time: datetime.datetime) -> str:
    """Get formatted string of timedelta between cafe create time to now."""
    delta = relativedelta(dt1=datetime.datetime.now(), dt2=update_time)
    formatted_delta = ""
    if delta.years:
        if delta.years > 1:
            formatted_delta += f"{delta.years} years ago"
        else:
            formatted_delta += f"{delta.years} year ago"
    elif delta.months:
        if delta.months > 1:
            formatted_delta += f"{delta.months} months ago"
        else:
            formatted_delta += f"{delta.months} month ago"
    elif delta.weeks:
        if delta.weeks > 1:
            formatted_delta += f"{delta.weeks} weeks ago"
        else:
            formatted_delta += f"{delta.weeks} week ago"
    elif delta.days:
        if delta.days > 1:
            formatted_delta += f"{delta.days} days ago"
        else:
            formatted_delta += f"{delta.days} day ago"
    elif delta.hours:
        if delta.hours > 1:
            formatted_delta += f"{delta.hours} hours ago"
        else:
            formatted_delta += f"{delta.hours} hour ago"
    elif delta.minutes:
        if delta.minutes > 1:
            formatted_delta += f"{delta.minutes} minutes ago"
        else:
            formatted_delta += f"{delta.minutes} minute ago"
    else:
        formatted_delta += "<1 minute ago"
    return formatted_delta
