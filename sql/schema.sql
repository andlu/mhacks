CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  fullname VARCHAR(40) NOT NULL,
  password VARCHAR(256) NOT NULL,
  PRIMARY KEY(username)
);
CREATE TABLE posts(
  username VARCHAR(20) NOT NULL,
  title VARCHAR(256) NOT NULL,
  id VARCHAR(256) NOT NULL,
  url VARCHAR(256) NOT NULL,
  platform VARCHAR(1) NOT NULL,
  PRIMARY KEY(id, platform),
  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);
