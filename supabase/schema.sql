-- Chainline 2.0 Database Schema (SRS 2.0 Section 7.1)
-- Run this script first in the Supabase SQL Editor.

create table app_users (
  id uuid primary key default gen_random_uuid(),
  username text unique not null check (username ~ '^[a-z0-9_]{3,20}$'),
  display_name text,
  pin_hash text,
  daily_goal int not null default 2 check (daily_goal between 1 and 10),
  language text not null default 'java' check (language in ('java','python')),
  theme text not null default 'light' check (theme in ('light','evening','dark')),
  created_at timestamptz not null default now()
);

create table progress (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 300),
  status text not null default 'todo' check (status in ('todo','in_progress','done','revisit')),
  mistake boolean not null default false,
  notes text not null default '',
  solved_at timestamptz,
  updated_at timestamptz not null default now(),
  primary key (user_id, question_seq)
);

create table reviews (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 300),
  due_date date not null,
  step int not null default 0,
  source text not null default 'auto' check (source in ('auto','manual')),
  primary key (user_id, question_seq)
);

create table activity (
  user_id uuid references app_users(id) on delete cascade,
  day date not null,
  solved_count int not null default 0,
  primary key (user_id, day)
);

alter table app_users enable row level security;
alter table progress enable row level security;
alter table reviews enable row level security;
alter table activity enable row level security;
revoke all on app_users, progress, reviews, activity from anon, authenticated;
