select event_type, count(event_type) as event 
from clickstream
group by event_type
order by event desc
