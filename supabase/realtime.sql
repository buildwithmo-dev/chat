-- Run this in the Supabase SQL editor after confirming the existing table names/columns.
-- The Django API remains the trusted writer; the browser only needs read access
-- so Supabase Realtime can deliver new messages to authenticated members.

alter table public.messages enable row level security;

grant select on table public.messages to authenticated;

 drop policy if exists "members can read messages" on public.messages;
create policy "members can read messages"
on public.messages
for select
to authenticated
using (
  exists (
    select 1
    from public.memberships m
    where m.group_id = messages.group_id
      and m.user_id = auth.uid()
  )
);

-- Make sure the messages table is part of the Realtime publication.
alter publication supabase_realtime add table public.messages;
