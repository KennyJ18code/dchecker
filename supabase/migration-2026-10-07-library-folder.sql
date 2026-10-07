-- Run once in SQL Editor: recordings are now filed as plain CSV under library/<year>/<month>/ instead of gzipped under anon/<device>/.
create policy "recordings files anon insert library" on storage.objects for insert to anon
  with check (bucket_id = 'recordings' and (storage.foldername(name))[1] = 'library');
