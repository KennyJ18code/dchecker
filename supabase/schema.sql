-- D-Checker Cycle Viewer · shop library schema (v2, 2026-10-05)
-- Run once in a fresh Supabase project: SQL Editor → paste → Run. Then copy Settings → API → Project URL and the
-- publishable (anon) key into the app's S_DEF (sbUrl / sbKey) and rebuild. Recommended: Storage → bucket "recordings" →
-- file size limit 20 MB.
--
-- Anyone using the published app inserts anonymously (publishable key); nothing can be read back with that key.
-- Reading is for signed-in users only (Authentication → Users: you, Andy), from the Supabase dashboard, the API, or the
-- app's Fleet tab on a device that signed in.

create extension if not exists pgcrypto;

-- one row per recording the app analyzed (the decoded CSV, gzipped, is in the bucket at file_path)
create table if not exists public.recordings (
  id            uuid primary key default gen_random_uuid(),
  created_at    timestamptz not null default now(),
  uploaded_by   uuid references auth.users(id),   -- null for anonymous uploads
  device_id     text,                             -- random id the app keeps per device
  tech_email    text,
  tech_name     text,                             -- customer.txt field 8 (the phone app's tech name)
  company       text,                             -- customer.txt field 9
  site          text,                             -- not sent by the app (kept for the old signed-in path)
  customer      text,                             -- not sent by the app
  file_name     text not null,
  file_path     text,
  sha256        text not null unique,             -- of the decoded CSV text: the same recording from two phones is one row
  model         text,                             -- INV_Unitary_DZ6VS etc. from header.txt
  refrigerant   text,                             -- R410A / R32 as the app resolved it
  unit_size     text,                             -- the size the tech picked (RATED key), if any
  started_at    timestamptz,
  ended_at      timestamptz,
  row_count     int,
  interval_s    numeric,
  equipment     jsonb,                            -- {out:'hp'|'ac', auto:true/false}
  summary       jsonb,                            -- findings, runs, signatures, steady minutes, worst readings
  capacity      jsonb,                            -- method, learned displacement, energy, median BTU/h and COP per mode, rest offsets
  app_version   text
);

-- usage: what techs open, pin, change (session_id groups one visit; device_id groups one phone)
create table if not exists public.events (
  id            bigint generated always as identity primary key,
  created_at    timestamptz not null default now(),
  uploaded_by   uuid references auth.users(id),
  device_id     text,
  session_id    text,
  kind          text not null,
  detail        jsonb,
  app_version   text,
  device        text
);

-- a tech's verdict on the app's read of a recording
create table if not exists public.feedback (
  id            bigint generated always as identity primary key,
  created_at    timestamptz not null default now(),
  uploaded_by   uuid references auth.users(id),
  device_id     text,
  recording_id  uuid references public.recordings(id) on delete cascade,
  sha256        text,                             -- the recording, when the row id is not known to the phone
  verdict       text not null check (verdict in ('right','wrong','unclear')),
  note          text,
  app_version   text
);

-- grille readings a tech typed, paired with what the app calculated on that row: the calibration set for the capacity math
create table if not exists public.measurements (
  id            bigint generated always as identity primary key,
  created_at    timestamptz not null default now(),
  device_id     text,
  sha256        text,                             -- recording
  row_time      timestamptz,
  mode          text,
  return_db     numeric, return_wb numeric,
  supply_db     numeric, supply_wb numeric,
  cfm           numeric,                          -- the airflow used (typed, else the blower's logged figure)
  cfm_logged    numeric,
  cfm_typed     boolean,
  air_sensible  numeric,                          -- 1.08 × CFM × ΔT
  air_total     numeric,                          -- 4.5 × CFM × Δh (null without wet bulbs)
  ref_capacity  numeric,                          -- the app's refrigerant-side BTU/h on that row
  ref_grade     text,                             -- good / fair / poor / disp
  ref_cop       numeric,
  expected_dt   numeric,                          -- the app's calculated supply ΔT on that row
  rps           numeric, oat numeric,
  model         text, unit_size text, volts numeric, refrigerant text,
  app_version   text
);

-- the effective displacement the app learned for a model and size on a device
create table if not exists public.calibrations (
  id            bigint generated always as identity primary key,
  created_at    timestamptz not null default now(),
  device_id     text,
  model_key     text,                             -- e.g. DZ6VS/36
  e0            numeric, e1 numeric,              -- effective cc/rev at PR 2.5 and its slope per unit PR
  n             int, pr_lo numeric, pr_hi numeric, fitted boolean,
  sha256        text,
  app_version   text
);

alter table public.recordings   enable row level security;
alter table public.events       enable row level security;
alter table public.feedback     enable row level security;
alter table public.measurements enable row level security;
alter table public.calibrations enable row level security;

-- anyone may add; only signed-in users may read
create policy "recordings anon insert"   on public.recordings   for insert to anon, authenticated with check (true);
create policy "recordings auth read"     on public.recordings   for select to authenticated using (true);
create policy "events anon insert"       on public.events       for insert to anon, authenticated with check (true);
create policy "events auth read"         on public.events       for select to authenticated using (true);
create policy "feedback anon insert"     on public.feedback     for insert to anon, authenticated with check (true);
create policy "feedback auth read"       on public.feedback     for select to authenticated using (true);
create policy "measurements anon insert" on public.measurements for insert to anon, authenticated with check (true);
create policy "measurements auth read"   on public.measurements for select to authenticated using (true);
create policy "calibrations anon insert" on public.calibrations for insert to anon, authenticated with check (true);
create policy "calibrations auth read"   on public.calibrations for select to authenticated using (true);

-- private bucket for the gzipped CSVs; anonymous uploads go under anon/<device>/, signed-in ones under <user id>/
insert into storage.buckets (id, name, public) values ('recordings', 'recordings', false) on conflict (id) do nothing;
create policy "recordings files anon insert" on storage.objects for insert to anon
  with check (bucket_id = 'recordings' and (storage.foldername(name))[1] = 'anon');
create policy "recordings files auth insert" on storage.objects for insert to authenticated
  with check (bucket_id = 'recordings');
create policy "recordings files auth update" on storage.objects for update to authenticated
  using (bucket_id = 'recordings');
create policy "recordings files auth read" on storage.objects for select to authenticated
  using (bucket_id = 'recordings');

create index if not exists recordings_created_idx   on public.recordings (created_at desc);
create index if not exists recordings_model_idx     on public.recordings (model, unit_size);
create index if not exists events_created_idx       on public.events (created_at desc);
create index if not exists measurements_sha_idx     on public.measurements (sha256);
create index if not exists calibrations_model_idx   on public.calibrations (model_key, created_at desc);
