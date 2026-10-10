-- Run once in SQL Editor: short links for the Route tab. Share link, Email and the QR code on the printed route sheet carry
-- #r=<code>; the code opens a snapshot of the route (the unit, the logged codes and readings it needs, the tech's answers so far).
-- A snapshot never holds a customer's name or address. The table has no row policies: the two functions below are the only way in,
-- so anyone holding a code can open that one route, and nobody can list or change the others.
create table if not exists public.routes (
  code        text primary key,                -- 10 random hex characters
  created_at  timestamptz not null default now(),
  app_version text,
  device_id   text,
  snapshot    jsonb not null,
  constraint routes_snapshot_size check (pg_column_size(snapshot) < 200000)
);
alter table public.routes enable row level security;

create or replace function public.route_put(p_snapshot jsonb, p_app text default null, p_device text default null)
returns text language plpgsql security definer set search_path = public as $$
declare c text;
begin
  if p_snapshot is null or jsonb_typeof(p_snapshot) <> 'object' or pg_column_size(p_snapshot) >= 200000 then
    raise exception 'route snapshot missing or too large';
  end if;
  loop
    c := substr(replace(gen_random_uuid()::text, '-', ''), 1, 10);
    begin
      insert into public.routes (code, app_version, device_id, snapshot) values (c, left(p_app, 20), left(p_device, 64), p_snapshot);
      return c;
    exception when unique_violation then
      -- that code is taken: draw another
    end;
  end loop;
end $$;

create or replace function public.route_get(p_code text)
returns jsonb language sql stable security definer set search_path = public as $$
  select snapshot from public.routes where code = p_code
$$;

revoke all on function public.route_put(jsonb, text, text) from public;
revoke all on function public.route_get(text) from public;
grant execute on function public.route_put(jsonb, text, text) to anon, authenticated;
grant execute on function public.route_get(text) to anon, authenticated;
notify pgrst, 'reload schema';
