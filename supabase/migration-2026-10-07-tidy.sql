-- Run once in SQL Editor: lets a signed-in reader repoint rows and delete stray files (the Library tab's "Tidy old files").
create policy "recordings auth update" on public.recordings for update to authenticated using (true) with check (true);
create policy "recordings files auth delete" on storage.objects for delete to authenticated using (bucket_id = 'recordings');
