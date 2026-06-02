-- Daily active accounts, sourced from raw login events.
select
    date_trunc('day', event_ts) as activity_date,
    count(distinct account_id) as daily_active_accounts
from {{ source('raw_auth_events', 'login_attempted') }}
where status = 'success'
group by 1
