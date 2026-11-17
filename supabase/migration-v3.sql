-- Chainline 3.0 Database Migration (SRS 3.0 Section 9)
-- Additive migration: safe to run multiple times, loses no existing data.

alter table progress drop constraint if exists progress_question_seq_check;
alter table progress add constraint progress_question_seq_check check (question_seq between 1 and 1000);
alter table reviews drop constraint if exists reviews_question_seq_check;
alter table reviews add constraint reviews_question_seq_check check (question_seq between 1 and 1000);

alter table app_users add column if not exists interview_date date;
alter table app_users add column if not exists interview_company text;

create table if not exists question_stats (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 1000),
  seconds int not null default 0 check (seconds >= 0),
  attempts int not null default 0,
  forgot_count int not null default 0,
  slow boolean not null default false,
  last_at timestamptz not null default now(),
  primary key (user_id, question_seq)
);

create table if not exists user_solutions (
  user_id uuid references app_users(id) on delete cascade,
  question_seq int not null check (question_seq between 1 and 1000),
  language text not null check (language in ('java','python')),
  code text not null default '' check (length(code) <= 20000),
  updated_at timestamptz not null default now(),
  primary key (user_id, question_seq, language)
);

alter table question_stats enable row level security;
alter table user_solutions enable row level security;
revoke all on question_stats, user_solutions from anon, authenticated;

create or replace function get_extras(p_username text, p_pin_hash text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid; v app_users;
begin
  v_id := _auth(p_username, p_pin_hash);
  select * into v from app_users where id = v_id;
  return jsonb_build_object(
    'interview_date', v.interview_date,
    'interview_company', v.interview_company,
    'stats', coalesce((select jsonb_agg(to_jsonb(s) - 'user_id') from question_stats s where s.user_id = v_id), '[]'::jsonb),
    'solutions', coalesce((select jsonb_agg(distinct u.question_seq) from user_solutions u
                           where u.user_id = v_id and length(u.code) > 0), '[]'::jsonb));
end $$;

create or replace function save_stats(p_username text, p_pin_hash text, p_seq int,
  p_add_seconds int, p_new_attempt boolean, p_forgot boolean, p_slow boolean)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  insert into question_stats(user_id, question_seq, seconds, attempts, forgot_count, slow, last_at)
  values (v_id, p_seq, greatest(coalesce(p_add_seconds, 0), 0),
    case when p_new_attempt then 1 else 0 end,
    case when p_forgot then 1 else 0 end,
    coalesce(p_slow, false), now())
  on conflict (user_id, question_seq) do update set
    seconds = question_stats.seconds + greatest(coalesce(p_add_seconds, 0), 0),
    attempts = question_stats.attempts + case when p_new_attempt then 1 else 0 end,
    forgot_count = question_stats.forgot_count + case when p_forgot then 1 else 0 end,
    slow = question_stats.slow or coalesce(p_slow, false),
    last_at = now();
  return jsonb_build_object('ok', true);
end $$;

create or replace function save_user_solution(p_username text, p_pin_hash text, p_seq int,
  p_language text, p_code text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  if p_language not in ('java','python') then raise exception 'BAD_LANGUAGE'; end if;
  if length(coalesce(p_code, '')) > 20000 then raise exception 'CODE_TOO_LONG'; end if;
  insert into user_solutions(user_id, question_seq, language, code, updated_at)
  values (v_id, p_seq, p_language, coalesce(p_code, ''), now())
  on conflict (user_id, question_seq, language) do update set code = excluded.code, updated_at = now();
  return jsonb_build_object('ok', true);
end $$;

create or replace function get_user_solutions(p_username text, p_pin_hash text, p_seq int)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  return coalesce((select jsonb_agg(jsonb_build_object('language', language, 'code', code, 'updated_at', updated_at))
                   from user_solutions where user_id = v_id and question_seq = p_seq), '[]'::jsonb);
end $$;

create or replace function save_interview(p_username text, p_pin_hash text, p_date date, p_company text)
returns jsonb language plpgsql security definer set search_path = public as $$
declare v_id uuid;
begin
  v_id := _auth(p_username, p_pin_hash);
  update app_users set interview_date = p_date, interview_company = nullif(trim(p_company), '') where id = v_id;
  return jsonb_build_object('ok', true);
end $$;

grant execute on function
  get_extras(text, text),
  save_stats(text, text, int, int, boolean, boolean, boolean),
  save_user_solution(text, text, int, text, text),
  get_user_solutions(text, text, int),
  save_interview(text, text, date, text)
to anon;
