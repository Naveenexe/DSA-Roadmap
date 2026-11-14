-- DSA Roadmap Tracker: Supabase Database Schema and Functions
-- Conforms to SRS Section 6.2 and 6.3

create extension if not exists "pgcrypto";

create table if not exists app_users (
  id uuid primary key default gen_random_uuid(),
  username text unique not null check (username ~ '^[a-z0-9_]{3,20}$'),
  pin_hash text,
  daily_goal int not null default 2 check (daily_goal between 1 and 10),
  language text not null default 'java' check (language in ('java','python')),
  theme text not null default 'dark' check (theme in ('dark','light')),
  created_at timestamptz not null default now()
);

create table if not exists progress (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 300),
  status text not null default 'todo' check (status in ('todo','in_progress','done','revisit')),
  mistake boolean not null default false,
  notes text not null default '',
  solved_at timestamptz,
  updated_at timestamptz not null default now(),
  primary key (user_id, question_seq)
);

create table if not exists reviews (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 300),
  due_date date not null,
  step int not null default 0,
  source text not null default 'auto' check (source in ('auto','manual')),
  primary key (user_id, question_seq)
);

create table if not exists activity (
  user_id uuid references app_users(id) on delete cascade,
  day date not null,
  solved_count int not null default 0,
  primary key (user_id, day)
);

-- Row Level Security: enabled on every table with no anon policies so direct access is denied
alter table app_users enable row level security;
alter table progress enable row level security;
alter table reviews enable row level security;
alter table activity enable row level security;

-- Helper to verify user credentials and return user row
create or replace function internal_verify_user(p_username text, p_pin_hash text)
returns app_users
language plpgsql security definer as $$
declare
  v_user app_users;
begin
  select * into v_user from app_users where username = lower(trim(p_username));
  if not found then
    raise exception 'User not found';
  end if;
  if v_user.pin_hash is not null and v_user.pin_hash <> '' then
    if p_pin_hash is null or v_user.pin_hash <> p_pin_hash then
      raise exception 'Invalid PIN';
    end if;
  end if;
  return v_user;
end;
$$;

-- 1. login_user
create or replace function login_user(p_username text, p_pin_hash text default null)
returns jsonb
language plpgsql security definer as $$
declare
  v_user app_users;
  v_clean_user text;
begin
  v_clean_user := lower(trim(p_username));
  if v_clean_user !~ '^[a-z0-9_]{3,20}$' then
    raise exception 'Username must be 3-20 characters consisting of a-z, 0-9, and underscore';
  end if;

  select * into v_user from app_users where username = v_clean_user;
  if not found then
    insert into app_users (username, pin_hash)
    values (v_clean_user, nullif(p_pin_hash, ''))
    returning * into v_user;
  else
    if v_user.pin_hash is not null and v_user.pin_hash <> '' then
      if p_pin_hash is null or v_user.pin_hash <> p_pin_hash then
        raise exception 'Invalid PIN';
      end if;
    elsif p_pin_hash is not null and p_pin_hash <> '' then
      -- If account had no PIN and one is now provided, associate it
      update app_users set pin_hash = p_pin_hash where id = v_user.id returning * into v_user;
    end if;
  end if;

  return jsonb_build_object(
    'id', v_user.id,
    'username', v_user.username,
    'has_pin', (v_user.pin_hash is not null and v_user.pin_hash <> ''),
    'daily_goal', v_user.daily_goal,
    'language', v_user.language,
    'theme', v_user.theme
  );
end;
$$;

-- 2. get_state
create or replace function get_state(p_username text, p_pin_hash text default null)
returns jsonb
language plpgsql security definer as $$
declare
  v_user app_users;
  v_progress jsonb;
  v_reviews jsonb;
  v_activity jsonb;
begin
  v_user := internal_verify_user(p_username, p_pin_hash);

  select coalesce(jsonb_agg(jsonb_build_object(
    'question_seq', question_seq,
    'status', status,
    'mistake', mistake,
    'notes', notes,
    'solved_at', solved_at,
    'updated_at', updated_at
  )), '[]'::jsonb) into v_progress
  from progress where user_id = v_user.id;

  select coalesce(jsonb_agg(jsonb_build_object(
    'question_seq', question_seq,
    'due_date', due_date,
    'step', step,
    'source', source
  )), '[]'::jsonb) into v_reviews
  from reviews where user_id = v_user.id;

  select coalesce(jsonb_agg(jsonb_build_object(
    'day', day,
    'solved_count', solved_count
  )), '[]'::jsonb) into v_activity
  from activity where user_id = v_user.id;

  return jsonb_build_object(
    'user', jsonb_build_object(
      'id', v_user.id,
      'username', v_user.username,
      'daily_goal', v_user.daily_goal,
      'language', v_user.language,
      'theme', v_user.theme
    ),
    'progress', v_progress,
    'reviews', v_reviews,
    'activity', v_activity
  );
end;
$$;

-- 3. save_progress
create or replace function save_progress(
  p_username text,
  p_pin_hash text,
  p_question_seq int,
  p_status text,
  p_mistake boolean,
  p_notes text,
  p_remind boolean default true,
  p_due_date date default null
)
returns jsonb
language plpgsql security definer as $$
declare
  v_user app_users;
  v_old_status text;
  v_old_solved_at timestamptz;
  v_now timestamptz := now();
  v_today date := current_date;
begin
  v_user := internal_verify_user(p_username, p_pin_hash);

  if p_question_seq < 1 or p_question_seq > 300 then
    raise exception 'Invalid question_seq';
  end if;

  select status, solved_at into v_old_status, v_old_solved_at
  from progress where user_id = v_user.id and question_seq = p_question_seq;

  if p_status = 'done' then
    if v_old_solved_at is null then
      v_old_solved_at := v_now;
      -- Increment today's activity count
      insert into activity (user_id, day, solved_count)
      values (v_user.id, v_today, 1)
      on conflict (user_id, day) do update
      set solved_count = activity.solved_count + 1;
    end if;

    if p_remind then
      insert into reviews (user_id, question_seq, due_date, step, source)
      values (v_user.id, p_question_seq, v_today + 1, 0, 'auto')
      on conflict (user_id, question_seq) do update
      set due_date = v_today + 1, step = 0, source = 'auto';
    end if;
  elsif p_status = 'revisit' then
    insert into reviews (user_id, question_seq, due_date, step, source)
    values (v_user.id, p_question_seq, coalesce(p_due_date, v_today + 1), 0, 'manual')
    on conflict (user_id, question_seq) do update
    set due_date = coalesce(p_due_date, v_today + 1), step = 0, source = 'manual';
  end if;

  insert into progress (user_id, question_seq, status, mistake, notes, solved_at, updated_at)
  values (v_user.id, p_question_seq, p_status, p_mistake, p_notes, v_old_solved_at, v_now)
  on conflict (user_id, question_seq) do update
  set status = p_status,
      mistake = p_mistake,
      notes = p_notes,
      solved_at = coalesce(progress.solved_at, v_old_solved_at),
      updated_at = v_now;

  return get_state(p_username, p_pin_hash);
end;
$$;

-- 4. save_review
create or replace function save_review(
  p_username text,
  p_pin_hash text,
  p_question_seq int,
  p_action text, -- 'recalled', 'forgot', 'delete', 'reschedule'
  p_due_date date default null
)
returns jsonb
language plpgsql security definer as $$
declare
  v_user app_users;
  v_review reviews;
  v_today date := current_date;
  v_next_interval int;
begin
  v_user := internal_verify_user(p_username, p_pin_hash);

  select * into v_review from reviews where user_id = v_user.id and question_seq = p_question_seq;

  if p_action = 'delete' then
    delete from reviews where user_id = v_user.id and question_seq = p_question_seq;
  elsif p_action = 'recalled' then
    if found then
      if v_review.step >= 3 then
        delete from reviews where user_id = v_user.id and question_seq = p_question_seq;
      else
        -- Intervals: step 0 -> next is step 1 (+3 days), step 1 -> step 2 (+7 days), step 2 -> step 3 (+21 days)
        if v_review.step = 0 then v_next_interval := 3;
        elsif v_review.step = 1 then v_next_interval := 7;
        else v_next_interval := 21;
        end if;
        update reviews
        set step = v_review.step + 1, due_date = v_today + v_next_interval
        where user_id = v_user.id and question_seq = p_question_seq;
      end if;
    end if;
  elsif p_action = 'forgot' then
    if found then
      update reviews
      set step = 0, due_date = v_today + 1
      where user_id = v_user.id and question_seq = p_question_seq;
    else
      insert into reviews (user_id, question_seq, due_date, step, source)
      values (v_user.id, p_question_seq, v_today + 1, 0, 'auto');
    end if;
    -- Mark mistake = true in progress table
    update progress set mistake = true where user_id = v_user.id and question_seq = p_question_seq;
  elsif p_action = 'reschedule' then
    insert into reviews (user_id, question_seq, due_date, step, source)
    values (v_user.id, p_question_seq, coalesce(p_due_date, v_today + 1), 0, 'manual')
    on conflict (user_id, question_seq) do update
    set due_date = coalesce(p_due_date, v_today + 1), step = 0, source = 'manual';
  end if;

  return get_state(p_username, p_pin_hash);
end;
$$;

-- 5. save_settings
create or replace function save_settings(
  p_username text,
  p_pin_hash text,
  p_daily_goal int,
  p_language text,
  p_theme text
)
returns jsonb
language plpgsql security definer as $$
declare
  v_user app_users;
begin
  v_user := internal_verify_user(p_username, p_pin_hash);

  update app_users
  set daily_goal = greatest(1, least(10, p_daily_goal)),
      language = case when p_language in ('java','python') then p_language else v_user.language end,
      theme = case when p_theme in ('dark','light') then p_theme else v_user.theme end
  where id = v_user.id
  returning * into v_user;

  return jsonb_build_object(
    'daily_goal', v_user.daily_goal,
    'language', v_user.language,
    'theme', v_user.theme
  );
end;
$$;

-- 6. delete_user
create or replace function delete_user(p_username text, p_pin_hash text)
returns boolean
language plpgsql security definer as $$
declare
  v_user app_users;
begin
  v_user := internal_verify_user(p_username, p_pin_hash);
  delete from app_users where id = v_user.id;
  return true;
end;
$$;

