-- Safe to re-run. Run in the Supabase SQL editor.
create index if not exists messages_group_created_idx on public.messages (group_id, created_at desc);
create index if not exists memberships_user_group_idx on public.memberships (user_id, group_id);
create index if not exists memberships_group_user_idx on public.memberships (group_id, user_id);

alter table public.messages alter column created_at set default now();

alter table public.messages enable row level security;
grant select on table public.messages to authenticated;

drop policy if exists "members can read messages" on public.messages;
create policy "members can read messages" on public.messages
for select to authenticated
using (exists (
  select 1 from public.memberships m
  where m.group_id = messages.group_id and m.user_id = auth.uid()
));

do $$ begin
  alter publication supabase_realtime add table public.messages;
exception when duplicate_object then null; end $$;
