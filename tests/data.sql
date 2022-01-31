INSERT INTO pdf_content (metadata, pdf_name, uploaded, author, body, title)
VALUES
  ('test' || x'0a' || 'metadata', 'test name', '2018-01-01 00:00:00', 'test author',  'test' || x'0a' || 'body', 'test title');