CREATE TABLE IF NOT EXISTS users (
  UserID integer PRIMARY KEY,
  Active integer DEFAULT 1,
  XP integer DEFAULT 0,
  Level integer DEFAULT 0,
  XPLock text DEFAULT CURRENT_TIMESTAMP,
  Currency integer DEFAULT 0,
  CurrencyLock text DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS roles (
  EmoteID integer PRIMARY KEY,
  RoleID integer DEFAULT 0
)
