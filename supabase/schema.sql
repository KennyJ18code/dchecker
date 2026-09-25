-- D-Checker Cycle Viewer · fleet sync schema
-- Run once in Supabase → SQL Editor. Then create tech users under Authentication → Users
-- (email + password; "Auto confirm user" on), and copy Project URL + anon key from Settings → API
-- into the app's Settings → Fleet sync.

create extension if not exists pgcrypto;

-- one row per recording a tech opened in the app
create table if not exists public.recordings (
  id            uuid primary key default gen_random_uuid(),
  created_at    timestamptz not null default now(),
  uploaded_by   uuid not null default auth.uid() references auth.users(id),
  tech_email    text,
  file_name     text not null,
  file_path     text,                 -- storage path in bucket "recordings"
  sha256        text not null,        -- dedupe: same file uploaded twice = one row
  site          text,                 -- customer.txt field 2
  customer      text,                 -- customer.txt field 4
  tech_name     text,                 -- customer.txt field 8
  model         text,                 -- model file named in header.txt
  started_at    timestamptz,
  ended_at      timestamptz,
  row_count     int,
  interval_s    numeric,
  equipment     jsonb,                -- {out:'hp'|'ac', in:'furnace'|'strips'|'ah', auto:true/false}
  summary       jsonb,                -- runs, signature/fault counts, steady minutes, worst readings
  app_version   text,
  unique (uploaded_by, sha256)
);

-- lightweight usage telemetry
create table if not exists public.events (
  id            bigint generated always as identity primary key,
  created_at    timestamptz not null default now(),
  uploaded_by   uuid not null default auth.uid() references auth.users(id),
  session_id    text,
  kind          text not null,        -- session_start, view, pin, custom_tag, equipment, layout, open_log, ...
  detail        jsonb,
  app_version   text,
  device        text
);

-- tech verdict on what the app said
create table if not exists public.feedback (
  id            bigint generated always as identity primary key,
  created_at    timestamptz not null default now(),
  uploaded_by   uuid not null default auth.uid() references auth.users(id),
  recording_id  uuid references public.recordings(id) on delete cascade,
  verdict       text not null check (verdict in ('right','wrong','unclear')),
  note          text
);

alter table public.recordings enable row level security;
alter table public.events     enable row level security;
alter table public.feedback   enable row level security;

-- every signed-in tech can add rows; the whole shop can read them
create policy "recordings insert own" on public.recordings for insert to authenticated with check (uploaded_by = auth.uid());
create policy "recordings read all"   on public.recordings for select to authenticated using (true);
create policy "events insert own"     on public.events     for insert to authenticated with check (uploaded_by = auth.uid());
create policy "events read all"       on public.events     for select to authenticated using (true);
create policy "feedback insert own"   on public.feedback   for insert to authenticated with check (uploaded_by = auth.uid());
create policy "feedback read all"     on public.feedback   for select to authenticated using (true);

-- private bucket for the raw .tgz / .csv files
insert into storage.buckets (id, name, public) values ('recordings', 'recordings', false)
  on conflict (id) do nothing;
create policy "recordings files insert" on storage.objects for insert to authenticated
  with check (bucket_id = 'recordings');
create policy "recordings files read" on storage.objects for select to authenticated
  using (bucket_id = 'recordings');

create index if not exists recordings_created_idx on public.recordings (created_at desc);
create index if not exists events_created_idx on public.events (created_at desc);
