
from app.domain.timezone_service import get_current_time_by_timezone

print(get_current_time_by_timezone("Europe/Greece"))
print(get_current_time_by_timezone("NARNIA"))