-- Run once in SQL Editor: call notes (why the customer called, what was found, what fixed it), one row per save, latest wins.
create table if not exists public.calls (
  id             bigint generated always as identity primary key,
  created_at     timestamptz not null default now(),
  device_id      text,
  sha256         text,                 -- the recording the notes belong to
  tech_name      text,                 -- the name typed on the phone (a label, not a login)
  complaint      text,                 -- the customer's reason for calling, in their words
  complaint_cats text[],               -- quick picks: No cooling, No heat, Not keeping up, Humid / sticky, Icing, Noise, Water / leak, High bill, Error code, Short cycling, Maintenance, Other
  found          text,                 -- what the tech found
  fix            text,                 -- what fixed it
  outcome        text,                 -- Fixed, Parts ordered, Monitoring, No fault found, Referred
  model          text,
  app_version    text
);
alter table public.calls enable row level security;
create policy "calls anon insert" on public.calls for insert to anon, authenticated with check (true);
create policy "calls auth read"   on public.calls for select to authenticated using (true);
create index if not exists calls_sha_idx on public.calls (sha256, created_at desc);
