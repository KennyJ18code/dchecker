-- Run once in SQL Editor: job details (tech, customer, address) on recordings and call notes.
alter table public.recordings add column if not exists address text;
alter table public.calls add column if not exists customer text;
alter table public.calls add column if not exists address text;
