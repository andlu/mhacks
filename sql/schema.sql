CREATE TABLE users(
  username VARCHAR(20) NOT NULL,    -- Username of user
  fullname VARCHAR(40) NOT NULL,    -- Fullname of user
  password VARCHAR(256) NOT NULL,   -- Password of user
  PRIMARY KEY(username)
);
CREATE TABLE playlists(
  playlistID INT,                         -- A unique number we create associated to the playlist
  username VARCHAR(20) NOT NULL,          -- Username of user who created playlist
  title VARCHAR(256) NOT NULL,            -- Title of playlist
  id VARCHAR(256) NOT NULL,               -- id of playlist on platform
  url VARCHAR(256) NOT NULL,              -- url of playlist on platform
  platform VARCHAR(1) NOT NULL,           -- Indicates which platform the playlist is from
  platformUsername VARCHAR(256) NOT NULL, -- Username of the user on the specific platform
  PRIMARY KEY(id, platform),
  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);
CREATE TABLE songs()
  songID INT,                             -- A unique number we create associated to the song 
  songname VARCHAR(256) NOT NULL,         -- Name of the song
  artist VARCHAR(256) NOT NULL,           -- Artist of the song
  album VARCHAR(256) NOT NULL,            -- Album of the song
  PRIMARY KEY(songID)
);
CREATE TABLE playListSongs(
  songID INT NOT NULL,                    -- The songID of the song based on the songs table
  username VARCHAR(20) NOT NULL,          -- Username of the user
  databasePlaylistID INT NOT NULL,        -- The playlist id of where the song is from in our database
  playlistID VARCHAR(256) NOT NULL,       -- The ID of the playlist from the platform
  PRIMARY KEY(songID, databasePlaylistID),
  FOREIGN KEY (playlist) REFERENCES playlists(title) ON DELETE CASCADE,
  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);

-- To find all songs associated with a playlist, query username and playlist on playListSongs
-- This should return a dictionary with all the songIDs
-- Iterate through songs for the song associated with the songID
