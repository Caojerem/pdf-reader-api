DROP TABLE IF EXISTS pdf;
DROP TABLE IF EXISTS pdf_content;

CREATE TABLE pdf (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pdf_name TEXT UNIQUE NOT NULL,
);

CREATE TABLE pdf_content (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  pdf_id INTEGER NOT NULL,
  uploaded TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  author TEXT NOT NULL,
  body TEXT NOT NULL,
  FOREIGN KEY (pdf_id) REFERENCES pdf (id)
);